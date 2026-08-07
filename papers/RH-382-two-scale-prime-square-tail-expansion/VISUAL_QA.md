# RH-382 visual PDF QA

The final `main.pdf` was rendered with Poppler at 130 dpi. All 8 pages were
inspected individually at readable resolution.

| Page | Content checked | Verdict |
|---|---|---|
| 1 | Title, abstract, three coefficients, boxed expansion, keywords, start of fixed-class definition | PASS: balanced title block; formulas centered; no clipping or collision |
| 2 | Exact gap input, square-clock data, finite Euler ratios, terminal `R8=P E8` | PASS: equation numbers and prose margins clear |
| 3 | Exact numerator/memory forms, `E9=0`, coefficient definitions, Bonferroni lemma | PASS: terminal argument and displays legible; no orphaned heading |
| 4 | Product proof, explicit `7/24<1`, inverse-product remainder, `931/4` and `63` ledgers | PASS: multi-line proof flows cleanly; no overflow |
| 5 | `H` loss, quadratic identities, cube telescopes and proof | PASS: all summation indices and powers readable |
| 6 | Boxed main theorem, numerator and memory error ledgers, `3301/6<551`, `S_y` remark | PASS: both boxes fit; opposite `S_y` signs visually distinct |
| 7 | Exact artifact, corrected `p=71` values `a=T=1/5040`, `S=a^2=1/5040^2`, wrong-sign mutation, start of limitations | PASS: no contradictory equality; code block and bullets fit |
| 8 | Remaining limitations, declarations, five references | PASS: complete ending; bibliography labels and long commit strings remain inside margins |

Global checks:

- A4 portrait, 8 pages, no blank or truncated page.
- No overlapping text, clipped glyphs, broken equations, or margin overflow was
  observed.
- Main and semantic PDFs are byte-identical after the final build.
- Poppler text extraction and Ghostscript parsing pass.
- All fonts are embedded, subsetted, and Unicode-mapped.
