# Causal Chain Analysis

## Task

Starting from the selected core problem, trace back to root causes, build a clear problem tree, and identify the most actionable technical intervention points.

Core method: Why-Why analysis (continuously asking "why"), tracing from surface-level problems to root causes, closing at the engineering-operable layer or uncontrollable boundary.

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **Core problem description**: Description of the selected core problem
- **Functional model**: Functional modeling result data
- **Modification request** (optional): User-input modification content, provided in modification scenarios
- **Existing data** (optional): Already-generated causal chain content, provided in modification scenarios

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `CAUSAL_CHAIN_ANALYSIS`
- **user_input**: Organize the input information as text, using tags to distinguish each part:
    ```
    [Problem Summary]
    {problem summary content}

    [Core Problem Description]
    {core problem description automatically selected in Step 4}

    [Functional Model]
    {functional modeling result data}

    // Append the following in modification scenarios
    [Modification Request]
    {user's modification content}

    [Existing Data]
    {already-generated causal chain content}
    ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "causal_chain": [
    {
      "node_id": "N001",
      "parent_id": "ROOT",
      "problem_text": "Problem description",
      "key_problem_id": "",
      "logic_relation": "SINGLE"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `causal_chain` array into a Markdown table with field mappings:
   - `node_id` → `Node ID`
   - `parent_id` → `Parent Node`
   - `problem_text` → `Problem Description`
   - `logic_relation` → `Logic Relation`
   - `key_problem_id` → `Key Problem` (empty string outputs as empty cell)

---

## Output Format

### Summary Mode

Summarize the causal chain analysis results in a paragraph, focusing on key problem nodes.

**Example**:

Causal chain analysis complete. Traced 6 nodes, identified 2 key problem nodes: N003 (condensate accumulates at the seam and cannot drain in time) and N005 (drainage system flow capacity insufficient to handle peak condensate).

### Detailed Mode

Output the parsed data in Markdown table format, containing five fields: node ID, parent node, problem description, logic relation, and key problem.

**Output Example**:

| Node ID | Parent Node | Problem Description | Logic Relation | Key Problem |
|---------|------------|---------------------|---------------|------------|
| N001 | ROOT | Heat dissipation structure costs remain high, blocking low-cost solution implementation | SINGLE | |
| N002 | N001 | Forced to use liquid cooling or large aluminum substrates, causing cost surge | SINGLE | |
| N003 | N002 | Heat flux density transferred from LED display unit to heat dissipation structure exceeds passive cooling threshold | SINGLE | |
| N004 | N003 | Excessive heat generation per unit area of LED chip causes localized heat flux concentration | AND | 1 |
| N005 | N003 | Limited capacity of heat dissipation structure to receive heat from LED display unit causes heat accumulation | AND | |
| N006 | N004 | Drive current density set in high-power range to achieve ultra-high brightness target | AND | |
| N007 | N004 | LED chip layout density on curved substrate too high, causing insufficient heat dissipation channels | AND | 2 |

---

## Output Notes

- **Key problem**: Nodes marked 1/2/3 are identified key intervention points, maximum 3
- **Termination condition**: Nodes ending with `[Termination Condition X: description]` are trace-back endpoints
- **Supplementary note**: Nodes starting with `[Supplementary Note]` are mechanism supplements and do not participate in key problem selection
- **Logic relation**: SINGLE (single cause), AND (multiple causes must coexist), OR (any one of multiple causes is sufficient)
