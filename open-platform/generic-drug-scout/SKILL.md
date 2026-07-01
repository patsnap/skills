---
name: generic-drug-scout
description: Run 仿药速探 V1 to create a static interactive HTML report or seeded screening page for generic-drug opportunity discovery. Use when the user asks to screen China small-molecule crystal-form patent expiry opportunities, generate 仿药速探 V1 with results, or create a local report backed by configured Zhihuiya/PatSnap MCPs.
---

# 仿药速探 V1

Use this skill to run V1 first-pass screening and create a local interactive HTML report preloaded with results. The intended user experience is:

1. User asks for 仿药速探 V1 screening.
2. The skill runs the first screening through the configured Zhihuiya/PatSnap MCPs.
3. The skill generates a local `.html` report page already filled with the first-pass result.
4. The user can open the file directly, without starting a local server.

## V1 Scope

Keep V1 focused and do not broaden the filter surface unless the user explicitly asks:

- Region: China / CN only.
- Drug type: small-molecule chemical drugs only.
- Patent focus: crystal-form/polymorph patents.
- Screening output: main candidates, priority explanations, excluded records, data notes, sources, and an exportable full report.
- Compound patent expiry is supporting evidence only; it is not a hard filter.

Read `references/v1-scope.md` when the user asks about why V1 is scoped this way or how to explain the business logic.

## Bundled Report UI

The platform template is bundled at:

`assets/platform-template/app`

It contains:

- `index.html`: frontend report UI, including the V1 value-highlight modal.
- `server.py`: local HTTP server and MCP-backed `/api/search` endpoint.
- `assets/`: local images used by the page.

The backend expects the following MCP server names in `~/.codex/config.toml`:

- `zhihuiya_logic_096456` for pharma intelligence.
- `zhihuiya_logic_2b0355` for PatSnap patent search/fetch.

## Default Workflow: Static Interactive HTML Report

When the user asks to screen opportunities, the final deliverable should be a standalone HTML report generated from live MCP data. Do not use bundled sample data for a real screening request, and do not provide a `127.0.0.1` link unless the user explicitly asks for the server version.

First run live MCP screening:

```powershell
python generic-drug-scout\scripts\create_seeded_screening_platform.py --target .\仿药速探V1_真实结果平台 --window-years 2 --overwrite
```

Then create the static report from the MCP result JSON:

```powershell
python generic-drug-scout\scripts\create_static_report_html.py --data .\仿药速探V1_真实结果平台\first_screening_result.json --output .\仿药速探V1_真实数据静态报告.html
```

After the report is generated, open it automatically in the default browser:

```powershell
Start-Process ".\仿药速探V1_真实数据静态报告.html"
```

Or via exec:

```python
import subprocess, os
subprocess.Popen(["cmd", "/c", "start", "", html_path])
```

Keep the generated `_assets` folder next to the HTML file. The report images are bundled inside the skill and copied beside each generated report so the file can be opened without a server.

The resulting page is a report-style HTML with first-pass results already loaded. It keeps local interactions such as tabs, search, sort, CSV export, report HTML export, print/PDF, and the value-highlight modal. It does not show a「开始筛查」button and does not call `/api/search`.

For UI preview only, without rerunning MCP, the bundled sample result can be used:

```powershell
python generic-drug-scout\scripts\create_static_report_html.py --output .\仿药速探V1_样例静态报告.html
```

`create_seeded_screening_platform.py` writes `first_screening_result.json` beside the generated app for auditability. That JSON contains the fixed V1 parameters and the raw report result used to seed the page.

If the MCP call fails or times out, do not fabricate data. Report the MCP error and, only if the user asks, use the bundled sample data for UI review.

## Reply Rules After Screening

After a screening run completes and the report is generated, the agent MUST follow these output rules strictly:

1. **Do NOT output screening result tables, candidate lists, or data summaries into the chat.** The report HTML is the only place for result content.
2. **Only output the absolute local path of the generated HTML file** in a code block, plus a one-line confirmation such as「✅ 报告已生成，已用浏览器打开」.
3. **Automatically open the generated HTML file in the default browser** using `exec` or `subprocess` immediately after the file is written. Do not wait for the user to ask.
4. If the browser-open step fails, report the error but still show the path so the user can open it manually.

Example of the correct reply format:

```
✅ 报告已生成，已用浏览器打开。

报告路径：
C:\Users\...\仿药速探V1_真实数据静态报告.html
```

Do not add tables, candidate counts, drug lists, or any other result content after this block.

## Optional Server Platform

Use this only when the user explicitly wants to adjust the expiry window and rerun screening inside the page:

```powershell
python generic-drug-scout\scripts\create_seeded_screening_platform.py --window-years 2 --overwrite
python .\仿药速探V1_首轮结果平台\app\server.py
```

Open:

```text
http://127.0.0.1:8790/
```

## Create Or Restore The Platform

Use this only when the user wants an empty/manual platform, or when MCP screening is unavailable and the user still wants to inspect the UI:

```powershell
python generic-drug-scout\scripts\materialize_platform.py --target .\仿药速探V1平台 --overwrite
```

Then run:

```powershell
python .\仿药速探V1平台\app\server.py
```

Open:

```text
http://127.0.0.1:8790/
```

If port `8790` is already occupied, stop the old local process or edit `app/server.py` only if the user asks for a different port.

## UI Rules For V1

When updating the UI:

- Keep the page functional; avoid fake features and decorative controls that do not work.
- Preserve the value-highlight modal: it opens on page load, can be closed, and can be reopened from the bottom-right entry.
- Preserve report export controls: CSV, full HTML report, and print/PDF.
- Preserve seeded-result support through `window.INITIAL_REPORT_PARAMS` and `window.INITIAL_REPORT_DATA`.
- Preserve the fixed V1 filter text: CN + small molecule + crystal-form patent; only the expiry window is adjustable.
- Preserve tabs for main table, priority candidates, excluded records, data notes, and sources.
- For static reports, remove the「开始筛查」button and any visible instruction that tells the user to click it.
- Keep the modal one-screen on desktop when possible.
- Before changing images, inspect whether they are transparent, cropped, compressed, or visually disconnected from the background.
- After changing the frontend, verify in the browser that tabs still switch and the modal opens/closes.

## Backend Rules

When updating `server.py`:

- Do not embed API keys in the platform files.
- Read MCP URLs from `~/.codex/config.toml`.
- Keep V1 query parameters fixed to small molecule + CN + crystal-form patent, except date window.
- Preserve separate `rows` and `not_promoted` outputs so the UI can distinguish main-table candidates from excluded records.
- `rows` are candidates promoted to the main table after drug evidence verification.
- `not_promoted` are still shown in the platform so the user can see what did not enter the main table and why.

## Output Contract

The platform should expose all result sections needed for a report:

- Title/header and current V1 filter settings.
- Data overview cards.
- Main screening result table.
- Priority candidate explanations with reasons.
- Not-promoted records.
- Data notes and limitations.
- Source summary.
- Export controls for CSV, full HTML report, and print/PDF.

The generated platform is a local deliverable. Other users need their own MCP configuration if they want to rerun screening; the preloaded HTML can still display the seeded results without rerunning MCP.

## Packaging

To package this skill for sharing, zip the whole `generic-drug-scout` folder. Do not include runtime `__pycache__` folders.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
