# RH-384 Visual QA

## Review protocol

The PDF is checked in three layers:

1. automated log scan for unresolved references, undefined citations, overfull boxes, and fatal errors;
2. `pdfinfo`, `pdffonts`, and `pdftotext` checks for page metadata, embedded fonts, and selectable text;
3. raster rendering of every page followed by visual inspection of the title page, theorem displays, interval section, table, claim boundary, declarations, and bibliography.

## Layout criteria

- no clipped text, equations, hashes, or table cells;
- no blank or duplicate pages;
- consistent margins and running page numbers;
- readable abstract and bibliography;
- displayed equations do not cross the text block;
- table rules and column wrapping remain legible;
- semantic and build PDFs are byte-identical.

## Final observations

- Final length: 8 pages, A4, no blank or duplicate page.
- Title page: balanced two-line title; abstract, display equations, keywords, and opening section remain inside margins.
- Pages 2–6: theorem headings, proof endings, equation numbers, fractions, and the long positive-contrast display are unclipped and legible.
- Page 7: certificate table, 64-character hashes, source counts, and boundary bullets fit the text block.
- Page 8: remaining boundary bullets, all six declarations, and nine bibliography entries fit without an orphaned final reference page.
- LaTeX log: zero overfull boxes, underfull boxes, undefined references, undefined citations, or package warnings.
- Fonts: all reported fonts are embedded, subset Type 1 fonts with Unicode mappings.
- Text: `pdftotext` confirms selectable title, abstract, theorem statements, declarations, and references.
- Ghostscript null-device render: PASS.
- Semantic/build PDF byte identity: PASS.

`pdfinfo` reports 8 pages, A4 (`595.276 x 841.89 pt`), 366,799 bytes, PDF 1.5, no encryption, forms, JavaScript, or suspect objects. The final PDF SHA-256 is `87f3ef9b67af90c204907121946c1fe736573321b3eb526623f8bb9352b29f74`. Every page was rasterized and visually inspected after the final bibliography reflow.
