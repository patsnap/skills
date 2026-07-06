# HTML Dashboard Specification

Generate a standalone HTML file for a company patent portfolio. The dashboard should look like a dark patent roadmap/timeline and support analyst exploration.

## Title and Scope

Use `{Company} 公司多维标签时间轴` as the title. Infer the company from normalized applicants; if multiple applicants appear, use the operating company and mention collaborators in the workbook.

## Default View

Default dimension: `客户可读技术方向`.

Do not use raw gene names as the first-view swimlanes. Put gene/disease/platform labels in hover cards as `专业细分`.

## Dimension Switches

Provide buttons for:

- 技术方向
- 作用机制
- RNA类型
- 化学修饰
- 递送/组织
- 产品化阶段

Provide filters for:

- 全部趋势 / 持续或近期加码 / 早期集中或孤立 / 高关注
- 标签 dropdown for the active dimension
- free-text search across publication number, title, mechanism, chemistry, delivery, and countries

## Timeline

Use earliest family publication year as the default timeline year. If missing, use current publication year.

Each lane is one active tag. Each card is a patent. Card intensity should reflect importance:

- 高: bright/saturated
- 中高: normal-bright
- 中: muted
- 低: dim

Add `技术缺口` or `机会点` markers directly into the timeline when the portfolio implies an actionable gap. These markers should be visually distinct from patent cards, preferably yellow or amber with a dashed border. They should be placed in the relevant swimlane at the next-step/future year, usually the current year or next visible year. They are not patent records; they are recommended patent-layout opportunities.

Each opportunity marker should have:

- title, e.g. `机会点：CNS递送参数补强`
- gap explanation
- recommended R&D/IPR action
- hover tooltip explaining how to convert the gap into a patent theme

Always consider opportunity markers for these common small RNA gaps:

| Dimension | Lane/tag | Opportunity marker |
|---|---|---|
| 递送/组织 | 中枢神经 / 鞘内给药 | CNS递送参数补强：CSF/脑区暴露、鞘内给药间隔、重复给药安全性。 |
| 递送/组织 | 眼科 / 玻璃体腔给药 | 眼科局部给药外延：玻璃体稳定性、炎症控制、视功能终点、重复给药。 |
| 递送/组织 | 肾脏 / 肾病 | 肾脏组织选择性：肾组织暴露、系统给药窗口、组织选择性修饰。 |
| 递送/组织 | 制剂 / 辅料 | 制剂稳定性与浓度窗口：浓度、缓冲液、渗透压、稳定性、临床给药便利性。 |
| 作用机制 | NMD抑制 / 逃逸 | NMD机制迁移：将 NMD escape 迁移到新的单倍剂量不足疾病。 |
| 作用机制 | 隐蔽外显子 / 毒性外显子调控 | 隐蔽/毒性外显子新靶点：寻找未覆盖疾病、异常剪接事件或患者亚型。 |
| 作用机制 | 剪接转换 / 外显子纳入 | 剪接转换适应症拓展：新外显子事件、新用途、新序列族。 |
| 产品化阶段 | 患者分层 / 诊断赋能 | 患者筛选壁垒：基因型、biomarker、入排标准、疗效预测。 |

## Visual Style (v3 — 实心彩色卡片)

> **This section encodes the final visual style agreed in the Stoke Therapeutics session (stoke_dashboard_v3). Always apply these rules when generating HTML output.**

### Color System

Use a dark GitHub-style palette as the base:

```css
:root {
  --bg:      #0d1117;
  --bg2:     #161b22;
  --bg3:     #1c2230;
  --bg4:     #21283a;
  --border:  #30363d;
  --border2: #3d4a5c;
  --text:    #e6edf3;   /* primary text — always white */
  --text2:   #e6edf3;   /* secondary text — white (NOT grey) */
  --text3:   #c8d1da;   /* tertiary text — light grey, not dark grey */
  --accent:  #58a6ff;
  --accent2: #388bfd;
  --green:   #3fb950;
  --yellow:  #d29922;
  --amber:   #f0883e;
  --red:     #f85149;
  --purple:  #bc8cff;
  --cyan:    #76e3ea;
  --pink:    #ff7ab2;
  --teal:    #39d353;
}
```

