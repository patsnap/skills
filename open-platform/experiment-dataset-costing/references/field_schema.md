# 数据集字段规范参考

## 适用范围
本文件定义数据集构建的标准字段体系，适用于小分子、抗体/双抗、融合蛋白三类分子类型。

---

## 一、小分子数据集字段

### 必须字段

```
compound_id          : str   # 化合物唯一标识（来源库_原始ID，如 ChEMBL_CHEMBL123456）
smiles               : str   # 标准化 SMILES（经 RDKit Chem.MolToSmiles 规范化）
inchi_key            : str   # InChIKey（去重主键，27位标准格式）
target_name          : str   # 靶点名称（标准化，如 PD-L1 / 4-1BB / PD-L1+4-1BB）
target_uniprot       : str   # UniProt ID（如 Q9NZQ7 for PD-L1；Q07011 for 4-1BB）
activity_type        : str   # 活性类型（IC50 / Ki / Kd / EC50 / %Inhibition）
activity_value       : float # 活性数值（原始单位）
activity_unit        : str   # 单位（nM / μM / M / %）
pactivity            : float # pActivity = -log10(value_in_M)，统一比较量
activity_label       : str   # active(pActivity≥6) / inactive(pActivity<5) / ambiguous
data_source          : str   # 来源（ChEMBL / BindingDB / PubChem / Patent-SAR / Literature）
assay_type           : str   # 测试类型（Biochemical / Cellular / In_vivo）
reference_id         : str   # 参考文献标识（DOI / 专利号 / ChEMBL Assay ID）
```

### 推荐补充字段

```
molecular_weight     : float # 分子量（Da）
logP                 : float # 脂水分配系数
tpsa                 : float # 拓扑极性表面积（Å²）
hbd                  : int   # 氢键供体数
hba                  : int   # 氢键受体数
rotatable_bonds      : int   # 可旋转键数
ro5_pass             : bool  # 是否符合 Lipinski 五规则
admet_ames           : float # AMES 致突变概率（0–1）
admet_herg           : float # hERG 阻断概率（0–1）
admet_bbb            : float # 血脑屏障穿透概率（0–1）
admet_bioavailability: float # 口服生物利用度概率（0–1）
patent_status        : str   # 相关专利法律状态（active/inactive/pending/unknown）
scaffold_murcko      : str   # Murcko 骨架 SMILES（用于数据集分割）
cluster_id           : int   # Butina 聚类 ID（用于多样性评估）
data_split           : str   # train / val / test_in / test_out
```

---

## 二、抗体/双特异性抗体数据集字段

```
antibody_id          : str   # 抗体唯一标识
heavy_chain_seq      : str   # 重链氨基酸序列（FASTA格式）
light_chain_seq      : str   # 轻链氨基酸序列
hcdr1/2/3            : str   # 重链 CDR 1/2/3 序列（Chothia/IMGT编号）
lcdr1/2/3            : str   # 轻链 CDR 1/2/3 序列
target_1             : str   # 第一靶点名称
target_2             : str   # 第二靶点名称（双特异性）
binding_kd_target1   : float # 对靶点1的解离常数 Kd（nM）
binding_kd_target2   : float # 对靶点2的解离常数 Kd（nM）
selectivity_ratio    : float # 双靶选择性比值
epitope_pdb          : str   # 结合表位 PDB 条目
antibody_type        : str   # mAb / bispecific / nanobody / fusion_protein
data_source          : str   # 来源
reference_id         : str   # 参考文献
```

---

## 三、活性阈值定义

| pActivity 值 | 活性标签 | 对应浓度 | 说明 |
|---|---|---|---|
| ≥ 8.0 | highly_active | ≤ 10 nM | 高活性，适合先导化合物优化 |
| 6.0–7.99 | active | 10 nM–1 μM | 活性，进入正样本集 |
| 5.0–5.99 | weakly_active | 1–10 μM | 弱活性，可作为边界样本 |
| < 5.0 | inactive | > 10 μM | 非活性，进入负样本集 |
| 无数据 | unknown | — | 排除或单独处理 |

---

## 四、数据集分割策略

```python
# 推荐分割方案（基于 Murcko 骨架）
train_ratio      = 0.70   # 训练集
val_ratio        = 0.15   # 验证集
test_in_ratio    = 0.08   # 插值测试集（骨架内）
test_out_ratio   = 0.07   # 外推测试集（仅未见骨架）

# 推荐工具
# from rdkit.Chem.Scaffolds import MurckoScaffold
# 或使用 deepchem.splits.ScaffoldSplitter
```
