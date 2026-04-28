# Causal Chain Problem Filtering

## Task

Filter the most valuable core problems from the causal chain analysis results, generate a problem selection menu that balances technical depth and user-friendliness, and allow the user to select a problem to proceed to solution generation.

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **Functional model**: Functional modeling result data
- **Causal chain analysis results**: Causal chain analysis output

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `CAUSAL_CHAIN_PROBLEM_SUMMARY`
- **user_input**: Organize the above input information as text, using tags to distinguish each part:
  ```
  [Problem Summary]
  {problem summary content}

  [Functional Model]
  {functional modeling result data}

  [Causal Chain Analysis Results]
  {causal chain analysis output}
  ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "selected_problems": [
    {
      "id": 1,
      "user_friendly_description": "User-friendly description",
      "technical_description": "Technical detailed description"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `selected_problems` array into a Markdown table with field mappings:
   - `id` → `#`
   - `user_friendly_description` → `User-Friendly Description`
   - `technical_description` → `Technical Detailed Description`

---

## Output Format

### Summary Mode

Summarize the filtered key problems in a paragraph.

**Example**:

Causal chain problem filtering complete. Identified 1 key problem: [Adjust Operating Parameters] The refrigeration system controller sets the temperature too low, causing frost formation on the fin surface.

### Detailed Mode

Output the parsed data in Markdown table format, containing three fields: number, user-friendly description, and technical detailed description. The number of problems matches the number of key problem identifiers in the input (maximum 3).

After outputting the table, output the marker `<!-- TRIZ_QUESTION_CONFIRM -->` on a new separate line. Do not output any selection prompt text.

**Output Example**:

| # | User-Friendly Description | Technical Detailed Description |
|---|--------------------------|-------------------------------|
| 1 | [Adjust Operating Parameters] **Refrigeration system controller** sets temperature too low → frost forms on fin surface | The **refrigeration system controller** sets the refrigerant evaporation temperature target too low (pursuing high cooling capacity), causing the root temperature of the **air conditioner fin heat exchanger** to remain continuously below the air dew point temperature (over-cooled), driving water vapor to continuously condense and solidify into frost on the fin surface |
