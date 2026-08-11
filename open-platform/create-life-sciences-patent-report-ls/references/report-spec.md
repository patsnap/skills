# Life Sciences Patent Report Specification

## 1. Source and link contract

### 1.1 Source record

Maintain one record for every cited item:

```json
{
  "source_id": "PAT-001",
  "source_type": "patent|trial|trial_result|drug|target|paper|translational|regulatory|deal|news|figure|other",
  "display_id": "WO...A1",
  "entity_id": "provider identifier",
  "title": "...",
  "exact_url": "https://...",
  "url_origin": "MCP returned URL|official source|verified primary source",
  "query_or_tool": "...",
  "retrieved_at": "YYYY-MM-DDThh:mm:ssZ",
  "database_cutoff": "YYYY-MM-DD|null",
  "supports": ["finding-01"],
  "evidence_class": "primary|secondary|database-derived",
  "confidence": "high|medium|low",
  "notes": ""
}
```

### 1.2 Link priority

1. exact URL returned by the global PatSnap MCP/source;
2. verified official patent office, trial registry, regulator, journal/publisher, company filing, or other primary source;
3. verified stable secondary source when the primary source is unavailable;
4. identifier and source name without a hyperlink when no stable URL is available.

### 1.3 Forbidden routing

Do not:

- construct a product frontend URL from an MCP UUID unless current global documentation defines it;
- insert an entity UUID into a list/search `query_id`;
- insert a publication number, NCT number, title, company, or display name into a UUID-only parameter;
- insert a provider UUID into a parameter documented for a search-session ID;
- replace a source-returned URL with an assumed domestic route;
- expose API keys or signed/private URL tokens.

If a returned URL is temporary or authenticated, cite the stable identifier and primary source instead.

### 1.4 Patent links

For patents, preserve publication/application/grant identities. Link to the exact returned global PatSnap record URL or the corresponding official patent-office record. Do not synthesize a patent-detail path. Record kind code and verify that the URL resolves to the intended publication/member.

### 1.5 Link audit table

| Source ID | Display ID | URL type | Identifier expected | Identifier supplied | Verified date | Result |
|---|---|---|---|---|---|---|

Any mismatch blocks report release.

## 2. Report metadata

The HTML must expose:

- report title and version;
- subject and anchor identifiers;
- audience and decision;
- jurisdictions/languages;
- analysis cutoff and generation timestamp/time zone;
- patent/family counting rule;
- data sources and database cutoffs;
- release status: draft, provisional, review-ready, or monitoring update;
- author/reviewer role;
- confidentiality classification;
- link/interaction validation status.

## 3. Recommended information architecture

Include applicable chapters and explain omissions.

### 3.1 Overview

- precise research question;
- three to six evidence-backed findings;
- key metrics with denominators/counting rule;
- opportunity/risk/uncertainty callout;
- scope, cutoff, and known gaps.

### 3.2 Patent core

- representative and material family members;
- publication/application/grant numbers;
- title, applicants/assignees/inventors;
- priority, filing, publication, and grant dates;
- family/continuity relationships;
- target-jurisdiction legal status with retrieval date;
- CPC/IPC with scheme caveat;
- current relevant claims and versions;
- source links.

### 3.3 Target or technology background

- target biology or technical problem;
- modality/platform definition;
- mechanism and relevant disease context;
- terminology/taxonomy used in the search;
- source-evidence hierarchy and limitations.

### 3.4 Claims and technical architecture

As applicable:

- independent/material dependent claims;
- sequence/SEQ ID/CDR/scaffold;
- target/epitope/function;
- antibody format/Fc/glycan;
- payload/linker/conjugation/DAR;
- small-molecule structure/SAR;
- formulation/manufacturing/analytical features;
- use, biomarker, dose, regimen, or combination;
- claim-feature matrix and uncertainty.

Separate claim text, specification disclosure, and analyst interpretation.

### 3.5 Experimental evidence

- assay and model;
- construct/sample;
- endpoint/unit/time point;
- controls/comparator;
- sample size/statistics where reported;
- exact value/range and source locator;
- patent figure/table citation;
- what the result supports and does not support.

Examples may include affinity, internalization, cytotoxicity, IC50/EC50, DAR, SEC/aggregation, PK, tolerability, xenograft TGI, biomarkers, or process/formulation performance. Do not compare values across incompatible assays without caveat.

### 3.6 Pipeline and clinical landscape

- drug/asset aliases and sponsor;
- modality/target/payload or mechanism;
- indication and phase/status;
- milestone date/source;
- trial identifiers and geography;
- discontinued/terminated/unknown distinctions;
- relationship to the patent thesis.

### 3.7 Clinical results

- trial/result source and cutoff;
- population, intervention, comparator;
- endpoint and analysis set;
- efficacy/safety result with unit and uncertainty;
- publication/registry status;
- limitations and whether inference to the patent technology is justified.

### 3.8 Patent landscape and legal implications

- search method and funnel;
- family/publication counts and legal-status breakdown;
- technical-route/assignee/jurisdiction/time views;
- key families and claim themes;
- whitespace/opportunity hypotheses;
- FTO/validity/enforceability questions clearly framed as issues for counsel;
- monitoring priorities.

