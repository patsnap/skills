---
name: asset-dashboard-search
description: 专利资产看板检索技能，封装多个智慧芽专利检索API能力，支持按申请人、关键词等维度检索专利，返回去重后的专利列表。
---

# asset-dashboard-search

## 概述
本技能封装了多个智慧芽专利检索API能力，用于专利资产看板场景下的专利数据获取。
每个子能力以 P00X / A00X / S00X / D00X 编号标识，逐步扩充。

## 鉴权方式
所有接口均通过 HTTP Header 传递 API Token：
```
Authorization: Bearer <token>
```
Token 通过环境变量 `ZHIHUIYA_API_TOKEN` 注入，或通过 `--token` 参数传入。

---

## 公共固定请求体参数（所有 P002 系列共用）

```json
{
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> ⚠️ **不得添加 `collapse_order_authority` 字段**，否则会导致 CN 申请量统计偏差。

---

## P002 — 按申请人检索全部专利（合并同族）

### 接口信息
- **方法**：POST
- **地址**：`https://connect.zhihuiya.com/search/patent/query-search-patent/v2`

### 请求体
```json
{
  "query_text": "ANCS:(申请人名称)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

### 数据路径
```python
total = result["data"]["total_search_result_count"]
patents = result["data"]["results"]
```

### 测试验证记录
| 测试申请人 | 返回总数 | 状态 |
|-----------|---------|------|
| 北京低碳清洁能源研究院 | 3,341 | ✅ |
| 国家能源集团科学技术研究院有限公司 | 1,463 | ✅ |

---

## P002B — 按申请人检索授权发明专利

### 请求体
```json
{
  "query_text": "ANCS:(申请人名称) and PATENT_TYPE:(B)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

---

## P002U — 按申请人检索实用新型专利

### 请求体
```json
{
  "query_text": "ANCS:(申请人名称) and PATENT_TYPE:(U)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

---

## P002D — 按申请人检索外观设计专利

### 请求体
```json
{
  "query_text": "ANCS:(申请人名称) and PATENT_TYPE:(D)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> 部分企业无外观设计专利，返回 `total_search_result_count = 0`。

---

## A001 — 申请趋势（近10年：2016—2025）

### 接口信息
- **方法**：POST
- **地址**：`https://connect.zhihuiya.com/insights-openapi/patent-trends-query`

### 请求体参数
```json
{
  "query_text": "ANCS:(申请人名称)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> ⚠️ 不得添加 `collapse_order_authority`。

### 返回结构
```json
{
  "status": true,
  "data": [
    {"year": "2016", "application": 163, "granted": 133, "percentage": 0.816},
    ...
  ]
}
```
> `data` 是**直接数组**，用 `result["data"]` 取列表，再按年份过滤 2016—2025。

### 过滤逻辑
```python
years_10 = [str(y) for y in range(2016, 2026)]
trend_10y = [item for item in result["data"] if item["year"] in years_10]
```

---

## S001 — 战略新兴产业分布检索

### 接口信息
- **方法**：POST
- **地址**：`https://connect.zhihuiya.com/search/patent/query-search-patent/v2`

### 9个产业标签（固定顺序，循环9次）
1. 新材料产业
2. 节能环保产业
3. 新能源汽车产业
4. 新能源产业
5. 生物产业
6. 高端装备制造产业
7. 新一代信息技术产业
8. 相关服务业
9. 数字创意产业

### 请求体（每次循环）
```json
{
  "query_text": "ANCS:(申请人名称) and SEIC:(产业名称)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

### 循环逻辑
```python
seic_list = [
    "新材料产业", "节能环保产业", "新能源汽车产业", "新能源产业",
    "生物产业", "高端装备制造产业", "新一代信息技术产业", "相关服务业", "数字创意产业"
]
results = {}
for seic in seic_list:
    query = f"ANCS:({applicant_name}) and SEIC:({seic})"
    results[seic] = total_count
```

---

## D109 — 海外布局（受理局分布）

### 接口信息
- **方法**：POST
- **地址**：`https://connect.zhihuiya.com/shhgy/reportdata/rec-office`

### 请求体参数
```json
{
  "query_text": "ANCS:(申请人名称)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> ⚠️ **严禁添加 `collapse_order_authority` 字段**，否则 CN 申请量会从 13,378 变成 16,179（宝山钢铁已验证）。

### 海外申请量计算规则
`海外申请量 = 所有受理局之和 - 中国（CN）申请量`

### 返回结构
```json
{
  "data": {
    "values": [
      {"rec_office": "中国", "code": "CN", "num": 13378},
      {"rec_office": "欧洲", "code": "EP", "num": 628},
      ...
    ]
  }
}
```

### 计算逻辑
```python
values = result["data"]["values"]
total_all = sum(item["num"] for item in values)
cn_count = next((item["num"] for item in values if item["code"] == "CN"), 0)
overseas_count = total_all - cn_count
```

### 测试验证记录
| 申请人 | 总量 | CN | 海外 |
|--------|------|----|------|
| 北京低碳清洁能源研究院 | 3,341 | 3,066 | 275 ✅ |
| 宝山钢铁股份有限公司 | 17,088 | 13,378 | 3,710 ✅ |

---

## A006 — 重点发明人（有效专利持有数量）

### 接口信息
- **方法**：GET
- **地址**：`https://connect.zhihuiya.com/insights/inventor-ranking`

### query_text 格式
```
ANCS:(申请人名称) and SIMPLE_LEGAL_STATUS:(1) and PATENT_TYPE:(B or U or D)
```

### 返回结构
```json
{
  "data": [
    {"name": "孙琦", "count": 137},
    ...
  ]
}
```

### 数据路径
```python
inventors = result["data"]  # 直接数组，按count降序
```

---

## A002 — 创新词云

### 接口信息
- **方法**：POST
- **地址**：`https://connect.zhihuiya.com/insights/word-cloud-query`

### 请求体参数（完整，缺一不可）
```json
{
  "lang": "cn",
  "query_text": "ANCS:(申请人名称)",
  "collapse_by": "PBD",
  "collapse_type": "DOCDB",
  "collapse_order": "LATEST"
}
```
> ⚠️ 本接口 `collapse_type` 使用 **`DOCDB`**，与其他接口不同（其他用 `APNO`）。
> ⚠️ 必须传入 `lang`、`collapse_by`、`collapse_order`，缺少任一将导致结果不准确。

### 数据路径
```python
words = result["data"]  # 直接数组，100个词条，按count降序
```

---

## 能力汇总

| 能力编号 | 方法 | 接口 | 说明 |
|----------|------|------|------|
| P002 | POST | query-search-patent/v2 | 全类型专利 |
| P002B | POST | query-search-patent/v2 | 授权发明专利 |
| P002U | POST | query-search-patent/v2 | 实用新型专利 |
| P002D | POST | query-search-patent/v2 | 外观设计专利 |
| A001 | POST | patent-trends-query | 申请趋势（近10年 2016—2025） |
| S001 | POST | query-search-patent/v2 | 战略新兴产业分布（9次循环） |
| D109 | POST | rec-office | 海外布局（海外=总量-CN，禁用collapse_order_authority） |
| A006 | GET | inventor-ranking | 重点发明人（有效专利持有数量） |
| A002 | POST | word-cloud-query | 创新词云（lang=cn，collapse_type=DOCDB） |

---

## 待扩充能力
- 更多能力持续补充中

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
