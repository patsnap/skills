---
name: smartlink-ip-workbench
description: 构建、更新、运行并验证 SmartLink / 智界通跨境电商知识产权 HTML 工作台。适用于用户要求修改智界通-SmartLink智能工作台、智慧芽跨境电商 IP 解决方案页面、由 MCP 支撑的专利工作流、竞品专利分析、上架合规、侵权投诉/OCR 流程、知识支撑检索、本地 HTML 保存、localhost 预览，或在单文件 HTML 演示中接入实时 Patsnap/智慧芽数据的场景。
---

# SmartLink IP 工作台

## 目标

使用本 Skill 维护用户面向跨境电商知识产权场景的单文件 HTML 工作台。页面应保持客户可见、非技术化、可演示：每一个可见工作流都应呈现为真实产品能力，同时实现方式仍保持为本地 HTML + 本地代理，除非用户明确要求生产级集成。

默认工作文件：

- 主 HTML：`/Users/tangmingying/Downloads/智界通-SmartLink智能工作台_本地版_20260527.html`
- 最新副本命名规则：`/Users/tangmingying/Downloads/智界通-SmartLink智能工作台_最新版_YYYYMMDD.html`
- 备份文件夹：`/Users/tangmingying/Downloads/智慧芽HTML自动备份`
- MCP 代理：`/Users/tangmingying/Downloads/AI项目文件库/zhihuiya_mcp_proxy.js`
- 本地页面服务：`http://127.0.0.1:8767/`
- 本地代理服务：`http://127.0.0.1:8788/`

## 核心工作流

1. 编辑前先读取当前 HTML。用 `rg` 搜索精确的可见标签或函数名。
2. 保持面向用户的简单表达。除非用户明确要求展示，否则隐藏技术流程文字。
3. 使用 `apply_patch` 做范围明确的编辑。
4. 使用 `scripts/verify_html_js.js` 或等效的内联脚本语法检查进行验证。
5. 在 localhost 上运行或刷新页面。需要调用 MCP 代理时，优先使用 `127.0.0.1:8767`，不要使用 `file://`。
6. 每次有意义的 HTML 更新都保存到工作文件、备份文件夹和最新版副本。
7. 最终回复必须包含精确的本地文件链接和运行 URL。

## 页面产品规则

- 保持产品名称和主工作流清晰：侵权投诉、上架合规、竞品专利分析、知识支撑。
- 除非用户特别希望展示 MCP，否则不要在可见 UI 中暴露“MCP”。
- 对声称使用实时数据的区块，避免使用静态占位行。
- 使用同一个返回数据对象更新表格、图表、卡片和摘要。
- 切换市场后，必须重新查询或重新计算所有依赖视图。

## 竞品专利分析

当用户询问竞品专利分析、申请人检索、雷达图、趋势图、多维度对比表时使用。

- 用户输入 1-5 个竞品/申请人名称。
- “开始分析”调用本地代理 `/api/competitor-patent-search`。
- 代理使用已配置的智慧芽/Patsnap MCP。
- 目标市场下拉项：全部市场=global，美国=US，欧盟=EP，WIPO/PCT=WO。
- 雷达图轴：专利武器库、外观布局、技术覆盖、申请活跃度、市场壁垒、平台适配。

实现细节请读取 `references/competitor-analysis.md`。

## 上架合规工作流

用于上架合规、选品专利扫描、图片上传/拖拽、LOC 分类、FTO 报告。

## 侵权投诉工作流

用于侵权投诉、通知解读、OCR、投诉平台自动识别、专利号提取、申诉材料。

## 知识支撑工作流

用于知识支撑、综合文档搜索问答、政策情报、IP 知识图谱。

## 本地服务

需要时启动或重启以下服务：

```bash
screen -S zhihuiya_mcp_proxy -X quit >/dev/null 2>&1 || true
screen -dmS zhihuiya_mcp_proxy bash -lc 'cd "/Users/tangmingying/Downloads/AI项目文件库" && node zhihuiya_mcp_proxy.js > /tmp/zhihuiya_mcp_proxy.log 2>&1'

screen -S smartlink_http_8767 -X quit >/dev/null 2>&1 || true
screen -dmS smartlink_http_8767 bash -lc 'cd "/Users/tangmingying/Downloads" && python3 -m http.server 8767 --bind 127.0.0.1 > /tmp/smartlink_http_8767.log 2>&1'
```

## 回复模式

完成修改后，用中文回答，并包含：修改内容、本地文件路径、备份路径、运行 URL，以及任何验证注意事项。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
