"""
zhihuiya_api.py
===============
智慧芽 PatSnap OpenAPI 标准调用库 —— 服务器滑轨 FTO 分析专用，可独立复用。

涵盖接口（优先使用 skill 内部 query_api_key 配置；也兼容 OAuth）：
  - P070 关键词助手：POST /search/patent/keyword-suggest
  - P002 检索式检索专利：POST /search/patent/query-search-patent/v2
  - P018 专利权利要求：GET /basic-patent-data/claim-data
  - AI07 大模型：POST /chat/cc-gpt-stream

强约束：不得通过外部 MCP、其他 skill 或外部封装调用智慧芽 API。

使用示例：
    from zhihuiya_api import ZhihuiyaClient
    client = ZhihuiyaClient(
        client_id="your_client_id",
        client_secret="your_secret",
    )
    expanded = client.expand_keywords("服务器")
    patents  = client.search_all_patents("TAC_ALL:(服务器) AND IPC:(A47B88/)", max_total=500)
    claims   = client.get_claims("CN105078033B")
"""

from __future__ import annotations

import base64
import html
import json
import logging
import re
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)

# ── 基础 URL ─────────────────────────────────────────────────────────────────
BASE_URL  = "https://connect.zhihuiya.com"
TOKEN_URL = f"{BASE_URL}/oauth/token"

# 业务接口路径
P002_PATH = "/search/patent/query-search-patent/v2"
P070_PATH = "/search/patent/keyword-suggest"
P018_PATH = "/basic-patent-data/claim-data"
AI07_PATH = "/chat/cc-gpt-stream"
P025_PATH = "/high-value-data/tech-problem-and-benefit-summary"  # P018 降级备选


def _strip_claim_html(text: str) -> str:
    """将 P018 claim-data 返回的 HTML 片段转为纯文本。"""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return re.sub(r"\s+", "", text).strip()


class ZhihuiyaApiError(RuntimeError):
    """智慧芽接口业务错误（status=false）"""

    def __init__(self, endpoint: str, error_code: Any, error_msg: str):
        self.endpoint   = endpoint
        self.error_code = error_code
        self.error_msg  = error_msg
        super().__init__(f"{endpoint} 失败：{error_msg} (code={error_code})")


