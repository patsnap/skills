# System Component Analysis

## Task

Based on the complete technical problem description provided by the user, use the TRIZ functional analysis method to systematically identify and classify all key components (internal system components and super-system components), clarify the primary function description of each component, and provide an accurate functional model for subsequent TRIZ analysis.

- If there is no modification request, treat it as an initial generation task and output results directly based on the problem summary
- If there is a modification request, understand the user's modification intent, adjust based on existing results, and output again

---

## Input Information

- **Problem summary**: The complete technical problem description provided by the user, clarified and confirmed
- **Modification request** (optional): User-input modification content, provided in modification scenarios
- **Existing data** (optional): Already-generated system component analysis content, provided in modification scenarios

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `SYSTEM_COMPONENT_ANALYSIS`
- **user_input**: Organize the input information as text, using tags to distinguish each part:
    ```
    [Problem Summary]
    {problem summary content}

    // Append the following in modification scenarios
    [Modification Request]
    {user's modification content}

    [Existing Data]
    {already-generated system component analysis content}
    ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "components": [
    {
      "component_name": "Component Name",
      "primary_function": "Primary function description (verb-object structure)"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `components` array into a "Components" Markdown table with field mappings:
   - `component_name` → `Component Name`
   - `primary_function` → `Primary Function Description`

---

## Output Format

### Summary Mode

Summarize the analysis results in a paragraph.

**Example**:

System component analysis complete. Identified 4 internal system components (fin heat exchanger, refrigerant, frost layer, thermal field) and 3 super-system components (ambient air, compressor, humidity field).

### Detailed Mode

Output the system component list in Markdown table format, including both internal system components and super-system components. Each component includes a number, name, type, and primary function description.

#### Example (using "heat exchanger frosting causing efficiency drop")

#### System Component Analysis Results

| Component Name | Primary Function Description |
|---------------|------------------------------|
| Fin Heat Exchanger | Extends surface area via fins to transfer refrigerant cooling to air |
| Refrigerant | Flows inside the heat exchanger to absorb external heat for cooling |
| Frost Layer | Condenses into an ice crystal layer on low-temperature fin surfaces, impeding heat exchange |
| Ambient Air | Acts as a heat source, supplying airflow to be cooled by the heat exchanger |
| Compressor | Provides circulation power for the refrigerant to maintain the refrigeration cycle |
| Thermal Field | Drives heat transfer between refrigerant and air |
| Humidity Field | Supplies water vapor, the material source for frost layer formation |
| Ambient Temperature | Affects heat exchange temperature difference and frosting rate |
