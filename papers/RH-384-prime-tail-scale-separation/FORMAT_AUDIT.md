# RH-384 Format Audit

## Manuscript structure

- Title, author, date, abstract, keywords: present.
- Frozen class and predecessor inputs: present before new theorems.
- Definitions, lemma, theorem, corollary, proposition, proof, and remark environments: consistent.
- Main theorem chain: Abel tail, partition scale, five intrinsic scales, five gap limits, interval positivity, eventual sign.
- Executable protocol and claim boundary: separate sections.
- Six required declarations: present.
- Bibliography: all entries cited.

## LaTeX checks

- Engine: pdfLaTeX through `latexmk`.
- Page size/margins: A4, one inch.
- Fonts: embedded Latin Modern Type 1.
- Hyperlinks: internal/citation links enabled without colored boxes.
- Cross-references and citations: resolved after full build.
- Mathematical notation: `Delta_y` reserved for the gap; `A,B,C` defined once; interval quantity labeled explicitly.
- Tables: booktabs, no vertical rules, widths confined to the text block.

## Artifact naming

- Build PDF: `main.pdf`.
- Semantic PDF: `prime-tail-scale-separation.pdf`.
- Archive verifier requires byte identity.

The final PDF/log and rendered-page checks are recorded in `VISUAL_QA.md` and `REPLAY_AUDIT.md`.

Final build status: 8 pages; zero LaTeX warnings, overfull boxes, underfull boxes, unresolved references, or unresolved citations. The bibliography was set one size smaller to keep all nine entries on the declarations/reference page without sacrificing legibility.
