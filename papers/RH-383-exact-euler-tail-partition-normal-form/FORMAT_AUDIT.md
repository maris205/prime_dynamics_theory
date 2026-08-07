# RH-383 format and citation audit

The manuscript follows the ARS theoretical-paper workflow: title, abstract,
keywords, definitions, frozen predecessor inputs, theorem statements, proofs,
an exact artifact protocol, limitations, an explicit route verdict, and
declarations are present.

## Citation checks

- Every repository citation key in `main.tex` resolves in `references.bib`.
- RH-374 supports the finite run formula and terminal convention.
- RH-379 supports the fixed universally safe phasewise `c11=0` factor class.
- RH-380 supports the exact ordered increment.
- RH-381 supports the infinite telescope and first coefficient layer.
- RH-382 supports the two-scale quadratic coefficient layer and its distinct
  special-purpose remainder boundary.
- RH-MVP2 supports the preserved four-volume corpus and Gate boundary.
- No web result or theorem outside the 41-file immutable repository contract is
  presented as a source for an RH-383 claim.

## Mathematical typography

- The square-clock product `mathcal P_y`, the power sums `P_r(y)`, the tail
  radius `rho_y`, and the square clock `q_y` are kept distinct.
- The successor loss is `d_(j+1)` throughout; it is not the predecessor
  even-run count `L_j`.
- The partition sign is displayed by partition length, while the aggregated
  elementary-symmetric sign is displayed separately by total degree.
- Terminal `R8=mathcal P_y E8`, exact `E9=0`, and the exclusion of `E10` are
  explicit.
- Formula labels and references resolve after a complete `latexmk` pass.
- Literal carriage-return scan is zero.

## Declarations and metadata

PDF title, author, subject, and keywords match the manuscript. Data/code,
contributions, funding, competing interests, ethics, and AI-assistance
declarations are present. Code and data provenance is supplied by the
repository artifact, its 41 immutable source locks, and the replay
instructions. The final PDF has 9 A4 pages and 25 font rows; every font is
embedded, subsetted, and Unicode-mapped. The bibliography's `Möbius` glyph
survives Poppler text extraction.
