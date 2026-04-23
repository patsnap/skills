---
name: understand-technology
description: >- 
  Use for explaining materials science and engineering concepts, including material properties, structure–property relationships, processing methods, and performance mechanisms. Generate structured explanations of materials and engineering technologies by covering underlying scientific principles, structure–property relationships, processing methods, and performance characteristics, with clear connections between material composition, microstructure, and functional behavior in practical applications. Use for queries such as "What is X?", "How does X work?", or "Explain the science behind X".
---

# Understand Technology

Generate a response that helps users **clearly understand, analyze, and evaluate a technology** from both scientific and engineering perspectives.

---

## Expected Input

- A user query about a technology (e.g., concept, mechanism, comparison, or evaluation)
- Optional: additional context such as technical documents, extracted data, or prior analysis

---

## Context Usage

- Use any available context (e.g., retrieved documents, prior messages, or tool outputs) to support the explanation
- When external technical sources are available:
  - Extract concrete details such as materials, parameters, performance metrics, and implementation insights
- When no external context is provided:
  - Rely on general technical knowledge and clearly reasoned explanations

---

## Core Behavior

**Do:**
- Start directly with the answer (no meta commentary)
- Provide a concise high-level explanation first (2–3 sentences)
- Expand into structured, in-depth analysis
- Focus on clarity, accuracy, and technical usefulness
- Include concrete examples, parameters, and real-world context where relevant

**Do NOT:**
- Repeat or restate the user’s question
- Explain your reasoning process or structure
- Use filler phrases (e.g., “Let’s explore…”, “In this response…”)

---

## Response Structure

### 1. Overview
- What the technology is
- Its core purpose and importance
- Key applications and where it is used

---

### 2. Scientific Foundation

| Principles / Theories | Laws / Models | Key Variables | Assumptions / Limits |
|----------------------|--------------|--------------|---------------------|
| Core scientific concepts and mechanisms | Governing equations or models (if applicable) | Important measurable parameters and typical ranges | Ideal conditions and known constraints |

**Guidelines:**
- Focus on explaining *why and how* the technology works
- Include formulas only when they add value
- Keep explanations intuitive but technically accurate

---

### 3. Engineering Implementation

| Materials & Components | Hardware / Systems | Software / Modeling | Process & Integration | Performance & Optimization |
|------------------------|-------------------|---------------------|------------------------|-----------------------------|
| Key materials, compositions, or structures | Equipment, devices, or infrastructure used | Simulation tools, algorithms, or control systems | Manufacturing steps, workflows, or system integration | Key metrics, trade-offs, and optimization strategies |

**Guidelines:**
- Emphasize real-world implementation, not just theory
- Include typical ranges, constraints, or design considerations where useful
- Highlight how performance is measured and improved

---

### 4. Ecosystem (Organizations & Contributors)

| Entity | Type | Role |
|-------|------|------|
| Companies, universities, or institutes | Industry / Academic / Research | Contribution to development, research, or commercialization |

**Guidelines:**
- Include notable players when relevant
- Focus on contributions rather than exhaustive lists

---

### 5. Advantages & Limitations

- Key strengths and benefits
- Practical applications and value
- Limitations, risks, or technical challenges
- Trade-offs compared to alternative approaches (if relevant)

---

### 6. Summary & Assessment

Provide a concise synthesis:
- Key takeaways
- Technology maturity (emerging, developing, mature)
- Where it is most effective
- Important considerations for adoption or further research

---

## Writing Style

- Professional, technical, and clear
- Concise but informative
- Structured and easy to scan
- Avoid unnecessary jargon, but preserve technical depth
- Use tables where they improve clarity