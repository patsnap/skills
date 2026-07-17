"""
run.py v31.1 - BD管线估值统一执行入口（MD + PPT + HTML 三输出）
"""
import argparse, json, os, sys, datetime, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from valuation_calculator import (
    PipelineInput, EpiInput, CompetitionInput,
    PricingInput, DealInput, calculate_valuation,
)

PIPELINE_DEFAULTS = {
    "drug_name": "unknown", "target": "unknown", "mechanism": "unknown",
    "drug_type": "small molecule", "clinical_stage": "preclinical",
    "indication": "unknown", "market": "GLOBAL",
    "purpose": "BD谈判", "developer": "unknown",
    "licensee": "", "product_type": "default",
    "deal_type": "license_out", "combo_therapy": False, "patent_count": -1,
}
EPI_DEFAULTS = {
    "total_population": 1000.0, "addressable_population": 500.0,
    "data_source": "行业先验", "confidence": "MEDIUM", "epi_result_count": 0,
}
COMPETITION_DEFAULTS = {
    "competitor_count": 5, "approved_count": 1, "phase3_count": 3,
    "penetration_base": 0.05, "penetration_rationale": "行业先验", "market_type": "competitive",
}
PRICING_DEFAULTS = {"annual_cost_usd": 50000.0, "pricing_basis": "行业先验", "comparable_drug": "N/A"}
DEAL_DEFAULTS = {
    "ps_base": 2.5, "ps_low": 1.5, "ps_high": 4.5,
    "deal_case_count": 3, "deal_rationale": "行业先验", "comp_deal_median_m": 0.0,
}

