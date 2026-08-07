# RH-383 visual PDF QA

The final `main.pdf` was rendered with Poppler at 140 dpi. All 9 pages were
inspected individually at readable resolution.

| Page | Content checked | Verdict |
|---|---|---|
| 1 | Title, abstract, endpoint formula, partition compiler, remainder theorem, keywords, start of frozen class | PASS: balanced title block; formulas centered; no clipping or collision |
| 2 | Factor-class definition, terminal convention, odd-prime tail bound, convergence lemma, endpoint products | PASS: symbols and equation numbers are clear; no margin overflow |
| 3 | Exact `C/W` normal form, absolute-convergence proof, partition notation and signs | PASS: displays and prose flow cleanly; no orphaned heading |
| 4 | Boxed all-order compiler, `m=2` cancellation, sign firewall, increment arrays and strict-successor formula | PASS: box fits; `d_(j+1)` is consistent and legible |
| 5 | Ordered increment compiler, direct `A_c/F_c` telescope, coefficient bridge, low-order identities | PASS: all suffix indices and denominators are readable |
| 6 | New cubic block and arbitrary-order remainder through the two increment ledgers | PASS: cubic vectors, box, powers, and constants are visually distinct |
| 7 | Remainder summation, executable protocol, exact-row table, mutation and schema boundary | PASS: table fits the text width; all row labels remain readable |
| 8 | Route verdict, limitations, future source-lock trigger, data/code, contributions, funding, competing-interest, and ethics declarations | PASS: bullets and declaration paragraphs are balanced and unclipped |
| 9 | AI-assistance disclosure and six references | PASS: declaration and bibliography are complete and unclipped; `Möbius` renders correctly |

Global checks:

- A4 portrait, 9 pages, no blank or truncated page.
- No overlapping text, clipped glyphs, broken equations, or margin overflow was
  observed.
- Main and semantic PDFs are byte-identical after the final build.
- Poppler text extraction and Ghostscript parsing pass.
- All 25 font rows are embedded, subsetted, and Unicode-mapped.
