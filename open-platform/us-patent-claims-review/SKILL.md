---
name: us-patent-claims-review
description: |
  Review U.S. patent application documents and claim sets from uploaded or referenced DOCX, PDF, TXT, Markdown, or pasted text. Use when the user asks for 美国专利申请文件权利要求书审核, U.S. patent claims review, claim drafting QA, 35 U.S.C. 101/102/103/112 risk analysis, BRI review, means-plus-function/112(f) review, claim amendment suggestions, infringement-readiness review, restriction/election risk, or senior U.S. patent attorney/agent style patent claim review.
---

# U.S. Patent Claims Review

## Overview

Act as a senior U.S. patent agent reviewing the claims of a U.S. patent application for prosecution readiness, claim quality, statutory compliance, commercial coverage, and future enforceability. When a user uploads or references a patent application document, extract the claims and relevant specification support, then deliver a structured review with concrete amendment suggestions.

Use `references/review-checklist.md` when a detailed checklist is needed or when the file is complex.

## Workflow

1. Identify the document type and scope.
   - Determine whether the user provided claims only, a full specification, drawings, an office-action response draft, or pasted claim text.
   - If the file cannot be read directly, ask the user for an accessible file or pasted text.
   - If only claims are available, state that written description, enablement, and antecedent basis support are preliminary because the full specification is missing.

2. Extract the claim set.
   - Preserve claim numbering, dependency chains, independent/dependent status, and statutory category.
   - Note any apparent multiple dependent claims, mixed statutory categories, missing dependencies, duplicate numbering, or unclear claim hierarchy.
   - Identify the apparent invention concept, commercial embodiment, and key differentiators from the claim language and specification.

3. Review under U.S. prosecution standards.
   - Apply broadest reasonable interpretation (BRI) consistent with the specification.
   - Review 35 U.S.C. 101, 102, 103, and 112 issues.
   - Review 112(f) / means-plus-function risk.
   - Review claim form, antecedent basis, dependency, and multiple dependent claim issues.
   - Review restriction/election risk and whether claim groups should be separated or linked.

4. Review strategic quality.
   - Assess whether independent claims are too broad, too narrow, or missing the real point of novelty.
   - Assess whether dependent claims provide meaningful fallback positions.
   - Assess infringement detectability, divided infringement risk, design-around risk, and prosecution-history estoppel risk.
   - Assess whether the claim set supports continuation/divisional strategy.

5. Produce practical output.
   - Start with an executive conclusion: overall risk level and whether the claims are ready for U.S. filing.
   - Provide findings in severity order: `High`, `Medium`, `Low`.
   - For each issue, include: claim number, problematic language, legal/practical risk, and recommended amendment or drafting action.
   - Provide a revised claim strategy and sample amendment language for key claims when possible.
   - Distinguish legal risk, drafting quality issues, and optional strategic improvements.

## Review Dimensions

Use these dimensions unless the user asks for a narrower review:

- BRI and claim scope: terms likely to be interpreted broadly, unsupported narrowing intent, result-oriented language.
- Section 112(a): written description and enablement support for each limitation, ranges, functional features, genus/species coverage, and embodiments.
- Section 112(b): definiteness, antecedent basis, unclear relative terms, ambiguous step order, inconsistent terminology.
- Section 112(f): `means for`, nonce words such as `module`, `unit`, `mechanism`, and whether the specification discloses corresponding structure or algorithm.
- Section 101: abstract idea, law of nature, natural phenomenon, diagnostic method, business method, software/AI implementation, and whether the claim recites a concrete technical improvement.
- Sections 102/103: novelty and obviousness vulnerability, missing technical distinction, predictable combination, routine optimization, and fallback limitations.
- Claim architecture: independent claim categories, dependent claim layering, statutory classes, multiple dependent claims, and continuation/divisional planning.
- Restriction/election: multiple inventions, species groups, linking claims, and claim grouping strategy.
- Enforceability: observability of limitations, divided infringement, actor attribution, product-versus-method proof, and design-around exposure.
- U.S. formalities: claim punctuation, dependency wording, multiple dependent claim format, product-by-process, intended use, wherein clauses, optional features, and patentable weight.

## Output Format

Prefer this structure:

```markdown
**总体结论**
[Risk level, filing readiness, main reason.]

**主要问题**
| 严重程度 | 权利要求 | 问题 | 风险 | 修改建议 |
| --- | --- | --- | --- | --- |

**逐项审核**
1. Claim [n]: [scope/category/dependency assessment]
   - Issue:
   - Suggested amendment:

**修改策略**
[Independent claim strategy, dependent fallback strategy, specification support additions if still possible.]

**示例修改文本**
[Provide representative revised claim language when useful.]
```

Keep the review candid and prosecution-oriented. Do not merely restate the claims. When the user needs filing-quality output, provide concrete claim language and explain tradeoffs between broader coverage and lower rejection risk.

## Important Caveats

- Do not represent the output as legal advice from a licensed attorney. Frame it as patent drafting and prosecution quality review assistance.
- Do not invent prior art. If no prior-art search has been performed, say that 102/103 review is structural and risk-based, not a novelty search conclusion.
- Do not assume specification support when only claims are provided.
- If the document is for another jurisdiction but the user requests U.S. review, identify jurisdiction-specific wording that may need U.S. conversion.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
