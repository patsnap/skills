# 专利同族合并规则 — mab-fto-check

## 一、同族合并时机

在步骤4（地域+法律状态过滤）执行后，对 `patent_pool_filtered.json` 中所有专利按 INPADOC 同族进行合并，输出 `patent_pool_family.json`。

---

## 二、同族分组规则

```
分组依据：INPADOC 同族ID（通过 patsnap_fetch module=family 获取）
分组键：priority_number（最早优先权号）
命名规则：以家族序号（1-1, 1-2...）标记，同族内按风险等级→申请时间排序
```

### 分组字段
```json
{
  "family_id": "WO2009086320A1",
  "family_seq": "1",
  "priority_date": "2007-12-26",
  "family_members": [
    {
      "seq": "1-1",
      "patent_number": "EP2444423B1",
      "jurisdiction": "EP",
      "legal_status": "active",
      "grant_status": "granted",
      "expiry_date": "2028-09-22",
      "display_text": "B文本",
      "fetch_module": "basic"
    }
  ],
  "representative_claim": "（取授权成员的独立权利要求1）",
  "risk_level": "high",
  "assignee": "Xencor Inc."
}
```

---

## 三、B文本展示规则

### 3.1 何为B文本
- `B1`/`B2`/`B` 后缀专利 = 已授权公告文本（Granted Patent）
- `A1`/`A2` 后缀 = 公开申请文本（尚未授权）
- `B文本` 优先级高于 `A文本`，代表最终授权的权利要求范围

### 3.2 B文本获取流程
```
Step 1: 检查 family_members 中是否存在 grant_status = "granted"
Step 2: 若存在 → 调用 patsnap_fetch(pn=「B号」, module=["basic"]) 获取完整权利要求
Step 3: 提取 claims 字段中的独立权利要求（Independent Claim）
Step 4: 将B文本权利要求作为 representative_claim 写入family记录
Step 5: 报告第四章中优先展示B文本独立权利要求（含原文+中文译文）
```

### 3.3 无B文本处理
```
若同族内所有成员均为A文本（审中）→
  取最新修改的权利要求（Office Action Reply后的claim版本）
  标注：「审中申请，权利要求可能变化，按当前版本评估」
```

### 3.4 多个B文本的选取优先级
```
优先级顺序（按目标市场）：
1. 与用户目标市场匹配的B文本（CN优先CN、US优先US）
2. EP已授权B文本
3. 最早授权的B文本
```

---

## 四、报告中的家族展示格式

### 专利列表表格（第三章3.4节）

```
专利家族 | 序号  | 公开（公告）号    | 申请日     | 法律状态 | 失效日     | 专利权人    | 风险等级 | B文本
---------|-------|------------------|------------|----------|------------|-------------|----------|---------
1        | 1-1   | EP2444423B1      | 2008-09-22 | 授权     | 2028-09-22 | Xencor Inc. | 高       | ✅
1        | 1-2   | CN105418762B     | 2008-12-22 | 授权     | 2028-12-22 | Xencor      | 高       | ✅
1        | 1-9   | US20240327508A1  | 2024-06-14 | 公开/审中| —          | Xencor Inc. | 中       | ❌
```

**注释模板：**
```
注1：序号以专利家族分组，「组号-顺序号」排列（1-1, 1-2…）；组内按风险等级降低、申请时间递增排序；组间按风险等级由高到低排序。
注2：失效日含PTA/PTE补偿的，已标注。
注3：欧洲专利SPC保护期不计入失效日，如有上市需另行确认。
注4：B文本列「✅」表示已获取授权文本用于权利要求比对；「❌」表示仅有A申请文本。
```

---

## 五、patent_pool_family.json 字段规范

```json
[
  {
    "family_seq": "1",
    "family_id": "WO2009086320A1",
    "priority_date": "2007-12-26",
    "assignee": ["Xencor Inc."],
    "risk_level": "high",
    "representative_pn": "EP2444423B1",
    "representative_claim_text": "（B文本独立权利要求原文）",
    "representative_claim_cn": "（中文译文）",
    "claim_source": "B文本|A文本（审中）",
    "members": [
      {
        "seq": "1-1",
        "pn": "EP2444423B1",
        "jurisdiction": "EP",
        "legal_status": "active",
        "grant_status": "granted",
        "application_date": "2008-09-22",
        "expiry_date": "2028-09-22",
        "pta_applied": false
      }
    ],
    "source_modules": ["M1", "M2"],
    "notes": ""
  }
]
```

---

## 六、同族合并对风险评级的影响

```
规则1：同族内任一成员为高风险 → 整个家族标记为高风险
规则2：同族内高风险成员均在目标市场已到期 → 降级为「地域豁免」
规则3：同族命中多个检索模块（source_modules长度>1）→ 风险权重上调
规则4：同族内有PCT申请且国家阶段未确认 → 附加「PCT空窗期」标注
```
