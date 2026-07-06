import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const input = process.argv[2];
if (!input) throw new Error("Usage: node validate_labeling_output.mjs <output.xlsx>");
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const required = ["Source Data", "Labeling Results", "Evidence", "Review Queue", "Taxonomy", "Decision Rules", "QA Summary", "Task Info", "MCP Provenance"];
const found = wb.worksheets.items.map((s) => s.name);
const missing = required.filter((name) => !found.includes(name));
const errors = [];
if (missing.length) errors.push(`missing sheets: ${missing.join(", ")}`);
const matrices = {};
for (const name of required.filter((n) => found.includes(n))) {
  const sheet = wb.worksheets.getItem(name);
  const used = sheet.getUsedRange(true);
  if (!used) {
    errors.push(`empty sheet: ${name}`);
  } else {
    matrices[name] = used.values || [];
  }
}

const objects = (name) => {
  const rows = matrices[name] || [];
  if (rows.length < 2) return [];
  const headers = rows[0].map(String);
  return rows.slice(1).filter((r) => r.some((v) => v !== null && v !== "")).map((r) => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
};
const duplicates = (values) => [...new Set(values.filter((v, i) => v && values.indexOf(v) !== i))];
const source = objects("Source Data");
const results = objects("Labeling Results");
const evidence = objects("Evidence");
const taxonomy = objects("Taxonomy");
const sourceIds = source.map((r) => String(r.record_id || "").trim());
const resultIds = results.map((r) => String(r.record_id || "").trim());
const duplicateSourceIds = duplicates(sourceIds);
const duplicateResultIds = duplicates(resultIds);
if (duplicateSourceIds.length) errors.push(`duplicate source record_id: ${duplicateSourceIds.join(", ")}`);
if (duplicateResultIds.length) errors.push(`duplicate result record_id: ${duplicateResultIds.join(", ")}`);
const dropped = sourceIds.filter((id) => id && !new Set(resultIds).has(id));
const unexpected = resultIds.filter((id) => id && !new Set(sourceIds).has(id));
if (source.length && dropped.length) errors.push(`source records missing results: ${dropped.join(", ")}`);
if (unexpected.length) errors.push(`results without source records: ${unexpected.join(", ")}`);

const formalPaths = new Set(taxonomy.filter((r) => String(r.status).trim() === "formal" && String(r.output_eligible || "true").toLowerCase() !== "false").map((r) => String(r.label_path).trim()));
const allowedStatus = new Set(["formal", "candidate", "unclassified", "needs_review"]);
const allowedConfidence = new Set(["high", "medium", "low", "高", "中", "低", ""]);
let illegalFormalLabels = 0;
let missingEvidence = 0;
for (const [index, row] of evidence.entries()) {
  const status = String(row.label_status || "").trim();
  const labelPath = String(row.label_path || "").trim();
  const confidence = String(row.confidence || "").trim();
  if (status && !allowedStatus.has(status)) errors.push(`Evidence row ${index + 2}: invalid label_status ${status}`);
  if (!allowedConfidence.has(confidence)) errors.push(`Evidence row ${index + 2}: invalid confidence ${confidence}`);
  if (status === "formal" && !formalPaths.has(labelPath)) {
    illegalFormalLabels += 1;
    errors.push(`Evidence row ${index + 2}: formal label not in eligible taxonomy: ${labelPath}`);
  }
  if (status === "formal" && !String(row.evidence_excerpt || "").trim()) {
    missingEvidence += 1;
    errors.push(`Evidence row ${index + 2}: formal label lacks evidence`);
  }
}
for (const [index, row] of results.entries()) {
  const status = String(row.label_status || "").trim();
  const confidence = String(row.confidence || "").trim();
  if (status && !allowedStatus.has(status)) errors.push(`Labeling Results row ${index + 2}: invalid label_status ${status}`);
  if (!allowedConfidence.has(confidence)) errors.push(`Labeling Results row ${index + 2}: invalid confidence ${confidence}`);
}

const report = {
  valid: errors.length === 0,
  sheets: found,
  metrics: {
    source_records: source.length,
    result_records: results.length,
    evidence_rows: evidence.length,
    taxonomy_rows: taxonomy.length,
    dropped_source_records: dropped.length,
    unexpected_result_records: unexpected.length,
    illegal_formal_labels: illegalFormalLabels,
    formal_labels_missing_evidence: missingEvidence,
  },
  errors,
};
console.log(JSON.stringify(report, null, 2));
process.exitCode = errors.length ? 1 : 0;
