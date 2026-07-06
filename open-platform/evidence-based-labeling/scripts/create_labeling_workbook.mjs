import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const output = process.argv[2];
if (!output) throw new Error("Usage: node create_labeling_workbook.mjs <output.xlsx>");

const wb = Workbook.create();
const sheets = [
  ["Source Data", ["record_id", "title", "source_text"]],
  ["Labeling Results", ["record_id", "formal_labels", "candidate_labels", "label_status", "confidence", "needs_review", "review_reason", "taxonomy_version", "rules_version", "mcp_enrichment_status"]],
  ["Evidence", ["record_id", "dimension", "label_id", "label_path", "label_status", "evidence_field", "evidence_excerpt", "reason", "confidence", "needs_review", "review_reason", "source_type", "source_identifier"]],
  ["Review Queue", ["record_id", "issue_type", "issue_detail", "suggested_action", "review_status", "reviewer_note"]],
  ["Taxonomy Backlog", ["gap_id", "gap_type", "affected_records", "current_handling", "proposed_taxonomy_or_rule_change", "priority", "record_review_required"]],
  ["Taxonomy", ["label_id", "dimension", "label_name", "label_path", "parent_label_id", "definition", "include_when", "exclude_when", "synonyms", "confusable_labels", "positive_example", "negative_example", "status", "taxonomy_version"]],
  ["Decision Rules", ["rule_key", "rule_value", "rules_version", "user_modified", "notes"]],
  ["QA Summary", ["metric", "value", "status", "notes"]],
  ["Task Info", ["key", "value", "confirmation_status", "confirmed_at"]],
  ["MCP Provenance", ["timestamp", "stage", "service", "tool", "purpose", "query_summary", "record_or_label_id", "returned_identifiers", "status", "notes"]],
];

for (const [name, headers] of sheets) {
  const sheet = wb.worksheets.add(name);
  sheet.showGridLines = false;
  const header = sheet.getRangeByIndexes(0, 0, 1, headers.length);
  header.values = [headers];
  header.format = { fill: "#1F4E78", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
  header.format.rowHeightPx = 32;
  sheet.freezePanes.freezeRows(1);
  const widths = headers.map((h) => Math.min(260, Math.max(90, h.length * 10 + 24)));
  headers.forEach((_, i) => { sheet.getRangeByIndexes(0, i, 200, 1).format.columnWidthPx = widths[i]; });
}

await fs.mkdir(path.dirname(path.resolve(output)), { recursive: true });
const blob = await SpreadsheetFile.exportXlsx(wb);
await blob.save(output);
console.log(output);
