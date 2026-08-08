# RH-388 format audit

## Manuscript structure

The paper contains title metadata, abstract, keywords, two quantified
main theorems, numbered proof sections, novelty and source-integrity
sections, six declarations, and bibliography.  All equation labels,
cross-references, and citations resolve.

## Bibliography

All seven bibliography entries are cited.  The Johnston--Yang entry
records the JMAA article and DOI; the Maynard entry records the Annals
article, page range, and DOI.  RH-381, RH-383, RH-384, RH-386, and RH-387
are cited only at the inherited facts they support.  There are no orphan
entries.

## Typesetting checks

The final rebuild satisfies:

- ten A4 pages with zero rotation;
- no LaTeX, BibTeX, undefined-reference, overfull, or underfull warning;
- all 22 font rows embedded, subset, and Unicode-mapped;
- Ghostscript null-device pass;
- successful text extraction without replacement characters;
- semantic publication PDF byte-identical to `main.pdf`;
- visual inspection of every rasterized page for clipping, overlap,
  truncation, blank pages, duplicates, rotation, or illegible hashes.

The exact byte count and SHA-256 are recorded in `VISUAL_QA.md`.

## Machine-readable format

`results/result.json` is strict finite JSON.  Its schema declares
official Draft 2020-12, is recursively closed, fixes all array lengths,
and rejects Boolean aliases for integers.  Builders run identically
under `python -OO`.
