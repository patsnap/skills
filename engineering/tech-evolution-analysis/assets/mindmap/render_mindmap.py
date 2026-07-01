"""Step 1 系统拆解思维导图渲染器 — 读 JSON 填 5 列网格.

基准范本：02_案例库/02_PLC/PLC技术趋势分析/PLC系统拆解思维导图.html
版式（麦肯锡风格 5 列：产品 / 大系统 / 子系统 / 组件 / 关键件）逐字锁在 CSS 里，
换案例只改数据 JSON，版式零漂移。

用法:
  python render_mindmap.py --data <案例>/mindmap_data.json --out <案例>/系统拆解思维导图.html

数据契约 (mindmap_data.json):
{
  "title": "PLC 产品系统拆解思维导图",
  "sub": "形态 E 全口径 · 4 大系统 + 1 横向系统 · 15 组件 · 15 关键件",
  "product": {"name": "PLC", "desc": "可编程逻辑控制器<br>(形态 E 全口径)"},
  "systems": [
    {"id": "S1", "name": "控制系统", "tag": "控制 · 逻辑大脑", "accent": "red"},
    {"id": "S5", "name": "横向系统", "tag": "韧性 · 安全/AI", "accent": "gold"}
  ],
  "subsystems": ["运算核", "存储", "..."],
  "components": [
    {"id": "C1.1", "name": "处理器单元"},
    {"id": "C1.2", "name": "程序与数据存储", "merge": true, "tag": "即关键件"}
  ],
  "parts": [
    {"id": "P1.1", "name": "主控 SoC", "tag": "MCU/MPU · 物理+生态", "star": true},
    {"id": "— C1.2 即关键件", "name": "非易失存储介质", "muted": true}
  ],
  "footnotes": [
    "<b>四独立性原则</b>: 物理学/矛盾/接口/生态 — 满足任一即纳入关键件层",
    "v1 · 2026-06-01 · 下一步 → Step 3"
  ]
}

字段说明:
  systems[].accent : "red"(默认左红边) | "gold"(横向系统左金边)
  components[].merge=true : 组件即关键件，斜体虚线样式(.merge)，可带 tag
  parts[].star=true : 关键件前加 ★；parts[].muted=true : 灰色「即关键件」引用行
  name/desc/tag/footnotes 支持内联 HTML(如 <br> ◐ ★)，按范本写法填。
"""
import argparse, json, os, sys, html

CSS = """
:root{
  --bg:#F5F1E8; --paper:#FAF7EE; --ink:#1A1A1A; --muted:#6B6B6B;
  --accent:#8B1A1A; --line:#C8B89A; --gold:#B8860B; --soft:#5B7A8C;
  --shadow:0 2px 8px rgba(60,40,20,.08);
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);font-family:"Noto Serif SC","SimSun",serif;color:var(--ink);padding:32px 40px;min-width:1280px}
.header{border-bottom:2px solid var(--accent);padding-bottom:16px;margin-bottom:28px}
.header h1{font-size:24px;font-weight:600;letter-spacing:.05em}
.header .sub{font-size:13px;color:var(--muted);margin-top:6px;font-family:"Noto Sans SC",sans-serif}
.legend{display:flex;gap:24px;margin-bottom:20px;font-family:"Noto Sans SC",sans-serif;font-size:12px;color:var(--muted)}
.legend span{display:inline-block;margin-right:6px}
.k-star{color:var(--gold);font-weight:bold}
.k-soft{color:var(--soft)}
.k-dash{border-bottom:1px dashed var(--muted);padding:0 4px}
.grid{display:grid;grid-template-columns:140px 200px 220px 240px 320px;gap:16px;align-items:start}
.col-title{font-family:"Noto Sans SC",sans-serif;font-size:11px;letter-spacing:.2em;color:var(--accent);font-weight:600;text-transform:uppercase;border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:10px}
.node{background:var(--paper);border:1px solid var(--line);border-radius:4px;padding:8px 10px;margin-bottom:8px;font-size:13px;box-shadow:var(--shadow);position:relative}
.node .id{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--accent);letter-spacing:.05em}
.node .name{font-weight:500;margin-top:2px}
.node .tag{font-family:"Noto Sans SC",sans-serif;font-size:10px;color:var(--muted);margin-top:3px}
.product{background:var(--accent);color:#FAF7EE;border:none;text-align:center;padding:24px 12px;font-size:15px;font-weight:600;letter-spacing:.1em}
.system{background:#fff;border-left:4px solid var(--accent)}
.system .id{color:var(--accent)}
.subsys{background:var(--paper)}
.component{background:var(--paper);border-color:var(--line)}
.part{background:#fff;border-left:3px solid var(--gold)}
.part .id{color:var(--gold)}
.merge{background:#fff;border-left:3px dashed var(--muted);font-style:italic}
.merge .id{color:var(--muted)}
.foot{margin-top:32px;padding-top:16px;border-top:1px solid var(--line);font-family:"Noto Sans SC",sans-serif;font-size:11px;color:var(--muted);line-height:1.7}
"""


