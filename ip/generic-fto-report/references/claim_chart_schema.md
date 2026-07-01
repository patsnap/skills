# Claim Chart JSON Schema 文档（Fix #7）

> **用途**：指导 Claude 在阶段二生成 `--claim-chart` 参数所需的 JSON 结构。

## 文件来源

阶段一完成后，`fto_main.py` 输出：
- `candidates_claims.json`：候选专利 + 权利要求1 原文
- `fto_result.json`：AI07 比对 prompt（`_ai07_prompt` 字段）

Claude 读取上述文件，通过 `zhihuiya-local` MCP `ai_chat` 工具执行 AI07 比对，然后按本 Schema 生成 `claim_chart.json`。

---

## 顶层结构

```json
[
  { /* PatentComparisonResult 对象，见下方 */ },
  { /* ... */ }
]
```

---

## PatentComparisonResult 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `patent_id` | string | ✅ | 智慧芽专利 UUID（可为空串） |
| `pn` | string | ✅ | 公开号，如 `"CN106488683B"` |
| `title` | string | ✅ | 专利中文标题 |
| `claim1` | string | ✅ | 权利要求1 完整原文（从 P018 获取） |
| `risk_level` | string | ✅ | `"High"` / `"Medium"` / `"Low"` |
| `features_comparison` | array | ✅ | 逐条技术特征比对，见下方 |
| `conclusion` | object | ✅ | 总体结论，见下方 |

---

## features_comparison 元素

| 字段 | 类型 | 说明 |
|------|------|------|
| `claim_feature` | string | 权利要求中的技术特征原文片段 |
| `product_feature` | string | 标的产品对应的技术特征描述 |
| `similar` | boolean | 是否相似/覆盖：`true` = 覆盖，`false` = 不覆盖 |
| `match_type` | string | `"identical"` / `"equivalent"` / `"missing"` |
| `score` | integer | 相似度评分 0–100 |
| `reasoning` | string | AI07 给出的比对理由（中文，1–2 句） |

---

## conclusion 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| `infringement_type` | string | `"literal"` 字面侵权 / `"equivalent"` 等同侵权 / `"no_infringement"` 不侵权 |
| `risk_summary` | string | AI07 输出的侵权比对总结（中文，3–5 句） |
| `recommendation` | string | 应对建议，如绕过设计方案、无效化策略等 |

---

## 完整示例

```json
[
  {
    "patent_id": "8a3b2c1d-...",
    "pn": "CN106488683B",
    "title": "一种具有定位功能的滑轨总成",
    "claim1": "一种滑轨总成，包括外轨、中轨和内轨...",
    "risk_level": "Medium",
    "features_comparison": [
      {
        "claim_feature": "卡勾设置于中轨后端，可向上弹起",
        "product_feature": "标的产品后定位挡片弹开锁定结构",
        "similar": true,
        "match_type": "equivalent",
        "score": 72,
        "reasoning": "功能相似（均为后端弹性定位），但标的产品挡片可活动、专利卡勾固定，存在结构差异。"
      },
      {
        "claim_feature": "弹性件设置于外轨内侧",
        "product_feature": "标的产品弹片集成于珠巢组件",
        "similar": false,
        "match_type": "missing",
        "score": 30,
        "reasoning": "安装位置不同，标的产品弹性元件位于内轨，而非外轨内侧。"
      }
    ],
    "conclusion": {
      "infringement_type": "equivalent",
      "risk_summary": "标的产品与本专利存在等同技术特征，均实现后端弹性定位锁定功能，区别在于弹性元件集成方式不同。建议律师深度审查等同侵权风险。",
      "recommendation": "建议调整挡片驱动方式，使其与权利要求技术方案在结构和原理上存在可辨别差异；或委托律师准备无效请求。"
    }
  }
]
```

---

## 注意事项

1. `risk_level` 由 AI07 综合 `features_comparison` 给出，**不可由人工修改后省略 `features_comparison`**。
2. `reasoning` 必须是 AI07 真实输出，不可由 Claude 模型直接编写后略过 AI07 调用。
3. 若某条专利 P018 未返回权利要求（`claim1` 为空），`risk_level` 填 `"Unknown"`，`conclusion.risk_summary` 填 `"缺少权利要求，无法比对"`。
