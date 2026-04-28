# Solution Generation

## Task

Retrieve the key problem descriptions selected by the user from the causal chain problem filtering, call the `BatchSolutionWorkflow` tool to batch-generate concept solutions, and recommend them to the user after filtering.

---

## Input Information

Retrieve the following data from the causal chain problem filtering:

- **Key problem list**: Key problems selected by the user from the causal chain analysis (maximum 3)
- **Problem description**: Technical detailed description of each key problem (content of the `problem_description` field)

---

## Concept Solution Generation

### Tool Invocation Instructions

Call the `BatchSolutionWorkflow` tool, passing in the key problems selected by the user.

#### Input Parameters

```json
{
    "workflow_type": "INNOVATION",
    "problems": [
        {
            "problem_id": "Causal chain problem ID (e.g., P1, P2)",
            "problem_description": "Technical detailed description of the specific problem selected by the user"
        }
    ]
}
```

- `workflow_type` (required): Workflow type, fixed value `"INNOVATION"`
- `problems` (required): List of problems selected by the user; each entry corresponds to one specific problem
  - `problem_id`: ID of the causal chain problem, taken from the `id` field of the corresponding problem in the causal chain problem filtering results
  - `problem_description`: Technical detailed description of the problem selected by the user, taken from the `technical_description` field of the corresponding problem in the causal chain problem filtering results

#### Return Result

The tool returns data in JSON format — a collection of concept solutions grouped by problem:

```json
{
  "solution_idea_groups": [
    {
      "key_problem": {
        "problem_id": "Causal chain problem ID",
        "problem_description": "Specific problem description",
        "select": true
      },
      "idea_list": [
        {
          "idea_id": "Unique solution identifier (UUID)",
          "problem": "Corresponding problem description",
          "idea_title": "Concept solution title",
          "advantage_tag_list": ["Advantage tag 1", "Advantage tag 2"],
          "idea_summary": "Solution summary (HTML format, with technical parameters)",
          "analysis_method": "Analysis method",
          "triz_principle": "Applied TRIZ principle",
          "is_cross_domain": false,
          "feasibility": "Feasibility rating (High/Medium/Low)",
          "triz_feature_mapping": [
            {
              "patent_id": "Reference patent ID",
              "title": "Reference patent title",
              "feature_type": "Feature type",
              "feature_content": "Feature content description",
              "application_method": "Application method description"
            }
          ]
        }
      ],
      "used_patent_ids": ["List of referenced patent IDs"]
    }
  ]
}
```

### Result Processing Rules

> **Note**: If a problem in the returned result has no corresponding solution data, it means no solution can currently be found for that problem — this is normal and the `BatchSolutionWorkflow` tool should not be called again.

The tool has already completed solution filtering. Use the solutions in `solution_idea_groups` directly for display without additional sorting or filtering.

### Output Format

Display all solutions from `solution_idea_groups` to the user:

#### Summary Mode

Display in a concise list, each entry containing only the title, feasibility, and a one-sentence summary:

```
### Recommended Concept Solutions

| # | Solution Title | Feasibility | Summary |
|---|---------------|------------|---------|
| 1 | [Solution Title] | [High/Medium/Low] | [idea_summary converted to plain text, first sentence only] |
| 2 | [Solution Title] | [High/Medium/Low] | [idea_summary converted to plain text, first sentence only] |
| ... | ... | ... | ... |
```

#### Detailed Mode

Display concept solutions in a numbered list, each entry containing full details:

```
### Recommended Concept Solutions

---

**Solution 1: [Solution Title]**

**Basic Information**
- Source problem: [Key problem description]
- Feasibility: [High/Medium/Low]
- Analysis method: [Name]
- TRIZ principle: [Principle name]
- Cross-domain: [Yes/No]

**Advantage Tags**
[Each tag displayed independently]

**Solution Summary**
[Converted to plain text, displayed item by item]

**Reference Patents and Application Methods**

| PN | Patent Title | Feature Type | Feature Content | Application Method |
|----|-------------|-------------|----------------|-------------------|
| ... | ... | ... | ... | ... |

---

**Solution 2: [Solution Title]**
...
```

#### Analysis Method Mapping

| Value | Display Name |
|-------|-------------|
| physical_contradiction | Physical Contradiction Analysis |
| technical_contradiction | Technical Contradiction Analysis |
| function_modeling | Functional Modeling Analysis |
| substance_field_model | Substance-Field Model Analysis |

#### Feature Type Mapping

| Value | Display Name |
|-------|-------------|
| physical_contradiction | Physical Contradiction |
| technical_contradiction | Technical Contradiction |
| function_fingerprint | Function Fingerprint |
| sufield_features | Substance-Field Features |

---

## User Interaction: Refresh Solutions

Triggered when the user expresses the following intent:
- "Refresh", "show different solutions", "any other options?", "let me see others"
- "I want to see more solutions", "any other ideas?", "recommend a few more"

**Processing Rules**:
1. Re-select from the results of the most recent tool call
2. Exclude solutions that have already been displayed
3. If the user expresses specific preferences (e.g., "want cross-domain ones", "any simpler ones"), filter from remaining solutions based on user requirements before displaying
4. If remaining solutions are insufficient, display all remaining solutions and inform the user "All solutions have been displayed"

---

## Guide User to Select

After displaying concept solutions, guide the user to select one for detailed design generation:

> Above are the recommended concept solutions. Please select one to generate a detailed design (enter the corresponding number), or enter "refresh" to see more solutions.

After user selection → read [08_solution_detail.md](08_solution_detail.md) to generate the detailed design.
