"""Bridge between the DTree Explorer page and the library (package triordinal-dtree).

The page runs this module in the browser (Pyodide) with the published triordinal-dtree
package; the same code runs under CPython for the tests and to precompute the example
that is shown while the Python runtime loads. Everything the page displays about the
encoding (the order of the lists, the positions, the parents) comes from here.

Two encodings: "dtree" (DTree, two lists Q1 and Q2) and "euler" (EulerTree, one list: Q1
with its closing cells, the Euler tour). Two kinds of position: "rational" and "integer".
"""

import json
from fractions import Fraction

import triordinal.dtree as dtree
from triordinal.dtree import DTree
from triordinal.dtree.euler import EulerTree

LIMIT = 300  # insertions recorded step by step; larger trees show the final state only
KINDS = {"dtree": DTree, "euler": EulerTree}
POSITIONS = ("rational", "integer")


def _split(line):
    at = min((i for i in (line.find(":"), line.find(">"), line.find("<")) if i >= 0), default=-1)
    if at < 0:
        return None
    return line[at], line[:at].strip(), [c.strip() for c in line[at + 1:].split(";") if c.strip()]


def _position(t, cell):
    """A cell's position as the library stores it: an integer, or a fraction."""
    return str(cell.num) if t.positions == "integer" else str(Fraction(cell.num, cell.den))


def _state(t, kind):
    q1 = t.q1
    if kind == "dtree":
        pos = {v: [str(t.Q1.index(v)), str(t.Q2.index(v))] for v in q1}
        return {"q1": q1, "q2": t.q2, "pos": pos}
    # EulerTree: the whole list, with the closing cells; each node's block runs from its own cell
    # to its closing cell (to its own cell for a leaf). Read from the right, the block ends give
    # Q2: sorting the nodes by their block end, last first, is DTree's second list.
    cells, opens, ends = [], {}, {}
    c = t.get_node(t.root).c1
    while c.name != "]":                                  # up to SINK
        if c.name is None:                                # a closing cell: ")x" closes x's block
            cells.append([")" + c.node.name, _position(t, c)])
            ends[c.node.name] = len(cells) - 1
        else:
            cells.append([c.name, _position(t, c)])
            opens[c.name] = len(cells) - 1
        c = c.next
    end = {v: ends.get(v, opens[v]) for v in q1}
    q2 = sorted(q1, key=lambda v: -end[v])
    pos = {v: [cells[opens[v]][1], cells[end[v]][1]] for v in q1}
    return {"q1": q1, "q2": q2, "pos": pos, "cells": cells, "open": opens, "end": end}


def encode(text, limit=LIMIT, kind="dtree", positions="rational"):
    """Build a tree from the description and return the steps as JSON.

    Each step is one inserted node: the operation, its line, the new node and its parent,
    and (up to ``limit`` insertions) the full state after it: the lists and the positions.
    ``kind`` is "dtree" (two lists) or "euler" (one list), ``positions`` "rational" or "integer".
    """
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {sorted(KINDS)}, not {kind!r}")
    if positions not in POSITIONS:
        raise ValueError(f"positions must be one of {POSITIONS}, not {positions!r}")
    t = KINDS[kind]("E", positions=positions)
    steps, errors, parents = [], [], {}
    recording = True
    for no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip().lstrip("﻿")
        if not line or line.startswith(("#", "--", "**")):
            continue
        if line.startswith("@@"):
            break
        parts = _split(line)
        if parts is None:
            errors.append({"line": no, "text": line, "msg": "expected ':', '>' or '<'"})
            continue
        op, anchor, kids = parts
        for child in kids:
            try:
                if op == ":":
                    t.insert(anchor, child)
                    shown = f"{anchor}:{child}"
                elif op == ">":
                    t.insert_after(anchor, child)
                    shown = f"{anchor}>{child}"
                    anchor = child
                else:
                    t.insert_before(anchor, child)
                    shown = f"{anchor}<{child}"
            except (KeyError, ValueError, TypeError) as e:
                msg = e.args[0] if e.args else str(e)
                errors.append({"line": no, "text": line, "msg": f"{child}: {msg}"})
                continue
            parents[child] = t.get_parent(child)
            step = {"line": no, "op": shown, "new": child}
            if recording and len(steps) < limit:
                step.update(_state(t, kind))
            elif recording:
                recording = False
                for s in steps:
                    for k in ("q1", "q2", "pos", "cells", "open", "end"):
                        s.pop(k, None)
            steps.append(step)
    empty = {"q1": [], "q2": [], "pos": {}, "cells": [], "open": {}, "end": {}}
    final = _state(t, kind) if t.root is not None else empty
    lists = [t.Q1] if kind == "euler" else [t.Q1, t.Q2]
    return json.dumps({
        "version": dtree.__version__,
        "kind": kind,
        "positions": positions,
        "root": t.root,
        "parents": parents,
        "steps": steps,
        "final": final,
        "stepwise": recording,
        "limit": limit,
        "renumber": [q.renumber_count for q in lists],
        "errors": errors,
    })
