import json
import re
import urllib.error
import urllib.request
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent
CONFIG = Path.home() / ".codex" / "config.toml"
PHASES = ["phase_3", "phase_4", "nda_bla", "approved"]


def read_mcp_url(name):
    text = CONFIG.read_text(encoding="utf-8-sig")
    pattern = r'(?s)\[mcp_servers\.' + re.escape(name) + r'\].*?url\s*=\s*"([^"]+)"'
    match = re.search(pattern, text)
    if not match:
      raise RuntimeError(f"MCP server {name} not found in {CONFIG}")
    return match.group(1)


PHARMA_MCP = read_mcp_url("zhihuiya_logic_096456")
PATENT_MCP = read_mcp_url("zhihuiya_logic_2b0355")
DRUG_TYPE_MAP = {
    "Small molecule drug": "小分子化药",
    "Monoclonal antibody": "单克隆抗体",
    "ADC": "ADC",
    "Biological product": "生物制品",
    "Gene therapy": "基因治疗",
}


def mcp_call(url, tool, arguments, request_id=1, timeout=90):
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    match = re.search(r"data:\s*(\{.*\})", raw, re.S)
    body = json.loads(match.group(1) if match else raw)
    if "error" in body:
        raise RuntimeError(body["error"].get("message", "MCP error"))
    content = body.get("result", {}).get("content", [])
    if not content:
        return {}
    text = content[0].get("text", "{}")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"text": text}


def normalize_date(value):
    if not value:
        return None
    digits = re.sub(r"\D", "", str(value))
    if len(digits) >= 8:
        return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
    if len(digits) == 6:
        return f"{digits[:4]}-{digits[4:6]}"
    if len(digits) == 4:
        return digits
    return str(value)


def parse_estimated_expiry(markdown):
    if not markdown:
        return None
    match = re.search(r"Estimated Expiry Date\s*\n+\s*([0-9]{4,8})", markdown)
    if match:
        return normalize_date(match.group(1))
    return None


def fetch_expiry_by_pn(pn):
    if not pn:
        return None
    try:
        data = mcp_call(
            PATENT_MCP,
            "patsnap_fetch",
            {
                "keys": [pn],
                "key_type": "pn",
                "compress": False,
                "include_images": False,
                "module": ["basic", "legal"],
                "include_structured": True,
            },
            request_id=300,
        )
    except Exception:
        return None
    for result in data.get("results", []):
        expiry = parse_estimated_expiry(result.get("markdown", ""))
        if expiry:
            return expiry
        structured = result.get("structured") or {}
        basic = structured.get("basic") or {}
        legal = structured.get("legal") or {}
        for container in (basic, legal):
            text = json.dumps(container, ensure_ascii=False)
            match = re.search(r'"exdt"\s*:\s*"?([0-9]{8})"?', text)
            if match:
                return normalize_date(match.group(1))
    return None


def verify_drug(drug_name, country, drug_type):
    try:
        data = mcp_call(
            PHARMA_MCP,
            "ls_drug_search",
            {
                "drug": [drug_name],
                "drug_type": [drug_type],
                "highest_phase": PHASES,
                "country": [country],
                "limit": 5,
                "offset": 0,
            },
            request_id=200,
        )
    except Exception:
        data = {"total": 0, "items": []}
    if not data.get("items"):
        try:
            data = mcp_call(
                PHARMA_MCP,
                "ls_drug_search",
                {
                    "drug": [drug_name],
                    "drug_type": [drug_type],
                    "highest_phase": PHASES,
                    "limit": 5,
                    "offset": 0,
                },
                request_id=201,
            )
        except Exception:
            data = {"total": 0, "items": []}
    item = (data.get("items") or [None])[0]
    if not item:
        return None
    return {
        "drug_id": item.get("drug_id"),
        "name_cn": item.get("display_name_cn") or drug_name,
        "name_en": item.get("display_name_en") or drug_name,
        "drug_type": DRUG_TYPE_MAP.get(drug_type, drug_type),
        "phase": "Approved" if item.get("first_approved_date") else "Phase 3+",
        "first_approved_date": item.get("first_approved_date"),
    }


def search_compound_patent(drug_name, country):
    levels = [
        ("CN exact parent/product-compound", {"country": [country]}),
        ("Global exact parent/product-compound", {}),
    ]
    for level, extra in levels:
        args = {
            "drug": [drug_name],
            "patent_core_type": ["product_compound"],
            "limit": 5,
            "offset": 0,
        }
        args.update(extra)
        try:
            data = mcp_call(PHARMA_MCP, "ls_patent_search", args, request_id=250)
        except Exception:
            continue
        items = data.get("items") or []
        if items:
            item = items[0]
            pn = item.get("pn")
            return {
                "pn": pn,
                "title": item.get("title"),
                "assignee": assignee_name(item),
                "expiry": fetch_expiry_by_pn(pn) or "未返回估算到期日",
                "match_level": level,
            }
    return {
        "pn": "未检索到",
        "title": "",
        "assignee": "",
        "expiry": "未检索到",
        "match_level": "Not found",
    }


