"""
valuation_calculator.py  v31.0 — 三层合并版
================================================
合并来源：
  biopharma-asset-valuation              : 真实交易库(1394条) + MCP 9步SOP + 十章节报告
  biopharma-asset-valuation-to-be-improved: r-NPV x P/Peak x 可比三层加权 + 七因子调整(v30.4)
  pharma-bd-pipeline-valuation: PPT生成衔接接口

核心升级：
  1. 估值公式：单层(峰值*PS*PoS) → 三层加权(r-NPV 50% + P/Peak 30% + 可比 20%)
  2. 七因子调整矩阵：受让方溢价/靶点热度/PDL折扣/专利悬崖/溢价堆叠上限2.5x/区域折扣/竞争折扣
  3. 三层验证详细拆解写入报告第七章
  4. 七因子参数快照写入报告附录
"""

import json, datetime, os as _os, math
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any


# ═══════════════════════════════════════════════════════
# 七因子参数表 (server.py v30.4)
# ═══════════════════════════════════════════════════════

LICENSEE_MULT: Dict[str, float] = {
    "bms": 2.50, "bristol": 2.50, "gilead": 2.20,
    "abbvie": 2.00, "lilly": 2.00, "eli lilly": 2.00,
    "roche": 1.80, "novartis": 1.80, "pfizer": 1.80,
    "astrazeneca": 1.70, "az": 1.70,
    "merck": 1.60, "msd": 1.60,
    "johnson": 1.50, "jnj": 1.50, "sanofi": 1.50, "gsk": 1.50,
    "amgen": 1.40, "regeneron": 1.40, "biogen": 1.30,
    "biotech": 0.80,
}

TARGET_HOTSPOT: Dict[str, float] = {
    "glp-1": 1.40, "glp1": 1.40, "gcgr": 1.40,
    "kras": 1.35, "mat2a": 1.35,
    "bcma": 1.30,
    "pd-1": 1.25, "pd-l1": 1.25, "pdl1": 1.25,
    "cd19": 1.20, "cd20": 1.20, "trop2": 1.20, "cldn18": 1.20,
    "egfr": 1.15, "her2": 1.15, "erbb2": 1.15,
    "vegf": 1.10, "vegfr": 1.10, "il-4r": 1.15, "il4r": 1.15,
}

PRODUCT_TYPE_MULT: Dict[str, float] = {
    "fic": 1.40, "bic": 1.25, "me_better": 1.10,
    "me_too": 0.85, "platform": 1.30, "default": 1.00,
}

TERRITORY_WEIGHT: Dict[str, float] = {
    "US": 0.45, "EU": 0.25, "JP": 0.10,
    "CN": 0.15, "KR": 0.05, "GLOBAL": 1.00, "WW": 1.00,
}

INDICATION_KEYWORDS: Dict[str, List[str]] = {
    "oncology":   ["cancer","tumor","carcinoma","lymphoma","leukemia","melanoma","肿瘤","癌","淋巴瘤"],
    "autoimmune": ["arthritis","lupus","crohn","colitis","psoriasis","自身免疫","类风湿","银屑病"],
    "neurology":  ["alzheimer","parkinson","epilepsy","multiple sclerosis","神经","阿尔茨海默","帕金森"],
    "metabolic":  ["diabetes","obesity","nash","nafld","gout","糖尿病","肥胖","减重","代谢"],
    "infectious": ["hiv","hbv","hcv","rsv","influenza","covid","感染","病毒"],
    "rare":       ["rare","orphan","genetic","hemophilia","sma","duchenne","罕见","孤儿","遗传"],
}

PEAK_SALES_PRIOR: Dict[str, Dict[str, float]] = {
    "oncology":   {"low": 800,  "base": 2000, "high": 5000},
    "autoimmune": {"low": 600,  "base": 1500, "high": 4000},
    "neurology":  {"low": 400,  "base": 1200, "high": 3000},
    "metabolic":  {"low": 1000, "base": 3000, "high": 8000},
    "infectious": {"low": 300,  "base": 800,  "high": 2000},
    "rare":       {"low": 200,  "base": 600,  "high": 1500},
    "default":    {"low": 500,  "base": 1200, "high": 3000},
}

MARGIN_BY_TA: Dict[str, float] = {
    "oncology": 0.42, "autoimmune": 0.38, "neurology": 0.35,
    "metabolic": 0.22, "infectious": 0.30, "rare": 0.48, "default": 0.30,
}

DISCOUNT_RATE: Dict[str, float] = {
    "preclinical": 0.18, "phase_1": 0.16, "phase_1_2": 0.15, "phase_2": 0.14,
    "phase_2_3": 0.12, "phase_3": 0.11, "nda_bla": 0.10, "approved": 0.10,
}

YEARS_TO_MARKET_BASE: Dict[str, float] = {
    "preclinical": 9.0, "phase_1": 7.0, "phase_1_2": 6.0, "phase_2": 5.0,
    "phase_2_3": 3.5, "phase_3": 2.5, "nda_bla": 1.0, "approved": 0.0,
}

YEARS_EXTEND_BY_TA: Dict[str, float] = {
    "oncology": 0.0, "autoimmune": 0.5, "neurology": 1.0,
    "metabolic": 0.5, "infectious": 0.0, "rare": 1.0, "default": 0.0,
}

