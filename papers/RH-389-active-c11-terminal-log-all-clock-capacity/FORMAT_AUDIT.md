# RH-389 format audit

## Manuscript structure

The paper contains title metadata, abstract, keywords, two quantified main
theorems, a capacity definition, numbered proof sections, source and
novelty boundaries, six declarations, and bibliography.  All equation
labels, references, and citations resolve.

## Bibliography

All six bibliography entries are cited and there are no orphan entries.
Davenport and Mirsky support the classical analytic channels and densities.
TPC-137 is the direct determinant-two Mobius source; Tao is upstream
Liouville provenance.  RH-378 records the prior q=1 conditional constant,
and RH-379 supports the independent prefix-channel argument.

## Typesetting checks

The final rebuild satisfies:

- eight A4 pages with zero rotation;
- no LaTeX, BibTeX, undefined-reference, duplicate-label, overfull, or
  underfull warning;
- all 25 font rows embedded, subset, and Unicode-mapped;
- Ghostscript null-device rendering pass;
- successful text extraction without replacement characters;
- semantic publication PDF byte-identical to `main.pdf`;
- visual inspection of all eight rasterized pages for clipping, overlap,
  truncation, blank pages, duplicates, rotation, and malformed glyphs.

The exact PDF bytes and SHA-256 are recorded in `VISUAL_QA.md`.

## Machine-readable format

`results/result.json` is strict finite JSON.  Its schema declares official
Draft 2020-12, is recursively closed, fixes all array lengths, and rejects
Boolean aliases for integers.  Normal and `python -OO` builders agree.
