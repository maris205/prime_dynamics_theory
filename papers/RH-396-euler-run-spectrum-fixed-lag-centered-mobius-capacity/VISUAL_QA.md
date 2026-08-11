# RH-396 visual QA

## Method

The frozen 15-page `main.pdf` was parsed with Ghostscript, rendered page by
page, and inspected against extracted text.  Page size is A4 throughout and
the document is unencrypted.  The inspection checked clipping, overlaps,
equation breaks, table legibility, footer/header collisions, missing glyphs,
blank pages, and bibliography layout.

## Page record

| Page | Principal content | Verdict |
|---:|---|---|
| 1 | title, abstract, introduction, model opening | pass |
| 2 | definitions, density compiler, fixed-clock theorem | pass |
| 3 | four-state boundary, Euler-run endpoint, lag corollary | pass |
| 4 | RH-394 bridge, positive projection | pass |
| 5 | relation saturation, reflection, tropical optimizer | pass |
| 6 | non-self-loop compression proof | pass |
| 7 | self-loop obstruction and square-support definitions | pass |
| 8 | per-state marginal and pair/path charge | pass |
| 9 | square saturation, same-support cover, `h=6` fixtures | pass |
| 10 | finite run densities and finite endpoint | pass |
| 11 | infinite densities, cofinal limit, certified intervals | pass |
| 12 | fresh-prime deletion and recurrence | pass |
| 13 | plateau, CRT even run, eventual strictness | pass |
| 14 | finite nonattainment and lag landscape | pass |
| 15 | source roles, limitations, declarations, references | pass |

No visual blocker or minor defect was found.  All 24 font rows are embedded,
subset, and Unicode-mapped.  Visual verdict: pass, 15/15 pages.
