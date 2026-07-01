# 鸿远门户当前状态（2026-05-27 更新）

## 文件位置

- 项目根目录：`/Users/tianxiaochen/hongyuan-portal/`
- 前端文件：`/Users/tianxiaochen/hongyuan-portal/public/index.html`（当前约1934行）
- 后端文件：`/Users/tianxiaochen/hongyuan-portal/server.js`
- 环境配置：`/Users/tianxiaochen/hongyuan-portal/.env`
- 备份文件：`/Users/tianxiaochen/hongyuan-portal/public/index.html.bak`

## 启动方式

```bash
cd ~/hongyuan-portal && node server.js
# 访问 http://localhost:3000
```

## index.html 关键结构（1934行）

### HTML页面区块（顺序）

| id | 行号 | 说明 |
|----|------|------|
| page-home | ~400 | 情报总览首页，含竞品雷达4张card |
| page-weekly | ~500 | 本周技术情报详情页 |
| page-search | ~650 | 专利/论文检索页 |
| page-competitor | ~729 | 旧版竞品监控页（含cd-patents，已停用跳转） |
| page-comp-detail | ~1577 | 新版竞品详情页（含cd-patents-detail） |
| page-workspace | 后段 | 研究工作台 |

### 关键DOM元素

| id | 所在页面 | 说明 |
|----|----------|------|
| cd-patents | page-competitor（行741） | 旧版，已不用于跳转 |
| cd-patents-detail | page-comp-detail | 新版，竞品详情专利列表渲染目标 |
| cd-total/cd-active/cd-pending/cd-maxcite | page-comp-detail | 统计数字 |
| cd-name/cd-desc | page-comp-detail | 竞品名称/描述 |
| cd-stats | page-competitor（行733） | 旧版统计行（不用了） |

### 关键JS函数位置

| 函数名 | 行号 | 说明 |
|--------|------|------|
| showPage | ~759（已被新版覆盖，旧版已删） | 页面切换 |
| goCompDetail | 1865 | 点击竞品card入口，调showPage('comp-detail') |
| loadCompDetail | 1882 | 检索专利并渲染到 cd-patents-detail |
| renderCompPatents | 866 | 旧版渲染函数（page-competitor用） |
| loadWeekly | ~1100 | 本周技术情报加载 |
| heroSearch / runSearch | 早段 | 搜索主逻辑 |

### script块

- 全文共3个 `<script>` 块（语法验证已通过）

## server.js 关键路由

| 路由 | 说明 |
|------|------|
| GET /api/search | 调智慧芽MCP搜索，参数: q/type/topk |
| GET /api/weekly | 三路并行：智慧芽+SerpAPI+NewsAPI |
| GET /api/competitor/:name | 按公司名搜专利+新闻 |
| GET /api/docs | 读取本地docs目录 |
| POST /api/analyze | DeepSeek智能分析 |
| GET /api/health | 健康检查，返回 {status:'ok'} |

## 已完成功能

- ✅ 情报总览首页（Hero + 统计 + 搜索）
- ✅ 专利/论文检索页（含加载更多）
- ✅ 本周技术情报详情页（三路数据源）
- ✅ 竞品雷达角标（本周新增）
- ✅ 竞品详情页跳转（点card → 独立页面 → 专利列表）
- ✅ 研究工作台（收藏/文档/DeepSeek分析）
- ✅ 专利详情弹窗

## 待完善功能

- ⬜ 竞品详情页：技术领域分布饼图 + 近期专利趋势柱图
- ⬜ 竞品详情页：相关新闻列表
- ⬜ 竞品详情页：技术预警模块
- ⬜ 东阿阿胶门户（另一个客户，独立项目）

## API Key配置状态

- 智慧芽 PATSNAP_API_KEY：✅已配置
- DeepSeek DEEPSEEK_API_KEY：✅已配置
- SerpAPI SERPAPI_KEY：✅已配置
- NewsAPI NEWSAPI_KEY：✅已配置（国内访问不稳定）
