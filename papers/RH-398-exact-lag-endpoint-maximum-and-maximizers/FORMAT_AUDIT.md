# RH-398 format audit

## Frozen quartet

- `main.tex`: 27,562 bytes, SHA-256
  `96aa193b9fe66b613cf3ba95807e17c02b10e244e1d4a76bdbc5544e4337bdbf`.
- `references.bib`: 468 bytes, SHA-256
  `dc4ea72d618069df20559cd7af7ab5b6d6c7405516427dbf544248b672810161`.
- `main.pdf`: 358,870 bytes, SHA-256
  `b5ac3c2f5489815dc4c98c64c88bb64d818c4ca3789dc789027332e968cfe96f`.
- `main.log`: 27,083 bytes, SHA-256
  `54e9a49ad184cd8f7f3afe003c3ae52aa684c84c6976915f3f6cc8253011eb49`.

A targeted scan of the complete frozen log found no LaTeX error, undefined
control sequence, unresolved citation or reference, rerun request, overfull
box, underfull box, or multiply defined label.  The final tree contains no
LaTeX auxiliary or bibliography cache file.

## PDF structure and text

`pdfinfo` reports the exact title `Exact Lag Endpoint Maximum and Maximizers`,
author `Prime Dynamics Theory Project`, 11 A4 pages, zero rotation, no encryption, no
forms, and no JavaScript.  Ghostscript parses the PDF with exit status zero.
`pdftotext` recovers the fixed interface, product and telescope, four-branch
deletion formula, exact maximizer criterion, complement and quantitative gap,
joint endpoint, source-role and claim firewalls, declarations, and both
bibliography entries.  No replacement character, placeholder, or raw command
token remains in the text layer.

## Fonts, geometry, and semantic copy

`pdffonts` reports 22 rows.  Every row is embedded, subset, and Unicode-mapped.
All 11 pages have A4 media and crop boxes with zero rotation.  The semantic
publication PDF `exact-lag-endpoint-maximum-and-maximizers.pdf` is 358,870
bytes, has the same SHA-256 as `main.pdf`, and is byte-identical to it;
archive verification hard-gates that equality.

All 11 pages were rasterized at 150 dpi and inspected at page scale after the
final quartet was declared unique and quiescent.  No clipped equation, margin
escape, overlap, broken glyph, unintended blank page, or unreadable table was
found.  `VISUAL_QA.md` records the page-by-page check.

Format verdict: pass.