class ZhihuiyaClient:
    """智慧芽 OpenAPI 统一客户端（OAuth 鉴权）"""

    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        api_key: str = "",
        base_url: str = BASE_URL,
        timeout: int = 60,
    ):
        """
        Parameters
        ----------
        client_id     : P002/P070/P018 OAuth 用的 Client ID
        client_secret : P002/P070/P018 OAuth 用的 Client Secret
        timeout       : 请求超时秒数
        """
        self.client_id     = client_id
        self.client_secret = client_secret
        self.api_key       = api_key or client_id
        self.base_url      = base_url.rstrip("/")
        self.timeout       = timeout
        self._token: str           = ""
        self._token_expire_at: float = 0.0

    # ── Token 管理 ───────────────────────────────────────────────────────────

    def _get_token(self) -> str:
        """返回有效的 Bearer token，过期/即将过期时自动续期（提前 60s）"""
        if self._token and time.time() < self._token_expire_at - 60:
            return self._token

        if not self.client_id or not self.client_secret:
            raise ValueError("client_id 和 client_secret 不能为空")

        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        resp = requests.post(
            TOKEN_URL,
            headers={
                "Content-Type":  "application/x-www-form-urlencoded",
                "Authorization": f"Basic {credentials}",
            },
            data={"grant_type": "client_credentials"},
            timeout=30,
        )
        resp.raise_for_status()
        data      = resp.json()
        token_obj = data.get("data") if isinstance(data.get("data"), dict) else data
        if not token_obj or "token" not in token_obj:
            raise RuntimeError(f"获取 OAuth token 失败：{data}")
        self._token            = token_obj["token"]
        self._token_expire_at  = time.time() + int(token_obj.get("expires_in", 1799))
        logger.debug("OAuth token 已刷新，有效期 %s 秒", token_obj.get("expires_in"))
        return self._token

    def _headers(self) -> dict:
        """通用请求头（OAuth token）"""
        return {
            "Authorization":   f"Bearer {self._get_token()}",
            "Content-Type":    "application/json",
            "X-PatSnap-Version": "1.0",
        }

    def _post(self, path: str, payload: dict) -> dict:
        """POST 业务接口；附带 apikey query 参数"""
        url    = f"{self.base_url}{path}"
        params = {"apikey": self.api_key}
        resp = requests.post(
            url,
            headers=self._headers() if self.client_id and self.client_secret else {"Content-Type": "application/json", "X-PatSnap-Version": "1.0"},
            params=params,
            json=payload,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        try:
            data = resp.json()
        except ValueError:
            return {"raw_text": resp.text}
        if data.get("status") is False:
            raise ZhihuiyaApiError(path, data.get("error_code"), data.get("error_msg"))
        return data.get("data", {}) or {}

    def _get(self, path: str, params: dict | None = None) -> dict:
        """GET 业务接口；附带 apikey query 参数"""
        url        = f"{self.base_url}{path}"
        all_params = {"apikey": self.api_key}
        if params:
            all_params.update(params)
        resp = requests.get(
            url,
            headers=self._headers() if self.client_id and self.client_secret else {"Content-Type": "application/json", "X-PatSnap-Version": "1.0"},
            params=all_params,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") is False:
            raise ZhihuiyaApiError(path, data.get("error_code"), data.get("error_msg"))
        return data.get("data", {}) or {}

    # ── P070 关键词助手 ──────────────────────────────────────────────────────

    def expand_keywords(
        self,
        keyword: str,
        lang: list[str] | None = None,
        types: list[str] | None = None,
        max_words: int = 20,
    ) -> list[str]:
        """
        调用 P070 关键词助手，返回扩展后的关键词列表（含原词）。

        Parameters
        ----------
        keyword   : 单个关键词或短语
        lang      : 输出语言，['cn'] / ['en'] / ['cn','en']，默认 ['cn']
        types     : 扩展类型，可选 'synonym'(同义词) / 'related'(相关词) / 'hypernym'(下位词)
                    默认 ['synonym', 'related']
        max_words : 最多返回多少个扩展词（含原词）

        Returns
        -------
        list[str]：[原词, 同义词1, 同义词2, ...]，已去重保序
        """
        payload = {
            "keyword": [keyword],
            "lang":    lang  or ["cn"],
            "type":    types or ["synonym", "related"],
        }
        try:
            data = self._post(P070_PATH, payload)
        except (ZhihuiyaApiError, requests.HTTPError, requests.RequestException) as exc:
            logger.warning("P070 调用失败 [%s]：%s，使用原词降级", keyword, exc)
            return [keyword]

        result: list[str] = [keyword]
        for item in data.get("items", []) or []:
            for kw_obj in item.get("keyword_list", []) or []:
                w = (kw_obj.get("keyword") or "").strip()
                if w and w != keyword and w not in result:
                    result.append(w)
        return result[:max_words]

    # ── P002 检索式检索专利 ──────────────────────────────────────────────────

    def search_patents(
        self,
        query_text: str,
        limit: int = 100,
        offset: int = 0,
        sort_field: str = "SCORE",
        sort_order: str = "DESC",
        collapse_by: str = "PBD",
        collapse_type: str = "ALL",
        collapse_order: str = "LATEST",
        collapse_order_authority: list[str] | None = None,
    ) -> dict:
        payload = {
            "query_text":              query_text,
            "limit":                   limit,
            "offset":                  offset,
            "stemming":                0,
            "sort":                    [{"field": sort_field, "order": sort_order}],
            "collapse_by":             collapse_by,
            "collapse_type":           collapse_type,
            "collapse_order":          collapse_order,
            "collapse_order_authority": collapse_order_authority or ["CN", "US", "EP", "JP", "KR"],
        }
        return self._post(P002_PATH, payload)

    def search_all_patents(
        self,
        query_text: str,
        page_size: int = 100,
        max_total: int = 500,
    ) -> list[dict]:
        """
        分页拉取检索式所有命中专利。

        Fix #2：新增 max_total 参数（默认 500），到达上限后停止翻页并记录警告，
        防止大结果集无限翻页导致超时或内存耗尽。
        上限同时受 API 20000 条硬限制约束（取两者较小值）。
        """
        hard_limit = min(max_total, 20000)
        out: list[dict] = []
        offset = 0
        while True:
            data  = self.search_patents(query_text, limit=page_size, offset=offset)
            batch = data.get("results", []) or []
            out.extend(batch)
            total  = data.get("total_search_result_count", 0)
            offset += len(batch)
            logger.debug("P002 已获取 %d / %d 条（上限 %d）", offset, total, hard_limit)
            if not batch or offset >= total:
                break
            if offset >= hard_limit:
                logger.warning(
                    "P002 已达 max_total=%d 上限，停止翻页（实际总量 %d 条）",
                    hard_limit, total,
                )
                break
        return out

    # ── P018 专利权利要求 ────────────────────────────────────────────────────

    def get_claims(self, patent_number: str) -> list[str]:
        """
        调用 P018 获取专利权利要求列表。

        Parameters
        ----------
        patent_number : 专利公开号，如 "CN105078033B"

        Returns
        -------
        list[str]：权利要求文本列表（按 claim_num 排序），失败返回空列表。
                   通常取 [0] 即为独立权利要求1。
        """
        try:
            data = self._get(P018_PATH, {"patent_number": patent_number, "replace_by_related": 0})
        except ZhihuiyaApiError as exc:
            logger.warning("P018 [%s] 调用失败：%s", patent_number, exc)
            return []
        except (requests.HTTPError, requests.RequestException) as exc:
            logger.warning("P018 [%s] 网络异常：%s", patent_number, exc)
            return []

        # 正确响应结构：data[0].claims[0].claim_text 中包含 num="1" 的 HTML 片段。
        # 兼容旧格式。
        claims_raw = []
        if isinstance(data, list) and data and isinstance(data[0], dict) and data[0].get("claims"):
            claims_raw = data[0].get("claims", []) or []
        elif isinstance(data, dict):
            claims_raw = data.get("claims", []) or []
        elif isinstance(data, list):
            claims_raw = data

        if not claims_raw:
            logger.warning("P018 [%s] 返回空权利要求", patent_number)
            return []

        # 按 claim_num 排序
        try:
            claims_raw.sort(
                key=lambda x: int(x.get("claim_num", 0)) if isinstance(x, dict) else 0
            )
        except Exception:
            pass

        result = []
        for c in claims_raw:
            if isinstance(c, dict):
                text = c.get("claim_text") or c.get("text") or ""
                text = _strip_claim_html(text)
            else:
                text = str(c)
            if text.strip():
                result.append(text.strip())

        logger.info("P018 [%s] 获取到 %d 条权利要求", patent_number, len(result))
        return result

    def call_ai07(self, prompt: str, stream: bool = True) -> dict:
        """调用 AI07 CC GPT。仅作为辅助记录；最终 FTO 结论以 P018 权利要求结构化比对为准。"""
        data = self._post(AI07_PATH, {"prompt": prompt[:500], "stream": stream})
        if "raw_text" not in data:
            return data
        chunks: list[str] = []
        for match in re.finditer(r"data:(\{.*?\})(?=\s*data:|$)", data["raw_text"], flags=re.S):
            try:
                obj = json.loads(match.group(1))
                content = (((obj.get("data") or {}).get("output") or {}).get("content") or "")
                if content:
                    chunks.append(content)
            except Exception:
                continue
        return {"content": "".join(chunks).strip(), "raw_text": data["raw_text"]}

    def get_claims_batch(self, patent_numbers: list[str]) -> dict[str, list[str]]:
        """批量获取多条专利的权利要求，返回 {pn: [claim_text, ...]} 字典"""
        results: dict[str, list[str]] = {}
        for pn in patent_numbers:
            results[pn] = self.get_claims(pn)
            time.sleep(0.2)  # 避免 QPS 超限
        return results

    # ── P025 技术三要素（P018 降级备选）─────────────────────────────────────
    # Fix #3：明确标注本方法为"P018 无权限时的降级方案"，主流程不调用此方法

    def get_tech_summary(self, patent_number: str) -> dict:
        """
        [降级备选] P018 无权限（error_code=67200004）时改用 P025 技术三要素。

        ⚠️ 本方法不在主流程中自动调用。
           仅在 P018 开通前作为临时替代方案，需手动在 fto_main.py 中切换。
           P025 注入字段（cc_pids 等）为非官方参数，服务端可能忽略。

        Returns
        -------
        dict 结构：
        {
            "pn":           "CN104939545B",
            "title":        "...",
            "tech_problem": [...],
            "tech_approach": [...],
            "benefit":      [...],
        }
        失败返回空 dict。
        """
        try:
            data = self._get(P025_PATH, {"patent_number": patent_number})
        except Exception as exc:
            logger.warning("P025 [%s] 调用异常: %s", patent_number, exc)
            return {}

        if not data:
            return {}

        item = data[0] if isinstance(data, list) else data
        return {
            "pn":           patent_number,
            "patent_id":    item.get("patent_id", ""),
            "title":        item.get("patsnap_title", ""),
            "tech_problem": (item.get("tech_problem_summary") or {}).get("tech_problem_para", []),
            "tech_approach":(item.get("technical_approach_summary") or {}).get("technical_approach_para", []),
            "benefit":      (item.get("benefit_summary") or {}).get("benefit_para", []),
        }
