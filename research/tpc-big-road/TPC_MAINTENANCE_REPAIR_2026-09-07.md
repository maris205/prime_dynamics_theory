# Source-Markdown repair and bounded prerequisite audit

Updated 2026-09-07. Scope: repair TPC355–418 (64 prior conversions) and add
TPC350–354 (five preserved manuscripts). This is archive maintenance, not a
numbered publication, a certificate rerun, or a route decision.

## What was repaired

The previous conversion pipeline and its aggregate prose were not reliable
enough to reuse unchanged. The repair regenerates only the identified
mechanical `paper/main.md` and `CONVERSION_RECORD.md` files, while preserving
original TeX, PDFs, bibliographies, code, certificates, README files, proof
packages, and hand-edited notes.

- A whitespace-cleanup character class also matched literal terminal `t`
  and backslash characters. Examples included `text` becoming `tex` and
  `highest` becoming `highes`. The replacement uses whitespace-only trimming
  and checks the entire normalized text after Markdown parsing.
- Older PDF page maps used inferred positions and asserted match scores.
  New maps record actual extracted heading-text hits, with absent or multiple
  hits explicitly marked `UNMAPPED_OR_AMBIGUOUS`. TPC402's “Signed coefficient
  identity” matches pages 1 and 2; neither is silently selected.
- Generic proof-package `PASS` wording overstated the review, especially for
  TPC359–363, which have no separate `PROOF_PACKAGE.md`. New records identify
  available files and distinguish availability, mechanical preservation, and
  mathematical review.
- The claim that every converted source lacked references was false.
  TPC350–355 have source `thebibliography` entries; TPC356–358 use external
  `references.bib` files. The reference text/BibTeX is now retained and hashed
  where applicable. Citation keys remain explicit when not resolved.
- Title/author/date metadata is taken from the source; missing metadata is
  not filled with a standard date or affiliation. The complete abstract,
  tables, and source sections are retained. Theorem/proof environment names
  and boundaries are preserved, without inventing their printed numbering.
- Label cross-references point to the corresponding original TeX line where
  Markdown does not provide the printed equation target. Original label TeX
  is retained in the formulas. Rendering remains Markdown-engine dependent.
- Coverage summaries and per-directory file counts are recounted. A
  source-complete conversion is not called a reliable, independently reviewed
  mathematical manuscript merely because it has an abstract and references.

## Reproducible mechanical scope

The read-only planner/checker is
[maintain_source_markdown.py](maintain_source_markdown.py). It emits patches
only on request and never writes original sources or runs scientific jobs.
Its initial repair source lock is repository commit
`388a605cbc0ce49256310c2efc1f2df77edafadd`. Each record includes TeX/PDF and
applicable bibliography hashes; each file is compared with that source commit.

For TPC350–418, the full abstract/body math-node sequence is compared before
Markdown writing and after Markdown parsing, including inline/display kind
and whitespace-normalized TeX. All 69 sequences pass (2,881 math nodes in
total), and all 69 normalized plain-text roundtrips pass. These checks detect
writer/cleanup corruption; they do not independently prove that Pandoc's
LaTeX reader implements every source macro correctly. Raw source display
blocks are separately catalogued with line locations and hashes. PDF text
is used for navigation, not as a claim that the PDF was rebuilt from this TeX.

The focused regression suite contains 12 tests for text endings, nested
titles, display-count boundaries, real/absent page matches, patch EOFs,
equation-source/repository-relative links, bibliography retention, absent proof packages, and
the current endpoint's math preservation:

```bash
python -B -m unittest discover -s research/tpc-big-road -p test_source_markdown_maintenance.py -v
python -B research/tpc-big-road/maintain_source_markdown.py --paper 418 --check
```

No claim is made that the production certificates, numerical row counts,
Bridge-B cascade, or all archived proofs were rerun or independently verified
in this maintenance pass. Prior broad semantic `PASS` wording is superseded
by these explicit limits, not upgraded through a different label.

## Manual prerequisite audit: TPC350–354

The complete TeX, README, and proof package for these five papers were read.
The review below checks the stated elementary identities and their necessary
hypotheses, not the numerical certificates. Source claims and review findings
are kept distinct.

