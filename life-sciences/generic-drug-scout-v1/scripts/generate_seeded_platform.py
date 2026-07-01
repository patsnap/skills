import argparse
import json
import shutil
from pathlib import Path


MARKER = "    initDates();"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a 仿药速探 V1 platform preloaded with first-screening results.")
    parser.add_argument("--target", required=True, help="Directory where the seeded platform should be created.")
    parser.add_argument("--data", required=True, help="JSON file containing rows, not_promoted, and summary.")
    parser.add_argument("--date-from", required=True)
    parser.add_argument("--date-to", required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template = skill_root / "assets" / "platform-template"
    target = Path(args.target).resolve()
    data_path = Path(args.data).resolve()

    if target.exists():
        if not args.overwrite:
            raise SystemExit(f"Target already exists: {target}. Pass --overwrite to replace it.")
        shutil.rmtree(target)
    shutil.copytree(template, target)

    data = json.loads(data_path.read_text(encoding="utf-8-sig"))
    index_path = target / "app" / "index.html"
    html = index_path.read_text(encoding="utf-8")
    seed = (
        f"    window.INITIAL_REPORT_PARAMS = {json.dumps({'date_from': args.date_from, 'date_to': args.date_to}, ensure_ascii=False)};\n"
        f"    window.INITIAL_REPORT_DATA = {json.dumps(data, ensure_ascii=False)};\n"
    )
    if MARKER not in html:
        raise SystemExit("Could not find init marker in index.html")
    html = html.replace(MARKER, seed + MARKER, 1)
    index_path.write_text(html, encoding="utf-8")
    print(f"Created seeded platform at: {target}")
    print(f"Run: python {target / 'app' / 'server.py'}")
    print("Open: http://127.0.0.1:8790/")


if __name__ == "__main__":
    main()
