# 智慧芽 MCP 工具调用路由手册

## 适用范围
本文件定义 experiment-dataset-costing 技能中各步骤对应的 MCP 工具调用方式，
供代码生成与步骤执行参考。

---

## Step 1：实体规范化

```python
# 工具：ls_ner_nor_normalize
# 用途：将用户输入的靶点名称标准化为内部 ID
result = ls_ner_nor_normalize(
    user_input="PD-L1 and 4-1BB dual target small molecule"
)
# 返回：entities_standardize_info（JSON string）
# 提取：target_id, normalized_name, uniprot_id
```

---

## Step 2：药物情报检索

```python
# 工具：ls_drug_search
# 用途：统计靶点相关药物数量，评估靶点热度
drug_results = ls_drug_search(
    target=["PD-L1", "4-1BB"],
    highest_phase=["approved", "phase_3", "phase_2"],
    limit=100
)
# 关注字段：total（总数）, items（药物列表）

# 工具：ls_target_fetch
target_info = ls_target_fetch(target=["PD-L1", "4-1BB"])
# 关注字段：结构域、表达谱、通路注释
```

---

## Step 3：专利化学结构估算

```python
# Step 3a：检索化合物专利数量
patent_results = ls_patent_search(
    target=["PD-L1", "4-1BB"],
    patent_core_type=["product_compound"],
    limit=20
)
# 关注字段：total（总专利数）

# Step 3b：获取代表性专利的化合物列表
for pn in top_patent_numbers[:10]:
    structure_data = ls_patent_structure_fetch(pn=pn, limit=100)
    # 返回：total（化合物总数）, items（SMILES列表）

# Step 3c：SAR 结构-活性提取
import time
for pn in selected_patents[:5]:  # 建议先试提取5件
    task = ls_sar_submit(pn=pn, language="EN")
    while True:
        result = ls_sar_fetch(task_id=task["task_id"])
        if result["status"] in ["SUCCESS", "FAILED"]:
            break
        time.sleep(10)  # 等待10秒后重试
```

---

## Step 4：ADMET 预筛选

```python
# 工具：ls_admet_predict
# 批量限制：每次最多100个 SMILES
batch_size = 100
all_predictions = []
for i in range(0, len(smiles_list), batch_size):
    batch = smiles_list[i:i+batch_size]
    result = ls_admet_predict(smiles=batch)
    all_predictions.extend(result["predictions"])

# 过滤条件（可配置）
AMES_THRESHOLD = 0.7     # AMES阳性概率上限
hERG_THRESHOLD = 0.9     # hERG阻断概率上限

filtered = [
    p for p in all_predictions
    if p["properties"]["AMES"] < AMES_THRESHOLD
    and p["properties"]["hERG"] < hERG_THRESHOLD
]
retention_rate = len(filtered) / len(all_predictions)
```

---

## Step 5：文献数据量评估

```python
# 工具：ls_paper_search
paper_results = ls_paper_search(
    target=["PD-L1", "4-1BB"],
    limit=1  # 仅需 total 数量
)
total_papers = paper_results["total"]

# 工具：ls_translational_medicine_search
tm_results = ls_translational_medicine_search(
    target=["PD-L1", "4-1BB"],
    limit=1
)
total_tm = tm_results["total"]

# 经验估算：每1000篇文献可提取约50–200条有效数值数据
estimated_literature_data = total_papers * 0.1  # 保守估算10%可提取率
```

---

## Step 6：合规性评估

```python
# 读取 references/compliance_rules.md 规则模板
# 根据 use_case（academic/commercial）自动生成合规矩阵

DATA_SOURCE_COMPLIANCE = {
    "ChEMBL":       {"academic": "✅", "commercial": "✅",  "risk": "低"},
    "BindingDB":    {"academic": "✅", "commercial": "✅",  "risk": "低"},
    "PubChem":      {"academic": "✅", "commercial": "✅",  "risk": "极低"},
    "PDB":          {"academic": "✅", "commercial": "✅",  "risk": "极低"},
    "Patent-SAR":   {"academic": "✅", "commercial": "⚠️", "risk": "中-高"},
    "PatSnap-MCP":  {"academic": "✅", "commercial": "✅",  "risk": "低"},
    "Literature":   {"academic": "✅", "commercial": "✅",  "risk": "极低"},
    "ZINC":         {"academic": "✅", "commercial": "⚠️", "risk": "中"},
}
```

---

## Step 7：成本估算

```python
# 读取 references/cost_benchmarks.md 基准参数
# 根据实际数据量和专利件数计算工时区间

def estimate_cost(n_compounds, n_patents, n_targets, use_case):
    unit = max(n_compounds / 10000, 1)
    patent_unit = max(n_patents / 20, 1)
    days = {
        "collection":  {"low": n_targets*1.0, "mid": n_targets*2.0,    "high": n_targets*4.0},
        "cleaning":    {"low": unit*1.5,      "mid": unit*3.5,         "high": unit*6.0},
        "admet":       {"low": (n_compounds/1000)*0.3, "mid": (n_compounds/1000)*0.5, "high": (n_compounds/1000)*0.8},
        "patent_sar":  {"low": patent_unit*0.5, "mid": patent_unit*1.0, "high": patent_unit*2.0},
        "report":      {"low": 0.5,           "mid": 1.0,              "high": 2.0},
    }
    if use_case == "commercial":
        days["compliance"] = {"low": 2.0, "mid": 4.0, "high": 8.0}
    total = {k: round(sum(v[k] for v in days.values()), 1) for k in ["low","mid","high"]}
    return {"breakdown": days, "total": total}
```
