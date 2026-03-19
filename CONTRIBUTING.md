# Contributing

Contributions should improve the public skill experience without breaking existing usage.

## Repository Rules

- Keep skill names, directory names, script entrypoints, and artifact filenames stable unless a breaking change is explicitly approved.
- Treat `SKILL.md` as the source of truth for workflow and trigger boundary.
- Keep public references concise and reusable. Move non-public detail to the private companion source instead of expanding the public repo.
- Update `skill.manifest.json` and `agents/openai.yaml` whenever the public-facing behavior or MCP mode changes.

## Public Review Gate

Before opening a PR, complete the checklist in [docs/public-review-checklist.md](docs/public-review-checklist.md).

Changes should only merge when all of the following remain true:

- the skill still routes to the correct trigger boundary
- the MCP install path is still one hop away
- the core workflow can still run as documented
- public content does not leak internal URLs, customer material, or private playbooks

## Private Companion Source

If a change introduces any of the following, do not keep it in this repo:

- advanced case libraries
- internal search heuristics
- expert-only templates
- enterprise report packs
- internal-only URLs or operations notes

Move that material to the companion source defined in [docs/companion-private-source.md](docs/companion-private-source.md), then leave only the public-safe summary here.

## Suggested Change Flow

1. Update the relevant `SKILL.md`.
2. Keep or refine only the minimum public-safe references needed for the workflow.
3. Update `skill.manifest.json` with any MCP or output metadata changes.
4. Update `agents/openai.yaml` so the marketplace description stays aligned.
5. Re-run any relevant tests or validation commands for the skill.

## Pull Request Notes

Every PR description should call out:

- which skill or shared docs changed
- whether MCP mode changed
- whether any content was moved to the private companion source
- what validation was run