def build_input(cls, data, defaults):
    import dataclasses
    merged = {**defaults, **data}
    valid  = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in merged.items() if k in valid})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",      required=True)
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--no-ppt",     action="store_true", help="跳过PPT生成")
    parser.add_argument("--no-html",    action="store_true", help="跳过HTML生成")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw = json.load(f)

    out_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", args.output_dir)
    os.makedirs(out_dir, exist_ok=True)

    p_data    = raw.get("pipeline", raw)
    epi_data  = raw.get("epi", {})
    com_data  = raw.get("competition", {})
    pri_data  = raw.get("pricing", {})
    deal_data = raw.get("deal", {})

    pipeline    = build_input(PipelineInput,    p_data,    PIPELINE_DEFAULTS)
    epi         = build_input(EpiInput,         epi_data,  EPI_DEFAULTS)
    competition = build_input(CompetitionInput, com_data,  COMPETITION_DEFAULTS)
    pricing     = build_input(PricingInput,     pri_data,  PRICING_DEFAULTS)
    deal        = build_input(DealInput,        deal_data, DEAL_DEFAULTS)

    extra = {
        "comparable_deals":   raw.get("comparable_deals",   []),
        "competitor_detail":  raw.get("competitor_detail",  []),
        "patent_summary":     raw.get("patent_summary",     {}),
        "clinical_summary":   raw.get("clinical_summary",   {}),
        "bd_strategy":        raw.get("bd_strategy",        []),
        "value_propositions": raw.get("value_propositions", []),
        "risks":              raw.get("risks",              []),
        "licensee":           raw.get("licensee",           p_data.get("licensee","")),
        "region":             raw.get("region",             p_data.get("market","GLOBAL")),
    }

    result    = calculate_valuation(pipeline, epi, competition, pricing, deal, extra)
    drug_name = p_data.get("drug_name", "unknown")
    ts        = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── MD 报告 ──
    md_path = os.path.join(out_dir, f"bd_valuation_{drug_name}_{ts}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(result["markdown_report"])
    print(f"[OK] MD报告: {md_path}")

    # ── HTML 报告（新增）──
    if not args.no_html:
        try:
            from valuation_html import generate_html
            html_path = os.path.join(out_dir, f"bd_valuation_{drug_name}_{ts}.html")
            generate_html(result, html_path)
            print(f"[OK] HTML报告: {html_path}")
        except Exception as e:
            print(f"[WARN] HTML生成失败: {e}")

    # ── PPT 报告 ──
    if not args.no_ppt:
        try:
            from valuation_ppt import generate_ppt
            scenarios  = result["scenarios"]
            base_s     = next((s for s in scenarios if s["scenario"]=="基准"), scenarios[1])
            cons_s     = next((s for s in scenarios if s["scenario"]=="保守"), scenarios[0])
            opti_s     = next((s for s in scenarios if s["scenario"]=="乐观"), scenarios[2])
            comp_deals = raw.get("comparable_deals", [])
            top_deals  = []
            for i, d in enumerate(comp_deals[:5]):
                top_deals.append({
                    "name":    d.get("name","")[:25],
                    "year":    d.get("year",""),
                    "value":   f"${d.get('total_m',0)/1000:.2f}B" if d.get("total_m") else "未披露",
                    "ps":      f"{d.get('ps_implied','—')}",
                    "is_base": i == 0,
                })
            import re as _re
            rl = 8; rh = 12
            m = _re.search(r"Royalty区间.*?(\d+)%–(\d+)%", result["markdown_report"])
            if m:
                rl, rh = int(m.group(1)), int(m.group(2))

            ppt_data = {
                "drug_name":       drug_name,
                "disease":         p_data.get("indication","适应症"),
                "stage":           p_data.get("clinical_stage",""),
                "mechanism":       p_data.get("mechanism",""),
                "sponsor":         p_data.get("developer",""),
                "today":           datetime.date.today().isoformat(),
                "deal_count":      deal_data.get("deal_case_count", 0),
                "deals_by_year":   raw.get("deals_by_year",   []),
                "type_ps_data":    raw.get("type_ps_data",    []),
                "top_deals":       top_deals,
                "comp_ps_data":    raw.get("comp_ps_data",    []),
                "ps_low":          deal_data.get("ps_low",  1.5),
                "ps_base":         deal_data.get("ps_base", 2.5),
                "ps_high":         deal_data.get("ps_high", 4.5),
                "ps_note":         deal_data.get("deal_rationale",""),
                "peak_sales_base": base_s["peak_sales_usd_b"],
                "peak_cons":       cons_s["peak_sales_usd_b"],
                "peak_opt":        opti_s["peak_sales_usd_b"],
                "pos":             base_s["pos"],
                "pos_cons":        cons_s["pos"],
                "pos_opt":         opti_s["pos"],
                "total_deal_base": base_s["deal_value_usd_b"],
                "total_cons":      cons_s["deal_value_usd_b"],
                "total_opt":       opti_s["deal_value_usd_b"],
                "upfront_lo":      base_s["upfront_low_usd_m"]/1000,
                "upfront_hi":      base_s["upfront_high_usd_m"]/1000,
                "milestone":       base_s["deal_value_usd_b"] * 0.82,
                "royalty_lo":      rl, "royalty_hi": rh,
                "value_props":     raw.get("value_propositions", []),
                "risks":           raw.get("risks",              []),
            }
            ppt_path = os.path.join(out_dir, f"bd_valuation_{drug_name}_{ts}.pptx")
            generate_ppt(ppt_data, ppt_path)
            print(f"[OK] PPT报告: {ppt_path}")
        except ImportError:
            print("[WARN] python-pptx未安装，跳过PPT生成。运行: pip install python-pptx")
        except Exception as e:
            print(f"[WARN] PPT生成失败: {e}")

    # ── 摘要 ──
    print("\n" + "="*60)
    print(f"  BD估值摘要 v31.1 - {drug_name}")
    print("="*60)
    for s in result["scenarios"]:
        print(f"  [{s['scenario']}] r-NPV:${s['rnpv_usd_b']:.3f}B  P/Peak:${s['ppeak_usd_b']:.3f}B  "
              f"总交易额:${s['deal_value_usd_b']:.3f}B  首付:${s['upfront_low_usd_m']:.0f}M–${s['upfront_high_usd_m']:.0f}M")
    print("="*60)

if __name__ == "__main__":
    main()
