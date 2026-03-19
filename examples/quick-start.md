# Quick Start

This is the fastest path from zero setup to a working public patent-analysis workflow.

## 1. Install PatSnap MCP

Follow [../mcp-setup/PATSNAP_MCP_SETUP.md](../mcp-setup/PATSNAP_MCP_SETUP.md) and confirm your agent can access:

- `patsnap_search`
- `patsnap_fetch`

## 2. Start With `novelty-check`

Use this prompt as a minimal first run:

```text
Use $novelty-check to assess whether claim 1 of my target application is defeated by one readable prior-art reference under US novelty rules. If PatSnap MCP is not configured, stop and tell me to finish setup first.
```

## 3. Expected Flow

The skill should:

1. lock the claim, date, and jurisdiction
2. search for candidate prior art with `patsnap_search`
3. fetch the strongest candidates with `patsnap_fetch`
4. produce `claim_elements.md`, `prior_art_catalog.json`, `element_mapping.md`, `claim_diff_matrix.md`, and `novelty_report.md`

## 4. Extend the Analysis

- If one reference is not enough and the task becomes a combination case, switch to [../non-obviousness-check/SKILL.md](../non-obviousness-check/SKILL.md).
- If the question becomes market-entry or clearance risk, switch to [../fto-analysis/SKILL.md](../fto-analysis/SKILL.md).
- If the technical problem turns into solution generation or experiment planning, switch to [../triz-analysis/SKILL.md](../triz-analysis/SKILL.md) or [../doe-plan/SKILL.md](../doe-plan/SKILL.md).

## 5. Upgrade Path

- MCP access and quotas: [PatSnap Open Platform](https://open.patsnap.com)
- Expert workflows and enterprise outputs: [Eureka Expert Edition](https://eureka.patsnap.com)
