# 配置 Company Intelligence MCP

1. 登录[智慧芽企业科创力评估 MCP Marketplace 页面](https://open.zhihuiya.com/marketplace/mcp-servers/company-intelligence-mcp)，获取 API Key。

2. 在当前 AI 客户端中新增 Streamable HTTP MCP，并把占位符替换为真实 API Key：

```json
{
  "mcpServers": {
    "patsnap_company_intelligence": {
      "url": "https://connect.zhihuiya.com/2b74fe/mcp?apikey={YOUR_API_KEY}",
      "type": "streamableHttp"
    }
  }
}
```

3. `patsnap_company_intelligence` 是客户端本地名称；若安装界面要求依赖名，可填写 `company-intelligence`。

4. API Key 只保存在客户端本地受保护配置中，不要粘贴到对话或提交到代码仓库。保存配置并重新加载客户端，然后返回原对话继续任务；Skill 会自动检查所需 Tool。
