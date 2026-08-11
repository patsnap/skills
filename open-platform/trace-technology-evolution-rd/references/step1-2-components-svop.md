# Stages 1–2: System Decomposition and SVOP Anchors

## Position in the workflow

- Stage 1 decomposes the authorized product or technical system.
- Stage 2 converts selected components and critical parts into searchable SVOP expressions.
- Stage 3 consumes the resulting anchors for parallel patent and non-patent research.
- This reference preserves the source headphone example as a worked method example, not as current evidence or a mandatory ontology.

## Required project header

Record before analysis:

- project and product name;
- product boundary and excluded variants;
- decision context;
- evidence cutoff;
- geographies and languages;
- operating environments;
- target users and stakeholders;
- current baseline;
- target outcomes;
- confidentiality constraints;
- analyst and reviewer;
- decomposition version and review status.

## Stage 1 — Decompose the system

### 1.1 Hierarchy

Use five levels when they improve search traceability:

```text
Product or technical system
→ major system
→ subsystem
→ component
→ critical part or functional module
```

Definitions:

- **Product or technical system**: the authorized object and its declared boundary.
- **Major system**: a high-level functional grouping meaningful for the domain.
- **Subsystem**: a coherent physical, computational, biological, or operational unit.
- **Component**: a unit specific enough to support a distinct technical search.
- **Critical part or functional module**: an element whose constraints, interfaces, tradeoffs, or ecosystem justify independent analysis.

The source uses execution, control, power, and transmission as first-level groups. These are useful for many engineered products, but they are not universal. A medical, chemical, software, or biological system may need other groups. Document any adapted ontology.

### 1.2 Critical-unit review

Evaluate each candidate independently across four dimensions:

1. **Constraint independence** — governed by a distinct physical, chemical, biological, computational, or manufacturing constraint.
2. **Tradeoff independence** — carries a distinct engineering contradiction or optimization tradeoff.
3. **Interface independence** — has a stable or reviewable interface and can plausibly change separately.
4. **Ecosystem independence** — has a distinct supplier, research, standards, regulatory, or developer community.

The source used a mechanical four-point keep/merge/delete score. Do not retain that shortcut. Instead record:

| Field | Required content |
|---|---|
| Candidate ID | Stable local identifier |
| Candidate name | Controlled English term |
| Parent | Parent component or subsystem |
| Constraint evidence | Source location and explanation |
| Tradeoff evidence | Source location and explanation |
| Interface evidence | Source location and explanation |
| Ecosystem evidence | Source location and explanation |
| Decision | retain / merge / exclude / unresolved |
| Rationale | Why the decision improves analysis |
| Search consequence | Coverage gained or lost |
| Reviewer | Named review role |

Retain a unit when independent analysis materially affects the decision. Merge it when a parent search covers it without hiding a distinct path. Exclude it only with documented rationale. Keep unresolved units visible until review.

### 1.3 Boundary checks

- Do not confuse a product configuration with a universal system architecture.
- Do not treat an installation location as a distinct technology when the mechanism is the same.
- Do not split parameters into parts unless they have independent mechanisms or ecosystems.
- Do not merge software, algorithms, protocols, or information models merely because they lack a physical part.
- Do not omit safety, security, control, manufacturing, service, or enabling infrastructure when they affect the decision.
- Record cross-cutting units explicitly instead of duplicating them under every branch.

## Worked decomposition: headphone family

The following is a localized structural example from the source. Validate every term and boundary for an actual engagement.

### 2.1 Scope

Illustrative family:

- true wireless stereo earbuds;
- in-ear headphones;
- over-ear headphones;
- open-ear devices;
- bone-conduction devices.

Potential exclusions must be declared, for example hearing aids, professional monitoring systems, or headsets with separate compute packs.

### 2.2 Example hierarchy

```text
Headphone product family
│
├─ Execution system
│  ├─ Acoustic-output subsystem
│  │  └─ C1 Transducer assembly
│  │     ├─ P1.1 Diaphragm
│  │     ├─ P1.2 Voice coil or actuator
│  │     └─ P1.3 Magnetic or drive circuit
│  └─ Acoustic-structure subsystem
│     └─ C2 Acoustic enclosure
│
├─ Control system
│  ├─ Noise-control subsystem
│  │  └─ C3 Active-noise-control module
│  │     └─ P3.1 Control algorithm
│  └─ Capture subsystem
│     └─ C4 Microphone array
│        ├─ P4.1 Microphone sensor
│        └─ P4.2 Beamforming processor
│
├─ Power system
│  └─ Energy-storage subsystem
│     └─ C5 Battery
│        ├─ P5.1 Positive electrode
│        ├─ P5.2 Negative electrode
│        ├─ P5.3 Electrolyte
│        └─ P5.4 Package or enclosure
│
└─ Communication system
   └─ Wireless subsystem
      └─ C6 Wireless system-on-chip
         ├─ P6.1 Radio-frequency front end
         ├─ P6.2 Baseband processor
         ├─ P6.3 Antenna
         └─ P6.4 Protocol-stack firmware
```

