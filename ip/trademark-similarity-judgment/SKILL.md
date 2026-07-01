---
name: trademark-similarity-judgment
description: |
  Professional trademark similarity and confusion-risk assessment for Chinese trademark work. Use when a user uploads or describes a mark, logo, packaging, screenshot, search result, trademark list, image, Word/PDF/Excel file, or asks for 商标近似判断, 图文双模态比对, 驳回风险, 引证商标分析, 商品/服务类似判断, 混淆可能性评估, or handling suggestions before filing, review, opposition, invalidation, coexistence, or brand clearance.
---

# Trademark Similarity Judgment

## Objective

Assess whether the user's target mark is likely to be considered identical or similar to prior marks on identical or similar goods/services, with emphasis on confusion likelihood under Chinese trademark practice. Produce a professional risk level, reasoning, evidence gaps, and handling suggestions.

This skill is a business/legal analysis aid, not a legal opinion. State uncertainty when official registry data, status, goods/services, or image quality is incomplete.

## Inputs To Collect

Use the uploaded files and user text first. If key facts are missing, proceed with explicit assumptions and list the missing items instead of blocking, unless the missing item makes the assessment impossible.

Collect:

- Target mark: text, image, logo, packaging/screenshot, pronunciation, meaning, colors, layout, dominant elements.
- Goods/services: Nice class, standard item names, business scenario, sales channels, target consumers.
- Prior marks: registration/application number, owner, mark sample, class, goods/services, filing date, status, cited mark source.
- Market context: actual use, brand fame, evidence of coexistence or confusion, planned filing strategy.

For image uploads, inspect both the whole visual impression and separable elements: text, figure, shape, color, layout, packaging trade dress, and the visually dominant part.

## Workflow

1. **Normalize the target mark**
   - Extract text in Chinese, English, pinyin, numbers, symbols, and variants.
   - Describe graphic elements, composition, color, and dominant visual features.
   - Identify weak elements such as generic names, descriptive words, model numbers, geographic terms, common slogans, and decorative shapes.

2. **Define goods/services**
   - Identify class and specific goods/services.
   - Compare function, purpose, raw materials, providers, sales channels, consumer groups, service content, and transaction scenes.
   - Do not rely only on class number; explain cross-class association when commercially relevant.

3. **Identify prior rights**
   - Use user-provided cited marks when available.
   - If the user asks for live registry verification, browse or use available official sources where possible; cite source limits.
   - Check status and dates: valid, pending, rejected, invalidated, cancelled, expired, renewal status, and vulnerability to non-use cancellation.

4. **Compare signs**
   - Text marks: compare character shape, pronunciation, meaning, word order, length, rhythm, translation/transliteration, and overall call.
   - English/pinyin/number marks: compare letters, syllables, prefixes/suffixes, pronunciation, meaning, and visual length.
   - Graphic marks: compare subject, outline, composition, color, style, and overall visual impression.
   - Composite marks: apply overall observation while identifying the dominant/distinctive part.
   - Packaging/screenshots: separate trademark similarity from broader trade dress similarity, then explain both if relevant.

5. **Assess distinctiveness and fame**
   - Weigh invented or highly distinctive elements more heavily than descriptive/common elements.
   - If the shared part is weak, require stronger overall similarity or stronger goods/service overlap for high risk.
   - If a prior mark is famous or highly distinctive, treat protection scope as broader and explain why.

6. **Assess confusion likelihood**
   - Evaluate whether relevant consumers may believe the goods/services come from the same source or from affiliated, licensed, series-brand, group-company, franchise, distributor, or cooperation relationships.
   - Consider consumer attention level, purchase scenario, channel overlap, actual use, search/e-commerce display, and evidence of actual confusion or coexistence.

7. **Assign risk level**
   - High: close sign similarity plus identical/similar goods/services, valid prior right, distinctive or known prior mark, likely confusion.
   - Medium: partial similarity or arguable goods/service relationship; outcome depends on dominant elements, evidence, or examiner discretion.
   - Low: clear overall differences, unrelated goods/services, weak shared elements, invalid prior right, or persuasive coexistence/no-confusion facts.
   - Arguable: likely office action or dispute risk, but there are credible review, non-use cancellation, invalidation, coexistence, or narrowing arguments.

8. **Recommend handling**
   - Filing: proceed, redesign, add distinguishing elements, change name, change logo, adjust colors/layout, split applications.
   - Goods/services: delete or narrow high-risk items, reclassify, stage filing, add defensive filings.
   - Prior-right strategy: monitor, non-use cancellation, invalidation, assignment, license/coexistence negotiation, evidence preparation.
   - Dispute response: prepare refusal review, distinction arguments, use evidence, fame evidence, coexistence evidence, or challenge cited marks.

## Output Format

Use concise professional Chinese unless the user asks otherwise.

Include:

- **结论**: risk level and one-sentence reason.
- **对象拆解**: target mark elements and dominant/distinctive parts.
- **商品/服务关系**: identical, similar, related, or unrelated, with reasons.
- **近似比对**: text, pronunciation, meaning, graphic, layout, and overall impression as applicable.
- **混淆可能性**: relevant public, channels, source association risk.
- **风险等级**: high/medium/low/arguable, with confidence.
- **处理建议**: concrete next actions.
- **需补充信息**: only items that materially affect the conclusion.

For complex matters or multiple cited marks, use a table with columns: cited mark, status, goods/services relation, sign similarity, key risk reason, risk level, action.

## Reference

For a fuller checklist, scoring rubric, and report template, read `references/assessment-framework.md` when the user asks for a formal report, batch review, detailed scoring, or deliverable suitable for business handoff.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
