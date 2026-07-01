# 示例输出结构

## 报告目录结构（生成后）

```
output/
├── index.html              ← 主报告（1400行+，内容丰富）
├── patents.html            ← 50+ 代表专利，含搜索/分页
├── evidence.html           ← 15+ 条证据链，按强度分类
├── subfields.html          ← 6 个子技术分支详细分析
├── methodology.html        ← 检索式、口径说明、质量核查
├── intermediate_data.json  ← 完整结构化中间数据
├── patent_list.csv         ← 代表专利 CSV
├── evidence_mapping.csv    ← 证据映射 CSV
├── README.md               ← 文件说明
└── quality_check.md        ← 质量核查报告
```

> ⚠️ 无任何 .py 文件，无 scripts/ 目录。

---

## 对话最终输出示例

```
📊 分析完成：钠离子电池硬碳负极预钠化技术

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 综合推荐指数：78 / 100
💡 研发进入建议：建议进入
💰 投资吸引力：高
⚡ 竞争风险：中
📋 证据置信度：高
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 核心结论（基于全量统计）：
1. 全球专利总量 3,841 件，近五年 CAGR 32.4%，处于快速增长期 [C001]
2. 中国申请占全球 68%，主导地位显著，但国际布局不足 [C005]
3. 宁德时代、中科海钠为龙头，但 CR5 仅 38%，仍有进入空间 [C003]
4. 化学预钠化和电化学预钠化为当前主流，机械预钠化是空白点 [C007/C008]
5. 有效专利率 54%，质量中等，存在超越机会 [C006]
6. 预钠化均匀性控制为最大技术空白，近两年零篇幅 [C010]

📁 生成文件（共 10 个，无 .py）：
• index.html — 主报告（含 9 张 ECharts 交互图表 + 白皮书正文）
• patents.html — 50 条代表专利样本
• evidence.html — 18 条证据链
• subfields.html — 6 个子技术方向分析
• methodology.html — 检索策略和质量核查
• intermediate_data.json — 结构化中间数据
• patent_list.csv — 代表专利列表
• evidence_mapping.csv — 证据映射
• README.md — 文件说明
• quality_check.md — 质量核查通过报告

✅ 数据质量声明：
• 趋势图基于全量年度统计，非 TopK50 样本
• 趋势数据来源：patsnap-patent-technology-landscape trends MCP 全量接口
• TopK50 仅用于 patents.html 代表专利展示
• 所有图表均有真实数据，无占位符

👉 请打开 index.html 查看主报告
👉 打开 patents.html 查看更多专利
👉 打开 evidence.html 查看证据链
👉 打开 methodology.html 查看数据口径
```