| Paper | Key formula and source location | Prerequisite check / limitation |
|---|---|---|
| TPC350 | [masked matrix and balanced contrast](../../papers/tpc-350-fresh-growth-signed-incidence/paper/main.tex#L61); [Gram identity and norm witness](../../papers/tpc-350-fresh-growth-signed-incidence/paper/main.tex#L110) | Finite interval, both nondivisibility masks, and fixed source signs are retained. The balanced coefficients sum to zero by equal positive/negative block sizes. Every prime incidence is included, not an exclusive owner partition. Gram expansion follows from finite linearity; normalization requires `b_I != 0`. The 192-row panel is finite evidence only. |
| TPC351 | [reciprocal coefficients and identities](../../papers/tpc-351-reciprocal-shell-contrast/paper/main.tex#L79) | A nonempty ordered shell is required for the mean `1/r`; rational centering gives zero sum. Coefficients depend on the shell, not fitted responses. Gram expansion is algebraic; the norm witness requires `c_I != 0`. No sign cancellation or uniform floor follows. Numerical comparisons to the 192-row parent are retained as source claims, not recomputed. |
| TPC352 | [witness identities](../../papers/tpc-352-reciprocal-shell-adversarial-holdout/paper/main.tex#L62) | The same algebra works for any specified finite `D_I`, a nonempty shell, and nonzero `c_I`. The 144-row holdout remains finite. **Source/implementation mismatch:** the manuscript's operator definition does not match the inspected producer; see the separate finding below. The numerical claims are therefore not endorsed as statements about the literal printed operator. |
| TPC353 | [polarization and Cauchy envelope](../../papers/tpc-353-source-native-masked-l2-polarization/paper/main.tex#L71) | For finite real `A,L,b`, expanding `A(L-b)` proves polarization. The normalized coefficient and envelope require `E_L+E_b > 0`. Cauchy–Schwarz bounds the cross term; it does not prove its arithmetic sign. The declared finite V59 source is not an asymptotic identification. The 216-row signs/ranges were not rerun. Source notation issues remain below. |
| TPC354 | [polarization and Cauchy envelope](../../papers/tpc-354-higher-origin-masked-l2-holdout/paper/main.tex#L70) | The same finite-real and positive-denominator conditions apply. The higher-origin panel changes the finite origins only; it is not a growing or source-uniform theorem. The 216-row readout and parent comparison remain source claims. Source notation ambiguity remains below. |

### Unresolved source finding: TPC352 operator mismatch

At [TeX lines 42–52](../../papers/tpc-352-reciprocal-shell-adversarial-holdout/paper/main.tex#L42),
the source writes `P_p f(n) = p 1_{p|n} f(n)` and an uncentered kernel `K_s`.
Sandwiching that kernel produces support on multiples of `p` and a `p^2`
factor. Calling this weighted multiplication a projection is also not literal
idempotence for prime `p`.

The inspected [producer matrix construction](../../papers/tpc-352-reciprocal-shell-adversarial-holdout/code/tpc352_reciprocal_shell_adversarial_holdout.py#L145)
instead uses one `p` factor, the centered residue term
`1_{p|(u-t)} - 1/(p-1)`, and both **nondivisibility** masks. Its
[rational anchor matrix](../../papers/tpc-352-reciprocal-shell-adversarial-holdout/code/tpc352_reciprocal_shell_adversarial_holdout.py#L184)
uses the same nondivisibility/centering structure. These are different
operators, not a Markdown conversion discrepancy. TPC351's
[printed matrix](../../papers/tpc-351-reciprocal-shell-contrast/paper/main.tex#L60)
uses the latter structure. No original formula, producer, certificate, or
release is changed here. Resolving the publication mismatch requires a
separate source/certificate reconciliation before semantic promotion.

### Unresolved source notation: TPC353–354

TPC353 [line 66](../../papers/tpc-353-source-native-masked-l2-polarization/paper/main.tex#L66)
and TPC354 [line 65](../../papers/tpc-354-higher-origin-masked-l2-holdout/paper/main.tex#L65)
contain the literal string `b(t)=2C_2,1_{2\nmid t}...`. The comma is preserved;
a multiplication symbol is not guessed. TPC353
[line 83](../../papers/tpc-353-source-native-masked-l2-polarization/paper/main.tex#L83)
contains literal `qquad` without the leading backslash; this too is retained.
The abstracts use the shifted source `Lambda(t+2)`, while the displayed
finite vector identity abbreviates it as `Lambda`/`L`. The elementary identity
is valid for any specified finite `L`; this review does not supply an omitted
source-identification convention or certify the printed model definition.

## Remaining work and route ceiling

After this repair batch: 69 `full-source-md`, 0 `reliable-full-md`, 753
`partial-or-notes`, and 1 `source-inaccessible`, across 823 inventory entries.
The source-inaccessible entry is specifically
`tpc-207-moving-hole-bdh-translation-compiler`: the directory has other
artifacts but no local Markdown/TeX/PDF manuscript. It is not the accessible
`tpc-207-critical-moving-hole-bdh-defect` directory.

The remaining accessible sources still need conversion and per-paper review;
this batch does not complete the whole archive. Known source issues and the
TPC402 page ambiguity stay open. Rule-audit and PrimeGaps186 review work is
not repeated by this repair.

`TPC418_ROUND2_CLUE = NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES` remains
unchanged. No TPC419, arithmetic advance, fixed-power credit, or new theorem
is created.
