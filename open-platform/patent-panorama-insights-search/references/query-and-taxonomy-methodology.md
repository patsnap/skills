# Query and Taxonomy Methodology

This file documents the expert query construction methodology (Part A) and taxonomy design methodology (Part B) used across the patent panorama pipeline.

## Part A — Expert Query Construction

### A1: Field-operator assignment
Assign each keyword a field operator (TTL_ALL / TA_ALL / TAC_ALL / TACD_ALL / DESC_S) based on how decisive the term is for the concept.

### A2: Constant topic anchor
Build one anchor disjunction scoped to TACD_ALL, reused verbatim in every branch query.

### A3: Proximity operators
Escalation ladder: AND → $SEN → $Wn → TTL_ALL.

### A4: Semi-automatic IPC
Reverse-derive IPC from seed patents. Never fabricate IPC classes.

### A5: Tiered NOT rules
Every NOT rule must carry a recorded reason. Tiers: whole IPC class / main classification / title term / embodiment / specific assignee.

### A6: Four-part skeleton
Each branch query decomposes into: (1) strong keyword clause, (2) weak keyword AND IPC, (3) self-sufficient IPC, (4) constant anchor + NOT block.

### A7: Date basis declaration
State whether pbdt (publication) or E_PRIORITY_DATE (priority) is used and why.

## Part B — Taxonomy Design Methodology

### B1: 4-column breakdown table
Level-1 / Level-2 / Level-3 / description. ≤40 Level-3 nodes, mutually exclusive within each parent.

### B2: Two-pass decomposition
Top-down (architecture-first) + bottom-up (evidence-driven calibration sample).

### B3: Granularity control
Each Level-3 node must be: writable as one clean branch query, describable in one sentence, mutually exclusive with siblings.

### B4: Key technical questions
≥10 questions, split roughly evenly across Level-1 branches. Each seeds a 环节4 evolution storyline.

### B5: Recommended patent package rubric
Six-item rubric: disruptive_technology | novel_application_scenario | pulls_latent_user_demand | major_performance_gain | novel_function | novel_interaction_mode.

## Part C — tech_taxonomy.txt Format Specification

**层级型**，每行一个叶节点，格式为 `>L1\L2\L3`。

- `>` 后紧跟第一级
- `\` 后依次为第二级、第三级
- 每行只写一条路径
- 纯内容，无注释、无序号、无空行分组、无标题行
- 每个单元格支持多值（SaaS 工具侧支持）

示例：
```
>静态电压\稳定性
>静态电压\监测方法
>静态电压\PCMLE
>动态响应\瞬态抑制
>动态响应\环路补偿\Type-III补偿
```

## Part D — Precision Validation

1. Random-sample ~20–30 hits per branch.
2. Read title + abstract, judge relevant / not-relevant.
3. Report precision = relevant / N per branch.
4. Branches < 80% must be tightened before proceeding.
5. Recall sanity: sample hits just outside the boundary to check false negatives.
