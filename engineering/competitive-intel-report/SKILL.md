---
name: competitive-intel-report
description: |
  汽车NVH声学密封与结构增强件竞争情报HTML报告生成器。输入我方公司名称、竞争对手列表及专利检索结果，自动生成与V12版本风格完全一致的浅色交互式HTML情报简报，内嵌纯CSS图文图表（无外部依赖）、执行摘要KPI直展详情、SWOT分析、专利全景对比、威胁矩阵、应对建议等10大模块，所有专利链接可直接跳转智慧芽PatSnap。
---

# competitive-intel-report

## 功能说明

基于 V12 HTML 模板，生成汽车声学密封与结构增强件（Baffle / SNS）领域的竞争情报报告。

**V12 版本核心特性：**
- 📋 执行摘要：4张KPI卡直接展示威胁/风险/机会/评分详情（无需点击）
- 🎨 浅色调设计：白底卡片 + 浅蓝渐变 Header，专业简洁
- 📊 纯CSS图文图表：零外部依赖，环境100%兼容
- 🖱️ 图表/数字可点击：弹出对应专利浮层，专利号直跳智慧芽
- 📁 10大模块完整：市场全景→竞品画像→OEM矩阵→威胁评估→应对建议

## 输入参数

| 参数 | 说明 | 示例 |
|---|---|---|
| `our_company` | 我方公司全称 | 海程新材料有限公司 |
| `our_company_short` | 我方公司简称 | 海程 |
| `our_products` | 我方核心产品 | Baffle / SNS |
| `competitor_a1` | A级竞争对手1 | Zephyros / L&L Products |
| `competitor_a2` | A级竞争对手2 | Sika AG |
| `competitor_a3` | A级竞争对手3 | Henkel AG |
| `competitors_b` | B级竞争对手列表 | BASF / Dow / LANXESS / Sonderhoff |
| `industry` | 行业描述 | 汽车声学密封与结构增强 |
| `report_period` | 报告期 | 2026Q2 |

## 使用方式

直接告诉 Eureka：

> "帮我生成竞争情报报告，我方公司是XX，竞争对手是A、B、C"

Skill 自动将模板中的公司名替换为指定内容，风格/布局/图表/模块/交互功能全部锁定不变。

## 输出

- 完整 HTML 报告文件（单文件，可离线使用）
- 支持一键下载 HTML + 打印存为 PDF
- 所有专利号可跳转智慧芽PatSnap全文

## 模板版本

当前模板：**V12**（references/template_v12.html）
- 执行摘要KPI详情直接展示（无需点击）
- 全部空白图表替换为纯CSS图文
- 语法错误已修复，100%兼容Eureka预览环境

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
