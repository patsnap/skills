"""Shared TRIZ evolution-forest renderer (skeleton + tri-state).

CASE-AGNOSTIC CORE — reuse as-is across any product case.
Only the thin case driver (render_forest.py) carries case-specific data
(part-name dict, input/output paths). This module never needs editing.

Core principle (per user 2026-06-10):
  - Render the FULL authoritative node skeleton for every active route.
  - Color each node by data hits — NEVER auto-exclude a node as "historical".
  - 是否空白由数据 + 市场判断决定；任何位置(不分前后)的空白/稀疏都是布局机会。

States per node:
  已布局 (hits >= 2)  橙   — 有数据支撑的活跃节点
  稀疏   (hits == 1)  黄   — 数据薄弱，布局机会
  空白   (hits == 0)  蓝   — 无数据，布局机会(无论 tier 前后)

Routes are shown for a unit only if the unit has >=1 hit on that route
(an "active route"); within an active route the WHOLE skeleton is drawn so
middle/early gaps surface as 空白/稀疏 instead of vanishing.
"""
import html

# Authoritative 11-route dictionary (TRIZ进化路线AI标引-Prompt-v1.0.md) — full node names.
# This is the single source of truth; do NOT extend or renumber (see memory:
# triz-route-dictionary-authority).
DICT = {
 1:[("1.1","单系统"),("1.2","双系统"),("1.3","多系统")],
 2:[("2.1","少量组件"),("2.2","增加一个组件"),("2.3","增加多个组件"),("2.4","向超系统跃迁"),
    ("2.5","去除一个组件"),("2.6","去除多个组件"),("2.7","最大程度简化")],
 3:[("3.1","实心"),("3.2","单向单次分割"),("3.3","多向多次分割"),("3.4","粒状"),("3.5","膏状"),
    ("3.6","液状"),("3.7","泡沫状"),("3.8","气状"),("3.9","原子态"),("3.10","场"),("3.11","真空态")],
 4:[("4.1","光滑"),("4.2","凸起凹陷"),("4.3","轮廓精细化"),("4.4","引入场或力")],
 5:[("5.1","实心"),("5.2","引入空腔"),("5.3","几个空间"),("5.4","多个空间"),("5.5","引入场和力")],
 6:[("6.1","不可控"),("6.2","手动控制"),("6.3","机械控制"),("6.4","自动化")],
 7:[("7.1","参数不可变"),("7.2","梯度变化"),("7.3","均匀变化"),("7.4","间歇变化(自适应)")],
 8:[("8.1","刚性"),("8.2","单自由度"),("8.3","双自由度"),("8.4","多自由度"),("8.5","无极移动")],
 9:[("9.1","棱柱形"),("9.2","圆柱形"),("9.3","球形"),("9.4","复杂体")],
 10:[("10.1","平坦"),("10.2","单方向弯曲"),("10.3","多方向变形"),("10.4","复杂复合")],
 11:[("11.1","直线"),("11.2","单曲率"),("11.3","多曲率"),("11.4","复杂线性")],
}
ROUTE_NAME = {1:"单-双-多系统",2:"扩展裁剪",3:"分割向微观",4:"系统表面特性",5:"系统内部结构",
 6:"系统可控性提高",7:"频率匹配性提高",8:"系统动态化",9:"体组件几何",10:"表面几何",11:"线性组合几何"}

SPARSE_MAX = 1   # hits <= this (but >0) => 稀疏

def esc(s):
    return html.escape(str(s)) if s is not None else ""

def state_of(hits):
    if hits == 0: return "blank"
    if hits <= SPARSE_MAX: return "sparse"
    return "filled"


