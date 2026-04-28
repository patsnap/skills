# Functional Modeling

## Task

Based on system component information and contact analysis results, build a complete functional relationship network, identify beneficial, harmful, and neutral functions, and provide an accurate functional model foundation for subsequent technical contradiction analysis and innovative solution design.

- Every component in the system component list must appear at least once in the model
- For core problem components, deeply decompose their conflict chains; for peripheral components, assign only the most basic maintenance functions (support, containment, etc.) — do not expand or create unnecessary connections
- If there is a modification request, understand the user's modification intent and adjust based on existing results

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **System component list**: System component inventory
- **Contact relationship matrix**: Contact relationships between components
- **Modification request** (optional): User-input modification content, provided in modification scenarios
- **Existing data** (optional): Already-generated functional modeling content, provided in modification scenarios

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `FUNCTIONAL_MODELING`
- **user_input**: Organize the input information as text, using tags to distinguish each part:
    ```
    [Problem Summary]
    {problem summary content}

    [System Component List]
    {system component list content}

    [Contact Relationship Matrix]
    {contact relationship analysis content}

    // Append the following in modification scenarios
    [Modification Request]
    {user's modification content}

    [Existing Data]
    {already-generated functional modeling content}
    ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "functionModels": [
    {
      "function_carrier": "Component name",
      "action_verb": "Action verb",
      "function_object": "Component name",
      "performance_level": "N/H/I/E"
    }
  ]
}
```

### Parsing Rules

1. **Data extraction**:
   - Locate the `functionModels` array in the returned JSON
   - Extract functional relationship records one by one

2. **Field mapping**:
   - `function_carrier` → `Function Carrier`
   - `action_verb` → `Action`
   - `function_object` → `Function Object`
   - `performance_level` → `Performance Level`

3. **Performance level handling**:
   - The tool returns single-letter format (`N`, `H`, `I`, `E`)
   - Use directly without conversion
   - If Chinese format is encountered (e.g., `N（正常）`), extract the letter part

4. **Completeness verification**:
   - Check whether each component in the system component list appears at least once
   - Count coverage of function carriers and function objects

---

## Output Format

### Summary Mode

Summarize the analysis results in a paragraph, focusing on abnormal functional relationships.

**Example**:

Functional modeling complete. Identified 8 functional relationships. Found 3 anomalies: condensate wetting of the connection structure is a harmful function (H); the sealing structure's blocking function for condensate is insufficient (I); the refrigeration system's cooling function for the upper panel is excessive (E).

### Detailed Mode

Output the parsed data in Markdown table format, containing four fields: function carrier, action, function object, and performance level (H/I/N/E).
- **H (Harmful)**: Causes performance degradation >20%, creates safety risks, causes user discomfort
- **I (Insufficient)**: Function completion <70%, does not meet design specifications
- **E (Excessive)**: Function output >130% of requirement, causes resource waste >20%
- **N (Normal)**: None of the above conditions are met

### Performance Level Definitions

| Level | Name | Criteria |
|:-----:|------|---------|
| **N** | Normal Function | Meets design requirements (within 70%–130%) |
| **H** | Harmful Function | Causes performance degradation >20%, safety risks, or user discomfort |
| **I** | Insufficient Function | Function completion <70%, does not meet design specifications |
| **E** | Excessive Function | Function output >130% of requirement, resource waste >20% |

### Output Example

| Function Carrier | Action | Function Object | Performance Level |
|----------------|--------|----------------|:-----------------:|
| Power Interface | Transmit | Driver Circuit Board | N |
| Driver Circuit Board | Control | LED Display Unit | N |
| LED Display Unit | Emit | Optical Brightness Enhancement Film | N |
| Optical Brightness Enhancement Film | Enhance | LED Display Unit | N |
| LED Display Unit | Heat | Heat Dissipation Structure | N |
| Heat Dissipation Structure | Transfer | LED Display Unit | I |
| Curved Substrate | Support | LED Display Unit | N |
| Curved Substrate | Constrain | LED Display Unit | N |
| Curved Substrate | Support | Driver Circuit Board | N |
| Curved Substrate | Fix | Heat Dissipation Structure | N |
| Sealing Component | Block | LED Display Unit | I |
| Sealing Component | Isolate | Curved Substrate | N |
| Sealing Component | Cover | Heat Dissipation Structure | N |
| Mounting Bracket | Fix | Curved Substrate | N |
| Mounting Bracket | Constrain | Heat Dissipation Structure | N |
| Mounting Bracket | Fix | Sealing Component | N |

### Output Requirements

1. ✓ **Accurate field names**: Strictly map `function_carrier`, `action_verb`, `function_object`, `performance_level`
2. ✓ **Performance level format**: Output only a single letter (N/H/I/E), center-aligned
3. ✓ **Consistent component names**: Must be completely consistent with the system component list; do not modify
4. ✓ **Complete coverage**: Ensure every system component appears at least once as a function carrier or function object
5. ✓ **Concise output**: Output only the table, without additional explanatory text
