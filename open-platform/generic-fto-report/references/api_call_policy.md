# 智慧芽 API 调用强约束

本 skill 调用智慧芽 API 必须内部自洽：

- 只能使用本 skill 的 `scripts/` 下脚本调用智慧芽 API。
- 禁止使用外部 MCP（包括 zhihuiya MCP）、其他 skill、其他插件或外部临时脚本调用智慧芽 API。
- API key 固定从 `references/zhihuiya_config.json` 读取，除非用户明确指定另一个 skill 内部配置文件。
- 对外分享版不得携带真实 API key。安装用户必须将 `zhihuiya_api_key` 的占位值 `PUT_YOUR_ZHIHUIYA_API_KEY_HERE` 替换成自己的智慧芽 API key。
- P070、P002、P018、AI07 的调用均通过 `scripts/run_fto_report.py` 或 `scripts/zhihuiya_api.py` 实现。
- P018 必须使用 `/basic-patent-data/claim-data`，不得使用旧路径 `/basic-patent-data/claims`。
- AI07 仅作为辅助记录。若 AI07 输出与 P018 权利要求结构化比对冲突，以 P018 权利要求结构化比对为报告结论依据，并在追溯文件记录 AI07 原始返回。

交付前必须检查：

- `references/zhihuiya_config.json` 存在且 `zhihuiya_api_key` 已由安装用户替换为真实值。
- `queries.json`、`patent_list.json`、`fto_structured_data.json` 均由 skill 内部脚本生成。
- 报告正文不得声称使用外部 MCP 或外部 skill 获得智慧芽数据。
