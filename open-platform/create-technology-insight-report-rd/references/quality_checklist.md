# Technology Insight Report — Release Review Checklist

Use this checklist after automated validation. A numeric total does not override a failed blocking gate.

## A. Scope, decision, and metadata

- [ ] Decision context, audience, technical boundary, geographies, languages, and exclusions are explicit.
- [ ] Report date and evidence cutoff use ISO dates and are not conflated.
- [ ] Version matches title, metadata, and footer.
- [ ] Review status and next-review date are visible.
- [ ] Confidentiality and external-research authorization were respected.
- [ ] Patent count unit, family normalization, and entity normalization are disclosed.

## B. Ten-section completeness

- [ ] s0 Decision brief contains evidence-linked actions, owners, milestones, uncertainties, and specialist boundaries.
- [ ] s1 Market and industry context contains definition-compatible evidence or an explicit gap.
- [ ] s2 Technology routes separates route, maturity, performance, adoption, and timing.
- [ ] s3 Competitive and value-chain evidence uses declared inclusion criteria and comparable fields.
- [ ] s4 Patent landscape distinguishes matched, returned, reviewed, accepted, publication, and family counts.
- [ ] s5 Standards and regulation includes identifier, status, clause, jurisdiction, and effective/as-of date.
- [ ] s6 Signals and candidate gaps uses bounded “not observed” language and search IDs.
- [ ] s7 Emerging applications includes transfer conditions, barriers, and validation requirements.
- [ ] s8 Technical options and specialist review avoids automated infringement/FTO conclusions.
- [ ] s9 Vertical scenario uses an appropriate evidence-backed comparison rather than decorative scoring.
- [ ] No required section is empty; not-applicable/evidence-gap states include rationale and consequences.

## C. Evidence and source register

- [ ] Every factual finding resolves to accepted evidence IDs.
- [ ] Every accepted record appears once in the complete source register.
- [ ] Stable links/identifiers are present and verified.
- [ ] Evidence dates do not exceed the cutoff.
- [ ] Direct, corroborating, and contradicting evidence roles are distinguished.
- [ ] Repeated secondary reports are not counted as independent sources.
- [ ] Source authority, directness, independence, method, recency, and applicability are reviewed.
- [ ] Inaccessible, rejected, duplicate, and superseded records remain traceable outside accepted findings.
- [ ] Quotations and reproductions respect licensing/copyright limits.

## D. Patent integrity and legal boundary

- [ ] Publication/application/grant/family identifiers are not conflated.
- [ ] Earliest priority, publication, and relevant status dates are correct.
- [ ] Legal status includes jurisdiction and “as of” date.
- [ ] Claims or description locations reviewed are recorded.
- [ ] Claim-relevance screening uses dated product/feature evidence.
- [ ] All-elements correspondence is documented without percentage shortcuts.
- [ ] Review priority is not labeled infringement risk.
- [ ] Technical options are not called confirmed design-arounds.
- [ ] No absolute FTO, infringement, validity, enforceability, or patentability conclusion appears.
- [ ] Qualified patent-professional review is requested where material.

## E. Search and metric integrity

- [ ] Every search records tool/source, query, filters, language, date, limit, returned/reviewed IDs, pagination, and limitations.
- [ ] `matched_total` is labeled reported/estimated/unavailable and not treated as reviewed records.
- [ ] Pagination, truncation, segmentation, overlap, and deduplication are disclosed.
- [ ] Search universe and denominator accompany every trend/share/ranking.
- [ ] Transparent samples are labeled with selection method and not presented as population statistics.
- [ ] Candidate gaps include terminology, classification, language, citation/family/actor, and non-patent checks as relevant.
- [ ] No zero result is described as proof that no patent/technology/standard exists.
- [ ] Sparse, failed, omitted, and inaccessible tracks are visible.

## F. Market and economic evidence

