# RH-386 visual QA

## Final manuscript build

The quiescent warning-clean manuscript build produced:

```text
pages: 8
page size: A4
rotation: 0
PDF bytes: 371254
PDF SHA-256: f05f74be2e8ad392bbba98f5488706912a0ece48e9b372ddf14b9d4e32d5de8d
font rows: 22
```

All 22 font rows are embedded, subset, and Unicode-mapped. The LaTeX and
BibTeX warning scan is empty. Ghostscript null-device rendering and
`pdftotext` extraction pass. The semantic publication PDF is byte-identical
to `main.pdf`.

## Completed visual inspection

Every page was rasterized at 120 dpi and inspected. The review found no:

- clipped or overlapping text;
- equations, tables, or hashes outside the text block;
- blank, duplicate, rotated, or truncated pages;
- illegible bibliography or metadata;
- inconsistent page geometry.

The title, abstract, numbered displays, uniform-family suprema, certificate
hash, declarations, and bibliography are all legible. Independent physical
QA reproduced the same 8-page, 371,254-byte PDF and exact SHA-256.
