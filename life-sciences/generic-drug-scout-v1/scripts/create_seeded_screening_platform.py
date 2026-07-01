import argparse
import importlib.util
import json
import shutil
from datetime import date
from pathlib import Path


MARKER = "    initDates();"
DEFAULT_TARGET = "仿药速探V1_首轮结果平台"


def add_years(day: date, years: int) -> date:
    try:
        return day.replace(year=day.year + years)
    except ValueError:
        return day.replace(month=2, day=28, year=day.year + years)


def load_server_module(server_path: Path):
    spec = importlib.util.spec_from_file_location("generic_drug_scout_v1_server", server_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load server module: {server_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ensure_safe_target(target: Path, skill_root: Path) -> None:
    if target == skill_root or skill_root in target.parents:
        raise SystemExit("Refusing to overwrite files inside the skill package. Choose a separate --target directory.")
    if target.anchor and target == Path(target.anchor):
        raise SystemExit(f"Refusing to use drive root as target: {target}")


def inject_initial_data(index_path: Path, data: dict, date_from: str, date_to: str) -> None:
    html = index_path.read_text(encoding="utf-8")
    seed = (
        f"    window.INITIAL_REPORT_PARAMS = {json.dumps({'date_from': date_from, 'date_to': date_to}, ensure_ascii=False)};\n"
        f"    window.INITIAL_REPORT_DATA = {json.dumps(data, ensure_ascii=False)};\n"
    )
    if MARKER not in html:
        raise RuntimeError("Could not find init marker in index.html")
    html = html.replace(MARKER, seed + MARKER, 1)
    index_path.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run 仿药速探 V1 first screening and create an interactive platform preloaded with results."
    )
    parser.add_argument("--target", default=DEFAULT_TARGET, help="Directory where the seeded platform should be created.")
    parser.add_argument("--date-from", default=date.today().isoformat(), help="Crystal patent expiry window start.")
    parser.add_argument("--date-to", default=None, help="Crystal patent expiry window end.")
    parser.add_argument("--window-years", type=int, default=2, help="Used when --date-to is omitted.")
    parser.add_argument("--retrieval-cap", type=int, default=100)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    date_from = args.date_from
    date_to = args.date_to or add_years(date.fromisoformat(date_from), args.window_years).isoformat()

    skill_root = Path(__file__).resolve().parents[1]
    template = skill_root / "assets" / "platform-template"
    target = Path(args.target).resolve()
    server_path = template / "app" / "server.py"

    ensure_safe_target(target, skill_root)
    if target.exists():
        if not args.overwrite:
            raise SystemExit(f"Target already exists: {target}. Pass --overwrite to replace it.")
        shutil.rmtree(target)

    server = load_server_module(server_path)
    params = {
        "drug_type": "Small molecule drug",
        "country": "CN",
        "date_from": date_from,
        "date_to": date_to,
        "retrieval_cap": args.retrieval_cap,
    }
    result = server.build_report(params)

    shutil.copytree(template, target)

    output_json = target / "first_screening_result.json"
    output_json.write_text(
        json.dumps(
            {
                "params": params,
                "result": result,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    inject_initial_data(target / "app" / "index.html", result, date_from, date_to)

    print(f"Created seeded platform at: {target}")
    print(f"Screening result JSON: {output_json}")
    print(f"Run: python {target / 'app' / 'server.py'}")
    print("Open: http://127.0.0.1:8790/")


if __name__ == "__main__":
    main()
