# RH-390 visual QA

## Final manuscript build

The quiescent warning-clean manuscript build produced:

    pages: 9
    page size: A4
    rotation: 0
    PDF bytes: 362762
    PDF SHA-256:
    f86dd4f2705acd87a532bf489f9b1c98996c076497b2cefba940b83693412bc5
    log bytes: 25679
    log SHA-256:
    13e8289c85a89edb8c8f62d74ecc10b66678fe94cef70e2304475deb5c3bc34b
    font rows: 21

All 21 font rows are embedded, subset, and Unicode-mapped.  The LaTeX and
BibTeX diagnostic scan is empty.  Ghostscript null-device rendering and
`pdftotext` extraction pass without replacement characters.  The semantic
publication PDF is byte-identical to `main.pdf`.

## Completed visual inspection

Every one of the nine pages was rasterized and inspected.  The review
found no:

- clipped or overlapping text;
- equations, tables, URLs, hashes, or bibliography outside the text block;
- blank, duplicate, rotated, or truncated page;
- malformed math glyph or literal formatting command;
- illegible source locator, declaration, or scope statement.

The title, abstract, three theorem statements, strict endpoint, safe
`A/B/C` ledger, full factorial window, growing-rank proof, all-rank gamma
table, bounded-gap jump, common-head Taylor estimate, source identifiers,
declarations, and bibliography are legible.  Independent physical QA
reproduced the same nine-page, 362,762-byte PDF and exact SHA-256.
