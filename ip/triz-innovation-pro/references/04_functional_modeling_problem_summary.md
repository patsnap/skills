# Problem Description and Core Problem Selection

## Task

Convert the key problems already identified in functional modeling into a user-friendly problem description list. Each problem will serve as an entry point for the user to proceed with causal chain analysis. Based on the problem identifiers already assigned in the system structure analysis, convert functional relationship data into clear, specific, and actionable problem descriptions, maintaining full consistency with the structure analysis.

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **Functional model**: Functional modeling analysis results
- **System structure analysis**: Structural elements containing annotated problem identifiers

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `FUNCTIONAL_MODELING_PROBLEM_SUMMARY`
- **user_input**: Organize the above input information as text, using tags to distinguish each part:
  ```
  [Problem Summary]
  {problem summary content}

  [Functional Model]
  {functional modeling analysis results}

  [System Structure Analysis]
  {structural elements containing problem identifiers}
  ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "problems": [
    {
      "id": 1,
      "problem_type": "Problem type",
      "problem_description": "Problem description"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `problems` array into a Markdown table with field mappings:
   - `id` → `#`
   - `problem_type` → `Problem Type`
   - `problem_description` → `Problem Description`

---

## Output Format

### Summary Mode

Summarize the core problems in a paragraph.

**Example**:

Problem analysis complete. Identified 2 core problems: 1) The connection structure expands the gap at the panel joint, becoming the root source of condensate leakage; 2) The sealing structure has insufficient ability to block condensate, directly leading to the formation of a leakage path.

### Detailed Mode

Output the parsed data in Markdown table format, containing three fields: number, problem type, and problem description. The number of problems is 3–5.

**Output Example**:

| # | Problem Type | Problem Description |
|---|-------------|---------------------|
| 1 | Harmful Elimination | **[Root Problem]** The **connection structure** expands the **gap** at the panel joint, becoming the root source of condensate leakage |
| 2 | Function Enhancement | **[Key Link]** The **sealing structure** has insufficient ability to block **condensate**, directly leading to the formation of a leakage path |
