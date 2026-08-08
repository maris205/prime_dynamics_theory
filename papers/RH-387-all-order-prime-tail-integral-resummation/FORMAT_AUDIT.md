# RH-387 format audit

## Manuscript structure

The paper contains title metadata, abstract, keywords, a quantified main
theorem, numbered proof sections, exact-artifact and source-integrity
sections, declarations, and bibliography. All equation labels,
cross-references, and citations resolve.

## Bibliography

The Johnston--Yang entry records the exact authors, article title, journal,
volume, issue, article number, year, DOI, and arXiv version. RH-383 is cited
only for the exact endpoint normal form, and RH-386 only for the frozen
strict source transfer and the comparison with its finite-partition
scope. There are no orphan bibliography entries.

## Typesetting checks

The final rebuild satisfies:

- six A4 pages with zero rotation;
- no LaTeX, BibTeX, undefined-reference, overfull, or underfull warnings;
- all 21 font rows embedded, subset, and Unicode-mapped;
- Ghostscript null-device pass;
- successful text extraction;
- semantic publication PDF byte-identical to main.pdf;
- visual inspection of every rasterized page for clipping, overlap,
  truncation, blank pages, duplicates, rotation, or illegible hashes.

The exact final byte count and SHA-256 are recorded in VISUAL_QA.md.

## Machine-readable format

results/result.json is strict finite JSON. Its schema declares official
Draft 2020-12, is recursively closed, fixes every array length, and rejects
Boolean aliases for integers. Builders run identically under python -OO.
