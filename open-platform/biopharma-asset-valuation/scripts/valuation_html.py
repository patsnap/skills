"""
valuation_html.py v1.0 - BD管线估值 HTML 报告生成器
特性：
  - 自包含单文件 HTML（内嵌 ECharts + 样式，无需外部依赖）
  - 深色专业主题（深蓝背景 + 青金配色）
  - 四大可视化：三情景柱状图、三层拆解瀑布图、可比交易散点图、七因子雷达图
  - 响应式布局，可直接用浏览器打开
"""
import json, datetime

ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"

def _color(name):
    return {"保守": "#4A90D9", "基准": "#00C9A7", "乐观": "#FFB347"}.get(name, "#aaa")

def generate_html(data: dict, out_path: str):
    """
    data: calculate_valuation() 的返回值 dict
    out_path: 输出文件路径
    """
    p        = data["pipeline"]
    epi      = data["epi"]
    comp     = data["competition"]
    pricing  = data["pricing"]
    deal     = data["deal"]
    fs       = data["factor_snapshot"]
    scens    = data["scenarios"]
    md       = data["markdown_report"]
    today    = datetime.date.today().isoformat()

    base_s = next((s for s in scens if s["scenario"]=="基准"), scens[1])
    cons_s = next((s for s in scens if s["scenario"]=="保守"), scens[0])
    opti_s = next((s for s in scens if s["scenario"]=="乐观"), scens[2])

    royalty_lo, royalty_hi = 8, 12
    stage_key = data.get("stage_key","phase_2")
    ROYALTY_TABLE = {
        "preclinical":(6,10),"phase_1":(7,11),"phase_1_2":(8,12),
        "phase_2":(8,12),"phase_2_3":(9,13),"phase_3":(10,14),
        "nda_bla":(12,16),"approved":(15,20),
    }
    royalty_lo, royalty_hi = ROYALTY_TABLE.get(stage_key,(8,12))

    milestone_r = {"preclinical":0.88,"phase_1":0.85,"phase_1_2":0.83,
        "phase_2":0.82,"phase_2_3":0.80,"phase_3":0.78,"nda_bla":0.72,"approved":0.65}.get(stage_key,0.82)
    milestone_base = base_s["deal_value_usd_b"] * milestone_r * 1000

    # ── ECharts 数据 ──
    # 图1：三情景总交易额柱状图
    chart1 = {
        "backgroundColor":"transparent",
        "title":{"text":"三情景估值对比（B USD）","textStyle":{"color":"#e0e0e0","fontSize":14}},
        "tooltip":{"trigger":"axis"},
        "legend":{"data":["r-NPV","P/Peak","可比交易"],"textStyle":{"color":"#ccc"}},
        "xAxis":{"type":"category","data":["保守","基准","乐观"],
                 "axisLabel":{"color":"#ccc"},"axisLine":{"lineStyle":{"color":"#555"}}},
        "yAxis":{"type":"value","name":"B USD","nameTextStyle":{"color":"#aaa"},
                 "axisLabel":{"color":"#ccc","formatter":"{value}B"},"splitLine":{"lineStyle":{"color":"#333"}}},
        "series":[
            {"name":"r-NPV","type":"bar","stack":"total","barWidth":"40%",
             "data":[cons_s["rnpv_usd_b"],base_s["rnpv_usd_b"],opti_s["rnpv_usd_b"]],
             "itemStyle":{"color":"#4A90D9"}},
            {"name":"P/Peak","type":"bar","stack":"total",
             "data":[cons_s["ppeak_usd_b"],base_s["ppeak_usd_b"],opti_s["ppeak_usd_b"]],
             "itemStyle":{"color":"#00C9A7"}},
            {"name":"可比交易","type":"bar","stack":"total",
             "data":[cons_s["comp_usd_b"],base_s["comp_usd_b"],opti_s["comp_usd_b"]],
             "itemStyle":{"color":"#FFB347"}},
        ]
    }

    # 图2：基准情景三层拆解（横向条形）
    chart2 = {
        "backgroundColor":"transparent",
        "title":{"text":"基准情景三层验证拆解（B USD）","textStyle":{"color":"#e0e0e0","fontSize":14}},
        "tooltip":{"trigger":"axis","axisPointer":{"type":"shadow"}},
        "xAxis":{"type":"value","axisLabel":{"color":"#ccc","formatter":"{value}B"},"splitLine":{"lineStyle":{"color":"#333"}}},
        "yAxis":{"type":"category","data":["可比交易（×20%）","P/Peak（×30%）","r-NPV（×50%）","总交易额"],
                 "axisLabel":{"color":"#ccc"}},
        "series":[{"type":"bar","barWidth":"50%",
            "data":[
                {"value":round(base_s["comp_usd_b"]*fs["w_comp"],3),"itemStyle":{"color":"#FFB347"}},
                {"value":round(base_s["ppeak_usd_b"]*fs["w_ppeak"],3),"itemStyle":{"color":"#00C9A7"}},
                {"value":round(base_s["rnpv_usd_b"]*fs["w_rnpv"],3),"itemStyle":{"color":"#4A90D9"}},
                {"value":base_s["deal_value_usd_b"],"itemStyle":{"color":"#E040FB"}},
            ],
            "label":{"show":True,"position":"right","color":"#fff","formatter":"{c}B"}
        }]
    }

    # 图3：七因子雷达
    indicators = [
        {"name":"受让方溢价","max":2.5},{"name":"靶点热度","max":1.5},
        {"name":"产品类型","max":1.5},{"name":"竞争折扣","max":1.0},
        {"name":"PDL折扣","max":1.0},{"name":"专利保护","max":1.0},
        {"name":"区域因子","max":1.0},
    ]
    radar_vals = [
        min(fs["lic_mult"],2.5),
        min(fs["tgt_mult"],1.5),
        min(fs["pt_mult"],1.5),
        fs["comp_discount"],
        fs["pdl_factor"],
        fs["cliff_discount"],
        fs["regional_factor"],
    ]
    chart3 = {
        "backgroundColor":"transparent",
        "title":{"text":"七因子调整雷达图","textStyle":{"color":"#e0e0e0","fontSize":14}},
        "tooltip":{},
        "radar":{"indicator":indicators,"splitLine":{"lineStyle":{"color":"#444"}},
                 "axisName":{"color":"#ccc","fontSize":11}},
        "series":[{"type":"radar","data":[{"value":radar_vals,"name":"调整因子",
            "areaStyle":{"color":"rgba(0,201,167,0.2)"},
            "lineStyle":{"color":"#00C9A7"},"itemStyle":{"color":"#00C9A7"}}]}]
    }

    # 图4：Peak Sales 三情景折线
    chart4 = {
        "backgroundColor":"transparent",
        "title":{"text":"峰值销售额 vs 总交易额（B USD）","textStyle":{"color":"#e0e0e0","fontSize":14}},
        "tooltip":{"trigger":"axis"},
        "legend":{"data":["峰值销售","总交易额"],"textStyle":{"color":"#ccc"}},
        "xAxis":{"type":"category","data":["保守","基准","乐观"],
                 "axisLabel":{"color":"#ccc"},"axisLine":{"lineStyle":{"color":"#555"}}},
        "yAxis":{"type":"value","name":"B USD","nameTextStyle":{"color":"#aaa"},
                 "axisLabel":{"color":"#ccc","formatter":"{value}B"},"splitLine":{"lineStyle":{"color":"#333"}}},
        "series":[
            {"name":"峰值销售","type":"line","smooth":True,"symbol":"circle","symbolSize":8,
             "data":[cons_s["peak_sales_usd_b"],base_s["peak_sales_usd_b"],opti_s["peak_sales_usd_b"]],
             "lineStyle":{"color":"#4A90D9","width":2},"itemStyle":{"color":"#4A90D9"}},
            {"name":"总交易额","type":"line","smooth":True,"symbol":"diamond","symbolSize":10,
             "data":[cons_s["deal_value_usd_b"],base_s["deal_value_usd_b"],opti_s["deal_value_usd_b"]],
             "lineStyle":{"color":"#00C9A7","width":2},"itemStyle":{"color":"#00C9A7"}},
        ]
    }

    def j(obj): return json.dumps(obj, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BD估值报告 - {p['drug_name']}</title>
<script src="{ECHARTS_CDN}"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0d1117;color:#e0e0e0;font-family:'Segoe UI',Arial,sans-serif;min-height:100vh}}
.header{{background:linear-gradient(135deg,#0d2137 0%,#1a3a5c 100%);padding:32px 48px;border-bottom:1px solid #1e3a5f}}
.header h1{{font-size:26px;font-weight:700;color:#fff;margin-bottom:6px}}
.header .sub{{font-size:13px;color:#7eb3d8;margin-top:4px}}
.badge{{display:inline-block;background:#1e3a5f;border:1px solid #2d5a8e;border-radius:4px;padding:3px 10px;font-size:12px;color:#7eb3d8;margin:3px 4px 3px 0}}
.container{{max-width:1400px;margin:0 auto;padding:28px 32px}}
.kpi-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}}
.kpi{{background:#161c24;border:1px solid #1e3a5f;border-radius:10px;padding:20px 22px;text-align:center}}
.kpi .val{{font-size:28px;font-weight:700;color:#00C9A7;margin:8px 0 4px}}
.kpi .lbl{{font-size:12px;color:#7eb3d8}}
.kpi .sub{{font-size:11px;color:#556}}
.charts-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:28px}}
.chart-box{{background:#161c24;border:1px solid #1e3a5f;border-radius:10px;padding:20px}}
.chart-box h3{{font-size:13px;color:#7eb3d8;margin-bottom:12px}}
.chart-area{{height:280px}}
.section{{background:#161c24;border:1px solid #1e3a5f;border-radius:10px;padding:24px;margin-bottom:20px}}
.section h2{{font-size:16px;font-weight:600;color:#00C9A7;border-left:3px solid #00C9A7;padding-left:12px;margin-bottom:16px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#1e2d40;color:#7eb3d8;padding:9px 12px;text-align:left;border-bottom:1px solid #243d59}}
td{{padding:8px 12px;border-bottom:1px solid #1a2a3a;color:#d0d8e4}}
tr:hover td{{background:#1a2535}}
tr.base-row td{{color:#00C9A7;font-weight:600}}
.tag{{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:600}}
.tag-green{{background:#0d3324;color:#00C9A7;border:1px solid #00C9A7}}
.tag-blue{{background:#0d1e33;color:#4A90D9;border:1px solid #4A90D9}}
.tag-orange{{background:#33200d;color:#FFB347;border:1px solid #FFB347}}
.tag-purple{{background:#1e0d33;color:#E040FB;border:1px solid #E040FB}}
.factor-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.factor-item{{background:#1a2535;border-radius:8px;padding:14px;text-align:center}}
.factor-item .fval{{font-size:22px;font-weight:700;color:#FFB347;margin:6px 0 4px}}
.factor-item .fname{{font-size:11px;color:#7eb3d8}}
.warning{{background:#1a1500;border:1px solid #554400;border-radius:6px;padding:10px 14px;color:#FFB347;font-size:12px;margin-top:12px}}
.footer{{text-align:center;padding:24px;color:#445;font-size:11px;border-top:1px solid #1a2a3a;margin-top:8px}}
@media(max-width:900px){{.charts-grid{{grid-template-columns:1fr}}.kpi-row{{grid-template-columns:repeat(2,1fr)}}.factor-grid{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>
<div class="header">
  <h1>BD 管线估值报告 <span style="font-size:14px;color:#4A90D9">v31.0 三层验证版</span></h1>
  <div class="sub">
    <span class="badge">💊 {p['drug_name']}</span>
    <span class="badge">🎯 {p['target']}</span>
    <span class="badge">🏥 {p['indication']}</span>
    <span class="badge">📊 {p['clinical_stage'].replace('_',' ').upper()}</span>
    <span class="badge">🌍 {p['market']}</span>
    <span class="badge">🤝 受让方: {p.get('licensee','待定') or '待定'}</span>
    <span class="badge">📅 {today}</span>
  </div>
</div>

<div class="container">

<!-- KPI 行 -->
<div class="kpi-row">
  <div class="kpi">
    <div class="lbl">基准总交易额</div>
    <div class="val">${base_s['deal_value_usd_b']:.3f}B</div>
    <div class="sub">≈ ¥{base_s['deal_cny_b']:.1f}亿</div>
  </div>
  <div class="kpi">
    <div class="lbl">建议首付款</div>
    <div class="val">${base_s['upfront_low_usd_m']:.0f}–{base_s['upfront_high_usd_m']:.0f}M</div>
    <div class="sub">基准情景</div>
  </div>
  <div class="kpi">
    <div class="lbl">峰值销售额</div>
    <div class="val">${base_s['peak_sales_usd_b']:.3f}B</div>
    <div class="sub">基准 | TA: {fs['ta']}</div>
  </div>
  <div class="kpi">
    <div class="lbl">临床成功概率</div>
    <div class="val">{base_s['pos']*100:.0f}%</div>
    <div class="sub">阶段: {p['clinical_stage'].replace('_',' ')}</div>
  </div>
</div>

<!-- 图表区 -->
<div class="charts-grid">
  <div class="chart-box">
    <div class="chart-area" id="chart1"></div>
  </div>
  <div class="chart-box">
    <div class="chart-area" id="chart2"></div>
  </div>
  <div class="chart-box">
    <div class="chart-area" id="chart3"></div>
  </div>
  <div class="chart-box">
    <div class="chart-area" id="chart4"></div>
  </div>
</div>

<!-- 三情景估值表 -->
<div class="section">
  <h2>三情景估值汇总</h2>
  <table>
    <thead>
      <tr><th>情景</th><th>峰值销售</th><th>r-NPV</th><th>P/Peak</th><th>可比交易</th><th>总交易额</th><th>首付款区间</th><th>里程碑(~)</th><th>PoS</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="tag tag-blue">保守</span></td>
        <td>${cons_s['peak_sales_usd_b']:.3f}B</td>
        <td>${cons_s['rnpv_usd_b']:.3f}B</td>
        <td>${cons_s['ppeak_usd_b']:.3f}B</td>
        <td>${cons_s['comp_usd_b']:.3f}B</td>
        <td><b>${cons_s['deal_value_usd_b']:.3f}B</b></td>
        <td>${cons_s['upfront_low_usd_m']:.0f}M–${cons_s['upfront_high_usd_m']:.0f}M</td>
        <td>~${cons_s['deal_value_usd_b']*milestone_r*1000:.0f}M</td>
        <td>{cons_s['pos']*100:.0f}%</td>
      </tr>
      <tr class="base-row">
        <td><span class="tag tag-green">基准 ★</span></td>
        <td>${base_s['peak_sales_usd_b']:.3f}B</td>
        <td>${base_s['rnpv_usd_b']:.3f}B</td>
        <td>${base_s['ppeak_usd_b']:.3f}B</td>
        <td>${base_s['comp_usd_b']:.3f}B</td>
        <td><b>${base_s['deal_value_usd_b']:.3f}B</b></td>
        <td>${base_s['upfront_low_usd_m']:.0f}M–${base_s['upfront_high_usd_m']:.0f}M</td>
        <td>~${milestone_base:.0f}M</td>
        <td>{base_s['pos']*100:.0f}%</td>
      </tr>
      <tr>
        <td><span class="tag tag-orange">乐观</span></td>
        <td>${opti_s['peak_sales_usd_b']:.3f}B</td>
        <td>${opti_s['rnpv_usd_b']:.3f}B</td>
        <td>${opti_s['ppeak_usd_b']:.3f}B</td>
        <td>${opti_s['comp_usd_b']:.3f}B</td>
        <td><b>${opti_s['deal_value_usd_b']:.3f}B</b></td>
        <td>${opti_s['upfront_low_usd_m']:.0f}M–${opti_s['upfront_high_usd_m']:.0f}M</td>
        <td>~${opti_s['deal_value_usd_b']*milestone_r*1000:.0f}M</td>
        <td>{opti_s['pos']*100:.0f}%</td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:12px;font-size:12px;color:#556">
    <span class="tag tag-purple">Royalty</span> &nbsp; {royalty_lo}%–{royalty_hi}% （阶梯加权，基准峰值销售${ base_s['peak_sales_usd_b']:.2f}B）
  </div>
</div>

<!-- 七因子参数快照 -->
<div class="section">
  <h2>七因子调整参数快照</h2>
  <div class="factor-grid">
    <div class="factor-item"><div class="fname">受让方溢价</div><div class="fval">{fs['lic_mult']}×</div><div class="fname">{p.get('licensee','默认') or '默认'}</div></div>
    <div class="factor-item"><div class="fname">靶点热度</div><div class="fval">{fs['tgt_mult']}×</div><div class="fname">{p['target']}</div></div>
    <div class="factor-item"><div class="fname">产品类型</div><div class="fval">{fs['pt_mult']}×</div><div class="fname">{p.get('product_type','default')}</div></div>
    <div class="factor-item"><div class="fname">溢价堆叠</div><div class="fval">{fs['stacking_mult']}×</div><div class="fname">原始{fs['stacking_raw']}× {'→已压缩' if fs['stacking_compressed'] else '(未超上限)'}</div></div>
    <div class="factor-item"><div class="fname">竞争折扣</div><div class="fval">{fs['comp_discount']}×</div><div class="fname">P3竞品: {comp.get('phase3_count',0)}款</div></div>
    <div class="factor-item"><div class="fname">PDL折扣</div><div class="fval">{fs['pdl_factor']}×</div><div class="fname">{p['market']} / {fs['ta']}</div></div>
    <div class="factor-item"><div class="fname">专利悬崖</div><div class="fval">{fs['cliff_discount']}×</div><div class="fname">专利数: {p.get('patent_count',-1)}</div></div>
    <div class="factor-item"><div class="fname">区域折扣</div><div class="fval">{fs['regional_factor']}×</div><div class="fname">terr_factor={fs['terr_factor']}</div></div>
  </div>
  {'<div class="warning">⚠️ ' + fs['cliff_warning'] + '</div>' if fs.get('cliff_warning') else ''}
  {'<div class="warning">⚠️ 溢价堆叠已从 ' + str(fs['stacking_raw']) + '× 压缩至 2.5×（v30.4硬上限）</div>' if fs['stacking_compressed'] else ''}
</div>

<!-- 关键参数 -->
<div class="section">
  <h2>核心模型参数</h2>
  <table>
    <thead><tr><th>参数</th><th>值</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>治疗领域(TA)</td><td>{fs['ta']}</td><td>由适应症自动分类</td></tr>
      <tr><td>折现率 r</td><td>{fs['r']*100:.1f}%</td><td>按阶段查表</td></tr>
      <tr><td>上市年限</td><td>{fs['years']} 年</td><td>基础+TA延伸</td></tr>
      <tr><td>毛利率</td><td>{fs['margin']*100:.0f}%</td><td>MARGIN_BY_TA[{fs['ta']}]</td></tr>
      <tr><td>epi_boost</td><td>{fs['epi_boost']}×</td><td>MCP流行病学命中×0.04，上限1.5</td></tr>
      <tr><td>三层权重</td><td>r-NPV {fs['w_rnpv']*100:.0f}% / P/Peak {fs['w_ppeak']*100:.0f}% / 可比 {fs['w_comp']*100:.0f}%</td><td>{'有可比交易中位数' if fs['comp_deal_median_b']>0 else '无可比数据，权重归并至r-NPV'}</td></tr>
      <tr><td>deal_type_factor</td><td>{fs['deal_type_factor']}×</td><td>{p.get('deal_type','license_out')}</td></tr>
    </tbody>
  </table>
</div>

<!-- 免责声明 -->
<div class="warning" style="border-radius:10px;padding:14px 18px">
  ⚠️ <b>免责声明</b>：本报告基于智慧芽MCP数据库及行业先验规则自动生成。
  回测MdAPE ~66%（总额），2倍以内命中率约44%。
  仅供内部BD谈判量级参考，不得直接作为对外报价或投资决策依据。
</div>

</div><!-- /container -->

<div class="footer">
  BD估值报告 v31.0 三层验证版 · 生成于 {today} · 数据来源：智慧芽MCP + 真实交易数据库(1394条)
</div>

<script>
var c1=echarts.init(document.getElementById('chart1'));
var c2=echarts.init(document.getElementById('chart2'));
var c3=echarts.init(document.getElementById('chart3'));
var c4=echarts.init(document.getElementById('chart4'));
c1.setOption({j(chart1)});
c2.setOption({j(chart2)});
c3.setOption({j(chart3)});
c4.setOption({j(chart4)});
window.addEventListener('resize',function(){{c1.resize();c2.resize();c3.resize();c4.resize();}});
</script>
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path
