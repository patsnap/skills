# -*- coding: utf-8 -*-
"""Generate HTML report from final_records.json (single-pass)."""
import html, datetime
from collections import Counter
from hv_common import jload, load_query

def esc(x):
    return html.escape('' if x is None else str(x))

CSS = """
 body{font-family:"Microsoft YaHei",Arial,sans-serif;margin:0;background:#f5f6f8;color:#222;}
 .wrap{max-width:1600px;margin:0 auto;padding:28px;}
 h1{font-size:26px;border-left:6px solid #2f6fed;padding-left:12px;}
 h2{font-size:19px;margin-top:34px;border-bottom:2px solid #e2e6ee;padding-bottom:6px;}
 h3{font-size:15px;margin-top:18px;}
 .cards{display:flex;gap:16px;flex-wrap:wrap;margin:16px 0;}
 .card{background:#fff;border-radius:10px;padding:16px 20px;box-shadow:0 1px 4px rgba(0,0,0,.08);min-width:150px;}
 .card .n{font-size:26px;font-weight:700;color:#2f6fed;}
 .card .l{font-size:13px;color:#666;margin-top:4px;}
 table{border-collapse:collapse;width:100%;background:#fff;font-size:12.5px;}
 th,td{border:1px solid #dde2ea;padding:7px 9px;text-align:left;vertical-align:top;}
 th{background:#2f6fed;color:#fff;}
 .mini{max-width:520px;} .mini th{background:#42506b;}
 tr:nth-child(even) td{background:#f8fafc;}
 .q{background:#fff;border:1px solid #dde2ea;border-radius:8px;padding:12px 14px;font-family:Consolas,monospace;font-size:12px;white-space:pre-wrap;word-break:break-all;}
 .badge{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;color:#fff;}
 .b-yes{background:#2e9e5b;} .b-no{background:#9aa3b2;} .b-ev{background:#d9822b;}
 .draw img{max-width:110px;max-height:110px;border:1px solid #eee;}
 .reason{font-size:12px;color:#333;}
 .small{font-size:12px;color:#555;}
 .note{background:#fff8e6;border:1px solid #f0d98c;border-radius:8px;padding:10px 14px;font-size:13px;}
 td.t{min-width:160px;} td.ai{min-width:220px;font-size:11.5px;}
 a.pnlink{color:#2f6fed;font-weight:600;text-decoration:none;border-bottom:1px dotted #2f6fed;}
 a.pnlink:hover{color:#1748b5;border-bottom-style:solid;background:#eef3ff;}
"""

def section_head(m, sel, now):
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>高价值专利包筛选报告</title><style>{CSS}</style></head><body><div class="wrap">
<h1>高价值专利包筛选报告</h1>
<p class="small">生成时间：{now}　|　数据来源：PatSnap / 智慧芽 Connect API（实时检索，未人工编造）</p>
<h2>一、检索与筛选概览</h2>
<div class="cards">
 <div class="card"><div class="n">{m['candidate_count']}</div><div class="l">检索返回候选专利</div></div>
 <div class="card"><div class="n">{m['selected_count']}</div><div class="l">筛选高价值专利</div></div>
 <div class="card"><div class="n">{m['ratio']}%</div><div class="l">高价值占比</div></div>
 <div class="card"><div class="n">{sel[0]['score']}</div><div class="l">最高评分</div></div>
 <div class="card"><div class="n">{sel[-1]['score']}</div><div class="l">入选最低评分</div></div>
