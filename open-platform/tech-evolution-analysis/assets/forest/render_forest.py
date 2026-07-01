"""TRIZ evolution-forest renderer — case driver (skeleton + tri-state).

This is the THIN, case-specific layer. To use for a new product case you only
edit/supply three things; the rendering core (triz_forest_common.py) is untouched:

  1. PART_NAME  — map each part id (e.g. P1.1 / C4.4) to a human label
  2. --records  — path to that case's triz_relabeled_records_v3.json
  3. --out      — output html path

Usage:
  python render_forest.py --records <relabeled_records_v3.json> --out <forest.html> \
         --title "XX 技术进化森林 · Step 6 v3"

Input JSON shape (triz_relabeled_records_v3.json):
  {"records": [
     {"pn": "...", "route_attr": "P1.1 ...", "core": "...",
      "labels": {"6": {"node": "6.4", "act": "..."}, ...},
      "spawns_new_route": [{"from": 6, "to": 7, "why": "..."}]},
     ...
  ]}

Each active route is drawn as the FULL authoritative skeleton; nodes are
tri-state colored by hit count (已布局≥2 / 稀疏=1 / 空白=0). No node is ever
auto-excluded — gaps anywhere surface as 布局机会.
"""
import argparse, json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import triz_forest_common as C

# ── CASE CONFIG ───────────────────────────────────────────────────────────
# Replace this dict for each new case. Keys are part ids that appear in
# `route_attr`; values are the labels shown as the unit root. The example
# below is the PLC case — overwrite it (or load from a sidecar json) per case.
PART_NAME = {
 "P1.1":"主控SoC","P1.2":"FPGA加速核","P3.1":"IEC61131-3编译器","P4.1":"实时调度内核",
 "P5.1":"DI/DO隔离驱动","P6.1":"模拟前端ADC/DAC","P7.1":"运动控制IC","P8.1":"电源变换",
 "P10.1":"TSN交换芯片","P10.2":"实时以太网协议栈","P13.2":"硬件根信任","P14.1":"SIL双核冗余",
 "P15.1":"NPU加速器","P15.2":"AI模型部署框架","P16.1":"实时Hypervisor",
 "C4.1":"现场总线","C4.4":"OPC UA信息建模",
}
# ──────────────────────────────────────────────────────────────────────────


def primary_part(ra):
    m = re.search(r'([PC]\d+\.\d+)', ra or "")
    if m: return m.group(1)
    cm = re.search(r'(cross_[A-Za-z0-9_]+)', ra or "")
    return cm.group(1) if cm else "其他"


def build_units(recs):
    """recs -> units[part] -> {routes:{route:{hits,rep}}, pns, spawns}."""
    units = defaultdict(lambda: {"routes": defaultdict(lambda: {"hits": defaultdict(int), "rep": {}}),
                                 "pns": set(), "spawns": []})
    for r in recs:
        part = primary_part(r.get("route_attr"))
        u = units[part]; u["pns"].add(r["pn"])
        for rk, lbl in (r.get("labels") or {}).items():
            route = int(rk); pos = lbl["node"]
            ru = u["routes"][route]
            ru["hits"][pos] += 1
            if pos not in ru["rep"]:
                ru["rep"][pos] = {"act": lbl.get("act"), "pn": r["pn"], "core": r.get("core")}
        for sp in (r.get("spawns_new_route") or []):
            u["spawns"].append({"from": sp.get("from"), "to": sp.get("to"),
                                "why": sp.get("why"), "pn": r["pn"]})
    return units


def render_doc(units, n_recs, title):
    order = sorted(units, key=lambda p: (p.startswith("cross"), p))
    blanks_total = sparse_total = 0
    body = []
    for part in order:
        u = units[part]
        name = PART_NAME.get(part, part)
        active_routes = sorted(u["routes"])
        head = (f'<div class="unit"><div class="unit-head"><span class="unit-root">{C.esc(name)}</span>'
                f'<span class="unit-cur">{C.esc(part)} ｜ 活跃路线 {len(active_routes)} 条 ｜ 专利 {len(u["pns"])} 件</span>'
                f'</div><div class="unit-body">')
        seg = [head]
        foot_blank = []; foot_sparse = []
        for route in active_routes:
            ru = u["routes"][route]
            seg.append(C.render_route_skeleton(route, ru["hits"], ru["rep"]))
            for pos, name2 in C.DICT[route]:
                h = ru["hits"].get(pos, 0)
                if h == 0:
                    foot_blank.append(f"路线{route} {pos}·{name2}"); blanks_total += 1
                elif h <= C.SPARSE_MAX:
                    foot_sparse.append(f"路线{route} {pos}·{name2}"); sparse_total += 1
        foot = []
        for sp in u["spawns"]:
            foot.append(f'<span class="tag f">特征·派生</span>路线{sp["from"]}→路线{sp["to"]}: {C.esc(sp["why"])} <i>（{C.esc(sp["pn"])}）</i>')
        if foot_blank:
            foot.append('<span class="tag b">空白机会</span>' + "、".join(foot_blank))
        if foot_sparse:
            foot.append('<span class="tag y">稀疏机会</span>' + "、".join(foot_sparse))
        if foot:
            seg.append('<div class="pt-list">' + "<br>".join(foot) + '</div>')
        seg.append('</div></div>')
        body.append("".join(seg))

    doc = (f'<!doctype html><html lang="zh"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{C.esc(title)}</title><style>{C.CSS}</style></head><body>'
           f'<header><h1>{C.esc(title)}</h1>'
           f'<div class="meta">{len(units)} 个零部件 ｜ {n_recs} 件专利 ｜ 每条活跃路线按权威11路线字典铺满完整节点骨架；'
           f'节点按命中数染三态：已布局(≥2)/稀疏(1)/空白(0)。空白与稀疏不分 tier 前后，均为布局机会，是否真空白需结合市场已有产品判断。</div></header>'
           f'{C.LEGEND}{"".join(body)}</body></html>')
    return doc, blanks_total, sparse_total


def main():
    ap = argparse.ArgumentParser(description="TRIZ evolution-forest renderer (skeleton + tri-state)")
    ap.add_argument("--records", required=True, help="path to triz_relabeled_records_v3.json")
    ap.add_argument("--out", required=True, help="output html path")
    ap.add_argument("--title", default="技术进化森林 · Step 6 v3（完整字典骨架 + 三态空白识别）")
    args = ap.parse_args()

    recs = json.load(open(args.records, encoding="utf-8"))["records"]
    units = build_units(recs)
    doc, blanks_total, sparse_total = render_doc(units, len(recs), args.title)
    open(args.out, "w", encoding="utf-8").write(doc)
    print("parts:", len(units), "| 空白机会:", blanks_total, "| 稀疏机会:", sparse_total)
    print("-> " + args.out)


if __name__ == "__main__":
    main()
