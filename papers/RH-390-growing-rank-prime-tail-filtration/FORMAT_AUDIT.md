# RH-390 format audit

## Manuscript structure

The paper contains title metadata, abstract, keywords, three quantified
main theorems, a unified transfer lemma, an all-rank positivity lemma,
numbered proof sections, a novelty/source boundary, six declarations, and
bibliography.  All equation labels, references, and citations resolve.

## Bibliography

All eight bibliography entries are cited and there are no orphan entries.
Johnston--Yang and Maynard are the two remote primary inputs.  RH-381,
RH-383, RH-384, RH-386, RH-387, and RH-388 are cited at their exact roles.
No RH-389, TPC-137, or Tao dependency is introduced.

## Typesetting checks

The final rebuild satisfies:

- nine A4 pages with zero rotation;
- no LaTeX, BibTeX, undefined-reference, duplicate-label, overfull, or
  underfull warning;
- all 21 font rows embedded, subset, and Unicode-mapped;
- Ghostscript null-device rendering pass;
- successful text extraction without replacement characters;
- semantic publication PDF byte-identical to `main.pdf`;
- visual inspection of all nine rasterized pages for clipping, overlap,
  truncation, blank pages, duplicates, rotation, and malformed glyphs.

The exact PDF bytes and SHA-256 are recorded in `VISUAL_QA.md`.

## Machine-readable format

`results/result.json` is strict finite JSON.  Its schema declares official
Draft 2020-12, is recursively closed, fixes all array lengths, and rejects
Boolean aliases for integers.  Normal and optimized `python -OO` builders
agree for result, schema, manifest, and archive report.
