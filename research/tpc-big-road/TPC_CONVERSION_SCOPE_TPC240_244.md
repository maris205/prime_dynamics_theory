# TPC240–244 conversion and bounded prerequisite audit

Updated 2026-09-08. Original source lock:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. This is maintenance of five
existing papers, not a new theorem or paper batch. Original TeX/PDF,
READMEs, proof packages, scientific code, and saved certificates are preserved.

## Reading and conversion scope

The independent read-only source audit read all 75 local source/package text
files (4,154 lines), including the complete manuscript inputs, README,
proof package, and bibliography for each paper. It extracted all five
preserved PDFs (35 pages). Its verdict is `SCOPED_ARCHIVE_REVIEW_ONLY`:
bounded premise/formula checks, not full semantic verification, source/PDF
synchronization certification, or historical experiment reproduction.

All five manuscripts use local macro/section inputs. Their mechanical reading
layers expand only supported static local inputs, retain the original
file/line mapping, and hash-lock every included source against the same
commit. The [converter](maintain_source_markdown.py) and its
[restricted input helper](source_markdown_includes.py) execute no TeX.
Unsupported input syntax fails closed. TPC243–244's system glyph-map input
uses the separately audited exact hash described in the
[TPC250–254 audit](TPC_CONVERSION_SCOPE_TPC250_254.md); it is not manuscript
content or permission to execute arbitrary system inputs.

The per-paper `CONVERSION_RECORD.md` files carry the actual formula counts,
text/formula roundtrip results, complete dependency hashes, displayed-equation
catalogues, and PDF-heading candidates. A nonunique or absent heading hit
stays `UNMAPPED_OR_AMBIGUOUS`; the manual locators below supplement it rather
than replacing it with a guessed automated match. All source bibliographies
invoked by the manuscripts are retained. TPC244's bibliography file is
comment-only and not invoked: no references are invented.

The generated five-paper batch preserves 633 math nodes and 127 raw display
blocks over those 35 existing PDF pages. All five source locks and full
abstract/body formula/text roundtrips pass. Automatic unresolved-heading
counts are 1, 1, 2, 1, 1 for TPC240 through TPC244 respectively; the manual
locations below supplement them without changing their automated status.

### Static-input repair and regression record

Independent read-only task
`tpc-maintenance-include-provenance-audit-20260908` first returned
`REQUIRED_REPAIRS`, with three concrete failures: an IfFileExists wrapper
could drop content while retaining full mechanical status; an in-tree
symlink rebinding could change the requested dependency; CR-only child lines
could point a label to the wrong original file. Glyph-only conditionals and
comment environments were included in the first finding.

The repaired path rejects recognized unsupported conditional/control-flow
contexts before expansion or glyph resolution, refuses any dependency whose
resolved path differs from its declared absolute path, and rejects non-LF
line separators for multi-file source maps. Original bytes remain the hash
inputs. Full TPC245 mutations test that lost/rebound content cannot receive
full status. No original paper was modified to exercise a negative control.

The same independent reviewer replayed the original cases in normal and
optimized modes and returned `ACCEPT_SCOPED`, with no remaining one of the
three reported defects. Its explicit include/maintenance suites passed
51 tests in each mode. The parent's seven additional inventory/checklist
tests bring the complete focused suite to 58 in each mode. Acceptance is
bounded defect closure, not a general TeX-language safety proof.

The reviewed repair hashes are:

| Maintenance file | SHA-256 |
|---|---|
| maintain_source_markdown.py | `553c7c194330e1ae3a6f22e83e0bc1324e107a1597182fbbad7cb6a1f2dfa6bb` |
| source_markdown_includes.py | `e17cc2be3f335f882d6860daa5b15da2b19a6dc9608e4b65ba198fdca80b7698` |
| test_source_markdown_includes.py | `f6a671c01f6ea48b61058f9a83bce3ce18e8f5669582a9e3207f6bf076456e23` |

The parent separately replayed all 169 existing TPC250–418 conversions:
both generated files stayed byte-identical, with 9,850 math nodes retained.
The new ten-paper integrated check passed 10 source locks/roundtrips and
6,999 local-link checks over 28 linked documents. Cross-document non-line
fragments were not independently resolved by that checker. These are
maintenance checks only, not scientific or full semantic verification.

## Per-paper premises and formula boundaries

