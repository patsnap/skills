"""ceae_tree_export.py — 读取因果树JSON，生成PNG图片
支持：防重叠+大字体+争议节点橙色+右下角图例+第一性原理紫色层+参数矛盾终点
节点类型：root / principle / mid / key / dispute / end / contradiction

校验规则：根节点的直接子节点必须全部是 type=principle 的紫色节点，否则报错。
"""
import argparse, json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

COLOR = {
    'root':          '#ff4d4d',
    'principle':     '#722ed1',
    'mid':           '#1677ff',
    'key':           '#52c41a',
    'dispute':       '#fa8c16',
    'end':           '#8c8c8c',
    'contradiction': '#cf1322',
}
DPI = 150
MAX_FIG_INCHES = 80

FONT_NODE         = 14
FONT_TITLE        = 18
FONT_LEGEND       = 13
FONT_LEGEND_TITLE = 14
WRAP_CHARS        = 10
NODE_W_UNIT       = 2.2
NODE_H            = 1.8
VERT_GAP          = 4.5
H_PAD             = 1.4

LEGEND_ITEMS = [
    (COLOR['root'],          '根问题节点',   '分析起点，参数化后的目标问题'),
    (COLOR['principle'],     '第一性原理层', '前3层：物理本质/传递机制/控制方程，不含缺陷'),
    (COLOR['mid'],           '中间原因节点', '因果链中间层，可继续往下追问'),
    (COLOR['key'],           '关键缺陷节点', '参数可直接调节，改善后可实现目标'),
    (COLOR['dispute'],       '争议节点',     'TRIZ小组存在分歧，已投票确定比重'),
    (COLOR['contradiction'], '参数矛盾终点', '两参数相互制约，调一个会破坏另一个'),
    (COLOR['end'],           '边界终点',     '物理极限/项目范围/自然现象，停止追问'),
]

