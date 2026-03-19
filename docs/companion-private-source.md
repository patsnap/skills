# Companion Private Source

This public repository assumes a separate private companion source for expert-only assets.

The private companion should mirror the public skill names so teams can move material without changing the public workflow contract.

## Keep Public Here

- core skill workflow
- public-safe quick guides and summary references
- output contracts
- deterministic scripts that are safe to expose
- examples that contain no customer or internal data

## Move to the Private Companion

- complete jurisdiction playbooks or long-form legal guidance
- internal search and retrieval heuristics
- advanced exception handling branches
- internal case libraries and customer-derived examples
- expert report templates, enterprise packaging, or internal QA material

## Recommended Structure

Mirror the public repo by skill name, for example:

```text
private-patsnap-skills/
├── novelty-check/
├── non-obviousness-check/
├── fto-analysis/
├── triz-analysis/
├── doe-plan/
└── qfd-analysis/
```

## Migration Rule

When a public change introduces non-public detail:

1. move the detailed material to the private companion
2. keep a summary or placeholder in the public repo if the workflow still needs a reference
3. never leave public files pointing at internal-only URLs or systems

## Public Repo Contract

This repo should always remain independently usable for its public workflows, even after expert content moves out.
