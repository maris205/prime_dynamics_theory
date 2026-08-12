# RH-397 format audit

## Frozen quartet

- `main.tex`: 27,620 bytes, SHA-256
  `a0ded93cfcd46f48b602e3f276a39e01e99ba8c37d3961316540f3925064ec11`.
- `references.bib`: 505 bytes, SHA-256
  `2ef184fbd1594af83c0a16fd8f868c3572d91d86c30d40f98271781ca0044b3b`.
- `main.pdf`: 387,054 bytes, SHA-256
  `be06c3bcd37acb7f2144cd390423ae207f9b412ffd833a8156a317c59dd44ea6`.
- `main.log`: 26,381 bytes, SHA-256
  `3ff4d9317931ff356e76340cca833fba7fc50f38668234fe5ff4cec32c402aba`.

BibTeX followed by three successful `pdflatex` passes produced the frozen
quartet.  A targeted scan of the complete log found no LaTeX error, undefined
control sequence, unresolved citation or reference, rerun request, overfull
box, or underfull box.

## PDF structure and text

`pdfinfo` reports the exact title `Odd-Lag Half-Span Overlap Mobius Capacity`,
author `RH research program`, nine A4 pages, PDF version 1.5, no encryption,
no forms, and no JavaScript.  Ghostscript parses the PDF with exit status zero.
`pdftotext` recovers the fixed-clock weighted independent-set formula, the
odd-lag maximum and declared-clock parity classification, source-role and
claim firewalls, declarations, and both bibliography entries.  No replacement
character, placeholder, raw `qquad`, or raw `maxJ` token remains.

## Fonts, geometry, and semantic copy

`pdffonts` reports 25 rows.  Every row is embedded, subset, and Unicode-mapped.
All nine pages have A4 media and crop boxes with zero rotation.  The semantic
publication PDF `odd-lag-half-span-overlap-mobius-capacity.pdf` is byte-exact
with `main.pdf`; archive verification hard-gates that equality.

All nine pages were rasterized and inspected at page scale.  No clipped
equation, margin escape, overlap, broken glyph, blank-page anomaly, or unreadable
table was found.  `VISUAL_QA.md` records the page-by-page check.

Format verdict: pass.