**Rule: All `--text2` and `--text3` values must be white or near-white. Never use `#8b949e` or `#6e7681` (dark grey) as text colors — they are illegible on dark backgrounds.**

### Patent Card Style

Cards must be **solid (opaque) color blocks**, NOT semi-transparent. Follow these rules:

1. **Card background color = lane color** (the same color used in the left-side lane bar).
2. **Importance → opacity**, not hue. Use `hexToRgba(laneColor, alpha)` where alpha by importance tier:
   - `imp=3` (高): alpha = `0.92` — very bright, near-solid
   - `imp=2` (中高): alpha = `0.72`
   - `imp=1` (中): alpha = `0.52`
   - `imp=0` (低): alpha = `0.28` — dim but same hue
3. Cards for the **same lane always share the same hue**, making the lane color the visual anchor.
4. Each card has a **3 px top highlight bar** in the lane color at full opacity.
5. Card border = lane color at `0.6` opacity.
6. Card shadow: `0 2px 8px rgba(0,0,0,.45)` at rest, `0 10px 28px rgba(0,0,0,.65)` on hover.
7. Hover effect: `translateY(-3px) scale(1.03)` + `brightness(1.12)`.

Implement the helper function:

```js
function hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `rgba(${r},${g},${b},${alpha})`;
}
```

When rendering a card:

```js
const impAlpha = [0.28, 0.52, 0.72, 0.92][p.imp ?? 0];
const bg   = hexToRgba(lane.color, impAlpha);
const bdr  = hexToRgba(lane.color, 0.6);
const top  = lane.color; // full opacity top bar
card.style.cssText = `background:${bg}; border:1px solid ${bdr};`;
card.querySelector('::before') // set via inline style on a wrapper div
```

(In practice inject the top bar as a separate `<div class="pcard-top">` inside the card with `background: ${lane.color}; height:3px; ...`.)

### Card Text Colors

- Patent number (`.pcard-pn`): `font-size: 9px; font-weight: 700; color: #fff; opacity: .9;`
- Title (`.pcard-title`): `font-size: 10px; line-height: 1.3; color: #fff;`
- Tags / meta (`.pcard-tags`): `font-size: 9px; color: rgba(255,255,255,.75);`
- Importance dot: colored dot in top-right corner (`.imp-dot`) — kept for quick scanning.

### Lane Label Column

The left-side lane label has a **colored left border** using `lane.color`:

```css
.lane-name { border-left: 4px solid <lane.color>; }
```

The lane label text is white (`var(--text)`). Sub-label is `var(--text3)` (light grey).

### Lane Colors

Assign one distinct color per lane. Suggested palette (use in order, wrap if more lanes):

```
#58a6ff  #3fb950  #d29922  #bc8cff  #f0883e  #76e3ea
#ff7ab2  #39d353  #e3b341  #a371f7  #ffa657  #79c0ff
```

### Dimension Filter Buttons

```css
.dim-btn         { color: var(--text2); background: var(--bg3); border: 1px solid var(--border); }
.dim-btn:hover   { border-color: var(--accent); color: var(--accent); }
.dim-btn.active  { background: rgba(88,166,255,.15); border-color: var(--accent); color: var(--accent); font-weight: 600; }
```

### Header Legend

Add a small legend row in the header showing the 4 importance tiers as color chips with labels:

```
● 高关注  ● 中高  ● 中  ● 低关注
```

Use representative colors (blue hue at the four alpha levels) to illustrate the meaning.

### Opportunity Markers

