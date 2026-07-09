---
name: generic-drug-scout
description: 运行仿药速探 V1，创建用于仿制药机会发现的静态交互式 HTML 报告或预置结果筛查页面。适用于用户要求筛选中国小分子晶型专利到期机会、生成带结果的仿药速探 V1，或创建由已配置智慧芽/PatSnap MCP 支撑的本地报告的场景。
---

# 仿药速探 V1

使用本 Skill 运行 V1 首轮筛查，并创建已预载结果的本地交互式 HTML 报告。目标用户体验为：

1. 用户要求进行仿药速探 V1 筛查。
2. Skill 通过已配置的智慧芽/PatSnap MCP 执行首轮筛查。
3. Skill 生成已填入首轮结果的本地 `.html` 报告页面。
4. 用户可直接打开文件，无需启动本地服务。

## V1 范围

V1 保持聚焦；除非用户明确要求，否则不要扩展筛选条件范围：

- 地区：仅限中国 / CN。
- 药物类型：仅限小分子化学药。
- 专利重点：晶型/多晶型专利。
- 筛查输出：主候选、优先级解释、排除记录、数据说明、来源，以及可导出的完整报告。
- 化合物专利到期仅作为辅助证据，不作为硬性筛选条件。

当用户询问为什么 V1 这样限定，或如何解释业务逻辑时，读取 `references/v1-scope.md`。

## 内置报告 UI

平台模板内置于：

`assets/platform-template/app`

其中包含：

- `index.html`：前端报告 UI，包含 V1 价值亮点弹窗。
- `server.py`：本地 HTTP 服务和由 MCP 支撑的 `/api/search` 端点。
- `assets/`：页面使用的本地图片。

后端期望 `~/.codex/config.toml` 中存在以下 MCP 服务名：

- `zhihuiya_logic_096456`：用于医药情报。
- `zhihuiya_logic_2b0355`：用于 PatSnap 专利检索/获取。

## 默认工作流：静态交互式 HTML 报告

当用户要求筛查机会时，最终交付物应是基于实时 MCP 数据生成的独立 HTML 报告。真实筛查请求不得使用内置样例数据；除非用户明确要求服务器版本，否则不要提供 `127.0.0.1` 链接。

先运行实时 MCP 筛查：

```powershell
python generic-drug-scout-v1\scripts\create_seeded_screening_platform.py --target .\仿药速探V1_真实结果平台 --window-years 2 --overwrite
```

然后根据 MCP 结果 JSON 创建静态报告：

```powershell
python generic-drug-scout-v1\scripts\create_static_report_html.py --data .\仿药速探V1_真实结果平台\first_screening_result.json --output .\仿药速探V1_真实数据静态报告.html
```

报告生成后，自动用默认浏览器打开：

```powershell
Start-Process ".\仿药速探V1_真实数据静态报告.html"
```

或通过 exec：

```python
import subprocess, os
subprocess.Popen(["cmd", "/c", "start", "", html_path])
```

将生成的 `_assets` 文件夹与 HTML 文件放在同一目录。报告图片内置在 Skill 中，并复制到每次生成报告的旁边，使文件无需服务器即可打开。

生成页面是报告式 HTML，已加载首轮结果。它保留本地交互能力，例如标签页、搜索、排序、CSV 导出、报告 HTML 导出、打印/PDF，以及价值亮点弹窗。它不显示「开始筛查」按钮，也不会调用 `/api/search`。

仅用于 UI 预览且不重新运行 MCP 时，可使用内置样例结果：

```powershell
python generic-drug-scout-v1\scripts\create_static_report_html.py --output .\仿药速探V1_样例静态报告.html
```

`create_seeded_screening_platform.py` 会在生成的应用旁写入 `first_screening_result.json`，用于审计。该 JSON 包含固定 V1 参数，以及用于预置页面的原始报告结果。

如果 MCP 调用失败或超时，不要伪造数据。报告 MCP 错误；仅当用户要求时，才使用内置样例数据做 UI 评审。

## 筛查后的回复规则

