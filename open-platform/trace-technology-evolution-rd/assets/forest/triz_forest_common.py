"""Shared, case-neutral renderer for the compact evolution-route skeleton.

The compact skeleton below is preserved from the source visualization asset and
is not identical to the longer analytical taxonomy in the Step 5 methodology.
It is a versioned display taxonomy, not a universal law or a legal conclusion.
"""

from __future__ import annotations

import html
from typing import Any


TAXONOMY_ID = "compact-display-routes-v1-localized"

ROUTES: dict[int, list[tuple[str, str]]] = {
    1: [("1.1", "Single system"), ("1.2", "Dual system"), ("1.3", "Multiple systems")],
    2: [
        ("2.1", "Few components"),
        ("2.2", "Add one component"),
        ("2.3", "Add multiple components"),
        ("2.4", "Transition to a supersystem"),
        ("2.5", "Remove one component"),
        ("2.6", "Remove multiple components"),
        ("2.7", "Maximum simplification"),
    ],
    3: [
        ("3.1", "Solid"),
        ("3.2", "Single-direction division"),
        ("3.3", "Multidirectional division"),
        ("3.4", "Granular"),
        ("3.5", "Paste-like"),
        ("3.6", "Liquid"),
        ("3.7", "Foam"),
        ("3.8", "Gas"),
        ("3.9", "Atomic scale"),
        ("3.10", "Field-mediated"),
        ("3.11", "Vacuum-mediated"),
    ],
    4: [("4.1", "Smooth"), ("4.2", "Raised or recessed"), ("4.3", "Refined profile"), ("4.4", "Introduced field or force")],
    5: [("5.1", "Solid"), ("5.2", "Introduced cavity"), ("5.3", "Several spaces"), ("5.4", "Multiple spaces"), ("5.5", "Introduced field or force")],
    6: [("6.1", "Uncontrolled"), ("6.2", "Manual control"), ("6.3", "Mechanized control"), ("6.4", "Automated control")],
    7: [("7.1", "Fixed parameter"), ("7.2", "Gradient change"), ("7.3", "Uniform change"), ("7.4", "Intermittent or adaptive change")],
    8: [("8.1", "Rigid"), ("8.2", "One degree of freedom"), ("8.3", "Two degrees of freedom"), ("8.4", "Multiple degrees of freedom"), ("8.5", "Continuous motion")],
    9: [("9.1", "Prismatic"), ("9.2", "Cylindrical"), ("9.3", "Spherical"), ("9.4", "Complex solid")],
    10: [("10.1", "Flat"), ("10.2", "One-direction curvature"), ("10.3", "Multidirectional deformation"), ("10.4", "Complex composite surface")],
    11: [("11.1", "Straight"), ("11.2", "Single curvature"), ("11.3", "Multiple curvature"), ("11.4", "Complex linear combination")],
}

ROUTE_NAMES = {
    1: "Single–dual–multiple systems",
    2: "Expansion and trimming",
    3: "Division toward smaller scales",
    4: "Surface characteristics",
    5: "Internal structure",
    6: "Controllability",
    7: "Parameter matching",
    8: "Dynamization",
    9: "Solid geometry",
    10: "Surface geometry",
    11: "Linear-combination geometry",
}


def escape(value: Any) -> str:
    return html.escape(str(value) if value is not None else "", quote=True)


def state_for(hit_count: int) -> str:
    if hit_count < 0:
        raise ValueError("hit_count must not be negative")
    if hit_count == 0:
        return "not-observed"
    if hit_count == 1:
        return "single-record"
    return "multiple-records"


