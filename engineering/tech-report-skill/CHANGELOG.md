# 更新日志

本文档记录 tech-report-skill 的版本更新历史。

## [v1.1.0] - 2026-06-06

### 新增功能
- ✨ 添加装饰性背景图片功能，Hero区域支持自动下载并Base64嵌入背景图
- ✨ 新闻支持"查看原文"链接，可跳转到新闻网页
- ✨ 智能专利分类算法，基于关键词匹配度自动选取每个技术分类的Top-20专利
- ✨ 添加咖啡机技术配置示例（6个技术分类）

### 重要修复
- 🐛 修复专利链接丢失问题 - 使用openpyxl保留Excel超链接
- 🐛 修复专利摘要附图丢失问题 - 使用openpyxl保留Excel嵌入图片
- 🐛 修复技术分类专利数量过少问题 - 实现智能分类算法

### 改进优化
- 📝 完善文档体系，新增 IMPROVEMENTS.md 和 DISTRIBUTION.md
- 📝 添加配置文件说明文档（config/README.md）
- 📝 添加数据格式说明文档（examples/SAMPLE_DATA.md）
- 🚀 添加一键安装脚本（install.sh）
- 📦 添加标准依赖清单（requirements.txt）
- 🔧 添加 .gitignore 和 LICENSE 文件

### 技术细节
- 专利号到Excel行号的精确映射，避免图片和链接错位
- Base64图片嵌入确保HTML完全自包含
- 关键词相关度评分算法（统计匹配关键词数量）
- CSS渐变叠加背景图，确保文字可读性

### 文档更新
- README.md：增加通用性说明、安装方法、核心特性展示
- SKILL.md：增加核心特性章节、常见问题解答
- 新增 IMPROVEMENTS.md：详细记录5个核心改进和技术亮点
- 新增 DISTRIBUTION.md：分发前检查清单和打包指南

---

## [v1.0.0] - 2026-05-28

### 首次发布
- 🎉 首次发布 tech-report-skill
- ✨ 支持专利关键词标引（tag_relevant.py）
- ✨ 支持HTML简报生成（generate_report.py）
- ✨ 提供BIPV技术配置示例
- 📝 完成基础文档（SKILL.md, README.md）

### 核心功能
- 基于关键词的专利相关性判断
- 高相关专利高亮显示
- 响应式HTML简报生成
- 行业动态、重点公司、技术分类三大模块
- 固定导航栏，支持快速跳转
- 卡片式设计，美观清晰

### 技术特点
- 使用pandas处理Excel数据
- 动态加载配置文件
- CSS内联，无外部依赖
- 支持中英文双语关键词

---

## 版本规范

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- **主版本号**：不兼容的API修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

---

## 未来计划

### v1.2.0（计划中）
- [ ] 添加交互式图表（专利趋势、公司分布、技术雷达图）
- [ ] 支持PDF导出功能
- [ ] 添加多语言支持（中英文简报）
- [ ] 优化大数据量处理性能（2000+专利）

### v1.3.0（计划中）
- [ ] 集成LLM自动生成技术总结
- [ ] 自动提取专利核心创新点
- [ ] 智能推荐相关技术主题
- [ ] 添加单元测试

### v2.0.0（远期规划）
- [ ] Web界面支持
- [ ] 在线协作编辑配置
- [ ] 数据库存储历史简报
- [ ] 定时自动生成和邮件推送

---

## 贡献者

感谢所有为 tech-report-skill 做出贡献的开发者！

---

## 反馈与建议

如果你有任何建议或发现了问题，欢迎：
- 提交 [Issue](https://github.com/yourusername/tech-report-skill/issues)
- 发起 [Pull Request](https://github.com/yourusername/tech-report-skill/pulls)
- 在 Claude Code 中直接询问："tech-report-skill 有什么改进建议？"
