---
name: smart-document-parser
description: |
  通过 Smart Document 正式 REST API 上传并解析图片、PDF 和 Office 文档，执行版面检测与 OCR，返回 Markdown 或结构化页面区域。
  当用户要求读取、提取、总结、翻译或分析 png、jpg、jpeg、pdf、doc、docx、ppt、pptx、xls、xlsx 文件中的正文、表格、公式、图片或坐标信息时使用本技能。
---

# Smart Document Parser

通过生产环境 REST API 解析一个本地文档，并按用户需要整理结果。

## 服务配置

- 仅调用 `POST https://connect.zhihuiya.com/rd-llm/v1/documents/doc_parsing`。
- 使用 `multipart/form-data` 上传文件，文件字段名固定为 `file`。
- 使用 `Authorization: Bearer <API_KEY>` 认证。
- 从环境变量 `SMART_DOCUMENT_API_KEY` 读取 API Key。不得在 Skill、脚本、日志或回答中写入、回显或保存真实 Key。
- 不得调用任何 stage 域名，不得改用 `/mcp`，也不得在正式接口失败后回退到 stage 或 MCP。

## 执行前检查

1. 确认用户已提供可读取的本地文件或附件；如果没有可访问的文件，要求用户重新上传或提供有效路径。
2. 确认文件扩展名属于 `png`、`jpg`、`jpeg`、`pdf`、`doc`、`docx`、`ppt`、`pptx`、`xls`、`xlsx`。
3. 确认 `SMART_DOCUMENT_API_KEY` 已设置。若未设置，停止调用并要求用户通过安全的运行环境注入 Key；不要索要用户在聊天中粘贴明文 Key。
4. 选择输出格式：
   - 默认使用 `markdown`，适合阅读、总结、翻译、问答和正文提取。
   - 使用 `jsonl` 获取页码、区域类型、OCR 块、裁剪链接或归一化坐标。
   - 仅在任务同时需要 Markdown 与结构化区域时使用 `both`。

## 调用接口

设置待解析文件的绝对路径并执行一次请求：

```bash
DOCUMENT_PATH="/absolute/path/to/file.pdf"
OUTPUT_FORMAT="markdown"

test -n "${SMART_DOCUMENT_API_KEY:-}" || {
  echo "SMART_DOCUMENT_API_KEY is not set" >&2
  exit 2
}
test -f "$DOCUMENT_PATH" || {
  echo "Document does not exist: $DOCUMENT_PATH" >&2
  exit 2
}

curl --fail-with-body --silent --show-error \
  -X POST "https://connect.zhihuiya.com/rd-llm/v1/documents/doc_parsing" \
  -H "Authorization: Bearer ${SMART_DOCUMENT_API_KEY}" \
  -F "file=@${DOCUMENT_PATH}" \
  -F "output_format=${OUTPUT_FORMAT}"
```

每个文件只调用一次。成功请求可能按解析页数计量；不要为了改变展示方式重复上传同一文件。不要对未修改的失败请求自动重试。

## 处理响应

1. 首先检查 HTTP 状态、顶层 `status` 和 `error_code`。
2. 成功时从 `data` 读取：
   - `markdown`：`output_format=markdown` 或 `both` 时的聚合 Markdown。
   - `results`：`output_format=jsonl` 或 `both` 时的页面区域列表。
   - `total_pages` 与 `file_type`：页数和文件类型元数据。
3. `results[].page` 为从 0 开始的页码；只有结构化结果提供对应证据时才能引用页码或坐标。
4. 按用户任务返回提取、总结、翻译或结构化结果；默认不要倾倒完整 JSON 响应。
5. 保留重要标题、表格、公式和分页信息。不得编造缺失的 OCR、版面区域或页码。

## 失败处理

- `401` 或 `403`：说明 API Key 缺失、无效或无权限，停止调用；不得回显 Key。
- `INVALID_FILE_FORMAT`：要求用户提供受支持且未损坏的文件。
- `FILE_TOO_LARGE`：要求压缩或拆分文件。
- `PDF_PARSE_FAILED`：说明 PDF 可能加密或损坏，要求解密或重新导出。
- `DOCUMENT_CONVERSION_FAILED`：要求重新导出 Office 文件，必要时转为 PDF。
- `GATEWAY_TIMEOUT`：建议拆分文件；只有用户同意后才能重试。
- 其他 `4xx/5xx`：报告 HTTP 状态、`error_code` 和不含凭证的错误信息，不得转调 stage 或 MCP。

## 详细契约

在解释接口参数、响应字段、限制或错误码时，读取 [references/api.md](references/api.md)。
