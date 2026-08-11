# Protection-Path Decision Framework

Use this framework to recommend a review path, not to make the final legal or business decision. Applicable law, contracts, ownership, disclosure, security controls, tax/export rules, employee obligations, and business strategy vary by jurisdiction and organization.

## Decision sequence

### 1. Confirm a technical asset

Ask whether the record contains a specific technical implementation and whether the organization is authorized to evaluate it. If not, collect evidence or archive with rationale.

### 2. Identify disclosure urgency

Record exact publication, sale, use, demonstration, repository, conference, standards, customer, supplier, or investor events. Capture date, audience, access controls, NDA/contract status, and content disclosed.

Do not assume that submission, discussion, or publication has the same legal effect everywhere. Escalate potentially time-sensitive facts promptly to qualified counsel.

### 3. Assess observability and detectability

Can a third party learn the contribution from a product, service behavior, documentation, regulatory submission, publication, testing, reverse engineering, or employee movement? Can unauthorized use be detected and proven?

High observability may support patent review. Low observability may support trade-secret review, but only if reasonable secrecy controls are practical.

### 4. Assess independent-development risk

Consider competitor capability, technical convergence, standards, publication trends, workforce mobility, and ease of experimentation. Independent development is not stopped by trade-secret protection.

### 5. Assess disclosure and transaction needs

Consider licensing, collaboration, investment, standards participation, customer qualification, regulatory submissions, open-source obligations, procurement, and publication. Trade secrets can be licensed and transferred, but require contractual and operational controls; do not state that they are non-transferable.

### 6. Assess lifecycle and enforceability

Consider technology lifetime, time to obtain rights, jurisdictions, cost, detectability, claim scope uncertainty, and expected product evolution. Do not use one universal patent term or maintenance rule.

### 7. Assess secrecy feasibility

Review:

- need-to-know access;
- contractual duties;
- repository and document controls;
- logging and offboarding;
- supplier/customer access;
- physical and cybersecurity;
- data provenance and third-party rights;
- ability to separate public and confidential knowledge.

### 8. Select a review path

Possible recommendations:

- patent review;
- trade-secret review;
- dual-track review while disclosure remains controlled;
- defensive-publication review;
- collect more evidence;
- monitor;
- archive with reason.

## Comparison table

| Dimension | Patent review | Trade-secret review | Defensive publication | Monitor/archive |
|---|---|---|---|---|
| Disclosure | Requires eventual disclosure if pursued | Requires continuing secrecy | Intentionally public | Depends on record policy |
| Independent development | May provide exclusion within granted scope | Generally not prevented | Prevents later novelty claims only as law allows | No exclusion |
| Reverse engineering | Often favors review | Weakens practical secrecy | Not a protection goal | Accept risk |
| Detectability | Important for enforcement | Important for misuse evidence | Not applicable | Not applicable |
| Duration | Jurisdiction/right specific | While requirements and secrecy persist | Public indefinitely where hosted | Internal retention policy |
| Transaction use | Licensable/transferable subject to rights | Licensable/transferable with controls | Public asset | Context dependent |
| Cost | Filing, prosecution, maintenance, enforcement | Security, contracts, governance, enforcement | Review and publication | Review/storage |

## Technology-specific considerations

### Software and algorithms

Eligibility and patentability vary. Focus on the claimed technical implementation and technical effect, but do not promise eligibility. Review source-code exposure, open-source licenses, model/data provenance, service observability, and the feasibility of keeping implementation details secret.

### AI and machine learning

Separate model architecture, training/control procedure, data curation, evaluation, deployment optimization, hardware interaction, and business use. Training data, weights, prompts, parameters, and operational know-how may require different paths and security controls.

### Hardware-software systems

Map the combined system and independently useful subcomponents. Do not prescribe a universal claim portfolio; an IP professional should assess claim categories and jurisdictions.

### Parameters, formulations, and materials

Assess reverse engineering, analytical detectability, process know-how, range boundaries, comparative evidence, safety/regulatory disclosure, and reproducibility.

## Recommendation output

For each candidate include:

1. recommended review path;
2. alternative path;
3. reasons tied to evidence;
4. disclosure status and urgency;
5. missing legal, security, technical, or commercial facts;
6. owner for the next action;
7. target date based on verified events, not a universal seven-day rule;
8. specialist review required;
9. interim confidentiality control;
10. decision-revisit trigger.

## Prohibited shortcuts

- Do not recommend patenting solely because a product can be reverse engineered.
- Do not recommend secrecy without testing whether secrecy controls are reasonable.
- Do not call a disclosure harmless based on a generic grace-period statement.
- Do not infer ownership or inventorship from employment or document authorship.
- Do not equate a crowded search with `do not protect`.
- Do not treat a promising screen as authorization to file.
- Do not expose confidential details in the report distribution list.
