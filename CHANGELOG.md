# Changelog

## 1.3.1

- **EulerTree: Q1 as it develops**, suggested by Enis Olgac. View 3 opens on the one list for EulerTree (DTree keeps "Sorted by Q1"; each encoding remembers its own choice while the page is open). Blocks are bracketed: `A[` opens the block of A, `]A` closes it, so the list reads as a nested term. The new node is marked in every step, and so is its parent's closing cell when the parent was a leaf before; the cells glide to their new places as you step.

## 1.3.0

- **EulerTree:** a new choice "Encoding" shows triordinal-dtree's EulerTree (`triordinal.dtree.euler`) next to DTree. EulerTree keeps Q1 alone, with a closing cell after the subtree of every node with children; node u reaches v exactly when v's cell lies inside u's block. View 3 shows the one list as stored, closing cells included (clicking a closing cell picks its node), or the nodes in Q1 order with the rank of their block end read from the right, which is the Q2 rank; the plane is the same as with DTree. Picking two nodes answers by the block: "02's block: places 2 to 17 of the list; 15 at place 4 (inside)".
- **Positions:** a new choice "Positions" sets rational or integer positions (`positions="integer"`, new in triordinal-dtree 2.2.0) for both encodings. Integer positions are shown in full in the stored list and with five significant digits in the sorted view; each cell's tooltip has the exact value. The stats line names the kind of position and the renumberings of each list.
- Both choices are remembered per browser. The default example is computed in advance for all four combinations, so the page shows the chosen one while Python loads.
- The local server takes `?kind=dtree|euler&positions=rational|integer` on `/api/encode` (400 for other values); `dtree-explorer --version` names triordinal-dtree instead of dtree-encoding.
- Requires triordinal-dtree 2.2.0; the browser version installs 2.2.0 from PyPI, and the built-in fallback copy also holds `euler.py`.

## 1.2.1

- Computed by **triordinal-dtree** 2.1.0: the browser version installs 2.1.0 from PyPI, and the built-in fallback copy holds its sources. No change to the Explorer itself; the Q1 and Q2 positions it shows now come from lists in which every node with children also has a closing cell (not shown).

## 1.2.0

- Computed by **triordinal-dtree** 2.0.0, the new home of DTree (repository EnisOlgac/Triordinal), instead of dtree-encoding. The library's API is unchanged; the Explorer imports `triordinal.dtree`, the browser version installs `triordinal-dtree` (with `triordinal-dlist`) from PyPI, and its built-in fallback copy holds both.

## 1.1.0

- **Animated insertion:** each edge step glides from the old picture to the new one in every view. The new node starts at its parent and moves into place; the other nodes move to their new ranks, while their stored positions stay unchanged. Speed Slow, Normal, Fast or No animation (remembered per browser); Play waits for each step. Steps of more than one edge, and browsers set to reduced motion, switch without animation.
- **Q1 and Q2 sorted by Q1** (the new default of view 3), suggested by Enis Olgac: one column per node in Q1 order, with its Q1 and Q2 rank and stored positions. Q1 rises by one from column to column; Q2 rises from a node to the next exactly when the next is its child, and drops where a new block begins (marked in orange). Below the table, the Q2 ranks are joined in Q1 order, which is the plane's points joined in Q1 order. "Each in its own order" shows the previous layout.

## 1.0.2

Archived on Zenodo: doi:10.5281/zenodo.23701538 (all versions).

- Online at **https://dtree.digraphs.net/**; README and package links point there. The online copy counts visits with GoatCounter (no cookies, no personal data, no consent banner) instead of Google Analytics, and links to a privacy notice and an imprint (`site/privacy.html`, `site/imprint.html`).
- Citation metadata (`CITATION.cff`) and Zenodo metadata (`.zenodo.json`): the archive is linked to the chapter (is supplement to doi:10.5772/intechopen.1013408) and to DTree (requires doi:10.5281/zenodo.23395710).

## 1.0.1

- **Edge by edge:** the step buttons are labeled "Previous edge" and "Next edge", and the left and right arrow keys step backward and forward (except while typing). Suggested by Enis Olgac.
- The step line names the edge: "Edge 7 of 19: 02 → 07", "v before 6" or "X after 03".

## 1.0.0

First release of the DTree Explorer, a web page that encodes a directed tree with DTree's two projections Q1 and Q2 and shows it step by step.

- **Input:** examples from the paper (introductory example, Figure 1, Section 4.1 Cases A and B, Appendix A with its three variants, each also written with `<`/`>`), your own `.csx` file, or typed lines `p: c1; c2`, `s > c`, `s < c`. Faulty lines are reported one by one.
- **Step slider** with Play, up to 300 insertions; larger trees show the final state.
- **Views**, each switchable: the tree, the plane (each node at its rank in Q1 and Q2), and the lists Q1 and Q2 with the library's positions. Pictures can be saved as SVG or PNG.
- **Pick nodes:** one node shows what reaches it and what it reaches; two nodes answer "does u reach v?" with both comparisons. **Collapse/expand** subtrees in the tree.
- **Three ways to run it:** `dtree-explorer` (local server, computes with the installed dtree-encoding, works offline); the single file `DTree-Explorer.html` attached to each release (computes in the browser with Pyodide and dtree-encoding from PyPI); online at dtree.digraphs.net. Only the online copy counts visits, after consent.