PPEAK_MULT: Dict[str, Dict[str, float]] = {
    "preclinical": {"low": 0.30, "base": 0.50, "high": 0.80},
    "phase_1":     {"low": 0.40, "base": 0.65, "high": 1.00},
    "phase_1_2":   {"low": 0.50, "base": 0.75, "high": 1.10},
    "phase_2":     {"low": 0.60, "base": 0.90, "high": 1.30},
    "phase_2_3":   {"low": 0.80, "base": 1.10, "high": 1.50},
    "phase_3":     {"low": 1.00, "base": 1.30, "high": 1.70},
    "nda_bla":     {"low": 1.50, "base": 2.00, "high": 2.50},
    "approved":    {"low": 2.00, "base": 2.80, "high": 3.50},
}

# ═══════════════════════════════════════════════════════
# 原有兼容参数表
# ═══════════════════════════════════════════════════════

POS_TABLE = {
    "preclinical": {"base": 0.10, "low": 0.08, "high": 0.12},
    "phase_1":     {"base": 0.12, "low": 0.10, "high": 0.15},
    "phase_1_2":   {"base": 0.20, "low": 0.15, "high": 0.25},
    "phase_2":     {"base": 0.30, "low": 0.25, "high": 0.35},
    "phase_2_3":   {"base": 0.45, "low": 0.35, "high": 0.55},
    "phase_3":     {"base": 0.68, "low": 0.60, "high": 0.75},
    "nda_bla":     {"base": 0.85, "low": 0.80, "high": 0.90},
    "approved":    {"base": 0.90, "low": 0.85, "high": 0.95},
}

UPFRONT_TABLE = {
    "preclinical": (0.03, 0.06), "phase_1":   (0.05, 0.08),
    "phase_1_2":   (0.05, 0.10), "phase_2":   (0.05, 0.10),
    "phase_2_3":   (0.08, 0.12), "phase_3":   (0.10, 0.15),
    "nda_bla":     (0.15, 0.20), "approved":  (0.20, 0.25),
}

MILESTONE_RATIO = {
    "preclinical": 0.88, "phase_1": 0.85, "phase_1_2": 0.83,
    "phase_2": 0.82, "phase_2_3": 0.80, "phase_3": 0.78,
    "nda_bla": 0.72, "approved": 0.65,
}

ROYALTY_TABLE = {
    "preclinical": (6, 10), "phase_1": (7, 11), "phase_1_2": (8, 12),
    "phase_2": (8, 12), "phase_2_3": (9, 13), "phase_3": (10, 14),
    "nda_bla": (12, 16), "approved": (15, 20),
}

STAGE_CN = {
    "preclinical": "临床前（Preclinical）", "phase_1": "Phase I",
    "phase_1_2": "Phase I/II", "phase_2": "Phase II",
    "phase_2_3": "Phase II/III", "phase_3": "Phase III",
    "nda_bla": "NDA/BLA申报", "approved": "已获批",
}

DEAL_TYPE_FACTOR = {
    "license_out": 1.00, "co_development": 1.00,
    "co_commercialization": 0.35, "collaboration": 0.20, "option": 0.15,
}

USD_TO_CNY = 7.2

# ═══════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════

def safe_build(cls, **kwargs):
    import dataclasses
    if dataclasses.is_dataclass(cls):
        valid = {f.name for f in dataclasses.fields(cls)}
        kwargs = {k: v for k, v in kwargs.items() if k in valid}
    return cls(**kwargs)


@dataclass
class PipelineInput:
    drug_name: str
    target: str
    mechanism: str
    drug_type: str
    clinical_stage: str
    indication: str
    market: str
    purpose: str
    developer: str
    licensee: str = ""
    product_type: str = "default"
    deal_type: str = "license_out"
    combo_therapy: bool = False
    patent_count: int = -1


@dataclass
class EpiInput:
    total_population: float        # 单位：万人（例：248 表示248万人）
    addressable_population: float  # 单位：万人
    data_source: str
    confidence: str
    epi_result_count: int = 0

    def __post_init__(self):
        """单位自动校验：若输入值 > 10000，判定为绝对人数，自动转换为万人并打印警告。"""
        import warnings
        if self.total_population > 10000:
            corrected = self.total_population / 10000
            warnings.warn(
                f"[EpiInput 单位警告] total_population={self.total_population:.0f} "
                f"疑似绝对人数（>10000），已自动转换为 {corrected:.2f} 万人。"
                "如需保留原值请手动确认单位。",
                UserWarning, stacklevel=2
            )
            self.total_population = corrected
        if self.addressable_population > 10000:
            corrected = self.addressable_population / 10000
            warnings.warn(
                f"[EpiInput 单位警告] addressable_population={self.addressable_population:.0f} "
                f"疑似绝对人数（>10000），已自动转换为 {corrected:.2f} 万人。"
                "如需保留原值请手动确认单位。",
                UserWarning, stacklevel=2
            )
            self.addressable_population = corrected


@dataclass
class CompetitionInput:
    competitor_count: int
    approved_count: int
    phase3_count: int
    penetration_base: float
    penetration_rationale: str
    market_type: str


@dataclass
class PricingInput:
    annual_cost_usd: float
    pricing_basis: str
    comparable_drug: str


@dataclass
class DealInput:
    ps_base: float
    ps_low: float
    ps_high: float
    deal_case_count: int
    deal_rationale: str
    comp_deal_median_m: float = 0.0


@dataclass
class ScenarioResult:
    scenario: str
    addressable_pop: float
    penetration: float
    annual_cost_usd: float
    peak_sales_usd_b: float
    ps_multiple: float
    pos: float
    rnpv_usd_b: float = 0.0
    ppeak_usd_b: float = 0.0
    comp_usd_b: float = 0.0
    deal_value_usd_b: float = 0.0
    upfront_low_usd_m: float = 0.0
    upfront_high_usd_m: float = 0.0
    deal_cny_b: float = 0.0
    stacking_mult: float = 1.0
    pdl_factor: float = 1.0
    cliff_discount: float = 1.0
    regional_factor: float = 1.0


