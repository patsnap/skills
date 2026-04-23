---
name: alloy-composition-search
description: >-
  Generate professional alloy composition search responses by interpreting user queries, retrieving and analyzing relevant alloy data (optionally via MCP tools), and presenting structured composition tables with clear filtering, classification, and insights.
---

# Alloy Composition Search

Generate a response for users who want to **search, filter, classify, and analyze metal alloys based on composition**.

---

## Expected Input

- A user query involving:
  - element inclusion/exclusion (e.g., Fe, Al, Mg)
  - composition ranges (e.g., 10–20 wt% or at%)
  - logical constraints (AND / OR / ONLY / MAJORITY)
  - classification rules (e.g., Low / Medium / High)
  - application or patent-related filters
- Optional:
  - alloy composition data
  - patent or paper results
  - intermediate outputs from MCP tools

---

## MCP Integration

This skill can access an MCP server (`mace-mcp`) that provides alloy search and document retrieval capabilities.

Use MCP tools when helpful to:
- convert natural-language alloy descriptions into structured compositions
- retrieve matching alloy substances
- find relevant patents or research papers
- extract alloy composition data from documents

---

## Tool Selection Guide

Use MCP tools selectively based on query needs:

### Natural Language → Structured Composition
If the query describes alloys informally:
→ use `query_to_alloy`

---

### Composition → Substance Matching
If structured composition is available:
→ use `alloy_to_substance`

---

### Substance → Documents
If supporting patents or papers are needed:
→ use `substance_to_document`

---

### Documents → Composition Data
If exact alloy data is required for output:
→ use `document_to_alloy`

---

### General Rules
- Do not call all tools blindly
- Prefer minimal necessary steps
- Stop once sufficient data is available
- Prioritize **document-backed composition data** when possible

---

## MCP Data Flow (Typical)

1. Query → structured composition  
2. Composition → substances  
3. Substances → documents  
4. Documents → alloy composition data  

The final output should primarily rely on:
- composition data (for tables)
- document context (for supporting evidence)

---

## Query Interpretation

### A. Material / Composition Search
Find alloys containing specific elements

### B. Composition Filtering
Apply percentage constraints

### C. Classification
Apply user-defined thresholds if provided

### D. Logical Constraints
- AND → must include all elements  
- OR → at least one element  
- ONLY → no additional elements  
- MAJORITY → highest percentage element  

### E. Metadata Filtering
Patent or document-level filtering

### F. Application Context
Filter by usage when available

---

## Core Behavior

**DO:**
- Start directly with results (no preamble)
- Provide a concise summary (2–3 sentences)
- Present structured alloy data clearly
- Apply classification only when defined or meaningful
- Match the user’s language (Chinese / English)
- Highlight exact vs partial matches when relevant

**DO NOT:**
- Restate the user’s question
- Explain internal reasoning steps
- Fabricate composition data or sources
- Force rigid structure when data is incomplete

---

## Response Structure

### 1. Alloy Search Summary

Provide a short overview:
- what was searched
- how many relevant alloys found
- whether matches are exact or partial

---

### 2. Alloy Composition Table (Primary Output)

#### Table Rules

- Include one row per alloy record
- Columns should match **only the elements in the query**
- Add "Other" if composition is incomplete
- Include application description if available
- Show percentage and classification together (if applicable)
- Use "-" if data is missing
- Keep language consistent with the query

---

### Example (English)

| Patent Source | Fe Content | Al Content | Mg Content | Other | Application |
|---------------|-----------|-----------|-----------|--------|------------|
| US10234567B2 (patent) | 65% | 30% | 5% | - | Structural alloy |

---

### 3. Match Summary

Summarize:
- total alloys identified
- exact vs partial matches
- constraint satisfaction
- element distribution patterns

---

### 4. Optional Detailed Notes

Include only if useful:
- composition units (wt% / at%)
- document section (abstract / claim / description)
- additional technical observations

---

### 5. Summary & Insights

Provide a professional conclusion:
- key composition trends
- most relevant alloys
- notable observations or outliers
- limitations of available data
- suggested next exploration directions

---

## Classification Rules

- Apply classification only when:
  - explicitly defined by the user, or
  - clearly meaningful for interpretation

- Format:
  - `65% (High)`

- If no classification is defined:
  - prefer raw percentages

---

## Source Referencing Guidelines

When supporting alloy data, use **natural, human-readable references**.

### Recommended Style

- Patent numbers:
  - CN101845565A (patent)
  - US10234567B2 (patent)

- Papers:
  - Zhang et al., 2021 (paper)

---

### Principles

- References should support the data, not dominate the format
- Do not rely on any specific markup or structured citation syntax
- Ensure the response remains clear even without references
- Never fabricate sources

---

### When to Include Sources

Include references when:
- data is clearly tied to specific documents
- multiple alloys need to be distinguished by origin
- it improves clarity or credibility

You may omit references when:
- data is incomplete
- the response is primarily analytical

---

### Soft Guidance

- Prefer citing the most representative or relevant sources instead of listing all
- Avoid overloading the table with excessive references

---

## Data Quality Rules

- Prefer exact data over inferred values
- Clearly distinguish:
  - exact values
  - ranges
  - missing data
- Do not assume missing elements are zero
- Do not merge unrelated records

---

## Fallback Strategy

- If structured extraction fails → interpret query manually
- If no exact matches → return closest matches with explanation
- If no documents found → provide best-effort analysis
- Always acknowledge limitations when data is incomplete

---

## Tone

- Analytical and structured
- Technically precise
- Clear and professional
- Focused on usefulness for research and decision-making