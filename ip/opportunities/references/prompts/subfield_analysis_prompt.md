# Subfield Analysis Prompt — 子技术分支分析

## 任务
将技术方向拆分为 4-8 个子技术分支，并对每个分支进行机会评估。

## 子技术分支拆分原则

### 拆分维度（按领域选择）
- **材料领域**：按材料类型 / 功能性质 / 制备工艺 / 应用场景
- **能源领域**：按器件部件 / 性能优化目标 / 制备工艺 / 系统集成
- **生物医药**：按适应症 / 靶点类型 / 给药途径 / 剂型
- **化工领域**：按合成路线 / 催化剂类型 / 产品形态 / 应用终端
- **电子信息**：按电路/器件 / 算法/协议 / 应用场景 / 制造工艺

### 拆分规则
- 分支数量：4-8 个（不得少于 4，不得超过 8）
- 每个分支必须有独立的检索式
- 分支之间应尽量互斥且完全覆盖主技术方向
- 分支名称应简洁专业（不超过 15 字）

## 每个分支的分析内容

### 数据采集（全量统计）
- 独立检索该子方向，获取 total_count（全量，不是 TopK50）
- 通过 `patsnap-patent-technology-landscape__trends` 获取该子方向趋势
- 通过 `patsnap-patent-technology-landscape__applicant_ranking` 获取子方向申请人排名

### 机会评估维度
1. **专利数量**（来自全量统计）
2. **近五年增长趋势**（来自全量统计）
3. **竞争强度**（申请人集中度，来自全量统计）
4. **技术成熟度**（基于申请趋势阶段判断）
5. **代表专利质量**（来自 evidence_sample）
6. **机会评分**（1-10）

### 进入建议判断标准
- **推荐进入**：增长强劲 + 竞争分散 + 专利数量适中（有空间）
- **谨慎进入**：增长中等 OR 竞争较高 OR 技术成熟度高
- **暂不建议进入**：增长停滞 + 高度集中 + 大量有效专利封锁

## 输出格式
```json
{
  "subfield_analysis": [
    {
      "subfield_id": "SF01",
      "name": "子技术方向名称",
      "description": "技术描述（2-3句话）",
      "query": "检索式",
      "total_count": 1234,
      "total_count_source": "trends_mcp / bucketing_search",
      "trend_5yr": "持续增长/快速增长/稳定/下降",
      "cagr_5yr": 0.189,
      "competition_level": "高/中/低",
      "maturity": "起步期/成长期/成熟期",
      "representative_patents": ["CN1234567A", "US9876543B2"],
      "key_applicants": ["申请人1", "申请人2"],
      "opportunity_score": 7.5,
      "entry_recommendation": "推荐进入",
      "opportunity_description": "该子方向专利布局相对分散，近五年增长率高，适合切入",
      "risk_description": "主要风险：XX公司已有较强布局",
      "gap_description": "空白点：XX应用场景专利布局不足"
    }
  ]
}
```
