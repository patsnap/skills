# Applicant Analysis Prompt — 申请人分析

## 任务
基于全量申请人排名数据，生成申请人格局分析。

## 输入
- full_scope_metrics.top_applicants：全球 Top 20 申请人（全量）
- evidence_sample：代表专利（用于示例）

## 分析维度

### 1. 申请人类型识别
对每个 Top 20 申请人，判断类型：
- 企业（国内企业/跨国企业）
- 高校
- 科研机构/国家实验室
- 个人发明人
- 产学研联合体

### 2. 竞争集中度计算
- Top 3 申请人占比（CR3）= Top3 申请量之和 / 总量
- Top 5 申请人占比（CR5）
- HHI 估算（如数据支持）
- 判断：高度集中（CR5>60%）/ 中度集中（30%-60%）/ 分散（<30%）

### 3. 技术领导者识别
- 申请量最大者
- 技术布局最广者（如有 IPC 分布数据）
- 中国领导者 vs 国际领导者

### 4. 新进入者信号
- 近三年新出现的申请人
- 中小机构的快速增长

### 5. 产学研合作分析
- 高校/科研机构在 Top 20 中的比例
- 是否存在联合申请模式
- 基础研究 vs 应用研究倾向

## 输出格式
```json
{
  "applicant_analysis": {
    "top_applicants_detail": [
      {
        "rank": 1,
        "name": "申请人名",
        "count": 456,
        "country": "CN",
        "type": "企业",
        "description": "简要描述该申请人定位"
      }
    ],
    "cr3": 0.423,
    "cr5": 0.561,
    "concentration_level": "中度集中",
    "cn_leaders": ["申请人1", "申请人2"],
    "intl_leaders": ["申请人A", "申请人B"],
    "academia_ratio": 0.25,
    "emerging_players": ["近年快速增长的申请人"],
    "competition_conclusion": "该领域呈中度集中格局，前五名申请人共持有约56%的专利，以国内企业为主，高校比例约25%，产学研合作活跃。"
  }
}
```
