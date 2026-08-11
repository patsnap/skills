# Technology Taxonomy and OLED Seed Tags

Use this reference to define evidence-backed technology routes. The OLED tags below preserve the source's domain example in English, but they are discovery seeds rather than a complete, mutually exclusive, or current taxonomy.

## Taxonomy record contract

Each route requires:

- stable `id`;
- English `name`;
- definition;
- inclusion and exclusion criteria;
- synonyms and acronyms;
- disambiguation terms and known false positives;
- parent, child, and related route IDs;
- evidence IDs and review date;
- maturity framework and evidence when maturity is reported;
- review status and confidence;
- safe renderer slug derived from the ID.

## OLED seed taxonomy

### 1. Tandem OLED

`id: tandem-oled`

Multi-emissive-unit OLED stack architectures intended to alter luminance, efficiency, lifetime, or operating conditions. Include tandem/stacked emissive units only when the record describes the architecture; exclude generic multilayer OLED references.

Suggested terms: tandem OLED, stacked OLED, multi-stack OLED, multiple emissive units. Review product marketing names manually.

### 2. Quantum-dot OLED (QD-OLED)

`id: qd-oled`

OLED display architectures using quantum-dot color conversion or related quantum-dot integration. Exclude quantum-dot electroluminescent displays unless the scoped taxonomy intentionally includes them.

### 3. White OLED (WOLED)

`id: woled`

White-emitting OLED architectures and color-filter implementations. Disambiguate white OLED lighting from display applications when the scope is display-only.

### 4. Fine-metal-mask alternatives

`id: fmm-alternatives`

Patterning or deposition routes designed to reduce or eliminate conventional fine metal mask constraints. Source examples mention ViP and eLEAP; verify proprietary names, owners, and definitions from dated evidence.

### 5. LTPO and hybrid backplanes

`id: ltpo-hybrid-backplanes`

Low-temperature polycrystalline oxide and related LTPS/oxide hybrid backplane architectures. Exclude generic oxide TFT records that do not concern the hybrid route.

### 6. High-mobility oxide backplanes

`id: high-mobility-oxide`

Oxide semiconductor materials, devices, and processes directed to improved carrier mobility or backplane performance. Record the material system and measurement conditions.

### 7. Polarizer-free and color-on-encapsulation

`id: polarizer-free-coe`

Polarizer-free OLED stacks, color filter on encapsulation, and related optical-stack routes. Disambiguate `COE` from unrelated acronyms.

### 8. OLED emissive materials

`id: oled-emissive-materials`

Host, dopant, phosphorescent, thermally activated delayed fluorescence (TADF), hyperfluorescence, and related emissive-material systems. Split into child routes when the decision requires material-level granularity.

### 9. Flexible OLED

`id: flexible-oled`

Flexible substrates, device stacks, encapsulation, interconnects, mechanics, and manufacturing for bendable OLED systems. The word `display` alone is not a valid classifier.

### 10. Foldable OLED displays

`id: foldable-oled`

Foldable device mechanics, crease mitigation, stack durability, hinge interactions, and repeated-bending performance. Distinguish panels from complete devices and components.

### 11. Stretchable OLED displays

`id: stretchable-oled`

Stretchable device structures, materials, interconnects, substrates, encapsulation, and deformation management. Require explicit stretchability evidence.

### 12. Automotive OLED displays

`id: automotive-oled`

OLED systems and qualification issues specific to automotive displays. Do not tag generic automotive news without an OLED technical link.

### 13. Micro-lens arrays

`id: oled-micro-lens-array`

Micro-lens-array and related light-extraction structures used with OLED devices. Disambiguate MLA from machine-learning and other acronyms.

### 14. Inkjet-printed OLED

`id: inkjet-printed-oled`

Inkjet printing, printable materials, droplet/process control, drying, patterning, and manufacturing integration for OLED. Exclude generic printing without OLED relevance.

### 15. Under-display camera integration

`id: under-display-camera-oled`

OLED optical, pixel, driving, compensation, and image-processing adaptations for under-display cameras. Disambiguate UDC/FDC acronyms and separate panel from camera algorithm evidence.

### 16. Generation 8-class OLED manufacturing

`id: gen-8-oled-manufacturing`

Generation 8-class substrate, equipment, process, yield, investment, and manufacturing evidence. Record the exact substrate generation and source definition rather than grouping all `G8` strings automatically.

## Why the source keyword matcher is insufficient

Simple substring matching creates false positives and misses context. Examples:

- `material` is too broad for OLED emissive materials;
- `display` is too broad for flexible OLED;
- `UDC`, `MLA`, `COE`, and `IVO` are ambiguous;
- one record may validly map to several related routes;
- marketing names may change or be used inconsistently.

## Classification workflow

1. Normalize the record language without discarding the original.
2. Identify the technical subject, function, components, and application.
3. Generate candidate tags from controlled terms, classifications, and semantic evidence.
4. Apply inclusion and exclusion criteria.
5. Record matching passages and the classifier/reviewer.
6. Assign one or more tags with confidence.
7. Mark ambiguous records for manual review.
8. Reconcile parent/child and duplicate tags.

## Classification output

```json
{
  "record_id": "E042",
  "technology_ids": ["tandem-oled", "oled-emissive-materials"],
  "matches": [
    {
      "technology_id": "tandem-oled",
      "basis": "The source describes two serially connected emissive units.",
      "source_location": "abstract, sentences 2-3",
      "confidence": "high",
      "review_status": "checked"
    }
  ]
}
```

## Maturity and trend labels

If the portal reports maturity or momentum, define the framework and evidence. Keep research activity, patenting, capital investment, product announcement, qualification, manufacturing capacity, and commercial shipment separate. Do not infer one from another.

## Page rendering

The renderer creates `tech-{safe-slug}.html`. Each page shows definition, criteria, synonyms, evidence coverage, associated organizations, dated records, patent evidence, maturity/uncertainty, gaps, and refresh triggers.

## Generalizing beyond OLED

For another domain, replace the seed list with a reviewed taxonomy but preserve this file's record contract and classification workflow. Do not relabel OLED tags with unrelated terms or reuse their classifier keywords.