# ═══════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════

def normalize_stage(s: str) -> str:
    s = s.lower().replace(" ", "_").replace("-", "_")
    for key in ["approved","nda_bla","nda","bla","phase_2_3","phase_1_2",
                "phase_3","phase3","phase_2","phase2","phase_1","phase1","preclinical"]:
        if key.replace("_","") in s.replace("_",""):
            m = {"nda":"nda_bla","bla":"nda_bla","phase3":"phase_3","phase2":"phase_2","phase1":"phase_1"}
            return m.get(key, key)
    return "phase_2"


def classify_indication(indication: str) -> str:
    txt = indication.lower()
    for ta, kws in INDICATION_KEYWORDS.items():
        if any(k in txt for k in kws):
            return ta
    return "default"


def calc_territory_factor(market: str) -> float:
    up = market.upper()
    if "GLOBAL" in up or "WW" in up:
        return 1.0
    total = sum(TERRITORY_WEIGHT.get(t.strip(), 0.0)
                for t in up.replace("+",",").split(","))
    return min(total, 1.0)


def calc_penetration_scenarios(base: float, market_type: str):
    if market_type == "niche":
        return base*0.7, base, min(base*1.4, 0.90)
    elif market_type == "competitive":
        return base*0.6, base*0.85, base*1.1
    return base*0.7, base, base*1.25


def calc_licensee_mult(licensee: str) -> float:
    lc = licensee.lower()
    return max((v for k,v in LICENSEE_MULT.items() if k in lc), default=1.0)


def calc_target_mult(target: str) -> float:
    lc = target.lower()
    return max((v for k,v in TARGET_HOTSPOT.items() if k in lc), default=1.0)


def calc_comp_discount(phase3_count: int) -> float:
    if phase3_count <= 2: return 1.00
    if phase3_count <= 5: return 0.85
    return 0.70


def calc_pdl_factor(market: str, ta: str) -> float:
    up = market.upper()
    has_cn_global = "CN" in up or "GLOBAL" in up or "WW" in up
    if has_cn_global and ta in ("oncology","autoimmune"): return 0.72
    if has_cn_global: return 0.88
    return 1.0


def calc_cliff_discount(patent_count: int):
    if patent_count < 0:  return 0.60, "知识产权风险未验证，按0.60x折扣（最差档）"
    if patent_count == 0: return 0.60, "无有效专利，按0.60x折扣（专利风险极高）"
    if patent_count <= 2: return 0.75, f"有效专利{patent_count}项，按0.75x折扣"
    return 1.00, ""


def calc_regional_factor(stage_key: str, terr_factor: float) -> float:
    if terr_factor >= 0.90: return 1.00
    if stage_key in ("approved","nda_bla"): return 0.15
    if stage_key == "phase_3":   return 0.20
    if stage_key == "phase_2_3": return 0.25
    return 1.00


# ═══════════════════════════════════════════════════════
# 本地真实交易库读取
# ═══════════════════════════════════════════════════════

def load_local_deals(target="", drug_type="", indication="", top_n=20):
    import re
    db_path = _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
        "references", "real_deals_1394.json"
    )
    if not _os.path.exists(db_path):
        return []
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    deals = db.get("deals", [])
    target_kws  = [t.strip().lower() for t in re.split(r"[/|,\s]+", target)    if t.strip()] if target    else []
    type_kws    = [t.strip().lower() for t in re.split(r"[/|,\s]+", drug_type) if t.strip()] if drug_type else []
    disease_kws = [t.strip().lower() for t in re.split(r"[/|,\s]+", indication)if t.strip()] if indication else []

    def score(r):
        s = 0
        txt_t = (r.get("靶点","")+" "+r.get("药物","")).lower()
        txt_y = r.get("药物类型","").lower()
        txt_d = (r.get("药物适应症","")+" "+r.get("交易适应症","")).lower()
        for k in target_kws:
            if k and k in txt_t: s += 3
        for k in type_kws:
            if k and k in txt_y: s += 2
        for k in disease_kws:
            if k and k in txt_d: s += 1
        if r.get("金额已披露"): s += 2
        if r.get("首付款_M"):   s += 1
        if r.get("总金额_M"):   s += 1
        return s

    scored = sorted([(score(r),r) for r in deals if score(r)>0], key=lambda x:-x[0])
    results = []
    for sc, r in scored[:top_n]:
        results.append({
            "name":     (r.get("交易名称","")[:60]+"..."),
            "upfront_m":r.get("首付款_M"),
            "total_m":  r.get("总金额_M"),
            "year":     r.get("交易时间","")[:4],
            "type":     r.get("交易类型",""),
            "note":     f"{r.get('受让方','')[:20]} | {r.get('药物类型','')}",
            "source":   "本地真实数据（高置信度）",
            "target":   r.get("靶点",""),
            "drug_type":r.get("药物类型",""),
            "region":   r.get("权益地区",""),
            "score":    sc,
        })
    return results


# ═══════════════════════════════════════════════════════
# 核心三层估值计算
# ═══════════════════════════════════════════════════════

