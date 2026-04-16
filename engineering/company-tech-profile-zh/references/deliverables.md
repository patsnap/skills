# 交付物（Deliverables）

## 默认交付物

默认交付物为结构化 Markdown 报告：

- `report.md`

推荐章节：

1. 执行摘要
2. 公司-主题范围与边界
3. 路线画像与技术重点
4. 有证据支撑的优势与局限
5. 对用户决策的影响
6. 关键证据引用

## 可选正式导出

若宿主环境支持渲染，可选导出格式为：

- `deliverables/report.docx`
- `deliverables/report.pdf`

建议渲染路径：

- 使用 `pandoc` 将 Markdown 转换为 `docx` 和 `pdf`
- 需要自定义 Word 布局时使用 `python-docx`
- 偏好直接输出 `pdf` 时使用 `reportlab` 或 Markdown 转 PDF 工具

这些渲染器均为可选项。当 Markdown 质量高且证据文件完整时，本技能即视为完成。
