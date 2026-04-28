# Contact Relationship Analysis

## Task

Based on the system component list and function descriptions, analyze the contact relationship between every pair of components and output a standardized contact relationship matrix.

- If there is a modification request, understand the user's modification intent, adjust based on existing results, and output again

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **System component list**: Each component includes its name and primary function description
- **Modification request** (optional): User-input modification content, provided in modification scenarios
- **Existing data** (optional): Already-generated contact analysis content, provided in modification scenarios

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `COMPONENT_TOUCH_ANALYSIS`
- **user_input**: Organize the input information as text, using tags to distinguish each part:
    ```
    [Problem Summary]
    {problem summary content}

    [System Component List]
    {system component list content}

    // Append the following in modification scenarios
    [Modification Request]
    {user's modification content}

    [Existing Data]
    {already-generated contact analysis content}
    ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "touch_matrix": [
    {
      "component_a": "Component A name",
      "component_b": "Component B name",
      "contact_relation": "+/-/empty string"
    }
  ]
}
```

### Parsing Rules

1. **Data extraction**: Extract all component pair relationships from the `touch_matrix` array
2. **Relationship filtering**: Retain only component pairs that meet the following conditions:
   - `contact_relation` value is `"+"` (contact relationship exists)
   - `component_a` and `component_b` are different (exclude self-relationships)
3. **Field conversion**: Convert contact type symbols to specific descriptions:
   - Based on actual contact conditions, convert `"+"` to a specific contact type description (e.g., "mechanical connection", "energy transfer", "material exchange")
   - If the tool already returns a specific description, use it directly
4. **Order preservation**: Maintain the order of component pairs as returned by the tool

---

## Output Format

### Summary Mode

Summarize the analysis results in a paragraph.

**Example**:

Contact relationship analysis complete. Identified 5 contact relationships (indoor unit–upper panel and indoor unit–lower panel are mechanical connections; indoor unit–power module and indoor unit–wiring are energy transfers; upper panel–lower panel is surface bonding).

### Detailed Mode

Output the contact relationship list in Markdown table format.

### Output Example (6 components, 5 contact relationships)

| Component A | Component B | Contact Relationship |
|------------|------------|---------------------|
| Indoor Unit | Upper Panel | Mechanical Connection |
| Indoor Unit | Lower Panel | Mechanical Connection |
| Indoor Unit | Power Module | Energy Transfer |
| Indoor Unit | Wiring | Energy Transfer |
| Upper Panel | Lower Panel | Surface Bonding |

### Key Requirements

1. **Output contact relationships only**: Display only component pairs where contact exists (`contact_relation` is `"+"`)
2. **Exclude redundant information**:
   - Do not display non-contact relationships (`"-"`)
   - Do not display self-relationships (`component_a` = `component_b`)
3. **Maintain order**: Output strictly in the order returned by the tool
4. **Concise output**: Output only the table, without additional text
