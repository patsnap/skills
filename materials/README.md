# 🧪 Materials Science Agent Skills

This repository provides a set of **domain-specific agent skills** designed to support **materials science research, engineering analysis, and industrial applications**.

These skills enable AI agents to generate **structured, high-quality, and technically grounded responses** across key materials workflows, including:

* Technology understanding
* Landscape scouting
* Problem solving
* Product translation
* Alloy composition analysis

---

## 🎯 Design Principles

The skills are designed with the following goals:

* **Materials-first focus**
  Centered on metals, polymers, ceramics, composites, semiconductors, and energy materials.

* **Structured outputs**
  Responses follow consistent formats (tables, analysis sections) for clarity and usability.

* **Engineering relevance**
  Emphasis on real-world constraints such as manufacturability, cost, and performance.

* **Evidence-oriented reasoning**
  Designed to leverage external data sources (e.g., patents, technical documents, MCP tools).

* **Agent-friendly routing**
  Each skill has a clearly defined scope to improve selection accuracy.

---

## 🧠 Available Skills

### 1. `understand-technology`

**Purpose:**
Explain materials science and engineering concepts in a structured and practical way.

**Typical Use Cases:**

* “What is solid-state electrolyte and how does it work?”
* “Explain structure–property relationships in polymers”
* “How does microstructure affect material performance?”

**Core Capabilities:**

* Scientific principles and mechanisms
* Structure–property relationships
* Processing–performance linkage
* Advantages and limitations

---

### 2. `scout-tech-landscape`

**Purpose:**
Analyze technology landscapes across materials domains using patents, literature, and industry signals.

**Typical Use Cases:**

* “Who are the key players in solid-state batteries?”
* “What is the technology landscape of graphene materials?”
* “Map the value chain for hydrogen storage materials”

**Core Capabilities:**

* Value chain mapping
* Key organizations and players
* Patent and publication trends
* Technology maturity and adoption

---

### 3. `solve-tech-problems`

**Purpose:**
Provide solution-oriented analysis for materials engineering challenges.

**Typical Use Cases:**

* “How to improve battery cycle life?”
* “How to reduce porosity in casting?”
* “How to prevent corrosion in marine environments?”

**Core Capabilities:**

* Material selection and substitution
* Composition and microstructure optimization
* Processing improvements
* Failure analysis and mitigation
* Trade-off evaluation (cost, performance, manufacturability)

---

### 4. `tech-to-product`

**Purpose:**
Translate materials and technologies into real-world products and systems.

**Typical Use Cases:**

* “How are battery materials used in EV systems?”
* “How to apply graphene in electronics products?”
* “How are ceramics used in high-temperature components?”

**Core Capabilities:**

* Product application mapping
* System architecture and integration
* Material selection and processing
* Performance specifications and constraints
* Manufacturing and deployment considerations

---

### 5. `alloy-composition-search`

**Purpose:**
Search, filter, and analyze alloy compositions using structured data and patent sources.

**Typical Use Cases:**

* “Find Ni-based alloys with Co > 10%”
* “Search Fe-Cr-Ni alloys with nitrogen addition”
* “Compare compositions similar to Inconel 718”

**Core Capabilities:**

* Composition filtering (element, percentage ranges)
* Classification (low / medium / high content)
* Element relationship logic (AND / OR / ONLY / MAJORITY)
* Structured composition tables
* Patent-based alloy analysis

---

## 🔌 MCP Integration (Optional but Recommended)

These skills can be enhanced with the **MACE MCP (Materials Alloy Composition Extraction)** tools.

### MCP Pipeline

```
Natural Language Query
        ↓
query_to_alloy
        ↓
alloy_to_substance
        ↓
substance_to_document
        ↓
document_to_alloy
        ↓
Structured Alloy Data
```

### Key Capabilities

* Extract structured alloy compositions from text
* Match compositions to known substances
* Retrieve relevant patents and documents
* Access detailed alloy composition datasets

---

## 🧩 How Skills Work Together

These skills are designed to cover **different stages of materials workflows**:

| Stage                      | Skill                      |
| -------------------------- | -------------------------- |
| Understand materials       | `understand-technology`    |
| Explore ecosystem          | `scout-tech-landscape`     |
| Solve engineering problems | `solve-tech-problems`      |
| Build real-world products  | `tech-to-product`          |
| Retrieve composition data  | `alloy-composition-search` |

---

## 🚀 Example Workflow

**Query:**
“Improve cycle life of lithium-ion battery cathode”

1. `understand-technology` → explain degradation mechanisms
2. `scout-tech-landscape` → identify industry trends
3. `solve-tech-problems` → propose material solutions
4. `tech-to-product` → map into battery system design

---

## 🛠 Usage

* Integrate these skills into your agent framework (e.g., Claude Agents, MCP-enabled systems)
* Route user queries to the most appropriate skill based on intent
* Optionally connect to MCP tools for enhanced data retrieval

---

## 📌 Notes

* These skills are optimized for **materials science and engineering domains**
* Outputs are designed to be:

  * Structured
  * Technical
  * Practical
* No strict dependency on proprietary formats (portable across agents)

---

## 🤝 Contributing

Contributions are welcome:

* Improve skill definitions
* Add new materials domains
* Extend MCP integrations
* Enhance output structures

---

## 📄 License

Specify your license here (e.g., MIT, Apache 2.0)

---
