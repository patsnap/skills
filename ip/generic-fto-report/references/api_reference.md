# 智慧芽 PatSnap OpenAPI 浓缩参考（FTO skill 专用）

排错速查清单。当 `scripts/zhihuiya_api.py` 报错或返回异常时，先来这里对照官方契约。

## 1. 鉴权（skill 内部固定方式）

本 skill 的智慧芽调用必须由 skill 内部脚本完成，不得调用外部 MCP、其他 skill 或外部临时脚本。

默认配置文件：

```text
references/zhihuiya_config.json
```

当前默认使用 `query_api_key` 模式：所有业务接口在 query 参数中传入 `apikey=<zhihuiya_api_key>`。

对外分享版中的 `references/zhihuiya_config.json` 不包含真实 API key。安装后先将：

```json
"zhihuiya_api_key": "PUT_YOUR_ZHIHUIYA_API_KEY_HERE"
```

替换为安装用户自己的智慧芽 API key。

OAuth Client Credentials 仅作为兼容模式保留，非默认路径。

## 1.1 OAuth 兼容模式

```
POST https://connect.zhihuiya.com/oauth/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic base64(<client_id>:<client_secret>)
Body: grant_type=client_credentials
```

返回：
```json
{ "token": "<bearer>", "token_type": "BearerToken", "expires_in": 1799, "status": "approved" }
```

业务接口请求格式（**全部接口都按此格式**）：
- 请求头：`Authorization: Bearer <token>`、`Content-Type: application/json`、`X-PatSnap-Version: 1.0`
- query 参数：`apikey=<client_id>`（**必填，否则返回 67200008**）

> **关键澄清**：早期 FTO skill 草案里的 "AI66 用 sk- 格式 API Key"是错的。所有接口共用同一套 OAuth + apikey query 参数。

## 2. P070 关键词助手

```
POST /search/patent/keyword-suggest?apikey=<client_id>
```

请求体（注意 `keyword`、`lang`、`type` 都是**数组**）：
```json
{
  "keyword": ["服务器"],
  "lang": ["cn"],
  "type": ["synonym", "related"]
}
```

`type` 可选值：
- `synonym` — 同/近义词（"清洁能源" ↔ "绿色能源"）
- `related` — 相关词（"绿色能源" ↔ "温室气体"）
- `hypernym` — 下位词（"风能" 是 "绿色能源" 的下位词）

成功响应：
```json
{
  "data": {
    "items": [
      { "input": "服务器",
        "keyword_list": [{"keyword":"伺服器"},{"keyword":"服务端"}, ...]
      }
    ]
  },
  "status": true,
  "error_code": 0
}
```

## 3. P002 检索式检索专利

```
POST /search/patent/query-search-patent/v2?apikey=<client_id>
```

请求体核心字段：
```json
{
  "query_text": "TAC_ALL:(服务器) AND IPC:(A47B88/) AND ...",
  "limit": 1000,
  "offset": 0,
  "sort": [{"field":"SCORE","order":"DESC"}],
  "stemming": 0
}
```

约束：`limit + offset ≤ 20000`。检索式语法见 https://analytics.zhihuiya.com/search_helper。

返回 `data.results[]`：含 `patent_id` / `pn` / `title` / `current_assignee` / `pbdt` 等字段。

## 4. P018 权利要求

必须使用：

```text
GET /basic-patent-data/claim-data?apikey=<api_key>&patent_number=<PN>&replace_by_related=0
```

不要使用旧路径 `/basic-patent-data/claims`，该路径可能返回无权限或配额错误。

返回结构通常为：

```json
{
  "status": true,
  "data": [
    {
      "pn": "CN112386025B",
      "claim_count": 19,
      "claims": [
        {
          "lang": "CN",
          "data_format": "original",
          "claim_independent_count": 3,
          "claim_text": "<div class=\"indep-clm\" num=\"1\">...</div>"
        }
      ]
    }
  ]
}
```

`claim_text` 是 HTML 片段，脚本需按 `num="1"` 提取权利要求1并去除标签。

## 5. AI07 大模型（CC GPT）

必须使用：

```text
POST /chat/cc-gpt-stream?apikey=<api_key>
```

请求体：

```json
{ "prompt": "...", "stream": true }
```

注意：
- prompt 最大长度约 500 字。
- AI07 仅作为辅助记录，可能将“风险”误解为产品工程风险。
- 报告结论以 P018 权利要求1结构化比对为准；AI07 原始输出保存在 `fto_structured_data.json`。

## 6. AI66 防侵权检索接口（FTO Agent 子任务）

整条 AI66 链路（智慧芽内部 8 步）：