| Paper | Original source anchor | Bounded finding |
|---|---|---|
| TPC240 | [setup and asymptotic](../../papers/tpc-240-top-prime-direct-energy-floor/paper/sections/2_frozen_setup.tex#L23); [injective row and Riemann sum](../../papers/tpc-240-top-prime-direct-energy-floor/paper/sections/3_exact_row_riemann.tex#L22); [aggregation](../../papers/tpc-240-top-prime-direct-energy-floor/paper/sections/4_weighted_pnt_aggregation.tex#L12) | The smooth real profile is fixed independently of x, nonnegative, supported on [-1,1], and has integral one. Eventually p<q and twice the integer multiplier cutoff is below p. The elementary chain is consistent with the stated profilewise unsigned q-split floor. Uniformity over q is not uniformity over a varying profile class. Weighted PNT and the inherited frame theorem are not newly proved. |
| TPC241 | [kernel](../../papers/tpc-241-top-prime-collision-sharpness/paper/sections/2_frozen_setup.tex#L21); [row mass and Cauchy](../../papers/tpc-241-top-prime-collision-sharpness/paper/sections/3_row_mass_and_cauchy.tex#L24); [liminf](../../papers/tpc-241-top-prime-collision-sharpness/paper/sections/4_coefficient_liminf.tex#L3); [window](../../papers/tpc-241-top-prime-collision-sharpness/paper/sections/5_finite_window_transfer.tex#L16) | Both multiplier signs are already included by the integral-one normalization. Cauchy is applied after q-collapse, on p−1 primitive residues. The frame acts on the full vector before restricting nonnegative coefficient energy; physical-window cross terms are not deleted. The displayed results are lower liminf bounds, not exact energy asymptotics. |
| TPC242 | [Fourier convention](../../papers/tpc-242-phase-fourier-collision-separation/paper/sections/3_phase_fourier_theorem.tex#L11); [disk and defect](../../papers/tpc-242-phase-fourier-collision-separation/paper/sections/4_feasible_disk.tex#L5); [typed transfer limit](../../papers/tpc-242-phase-fourier-collision-separation/paper/sections/5_tpc241_no_transfer.tex#L24) | With conjugate-linear first slot and positive i^(kj) transform, the modes are (norm X squared + norm Y squared, inner(Y,X), 0, inner(X,Y)). Disk attainability uses a nonzero complex Hilbert space; the S=0 branch is separate. Finite Hilbert algebra does not identify the literal V59 remainder. |
| TPC243 | [domain](../../papers/tpc-243-hard-window-near-isometry-bilinear-transfer/paper/sections/2_setup_source_lock.tex#L3); [packing](../../papers/tpc-243-hard-window-near-isometry-bilinear-transfer/paper/sections/3_harmonic_row_bound.tex#L27); [bilinear bound](../../papers/tpc-243-hard-window-near-isometry-bilinear-transfer/paper/sections/4_near_isometry_bilinear.tex#L3); [selected mode](../../papers/tpc-243-hard-window-near-isometry-bilinear-transfer/paper/sections/6_tpc242_transport.tex#L18) | Finite distinct frequencies modulo one, 0<delta≤1/2, and N≥1 consecutive integers are required. Empty/singleton sets and the antipode are treated separately. Gram entries use beta−alpha and the transported target is inner(w,z), not its conjugate. Primitive specialization requires U≥2; a positive lower frame requires epsilon<1. No physical coefficient-norm saving follows. |
| TPC244 | [direct sum](../../papers/tpc-244-common-multiplier-sign-localization/paper/sections/3_direct_sum.tex#L3); [sign cut](../../papers/tpc-244-common-multiplier-sign-localization/paper/sections/4_sign_cut.tex#L19); [window](../../papers/tpc-244-common-multiplier-sign-localization/paper/sections/5_hard_window.tex#L19) | The same multiplier in both orthogonal lanes produces its modulus squared. Real-sign invariance concerns symmetrized edges, not separately zero directed edges. The window bound requires compatible coefficient lanes in one synthesis map and coefficient-space norms. Literal physical attachment remains conditional. |

## Preserved source qualifications

1. TPC240's [window kernel](../../papers/tpc-240-top-prime-direct-energy-floor/paper/sections/6_route_boundary.tex#L19)
   is top-prime-only, whereas TPC241's
   [same-named kernel](../../papers/tpc-241-top-prime-collision-sharpness/paper/sections/2_frozen_setup.tex#L36)
   uses all active denominators. The shared symbol does not identify the objects.
2. TPC241's [conclusion](../../papers/tpc-241-top-prime-collision-sharpness/paper/sections/8_conclusion.tex#L3)
   uses “of size,” but its proved display is a lower liminf. Sharpness up to
   logarithms additionally needs the inherited upper envelope, not reviewed here.
3. TPC242's [abstract](../../papers/tpc-242-phase-fourier-collision-separation/paper/sections/0_abstract.tex#L1)
   must be read with its common-offset hypothesis. Unsignedness alone does not
   prove the same offset in four phase-labelled energies or physical annihilation.
4. TPC243's [abstract error wording](../../papers/tpc-243-hard-window-near-isometry-bilinear-transfer/paper/sections/0_abstract.tex#L14)
   refers to a defined upper envelope, not equality with the actual Gram
   deviation. A singleton family has zero deviation even if that envelope is
   positive. An additive error also needs a strict margin to preserve nonzero sign.
5. TPC244's [coefficient display](../../papers/tpc-244-common-multiplier-sign-localization/paper/sections/2_source_lock.tex#L4)
   uses an arithmetic set D_x not defined locally. Its
   [proof-package interface](../../papers/tpc-244-common-multiplier-sign-localization/PROOF_PACKAGE.md#L186)
   names upstream papers, without re-establishing them here. This is a literal
   source prerequisite, not a counterexample to the arbitrary-coefficient algebra.
6. The [TPC244 window setup](../../papers/tpc-244-common-multiplier-sign-localization/paper/sections/5_hard_window.tex#L3)
   compresses the coefficient-space premise stated more explicitly in
   [Corollary C of its package](../../papers/tpc-244-common-multiplier-sign-localization/PROOF_PACKAGE.md#L64).
   Arbitrary abstract vectors cannot be fed to a frequency synthesis map without
   the compatible identification and inherited delta,N domain.
7. TPC244's [real-sign iff](../../papers/tpc-244-common-multiplier-sign-localization/paper/sections/4_sign_cut.tex#L44)
   is not an arbitrary-unit-phase iff. Its triangle constant is not shown to
   be attained by the literal V59 kernel.
8. The Montgomery–Vaughan book metadata is
   [2007 in TPC240](../../papers/tpc-240-top-prime-direct-energy-floor/paper/references.bib#L29)
   and [2006 in TPC241](../../papers/tpc-241-top-prime-collision-sharpness/paper/references.bib#L1).
   Both original values remain; this pass does not adjudicate the edition year.

## Manual existing-PDF locators

These are one-based physical PDF pages from complete text extraction, not
visual rendering certification. Main numbered sections are listed in order.

| Paper | Section start pages | Additional locators |
|---|---|---|
| TPC240 | 1, 2, 3, 4, 5, 5, 6 | References 6–7; appendix 7; PDF has 7 pages. |
| TPC241 | 1, 2, 3, 4, 5, 6, 6, 7 | References 7; appendix heading/prose 7, floated table 8; PDF has 8 pages. |
| TPC242 | 1, 2, 3, 4, 5, 5, 6, 6 | References 7; appendix 7–8; PDF has 8 pages. |
| TPC243 | 1, 2, 3, 4, 4, 5, 6, 6, 7 | Subsection 2.1 on 2; references/appendix 7; PDF has 7 pages. |
| TPC244 | 1, 2, 2, 3, 4, 4, 5, 5 | Appendix 5; no references heading; PDF has 5 pages. |

ActualText substitutions and extraction loss of overbars or nested norm
delimiters can obscure formulas, particularly TPC242–244. These are extraction
limitations, not established printing errors; TeX remains the formula source.

## Independent audit evidence and exclusions

Read-only audit task `tpc-maintenance-source-scope-240-244-20260908` reported
unchanged HEAD and handoff hash, no changed files, and exit 0 for its reads,
PDF metadata/text extraction, and one stdout-only exact-arithmetic check.
That check reproduced the frozen rational exponent/constants ledger, the
four-phase transform of X=1+i,Y=2−i, a disk-defect equality, and a two-block
real-sign versus complex-phase distinction. It imported no scientific
producer. These checks are finite deductions, not asymptotic or physical
evidence. The parent spot-checked the reported local source-domain omission.

Upstream PNT/frame/source interfaces, certificate and mutation claims,
scientific code, full PDF/TeX synchronization, and full semantic correctness
remain unverified by this bounded review. Converter verification is recorded
separately in the [maintenance handoff](../../TPC_HANDOFF.md).

TPC418 retains `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, arithmetic
advance `NO`, fixed-power credit `0`, and full Gate B `OPEN`. No new number,
physical identification, growing-family theorem, or scientific credit is created.