def assignee_name(item):
    assignees = item.get("current_assignee") or []
    if not assignees:
        return ""
    first = assignees[0]
    return first.get("display_name_cn") or first.get("display_name_en") or ""


def month_delta(start, end):
    if not start or not end or "未" in start or "未" in end:
        return "无法计算"
    try:
        a = date.fromisoformat(start[:10])
        b = date.fromisoformat(end[:10])
    except ValueError:
        return "无法计算"
    months = (b.year - a.year) * 12 + (b.month - a.month)
    if b.day < a.day:
        months -= 1
    return f"{months:+d} 月"


def build_report(params):
    country = params.get("country") or "CN"
    drug_type = params.get("drug_type") or "Small molecule drug"
    date_from = params.get("date_from") or date.today().isoformat()
    date_to = params.get("date_to") or f"{date.today().year + 5}-{date.today().month:02d}-{date.today().day:02d}"
    retrieval_cap = max(1, min(int(params.get("retrieval_cap") or 100), 1000))
    page_size = min(retrieval_cap, 100)

    patent_args = {
        "drug_type": [drug_type],
        "patent_core_type": ["crystal_form"],
        "legal_status": ["active", "pending"],
        "country": [country],
        "expiry_date_from": date_from,
        "expiry_date_to": date_to,
        "offset": 0,
        "limit": page_size,
    }
    patent_data = mcp_call(PHARMA_MCP, "ls_patent_search", patent_args, request_id=100)
    patent_items = patent_data.get("items") or []

    rows = []
    not_promoted = []
    seen_drugs = set()
    processed_patents = 0
    for patent in patent_items:
        processed_patents += 1
        detail = {}
        try:
            fetched = mcp_call(
                PHARMA_MCP,
                "ls_patent_fetch",
                {"patent_ids": [patent["id"]]},
                request_id=110,
            )
            detail = (fetched.get("result") or [{}])[0]
        except Exception:
            detail = {}

        linked = detail.get("drug_id_view") or []
        if not linked:
            not_promoted.append({
                "candidate": patent.get("title") or patent.get("pn"),
                "reason": "未返回结构化药物回连",
                "missing": "drug_id_view",
            })
            continue

        for drug in linked:
            drug_name = drug.get("display_name_en") or drug.get("display_name_cn")
            if not drug_name or drug_name in seen_drugs:
                continue
            verified = verify_drug(drug_name, country, drug_type)
            if not verified:
                not_promoted.append({
                    "candidate": drug.get("display_name_cn") or drug_name,
                    "reason": "阶段或药物类型未通过验证",
                    "missing": f"{drug_type} + Phase 3+",
                })
                continue

            seen_drugs.add(drug_name)
            crystal_pn = patent.get("pn")
            crystal_expiry = fetch_expiry_by_pn(crystal_pn) or "未返回估算到期日"
            compound = search_compound_patent(verified["name_en"], country)
            delta = month_delta(compound.get("expiry"), crystal_expiry)
            rows.append({
                "drug_name": f'{verified["name_cn"]} / {verified["name_en"]}',
                "drug_type": verified["drug_type"],
                "phase": verified["phase"],
                "assignee": assignee_name(patent),
                "compound_expiry": compound.get("expiry"),
                "crystal_expiry": crystal_expiry,
                "delta": delta,
                "match_level": compound.get("match_level"),
                "compound_patent": compound.get("pn"),
                "crystal_patent": crystal_pn,
                "notes": crystal_note(patent),
            })
            break

    return {
        "params": {
            "country": country,
            "drug_type": drug_type,
            "drug_type_label": DRUG_TYPE_MAP.get(drug_type, drug_type),
            "date_from": date_from,
            "date_to": date_to,
            "retrieval_cap": retrieval_cap,
        },
        "summary": {
            "total_crystal_hits": patent_data.get("total", 0),
            "retrieved": len(patent_items),
            "processed_patents": processed_patents,
            "promoted": len(rows),
            "not_promoted": len(not_promoted),
            "complete": (patent_data.get("total", 0) <= len(patent_items)),
        },
        "rows": rows,
        "not_promoted": not_promoted[:20],
    }


def crystal_note(patent):
    content = patent.get("content") or ""
    flags = []
    for word in ["X-射线", "XRD", "衍射", "晶型", "晶体", "DSC", "TGA"]:
        if word.lower() in content.lower():
            flags.append(word)
    if flags:
        return "晶型证据：" + "、".join(dict.fromkeys(flags[:4]))
    return "晶型类型来自数据库标引，建议复核专利原文"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/":
            path = "/index.html"
        file_path = (ROOT / path.lstrip("/")).resolve()
        if not str(file_path).startswith(str(ROOT)) or not file_path.exists():
            self.send_error(404)
            return
        content_types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
        }
        content_type = content_types.get(file_path.suffix.lower(), "application/octet-stream")
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != "/api/search":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        params = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        try:
            result = build_report(params)
            status = 200
        except Exception as exc:
            result = {"error": str(exc)}
            status = 500
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8790), Handler)
    print("Generic patent expiry scout running at http://127.0.0.1:8790")
    server.serve_forever()
