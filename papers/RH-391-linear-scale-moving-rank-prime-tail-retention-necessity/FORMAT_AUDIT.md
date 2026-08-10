# RH-391 format audit

## Manuscript structure

The paper contains exact title metadata, abstract, keywords, one central
quantified theorem, two supporting lemmas, a proof in three compact
sections, novelty and scope, executable source closure, six declarations,
and bibliography.  All equation labels, references, and citations
resolve.

## Bibliography

All six bibliography entries are cited and there are no orphan entries.
Maynard is the sole remote analytic theorem invoked.  Johnston--Yang is
cited only for inherited provenance.  RH-383, RH-384, RH-388, and RH-390
are cited at their exact roles.  No RH-389, TPC-137, or Tao dependency is
introduced.

## Typesetting checks

The final rebuild satisfies:

- eight A4 pages with zero rotation;
- no LaTeX, BibTeX, undefined-reference, duplicate-label, overfull, or
  underfull warning;
- all 21 font rows embedded, subset, and Unicode-mapped;
- Ghostscript null-device rendering pass;
- successful text extraction without replacement characters or literal
  formatting commands;
- semantic publication PDF byte-identical to `main.pdf`;
- visual inspection of all eight rasterized pages for clipping, overlap,
  truncation, blank pages, duplicates, rotation, and malformed glyphs.

The exact PDF bytes and SHA-256 are recorded in `VISUAL_QA.md`.

## Machine-readable format

`results/result.json` is strict finite JSON.  Its schema declares official
Draft 2020-12, is recursively closed, fixes every array length, and
rejects Boolean aliases for integers.  Normal and optimized `python -OO`
builders agree for result, schema, manifest, and archive report.