</div>
<p>本次检索返回 <b>{m['candidate_count']}</b> 件，筛选 <b>{m['selected_count']}</b> 件，占 <b>{m['ratio']}%</b>
（10% 下限 = {m['candidate_count']*10//100} 件，15% 上限 = {m['sel_max_15pct']} 件；按默认 10% 向上取整选取）。</p>
<h3>检索式</h3><div class="q">{esc(load_query())}</div>
"""

def section_method(m):
    t5 = ''.join(f"<tr><td>{i+1}</td><td>{esc(t['name'])}</td><td>{t['count']}</td></tr>"
                 for i, t in enumerate(m['top5_inventors']))
    return f"""
<h2>二、评分标准与方法</h2>
<table class="mini"><tr><th>指标</th><th>权重</th><th>数据来源 / 口径</th></tr>
<tr><td>简单同族被引专利数量多</td><td>30%</td><td>P015 cited_by_simple_family，候选集内百分位 ×30</td></tr>
<tr><td>简单同族专利数量多</td><td>30%</td><td>P014 len(simple_family)，候选集内百分位 ×30</td></tr>
<tr><td>属于核心发明人专利</td><td>20%</td><td>命中候选集发明人专利数 Top5 即得 20，否则 0</td></tr>
<tr><td>出现过专利法律事件</td><td>20%</td><td>P034 诉讼 / P027 无效复审 / P028 许可 / P029 权利转移，任一非空得 20</td></tr></table>
<h3>核心发明人（候选集专利数 Top5）</h3>
<table class="mini"><tr><th>排名</th><th>发明人</th><th>候选集专利数</th></tr>{t5}</table>
<div class="note" style="margin-top:12px">
<b>口径说明：</b>智慧芽发明人字段格式为「姓, 名|姓, 名」，逗号是单个发明人姓名内的姓/名分隔符，竖线「|」才是发明人之间的分隔符。
为避免把「TANNER, CHRISTOPHER RICHARD」拆成两个人，本次仅按「|、；、换行」切分发明人（与通用规则中“同时按逗号切分”有意偏离）。
中英文同族对同一发明人会以不同语言出现（如 TANNER 与 克里斯托弗·理查德·坦纳），跨语言不做归并，核心发明人基于检索返回候选集原样统计。
</div>
"""

THEAD = ("<tr><th>排名</th><th>评分</th><th>被选定为高价值的原因</th><th>公开公告号</th><th>标题</th>"
 "<th>摘要附图</th><th>[标]当前申请(专利权)人</th><th>简单法律状态</th><th>Patsnap专利标题</th>"
 "<th>AI技术问题</th><th>AI技术手段</th><th>AI技术功效</th><th>同族被引</th><th>同族数</th>"
 "<th>核心发明人</th><th>法律事件</th><th>数据缺口</th></tr>")

def draw_cell(d):
    if isinstance(d, str) and d.startswith('http'):
        return f'<div class="draw"><a href="{esc(d)}" target="_blank"><img src="{esc(d)}" loading="lazy"></a></div>'
    return esc(d)

def yesno(r):
    if r['core_inventor']:
        return f'<span class="badge b-yes">是</span> {esc("、".join(r["matched_inventors"]))}'
    return '<span class="badge b-no">否</span>'

def events_cell(r):
    ev = r['legal_events']
    if not ev:
        return '<span class="badge b-no">无</span>'
    return ' '.join(f'<span class="badge b-ev">{esc(k)}{("×"+str(v)) if v>1 else ""}</span>' for k, v in ev.items())

def pn_cell(r):
    url = r.get('view_url')
    if url:
        return (f"<td><a class='pnlink' href='{esc(url)}' target='_blank' "
                f"rel='noopener' title='在智慧芽中打开（需登录）'>{esc(r['pn'])}</a></td>")
    return f"<td>{esc(r['pn'])}</td>"

def row_html(r):
    gaps = '、'.join(r['gaps']) if r['gaps'] else '无'
    return ("<tr>"
        f"<td>{r['rank']}</td><td><b>{r['score']}</b></td>"
        f"<td class='reason'>{esc(r['rationale'])}</td>"
        f"{pn_cell(r)}<td class='t'>{esc(r['title'])}</td>"
        f"<td>{draw_cell(r['drawing'])}</td>"
        f"<td>{esc(r['current_assignee'])}</td><td>{esc(r['legal_status'])}</td>"
        f"<td class='t'>{esc(r['patsnap_title'])}</td>"
        f"<td class='ai'>{esc(r['tech_problem'])}</td><td class='ai'>{esc(r['tech_approach'])}</td>"
        f"<td class='ai'>{esc(r['benefit'])}</td>"
        f"<td>{r['cited_by_simple_family'] if not r['cited_missing'] else '未获取'}</td>"
        f"<td>{r['simple_family_count']}</td>"
        f"<td>{yesno(r)}</td><td>{events_cell(r)}</td><td class='small'>{esc(gaps)}</td>"
        "</tr>")

def section_table(sel):
    body = ''.join(row_html(r) for r in sel)
    return f"""
<h2>三、高价值专利清单（{len(sel)} 件）</h2>
<p class="small">提示：点击「公开公告号」可在智慧芽 PatSnap 数据库中打开该专利详情页（需登录智慧芽账号）。</p>
<div style="overflow-x:auto"><table>{THEAD}{body}</table></div>
"""

def section_gaps(sel):
    gc = Counter()
    for r in sel:
        for g in r['gaps']:
            gc[g] += 1
    li = ''.join(f"<li>{esc(k)}：{v} 件</li>" for k, v in gc.most_common()) or '<li>无</li>'
    return f"""
<h2>四、数据缺口与接口情况</h2>
<ul class="small">{li}</ul>
<p class="small">说明：缺失字段标记为「未获取」并保留在追溯数据 高价值专利包筛选数据.json 中；
法律事件仅作为价值信号，不构成专利稳定性或可执行性的法律结论。本次候选集法律事件以「权利转移」为主（304 件），许可 1 件，未检索到诉讼与无效/复审记录。</p>
</div></body></html>"""

if __name__ == '__main__':
    f = jload('final_records.json')
    m, sel = f['meta'], f['selected']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    htmlstr = (section_head(m, sel, now) + section_method(m)
               + section_table(sel) + section_gaps(sel))
    open('高价值专利包筛选报告.html', 'w', encoding='utf-8').write(htmlstr)
    print('HTML written, chars=', len(htmlstr))
