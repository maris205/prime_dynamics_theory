# RH-396 format audit

## Frozen source and build

- `main.tex`: 48,304 bytes, SHA-256
  `5d9a8c6c9a39436d07a94e082fffc003cfba91ece1d3859c11e2facbd5ffe99d`.
- `references.bib`: 1,739 bytes, SHA-256
  `2a5f201d51355bf0eb930484b4c9d3ad3d02bc145eed11809b0ab533956c599f`.
- `main.log`: 25,949 bytes, SHA-256
  `0cb4d57eb4c1f8ed0203a707fa8915258fb634c7499b69b21a232d731e061a25`.
- `main.pdf`: 447,519 bytes, SHA-256
  `590f472a38bbe652b4f3a2e1eac11a407d9c5ed8a076abb3419334106834db1d`.

The LaTeX/BibTeX build completed with resolved citations and references.  The
complete log contains no undefined-control-sequence, missing-reference,
missing-citation, overfull-box, underfull-box, or rerun warning.

## PDF structure

`pdfinfo` reports:

- title `Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity`;
- author `RH research program`;
- 15 pages;
- A4 geometry, `595.276 x 841.89 pts`;
- no encryption, forms, JavaScript, or suspect structure;
- PDF version 1.5.

Ghostscript parses the file with a zero exit status.  `pdftotext` extracts the
title, all three main theorem statements, the `B_infinity(h)` endpoint, the
lag infimum and claim firewall, declarations, and all five bibliography
entries.

## Fonts and semantic copy

`pdffonts` reports exactly 24 rows.  Every row is embedded, subset, and carries
a Unicode map.  The semantic publication PDF
`euler-run-spectrum-for-fixed-lag-centered-mobius-capacity.pdf` is required by
the archive gate to be byte-identical to `main.pdf`, including its exact
447,519-byte length and SHA-256.

## Page rendering

All 15 pages were rasterized and reviewed at page scale.  No clipped equation,
overlapping text, blank page, broken reference, margin escape, or unreadable
table was found.  The page-by-page record is in `VISUAL_QA.md`.

Format verdict: pass.