def calculate_valuation(pipeline: PipelineInput, epi: EpiInput,
                         competition: CompetitionInput, pricing: PricingInput,
                         deal: DealInput, extra: dict = None) -> dict:
    if extra is None:
        extra = {}

    stage_key    = normalize_stage(pipeline.clinical_stage)
    ta           = classify_indication(pipeline.indication)
    pos_row      = POS_TABLE.get(stage_key, POS_TABLE["phase_2"])
    upfront_row  = UPFRONT_TABLE.get(stage_key, UPFRONT_TABLE["phase_2"])
    milestone_r  = MILESTONE_RATIO.get(stage_key, 0.82)
    royalty_lo, royalty_hi = ROYALTY_TABLE.get(stage_key, (8, 12))

    # ── 七因子计算 ──
    terr_factor    = calc_territory_factor(pipeline.market)
    pt_mult        = PRODUCT_TYPE_MULT.get(pipeline.product_type, 1.0)
    # Phase 1/1-2 阶段 FIC 溢价收敛（v30.4 校准）
    if stage_key in ("phase_1","phase_1_2") and pipeline.product_type == "fic":
        pt_mult = 1.15
    lic_mult       = calc_licensee_mult(pipeline.licensee)
    tgt_mult       = calc_target_mult(pipeline.target)
    comp_discount  = calc_comp_discount(competition.phase3_count)
    pdl_factor     = calc_pdl_factor(pipeline.market, ta)
    cliff_discount, cliff_warning = calc_cliff_discount(pipeline.patent_count)
    regional_factor= calc_regional_factor(stage_key, terr_factor)
    deal_type_factor = DEAL_TYPE_FACTOR.get(pipeline.deal_type, 1.0)

    # 溢价堆叠上限 2.5x（v30.4）
    stacking_raw  = pt_mult * lic_mult * tgt_mult
    stacking_mult = min(stacking_raw, 2.5)
    stacking_compressed = stacking_raw > 2.5

    # epi_boost
    epi_count  = getattr(epi, "epi_result_count", 0)
    epi_boost  = min(1.0 + epi_count * 0.04, 1.5) if epi_count > 0 else 1.0

    # r, years, margin
    r       = DISCOUNT_RATE.get(stage_key, 0.14)
    years   = YEARS_TO_MARKET_BASE.get(stage_key, 5.0) + YEARS_EXTEND_BY_TA.get(ta, 0.0)
    if pipeline.combo_therapy: years += 1
    years   = max(years, 0)
    margin  = MARGIN_BY_TA.get(ta, 0.30)
    af      = (1 - (1+r)**-12) / r            # 年金因子（12年专利期）

    # P/Peak 倍数
    ppeak_mult = PPEAK_MULT.get(stage_key, PPEAK_MULT["phase_2"])

    # 可比交易中位数
    comp_deal_median_b = deal.comp_deal_median_m / 1000.0 if deal.comp_deal_median_m > 0 else 0.0

    # 渗透率三情景
    pen_low, pen_base, pen_high = calc_penetration_scenarios(
        competition.penetration_base, competition.market_type)

    params = [
        ("保守", epi.addressable_population*0.85, pen_low,  pricing.annual_cost_usd*0.85, "low"),
        ("基准", epi.addressable_population,       pen_base, pricing.annual_cost_usd,       "base"),
        ("乐观", epi.addressable_population*1.15,  pen_high, pricing.annual_cost_usd*1.15,  "high"),
    ]

    scenarios = []
    for scenario, pop, pen, cost, sc_key in params:
        # 用户输入 PS 倍数（保留作历史兼容，不再用于主公式）
        ps_map = {"low": deal.ps_low, "base": deal.ps_base, "high": deal.ps_high}
        pos    = pos_row[sc_key]

        # Peak Sales（MCP 直接计算版）
        peak_sales_b = (pop * 10000 * pen * cost) / 1e9

        # Peak Sales（先验版，用于 r-NPV 和 P/Peak 基底）
        prior_m      = PEAK_SALES_PRIOR.get(ta, PEAK_SALES_PRIOR["default"])[sc_key]
        peak_prior_b = (prior_m / 1000.0) * terr_factor * epi_boost * comp_discount * pdl_factor * regional_factor

        # 取 MCP 直接计算与先验的加权混合（MCP 数据优先权 70%，先验 30%）
        peak_eff_b   = peak_sales_b * 0.70 + peak_prior_b * 0.30

        # ── 层1：r-NPV ──
        rnpv_b = peak_eff_b * margin * af / ((1+r)**years) * stacking_mult * cliff_discount

        # ── 层2：P/Peak ──
        ppeak_b = peak_eff_b * ppeak_mult[sc_key] * stacking_mult * cliff_discount

        # ── 层3：可比交易 ──
        comp_scale = {"low": 0.6, "base": 1.0, "high": 1.6}[sc_key]
        if comp_deal_median_b > 0:
            comp_b = comp_deal_median_b * terr_factor * stacking_mult * comp_scale
            w_rnpv, w_ppeak, w_comp = 0.50, 0.30, 0.20
        else:
            comp_b = 0.0
            w_rnpv, w_ppeak, w_comp = 0.70, 0.30, 0.00

        # ── 三层加权合并 ──
        total_asset_b = rnpv_b*w_rnpv + ppeak_b*w_ppeak + comp_b*w_comp

        # deal_type 折扣
        deal_value_b  = total_asset_b * deal_type_factor

        upfront_low_m  = deal_value_b * upfront_row[0] * 1000
        upfront_high_m = deal_value_b * upfront_row[1] * 1000
        deal_cny_b     = deal_value_b * USD_TO_CNY

        scenarios.append(safe_build(ScenarioResult,
            scenario=scenario,
            addressable_pop=round(pop,1),
            penetration=round(pen,4),
            annual_cost_usd=round(cost,0),
            peak_sales_usd_b=round(peak_eff_b,3),
            ps_multiple=round(ps_map[sc_key],1),
            pos=round(pos,2),
            rnpv_usd_b=round(rnpv_b,3),
            ppeak_usd_b=round(ppeak_b,3),
            comp_usd_b=round(comp_b,3),
            deal_value_usd_b=round(deal_value_b,3),
            upfront_low_usd_m=round(upfront_low_m,1),
            upfront_high_usd_m=round(upfront_high_m,1),
            deal_cny_b=round(deal_cny_b,2),
            stacking_mult=round(stacking_mult,3),
            pdl_factor=round(pdl_factor,2),
            cliff_discount=round(cliff_discount,2),
            regional_factor=round(regional_factor,2),
        ))

    # 七因子快照（供报告附录使用）
    factor_snapshot = {
        "ta":               ta,
        "terr_factor":      round(terr_factor,2),
        "pt_mult":          round(pt_mult,2),
        "lic_mult":         round(lic_mult,2),
        "tgt_mult":         round(tgt_mult,2),
        "stacking_raw":     round(stacking_raw,3),
        "stacking_mult":    round(stacking_mult,3),
        "stacking_compressed": stacking_compressed,
        "comp_discount":    round(comp_discount,2),
        "pdl_factor":       round(pdl_factor,2),
        "cliff_discount":   round(cliff_discount,2),
        "cliff_warning":    cliff_warning,
        "regional_factor":  round(regional_factor,2),
        "deal_type_factor": round(deal_type_factor,2),
        "epi_boost":        round(epi_boost,2),
        "r":                round(r,3),
        "years":            round(years,1),
        "margin":           round(margin,2),
        "comp_deal_median_b": round(comp_deal_median_b,3),
        "w_rnpv":           0.50 if comp_deal_median_b>0 else 0.70,
        "w_ppeak":          0.30,
        "w_comp":           0.20 if comp_deal_median_b>0 else 0.00,
    }

    md = _build_markdown_report(
        pipeline, epi, competition, pricing, deal,
        scenarios, stage_key, ta, pos_row, upfront_row,
        milestone_r, royalty_lo, royalty_hi, factor_snapshot, extra
    )

    return {
        "pipeline":        asdict(pipeline),
        "epi":             asdict(epi),
        "competition":     asdict(competition),
        "pricing":         asdict(pricing),
        "deal":            asdict(deal),
        "stage_key":       stage_key,
        "ta":              ta,
        "pos_base":        pos_row["base"],
        "upfront_range":   upfront_row,
        "scenarios":       [asdict(s) for s in scenarios],
        "factor_snapshot": factor_snapshot,
        "markdown_report": md,
        "usd_to_cny":      USD_TO_CNY,
    }