This example contains four major systems, six subsystems, six components, and thirteen critical units. Those counts are source-case design choices, not targets for other products.

### 2.3 Example merge and exclusion decisions

| Candidate | Source decision | Localized review guidance |
|---|---|---|
| Support or frame | Merged or excluded | Reconsider if structural modes, fit, durability, manufacturing, or modular interfaces affect the decision |
| Front and rear cavities | Merged into acoustic enclosure | Split only if independently controlled, manufactured, or searched |
| Tuning mesh and damping material | Treated as enclosure parameters | Retain independently when material mechanisms or supplier ecosystems matter |
| Feedforward and feedback microphone positions | Not separate sensor technologies | Keep position as architecture metadata rather than duplicate sensor records |
| Adaptive filter | Merged into the control algorithm | Split when algorithm family, certification, compute, or training lifecycle requires independent analysis |
| Array topology | Treated as a design parameter | May deserve its own functional module in spatial-array research |

Do not copy the source's decisions without checking the project question.

## Stage 2 — SVOP functional abstraction

### 3.1 Canonical expression

```text
Subject → Verb → Object → Parameter
```

The parameter is the measurable property changed, maintained, transferred, constrained, or observed through the action.

### 3.2 Field rules

| Field | Rule | Failure mode |
|---|---|---|
| Subject | Specific functional unit under analysis | So broad that results cannot be assigned back to a unit |
| Verb | Transferable technical action | Product-specific marketing phrase or meaningless verb such as “affect” |
| Object | Physical, informational, biological, or computational entity acted on | Material brand or overly abstract “thing” |
| Parameter | Measurable property of the interaction or object | Unrelated product specification or unsupported target |
| Conditions | Operating state, medium, boundary, or load | Missing conditions make numerical values incomparable |
| Synonyms | Terms, spellings, acronyms, and translations | Narrow recall and language bias |
| Exclusions | Known false-positive mechanisms | Cross-domain noise overwhelms useful analogies |

### 3.3 Abstraction test

For each anchor:

1. run or design an in-domain test query;
2. identify at least three plausibly different product families that share the function;
3. inspect false positives produced by the generalized verb and object;
4. narrow with mechanism, condition, parameter, or exclusion terms;
5. retain both the specific and generalized query versions;
6. document why the final level fits the decision.

“Three product families” is a diagnostic, not a rigid acceptance quota.

### 3.4 Multiple functions

The source retained only a single primary function. The localized method records:

- primary function;
- material secondary functions;
- function priority;
- whether each function receives a separate search track;
- interaction or conflict between functions.

Discard a secondary function only when it cannot materially affect route analysis.

## Worked component-level SVOP anchors

| ID | Unit | Subject | Verb | Object | Parameters and conditions | Cross-domain anchor |
|---|---|---|---|---|---|---|
| C1 | Transducer assembly | transducer | convert | energy forms | acoustic pressure, frequency response, efficiency, distortion under stated load | convert energy form |
| C2 | Acoustic enclosure | enclosure | tune | wave field | resonance, quality factor, response uniformity, volume and boundary conditions | tune wave field |
| C3 | Active-noise-control module | active controller | cancel | disturbance field | residual level, bandwidth, convergence, stability and latency | cancel disturbance field |
| C4 | Microphone array | sensor array | spatially sample | field distribution | directivity, spatial resolution, SNR and geometry | spatially sample field |
| C5 | Battery | energy-storage device | store and release | energy | gravimetric/volumetric density, cycle life, power, temperature and safety | store and release energy |
| C6 | Wireless system-on-chip | transceiver system | relay | information flow | throughput, latency, jitter, loss, energy per bit and coexistence | relay information flow |

Every numerical target must identify source, units, conditions, and whether it is a requirement, observed result, benchmark, or analyst assumption.

## Worked critical-unit anchors

### Execution system

