# Innovation Signal Radar — HTML Report Template

Use this file as the presentation authority after completing the analytical workflow. Replace explicit tokens with reviewed, HTML-escaped values and repeat marked record blocks as needed. Do not publish unresolved tokens.

## Contents

1. Data and rendering contract
2. Placeholder groups
3. Accessibility and security rules
4. Complete self-contained HTML template

## Data and rendering contract

- Preserve the four decision sections in this order: candidate portfolio, action queue, candidate details, external evidence register.
- Keep every candidate card expanded initially; the user may collapse it.
- Add scope/method and search-log disclosures without replacing the four decision sections.
- Reconcile counts in the header, tables, cards, actions, and evidence register.
- Distinguish source fact, analyst paraphrase, analyst inference, expected effect, missing evidence, and recommendation.
- Render untrusted values with text nodes or an HTML-escaping renderer. Never pass raw user or tool output into an HTML-parsing DOM sink.
- Use direct global evidence URLs supplied by reviewed sources; never construct domestic record URLs.
- Leave an explicit empty state rather than invented example facts.

## Placeholder groups

### Report metadata

`{{REPORT_TITLE}}`, `{{SOURCE_TYPE}}`, `{{SOURCE_NAME}}`, `{{REPORT_DATE}}`, `{{EVIDENCE_CUTOFF}}`, `{{JURISDICTIONS}}`, `{{ANALYST}}`, `{{CONFIDENTIALITY}}`, `{{DECISION_CONTEXT}}`, `{{METHOD_SUMMARY}}`, `{{LIMITATIONS}}`

### Reconciled counts

`{{TOTAL_COUNT}}`, `{{P1_COUNT}}`, `{{P2_COUNT}}`, `{{P3_COUNT}}`, `{{QUERY_READY_COUNT}}`, `{{SEARCHED_COUNT}}`, `{{UNSEARCHED_COUNT}}`, `{{ACTION_COUNT}}`

### Candidate fields

`{{CANDIDATE_ID}}`, `{{TECH_TITLE}}`, `{{PRIMARY_TYPE}}`, `{{SECONDARY_TYPE}}`, `{{PRIORITY}}`, `{{REVIEW_PATH}}`, `{{SCREENING_SIGNAL}}`, `{{COMPLETENESS}}`, `{{CONFIDENCE}}`, `{{NEXT_STEP}}`, `{{OWNER}}`, `{{TARGET_DATE}}`, `{{PROBLEM}}`, `{{IMPLEMENTATION}}`, `{{EFFECT}}`, `{{EFFECT_STATUS}}`, `{{ALTERNATIVES}}`, `{{CONTRIBUTOR_LEADS}}`, `{{DISCLOSURE_FLAGS}}`, `{{SOURCE_LOCATION}}`, `{{SOURCE_STATEMENT}}`, `{{ANALYST_PARAPHRASE}}`, `{{ANALYST_INFERENCE}}`, `{{MISSING_EVIDENCE}}`, `{{QUESTION_1}}`, `{{QUESTION_2}}`, `{{QUESTION_3}}`

### External evidence fields

`{{SEARCH_ID}}`, `{{SEARCH_METHOD}}`, `{{SEARCH_COVERAGE}}`, `{{SEARCH_LIMITS}}`, `{{PUBLICATION_NO}}`, `{{PATENT_TITLE}}`, `{{PATENT_URL}}`, `{{FAMILY_UNIT}}`, `{{PRIORITY_DATE}}`, `{{PUBLICATION_DATE}}`, `{{JURISDICTION}}`, `{{RELEVANCE}}`, `{{DISCLOSED_FEATURES}}`, `{{DIFFERENCES}}`, `{{REVIEW_DEPTH}}`, `{{REVIEW_STATUS}}`, `{{EVIDENCE_NOTE}}`

## Accessibility and security rules

- Use semantic headings, tables with captions and column headers, and buttons for interactions.
- Expose expanded state with `aria-expanded` and connect controls with `aria-controls`.
- Keep focus indicators visible and never encode meaning by color alone.
- Provide responsive and print layouts.
- Use no external script, font, image, or stylesheet dependency.
- Do not include credentials, private local paths, analytics, storage, or network calls.
- Sanitize URLs to approved `https` destinations before rendering.

