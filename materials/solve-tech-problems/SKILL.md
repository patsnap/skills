---
name: solve-tech-problems
description: >-
  Use for solving materials engineering problems only. Generate solution-oriented responses for materials engineering problems by analyzing material composition, microstructure, processing conditions, and performance behavior. Provide practical solutions such as alloy design, heat treatment adjustments, defect mitigation, and material substitution, with clear evaluation of trade-offs in properties, manufacturability, cost, and operating conditions.
---

# Solve Technical Problems

Generate a response that helps users **identify, evaluate, and implement solutions to technical problems**, considering constraints, trade-offs, and practical feasibility.

---

## Expected Input

- A user query describing a technical problem, optimization goal, or failure scenario
- Optional: additional context such as technical documents, system constraints, experimental data, or prior analysis

---

## Context Usage

- Use any available context (e.g., retrieved documents, prior messages, or tool outputs) to support the solution
- When external sources are available:
  - Extract concrete solution approaches, parameters, and validation evidence
- When no external context is provided:
  - Propose realistic, experience-based solutions grounded in engineering principles

---

## Core Behavior

**Do:**
- Start directly with the answer (no meta commentary)
- Provide a concise high-level solution or approach first (2–3 sentences)
- Break down the problem into actionable components
- Present multiple solution options when relevant
- Highlight trade-offs, risks, and feasibility

**Do NOT:**
- Repeat or restate the user’s question
- Explain your reasoning process
- Use filler phrases (e.g., “Let’s analyze…”, “In this response…”)

---

## Response Structure

### 1. Problem Definition & Requirements

- Clear definition of the technical problem
- Key constraints (cost, materials, environment, performance, etc.)
- Success criteria (what “solved” looks like)
- Target performance metrics or thresholds (if applicable)

---

### 2. Solution Space & Approaches

| Objective / Target | Approach | Process / Method | Materials / Components | Equipment / Tools | Constraints | Notes |
|-------------------|----------|------------------|------------------------|-------------------|-------------|-------|
| What needs to be achieved | Solution option (S1, S2, etc.) | Key steps or workflow | Required materials or systems | Required tools or infrastructure | Practical limitations | Key insight or rationale |

**Guidelines:**
- Present multiple distinct solution approaches (S1, S2, S3…)
- Keep each solution practical and implementable
- Use “NA” where a field is not applicable
- Focus on how each solution works in practice

---

### 3. Solution Comparison

| Criteria | S1 | S2 | S3 | ... |
|----------|----|----|----|-----|
| Performance | ✔ / ✘ / – | | | |
| Cost | | | | |
| Complexity | | | | |
| Scalability | | | | |
| Reliability | | | | |

**Legend:**
- ✔ = Meets criterion  
- ✘ = Does not meet criterion  
- – = Not evaluated or uncertain  

**Guidelines:**
- Compare solutions across realistic decision criteria
- Keep evaluation consistent and practical
- Highlight meaningful differences

---

### 4. Scientific & Technical Basis

| Principles / Mechanisms | Models / Relationships | Key Parameters | Limitations |
|------------------------|------------------------|----------------|-------------|
| Core scientific reasoning behind solutions | Relevant equations or system relationships (if useful) | Important variables and ranges | Assumptions or constraints |

**Guidelines:**
- Explain *why* the solutions work
- Keep it concise and relevant to the problem

---

### 5. Implementation Strategy

- Typical steps to implement selected solutions:
  1. Feasibility assessment  
  2. Design and parameter selection  
  3. Prototyping or simulation  
  4. Testing and validation  
  5. Deployment and optimization  

- Key design decisions and trade-offs
- Integration with existing systems (if relevant)

---

### 6. Risks, Constraints & Mitigation

- Technical risks and failure modes
- Cost and resource considerations
- Operational or environmental constraints
- Mitigation strategies and best practices

---

### 7. Recommendations

Provide a concise synthesis:
- Most suitable solution(s) based on the scenario
- Why they are preferred (trade-offs and constraints)
- Practical next steps for implementation
- Alternative fallback options if conditions change

---

## Writing Style

- Solution-oriented and actionable
- Technically precise but practical
- Structured and easy to follow
- Focused on real-world feasibility
- Use tables where they improve clarity