| 步骤 | 路径 | 输入 | 输出 |
|---|---|---|---|
| AI66-1 创建任务 | `POST /ai/fto/submit` | input(技术描述) + lang | task_id |
| AI66-2 提取技术特征 | `POST /ai/fto/feature` | task_id | tech_features 列表 |
| AI66-3 确认技术特征 | `POST /ai/fto/feature/confirm` | task_id + tech_features | task_id |
| AI66-4 启动 FTO 检索 | `POST /ai/fto/search/agent` | task_id | task_id |
| AI66-5 获取检索结果 | `POST /ai/fto/search/agent/result` | task_id | final_result + 元数据 |
| AI66-6 创建报告 | `POST /ai/fto/report/create` | task_id + title + final_res(1-5) | report_task_id |
| AI66-7 下载报告 | `POST /ai/fto/report/get` | task_id | report_url（status=2 时） |
| AI66-8 添加对比文献/专利 | （未在本 skill 使用） | — | — |

### 本 skill 实际只用 1 / 5 / 6 / 7

理由：用户希望用 P002 自定义检索式（按川湖科技 + IPC + 法律状态过滤）替代 AI66-2/3/4 的内置 Agent 检索。

#### AI66-1 请求/响应

请求：
```json
{ "lang": "cn", "input": "<标的产品技术描述全文>",
  "country": ["CN","US","EP"], "legal_status": [1, 2] }
```
响应：`data.task_id`

#### AI66-5 请求/响应（关键）

官方文档示例只列：
```json
{ "task_id": "<task_id>" }
```

我们注入 P002 清单的方式（按响应字段反推）：
```json
{ "task_id": "<task_id>", "cc_pids": ["pid1", "pid2", ...] }
```

> **如果 cc_pids 字段被服务端忽略**：返回的 final_result 可能是 Agent 自己检索的结果。`zhihuiya_api.py:ai66_get_result_with_patents` 已加客户端二次过滤——若 final_result 里有任何 patent_id 落在 cc_pids 集合内则保留这部分；否则保留原 final_result（避免清空）。

异步轮询：响应 `data.task_status` ∈ {`running`, `success`, `failed`}。`success` 时停止；最大等待秒数默认 900s。

成功时 final_result 每条核心字段（输给 AI66-6 用）：
```
patent_id, lang, claims[], document, features[],
risk_level (High/Medium/Low), public_score, feature_match_num,
claim_equivalent_info[{claim_num, infringement}],
comparison_conclusion{en,zh},
selected, user_added, most_similar,
independent_claim_num, dependent_claim_num,
comparative_literature_type,
equivalent_independent_claim_num, equivalent_dependent_claim_num
```

#### AI66-6 请求/响应

请求：
```json
{
  "task_id": "<task_id>",
  "title": "...",
  "final_res": [ /* 选中的 1-5 条 final_result，需要带 selected:true 和 claim_equivalent_info */ ]
}
```

> 限制：`final_res` 数量必须 1-5。`zhihuiya_api.py:ai66_create_report` 会在数量越界时直接抛错。

响应：`data.task_id`（这是 report_task_id，传给 AI66-7）

#### AI66-7 请求/响应

请求：`{ "task_id": "<report_task_id>" }`
响应：`data.status` ∈ {1=执行中, 2=完成, 3=失败}；`status=2` 时 `data.report_url` 可用。

## 5. 常见错误码

| 错误码 | 含义 | 处置 |
|---|---|---|
| 67200003 | Client ID/Secret 错或客户端被禁用 | 查凭证 |
| 67200004 | 接口无权限 | 联系智慧芽客户经理开通 |
| 67200005 | 余额/调用次数不足 | 充值 |
| 67200008 | 必填的 apikey 没传 | 检查 query 参数（脚本已自动加） |
| 67200009 | apikey 与 token 不匹配 | 检查 token 是否过期 |
| 68300004 | 参数异常 | 看 error_msg；常见是 final_res 数量越界 / 字段缺失 |
| 67200002 | QPS 超限 | 加 sleep 重试 |

## 6. fallback：完整 AI66-2/3/4 流程

如果 AI66-5 的 `cc_pids` 注入完全失效（例如服务端版本变更），改走完整链路：

```python
task_id = client.ai66_create_task(product_desc)

# AI66-2 提取技术特征
features = client._post("/ai/fto/feature", {"task_id": task_id})  # data.tech_features

# AI66-3 确认特征（直接全部 is_select=True 即可）
for f in features.get("tech_features", []):
    f["is_select"] = True
client._post("/ai/fto/feature/confirm", {"task_id": task_id, "tech_features": features["tech_features"]})

# AI66-4 启动 Agent 检索
client._post("/ai/fto/search/agent", {"task_id": task_id})

# AI66-5 拿结果（不带 cc_pids），然后客户端用 P002 清单过滤 final_result
result = client.ai66_get_result_with_patents(task_id, patent_ids=[], poll_interval=15, max_wait=1800)
pid_set = {p["patent_id"] for p in p002_patent_list if p.get("patent_id")}
result["final_result"] = [r for r in result.get("final_result", []) if r["patent_id"] in pid_set]
```

记得 AI66-2/3/4 都是同步的，AI66-5 是异步轮询。
