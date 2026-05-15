# Solution Detail Generation

## Task

Based on the concept solution selected by the user, generate complete solution details in one pass, including the solution name, working principle, technical grafting, solution transformation logic, implementation methods, and a mermaid-format implementation flowchart.

---

## Input Information

Retrieve the following data from preceding steps:

- **User problem**: Confirmed core problem / improvement goal
- **Key problem**: Description of the key problem in the causal chain for the user's selected solution
- **Concept solution**: Complete concept solution data selected by the user, including idea_id, solution title, solution summary, advantage tags, applied TRIZ principle, feasibility rating, analysis method, whether cross-domain, and associated patent feature mapping information
- **Component analysis**: System component list and function descriptions
- **Functional model**: Functional modeling results
- **Patent information**: Reference patent data associated with the concept solution, including patent title, feature type, feature content, and application method

---

## Execution Method

Call the `TrizAnalysis` tool to complete this task with the following parameters:

- **analysis_name**: `SOLUTION_DETAIL`
- **user_input**: Organize the above input information as text, using tags to distinguish each part:
  ```
  [User Problem]
  {core problem / improvement goal}

  [Key Problem]
  {causal chain key problem description}

  [Concept Solution]
  {complete concept solution data selected by the user}

  [Component Analysis]
  {system component list and function descriptions}

  [Functional Model]
  {functional modeling results}

  [Patent Information]
  {associated reference patent data}
  ```

---

## Tool Result Parsing

The tool returns data directly in JSON format with the following structure:

```json
{
  "idea_id": "idea_id of the concept solution",
  "idea_title": "Consistent with the solution title of the input concept solution",
  "principle_of_work": "Working principle description, containing patent reference markers [1], [2]",
  "technical_grafting": [
    {
      "patent_id": "PN number",
      "description": "Extract [core mechanism of original patent] + Execute [specific adaptation action] → Solve [current specific problem]"
    }
  ],
  "implementation": "Complete Markdown content of the specific implementation method",
  "implementation_flowchart": "Flowchart code in mermaid format"
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert each field to Markdown format output:
   - `idea_id` → idea identifier for the solution details
   - `idea_title` → solution details title (`## Solution Details: {idea_title}`)
   - `principle_of_work` → `### Working Principle` section content
   - `technical_grafting` → `### Technical Grafting Description` section, each entry formatted as: `- **Patent {patent_id}**: {description}`
   - `implementation` → `### Specific Implementation Method` section content (output Markdown directly)
   - `implementation_flowchart` → `### Implementation Flowchart` section, wrapped in a mermaid code block

## Output Format

### Summary Mode

Display only the solution title and working principle summary; omit technical grafting, specific implementation method, and flowchart.

```
## Solution Details: [idea_title]

### Working Principle
[principle_of_work]
```

### Detailed Mode

Display the parsed data completely in Markdown format:

```
## Solution Details: [idea_title]

### Working Principle
[principle_of_work]

### Technical Grafting Description
- **Patent [PN number]**: [description]

### Specific Implementation Method
[implementation]

### Implementation Flowchart
[mermaid flowchart]
```
