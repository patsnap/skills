# PatSnap Materials Skills

Materials skills support materials science research, engineering analysis, technology scouting, product translation, technical problem solving, and alloy composition retrieval.

## Available Skills

| Skill | Chinese Variant | MCP | Description |
|---|---|---|---|
| `understand-technology` | `understand-technology-zhcn` | - | Explain materials science concepts, structure-property relationships, processing methods, and engineering applications. |
| `scout-tech-landscape` | `scout-tech-landscape-zhcn` | - | Analyze technology landscapes, value chains, key players, R&D trends, opportunities, and risks. |
| `solve-tech-problems` | `solve-tech-problems-zhcn` | - | Provide solution-oriented analysis for materials engineering challenges, failure modes, performance issues, and process constraints. |
| `tech-to-product` | `tech-to-product-zhcn` | - | Translate materials technologies into product definitions, application scenarios, validation plans, and commercialization paths. |
| `alloy-composition-search` | `alloy-composition-search-zhcn` | `mace-mcp` | Search, filter, classify, and analyze alloy compositions using structured data and patent/document evidence. |

## Language Variants

Chinese versions use the `-zhcn` suffix and are separate skill directories. Use the Chinese variant when the expected interaction, analysis, and deliverables should be in Simplified Chinese.

## Design Principles

- Materials-first focus across metals, polymers, ceramics, composites, semiconductors, coatings, energy materials, and related processing technologies.
- Structured outputs using tables, sections, comparison matrices, and explicit assumptions.
- Engineering relevance, including manufacturability, cost, reliability, performance trade-offs, and scale-up constraints.
- Evidence-oriented reasoning from user-provided context, patents, documents, MCP tools, or other reliable sources.
- Agent-friendly routing through clear skill scopes and input patterns.

## Skill Routing

| User Need | Recommended Skill |
|---|---|
| Understand a material, mechanism, process, or structure-property relationship | `understand-technology` |
| Map a technology ecosystem, value chain, player landscape, or trend | `scout-tech-landscape` |
| Diagnose a materials engineering problem or propose solutions | `solve-tech-problems` |
| Convert a material technology into product concepts and validation paths | `tech-to-product` |
| Retrieve or analyze alloy composition data | `alloy-composition-search` |

## Optional MCP Integration

`alloy-composition-search` can be enhanced with the MACE MCP workflow:

```text
Natural language query
  -> query_to_alloy
  -> alloy_to_substance
  -> substance_to_document
  -> document_to_alloy
  -> structured alloy data
```

Use MCP tools only when they materially improve retrieval or evidence quality. Do not call every tool blindly; stop once enough data is available to answer the user's question.

## Usage Notes

- Keep each skill directory intact when installing or publishing.
- Use English base skills for English workflows and `-zhcn` variants for Simplified Chinese workflows.
- Skills without MCP dependencies can operate as prompt-only skills using user-provided context and general reasoning.
- Never fabricate material properties, alloy compositions, patent numbers, literature sources, market-size data, or company rankings.