| ID | Unit | Subject → verb → object | Candidate parameters | Cross-domain families |
|---|---|---|---|---|
| P1.1 | Diaphragm | diaphragm → actuate → elastic medium | pressure, bandwidth, displacement, distortion, modal behavior | loudspeakers, ultrasonic transducers, piezoelectric actuators, MEMS emitters |
| P1.2 | Voice coil or actuator | actuator → drive → mechanical load | force, displacement, bandwidth, efficiency, thermal state | linear motors, valves, locks, MEMS actuators |
| P1.3 | Magnetic or drive circuit | field circuit → establish → drive field | field strength, uniformity, leakage, volume, loss | motors, transformers, magnetic bearings, sensors |

### Control system

| ID | Unit | Subject → verb → object | Candidate parameters | Cross-domain families |
|---|---|---|---|---|
| P3.1 | Noise-control algorithm | controller → cancel → disturbance field | residual level, bandwidth, convergence, stability, compute and latency | acoustic, vibration, electromagnetic and wave control |
| P4.1 | Microphone sensor | sensor → transduce → physical field into signal | SNR, dynamic range, bandwidth, linearity and noise | acoustic, pressure, optical, inertial and magnetic sensors |
| P4.2 | Beamforming processor | array processor → shape → spatial response | beam width, sidelobes, robustness, latency and compute | radar, sonar, ultrasound, radio arrays and astronomy |

### Power system

| ID | Unit | Subject → verb → object | Candidate parameters | Cross-domain families |
|---|---|---|---|---|
| P5.1 | Positive electrode | electrode → insert and extract → charge carrier | capacity, potential, rate, stability and temperature | rechargeable batteries, electrochromic systems and ion storage |
| P5.2 | Negative electrode | electrode → store and release → charge carrier | capacity, potential, rate, expansion and cycle stability | batteries and electrochemical storage |
| P5.3 | Electrolyte | medium → transport → charged particles | conductivity, selectivity, stability window and temperature | batteries, fuel cells, membranes and biological ion transport |
| P5.4 | Package or enclosure | barrier → limit → mass and energy transfer | permeability, pressure, impact, thermal transfer and sealing | electronics, medical devices, food, aerospace and batteries |

### Communication system

| ID | Unit | Subject → verb → object | Candidate parameters | Cross-domain families |
|---|---|---|---|---|
| P6.1 | RF front end | transceiver → modulate and recover → carrier | selectivity, linearity, noise, efficiency and coexistence | radio, radar, satellite, optical and power-line communication |
| P6.2 | Baseband processor | processor → encode and decode → digital stream | error rate, compression, latency, compute and energy | communications, storage and media coding |
| P6.3 | Antenna | radiator → couple → current and electromagnetic field | efficiency, bandwidth, directivity, size and detuning | radio, terahertz, metasurfaces and optical antennas |
| P6.4 | Protocol stack | protocol system → schedule and negotiate → end-to-end link | latency, jitter, loss, reliability, security and interoperability | wireless, Ethernet, fieldbus and time-sensitive networks |

## Search-anchor register

For each unit create:

```json
{
  "unit_id": "P4.2",
  "unit_name": "Beamforming processor",
  "primary_svop": {
    "subject": "array processor",
    "verb": "shape",
    "object": "spatial response",
    "parameters": ["beam width", "sidelobe suppression", "latency"]
  },
  "secondary_functions": [],
  "conditions": ["declared geometry", "declared frequency band"],
  "in_domain_terms": [],
  "cross_domain_terms": [],
  "synonyms": [],
  "classifications": [],
  "exclusions": [],
  "source_locations": [],
  "review_status": "reviewed"
}
```

## Stage gate

Do not begin broad research until:

- scope and variants are explicit;
- every retained unit has a parent and rationale;
- merge/exclusion decisions are documented;
- every SVOP parameter has units or a declared qualitative definition;
- synonyms and exclusions are prepared;
- software and cross-cutting units are not silently lost;
- the user or designated reviewer accepts the decomposition when it materially controls downstream work;
- confidential details are safe to use in approved research services.

## Output

Deliver:

- decomposition register;
- reviewed mind-map JSON and HTML when requested;
- critical-unit decision log;
- component and critical-unit SVOP register;
- query-anchor packets;
- unresolved-boundary list;
- review status and version history.

## Limitations

- System boundaries are analyst choices and may change the resulting routes.
- Functional abstraction may improve recall while reducing precision.
- A unit may participate in several functions and route families.
- Product terminology and classification practice differ by language and jurisdiction.
- The worked headphone decomposition is illustrative and may age.
- No decomposition establishes novelty, FTO, market attractiveness, or feasibility.