def _find_cjk_font():
    candidates = ['Hiragino Sans GB', 'PingFang SC', 'STHeiti', 'Microsoft YaHei',
                  'WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'SimHei']
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    for c in candidates:
        if c in available:
            return c
    return 'DejaVu Sans'

FONT = _find_cjk_font()

def _strip_emoji(text):
    result = []
    for ch in text:
        cp = ord(ch)
        if 0x4E00 <= cp <= 0x9FFF:   result.append(ch)
        elif 0x20 <= cp <= 0x7E:     result.append(ch)
        elif 0x3000 <= cp <= 0x303F: result.append(ch)
        elif ch == '\n':             result.append(ch)
    return ''.join(result)

def _validate_principle_first(root_node):
    """校验：根节点的直接子节点必须全部是 type=principle，否则报错终止。"""
    children = root_node.get('children', [])
    if not children:
        print('[ceae_tree_export] ERROR: 根节点没有子节点，因果图无法生成。', file=sys.stderr)
        sys.exit(1)
    non_principle = [c for c in children if c.get('type', 'mid') != 'principle']
    if non_principle:
        labels = [c.get('label', c.get('id', '?')) for c in non_principle]
        print('[ceae_tree_export] ERROR: 根节点的直接子节点必须全部是第一性原理层（type=principle）。', file=sys.stderr)
        print(f'[ceae_tree_export] 以下节点类型不是 principle：{labels}', file=sys.stderr)
        print('[ceae_tree_export] 请先在因果图中补充第一性原理三层紫色节点，再展开缺陷分析。', file=sys.stderr)
        sys.exit(2)
    print(f'[ceae_tree_export] 校验通过：根节点有 {len(children)} 个第一性原理子节点。')

def _parse(node, G, parent=None):
    nid = node['id']
    label = _strip_emoji(node['label'])
    G.add_node(nid, label=label, ntype=node.get('type', 'mid'))
    if parent:
        G.add_edge(parent, nid)
    for child in node.get('children', []):
        _parse(child, G, parent=nid)

def _wrap(text, max_chars=WRAP_CHARS):
    out, buf = [], ''
    for ch in text:
        if ch == '\n':
            if buf: out.append(buf); buf = ''
        else:
            buf += ch
            if len(buf) >= max_chars:
                out.append(buf); buf = ''
    if buf: out.append(buf)
    return '\n'.join(out) if out else text

def _node_width(label):
    lines = label.split('\n')
    max_len = max(len(ln) for ln in lines) if lines else 4
    return max(max_len * NODE_W_UNIT * 0.55, 4.0)

def _min_subtree_w(G, node, cache=None):
    if cache is None: cache = {}
    if node in cache: return cache[node]
    label = _wrap(G.nodes[node].get('label', node))
    self_w = _node_width(label)
    children = list(G.successors(node))
    if not children:
        w = self_w
    else:
        children_w = sum(_min_subtree_w(G, c, cache) for c in children)
        total_gap = H_PAD * (len(children) - 1)
        w = max(self_w, children_w + total_gap)
    cache[node] = w
    return w

def _place(G, node, x_center, depth, pos, w_cache=None):
    if w_cache is None: w_cache = {}
    pos[node] = (x_center, -depth * VERT_GAP)
    children = list(G.successors(node))
    if not children: return
    child_ws = [_min_subtree_w(G, c, w_cache) for c in children]
    total_gap = H_PAD * (len(children) - 1)
    total_w = sum(child_ws) + total_gap
    cur_x = x_center - total_w / 2
    for c, cw in zip(children, child_ws):
        _place(G, c, cur_x + cw / 2, depth + 1, pos, w_cache)
        cur_x += cw + H_PAD

def _draw_legend_box(ax):
    box_x = 0.995
    box_y = 0.005
    row_h = 0.038
    swatch_w = 0.018
    swatch_h = 0.026
    text_offset = 0.024
    col_gap = 0.16
    title = '节点颜色说明'
    n = len(LEGEND_ITEMS)
    total_h = row_h * (n + 1.2)
    total_w = 0.46

    bg = mpatches.FancyBboxPatch(
        (box_x - total_w, box_y), total_w, total_h,
        boxstyle='round,pad=0.01',
        facecolor='white', edgecolor='#cccccc',
        linewidth=1.5, alpha=0.93,
        transform=ax.transAxes, zorder=10
    )
    ax.add_patch(bg)

    ax.text(
        box_x - total_w / 2, box_y + total_h - row_h * 0.7, title,
        ha='center', va='center',
        fontsize=FONT_LEGEND_TITLE, fontfamily=FONT,
        fontweight='bold', color='#333333',
        transform=ax.transAxes, zorder=11
    )

    sep_y = box_y + total_h - row_h * 1.15
    ax.plot(
        [box_x - total_w + 0.01, box_x - 0.01], [sep_y, sep_y],
        color='#dddddd', lw=1.0, transform=ax.transAxes, zorder=11
    )

    for i, (color, name, desc) in enumerate(LEGEND_ITEMS):
        row_y = box_y + total_h - row_h * (i + 2.0)
        sx = box_x - total_w + 0.012

        swatch = mpatches.FancyBboxPatch(
            (sx, row_y - swatch_h / 2), swatch_w, swatch_h,
            boxstyle='round,pad=0.002',
            facecolor=color, edgecolor='white',
            linewidth=0.8, alpha=0.95,
            transform=ax.transAxes, zorder=12
        )
        ax.add_patch(swatch)

        ax.text(
            sx + text_offset, row_y, name,
            ha='left', va='center',
            fontsize=FONT_LEGEND, fontfamily=FONT,
            fontweight='bold', color='#222222',
            transform=ax.transAxes, zorder=12
        )
        ax.text(
            sx + text_offset + col_gap, row_y, desc,
            ha='left', va='center',
            fontsize=FONT_LEGEND - 1, fontfamily=FONT,
            color='#666666',
            transform=ax.transAxes, zorder=12
        )

def draw(tree_data, output_path):
    # ── 步骤1：校验第一性原理层必须存在 ──
    _validate_principle_first(tree_data['root'])

    G = nx.DiGraph()
    _parse(tree_data['root'], G)
    root_id = tree_data['root']['id']

    pos = {}
    w_cache = {}
    _place(G, root_id, 0, 0, pos, w_cache)

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    x_span = max(xs) - min(xs)
    y_span = abs(min(ys))

    fig_w = min(max(32, x_span + 14), MAX_FIG_INCHES)
    fig_h = min(max(18, y_span + 10), MAX_FIG_INCHES)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_axis_off()
    fig.patch.set_facecolor('#f8f9fa')

    margin_x = x_span * 0.1 + 6
    margin_y = y_span * 0.1 + 4
    ax.set_xlim(min(xs) - margin_x, max(xs) + margin_x)
    ax.set_ylim(min(ys) - margin_y, NODE_H + 2)

    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(arrowstyle='-|>', color='#bbbbbb', lw=1.2, mutation_scale=14))

    for node in G.nodes():
        x, y = pos[node]
        ntype = G.nodes[node].get('ntype', 'mid')
        color = COLOR.get(ntype, COLOR['mid'])
        raw_label = G.nodes[node].get('label', node)
        label = _wrap(raw_label)

        edge_lw = 1.2
        edge_color = 'white'
        if ntype == 'principle':
            edge_lw = 2.5
            edge_color = '#d3adf7'
        elif ntype == 'contradiction':
            edge_lw = 2.5
            edge_color = '#ffccc7'

        ax.text(x, y, label, ha='center', va='center',
                fontsize=FONT_NODE, fontfamily=FONT,
                color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.6', facecolor=color,
                          edgecolor=edge_color, linewidth=edge_lw, alpha=0.95),
                zorder=3)

    _draw_legend_box(ax)

    ax.set_title('根因因果树（含第一性原理层）',
                 fontfamily=FONT, fontsize=FONT_TITLE,
                 fontweight='bold', pad=12, color='#333333')

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'[ceae_tree_export] PNG saved -> {output_path}')
    w_px = int(fig_w * DPI)
    h_px = int(fig_h * DPI)
    print(f'[ceae_tree_export] Size: {w_px} x {h_px} px')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',  required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    draw(data, args.output)
