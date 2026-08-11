# Competitive patent landscape search strategy

## Contents

1. Scope and counting rules
2. Entity resolution
3. Search modes
4. Date and jurisdiction handling
5. Technology taxonomy
6. Representative-record selection
7. Cross-market comparison
8. Quality checks

## 1. Scope and counting rules

Define the industry and technology boundary before searching.

Record inclusions, exclusions, adjacent technologies, intended use, and noise terms.

Choose the counting unit before calculating metrics:

- Publication.
- Application.
- Simple family.
- Extended family.
- Granted and in-force family.

State the date field: priority, filing, publication, or grant date.

Use a rolling window ending at an ISO 8601 cut-off date.

The source default is five years; allow the user to override it.

## 2. Entity resolution

Do not search a consumer brand as though it were always the patent applicant.

Resolve each competitor to legal entities, subsidiaries, former names, transliterations, and relevant acquisitions.

Record evidence for every added entity.

Distinguish original applicant from current assignee.

Keep uncertain aliases outside the production query until confirmed.

## 3. Search modes

### Mode A: Assignee plus technology query

Use the resolved assignee set with a documented keyword, classification, or nested query.

Conceptual request:

```json
{
  "assignee_scope": ["Verified legal entity A", "Verified subsidiary B"],
  "technology_query": "documented Boolean or nested query",
  "date_basis": "publication",
  "date_from": "rolling-start-date",
  "date_to": "cut-off-date",
  "jurisdictions": ["user-selected jurisdictions"],
  "counting_unit": "simple_family",
  "result_limit": 80
}
```

Translate this conceptual schema into the exact arguments documented by the connected PatSnap tool.

Do not send invented parameter names to an MCP server.

### Mode B: Semantic retrieval

Use semantic search to supplement, not silently replace, the reproducible query.

Record the full semantic prompt, filters, retrieval date, and result cap.

Review semantic-only records for scope drift.

### Mode C: Classification expansion

Use IPC or CPC groups found in seed records to test recall and identify adjacent routes.

Validate every classification before adding it.

Do not apply the tissue-industry taxonomy from the source to unrelated industries.

### Mode D: Citation and similarity expansion

Use citations, similar-patent search, and image similarity to find related records.

Keep expansion results labeled by retrieval channel.

Do not treat citation count as patent value or product importance.

## 4. Date and jurisdiction handling

Use exact dates rather than hard-coded 2021–2026 examples.

Do not include future dates beyond the retrieval cut-off.

Distinguish publication authority from commercial market coverage.

Normalize family members before geographic comparisons when possible.

Record PCT applications separately from national or regional phase entries.

Do not equate a WO publication with enforceable worldwide rights.

## 5. Local-language searching

For Japanese, Korean, Chinese, German, French, or other non-English records, use verified applicant names and relevant local-language terms when they improve recall.

Do not use Chinese keywords as the default supplement for Japanese applicants.

Preserve native-script entity names as query data, not interface prose.

Document transliterations and aliases.

## 6. Technology taxonomy

Build an industry-specific taxonomy from:

- User scope.
- Seed patents.
- Validated IPC/CPC groups.
- Technical literature or standards when relevant.
- Expert review.

Aim for mutually intelligible routes, not forced mutual exclusivity.

Allow multi-label classification when a family spans routes.

Record the rule for assigning each route.

The source tissue example may inform a tissue-sector analysis only:

| Example route | Candidate IPC/CPC area requiring validation |
|---|---|
| Softness and strength processes | D21H, D21F |
| Moisturizing or skin-contact formulations | A61K, relevant D21H subgroups |
| Sustainable fibers and feedstocks | Relevant D21H and D21C subgroups |
| Packaging and product format | Relevant B65D and B65B groups |
| Manufacturing equipment and process | Relevant D21F, B31F, and D21G groups |
| New materials | Relevant D21H and material-specific groups |

Validate subgroup syntax and relevance against official classification sources before use.

## 7. Representative-record selection

Select two or three records per competitor only when enough relevant evidence exists.

Balance:

1. Technical relevance.
2. Independent-claim or disclosure substance.
3. Recency relative to the cut-off.
4. Family breadth and jurisdiction path.
5. Citation context without using citations as a quality proxy.
6. Legal status.
7. Evidence of a distinct strategic signal.

Document why each record was selected.

Do not automatically choose the three most cited records.

## 8. Cross-market comparison

For the same competitor across multiple markets:

1. Use a consistent entity set and technology scope.
2. Retrieve family and jurisdiction data.
3. Normalize duplicate family members.
4. Compare filing routes and technology distributions.
5. Identify directions observed only in one jurisdiction.
6. Test whether the difference reflects filing practice, coverage, sample limits, or strategy.
7. State confidence and alternative explanations.

## 9. Sampling and quality checks

State when results are capped at a top-k sample.

Do not describe sample rank as portfolio-wide rank.

Record total hits separately when a count tool is available.

Review false positives and false negatives.

Check assignee coverage.

Check family deduplication.

Check missing jurisdictions and language bias.

Check taxonomy coverage and overlap.

Check that every reported number can be recomputed.

Store the exact query, filters, dates, tool, and retrieval timestamp in the report methodology.
