# RH-382 format and citation audit

The manuscript follows the ARS theoretical-paper workflow: title, abstract,
keywords, definitions, sourced predecessor propositions, lemmas, theorem,
proof, exact artifact protocol, limitations, and declarations are present.

## Citation checks

- Every repository citation key in `main.tex` resolves in `references.bib`.
- RH-374 supports the finite run formula and terminal convention.
- RH-379 supports the frozen factor class and supremum framework.
- RH-380 supports the exact increment.
- RH-381 supports the infinite telescope and `H` product.
- RH-MVP2 supports the retained Gate boundary.
- No external reference is presented as if independently searched or
  verified outside the repository.

## Mathematical typography

- `T_y` and `S_y` remain visually distinct.
- The opposite signs on `2m_infinity S_y` are displayed in the theorem.
- Terminal `R_8=P_yE_8`, exact `E_9=0`, and the exclusion of `E_10` are
  explicit.
- Formula labels and references resolve after a complete `latexmk` pass.
- Literal carriage-return scan is zero.

## Declarations and metadata

PDF title, author, subject, and keywords match the manuscript. Data/code,
contributions, funding, competing interests, ethics, and AI disclosure
sections are present. The final PDF has 8 A4 pages and 21 font rows; every
font is embedded, subsetted, and Unicode-mapped.
