# Changelog

## 1.0.2

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
