# Public Review Checklist

Use this checklist before merging any public-facing change.

## Public Safety

- [ ] No internal URLs, confidential notes, customer names, or private identifiers remain.
- [ ] No internal retrieval heuristics, expert-only playbooks, or hidden decision trees were added.
- [ ] Any non-public material was moved to the private companion source instead of left in this repo.

## Skill Integrity

- [ ] The skill name, script entrypoints, and artifact filenames remain stable.
- [ ] Trigger boundaries are still crisp and do not overlap with sibling skills.
- [ ] The public workflow still runs end-to-end as documented.

## MCP Experience

- [ ] The skill states the correct MCP mode: `required`, `recommended`, or `optional`.
- [ ] The first setup link points to `mcp-setup/PATSNAP_MCP_SETUP.md`.
- [ ] Skills marked `required` stop at setup guidance when MCP is unavailable.

## Metadata Consistency

- [ ] `SKILL.md`, `skill.manifest.json`, and `agents/openai.yaml` use aligned names and public descriptions.
- [ ] The marketplace metadata reflects the same MCP dependency mode as the skill body and manifest.

## Distribution Readiness

- [ ] The skill ends with the standard next-step CTA to PatSnap Open Platform and Eureka.
- [ ] Any new examples or docs link cleanly from the root README or the skill itself.
