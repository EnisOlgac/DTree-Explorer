"""Bridge between the DTree Explorer page and the dtree package.

The page runs this module in the browser (Pyodide) with the published dtree-encoding
package; the same code runs under CPython for the tests and to precompute the example
that is shown while the Python runtime loads. Everything the page displays about the
encoding (the order of Q1 and Q2, the positions, the parents) comes from here.
"""

import json

import dtree
from dtree import DTree

LIMIT = 300  # insertions recorded step by step; larger trees show the final state only


def _split(line):
    at = min((i for i in (line.find(":"), line.find(">"), line.find("<")) if i >= 0), default=-1)
    if at < 0:
        return None
    return line[at], line[:at].strip(), [c.strip() for c in line[at + 1:].split(";") if c.strip()]


def _state(t):
    q1, q2 = t.q1, t.q2
    pos = {v: [str(t.Q1.index(v)), str(t.Q2.index(v))] for v in q1}
    return {"q1": q1, "q2": q2, "pos": pos}


def encode(text, limit=LIMIT):
    """Build a tree from the description and return the steps as JSON.

    Each step is one inserted node: the operation, its line, the new node and its parent,
    and (up to ``limit`` insertions) the full state after it: Q1, Q2 and the positions.
    """
    t = DTree("E")
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
            except (KeyError, ValueError) as e:
                msg = e.args[0] if e.args else str(e)
                errors.append({"line": no, "text": line, "msg": f"{child}: {msg}"})
                continue
            parents[child] = t.get_parent(child)
            step = {"line": no, "op": shown, "new": child}
            if recording and len(steps) < limit:
                step.update(_state(t))
            elif recording:
                recording = False
                for s in steps:
                    for k in ("q1", "q2", "pos"):
                        s.pop(k, None)
            steps.append(step)
    final = _state(t) if t.root is not None else {"q1": [], "q2": [], "pos": {}}
    return json.dumps({
        "version": dtree.__version__,
        "root": t.root,
        "parents": parents,
        "steps": steps,
        "final": final,
        "stepwise": recording,
        "limit": limit,
        "renumber": [t.Q1.renumber_count, t.Q2.renumber_count],
        "errors": errors,
    })
