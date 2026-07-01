# 输出路径约定（全局唯一真理源）

本文件是 rd-direction-finder 技能所有输出文件路径的**全局唯一定义**。SKILL.md 正文与所有 bash 脚本必须引用本文件占位符或复用本文件的 bash 变量片段，**不得在他处硬编码具体路径**。若需调整目录或文件名，**只改本文件**。

## 占位符表

| 变量            | 默认值                                                      | 说明                             |
| :-------------- | :---------------------------------------------------------- | :------------------------------- |
| `REPORTS_DIR`   | `reports`                                                   | 报告输出目录（相对当前工作目录） |
| `DATE`          | `$(date +%Y%m%d)`                                           | 日期戳，格式 YYYYMMDD            |
| `PAYLOAD_PATH`  | `@session/reports/rd-direction-finder-payload-${DATE}.json` | 结构化 payload JSON              |
| `HTML_PATH`     | `@session/reports/rd-direction-finder-report-${DATE}.html`  | HTML 报告                        |
| `MARKDOWN_PATH` | `@session/reports/rd-direction-finder-report-${DATE}.md`    | Markdown 报告                    |

`DATE` 在执行时由 `date +%Y%m%d` 动态生成，不得保留字面占位符。

## 脚本路径

| 脚本     | 路径                       |
| :------- | :------------------------- |
| 渲染脚本 | `scripts/render_report.py` |

## 用户自定义路径

若用户在输入中明确指定输出目录或文件名，以用户值为准覆盖默认取值；占位符语义和引用方式保持不变。
