# RH-379 format and PDF audit

## Format profile

- Target: repository-native mathematical article; no external journal template
  or word limit was specified.
- Engine: PDFLaTeX through `latexmk`, using the repository's standard
  `article` layout, A4 paper, 11-point type, and one-inch margins.
- Language: English, matching the locked predecessor papers.  A bilingual
  abstract was not introduced because neither the repository house style nor
  the available PDFLaTeX toolchain provides that requirement.
- Front matter: title, program author, date, abstract, and keywords are
  present.  PDF title, author, subject, and keyword metadata are populated.
- Back matter: limitations, data availability, ethics, contributions,
  funding, interests, AI-assisted-workflow disclosure, and six-item
  bibliography are present.
- Citation style: repository-standard numeric `plain` BibTeX style.  All six
  cited keys resolve and there are no orphan entries.

## Final PDF checks

| Check | Result |
|---|---|
| Semantic PDF equals `main.pdf` byte-for-byte | Pass |
| Final SHA-256 | `a5cf5b0a80354e7d0d3d3b55023440a7631af2c6c4a36d5e4c579df898f5555f` |
| Page count and size | 9 pages, A4 (`595.276 x 841.89 pt`) |
| LaTeX log SHA-256 | `46702a5d8ac97bcd4d37e1ec06e423101d3c43f7f545061a334c5828435da08f` |
| Undefined citations or references | 0 |
| Multiply defined labels | 0 |
| Overfull or underfull boxes | 0 |
| LaTeX or package warnings in final log | 0 |
| Embedded fonts | 23 of 23 |
| `pdftotext` extraction | Pass; 3,870 words extracted |
| Ghostscript null-page render | Pass |
| Encryption, forms, JavaScript | None |

The PDF is not tagged for accessibility; tagged-PDF production was not part
of the repository profile.  Text extraction and Unicode maps are present for
all embedded fonts.

## Visual gate

Every final page was rendered at 120 dpi and inspected individually.  The
first render exposed a bibliography orphan page containing only reference 6.
The bibliography was locally set in `\small`, the PDF was rebuilt to nine
pages, and all nine final pages were rerendered and reinspected.  The detailed
page ledger is `VISUAL_QA.md`.

**Format verdict: PASS for the declared repository profile.**
