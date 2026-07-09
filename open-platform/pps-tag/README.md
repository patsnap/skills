## Setup Guide



> **PatSnap 智慧芽开放平台 MCP 服务** 让各类Agent平台直接访问超 2 亿条专利、药物研发及生物数据。

### 1. 获取 API Key

登录 [https://open.zhihuiya.com](https://open.zhihuiya.com/) ，注册账号并获取 **API Keys**，如何操作可参考说明 https://open.zhihuiya.com/devportal/guides/authentication。



### 2. 连接 MCP 服务

访问并登陆智慧芽开放平台的 MCP 服务市场：[https://open.zhihuiya.com/marketplace/mcp-servers](https://open.zhihuiya.com/marketplace/mcp-servers)

在市场中搜索并安装所需 MCP 服务，点击即可进入功能说明和安装页面。在详情说明页面，点击复制就能获取连接URL，粘贴到 Eureka Desktop/Codex/Claude Code 等常用客户端添加所需服务。



以下 MCP 为常用基础能力，可在 MCP 服务市场搜索安装：

| MCP 服务                                                     | 用途                                                         | 要求     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | -------- |
| [智慧芽专利&文献融合检索](https://open.zhihuiya.com/marketplace/mcp-servers/patsnap-search) | 专利/文献检索、语义搜索、关键词搜索、前置过滤、获取专利或文献基础信息 | 推荐安装 |
| [高级专利检索](https://open.zhihuiya.com/marketplace/mcp-servers/patent-search) | 提供更灵活、更深入的专利高级检索能力。支持语义、相似、图像、专利号、嵌套检索、统计和关键词辅助等方式。适合用于检索专家、分析师和高要求项目研究。 | 推荐安装 |
| [专利深度挖掘](https://open.zhihuiya.com/marketplace/mcp-servers/patent-mining) | 用于从专利文本和分类信息中进一步挖掘技术内容。支持技术主题、技术问题/技术手段/技术效果三要素、战略性新兴产业、材料物质、应用领域和分类号说明等分析。适合用于技术拆解、领域研究和研发启发。 | 推荐安装 |
| [专利速览简报](https://open.zhihuiya.com/marketplace/mcp-servers/patent-briefing) | 用于快速阅读和理解单件专利或专利家族的速览工具。可汇总著录项目、法律状态、家族信息、技术三要素、附图，以及说明书、摘要和权利要求翻译 | 推荐安装 |
| [专利图表分析](https://open.zhihuiya.com/marketplace/mcp-servers/patent-visual) | 将专利数据转化为更直观的图表分析结果。可从趋势、类型、价值、诉讼、被引、技术效果短语等维度进行可视化展示 | 可安装   |
| [专利全景任务分析](https://open.zhihuiya.com/marketplace/mcp-servers/landscape-projects) | 将专利全景分析做成可跟踪的任务流。支持创建分析任务、查看状态、读取分面结果和完整专利列表 | 可安装   |
| [创新与专利报告生成](https://open.zhihuiya.com/marketplace/mcp-servers/report-gen) | 将分析结果进一步沉淀为可交付的报告和任务。支持生成企业报告、专利价值报告、技术想法查新报告，并可下载结果或结合相似专利比对 | 可安装   |
| [科研文献与期刊](https://open.zhihuiya.com/marketplace/mcp-servers/literature-search) | 提供科研文献、期刊、作者、机构和引用信息的统一检索入口。帮助用户快速找到相关研究、识别核心作者与机构，并理解一项研究的引用影响力 | 可安装   |
| [查新检索轻量版](https://open.zhihuiya.com/marketplace/mcp-servers/novelty-search-lite) | 摘要提取、技术特征提取、关键词提取、专利/论文检索、查新报告生成、新颖性评价 | 可安装   |

💡 **使用其他Agent？** 访问上述任一MCP服务页面，在右下角切换 Cursor、API 等标签页获取对应配置。

### 3. 验证

在客户端中输入 `/mcp`，确认已添加的服务显示名称。

💡 **需要帮助？** 访问查阅 [PatSnap 开发者文档](https://open.patsnap.com/devportal)

------

## MCP 连通性自检

**首次安装技能、加载后，必须先执行以下自检。**

1. 调用一个轻量级 MCP 工具探测连通性，
2. 如果调用失败（工具不存在、连接超时、认证错误等）：
   - 向用户回复以下引导信息：

> ⚠️ **PatSnap MCP 服务未连接**
>
> 本技能依赖 PatSnap 智慧芽开放平台 MCP 服务。请先完成以下步骤：
>
> 1. 前往 [open.zhihuiya.com](https://open.zhihuiya.com/) 创建 API Key
> 2. 访问[https://open.zhihuiya.com/marketplace/mcp-servers](https://open.zhihuiya.com/marketplace/mcp-servers)获取必需的 MCP 服务
> 3. 输入 `/mcp` 确认服务状态
>
> 配置完成后重新提问即可。
