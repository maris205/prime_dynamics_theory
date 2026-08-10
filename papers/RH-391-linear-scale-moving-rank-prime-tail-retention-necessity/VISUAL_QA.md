# RH-391 visual QA

## Final manuscript build

The quiescent warning-clean manuscript build produced:

    pages: 8
    page size: A4
    rotation: 0
    PDF bytes: 341924
    PDF SHA-256:
    90275847d4e07c9c6fb8a7fdf8ea291abf1b044bb74c70cd59740c2baef0d9d1
    log bytes: 25675
    log SHA-256:
    4df66e0d74de6b8b5950b26d93a4ceb372ee5bfa9a436ebfda6128fbafe8b16d
    font rows: 21

All 21 font rows are embedded, subset, and Unicode-mapped.  The LaTeX and
BibTeX diagnostic scan is empty.  Ghostscript null-device rendering and
`pdftotext` extraction pass without replacement characters.  The
semantic publication PDF is byte-identical to `main.pdf`.

## Completed visual inspection

Every one of the eight pages was rasterized and inspected.  The review
found no:

- clipped or overlapping text;
- equations, URLs, hashes, or bibliography outside the text block;
- blank, duplicate, rotated, or truncated page;
- malformed math glyph or literal formatting command;
- illegible source locator, declaration, or scope statement.

The exact title, abstract, Theorem 1.1, same-rank quantifiers, fixed-gap
extraction, edge factors, integer-tail payment chains, gamma lemma,
Taylor lift, two-endpoint profile, source hashes, declarations, and
bibliography are legible.  Independent physical QA reproduced the same
eight-page, 341,924-byte PDF and exact SHA-256.
