# RH-385 Format Audit

## Manuscript structure

- Title, author, date, abstract, keywords: present.
- Frozen sources and claim boundary precede the new theorem.
- Definition, lemma, proposition, theorem, corollary, remark, and proof
  environments are consistent.
- The theorem chain is ordered as coefficient census, cutoff/DFT ledger,
  uniform limit, optimizer transfer, endpoint, and diagonal witness.
- Certificate/source lock and context/limitations are separate sections.
- Data, ethics, contributions, funding, interests, and AI-workflow
  declarations are present.
- Every bibliography entry is cited.

## LaTeX checks

- Engine: pdfLaTeX through `latexmk`.
- Page size and margins: A4, one inch.
- Fonts: embedded/subset Latin Modern Type 1 with Unicode mappings.
- Hyperlinks: internal and citation links enabled with hidden boxes.
- Cross-references and citations: resolved after a full bibliography build.
- Log scan: no package warning, overfull box, underfull box, unresolved
  reference, or unresolved citation.
- Long source hashes are set on dedicated small monospaced lines within the
  text block.

## Artifact naming

- Build PDF: `main.pdf`.
- Semantic PDF: `polylogarithmic-clock-phasewise-memory-uniformization.pdf`.
- The archive verifier requires byte identity.

The final PDF has 8 A4 pages. Detailed font, text, Ghostscript, raster, size,
and SHA-256 checks are recorded in `VISUAL_QA.md` and `REPLAY_AUDIT.md`.
