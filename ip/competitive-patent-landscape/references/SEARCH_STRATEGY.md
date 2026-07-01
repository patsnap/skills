# 专利检索策略参考

## 每品牌检索模板

### 策略一：按申请人+关键词（推荐首选）
```json
{
  "search_strategy": ["keyword", "filter"],
  "keywords": ["tissue", "facial tissue", "handkerchief"],
  "filters": {
    "assignees": ["Kimberly-Clark"],
    "date_from": 20210101,
    "date_to": 20261231,
    "date_type": "publication"
  },
  "sources": ["patent"],
  "topk": 80
}
```

### 策略二：语义检索（补充用）
```json
{
  "search_strategy": ["semantic", "filter"],
  "semantic_query": "facial tissue softness technology innovation new product development",
  "filters": {
    "assignees": ["Procter Gamble"],
    "date_from": 20210101
  },
  "sources": ["patent"],
  "topk": 50
}
```

## 日本品牌补充检索
日本品牌（大王制纸、王子制纸等）需额外使用申请人精确过滤：
- 大王制纸：`["Daio Paper", "大王製紙"]`
- 王子制纸：`["Oji Paper", "Oji Holdings", "王子製紙"]`

## IPC 技术路线映射

| 技术路线名称 | 对应 IPC 大组 |
|------|------|
| 柔软/强韧工艺 | D21H, D21F |
| 保湿/护肤配方 | A61K, D21H11 |
| 可持续纤维/原料 | D21H11/12, D21C |
| 包装/产品形态 | B65D, B65B |
| 制造工艺/设备 | D21F, B31F, D21G |
| 新材料 | D21H17, C01F |

## 核心专利精读选取原则
1. 引用量最高的 Top 3
2. 最新申请年份（2023-2025）中有战略信号的
3. 覆盖 WO/PCT 路径的（说明意图全球布局）
4. 每品牌最多 fetch 3 件，控制 token 消耗

## 跨市场对比检索
若同一品牌在多个市场（如金佰利美国+欧洲），需：
1. 分别检索 jurisdiction=["US"] 和 jurisdiction=["EP"]
2. 统计各市场 IPC 分布差异
3. 识别仅在某一市场布局的独有技术方向
