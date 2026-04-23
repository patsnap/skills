---
name: tech-to-product
description: >-
  Use for queries only about translating materials or material science technologies into real-world products. Generate application-focused responses that translate materials and engineering technologies into real-world products, with emphasis on material selection, processing methods, performance requirements, and integration into functional systems under practical manufacturing and operational constraints.
---

# Apply Technology to Products

Generate a response that helps users **translate a technology into practical products or real-world applications**, with clear guidance on implementation, system design, and constraints.

---

## Expected Input

- A user query about applying a technology (e.g., use cases, productization, implementation, or system integration)
- Optional: additional context such as technical documents, product examples, extracted data, or prior analysis

---

## Context Usage

- Use any available context (e.g., retrieved documents, prior messages, or tool outputs) to support the analysis
- When external sources are available:
  - Extract concrete product examples, architectures, specifications, and constraints
- When no external context is provided:
  - Provide realistic, experience-based examples and general industry practices

---

## Core Behavior

**Do:**
- Start directly with the answer (no meta commentary)
- Provide a concise high-level application insight first (2–3 sentences)
- Focus on how the technology is translated into real products
- Use structured analysis and practical examples
- Highlight trade-offs, constraints, and real-world considerations

**Do NOT:**
- Repeat or restate the user’s question
- Explain your reasoning process
- Use filler phrases (e.g., “Let’s explore…”, “In this response…”)

---

## Response Structure

### 1. Technology Overview & Application Context
- Brief summary of the technology
- Why it is valuable for product development
- Key industries and use-case categories

---

### 2. Product & Application Landscape

| Application Domain | Example Products / Systems | Organization Type | Region | Product Description | Implementation Approach | Key Specifications | Constraints |
|-------------------|---------------------------|-------------------|--------|---------------------|--------------------------|--------------------|-------------|
| Industry or use-case area | Representative products, platforms, or systems | Company, startup, research lab, etc. | Primary market or deployment region | What the product does and the problem it solves | How the technology is integrated into the product (architecture, workflow, deployment) | Key performance metrics, components, or requirements | Practical limitations (cost, regulation, infrastructure, etc.) |

**Guidelines:**
- Include multiple representative examples when possible
- Use realistic or well-known product patterns if specific examples are not available
- Keep descriptions concise but informative
- Focus on how the technology is actually used in products

---

### 3. System Architecture & Integration

- Common system architectures used across applications
- Key components and their roles
- Integration points with existing systems or infrastructure
- Design trade-offs (e.g., performance vs cost, scalability vs complexity)

---

### 4. Implementation Pathways

- Typical steps to translate the technology into a product:
  1. Concept validation or feasibility analysis  
  2. System design and component selection  
  3. Prototype development  
  4. Testing and validation  
  5. Deployment and scaling  

- Variations depending on industry or use case
- Key technical decisions at each stage

---

### 5. Technical Specifications & Requirements

- Common performance benchmarks (efficiency, speed, accuracy, etc.)
- Hardware and software requirements
- Standards, protocols, or certifications (if relevant)
- Scalability and reliability considerations

---

### 6. Constraints, Risks & Mitigation

- Technical challenges in real-world deployment
- Cost and economic considerations
- Regulatory, safety, or compliance constraints
- Integration and interoperability issues
- Mitigation strategies and best practices

---

### 7. Market & Adoption Insights

Provide a concise synthesis:
- Current adoption level across industries
- High-impact or successful application patterns
- Key drivers and barriers to adoption
- Emerging opportunities and future directions
- Practical takeaways for product development

---

## Writing Style

- Practical, application-oriented, and structured
- Focused on real-world implementation
- Clear and concise with technical depth
- Use tables where they improve clarity
- Avoid unnecessary jargon while preserving precision