- [ ] Market definition, segment, geography, currency, price year, base year, and forecast year are explicit.
- [ ] Publisher-reported value, publisher forecast, and analyst scenario are distinct.
- [ ] CAGR start/end values and formula reconcile.
- [ ] Currency conversion and inflation treatment are disclosed.
- [ ] Conflicting sources and scope differences remain visible.
- [ ] Porter, PEST, BCG, S-curve, or other frameworks use evidence and do not create facts.
- [ ] No market estimate is backfilled merely to complete a chart.

## G. Technology, company, standards, and application analysis

- [ ] Route definitions and versions are consistent across sections.
- [ ] TRL or maturity labels cite evidence and defined anchors.
- [ ] Company inclusion follows global, neutral, evidence-based criteria.
- [ ] Corporate names, aliases, relationships, and dates are normalized.
- [ ] Patent activity, products, partnerships, announcements, and market position remain distinct.
- [ ] Standards/regulatory claims distinguish draft, published, mandatory, voluntary, superseded, and withdrawn states.
- [ ] Application analogies name shared mechanism, different conditions, barriers, and required validation.
- [ ] “No public evidence found” is not described as no activity.

## H. Cross-section reconciliation

- [ ] s0 recommendations derive from final accepted evidence and analyses.
- [ ] s1 market figures match every reuse in s0/s9.
- [ ] s2 route terms match s3 company comparisons and s7/s9 applications.
- [ ] s4 patent records match s0 priorities and s8 technical options/specialist actions.
- [ ] s4/s5 evidence-gap candidates match s6 wording and search IDs.
- [ ] s7 transfer conditions match s9 vertical scenario.
- [ ] Organization, patent, standard, and event status dates match everywhere.
- [ ] All displayed totals reconcile with the source register under labeled units.

## I. HTML structure, accessibility, and security

- [ ] s0–s9 anchors exist once and in order.
- [ ] Every ID is unique.
- [ ] Table header/body column counts reconcile.
- [ ] Tables have captions or nearby scope and responsive overflow.
- [ ] Headings follow a logical hierarchy.
- [ ] Links use HTTP(S), mailto, or resolved internal anchors.
- [ ] No local path, source-only domestic domain, secret, or credential remains.
- [ ] No script, external runtime, external stylesheet/font, gradient, unsafe DOM, or raw user HTML remains.
- [ ] Color is not the sole carrier of meaning.
- [ ] Desktop, narrow-screen, and print layouts are reviewed.
- [ ] Explicit empty states are accessible and informative.
- [ ] `scripts/quality_check.py` passes all automated gates.

## J. Release decision

- [ ] Complete report read-through is finished.
- [ ] Domain reviewer signs off or affected findings are withheld.
- [ ] Patent professional signs off where claim/legal conclusions are material or those conclusions are withheld.
- [ ] Safety, regulatory, clinical, financial, or other specialist review is complete where applicable.
- [ ] Evidence licensing and confidentiality are acceptable for the audience.
- [ ] Open warnings have owners and documented exceptions.
- [ ] Release status is recorded: ready for review / approved / withheld / superseded.
- [ ] Delivered filename, version, report date, evidence cutoff, and next-review date are correct.

## Blocking gates

Release is blocked by any of:

- unresolved evidence IDs or unsupported factual findings;
- incorrect patent identity/status/claim references;
- automated infringement/FTO or absolute legal claim;
- undisclosed metric denominator/count unit/coverage limitation;
- global-white-space claim based on search absence;
- inconsistent cross-section facts or totals;
- unresolved placeholders;
- external runtime, unsafe content handling, local paths, credentials, or legacy domestic domains;
- failed specialist boundary for a material conclusion;
- failed automated structure/version/table/link/metadata gate.

## Review record

| Role | Name | Scope reviewed | Date | Status | Open issues |
|---|---|---|---|---|---|
| Analyst | | | YYYY-MM-DD | | |
| Technical reviewer | | | YYYY-MM-DD | | |
| Patent professional | | | YYYY-MM-DD | | |
| Other specialist | | | YYYY-MM-DD | | |
| Release approver | | | YYYY-MM-DD | | |
