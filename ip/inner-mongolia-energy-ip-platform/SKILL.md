---
name: inner-mongolia-energy-ip-platform
description: 内蒙古自治区现代能源知识产权运营中心平台生成器——通过 PatSnap MCP 检索真实专利数据，生成包含7大功能模块的完整单页 HTML 平台。
---

# 内蒙古现代能源知识产权运营中心平台

## 功能简介

本 SKILL 可一键生成「内蒙古自治区现代能源知识产权运营中心」完整 Web 平台（单文件 HTML），包含：

| 模块 | 说明 |
|------|------|
| 🏠 工作台 | 统计概览、专利卡片、简报快览、成果快览 |
| 📋 现代能源专利数据 | PatSnap MCP 实时检索、关键词过滤、分页、专利详情抽屉 |
| 🤖 AI 工具箱 | 6大极简文字卡，内置对话界面，支持 PatSnap API Key |
| 📰 情报简报 | 卡片展示、查看详情弹窗、下载 HTML/PDF、发布表单 |
| 🏆 成果发布库 | 成果卡片、详情弹窗、下载、发布/上传表单 |
| 🎯 技术需求库 | 需求列表、详情弹窗、下载、发布表单 |
| 🖥️ 驾驶舱大屏 | 深色极简，6KPI + 折线/柱状/饼图/排行榜，自适应布局 |

## 使用方式

### 方式一：直接运行脚本生成

```
生成内蒙古现代能源知识产权运营中心平台
```

Eureka 会自动：
1. 调用 `mcp_patent-search__patsnap_search` 检索最新现代能源专利（20条）
2. 调用 `mcp_patent-search__patsnap_fetch` 获取专利详情
3. 将专利数据注入 HTML 模板
4. 输出完整可用的 `energy-ip-platform.html`

### 方式二：仅刷新专利数据

```
刷新平台专利数据
```

保留现有 HTML，仅更新专利数据部分。

### 方式三：自定义领域检索

```
生成平台，专利领域聚焦：风电、储能
```

## 部署方式

生成的 HTML 为纯静态单文件，三种部署方案：

### Vercel（推荐，5分钟上线）
```bash
npm i -g vercel
vercel --yes
```

### GitHub Pages
1. 新建仓库，上传 HTML 文件命名为 `index.html`
2. Settings → Pages → Branch: main / root

### Nginx 自有服务器
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/energy-ip;
    index index.html;
}
```

## PatSnap API Key 配置

平台内置演示模式（无需 Key），如需对接真实 AI：
1. 登录 [PatSnap Connect](https://connect.patsnap.com)
2. 获取 API Key
3. 在平台「AI工具箱」任意工具弹窗右上角输入 Key
4. Key 自动保存至 localStorage

> ⚠️ 生产环境建议通过后端代理转发，避免 Key 暴露在前端。

## 技术栈

- 纯原生 HTML5 + CSS3 + JavaScript（无框架依赖）
- Chart.js 4.x（驾驶舱图表）
- PatSnap MCP（专利数据）
- PatSnap Connect API（AI 对话）
- localStorage（登录状态 + API Key 持久化）

## 文件说明

```
inner-mongolia-energy-ip-platform.skill
├── SKILL.md                         # 本文件
├── skill.manifest.json              # 运行配置
├── scripts/
│   └── generate.py                  # 主生成脚本
└── references/
    └── platform_template.html       # 完整平台 HTML 模板
```

## 版本历史

| 版本 | 说明 |
|------|------|
| v1.0 | 初始版本，7大模块，PatSnap MCP 真实数据 |
| v1.1 | 专利详情抽屉，AI工具箱对话界面 |
| v1.2 | 成果/需求/简报详情弹窗 + 表单上传 |
| v1.3 | 下载功能（HTML导出+打印PDF） |
| v1.4 | 驾驶舱大屏图表比例优化，极简文字卡AI工具箱 |

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
