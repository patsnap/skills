import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path


MARKER = "    initDates();"
STATIC_ASSET_DIR_SUFFIX = "_assets"


def copy_assets(output_path: Path, app_dir: Path) -> str:
    asset_dir = output_path.with_suffix("").name + STATIC_ASSET_DIR_SUFFIX
    target = output_path.parent / asset_dir
    target.mkdir(parents=True, exist_ok=True)
    for rel in (
        "assets/scout-logo-header-transparent.png",
        "assets/value-page.png",
    ):
        shutil.copy2(app_dir / rel, target / Path(rel).name)
    return asset_dir


def replace_asset_paths(html: str, asset_dir: str) -> str:
    for name in (
        "scout-logo-header-transparent.png",
        "value-page.png",
    ):
        html = html.replace(f'src="/assets/{name}"', f'src="{asset_dir}/{name}"')
        html = html.replace(f'src="assets/{name}"', f'src="{asset_dir}/{name}"')
    return html


def make_static(html: str, report_data: dict) -> str:
    params = report_data.get("params") or {}
    seed = (
        f"    window.INITIAL_REPORT_PARAMS = {json.dumps({'date_from': params.get('date_from'), 'date_to': params.get('date_to')}, ensure_ascii=False)};\n"
        f"    window.INITIAL_REPORT_DATA = {json.dumps(report_data, ensure_ascii=False)};\n"
    )
    if MARKER not in html:
        raise RuntimeError("Could not find init marker in template")
    html = html.replace(MARKER, seed + MARKER, 1)
    html = html.replace('<button id="runBtn" type="button">开始筛查</button>', "")
    html = html.replace("    .report-mode #runBtn { display: none; }\n", "")
    html = re.sub(r"\n    async function runSearch\(\) \{.*?\n    function exportCsv\(\) \{", "\n    function exportCsv() {", html, flags=re.S)
    html = html.replace('    $("runBtn").addEventListener("click", runSearch);\n', "")
    html = html.replace("设置条件后点击“开始筛查”。", "本报告已生成首轮筛查结果，可在表格内搜索、排序并导出。")
    html = html.replace("开始筛查后，将按晶型专利到期时间展示进入主表的重点候选。", "暂无重点候选。")
    html = html.replace("开始筛查后，未进入主表的候选会在这里展示。", "暂无未进入主表记录。")
    html = html.replace("开始筛查后自动汇总晶型专利与化合物专利编号。", "本报告已自动汇总晶型专利与化合物专利编号。")
    return html


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a standalone 仿药速探 V1 static HTML report.")
    parser.add_argument("--data", default=None, help="Report JSON. Defaults to bundled sample-report-data.json.")
    parser.add_argument("--output", default=None, help="Output HTML path.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    app_dir = skill_root / "assets" / "platform-template" / "app"
    template_path = app_dir / "index.html"
    data_path = Path(args.data).resolve() if args.data else skill_root / "references" / "sample-report-data.json"
    output_path = Path(args.output).resolve() if args.output else Path.cwd() / f"仿药速探V1_静态报告_{date.today().isoformat()}.html"

    report_data = json.loads(data_path.read_text(encoding="utf-8-sig"))
    if "result" in report_data and "rows" not in report_data:
        result = report_data["result"] or {}
        result.setdefault("params", report_data.get("params") or result.get("params") or {})
        report_data = result
    html = template_path.read_text(encoding="utf-8")
    asset_dir = copy_assets(output_path, app_dir)
    html = replace_asset_paths(html, asset_dir)
    html = make_static(html, report_data)
    output_path.write_text(html, encoding="utf-8")
    print(f"Created static report: {output_path}")
    print(f"Copied assets to: {output_path.parent / asset_dir}")


if __name__ == "__main__":
    main()