def _node(cls, inner):
    return f'<div class="node {cls}">{inner}</div>'


def render(d):
    # Column 1: product
    p = d["product"]
    col_product = _node("product", f'{p["name"]}<br><span style="font-size:11px;font-weight:400;letter-spacing:.05em">{p.get("desc","")}</span>')

    # Column 2: systems (accent: red default / gold horizontal)
    sys_nodes = []
    for s in d.get("systems", []):
        gold = s.get("accent") == "gold"
        style = ' style="border-left-color:var(--gold)"' if gold else ''
        idstyle = ' style="color:var(--gold)"' if gold else ''
        sys_nodes.append(
            f'<div class="node system"{style}><div class="id"{idstyle}>{s["id"]}</div>'
            f'<div class="name">{s["name"]}</div><div class="tag">{s.get("tag","")}</div></div>')

    # Column 3: subsystems (plain labels)
    sub_nodes = [_node("subsys", s) for s in d.get("subsystems", [])]

    # Column 4: components (merge => 组件即关键件)
    comp_nodes = []
    for c in d.get("components", []):
        cls = "component merge" if c.get("merge") else "component"
        inner = f'<div class="id">{c["id"]}</div><div class="name">{c["name"]}</div>'
        if c.get("tag"):
            inner += f'<div class="tag">{c["tag"]}</div>'
        comp_nodes.append(_node(cls, inner))

    # Column 5: parts (star / muted reference rows)
    part_nodes = []
    for pt in d.get("parts", []):
        if pt.get("muted"):
            inner = (f'<div class="id">{pt["id"]}</div>'
                     f'<div class="name" style="color:var(--muted)">{pt["name"]}</div>')
            part_nodes.append(f'<div class="node part" style="border-left-color:var(--muted)">{inner}</div>')
        else:
            star = " ★" if pt.get("star") else ""
            inner = f'<div class="id">{pt["id"]}{star}</div><div class="name">{pt["name"]}</div>'
            if pt.get("tag"):
                inner += f'<div class="tag">{pt["tag"]}</div>'
            part_nodes.append(_node("part", inner))

    foot = "".join(f"<div>{f}</div>" for f in d.get("footnotes", []))

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{html.escape(d.get("title",""))} · McKinsey 风格</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
  <h1>{d.get("title","")}</h1>
  <div class="sub">{d.get("sub","")}</div>
</div>
<div class="legend">
  <div><span class="k-star">★</span> 关键件（金色边）</div>
  <div><span class="k-soft">◐</span> 软件/语义类</div>
  <div><span class="k-dash">虚线</span> 组件即关键件（不下钻）</div>
  <div>左红边 = 第一层大系统</div>
</div>
<div class="grid">
  <div class="col-title">产品</div>
  <div class="col-title">大系统</div>
  <div class="col-title">子系统</div>
  <div class="col-title">组件</div>
  <div class="col-title">关键件 · 分析锚点</div>
  <div>{col_product}</div>
  <div>{"".join(sys_nodes)}</div>
  <div>{"".join(sub_nodes)}</div>
  <div>{"".join(comp_nodes)}</div>
  <div>{"".join(part_nodes)}</div>
</div>
<div class="foot">{foot}</div>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(description="Step 1 系统拆解思维导图渲染器（读 JSON 填 5 列）")
    ap.add_argument("--data", required=True, help="path to mindmap_data.json")
    ap.add_argument("--out", required=True, help="output html path")
    args = ap.parse_args()
    d = json.load(open(args.data, encoding="utf-8"))
    open(args.out, "w", encoding="utf-8").write(render(d))
    print(f"systems:{len(d.get('systems',[]))} subsys:{len(d.get('subsystems',[]))} "
          f"comps:{len(d.get('components',[]))} parts:{len(d.get('parts',[]))}")
    print("-> " + args.out)


if __name__ == "__main__":
    main()