CSS = """
:root {
  --canvas: #eef2f5;
  --paper: #ffffff;
  --ink: #16232d;
  --muted: #64717c;
  --line: #cbd5dc;
  --navy: #123247;
  --blue: #0b6b9a;
  --teal: #0f766e;
  --amber: #a16207;
  --soft-blue: #e5f3f9;
  --soft-teal: #e7f6f3;
  --soft-amber: #fff7dc;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--canvas); color: var(--ink); font: 14px/1.5 Inter, Arial, sans-serif; }
header { padding: 30px max(24px, calc((100vw - 1300px)/2)); background: var(--navy); color: #fff; border-bottom: 5px solid #38bdf8; }
header h1 { margin: 0; font: 700 2rem/1.15 Georgia, serif; }
header p { max-width: 1080px; margin: 8px 0 0; color: #d6e4eb; }
.legend { display: flex; flex-wrap: wrap; gap: 10px 20px; padding: 14px max(24px, calc((100vw - 1300px)/2)); background: #fff; border-bottom: 1px solid var(--line); }
.legend span { display: inline-flex; align-items: center; gap: 7px; color: var(--muted); font-size: .8rem; }
.swatch { width: 14px; height: 14px; border: 2px solid; display: inline-block; }
.swatch.multiple-records { border-color: var(--teal); background: var(--soft-teal); }
.swatch.single-record { border-color: var(--amber); background: var(--soft-amber); }
.swatch.not-observed { border-color: var(--blue); border-style: dashed; background: var(--soft-blue); }
main { max-width: 1300px; margin: auto; padding: 22px; }
.unit { margin: 0 0 22px; background: var(--paper); border: 1px solid var(--line); box-shadow: 0 6px 18px rgba(18, 50, 71, .08); }
.unit-header { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 20px; padding: 14px 18px; border-bottom: 1px solid var(--line); }
.unit-header h2 { margin: 0; font: 700 1.2rem Georgia, serif; }
.unit-header p { margin: 0; color: var(--muted); }
.unit-body { padding: 16px 18px; overflow-x: auto; }
.route { position: relative; margin: 14px 0 24px; padding: 22px 14px 14px; border: 2px solid var(--navy); }
.route-title { position: absolute; top: -12px; left: 12px; padding: 2px 8px; background: #fff; color: var(--navy); font-weight: 800; font-size: .78rem; }
.chain { display: flex; align-items: stretch; min-width: max-content; }
.node { position: relative; width: 155px; margin-right: 30px; padding: 10px; border: 2px solid; }
.node:last-child { margin-right: 0; }
.node.multiple-records { border-color: var(--teal); background: var(--soft-teal); }
.node.single-record { border-color: var(--amber); background: var(--soft-amber); }
.node.not-observed { border-color: var(--blue); border-style: dashed; background: var(--soft-blue); }
.node-id { margin: 0; font: 800 .72rem Consolas, monospace; }
.node-name { margin: 3px 0; font-weight: 750; }
.node-evidence { margin: 0; color: var(--muted); font-size: .72rem; }
.arrow { position: absolute; right: -27px; top: 50%; width: 25px; border-top: 2px solid var(--line); }
.arrow::after { content: ""; position: absolute; right: -1px; top: -5px; border-left: 7px solid var(--line); border-top: 4px solid transparent; border-bottom: 4px solid transparent; }
.annotations { margin: 9px 0 0; padding: 10px 12px; background: #f7fafc; border-left: 4px solid var(--blue); color: var(--muted); font-size: .8rem; }
.annotation { display: block; margin: 3px 0; }
@media (max-width: 700px) { main { padding: 12px; } .unit-body { padding: 12px; } }
@media print { body { background: #fff; font-size: 9pt; } header { background: #fff; color: var(--ink); padding: 16px 0; } header p { color: var(--muted); } main { max-width: none; padding: 0; } .unit { box-shadow: none; break-inside: avoid; } }
"""

LEGEND = (
    '<aside class="legend" aria-label="Evidence-state legend">'
    '<span><i class="swatch multiple-records"></i>Multiple accepted records</span>'
    '<span><i class="swatch single-record"></i>One accepted record; sparse evidence</span>'
    '<span><i class="swatch not-observed"></i>Not observed in the reviewed dataset</span>'
    '</aside>'
)


def render_route(
    route: int,
    node_hits: dict[str, int],
    representative: dict[str, dict[str, str]],
) -> str:
    if route not in ROUTES:
        raise ValueError(f"Unknown route: {route}")
    valid_nodes = {identifier for identifier, _ in ROUTES[route]}
    unknown = set(node_hits) - valid_nodes
    if unknown:
        raise ValueError(f"Route {route} contains unknown nodes: {', '.join(sorted(unknown))}")
    parts = [
        '<section class="route">',
        f'<h3 class="route-title">Route {route}: {escape(ROUTE_NAMES[route])}</h3>',
        '<div class="chain">',
    ]
    skeleton = ROUTES[route]
    for index, (position, name) in enumerate(skeleton):
        hits = node_hits.get(position, 0)
        state = state_for(hits)
        info = representative.get(position, {})
        action = info.get("action", "")
        record_id = info.get("record_id", "")
        arrow = "" if index == len(skeleton) - 1 else '<span class="arrow" aria-hidden="true"></span>'
        evidence = f"{hits} accepted record" + ("s" if hits != 1 else "")
        if record_id:
            evidence += f"; representative {record_id}"
        parts.extend(
            [
                f'<article class="node {state}">',
                f'<p class="node-id">{escape(position)}</p>',
                f'<p class="node-name">{escape(name)}</p>',
                f'<p class="node-evidence">{escape(action or evidence)}</p>',
                arrow,
                '</article>',
            ]
        )
    parts.extend(['</div>', '</section>'])
    return "".join(parts)
