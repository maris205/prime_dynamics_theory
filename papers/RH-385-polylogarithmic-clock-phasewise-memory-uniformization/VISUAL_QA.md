# RH-385 Visual QA

## Review protocol

The publication PDF is checked in three layers:

1. scan `main.log` for warnings, unresolved references/citations, overfull or
   underfull boxes, and fatal errors;
2. use `pdfinfo`, `pdffonts`, `pdftotext`, and Ghostscript to verify page
   metadata, embedded fonts, selectable text, and renderer acceptance;
3. rasterize every page and visually inspect the title, theorem displays,
   ledger, optimizer/diagonal sections, long hashes, boundaries,
   declarations, and bibliography.

## Layout criteria

- no clipped text, equations, hashes, or list items;
- no blank, duplicate, or unexpectedly rotated pages;
- consistent margins and page numbers;
- readable abstract, proofs, declarations, and bibliography;
- all displays stay within the text block;
- build and semantic PDFs are byte-identical.

## Final observations

- Final length: 8 A4 pages; no blank or duplicate page.
- Page 1: two-line title, abstract bound, keywords, and opening context are
  balanced and unclipped.
- Pages 2--4: interpolation census, cutoff definition, DFT normalization,
  and the `4/13/6/4` proof remain inside the margins.
- Pages 5--6: fixed-`B` closure, optimizer transfer, endpoint theorem, and
  square-clock sentinel/diagonal are legible.
- Page 7: certificate counts, dedicated 64-character hash lines, limitations,
  and Gate boundary fit without overflow.
- Page 8: conclusion, six disclosure paragraphs, and all bibliography entries
  are readable with no orphaned reference page.
- LaTeX log: zero actionable warnings, overfull/underfull boxes, undefined
  references, or undefined citations.
- Fonts: all reported rows are embedded and subset Type 1 fonts with Unicode
  mappings.
- Text extraction and Ghostscript null-device rendering: PASS.
- Semantic/build PDF byte identity: PASS.

`pdfinfo` reports 8 pages, A4 (`595.276 x 841.89 pt`), 385,944 bytes,
PDF 1.5, no encryption, forms, JavaScript, rotation, or suspect objects.
`pdffonts` reports 24 rows, all embedded and subset with Unicode mappings.
The final PDF SHA-256 is
`61b6949f38b21887c97115a07ed09e7155b9363ba98b7983a11412a4a1ced448`.