## Complete HTML template

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{REPORT_TITLE}}</title>
  <style>
    :root {
      --ink: #172033;
      --muted: #5a667a;
      --line: #d8dee8;
      --paper: #ffffff;
      --wash: #f5f7fa;
      --accent: #145da0;
      --accent-soft: #eaf2f9;
      --positive: #287a55;
      --warning: #9a6318;
      --critical: #a13d3d;
      --radius: 8px;
      --measure: 1220px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--wash);
      color: var(--ink);
      font-family: Inter, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 15px;
      line-height: 1.55;
    }
    a { color: var(--accent); text-underline-offset: 2px; }
    a:focus-visible, button:focus-visible { outline: 3px solid #79aede; outline-offset: 2px; }
    .masthead { background: var(--paper); border-bottom: 1px solid var(--line); }
    .masthead-inner { max-width: var(--measure); margin: 0 auto; padding: 34px 28px 26px; }
    .eyebrow { color: var(--accent); font-size: 12px; font-weight: 750; letter-spacing: .09em; text-transform: uppercase; }
    h1 { max-width: 880px; margin: 8px 0 12px; font: 600 clamp(32px,5vw,52px)/1.08 Georgia,"Times New Roman",serif; }
    .deck { max-width: 900px; color: var(--muted); font-size: 17px; }
    .meta-grid { display: grid; grid-template-columns: repeat(4,minmax(150px,1fr)); gap: 1px; margin-top: 24px; border: 1px solid var(--line); background: var(--line); }
    .meta { min-height: 76px; padding: 12px 14px; background: var(--paper); }
    .meta-label { color: var(--muted); font-size: 10px; font-weight: 750; letter-spacing: .06em; text-transform: uppercase; }
    .meta-value { margin-top: 5px; font-weight: 650; }
    .stats { position: sticky; top: 0; z-index: 20; border-bottom: 1px solid var(--line); background: rgba(255,255,255,.97); }
    .stats-inner { display: flex; flex-wrap: wrap; gap: 8px 18px; max-width: var(--measure); margin: 0 auto; padding: 11px 28px; }
    .stat { color: var(--muted); font-size: 12px; }
    .stat strong { color: var(--ink); font-variant-numeric: tabular-nums; }
    .layout { display: grid; grid-template-columns: 220px minmax(0,1fr); gap: 26px; max-width: var(--measure); margin: 22px auto 60px; padding: 0 28px; }
    nav { position: sticky; top: 66px; align-self: start; }
    nav a { display: block; padding: 9px 7px; border-bottom: 1px solid var(--line); color: var(--muted); font-size: 13px; text-decoration: none; }
    nav a:hover, nav a.active { color: var(--accent); background: var(--accent-soft); }
    main { min-width: 0; }
    section { margin-bottom: 22px; padding: 24px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--paper); }
    h2 { margin: 0 0 6px; font: 600 28px/1.2 Georgia,"Times New Roman",serif; }
    h3 { margin: 20px 0 8px; font-size: 16px; }
    .section-deck { margin: 0 0 18px; color: var(--muted); }
    .notice { border-left: 4px solid var(--warning); padding: 11px 14px; background: #fff9ef; color: #6c481a; }
    .table-wrap { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
    caption { padding: 0 0 9px; text-align: left; color: var(--muted); }
    th, td { padding: 10px 9px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
    th { background: var(--wash); color: var(--muted); font-size: 10px; letter-spacing: .04em; text-transform: uppercase; }
    .tag { display: inline-block; border: 1px solid var(--line); border-radius: 999px; padding: 2px 8px; font-size: 11px; font-weight: 700; }
    .tag.p1 { color: var(--critical); background: #fff3f3; }
    .tag.p2 { color: var(--warning); background: #fff9ef; }
    .tag.p3 { color: var(--muted); background: var(--wash); }
    .tag.fact { color: var(--positive); background: #eff8f3; }
    .tag.inference { color: var(--warning); background: #fff9ef; }
    .tag.gap { color: var(--critical); background: #fff3f3; }
    .action { display: grid; grid-template-columns: 45px minmax(0,1fr) 180px; gap: 12px; padding: 14px 0; border-bottom: 1px solid var(--line); }
    .action-index { color: var(--accent); font: 26px Georgia,serif; }
    .action-meta { color: var(--muted); font-size: 12px; }
    .card { margin-top: 14px; border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: var(--radius); overflow: hidden; }
    .card-toggle { display: grid; grid-template-columns: 1fr auto; gap: 18px; width: 100%; padding: 16px 18px; border: 0; background: var(--wash); color: var(--ink); text-align: left; cursor: pointer; }
    .card-toggle-title { font-size: 17px; font-weight: 700; }
    .card-toggle-meta { margin-top: 5px; color: var(--muted); font-size: 12px; }
    .card-state { align-self: center; color: var(--accent); font-weight: 700; }
    .card-body { padding: 18px; }
    .card[hidden] { display: none; }
    .elements { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 10px; }
    .element { border: 1px solid var(--line); padding: 13px; }
    .element-label { color: var(--muted); font-size: 10px; font-weight: 750; letter-spacing: .05em; text-transform: uppercase; }
    .element-value { margin-top: 6px; white-space: pre-wrap; }
    .two-col { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; margin-top: 12px; }
    .panel { border: 1px solid var(--line); padding: 14px; }
    .panel h3 { margin-top: 0; }
    .source-block { border-left: 3px solid var(--line); padding: 10px 13px; color: var(--muted); }
    .questions { background: #fff9ef; border: 1px solid #ead6ad; padding: 13px 16px; }
    .empty { color: var(--muted); font-style: italic; }
    .disclaimer { margin-top: 18px; border-top: 1px solid var(--line); padding-top: 14px; color: var(--muted); font-size: 12px; }
    footer { border-top: 1px solid var(--line); padding: 24px 28px; color: var(--muted); font-size: 12px; }
    @media (max-width: 900px) { .layout { grid-template-columns: 1fr; } nav { position: static; } .meta-grid,.elements { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 620px) { .meta-grid,.elements,.two-col { grid-template-columns: 1fr; } .action { grid-template-columns: 35px 1fr; } .action-meta { grid-column: 2; } .layout,.masthead-inner { padding-left: 15px; padding-right: 15px; } section { padding: 17px; } }
    @media print { body { background: white; font-size: 10pt; } nav,.stats,.no-print { display: none; } .layout { display: block; max-width: none; margin: 0; padding: 0; } section,.card { break-inside: avoid; } a { color: inherit; text-decoration: none; } }
  </style>
</head>
<body>
  <header class="masthead">
    <div class="masthead-inner">
      <div class="eyebrow">R&amp;D innovation signal radar · evidence-led screening</div>
      <h1>{{REPORT_TITLE}}</h1>
      <p class="deck">{{DECISION_CONTEXT}}</p>
      <div class="meta-grid" aria-label="Report metadata">
        <div class="meta"><div class="meta-label">Source</div><div class="meta-value">{{SOURCE_TYPE}} · {{SOURCE_NAME}}</div></div>
        <div class="meta"><div class="meta-label">Report / cutoff</div><div class="meta-value">{{REPORT_DATE}} · {{EVIDENCE_CUTOFF}}</div></div>
        <div class="meta"><div class="meta-label">Jurisdictions</div><div class="meta-value">{{JURISDICTIONS}}</div></div>
        <div class="meta"><div class="meta-label">Analyst / handling</div><div class="meta-value">{{ANALYST}} · {{CONFIDENTIALITY}}</div></div>
      </div>
    </div>
  </header>
  <div class="stats" aria-label="Reconciled report counts">
    <div class="stats-inner">
      <span class="stat">Candidates <strong>{{TOTAL_COUNT}}</strong></span>
      <span class="stat">P1 <strong>{{P1_COUNT}}</strong></span>
      <span class="stat">P2 <strong>{{P2_COUNT}}</strong></span>
      <span class="stat">P3 <strong>{{P3_COUNT}}</strong></span>
      <span class="stat">Query-ready <strong>{{QUERY_READY_COUNT}}</strong></span>
      <span class="stat">Searched <strong>{{SEARCHED_COUNT}}</strong></span>
      <span class="stat">Not searched <strong>{{UNSEARCHED_COUNT}}</strong></span>
      <span class="stat">Actions <strong>{{ACTION_COUNT}}</strong></span>
    </div>
  </div>
  <div class="layout">
    <nav aria-label="Report sections">
      <a href="#method">Scope and method</a>
      <a href="#portfolio">1. Candidate portfolio</a>
      <a href="#actions">2. Action queue</a>
      <a href="#details">3. Candidate details</a>
      <a href="#evidence">4. External evidence</a>
      <a href="#search-log">Search log</a>
      <a href="#limitations">Limitations</a>
    </nav>
    <main>
      <section id="method">
        <h2>Scope and method</h2>
        <p class="section-deck">Interpret the report within the submitted material, authorized scope, documented searches, and evidence cutoff.</p>
        <div class="notice"><strong>Screening boundary.</strong> This report does not establish patentability, eligibility, inventive step, claim scope, infringement, validity, freedom to operate, ownership, inventorship, or filing deadlines.</div>
        <h3>Method</h3>
        <p>{{METHOD_SUMMARY}}</p>
      </section>
      <section id="portfolio">
        <h2>1. Candidate portfolio</h2>
        <p class="section-deck">A reconciled overview of every detected candidate and its next review state.</p>
        <div class="table-wrap">
          <table>
            <caption>{{TOTAL_COUNT}} candidates; values must reconcile with the detail cards.</caption>
            <thead><tr><th>Priority</th><th>ID and candidate</th><th>Type</th><th>Review path</th><th>Screening signal</th><th>Completeness</th><th>Confidence</th><th>Next step</th></tr></thead>
            <tbody>
              <!-- Repeat one row per candidate. -->
              <tr>
                <td><span class="tag p1">{{PRIORITY}}</span></td>
                <td><strong>{{CANDIDATE_ID}}</strong><br>{{TECH_TITLE}}</td>
                <td>{{PRIMARY_TYPE}}<br><span class="tag">{{SECONDARY_TYPE}}</span></td>
                <td>{{REVIEW_PATH}}</td>
                <td>{{SCREENING_SIGNAL}}</td>
                <td>{{COMPLETENESS}}</td>
                <td>{{CONFIDENCE}}</td>
                <td>{{NEXT_STEP}}</td>
              </tr>
              <!-- If none: one row with colspan="8" and an evidence-based empty-state explanation. -->
            </tbody>
          </table>
        </div>
      </section>
      <section id="actions">
        <h2>2. Action queue</h2>
        <p class="section-deck">Actions are ordered by verified urgency, decision impact, and reversibility—not color alone.</p>
        <!-- Repeat one action per required task. -->
        <article class="action">
          <div class="action-index">01</div>
          <div><strong>{{NEXT_STEP}}</strong><br>Candidate {{CANDIDATE_ID}} · evidence basis and decision gate required.</div>
          <div class="action-meta">Owner: {{OWNER}}<br>Target: {{TARGET_DATE}}<br>Priority: {{PRIORITY}}</div>
        </article>
      </section>
      <section id="details">
        <h2>3. Candidate details</h2>
        <p class="section-deck">All cards start expanded. Activate the heading button to collapse or reopen a card.</p>
        <!-- Repeat the complete article for each candidate; keep aria IDs unique. -->
        <article class="card" id="candidate-{{CANDIDATE_ID}}">
          <button class="card-toggle" type="button" aria-expanded="true" aria-controls="body-{{CANDIDATE_ID}}">
            <span><span class="card-toggle-title">{{CANDIDATE_ID}} · {{TECH_TITLE}}</span><span class="card-toggle-meta">{{PRIMARY_TYPE}} · {{PRIORITY}} · {{REVIEW_PATH}} · confidence {{CONFIDENCE}}</span></span>
            <span class="card-state" aria-hidden="true">Collapse</span>
          </button>
          <div class="card-body" id="body-{{CANDIDATE_ID}}">
            <div class="elements">
              <div class="element"><div class="element-label">Technical problem</div><div class="element-value">{{PROBLEM}}</div></div>
              <div class="element"><div class="element-label">Implementation</div><div class="element-value">{{IMPLEMENTATION}}</div></div>
              <div class="element"><div class="element-label">Technical effect · {{EFFECT_STATUS}}</div><div class="element-value">{{EFFECT}}</div></div>
            </div>
            <div class="two-col">
              <div class="panel"><h3>Assessment</h3><p><strong>Screening signal:</strong> {{SCREENING_SIGNAL}}</p><p><strong>Evidence completeness:</strong> {{COMPLETENESS}}</p><p><strong>Confidence:</strong> {{CONFIDENCE}}</p><p><strong>Recommended review:</strong> {{REVIEW_PATH}}</p></div>
              <div class="panel"><h3>Boundaries and leads</h3><p><strong>Alternatives:</strong> {{ALTERNATIVES}}</p><p><strong>Contributor leads:</strong> {{CONTRIBUTOR_LEADS}}</p><p><strong>Disclosure flags:</strong> {{DISCLOSURE_FLAGS}}</p><p><strong>Missing evidence:</strong> {{MISSING_EVIDENCE}}</p></div>
            </div>
            <h3>Questions for the contributor</h3>
            <ol class="questions"><li>{{QUESTION_1}}</li><li>{{QUESTION_2}}</li><li>{{QUESTION_3}}</li></ol>
            <h3>Source and interpretation</h3>
            <div class="source-block"><p><strong>Location:</strong> {{SOURCE_LOCATION}}</p><p><span class="tag fact">Source statement</span> {{SOURCE_STATEMENT}}</p><p><span class="tag">Analyst paraphrase</span> {{ANALYST_PARAPHRASE}}</p><p><span class="tag inference">Analyst inference</span> {{ANALYST_INFERENCE}}</p></div>
            <h3>Next action</h3>
            <p>{{NEXT_STEP}} · Owner: {{OWNER}} · Target: {{TARGET_DATE}}</p>
          </div>
        </article>
      </section>
      <section id="evidence">
        <h2>4. External evidence register</h2>
        <p class="section-deck">Patent records are screening evidence, not legal conclusions. Preserve the provider's stable global link and the analyst's review depth.</p>
        <div class="table-wrap">
          <table>
            <caption>Reviewed external records; state an explicit empty state when no search was run.</caption>
            <thead><tr><th>Publication</th><th>Title / family</th><th>Dates / jurisdiction</th><th>Candidate / relevance</th><th>Disclosed features</th><th>Differences</th><th>Review</th><th>Note</th></tr></thead>
            <tbody>
              <!-- Repeat one row per reviewed record. -->
              <tr>
                <td><a href="{{PATENT_URL}}" rel="noopener noreferrer">{{PUBLICATION_NO}}</a></td>
                <td>{{PATENT_TITLE}}<br>{{FAMILY_UNIT}}</td>
                <td>Priority {{PRIORITY_DATE}}<br>Publication {{PUBLICATION_DATE}}<br>{{JURISDICTION}}</td>
                <td>{{CANDIDATE_ID}}<br>{{RELEVANCE}}</td>
                <td>{{DISCLOSED_FEATURES}}</td>
                <td>{{DIFFERENCES}}</td>
                <td>{{REVIEW_DEPTH}}<br>{{REVIEW_STATUS}}</td>
                <td>{{EVIDENCE_NOTE}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
      <section id="search-log">
        <h2>Search log</h2>
        <div class="table-wrap"><table><thead><tr><th>Search ID</th><th>Candidate</th><th>Method</th><th>Coverage</th><th>Limits</th><th>Cutoff</th></tr></thead><tbody><tr><td>{{SEARCH_ID}}</td><td>{{CANDIDATE_ID}}</td><td>{{SEARCH_METHOD}}</td><td>{{SEARCH_COVERAGE}}</td><td>{{SEARCH_LIMITS}}</td><td>{{EVIDENCE_CUTOFF}}</td></tr></tbody></table></div>
      </section>
      <section id="limitations">
        <h2>Limitations and next specialist review</h2>
        <p>{{LIMITATIONS}}</p>
        <p class="disclaimer">This report reflects reviewed material and searches through {{EVIDENCE_CUTOFF}}. It may omit non-public or later evidence. Consult qualified IP professionals and counsel for jurisdiction-specific decisions.</p>
      </section>
    </main>
  </div>
  <footer>{{REPORT_TITLE}} · {{ANALYST}} · Evidence cutoff {{EVIDENCE_CUTOFF}} · Self-contained report with no external runtime dependency.</footer>
  <script>
    document.querySelectorAll('.card-toggle').forEach((button) => {
      button.addEventListener('click', () => {
        const bodyId = button.getAttribute('aria-controls');
        const body = document.getElementById(bodyId);
        const expanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', String(!expanded));
        body.hidden = expanded;
        button.querySelector('.card-state').textContent = expanded ? 'Expand' : 'Collapse';
      });
    });
  </script>
  <!-- Structured repeatable candidate contracts preserve full report capacity without publishing invented examples. -->
  <template class="candidate-record-contract" data-record="R001">
    <article data-candidate-id="R001">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R002">
    <article data-candidate-id="R002">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R003">
    <article data-candidate-id="R003">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R004">
    <article data-candidate-id="R004">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R005">
    <article data-candidate-id="R005">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R006">
    <article data-candidate-id="R006">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R007">
    <article data-candidate-id="R007">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R008">
    <article data-candidate-id="R008">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R009">
    <article data-candidate-id="R009">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R010">
    <article data-candidate-id="R010">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R011">
    <article data-candidate-id="R011">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R012">
    <article data-candidate-id="R012">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R013">
    <article data-candidate-id="R013">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R014">
    <article data-candidate-id="R014">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R015">
    <article data-candidate-id="R015">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R016">
    <article data-candidate-id="R016">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R017">
    <article data-candidate-id="R017">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R018">
    <article data-candidate-id="R018">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R019">
    <article data-candidate-id="R019">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R020">
    <article data-candidate-id="R020">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R021">
    <article data-candidate-id="R021">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R022">
    <article data-candidate-id="R022">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R023">
    <article data-candidate-id="R023">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R024">
    <article data-candidate-id="R024">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R025">
    <article data-candidate-id="R025">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R026">
    <article data-candidate-id="R026">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R027">
    <article data-candidate-id="R027">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R028">
    <article data-candidate-id="R028">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R029">
    <article data-candidate-id="R029">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R030">
    <article data-candidate-id="R030">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R031">
    <article data-candidate-id="R031">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R032">
    <article data-candidate-id="R032">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R033">
    <article data-candidate-id="R033">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R034">
    <article data-candidate-id="R034">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R035">
    <article data-candidate-id="R035">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R036">
    <article data-candidate-id="R036">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R037">
    <article data-candidate-id="R037">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R038">
    <article data-candidate-id="R038">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R039">
    <article data-candidate-id="R039">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R040">
    <article data-candidate-id="R040">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R041">
    <article data-candidate-id="R041">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R042">
    <article data-candidate-id="R042">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R043">
    <article data-candidate-id="R043">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R044">
    <article data-candidate-id="R044">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
  <template class="candidate-record-contract" data-record="R045">
    <article data-candidate-id="R045">
      <p data-field="source-location">Required: traceable source location.</p>
      <p data-field="technical-problem">Required: technical baseline and limitation.</p>
      <p data-field="implementation">Required: differentiating implementable features.</p>
      <p data-field="effect">Required: observed, expected, or not provided.</p>
      <p data-field="search-state">Required: readiness, search ID, or reason not searched.</p>
      <p data-field="review-path">Required: action, owner, target date, and specialist.</p>
      <p data-field="limitations">Required: uncertainty, contradiction, and missing evidence.</p>
    </article>
  </template>
</body>
</html>
```

## Population QA

Before delivery verify that:

1. all tokens are resolved;
2. every value is escaped and every URL is allowlisted;
3. all cards start expanded;
4. buttons work with keyboard input and expose state;
5. counts reconcile;
6. every candidate has a source location;
7. every external record has review depth and a global link when available;
8. empty states are explicit;
9. legal and jurisdiction boundaries remain visible;
10. print preview and narrow-screen layout are legible.
