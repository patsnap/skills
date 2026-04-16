# 交付物（Deliverables）

## 默认交付物

默认交付物为结构化 Markdown 报告：

- `report.md`

推荐章节：

1. 执行摘要
2. 范围与候选池定义
3. 最终玩家集合与分层逻辑
4. 技术路线差异化与地理分布
5. 可选空白机会观察
6. 关键证据参考

## 可选正式导出

若宿主环境支持渲染，可选导出格式为：

- `deliverables/report.docx`
- `deliverables/report.pdf`

建议渲染路径：

- `pandoc`：从 Markdown 转换为 `docx` 和 `pdf`
- `python-docx`：用于自定义 Word 格式
- `reportlab` 或其他 Markdown 转 PDF 工具：用于 `pdf`

这些渲染器为可选项。当 Markdown 和证据文件质量过硬时，技能即视为完成。