# ═══════════════════════════════════════════════════════
# 十章节 Markdown 报告生成（含三层验证拆解）
# ═══════════════════════════════════════════════════════

def _build_markdown_report(pipeline, epi, competition, pricing, deal,
                            scenarios, stage_key, ta, pos_row, upfront_row,
                            milestone_r, royalty_lo, royalty_hi,
                            fs, extra) -> str:
    today    = datetime.date.today().isoformat()
    base_s   = next((s for s in scenarios if s.scenario=="基准"), scenarios[1])
    cons_s   = next((s for s in scenarios if s.scenario=="保守"), scenarios[0])
    opti_s   = next((s for s in scenarios if s.scenario=="乐观"), scenarios[2])
    stage_cn = STAGE_CN.get(stage_key, pipeline.clinical_stage)
    licensee = extra.get("licensee", pipeline.licensee or "待定")
    region   = extra.get("region",   pipeline.market)
    comparable_deals  = extra.get("comparable_deals",  [])
    competitor_detail = extra.get("competitor_detail", [])
    patent_summary    = extra.get("patent_summary",    {})
    clinical_summary  = extra.get("clinical_summary",  {})
    bd_strategy       = extra.get("bd_strategy",       [])
    value_props       = extra.get("value_propositions",[])
    risks             = extra.get("risks",             [])

    milestone_base = base_s.deal_value_usd_b * milestone_r * 1000
    milestone_cons = cons_s.deal_value_usd_b * milestone_r * 1000
    milestone_opti = opti_s.deal_value_usd_b * milestone_r * 1000

    L = []

    # ── 标题 ──
    L += [
        "# BD管线估值报告  (v31.0 三层验证版)", "",
        f"**资产名称：** {pipeline.drug_name}　　**适应症：** {pipeline.indication}　　**靶点：** {pipeline.target}",
        f"**阶段：** {stage_cn}　　**受让方：** {licensee}　　**权益地区：** {region}",
        f"**用途：** {pipeline.purpose}　　**生成日期：** {today}", "",
        "> **免责声明**：本报告基于智慧芽MCP数据库及行业先验规则自动生成。"
        "回测MdAPE ~66%（总额），2倍以内命中率约44%。仅供内部BD谈判量级参考，不得直接作为对外报价或投资决策依据。",
        "", "---", "",
    ]

    # ── 执行摘要 ──
    L += [
        "## 执行摘要（Executive Summary）", "",
        f"**三层加权估值（r-NPV × P/Peak × 可比交易）**：",
        f"基准情景总交易额 **${base_s.deal_value_usd_b:.3f}B（约人民币{base_s.deal_cny_b:.2f}亿元）**，"
        f"建议首付款 **${base_s.upfront_low_usd_m:.0f}M–${base_s.upfront_high_usd_m:.0f}M**，"
        f"里程碑合计约 **${milestone_base:.0f}M**，Royalty **{royalty_lo}%–{royalty_hi}%**。", "",
        "| 情景 | r-NPV | P/Peak | 可比 | **总交易额** | 首付款区间 | 里程碑 |",
        "|------|-------|--------|------|------------|-----------|--------|",
        f"| 保守 | ${cons_s.rnpv_usd_b:.3f}B | ${cons_s.ppeak_usd_b:.3f}B | ${cons_s.comp_usd_b:.3f}B | **${cons_s.deal_value_usd_b:.3f}B** | ${cons_s.upfront_low_usd_m:.0f}M–${cons_s.upfront_high_usd_m:.0f}M | ~${milestone_cons:.0f}M |",
        f"| **基准** | **${base_s.rnpv_usd_b:.3f}B** | **${base_s.ppeak_usd_b:.3f}B** | **${base_s.comp_usd_b:.3f}B** | **${base_s.deal_value_usd_b:.3f}B** | **${base_s.upfront_low_usd_m:.0f}M–${base_s.upfront_high_usd_m:.0f}M** | **~${milestone_base:.0f}M** |",
        f"| 乐观 | ${opti_s.rnpv_usd_b:.3f}B | ${opti_s.ppeak_usd_b:.3f}B | ${opti_s.comp_usd_b:.3f}B | **${opti_s.deal_value_usd_b:.3f}B** | ${opti_s.upfront_low_usd_m:.0f}M–${opti_s.upfront_high_usd_m:.0f}M | ~${milestone_opti:.0f}M |",
        "", "---", "",
    ]

    # ── 第一章 资产概览 ──
    L += [
        "## 一、资产概览", "",
        "| 字段 | 内容 |", "|------|------|",
        f"| 药物名称 | **{pipeline.drug_name}** |",
        f"| 靶点 | {pipeline.target} |",
        f"| 作用机制 | {pipeline.mechanism} |",
        f"| 药物类型 | {pipeline.drug_type} |",
        f"| 临床阶段 | {stage_cn} |",
        f"| 适应症 | {pipeline.indication} |",
        f"| 治疗领域(TA) | {ta} |",
        f"| 开发方 | {pipeline.developer} |",
        f"| 目标市场/权益地区 | {region} |",
        f"| 潜在受让方 | {licensee} |",
        f"| 产品类型 | {pipeline.product_type} |",
        f"| 交易类型 | {pipeline.deal_type} |", "",
    ]
    if value_props:
        L.append("**资产亮点：**")
        L += [f"- {v}" for v in value_props]
    if patent_summary:
        L += [
            "", "**专利保护状况：**",
            f"- 有效专利数：{patent_summary.get('active_count','N/A')}",
            f"- 最早到期：{patent_summary.get('earliest_expiry','N/A')}",
            f"- 备注：{patent_summary.get('note','')}",
        ]
    L += ["", "---", ""]

    # ── 第二章 流行病学 ──
    L += [
        "## 二、流行病学与目标市场规模", "",
        "| 指标 | 数值 | 置信度 |", "|------|------|--------|",
        f"| 总目标人群 | **{epi.total_population:,.0f} 万人** | {epi.confidence} |",
        f"| 可治疗人群 | **{epi.addressable_population:,.0f} 万人** | {epi.confidence} |",
        f"| 数据来源 | {epi.data_source} | — |",
        f"| MCP流行病学命中条数 | {epi.epi_result_count} 条（epi_boost={fs['epi_boost']}） | — |", "",
        f"- 理论市场天花板：**${epi.addressable_population*10000*pricing.annual_cost_usd/1e9:.2f}B**",
        f"- 基准渗透下峰值销售：**${base_s.peak_sales_usd_b:.3f}B**",
        "", "---", "",
    ]

    # ── 第三章 竞争格局 ──
    L += [
        "## 三、竞争格局分析", "",
        "| 指标 | 数值 |", "|------|------|",
        f"| 竞品总数 | **{competition.competitor_count} 款** |",
        f"| 已获批竞品 | **{competition.approved_count} 款** |",
        f"| Phase III 竞品 | **{competition.phase3_count} 款** |",
        f"| 市场类型 | **{competition.market_type}** |",
        f"| 竞争折扣(comp_discount) | **{fs['comp_discount']}** |", "",
    ]
    if competitor_detail:
        L += ["| 药物名称 | 类型 | 阶段 | 开发方 |", "|---------|------|------|--------|"]
        for c in competitor_detail:
            L.append(f"| {c.get('name','—')} | {c.get('type','—')} | {c.get('stage','—')} | {c.get('developer','—')} |")
        L.append("")
    L += [
        f"> 渗透率（{competition.market_type}）：保守 {cons_s.penetration*100:.1f}% / 基准 {base_s.penetration*100:.1f}% / 乐观 {opti_s.penetration*100:.1f}%",
        f"> **BD视角**：{competition.penetration_rationale}",
        "", "---", "",
    ]

    # ── 第四章 定价 ──
    L += [
        "## 四、定价假设", "",
        "| 情景 | 年治疗费用(USD) |", "|------|----------------|",
        f"| 保守 | ${cons_s.annual_cost_usd:,.0f} |",
        f"| 基准 | ${base_s.annual_cost_usd:,.0f} |",
        f"| 乐观 | ${opti_s.annual_cost_usd:,.0f} |", "",
        f"定价依据：{pricing.pricing_basis}　　可比药：{pricing.comparable_drug}",
        "", "---", "",
    ]

    # ── 第五章 临床数据与PoS ──
    L += [
        "## 五、临床数据与PoS", "",
        "| 参数 | 保守 | 基准 | 乐观 |", "|------|------|------|------|",
        f"| 临床阶段 | {stage_cn} | {stage_cn} | {stage_cn} |",
        f"| PoS | {cons_s.pos*100:.0f}% | {base_s.pos*100:.0f}% | {opti_s.pos*100:.0f}% |", "",
    ]
    if clinical_summary:
        cs = clinical_summary
        L += [
            f"- 检索到临床结果：{cs.get('result_count','N/A')} 条",
            f"- 整体评估：{cs.get('general_evaluation','N/A')}",
        ]
        for kd in cs.get("key_data_points",[]):
            L.append(f"  - {kd}")
    L += ["", "---", ""]

    # ── 第六章 可比交易 ──
    L += [
        "## 六、可比交易分析", "",
        f"共参考 **{deal.deal_case_count}** 笔可比交易（本地真实数据库优先 + 智慧芽MCP补充）", "",
        "| 情景 | PS倍数（参考）|", "|------|-------------|",
        f"| 保守 | {deal.ps_low}x |",
        f"| 基准 | {deal.ps_base}x |",
        f"| 乐观 | {deal.ps_high}x |",
        f"| 可比交易中位数 | ${deal.comp_deal_median_m:.0f}M（{'有效，权重20%' if deal.comp_deal_median_m>0 else '无数据，权重归并至r-NPV'}）|", "",
        f"**赋值依据**：{deal.deal_rationale}", "",
    ]
    if comparable_deals:
        L += ["| 交易名称 | 首付款 | 总额 | 年份 | 来源 |",
              "|---------|--------|------|------|------|"]
        for d in comparable_deals:
            up  = f"${d.get('upfront_m',0):.0f}M" if d.get("upfront_m") else "未披露"
            tot = f"${d.get('total_m',0)/1000:.2f}B" if d.get("total_m") else "未披露"
            L.append(f"| {d.get('name','—')} | {up} | {tot} | {d.get('year','—')} | {d.get('source','—')} |")
    L += ["", "---", ""]

    # ── 第七章 三情景详细估值（含三层拆解）──
    L += [
        "## 七、三情景估值详细结果", "",
        "### 7.1 估值公式（v31.0 三层加权）", "",
        "```",
        "Peak Sales(B)  = 可治疗人群(万) × 10000 × 渗透率 × 年治疗费用 ÷ 1e9",
        "                 （MCP直接计算×70% + 先验峰值×30%，经竞争/PDL/区域折扣调整）",
        "r-NPV(B)       = Peak × margin × 年金因子(12yr) / (1+r)^years × stacking × cliff",
        "P/Peak(B)      = Peak × P/Peak倍数 × stacking × cliff",
        "可比(B)        = 可比交易中位数 × terr_factor × stacking × {0.6/1.0/1.6}",
        "总资产价值(B)  = r-NPV × W_rnpv + P/Peak × W_ppeak + 可比 × W_comp",
        f"               = r-NPV × {fs['w_rnpv']} + P/Peak × {fs['w_ppeak']} + 可比 × {fs['w_comp']}",
        "总交易额(B)    = 总资产价值 × deal_type_factor",
        "```", "",
        "### 7.2 三情景完整参数表", "",
        "| 参数 | 保守 | 基准 | 乐观 |", "|------|------|------|------|",
        f"| 可治疗人群(万) | {cons_s.addressable_pop} | {base_s.addressable_pop} | {opti_s.addressable_pop} |",
        f"| 渗透率 | {cons_s.penetration*100:.2f}% | {base_s.penetration*100:.2f}% | {opti_s.penetration*100:.2f}% |",
        f"| 年治疗费用(USD) | {cons_s.annual_cost_usd:,.0f} | {base_s.annual_cost_usd:,.0f} | {opti_s.annual_cost_usd:,.0f} |",
        f"| **峰值销售额(B USD)** | **{cons_s.peak_sales_usd_b:.3f}** | **{base_s.peak_sales_usd_b:.3f}** | **{opti_s.peak_sales_usd_b:.3f}** |",
        f"| PoS | {cons_s.pos*100:.0f}% | {base_s.pos*100:.0f}% | {opti_s.pos*100:.0f}% |",
        f"| **r-NPV(B)** | **{cons_s.rnpv_usd_b:.3f}** | **{base_s.rnpv_usd_b:.3f}** | **{opti_s.rnpv_usd_b:.3f}** |",
        f"| **P/Peak(B)** | **{cons_s.ppeak_usd_b:.3f}** | **{base_s.ppeak_usd_b:.3f}** | **{opti_s.ppeak_usd_b:.3f}** |",
        f"| **可比交易锚(B)** | **{cons_s.comp_usd_b:.3f}** | **{base_s.comp_usd_b:.3f}** | **{opti_s.comp_usd_b:.3f}** |",
        f"| **总交易额(B USD)** | **{cons_s.deal_value_usd_b:.3f}** | **{base_s.deal_value_usd_b:.3f}** | **{opti_s.deal_value_usd_b:.3f}** |",
        f"| **总交易额(B CNY)** | **{cons_s.deal_cny_b:.2f}** | **{base_s.deal_cny_b:.2f}** | **{opti_s.deal_cny_b:.2f}** |",
        f"| 首付款区间(M USD) | {cons_s.upfront_low_usd_m:.0f}–{cons_s.upfront_high_usd_m:.0f} | **{base_s.upfront_low_usd_m:.0f}–{base_s.upfront_high_usd_m:.0f}** | {opti_s.upfront_low_usd_m:.0f}–{opti_s.upfront_high_usd_m:.0f} |",
        f"| 里程碑合计(M USD) | ~{milestone_cons:.0f} | **~{milestone_base:.0f}** | ~{milestone_opti:.0f} |",
        f"| Royalty区间 | {royalty_lo}%–{royalty_hi}% | {royalty_lo}%–{royalty_hi}% | {royalty_lo}%–{royalty_hi}% |",
        "", "---", "",
    ]

    # ── 第八章 交易结构 ──
    L += [
        "## 八、交易结构设计建议（基准情景）", "",
        "| 组成 | 金额(M USD) | 占总额 | 触发条件 |", "|------|------------|--------|---------|",
        f"| 签约首付款 | **{base_s.upfront_low_usd_m:.0f}–{base_s.upfront_high_usd_m:.0f}** | {upfront_row[0]*100:.0f}%–{upfront_row[1]*100:.0f}% | 协议签署即付 |",
        f"| 里程碑款 | **~{milestone_base:.0f}** | ~{milestone_r*100:.0f}% | 见里程碑节点 |",
        f"| Royalty | {royalty_lo}%–{royalty_hi}%（分层） | — | 商业化后按净销售额 |", "",
        "**里程碑节点建议：** IND获批 / Phase II POC / Phase III启动 / Phase III主终点达成 / NDA受理 / 首次上市 / 销售$500M / 销售$1B",
        "", "---", "",
    ]

    # ── 第九章 BD谈判策略 ──
    L += [
        "## 九、BD谈判策略", "",
        f"| 项目 | 开价锚点 | 内部底线 |", "|------|---------|---------|",
        f"| 首付款 | **${base_s.upfront_high_usd_m*1.2:.0f}M** | **${base_s.upfront_low_usd_m*0.8:.0f}M** |",
        f"| 总交易额 | **${opti_s.deal_value_usd_b:.2f}B** | **${cons_s.deal_value_usd_b:.2f}B** |",
        f"| Royalty | **{royalty_hi}%（分层）** | **{royalty_lo}%（保底）** |", "",
    ]
    if bd_strategy:
        for i, s in enumerate(bd_strategy, 1):
            L.append(f"{i}. {s}")
    else:
        L += [
            "1. 以最近同靶点/同类型交易作为开场报价锚点",
            "2. 强调差异化优势（product_type、靶点热度）",
            "3. 如受让方对首付款敏感，可提高里程碑比例换取更高总额",
            "4. 维持至少2-3家并行谈判，保持竞争压力",
            "5. 分批次开放临床数据包，核心数据保留至NDA签署前",
        ]
    L += ["", "---", ""]

    # ── 第十章 风险提示 ──
    L += ["## 十、风险提示", ""]
    default_risks = [
        "模型MdAPE ~66%（总额），2倍以内命中率~44%，结果为谈判量级参考，非精确报价",
        f"专利保护：{fs['cliff_warning'] or '有效专利≥3项，按1.0x计'}",
        "定价基于行业先验，非实际中标/上市价，建议补充目标市场WTP调研",
        "PoS基于行业标准参数表，未纳入该药物特异性临床风险",
    ]
    for r in (risks or default_risks):
        L.append(f"- {r}")
    if fs["stacking_compressed"]:
        L.append(f"- ⚠️ 原始溢价堆叠 {fs['stacking_raw']:.2f}x 被压缩到 2.5x（v30.4 校准上限）")
    if fs["regional_factor"] < 1.0:
        L.append(f"- ⚠️ 后期阶段+区域权益，按v30.2校准下调（regional_factor={fs['regional_factor']}）")
    L += ["", "---", ""]

    # ── 附录：七因子参数快照 ──
    L += [
        "## 附录：七因子调整参数快照（v31.0）", "",
        "| 因子 | 取值 | 说明 |", "|------|------|------|",
        f"| 治疗领域(TA) | {fs['ta']} | 适应症自动分类 |",
        f"| 地区权重(terr_factor) | {fs['terr_factor']} | 基于territory映射 |",
        f"| 产品类型乘数(pt_mult) | {fs['pt_mult']} | {pipeline.product_type} |",
        f"| 受让方溢价(lic_mult) | {fs['lic_mult']} | {licensee} |",
        f"| 靶点热度(tgt_mult) | {fs['tgt_mult']} | {pipeline.target} |",
        f"| 溢价堆叠(stacking_mult) | {fs['stacking_mult']} | 原始{fs['stacking_raw']:.3f}→上限2.5 |",
        f"| 竞争折扣(comp_discount) | {fs['comp_discount']} | Phase3竞品{competition.phase3_count}个 |",
        f"| PDL折扣(pdl_factor) | {fs['pdl_factor']} | 市场准入折扣 |",
        f"| 专利悬崖折扣(cliff_discount) | {fs['cliff_discount']} | 专利数={pipeline.patent_count} |",
        f"| 区域许可折扣(regional_factor) | {fs['regional_factor']} | {stage_key}+区域权益 |",
        f"| 交易类型折扣(deal_type_factor) | {fs['deal_type_factor']} | {pipeline.deal_type} |",
        f"| 流行病学加速(epi_boost) | {fs['epi_boost']} | MCP命中{getattr(epi,'epi_result_count',0)}条 |",
        f"| 折现率(r) | {fs['r']*100:.1f}% | {stage_key}阶段 |",
        f"| 上市年限(years) | {fs['years']} 年 | TA延伸{YEARS_EXTEND_BY_TA.get(fs['ta'],0)}年 |",
        f"| 毛利率(margin) | {fs['margin']*100:.0f}% | {fs['ta']} TA |",
        f"| 三层权重(r-NPV/P-Peak/可比) | {fs['w_rnpv']:.0%}/{fs['w_ppeak']:.0%}/{fs['w_comp']:.0%} | {'有可比数据' if fs['comp_deal_median_b']>0 else '无可比数据，权重重分'} |", "",
        "---", "",
        f"**检索元数据**：生成日期 {today} | 数据库：智慧芽MCP + 本地真实BD交易库(1394条) | 估值模型版本：v31.0",
    ]

    return "\n".join(L)
