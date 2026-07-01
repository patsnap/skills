---
name: base-station-antenna-monitor
description: |
  基站天线专利技术监控工具，面向普罗斯通信技术使用。自动检索近一个月内华为、康普、京信、爱立信等17家核心企业的基站天线相关专利，按振子、天线罩、反射板三大技术分支分类，生成包含专利清单与技术概要的专业HTML报告。
---

# 基站天线专利监控 Skill

## 用途

面向普罗斯通信技术，定期监控基站天线领域核心竞争对手的最新专利动态，输出结构化 HTML 报告。

## 功能

1. **多企业批量检索**：覆盖17家目标企业，每家独立检索后合并去重，突破单次100条限制
2. **技术分支自动分类**：按振子、天线罩、反射板三类自动归类
3. **专利技术概要提炼**：基于摘要自动生成中文技术概要
4. **HTML报告生成**：包含数据总量、关键词云、专利清单表格

## 输入参数

运行脚本时支持以下可选命令行参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--days` | `30` | 往前追溯天数（近一个月=30） |
| `--topk` | `100` | 每家企业每次检索返回条数上限 |
| `--output` | `report.html` | 输出HTML文件路径 |

## 技术分支关键词映射

- **振子**：振子、辐射单元、偶极子、radiating element、dipole、radiation unit
- **天线罩**：天线罩、radome、防护罩、protective cover
- **反射板**：反射板、反射器、底板、reflector、ground plane、back plate

## 输出

- `report.html`：完整的专业 HTML 监控报告

## 运行方式

```bash
python scripts/run_monitor.py --days 30 --output report.html
```

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
