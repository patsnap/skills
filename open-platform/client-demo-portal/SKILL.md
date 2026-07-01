---
name: client-demo-portal
description: 为企业客户快速搭建智慧芽情报门户演示原型，涵盖需求分析、本地搭建、数据对接、演示话术全流程
---

## 这个Skill是什么

帮客户搭本地情报门户的完整打法，核心经验来自2026年5月为元六鸿远电子搭建门户的实战。

触发词：「帮我给客户搭情报门户」「帮我准备演示」「client demo portal」

---

## 项目结构

```
[客户名]-portal/
├── server.js        ← Express后端（调智慧芽MCP）
├── .env             ← API Key配置
├── package.json
├── public/
│   └── index.html   ← Apple风格前端
└── docs/            ← 客户本地文档
```

---

## 已验证客户

| 客户 | 行业 | 竞争对手 | 主题色 |
|------|------|---------|------|
| 北京元六鸿远电子科技 | 军工电子元器件（MLCC） | 风华高科、TDK、村田、三环 | #C8102E |

当前稳定版备份：`index.html.bak_before_kb_searchfix2`

---

## 智慧芽MCP关键参数（已实测）

```
端点：https://connect.zhihuiya.com/f8fb98/mcp?apikey=API_KEY
协议：JSON-RPC 2.0，SSE返回
Accept Header：'application/json, text/event-stream'  ← 两种都要，缺一报错
数据路径：result.content[0].text → JSON解析 → data.results
总数字段：data.matched_total
```

---

## 前端JS铁律（血泪教训）

**1. 整个文件只能有一个`<script>`块**
HTML在上，JS在下，`</script>`只出现一次，不能在`</html>`后面追加script。

**2. patch脚本改代码必须：**
- 改前grep确认行号，assert保证唯一匹配
- 函数必须在主script块内，不能在DOMContentLoaded回调里（onclick调不到）
- 改完立刻验证语法：
```bash
node -e "const fs=require('fs');const c=fs.readFileSync('index.html','utf8');const b=[];let p=0;while(true){const s=c.indexOf('<script>',p);if(s===-1)break;const e=c.indexOf('</script>',s);if(e===-1)break;b.push(c.slice(s+8,e));p=e+9;}fs.writeFileSync('/tmp/vf.js',b.join('\n'));" && node --check /tmp/vf.js && echo '✅ OK' || echo '❌ 语法错误'
```

**3. 每次改动前先备份**，命名规范：`index.html.bak_before_[功能名]`

**4. goSearch/doSearch/runSearch三层分工**
- goSearch：只跳页+填值，调runSearch
- doSearch：只读输入框值，调runSearch
- runSearch：只发请求+渲染
- 禁止互相调用，会无限递归

**5. checkHealth判断和server.js返回必须一致**
```js
// server.js：res.json({ status: 'ok' })
// 前端：if(d && d.status === 'ok')  ✅
```

---

## 替代方案：DeepSeek替代方案探索MCP

patsnap-technical-qa是Eureka内部MCP，Node.js无法HTTP直连。
```js
// 用DeepSeek替代（同步返回，不卡界面）
const response = await fetch('https://api.deepseek.com/chat/completions', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${process.env.DEEPSEEK_API_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({ model: 'deepseek-chat', messages: [
    { role: 'system', content: '你是专利技术分析专家' },
    { role: 'user', content: `基于专利背景：${context}\n\n请分析：${question}` }
  ]})
});
return (await response.json()).choices[0].message.content;
```

---

## 演示话术（5分钟，5步）

1. **情报总览**（60s）→ 点竞品卡片展示弹窗
   > "这是研发团队的情报仪表盘，竞品动态实时更新，点进去看详情。"

2. **专利检索**（60s）→ 输入「MLCC介质材料」
   > "直接输关键词，自动调智慧芽专利库，30秒出真实数据。"

3. **本周情报**（45s）→ 点情报卡片
   > "每周自动归集外部动态，研发10分钟看完，不用自己找。"

4. **研发知识库**（60s）→ 上传文件演示动画
   > "内部文档上传入库，统一沉淀，支持搜索，解决知识散落问题。"

5. **研究工作台**（45s）→ 点「打开Eureka技术问答」
   > "工作台是融合分析的核心，左侧收藏夹汇聚外部专利，右侧连接Eureka AI问答。"

**收尾**：> "这是一期POC，6个月后我们知道哪些问题外部库答不了，那就是二期内网知识库的需求清单。"

---

## IT问答准备

| IT问题 | 回答 |
|------|------|
| 数据存哪里？ | 本地，`hongyuan-portal/docs/`目录 |
| 用了哪些外部API？ | 智慧芽开放平台、DeepSeek，已授权 |
| 安全性？ | POC本地部署，API Key在.env，不上传代码仓库 |
| 后续部署？ | POC验证后，二期走IT标准流程 |

---

## 待办事项

- [ ] Widget嵌入：需向智慧芽获取`companyId`和`publicKey`（AgentIframe模式）
- [ ] 本周情报内外融合：内部卡片动态读取知识库文件列表
- [ ] 知识库搜索：搜索框过滤功能待验证稳定性

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。
