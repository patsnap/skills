# PatSnap Data-Access Policy

This skill supports two mutually exclusive evidence-acquisition modes. Select
one mode for a run and preserve its provenance from request through report.

## Mode A — Bundled REST workflow

- Only the scripts under this skill's `scripts/` directory may call PatSnap
  REST endpoints for the bundled workflow.
- Read the API key from `references/zhihuiya_config.json` unless the user
  explicitly selects another configuration file within the same skill.
- The legacy filename is retained solely for source-topology fidelity; its
  contents use the global PatSnap service and English configuration keys.
- Use `https://connect.patsnap.com` and a valid API key in the
  `Authorization: Bearer <key>` request header.
- Never send the key in a query string, write it to logs, embed it in an output
  file, or include it in an exception message.
- P070, P002, P018, AI07, and any authorized AI66 calls must flow through
  `scripts/run_generic_fto_report.py` and `scripts/zhihuiya_api.py`.
- P018 must use `/basic-patent-data/claim-data`; do not use the obsolete
  `/basic-patent-data/claims` path.
- AI07 is supporting evidence only. If AI output conflicts with the retrieved
  claim text, product evidence, or structured limitation mapping, retain the
  conflict and rely on the primary evidence and qualified reviewer judgment.

## Mode B — MCP-assisted workflow

- Use an installed global PatSnap connector from the user's agent environment.
- Recommended connectors are Patsnap Patent Research, Advanced Patent Search,
  Patent Briefing, and, when needed, Global Core Patents.
- Record connector name, tool name, normalized request, filters, execution
  date, task ID where applicable, returned identifiers, and limitations.
- Normalize MCP results into the same patent-list, claim, family, status, and
  claim-chart schemas before report generation.
- The bundled Python scripts do not claim to have called an MCP server. If MCP
  results are supplied to a script, label them as imported evidence with their
  original provenance.
- Do not repeat the same paid or quota-consuming search through REST unless the
  user requests a cross-check or the MCP result is insufficient.

## Controls common to both modes

- Use only user-approved search expressions or visibly reviewed generated
  expressions.
- Keep query text, provider, fields, filters, dates, counts, and errors.
- Preserve partial results as partial. An empty or failed call is not evidence
  that no relevant patent exists.
- Distinguish publication, application, grant, and family identifiers.
- Treat `SIMPLE_LEGAL_STATUS` as a search filter, not proof of enforceability.
- Verify decision-material claim version, status, ownership, and family facts
  against suitable dated sources.
- Keep pending applications in a separate watchlist.
- Do not transmit the user's confidential risk document or product evidence to
  any external service unless the user has authorized that transmission.

## Pre-delivery checks

1. The selected data-access mode is stated.
2. The key placeholder has been replaced only in the user's local private
   configuration and no credential appears in deliverables.
3. `queries.json`, `patent_list.json`, `claim_chart.json`, and
   `fto_structured_data.json` identify their provenance and creation status.
4. P018 claim text is traceable to the patent identifier, language, version,
   and retrieval date.
5. AI output is retained as supporting material and does not silently override
   the structured comparison.
6. The report states that it is an FTO screening and requires qualified local
   counsel for a decision-material legal opinion.
