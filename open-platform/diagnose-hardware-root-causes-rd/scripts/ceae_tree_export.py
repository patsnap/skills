#!/usr/bin/env python3
"""Validate a causal-tree JSON file and export an English scientific PNG.

The accepted tree is nested under a top-level ``root`` object. Each node needs a
unique ``id``, a non-empty ``label`` and a supported ``type``. The visualization
retains the source convention that direct children of the root are neutral
``principle`` nodes, while allowing the actual physics chain to be represented
by nested relationships.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


NODE_STYLES = {
    "root": {"fill": "#B42318", "edge": "#7A271A", "label": "Measured problem"},
    "principle": {"fill": "#6941C6", "edge": "#53389E", "label": "Physical principle"},
    "mid": {"fill": "#175CD3", "edge": "#1849A9", "label": "Intermediate hypothesis"},
    "key": {"fill": "#067647", "edge": "#085D3A", "label": "Testable controllable hypothesis"},
    "dispute": {"fill": "#B54708", "edge": "#93370D", "label": "Disputed hypothesis"},
    "contradiction": {"fill": "#C01048", "edge": "#89123E", "label": "Parameter contradiction"},
    "end": {"fill": "#475467", "edge": "#344054", "label": "Verified boundary"},
}

ALLOWED_TYPES = frozenset(NODE_STYLES)
DPI = 170
MAX_FIGURE_INCHES = 70.0
NODE_HEIGHT = 1.35
LEVEL_GAP = 3.6
SIBLING_GAP = 0.8
WRAP_WIDTH = 27
MAX_NODES = 500
MAX_DEPTH = 40


class TreeValidationError(ValueError):
    """Raised when the causal-tree input violates the export contract."""


@dataclass(frozen=True)
class FlatNode:
    identifier: str
    label: str
    node_type: str
    parent: str | None
    depth: int
    edge_label: str
    evidence: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 causal-tree JSON")
    parser.add_argument("--output", required=True, type=Path, help="Output .png path")
    parser.add_argument("--title", default="Hardware Root-Cause Hypothesis Tree")
    parser.add_argument("--force", action="store_true", help="Replace an existing PNG")
    parser.add_argument("--dpi", type=int, default=DPI, help="PNG resolution (72–600)")
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise TreeValidationError(f"Input file does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TreeValidationError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise TreeValidationError("Top-level JSON value must be an object")
    return value


def clean_text(value: Any, field: str, identifier: str = "?") -> str:
    if not isinstance(value, str) or not value.strip():
        raise TreeValidationError(f"Node {identifier!r} needs a non-empty string {field!r}")
    cleaned = " ".join(value.replace("\x00", " ").split())
    if len(cleaned) > 600:
        raise TreeValidationError(f"Node {identifier!r} {field!r} exceeds 600 characters")
    return cleaned


def optional_text(value: Any, field: str, identifier: str) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value)
    if not isinstance(value, str):
        raise TreeValidationError(f"Node {identifier!r} {field!r} must be text or an array")
    return " ".join(value.replace("\x00", " ").split())


def validate_and_flatten(data: dict[str, Any]) -> list[FlatNode]:
    root = data.get("root")
    if not isinstance(root, dict):
        raise TreeValidationError("Top-level field 'root' must be an object")

    flattened: list[FlatNode] = []
    seen_objects: set[int] = set()
    identifiers: set[str] = set()

    def visit(node: dict[str, Any], parent: str | None, depth: int) -> None:
        if depth > MAX_DEPTH:
            raise TreeValidationError(f"Tree depth exceeds safe limit of {MAX_DEPTH}")
        object_id = id(node)
        if object_id in seen_objects:
            raise TreeValidationError("A node object is reused, creating a cycle")
        seen_objects.add(object_id)

        identifier = clean_text(node.get("id"), "id")
        if identifier in identifiers:
            raise TreeValidationError(f"Duplicate node id: {identifier}")
        identifiers.add(identifier)

        label = clean_text(node.get("label"), "label", identifier)
        node_type = node.get("type")
        if not isinstance(node_type, str) or node_type not in ALLOWED_TYPES:
            raise TreeValidationError(
                f"Node {identifier!r} has unsupported type {node_type!r}; "
                f"expected one of {sorted(ALLOWED_TYPES)}"
            )
        if parent is None and node_type != "root":
            raise TreeValidationError("The root object must have type='root'")
        if parent is not None and node_type == "root":
            raise TreeValidationError(f"Only the top node may use type='root' ({identifier})")

        edge_label = optional_text(node.get("edge_label"), "edge_label", identifier)
        evidence = optional_text(node.get("evidence_ids"), "evidence_ids", identifier)
        flattened.append(FlatNode(identifier, label, node_type, parent, depth, edge_label, evidence))
        if len(flattened) > MAX_NODES:
            raise TreeValidationError(
                f"Tree exceeds {MAX_NODES} nodes; split it into overview and branch figures"
            )

        children = node.get("children", [])
        if not isinstance(children, list):
            raise TreeValidationError(f"Node {identifier!r} children must be an array")
        for child in children:
            if not isinstance(child, dict):
                raise TreeValidationError(f"Node {identifier!r} contains a non-object child")
            visit(child, identifier, depth + 1)

    visit(root, None, 0)
    root_children = [node for node in flattened if node.parent == flattened[0].identifier]
    if not root_children:
        raise TreeValidationError("The root must have at least one child")
    invalid = [node.identifier for node in root_children if node.node_type != "principle"]
    if invalid:
        raise TreeValidationError(
            "Direct children of the root must be neutral type='principle' nodes; invalid: "
            + ", ".join(invalid)
        )
    return flattened


def import_plotting() -> tuple[Any, Any, Any, Any]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.patches as patches
        import matplotlib.pyplot as pyplot
        import networkx as networkx
    except ImportError as exc:
        raise TreeValidationError(
            "PNG export requires matplotlib and networkx in the execution environment"
        ) from exc
    return matplotlib, patches, pyplot, networkx


def select_font(matplotlib: Any) -> str:
    preferred = (
        "Arial",
        "Helvetica",
        "Noto Sans",
        "Liberation Sans",
        "DejaVu Sans",
    )
    available = {font.name for font in matplotlib.font_manager.fontManager.ttflist}
    return next((name for name in preferred if name in available), "DejaVu Sans")


def wrap_label(node: FlatNode) -> str:
    label = "\n".join(
        textwrap.wrap(node.label, width=WRAP_WIDTH, break_long_words=False, break_on_hyphens=False)
    )
    if node.evidence:
        label += f"\nEvidence: {node.evidence}"
    return label


def label_width(label: str) -> float:
    longest = max((len(line) for line in label.splitlines()), default=8)
    return max(4.5, min(12.0, longest * 0.23 + 1.5))


def build_graph(nodes: list[FlatNode], networkx: Any) -> Any:
    graph = networkx.DiGraph()
    for node in nodes:
        graph.add_node(
            node.identifier,
            label=wrap_label(node),
            node_type=node.node_type,
            depth=node.depth,
        )
        if node.parent is not None:
            graph.add_edge(node.parent, node.identifier, label=node.edge_label)
    if not networkx.is_directed_acyclic_graph(graph):
        raise TreeValidationError("Tree must be acyclic")
    if len(list(networkx.weakly_connected_components(graph))) != 1:
        raise TreeValidationError("Tree must be connected")
    return graph


def subtree_width(graph: Any, node: str, cache: dict[str, float]) -> float:
    if node in cache:
        return cache[node]
    own = label_width(graph.nodes[node]["label"])
    children = list(graph.successors(node))
    if not children:
        width = own
    else:
        child_total = sum(subtree_width(graph, child, cache) for child in children)
        width = max(own, child_total + SIBLING_GAP * (len(children) - 1))
    cache[node] = width
    return width


def layout_tree(graph: Any, root: str) -> dict[str, tuple[float, float]]:
    positions: dict[str, tuple[float, float]] = {}
    widths: dict[str, float] = {}
    subtree_width(graph, root, widths)

    def place(node: str, center: float, depth: int) -> None:
        positions[node] = (center, -depth * LEVEL_GAP)
        children = list(graph.successors(node))
        if not children:
            return
        total = sum(widths[child] for child in children) + SIBLING_GAP * (len(children) - 1)
        cursor = center - total / 2
        for child in children:
            width = widths[child]
            place(child, cursor + width / 2, depth + 1)
            cursor += width + SIBLING_GAP

    place(root, 0.0, 0)
    return positions


def add_legend(axis: Any, patches: Any, font: str) -> None:
    handles = [
        patches.Patch(
            facecolor=style["fill"],
            edgecolor=style["edge"],
            label=style["label"],
        )
        for style in NODE_STYLES.values()
    ]
    legend = axis.legend(
        handles=handles,
        title="Node classification",
        loc="lower right",
        frameon=True,
        framealpha=0.97,
        fontsize=8,
        title_fontsize=9,
    )
    for text in legend.get_texts():
        text.set_fontfamily(font)


def render(nodes: list[FlatNode], output: Path, title: str, dpi: int) -> None:
    matplotlib, patches, pyplot, networkx = import_plotting()
    font = select_font(matplotlib)
    graph = build_graph(nodes, networkx)
    root = nodes[0].identifier
    positions = layout_tree(graph, root)
    xs = [position[0] for position in positions.values()]
    ys = [position[1] for position in positions.values()]
    x_span = max(xs) - min(xs) if len(xs) > 1 else 10.0
    y_span = max(ys) - min(ys) if len(ys) > 1 else 4.0
    figure_width = min(MAX_FIGURE_INCHES, max(12.0, x_span + 4.0))
    figure_height = min(MAX_FIGURE_INCHES, max(8.0, y_span + 5.0))

    figure, axis = pyplot.subplots(figsize=(figure_width, figure_height))
    figure.patch.set_facecolor("#F8FAFC")
    axis.set_facecolor("#F8FAFC")
    axis.set_axis_off()

    for parent, child, metadata in graph.edges(data=True):
        x0, y0 = positions[parent]
        x1, y1 = positions[child]
        axis.annotate(
            "",
            xy=(x1, y1 + NODE_HEIGHT / 2),
            xytext=(x0, y0 - NODE_HEIGHT / 2),
            arrowprops={"arrowstyle": "-|>", "color": "#98A2B3", "lw": 1.2},
            zorder=1,
        )
        if metadata.get("label"):
            axis.text(
                (x0 + x1) / 2,
                (y0 + y1) / 2,
                metadata["label"],
                ha="center",
                va="center",
                fontsize=7,
                color="#475467",
                fontfamily=font,
                bbox={"facecolor": "#F8FAFC", "edgecolor": "none", "pad": 1.0},
                zorder=2,
            )

    for identifier, metadata in graph.nodes(data=True):
        x, y = positions[identifier]
        style = NODE_STYLES[metadata["node_type"]]
        axis.text(
            x,
            y,
            metadata["label"],
            ha="center",
            va="center",
            fontsize=8.5,
            color="white",
            fontfamily=font,
            fontweight="semibold",
            bbox={
                "boxstyle": "round,pad=0.55",
                "facecolor": style["fill"],
                "edgecolor": style["edge"],
                "linewidth": 1.3,
            },
            zorder=3,
        )

    margin_x = max(3.0, x_span * 0.08)
    axis.set_xlim(min(xs) - margin_x, max(xs) + margin_x)
    axis.set_ylim(min(ys) - 2.8, max(ys) + 2.0)
    axis.set_title(title, fontsize=16, fontweight="bold", color="#101828", fontfamily=font, pad=18)
    add_legend(axis, patches, font)
    figure.text(
        0.01,
        0.01,
        "Hypotheses require experimental validation; colors indicate classification, not probability.",
        fontsize=7.5,
        color="#475467",
        fontfamily=font,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, bbox_inches="tight", facecolor=figure.get_facecolor())
    pyplot.close(figure)


def validate_output(path: Path, force: bool, dpi: int) -> None:
    if path.suffix.lower() != ".png":
        raise TreeValidationError("Output path must use the .png suffix")
    if path.exists() and not force:
        raise TreeValidationError(f"Refusing to replace existing output without --force: {path}")
    if not 72 <= dpi <= 600:
        raise TreeValidationError("--dpi must be between 72 and 600")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_output(args.output, args.force, args.dpi)
        data = load_json(args.input)
        nodes = validate_and_flatten(data)
        render(nodes, args.output, args.title, args.dpi)
        print(f"Exported {len(nodes)} validated nodes to {args.output}")
        return 0
    except (OSError, TreeValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
