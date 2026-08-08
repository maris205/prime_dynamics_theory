# RH-386 format audit

## Manuscript structure

The paper contains title metadata, abstract, keywords, numbered theorem
and proof sections, exact-artifact and claim-boundary section, declarations,
and bibliography. Equation labels and cross-references are resolved.

## Bibliography

The Johnston--Yang entry records the exact authors, article title, journal,
volume, issue, article number, year, DOI, and arXiv version. RH-384 is cited
only for the explicitly labelled finite regression. There are no orphan
bibliography entries.

## Typesetting checks

The release PDF must satisfy all of the following after the final rebuild:

- A4 pages with zero rotation;
- no LaTeX, BibTeX, undefined-reference, overfull, or underfull warnings;
- all fonts embedded, subset, and Unicode-mapped;
- Ghostscript null-device pass;
- successful text extraction;
- semantic publication PDF byte-identical to `main.pdf`;
- visual inspection of every rasterized page for clipping, overlap,
  truncation, blank pages, duplicate pages, or illegible hashes.

The exact final byte count, SHA-256, page count, and font-row count are
recorded in `VISUAL_QA.md` after the quiescent build.

## Machine-readable format

`results/result.json` is strict finite JSON. Its schema declares official
Draft 2020-12, is recursively closed, fixes every array length, and rejects
Boolean aliases for integers. Builders run identically under `python -OO`.
