---
name: overseas-patent-translation
description: |
  Translate Chinese patent application documents for overseas filing and format them for Europe, United States, Japan, or Korea. Use when the user uploads or describes a Chinese patent specification, claims, abstract, drawings, priority text, or technical disclosure and asks for overseas patent application translation, 涉外专利翻译, PCT/巴黎公约进入海外文本, EP/US/JP/KR patent filing text, target-country formatting, translation QA, terminology consistency, or jurisdiction-specific patent translation guidance.
---

# Overseas Patent Translation

## Purpose

Produce target-jurisdiction patent application translations from Chinese priority/application text while preserving priority support, claim scope, terminology consistency, and local filing format.

## Intake Workflow

1. Confirm uploaded/input Chinese materials.
   - Identify whether the user provided claims, description, abstract, drawing descriptions, drawings, sequence listing, or only a technical disclosure.
   - If only partial materials are provided, proceed with the available sections and state what is missing.
   - Preserve the Chinese priority disclosure; do not add unsupported technical features, effects, parameters, or embodiments.

2. Ask the user to choose target jurisdiction if not already specified.
   - Supported options: Europe, United States, Japan, Korea.
   - Allow multiple selections; generate a separate jurisdiction-specific output for each selection.

3. Load only the relevant reference file:
   - Europe: `references/europe.md`
   - United States: `references/united-states.md`
   - Japan: `references/japan.md`
   - Korea: `references/korea.md`

4. Translate and format.
   - Convert Chinese patent language into target-language patent drafting style.
   - Keep technical facts anchored to the Chinese text.
   - Preserve claim dependencies, numbering, units, reference signs, formulas, tables, and sequence-listing identifiers.
   - Use local section headings and document order from the loaded jurisdiction reference.

5. Deliver the output.
   - Provide the formatted translated application text.
   - Include a terminology table for core terms.
   - Include a concise translation QA/risk note when issues are found.

## Translation Rules

- Prioritize claims first; they control protection scope.
- Keep the same technical term translated consistently across claims, description, abstract, and drawing descriptions.
- Preserve open-ended claim language unless the Chinese text clearly requires a closed limitation.
- Do not turn optional, preferred, or exemplary features into mandatory claim limitations.
- Do not silently impose a strict step order in method claims unless the Chinese text or technical logic requires it.
- Treat "至少一个", "多个", "任一", "和/或", "可选地", "优选地", and "包括/包含" as high-risk scope terms and translate deliberately.
- Avoid overclaiming effects such as "significantly", "completely", or "substantially" unless supported by data or explicit Chinese disclosure.
- Clean up Chinese-style long sentences and missing subjects only to improve clarity; do not change the technical content.
- Flag unclear Chinese source text instead of inventing unsupported meaning.

## Quality Checks

Before final delivery, check:

- Claim numbering and dependencies are intact.
- Each claim term appears consistently in the description.
- Reference signs match the drawings and drawing descriptions.
- Units, ranges, formulas, algorithm steps, materials, and test conditions are preserved.
- Abstract, title, and section headings match the target jurisdiction format.
- No source-disclosure expansion or unintended narrowing appears in the translation.

## Output Pattern

For each selected jurisdiction, structure the response as:

```text
[Jurisdiction] Patent Application Translation

1. Formatted translated application text
2. Terminology table
3. Translation QA and risk notes
```

When creating files, use this folder convention unless the user requests another structure:

```text
project-name/
├─ 01_chinese_source/
├─ 02_terminology/
├─ 03_europe_ep_english/
├─ 04_united_states_us_english/
├─ 05_japan_jp_japanese/
├─ 06_korea_kr_korean/
└─ 07_translation_qa/
```

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