筛查运行完成并生成报告后，Agent 必须严格遵循以下输出规则：

1. **不要在聊天中输出筛查结果表、候选清单或数据摘要。** 报告 HTML 是展示结果内容的唯一位置。
2. **只在代码块中输出生成 HTML 文件的绝对本地路径**，并附一句确认，例如「✅ 报告已生成，已用浏览器打开」。
3. **写入文件后立即使用 `exec` 或 `subprocess` 自动在默认浏览器打开生成的 HTML 文件。** 不要等用户再要求。
4. 如果打开浏览器失败，报告错误，但仍显示路径，便于用户手动打开。

正确回复格式示例：

```
✅ 报告已生成，已用浏览器打开。

报告路径：
C:\Users\...\仿药速探V1_真实数据静态报告.html
```

不要在该内容之后添加表格、候选数量、药物清单或任何其他结果内容。

## 可选服务器平台

仅当用户明确希望在页面中调整到期窗口并重新运行筛查时使用：

```powershell
python generic-drug-scout-v1\scripts\create_seeded_screening_platform.py --window-years 2 --overwrite
python .\仿药速探V1_首轮结果平台\app\server.py
```

打开：

```text
http://127.0.0.1:8790/
```

## 创建或恢复平台

仅当用户需要空白/手动平台，或 MCP 筛查不可用但用户仍希望查看 UI 时使用：

```powershell
python generic-drug-scout-v1\scripts\materialize_platform.py --target .\仿药速探V1平台 --overwrite
```

然后运行：

```powershell
python .\仿药速探V1平台\app\server.py
```

打开：

```text
http://127.0.0.1:8790/
```

如果端口 `8790` 已被占用，停止旧的本地进程；只有用户要求使用其他端口时，才编辑 `app/server.py`。

## V1 UI 规则

更新 UI 时：

- 保持页面功能可用；避免假功能和无法工作的装饰控件。
- 保留价值亮点弹窗：页面加载时打开，可关闭，也可从右下角入口重新打开。
- 保留报告导出控件：CSV、完整 HTML 报告和打印/PDF。
- 保留通过 `window.INITIAL_REPORT_PARAMS` 和 `window.INITIAL_REPORT_DATA` 预置结果的支持。
- 保留固定 V1 筛选文本：CN + 小分子 + 晶型专利；只有到期窗口可调整。
- 保留主表、优先候选、排除记录、数据说明和来源的标签页。
- 对静态报告，移除「开始筛查」按钮，以及任何提示用户点击该按钮的可见说明。
- 尽可能让弹窗在桌面端一屏内显示完整。
- 更换图片前，检查图片是否透明、被裁切、压缩，或与背景视觉割裂。
- 修改前端后，在浏览器中验证标签页仍可切换，弹窗仍可打开/关闭。

## 后端规则

更新 `server.py` 时：

- 不要在平台文件中嵌入 API key。
- 从 `~/.codex/config.toml` 读取 MCP URL。
- 除日期窗口外，保持 V1 查询参数固定为小分子 + CN + 晶型专利。
- 保留独立的 `rows` 和 `not_promoted` 输出，使 UI 能区分主表候选和排除记录。
- `rows` 是经过药物证据验证后进入主表的候选。
- `not_promoted` 仍在平台中展示，让用户看到哪些记录未进入主表以及原因。

## 输出契约

平台应展示报告所需的全部结果区块：

- 标题/页眉和当前 V1 筛选设置。
- 数据概览卡片。
- 主筛查结果表。
- 带理由的优先候选解释。
- 未提升记录。
- 数据说明和限制。
- 来源摘要。
- CSV、完整 HTML 报告和打印/PDF 导出控件。

生成的平台是本地交付物。其他用户如需重新运行筛查，需要自行配置 MCP；预载 HTML 无需重新运行 MCP 也能展示预置结果。

## 打包

分享该 Skill 时，压缩整个 `generic-drug-scout-v1` 文件夹。不要包含运行时 `__pycache__` 文件夹。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