Do not issue an infringement or FTO opinion from a landscape.

### 3.9 Scientific, translational, and regulatory evidence

- papers or translational records;
- guidelines or labels where relevant;
- evidence design and quality;
- relationship to patent assertions;
- conflicting or negative evidence;
- source links and retrieval dates.

### 3.10 Company, deal, and news context

- verified company/legal entity;
- deal type, parties, asset/scope, territory, date, disclosed economics;
- original announcement/filing where possible;
- news event date versus publication date;
- fact versus interpretation;
- explicit warning that a commercial announcement does not prove patent assignment/license scope.

### 3.11 Patent figure index

| Figure ID | Patent/member | Original figure/table | Local file | Caption | Used in sections | Verification |
|---|---|---|---|---|---|---|

### 3.12 Sources and audit

- source register;
- complete search queries/filters;
- counting and family rules;
- excluded/omitted evidence;
- link audit;
- local asset audit;
- data and interpretation limitations;
- update/monitoring plan.

## 4. Scientific/editorial HTML system

### 4.1 Document shell

```html
<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>...</title>
  <style>/* inline, report-scoped CSS */</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to report</a>
  <header class="report-head">...</header>
  <nav class="report-nav" aria-label="Report sections">...</nav>
  <main id="main">...</main>
  <footer>...</footer>
  <div id="img-float" role="tooltip" hidden>...</div>
  <script>/* optional progressive enhancement */</script>
</body>
</html>
```

### 4.2 Visual variables

```css
:root {
  --canvas: #f6f8fa;
  --surface: #ffffff;
  --surface-alt: #edf3f5;
  --ink: #17212b;
  --muted: #596674;
  --line: #d5dde3;
  --accent: #1f6675;
  --accent-soft: #e1f0f3;
  --amber: #8a5a19;
  --amber-soft: #fbf1df;
  --red: #9a3b34;
  --red-soft: #f8e9e7;
  --green: #366b50;
  --green-soft: #e5f1ea;
  --violet: #5f5684;
  --violet-soft: #eeeaf7;
}
```

Use system fonts. Maintain at least WCAG-compatible contrast. Status cannot depend on color alone.

### 4.3 Layout

- `.wrap` or equivalent max-width about 1200–1320 px;
- concise header rather than a landing-page hero;
- sticky navigation only above a wide-screen breakpoint;
- semantic `<section aria-labelledby>` blocks;
- alternating section treatment only when it improves scanability;
- grids of two to five columns that collapse responsibly;
- compact metrics with definition/denominator/source;
- `.table-wrap` for responsive tables;
- evidence callouts for finding, caution, risk question, opportunity, and limitation;
- no gradient, glow, particle, ticker, decorative animation, or copied product chrome.

### 4.4 Metrics

Every metric card includes:

- value;
- unit;
- label;
- denominator/counting rule;
- as-of date;
- source ID;
- `not reported` rather than zero when absent.

### 4.5 Tables

Use `<caption>`, `<thead>`, scoped `<th>`, and explicit units. Provide a mobile wrapper and repeat headers in print. Do not hide evidence in hover-only cells.

### 4.6 Source chips

```html
<a class="source-chip"
   href="VERIFIED_EXACT_URL"
   target="_blank"
   rel="noopener noreferrer"
   data-source-id="PAT-001">PAT-001 · WO…A1</a>
```

If no stable URL exists, use a non-link `<span class="source-chip">` and provide identifier/source in the source register.

### 4.7 Sequences

```html
<pre class="sequence" aria-label="Heavy-chain variable region sequence">...</pre>
```

Wrap long sequences, preserve monospacing, identify sequence version/region/numbering/source, and avoid embedding confidential sequences without authorization.

## 5. Inline patent-figure references

### 5.1 Markup

```html
<a class="figure-ref"
   href="assets/project/pat-001-fig-12.png"
   data-img="assets/project/pat-001-fig-12.png"
   data-caption="PAT-001 · Figure 12 · xenograft response"
   target="_blank"
   rel="noopener noreferrer">PAT-001 Fig. 12</a>
```

The normal link is the fallback. The local path must be report-relative, URL-encoded where needed, and present on disk.

### 5.2 CSS

```css
.figure-ref {
  display: inline-flex;
  align-items: center;
  padding: .08rem .42rem;
  border: 1px dashed var(--amber);
  border-radius: .35rem;
  color: var(--amber);
  background: var(--amber-soft);
  text-decoration: none;
  font-size: .82em;
}
.figure-ref:hover,
.figure-ref:focus-visible {
  color: #fff;
  background: var(--amber);
  outline: 2px solid transparent;
}
#img-float {
  position: fixed;
  z-index: 1000;
  pointer-events: none;
  width: min(430px, 92vw);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: .5rem;
  box-shadow: 0 12px 34px rgba(23,33,43,.22);
  overflow: hidden;
}
#img-float[hidden] { display: none; }
#img-float img {
  display: block;
  width: 100%;
  max-height: 62vh;
  object-fit: contain;
  background: #fff;
}
#img-float .caption { padding: .55rem .7rem; color: var(--muted); }
```

