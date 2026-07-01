---
name: competitor-skill
description: |
  "给定 PatSnap 专业检索式，检索专利数据库，生成竞争对手专利分析报告。当用户输入包含 PatSnap 字段操作符（如 ANCS:、TAC_all:、DESC_B:、MAINF:、ALL_AN:、PN:、APD:、PBD:、APNO:、PRNO: 等）的检索式时触发。"
---

# Competitor Patent Report Skill

## 用途

给定一条 PatSnap 专业检索式和报告标题，自动检索专利数据库，生成竞争对手专利分析报告 Markdown 文件，包含新公开专利概况、专利技术总结和专利详情三个部分。

## 首次安装配置

**首次使用前，使用者必须配置自己的智慧芽（PatSnap）API Key，否则无法检索专利数据。**

本 Skill 包不应内置任何 API Key。分享给他人前，请确认 `scripts/config.py` 中没有真实 key，且包内不包含 `scripts/.env`。

### AI 引导规则

当用户首次触发本 skill（输入检索式）时，**必须先执行以下检查**：

1. 在 skill 工作目录的 `scripts/` 子目录下查找名为 `.env` 的配置文件，检查是否存在 `PATSNAP_API_KEY`
2. 如果文件不存在或 key 为空：
   - 告知用户需要先配置他自己的智慧芽 API Key
   - 询问用户："请提供你的智慧芽 API Key（格式通常为 sk-xxx）："
   - 用户输入后，将其写入 skill 工作目录 `scripts/` 子目录下的 `.env` 配置文件：`PATSNAP_API_KEY=用户输入的key`
   - 确认写入成功后，继续执行检索
3. 如果 key 已存在，直接执行检索

`.env` 示例：

```bash
PATSNAP_API_KEY=sk-你的智慧芽APIKey

# 可选：如文献检索使用不同 key，可单独配置；未配置时默认复用 PATSNAP_API_KEY
# LITERATURE_API_KEY=sk-你的文献检索APIKey

# 可选：如需 AI 文献总结，可配置自己的 ARK Key；未配置时自动跳过该总结
# ARK_API_KEY=你的ARK_APIKey
```

---

## 触发条件

- 用户输入包含 PatSnap 字段操作符的检索式，例如：
  - `ANCS:`、`TAC_all:`、`DESC_B:`、`MAINF:`、`ALL_AN:`、`PN:`、`APD:[`、`PBD:[`、`APNO:`、`PRNO:`
- 用户明确要求"运行检索式"、"执行检索"、"根据检索式生成报告"等

## 调用方式

```bash
cd ~/Documents/competitor_skill
bash scripts/run.sh "<检索式>" "<报告标题>" [数量]
```

**参数说明：**

- `<检索式>`：PatSnap 专业检索式（必填）
- `<报告标题>`：报告标题，用于文件命名和报告头部（可选，默认"专利检索报告"）
- `[数量]`：最大检索条数，默认 200

## 报告结构

### 第一部分：新公开专利概况

- 检索元信息（检索式、报告标题）
- 各公司专利数量统计表格

### 第二部分：专利技术总结

- 每家公司一张卡片，总结技术焦点和技术手段

### 第三部分：专利详情

- 按细分技术方向 → 申请人（公司）→ 专利三级展开
- 每篇专利：标题、公开号（可点击跳转智慧芽）、法律状态、申请人、申请日、技术问题、技术手段、技术功效、摘要附图

## 输出

- `run.sh` 将报告 Markdown 内容直接输出到 stdout，同时保存到 `reports/` 目录

## 报告生成后的展示规则

`run.sh` 执行完毕后：

1. 在对话框中展示以下内容：
   - **第一部分（新公开专利概况）**：完整展示
   - **第二部分（专利技术总结）**：完整展示
   - **第三部分（专利详情）**：不在对话框展示，告知用户完整报告已保存到文件

## 环境要求

- Python 或 `uv`

## 依赖

```
requests>=2.31.0
python-dotenv>=1.0.0
```

自动安装（通过 `uv` 或 `pip`），无需手动操作。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
