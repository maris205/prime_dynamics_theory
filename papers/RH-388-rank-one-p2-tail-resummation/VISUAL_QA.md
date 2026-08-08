# RH-388 visual QA

## Final manuscript build

The quiescent warning-clean manuscript build produced:

    pages: 10
    page size: A4
    rotation: 0
    PDF bytes: 362578
    PDF SHA-256:
    e4e58fba1fbf8481ca258380d64a634fdce82ecb1811da837270e2f63f8c0da9
    font rows: 22

All 22 font rows are embedded, subset, and Unicode-mapped.  The LaTeX and
BibTeX warning scan is empty.  Ghostscript null-device rendering and
`pdftotext` extraction pass without replacement characters.  The
semantic publication PDF is byte-identical to `main.pdf`.

## Completed visual inspection

Every one of the ten pages was rasterized and inspected.  The review
found no:

- clipped or overlapping text;
- equations, hashes, source URLs, or bibliography outside the text block;
- blank, duplicate, rotated, or truncated pages;
- malformed math glyphs or literal formatting commands;
- illegible declarations or source metadata.

The title, abstract, both main theorems, `60/13` arithmetic, factorial
remainder, moving-window induction, endpoint derivative ledgers,
bounded-gap successor argument, rank-one direction, source identifiers,
declarations, and bibliography are legible.  Independent physical QA
reproduced the same ten-page, 362,578-byte PDF and exact SHA-256.