### 5.3 Progressive-enhancement script

```html
<script>
(() => {
  const box = document.querySelector('#img-float');
  if (!box) return;
  const image = box.querySelector('img');
  const caption = box.querySelector('.caption');
  const place = event => {
    const pad = 14, gap = 16;
    box.hidden = false;
    const rect = box.getBoundingClientRect();
    let x = event.clientX + gap;
    let y = event.clientY - rect.height / 2;
    if (x + rect.width + pad > innerWidth) x = event.clientX - rect.width - gap;
    x = Math.max(pad, x);
    y = Math.max(pad, Math.min(y, innerHeight - rect.height - pad));
    box.style.left = `${x}px`;
    box.style.top = `${y}px`;
  };
  document.querySelectorAll('.figure-ref').forEach(ref => {
    const show = event => {
      image.src = ref.dataset.img || ref.href;
      image.alt = ref.dataset.caption || ref.textContent.trim();
      caption.textContent = ref.dataset.caption || ref.textContent.trim();
      place(event);
    };
    const hide = () => { box.hidden = true; image.removeAttribute('src'); };
    ref.addEventListener('mouseenter', show);
    ref.addEventListener('mousemove', place);
    ref.addEventListener('mouseleave', hide);
    ref.addEventListener('focus', event => {
      const rect = ref.getBoundingClientRect();
      show({clientX: rect.right, clientY: rect.top + rect.height / 2});
    });
    ref.addEventListener('blur', hide);
  });
})();
</script>
```

Keep previews supplemental: users must be able to open the figure and understand the citation without hover.

## 6. Theme behavior

Dark mode is optional. If included:

- use a button with accessible name and `aria-pressed`;
- persist preference locally only if appropriate;
- respect `prefers-color-scheme` and explicit user selection;
- verify source chips, figures, tables, callouts, and print remain legible;
- never use a dark screenshot as evidence of scientific quality.

## 7. Print contract

```css
@media print {
  @page { size: A4; margin: 14mm; }
  body { background: #fff; color: #000; font-size: 10pt; }
  .report-nav, .theme-control, #img-float { display: none !important; }
  section, figure, table { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  thead { display: table-header-group; }
  a[href]::after { content: " (" attr(href) ")"; font-size: 8pt; }
}
```

Do not expose private/signed URLs in printed output; replace them with stable identifiers.

## 8. Validation protocol

### 8.1 HTML parse

Use an available standards parser. Python's basic `html.parser` can detect some structural issues but is not a full conformance validator. Record tool and result accurately.

### 8.2 Static route audit

Search generated HTML for:

- `query_id=` and determine the documented identifier type;
- `patentId=` or similar and verify the value type;
- list/detail paths that were manually constructed;
- domestic/legacy domains;
- API keys and authorization parameters;
- external `http(s)` CSS/JS/font/image dependencies;
- absolute Unix/Windows developer paths;
- duplicate element IDs;
- empty/malformed links.

Do not use a regex that only catches patent-number prefixes and call the route audit complete. Validate every parameter against the source map.

### 8.3 Local asset audit

Extract values from:

- `<img src>`;
- `<a href>` when local;
- `data-img`;
- CSS `url(...)`.

Resolve each relative to the HTML file, normalize without escaping the report directory, and verify it is a regular file. Ensure every inline figure appears in the figure index and every index entry has an existing file.

### 8.4 Browser audit

When a browser is available, test:

- initial render and console errors;
- navigation anchors;
- keyboard tab order/focus;
- figure hover and focus preview;
- opening figure fallback;
- optional theme toggle;
- narrow viewport at approximately 360–390 px;
- tablet and desktop widths;
- print preview;
- no unexpected network requests.

### 8.5 Evidence audit

- reconcile metrics to tables/source register;
- sample every chapter's citations;
- verify claim versions/status dates;
- verify trial/result/paper/deal identifiers;
- distinguish event date from publication/retrieval date;
- check that interpretation is no stronger than evidence;
- record unresolved contradictions.

## 9. Release checklist

- [ ] New version created; prior reports preserved.
- [ ] Scope, cutoff, jurisdictions, languages, and counting rules shown.
- [ ] Required/optional/omitted modules identified.
- [ ] Exact source URLs and IDs recorded before drafting.
- [ ] No entity UUID or display ID is placed in an incompatible route parameter.
- [ ] No manually invented frontend route remains.
- [ ] Patent, scientific, experimental, clinical, regulatory, deal, and news evidence are separated.
- [ ] Every specific claim/number/date has a source.
- [ ] Family/status/counting rules reconcile.
- [ ] Figures exist, support nearby text, and have accessible fallback.
- [ ] HTML is self-contained and parses.
- [ ] Responsive, keyboard, hover/focus, and print checks ran or are precisely caveated.
- [ ] No external dependency, credential, absolute path, or uncontrolled confidential data remains.
- [ ] Report limitations and update plan are visible.
