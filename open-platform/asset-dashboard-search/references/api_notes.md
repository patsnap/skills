# API 调用说明

## 鉴权
所有接口使用 Bearer Token 鉴权：
```
Authorization: Bearer <token>
```

## collapse 参数说明
| 参数 | 值 | 说明 |
|------|----|------|
| `collapse_by` | `PBD` | 按公开日合并 |
| `collapse_type` | `APNO` | 按申请号去重 |
| `collapse_order` | `LATEST` | 取最新公开的版本 |
| `collapse_order_authority` | `["CN","US","EP",...]` | 国家优先级顺序 |

## P002 接口
- **地址**：`https://connect.zhihuiya.com/search/patent/query-search-patent/v2`
- **方法**：POST
- **查询语法**：`ANCS:(申请人名称)`
- **测试时间**：2026-05-27
- **测试状态**：✅ 有效
