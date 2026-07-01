---
name: smartlink-ip-workbench
description: |
  Build, update, run, and validate the SmartLink / 智界通 cross-border e-commerce IP HTML workbench. Use when the user asks to modify 智界通-SmartLink智能工作台, 智慧芽跨境电商IP解决方案 pages, MCP-backed patent workflows, competitor patent analysis, listing compliance, infringement complaint/OCR flows, knowledge support search, local HTML saving, localhost preview, or real-time Patsnap/Zhihuiya data linkage in a single-file HTML demo.
---

# SmartLink IP Workbench

## Purpose

Use this skill to maintain the user's single-file HTML workbench for cross-border e-commerce IP scenarios. Keep the page customer-facing, non-technical, and demonstrable: every visible workflow should look like a real product capability, while implementation remains local HTML + local proxy unless the user asks for production integration.

Default working files:

- Main HTML: `/Users/tangmingying/Downloads/智界通-SmartLink智能工作台_本地版_20260527.html`
- Latest copy pattern: `/Users/tangmingying/Downloads/智界通-SmartLink智能工作台_最新版_YYYYMMDD.html`
- Backup folder: `/Users/tangmingying/Downloads/智慧芽HTML自动备份`
- MCP proxy: `/Users/tangmingying/Downloads/AI项目文件库/zhihuiya_mcp_proxy.js`
- Local page server: `http://127.0.0.1:8767/`
- Local proxy server: `http://127.0.0.1:8788/`

## Core Workflow

1. Read the current HTML before editing. Search with `rg` for the exact visible label or function name.
2. Preserve user-facing simplicity. Hide technical process text unless the user explicitly wants it.
3. Make scoped edits with `apply_patch`.
4. Validate with `scripts/verify_html_js.js` or equivalent inline-script syntax check.
5. Run or refresh the page on localhost. Prefer `127.0.0.1:8767` over `file://` when MCP proxy calls are needed.
6. Save every meaningful HTML update to the working file, backup folder, and latest copy.
7. Final response must include exact local file links and the running URL.

## Page Product Rules

- Keep the product name and main workflows clear: 侵权投诉、上架合规、竞品专利分析、知识支撑.
- Avoid exposing "MCP" in visible UI unless the user specifically wants to show MCP.
- Avoid static placeholder rows in sections that claim live data.
- Use the same returned data object to update table, charts, cards, and summaries.
- Changing market must re-query or recompute all dependent views.

## Competitor Patent Analysis

Use when the user asks about 竞品专利分析、申请人检索、雷达图、趋势图、多维度对比表.

- User enters 1-5 competitor/applicant names.
- "开始分析" calls the local proxy `/api/competitor-patent-search`.
- Proxy uses the configured Zhihuiya/Patsnap MCP.
- Target market dropdown: 全部市场=global, 美国=US, 欧盟=EP, WIPO/PCT=WO.
- Radar axes: 专利武器库、外观布局、技术覆盖、申请活跃度、市场壁垒、平台适配.

Read `references/competitor-analysis.md` for implementation details.

## Listing Compliance Workflow

Use for 上架合规、选品专利扫描、图片上传/拖拽、LOC分类、FTO报告.

## Infringement Complaint Workflow

Use for 侵权投诉、通知解读、OCR、投诉平台自动识别、专利号提取、申诉材料.

## Knowledge Support Workflow

Use for 知识支撑、综合文档搜索问答、政策情报、IP知识图谱.

## Local Servers

Start or restart these when needed:

```bash
screen -S zhihuiya_mcp_proxy -X quit >/dev/null 2>&1 || true
screen -dmS zhihuiya_mcp_proxy bash -lc 'cd "/Users/tangmingying/Downloads/AI项目文件库" && node zhihuiya_mcp_proxy.js > /tmp/zhihuiya_mcp_proxy.log 2>&1'

screen -S smartlink_http_8767 -X quit >/dev/null 2>&1 || true
screen -dmS smartlink_http_8767 bash -lc 'cd "/Users/tangmingying/Downloads" && python3 -m http.server 8767 --bind 127.0.0.1 > /tmp/smartlink_http_8767.log 2>&1'
```

## Response Pattern

For completed changes, answer in Chinese and include: what changed, local file path, backup path, running URL, any verification caveat.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
