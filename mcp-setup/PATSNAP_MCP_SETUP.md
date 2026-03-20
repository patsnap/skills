# PatSnap MCP Setup

PatSnap MCP gives AI agents a stable way to search patents and literature, then fetch readable full text for downstream analysis skills.

## What You Get

- `patsnap_search`: search patents, papers, and technical literature
- `patsnap_fetch`: fetch readable full text, claims, and key sections

These two tools are the default evidence path for `novelty-check`, `non-obviousness-check`, and `fto-analysis`, and the recommended evidence path for `triz-analysis` and `doe-plan`.

## 1. Get an API Key

Create or sign in to your account on the [PatSnap Open Platform](https://open.patsnap.com), then generate an API key for MCP access.

If plan or quota details vary by account, trust the numbers shown in the Open Platform dashboard.

## 2. Configure Your MCP Client

PatSnap MCP uses a streamable HTTP server:

- URL: `https://open.patsnap.com/v1/stream`
- Header: `Authorization: Bearer YOUR_API_KEY`

### Claude Desktop / Claude Code

Add a PatSnap server entry to your MCP config:

```json
{
  "mcpServers": {
    "patsnap": {
      "type": "streamable-http",
      "url": "https://open.patsnap.com/v1/stream",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### Other MCP Clients

Use the same streamable HTTP endpoint and bearer-token header in your client-specific MCP configuration.

## 3. Validate the Connection

Your agent setup is ready when it can see both of these tools:

- `patsnap_search`
- `patsnap_fetch`

If a skill in this repo says MCP is required and those tools are missing, stop and finish setup before running the workflow.

## 4. Start With a Public Skill

- First-time patentability check: [../novelty-check/SKILL.md](../novelty-check/SKILL.md)
- Multi-reference inventive-step review: [../non-obviousness-check/SKILL.md](../non-obviousness-check/SKILL.md)
- Product clearance and blocking patent review: [../fto-analysis/SKILL.md](../fto-analysis/SKILL.md)
- Innovation and R&D planning: [../triz-analysis/SKILL.md](../triz-analysis/SKILL.md), [../doe-plan/SKILL.md](../doe-plan/SKILL.md), [../qfd-analysis/SKILL.md](../qfd-analysis/SKILL.md)

## Need More

- Higher-volume or production MCP usage: [PatSnap Open Platform](https://open.patsnap.com)
- Expert workflows, richer orchestration, and enterprise reporting: [Eureka Expert Edition](https://eureka.patsnap.com)
