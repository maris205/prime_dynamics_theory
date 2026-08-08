# RH-387 visual QA

## Final manuscript build

The quiescent warning-clean manuscript build produced:

    pages: 6
    page size: A4
    rotation: 0
    PDF bytes: 336464
    PDF SHA-256:
    465ae4c9e6e08b47c3f69fa650cb0a92dac8457943403a5847a97a48c577c450
    font rows: 21

All 21 font rows are embedded, subset, and Unicode-mapped. The LaTeX and
BibTeX warning scan is empty. Ghostscript null-device rendering and
pdftotext extraction pass. The semantic publication PDF is byte-identical
to main.pdf.

## Completed visual inspection

Every page was rasterized and inspected. The review found no:

- clipped or overlapping text;
- equations, source hashes, or bibliography outside the text block;
- blank, duplicate, rotated, or truncated pages;
- illegible source metadata or declarations;
- inconsistent page geometry.

The title, abstract, theorem, strict Stieltjes boundary, all-order
coordinates, endpoint gradient ledger, scope firewalls, source identifiers,
declarations, and bibliography are legible. Independent physical QA
reproduced the same six-page, 336,464-byte PDF and exact SHA-256.