CSS = """
:root{--bg:#f4f6f9;--ink:#1f2733;--sub:#6b7686;
--filled:#f59e0b;--filled-bg:#fff8ec;--sparse:#eab308;--sparse-bg:#fefce8;
--blank:#2f6df6;--blank-bg:#eef3ff;--line:#c8cfda;--route-frame:#e23b3b;--root:#3b4a66;--green:#10b981;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI","Microsoft YaHei",Arial,sans-serif;font-size:14px}
header{padding:22px 28px 8px}
header h1{margin:0;font-size:22px}
header .meta{color:var(--sub);font-size:13px;margin-top:4px;max-width:1100px}
.legend{display:flex;gap:16px;flex-wrap:wrap;padding:10px 28px 18px;color:var(--sub);font-size:12.5px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.dot{width:14px;height:14px;border-radius:3px;display:inline-block}
.dot.o{background:var(--filled-bg);border:2px solid var(--filled)}
.dot.y{background:var(--sparse-bg);border:2px solid var(--sparse)}
.dot.b{background:var(--blank-bg);border:2px dashed var(--blank)}
.dot.r{border:2px solid var(--route-frame);background:transparent}
.unit{background:#fff;margin:14px 22px;border-radius:12px;box-shadow:0 1px 3px rgba(20,30,50,.08);overflow:hidden}
.unit-head{display:flex;align-items:center;gap:12px;padding:12px 18px;border-bottom:1px solid #eef1f5;background:#fbfcfe}
.unit-root{background:var(--root);color:#fff;padding:7px 14px;border-radius:8px;font-weight:600;font-size:15px;white-space:nowrap}
.unit-cur{color:var(--sub);font-size:12.5px}
.unit-body{padding:14px 18px 18px;overflow-x:auto}
.route-frame{border:2px solid var(--route-frame);border-radius:10px;padding:16px 14px 10px;margin:14px 0;position:relative}
.route-tag{position:absolute;top:-11px;left:14px;background:#fff;color:var(--route-frame);font-weight:600;font-size:12.5px;padding:0 8px}
.chain{display:flex;align-items:stretch;flex-wrap:nowrap;min-width:max-content}
.node{position:relative;min-width:120px;max-width:160px;border:2px solid var(--filled);background:var(--filled-bg);border-radius:9px;padding:8px 9px 7px;margin-right:30px}
.node:last-child{margin-right:0}
.node.sparse{border-color:var(--sparse);background:var(--sparse-bg)}
.node.blank{border-color:var(--blank);background:var(--blank-bg);border-style:dashed}
.node .pos{font-weight:700;font-size:11.5px;color:var(--filled)}
.node.sparse .pos{color:#a16207}
.node.blank .pos{color:var(--blank)}
.node .lab{font-size:11.5px;line-height:1.3;margin-top:2px}
.node .meta2{font-size:10px;color:var(--sub);margin-top:4px}
.node .arrow{position:absolute;right:-26px;top:50%;width:26px;height:2px;background:var(--line);transform:translateY(-50%)}
.node .arrow::after{content:"";position:absolute;right:0;top:-4px;border-left:7px solid var(--line);border-top:5px solid transparent;border-bottom:5px solid transparent}
.badge{position:absolute;top:-9px;right:-7px;font-size:9.5px;color:#fff;border-radius:10px;padding:1px 6px;font-weight:600;white-space:nowrap;background:var(--green)}
.pt-list{margin:8px 0 0;padding:8px 12px;background:#fbfcfe;border-radius:8px;font-size:12px;color:var(--sub);line-height:1.6}
.pt-list .tag{display:inline-block;font-size:10.5px;font-weight:600;padding:1px 7px;border-radius:9px;margin-right:6px;color:#fff}
.tag.f{background:var(--green)} .tag.b{background:var(--blank)} .tag.y{background:var(--sparse)}
"""

LEGEND = ('<div class="legend">'
  '<span><i class="dot r"></i>红框 = 一条进化路线(完整字典骨架)</span>'
  '<span><i class="dot o"></i>已布局(≥2件)</span>'
  '<span><i class="dot y"></i>稀疏(1件,布局机会)</span>'
  '<span><i class="dot b"></i>空白(0件,布局机会)</span>'
  '<span><i class="dot f"></i>派生母节点</span></div>')


def render_route_skeleton(route, node_hits, rep_info):
    """node_hits: {pos:count}; rep_info: {pos:{act,pn}}. Draws full dict chain."""
    skel = DICT[route]
    parts=[f'<div class="route-frame"><span class="route-tag">路线{route} · {esc(ROUTE_NAME[route])}</span><div class="chain">']
    for i,(pos,name) in enumerate(skel):
        hits=node_hits.get(pos,0)
        st=state_of(hits)
        arrow='' if i==len(skel)-1 else '<span class="arrow"></span>'
        info=rep_info.get(pos,{})
        if st=="filled":
            lab=esc(info.get("act") or info.get("core") or name)
            meta=f'{esc(info.get("pn",""))} · {hits}件'
        elif st=="sparse":
            lab=esc(info.get("act") or info.get("core") or name)
            meta=f'{esc(info.get("pn",""))} · 仅1件 ⚠'
        else:
            lab="无布局 · 机会点"
            meta="0件"
        parts.append(f'<div class="node {st}"><div class="pos">{esc(pos)} · {esc(name)}</div>'
                     f'<div class="lab">{lab}</div><div class="meta2">{meta}</div>{arrow}</div>')
    parts.append('</div></div>')
    return "".join(parts)