```css
.opp-marker {
  border: 1.5px dashed var(--amber);
  background: rgba(240,136,62,.08);
  border-radius: 6px;
  padding: 5px 6px;
}
.opp-marker:hover { background: rgba(240,136,62,.16); }
.opp-title  { font-size: 9px; font-weight: 700; color: var(--amber); }
.opp-body   { font-size: 8px; color: var(--text3); line-height: 1.35; }
```

### Strategy Cards

```css
.strategy-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,.3);
}
```

Strategy card label colors: `gap` → `var(--amber)`, `inspire` → `var(--cyan)`, `copy` → `var(--purple)`.

Strategy card body text (`.sc-text`): `color: var(--text2)` — must be white/near-white.

### Sidebar

Sidebar label text: `var(--text2)` (white). Sidebar value text: `var(--text)` (white). Layout judgment badges:
- 强: green background
- 中: yellow background  
- 弱: red background

### Lane Row Alternating

Even rows: `background: rgba(255,255,255,.012)` — very subtle, just enough to help scanning.

## Hover Card

Include:

- current publication number and title
- customer-readable direction
- professional subdivision
- patent type classification
- current publication date and family earliest date
- mechanism tags
- chemistry/structure tags
- delivery/tissue tags
- productization stage
- family count
- family-entered countries
- importance and reason
- evidence chain: claim strength, family coverage strength, legal-status strength, design-around difficulty
- borrowable layout idea
- possible breakthrough point
- recommended action
- Chinese strategic interpretation

Do not use vague labels such as `护城河` in customer-facing hover cards unless the user explicitly requests it; prefer `保护信号`, `布局层级`, or `竞争关注点`.

## Top Strategy Cards

Above the timeline, add three compact strategy cards:

- `查漏补缺`: where the portfolio is weak and what to file next.
- `研发启发`: technical or application areas that can be explored.
- `布局借鉴`: industry-leader patent playbooks to copy.

These cards should be generated from the strategy layer, not manually written after the fact.

## Opportunity Cards

When the active dimension has opportunity markers, show a compact opportunity-card area above the timeline. This makes conclusions visible even before the user scrolls to the marker year.

Examples:

- `机会点：CNS递送参数补强`
- `机会点：NMD机制迁移`
- `机会点：隐蔽/毒性外显子新靶点`

## Right-Side Overview

The right panel should be `标签概览与分布解读`, not only a chart legend. For the active dimension:

1. Show an overall summary:
   - number of visible tags
   - total patent-tag assignments
   - top concentrated tags
   - tags recently increasing
   - tags early-concentrated, shrinking, or isolated
2. For each tag, show:
   - tag meaning in Chinese
   - mini year distribution chart
   - distribution share
   - main years where the tag appears
   - trend label
   - high-importance count
   - average family count
   - layout judgment: 强, 中, 弱
   - potential gap
   - recommended action

## Language

Use professional Chinese for UI labels and strategic interpretation. Keep gene symbols, protein names, and standard modification terms as-is when translation would reduce clarity.

Examples:

- `splice switching` -> `剪接转换`
- `intrathecal` -> `鞘内给药`
- `intravitreal` -> `玻璃体腔给药`
- `gapmer / wingmer` -> `gapmer / wingmer结构`
- `phosphorothioate backbone` -> `硫代磷酸酯骨架`

## Implementation Checklist

Before declaring the HTML file complete, verify:

- [ ] All `--text2` / `--text3` values are white or near-white (no dark grey).
- [ ] Card backgrounds are solid (opaque) colored blocks — not semi-transparent washes.
- [ ] Card color matches the lane color in the left column.
- [ ] `imp=3` cards are clearly brighter than `imp=0` cards within the same lane.
- [ ] Header legend shows 4 importance tiers.
- [ ] All dimension switch buttons render correctly and switch the swimlane grouping.
- [ ] At least one opportunity marker renders in the correct lane.
- [ ] Hover card shows all required fields.
- [ ] Strategy cards use correct label colors (amber / cyan / purple).
- [ ] Sidebar labels and values are white / near-white.
