from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import check_source, distinct_output, load_json, require, source_ref, write_json
from history import STATISTICS_VERSION, current_statistics, validate_statistics, window_key
from chart_selection import select_dimensions


ROOT = Path(__file__).resolve().parent.parent


def statistics_sources(statistics: dict) -> list[dict]:
    references = [statistics["config"], statistics["target"]]
    if "plan" in statistics:
        references.append(statistics["plan"])
    references += [period["source"] for period in statistics["periods"]]
    return references


def bundle_sources(bundle: dict) -> list[dict]:
    return ([bundle["statistics"]] if bundle.get("statistics") else []) + bundle["sources"]


def make_bundle(statistics: dict, statistics_ref: dict | None = None,
                company_route_field: str | None = None, selection_ref: dict | None = None) -> dict:
    target = load_json(check_source(statistics["target"]))
    key = window_key(target)
    selected = None
    if selection_ref is not None:
        selected = select_dimensions(statistics, load_json(check_source(selection_ref)))
        require(company_route_field is None or company_route_field == selected["company_route_field"],
                "气泡图字段与维度选择结果不一致")
        company_route_field = selected["company_route_field"]
    if company_route_field is not None:
        definitions = [dimension["definition"] for period in statistics["periods"] if period["status"] == "available"
                       for dimension in period["dimensions"] if dimension["id"] == "field:" + company_route_field]
        require(bool(definitions) and all(item.get("data_format") == "enum" for item in definitions),
                "公司与技术方向气泡图需要实际存在的枚举分类字段")
    presentation = {"company_route_field": company_route_field} if company_route_field is not None else {}
    if selected is not None:
        presentation["dimension_selection"] = selected
    model = {"schema_version": STATISTICS_VERSION, "mode": statistics["mode"], "target": target,
             "periods": statistics["periods"], key: statistics[key], "checks": statistics["checks"], **presentation}
    encoded = json.dumps(model, ensure_ascii=False, separators=(",", ":"))
    encoded = encoded.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    markup = ('<div class="history-content intelligence-visuals"><div class="visual-scope"></div>'
              '<div class="visual-panels"></div><div class="visual-evidence"></div>'
              '<script type="application/json" class="intelligence-visual-data">' + encoded + '</script></div>')
    css = (ROOT / "assets/charts.css").read_text(encoding="utf-8")
    checks = {**statistics["checks"], "candidate_dimensions": sorted({dimension["id"] for period in statistics["periods"]
               if period["status"] == "available" for dimension in period["dimensions"]}),
              "browser_presentation_checked": False}
    return {"schema_version": STATISTICS_VERSION, "statistics": statistics_ref,
            "sources": statistics_sources(statistics) + ([selection_ref] if selection_ref is not None else []),
            "selection_source": selection_ref,
            "config": statistics["config"], "target": statistics["target"],
            "current_data": statistics.get("data"), "dimension_fields": statistics["dimension_fields"],
            **presentation,
            "model": model, "html": '<style>' + css + '</style>' + markup, "checks": checks}


def make_current_bundle(config_path: Path, data_path: Path, target_path: Path, requested: list[str] | None = None,
                        company_route_field: str | None = None, selection_ref: dict | None = None) -> dict:
    return make_bundle(current_statistics(config_path, data_path, target_path, requested or []),
                       company_route_field=company_route_field, selection_ref=selection_ref)


def load_charts(path: Path, config_ref: dict, target_ref: dict) -> dict:
    bundle = load_json(path)
    require(bundle.get("schema_version") == STATISTICS_VERSION, "统计展示文件版本无效，请从原始响应重新生成")
    require(bundle["config"] == config_ref and bundle["target"] == target_ref, "统计展示与报告的配置或目标来源不一致")
    if bundle.get("statistics"):
        statistics = validate_statistics(check_source(bundle["statistics"]))
    else:
        statistics = current_statistics(check_source(config_ref), check_source(bundle["current_data"]),
                                        check_source(target_ref), bundle["dimension_fields"])
    expected = make_bundle(statistics, bundle.get("statistics"), bundle.get("company_route_field"), bundle.get("selection_source"))
    require(bundle == expected, "统计展示与原始响应不一致")
    for reference in bundle_sources(bundle):
        check_source(reference)
    return bundle


def javascript() -> str:
    vendor = ROOT / "assets/vendor/echarts-5.6.0/dist/echarts.min.js"
    require(vendor.is_file(), "缺少内置 ECharts 资源")
    return vendor.read_text(encoding="utf-8") + "\n" + (ROOT / "assets/charts.js").read_text(encoding="utf-8")


def section_title(bundle: dict) -> str:
    available = [period for period in bundle["model"]["periods"] if period["status"] == "available"]
    if len(available) > 1:
        return "近期变化"
    if available:
        return "本期情报分布" if available[0]["target"]["period"] == bundle["model"]["target"]["period"] else "历史资料分布"
    return "资料概况"


def main() -> None:
    parser = argparse.ArgumentParser(description="为 Python 报告准备有来源的前端统计展示数据")
    parser.add_argument("--statistics", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--dimension-field", action="append", default=[])
    parser.add_argument("--company-route-field")
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.statistics:
        require(not any((args.config, args.data, args.target, args.dimension_field)), "历史统计与当期资料入口分别使用")
        value = make_bundle(validate_statistics(args.statistics), source_ref(args.statistics), args.company_route_field,
                            source_ref(args.selection) if args.selection else None)
    else:
        require(all((args.config, args.data, args.target)), "当期统计需要配置、资料和目标")
        value = make_current_bundle(args.config, args.data, args.target, args.dimension_field, args.company_route_field,
                                    source_ref(args.selection) if args.selection else None)
    distinct_output(args.output, [Path(reference["path"]) for reference in bundle_sources(value)])
    write_json(args.output, value)
    print(json.dumps({"charts": str(args.output.resolve()), **value["checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
