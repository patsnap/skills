import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const input = process.argv[2];
if (!input) throw new Error("Usage: node inspect_labeling_input.mjs <input.xlsx|input.csv>");
const ext = path.extname(input).toLowerCase();
let workbook;
if (ext === ".xlsx") {
  workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
} else if (ext === ".csv") {
  const csvText = (await fs.readFile(input, "utf8")).replace(/^\uFEFF/, "");
  workbook = await Workbook.fromCSV(csvText, { sheetName: "Source Data" });
} else {
  throw new Error(`Unsupported input type: ${ext}`);
}
const result = await workbook.inspect({
  kind: "workbook,sheet,table,region",
  include: "id,name,values",
  tableMaxRows: 8,
  tableMaxCols: 20,
  tableMaxCellChars: 160,
  maxChars: 12000,
});
process.stdout.write(result.ndjson);
process.exit(0);
