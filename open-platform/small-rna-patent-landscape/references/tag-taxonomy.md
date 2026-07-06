# Small RNA Patent Tag Taxonomy

Use these tags for company-level small RNA patent landscape analysis. Keep expert tags for analytical precision and Chinese customer-readable tags for the default dashboard.

## Customer-Readable Technology Directions

Use these as the default HTML swimlanes.

| Tag | Meaning |
|---|---|
| 眼科/视网膜-视神经疾病 ASO | ASO assets for OPA1, PRPF31, retinal or optic nerve disease; shows expansion into ophthalmic local delivery scenarios. |
| 肾脏疾病 ASO | ASO assets for PKD or other kidney/renal expression diseases. |
| 中枢神经遗传病蛋白上调 ASO | CNS genetic disease ASOs, commonly SCN1A/Dravet/Nav1.1, whose goal is protein upregulation. |
| 中枢神经发育障碍蛋白上调 ASO | CNS neurodevelopmental disease ASOs such as SYNGAP1, focused on increasing insufficient protein expression. |
| 罕见病靶点拓展 ASO | LIPA, JAG1, TSC or other rare-disease target expansion showing platform portability. |
| NMD/隐蔽外显子调控平台 | Mechanism-platform patents around NMD escape, cryptic exon, poison exon or ASCE-like regulation. |
| 通用 ASO 化学与序列平台 | Broad ASO chemistry, sequence, backbone, candidate selection or platform claims not limited to one asset. |
| 制剂、递送与剂量优化 | Productization-layer claims covering formulation, route, regimen, dose, buffer, concentration or clinical use. |

Mapping rule: if the patent is clearly a clinical dosing/formulation follow-on, classify as `制剂、递送与剂量优化`; otherwise map by disease/asset first, then mechanism platform, then broad ASO platform.

## Expert Primary Tags

Use these in XLSX and hover cards as professional subdivisions:

- `SCN1A / Dravet / Nav1.1`
- `OPA1 / 常染色体显性视神经萎缩`
- `PKD / 多囊肾`
- `SYNGAP1 / CNS neurodevelopment`
- `NMD-sensitive ASCE platform`
- `Broad ASO platform / target not explicit`
- `LIPA / CESD`
- `PRPF31 / RP13`
- `TSC / Tuberous sclerosis`
- `JAG1 / Alagille`
- `Liver disease`

## Mechanism Tags

- 剪接转换 / 外显子纳入
- 隐蔽外显子 / 毒性外显子调控
- NMD抑制 / 逃逸
- 蛋白表达上调
- RNase H / gapmer介导降解
- 患者筛选 / 诊断准入
- 剂量方案优化
- ASO靶向调控

## RNA Modality Tags

- 单链ASO / 剪接转换ASO
- PMO / 吗啉代ASO
- dsRNA / siRNA
- mRNA
- 小核酸/寡核苷酸

## Chemistry/Structure Tags

- 硫代磷酸酯骨架
- 2'-MOE修饰
- 2'-OMe修饰
- 2'-F修饰
- 5-甲基胞嘧啶
- LNA/BNA/cEt构象锁定核苷酸
- PMO / 磷酰二胺吗啉代骨架
- gapmer / wingmer结构
- 序列限定候选物
- 权利要求解析中未明确化学修饰

## Delivery/Tissue Tags

- 中枢神经 / 鞘内给药
- 眼科 / 玻璃体腔给药
- 肾脏 / 肾病
- 肝脏 / 肝细胞
- 系统给药
- 制剂 / 辅料
- 递送非核心或未明确

## Productization Stage Tags

- 核心发明 / 平台族基础
- 国家进入 / 审查推进
- 授权保护 / 可执行权利
- 续案 / 权利要求范围细化
- 临床剂量 / 制剂延伸
- 患者分层 / 诊断赋能

## Importance Heuristics

Use `高 / 中高 / 中 / 低` or numeric levels `3 / 2 / 1 / 0`.

Increase importance for:

- large family count or broad country entry
- US/CN/EP/JP active prosecution or grant
- core PCT family anchor
- granted rights
- sequence or compound claims
- clinical dosing/formulation/patient selection layer
- clear asset or platform relationship

Decrease importance for:

- isolated single-country applications
- unclear technical content
- family appears expired or inactive across key jurisdictions
