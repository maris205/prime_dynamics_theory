# RH-389 visual QA

## Final manuscript build

The quiescent warning-clean manuscript build produced:

    pages: 8
    page size: A4
    rotation: 0
    PDF bytes: 410071
    PDF SHA-256:
    87466ccb24166e7f1a71e1c0cead1f776e6ad9a733667858442fb22485dd3d24
    log bytes: 26169
    log SHA-256:
    fc0d9b88046e0d32fcebeb76e7cb3ba6a12cf25a5251e8c51bddd9bb14021da5
    font rows: 25

All 25 font rows are embedded, subset, and Unicode-mapped.  The LaTeX and
BibTeX diagnostic scan is empty.  Ghostscript null-device rendering and
`pdftotext` extraction pass without replacement characters.  The semantic
publication PDF is byte-identical to `main.pdf`.

## Completed visual inspection

Every one of the eight pages was rasterized and inspected.  The review
found no:

- clipped or overlapping text;
- equations, tables, URLs, hashes, or bibliography outside the text block;
- blank, duplicate, rotated, or truncated page;
- malformed math glyph or literal formatting command;
- illegible source locator, declaration, or scope statement.

The title, abstract, fixed-table theorem, all-clock capacity theorem, both
Abel endpoint regimes, determinant-two substitution, eight-action table,
predecessor charge, reflection parity, source identifiers, declarations,
and bibliography are legible.  Independent physical QA reproduced the
same eight-page, 410,071-byte PDF and exact SHA-256.
