# RH-379 final page-by-page visual QA

Final PDF SHA-256:
`a5cf5b0a80354e7d0d3d3b55023440a7631af2c6c4a36d5e4c579df898f5555f`.
All pages were rendered from that PDF at 120 dpi and inspected at original
render resolution.

| Page | Content checked | Verdict |
|---:|---|---|
| 1 | Two-line title, author/date, abstract equations, keywords, section opening | Pass: balanced title block; no clipped display; keywords wrap cleanly |
| 2 | Definition, interpolation, AP density formulas, phase-limit theorem | Pass: cases and product subscripts remain legible; equation numbers clear |
| 3 | Cutoff proof, blocker, 512 census, nine-row canonical table | Pass: exactly nine distinct rows; table rules and all columns fit |
| 4 | Subset proof, compatibility matrix, three-state DP | Pass: matrix centered; no overflow in max-plus display |
| 5 | MWIS converse, reflection, definition of `G`, square-clock setup | Pass: boxed absolute-value formula fits; run notation and new `B_y` definition are clear |
| 6 | Euler inequalities, run recurrence, square-clock theorem, `q=36` chain | Pass: dense page but full margins retained; theorem box and ranges readable |
| 7 | One-site embedding and arbitrary-clock retained/tail proof | Pass: finite-`N` bound including `O(1)` is fully visible; no stranded heading |
| 8 | Supremum close, exact fixture table, limitations | Pass: ten fixture rows fit; monospaced labels and census hash are unbroken |
| 9 | Gates, conclusion, declarations, six references | Pass: all six references fit at readable size; no bibliography orphan page |

The initial ten-page render failed only the page-balance criterion because
reference 6 occupied page 10 alone.  After the bibliography-only size
adjustment, the final nine-page render passed clipping, overlap, margin,
table, equation, heading, and page-balance checks on every page.

**Visual verdict: PASS.**
