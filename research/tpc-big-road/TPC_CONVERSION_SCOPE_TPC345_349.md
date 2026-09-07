# TPC345–349 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock: repository commit
`1de1964aa411aa631587da690524beadf1127d3c`. These are five existing
manuscripts, not five new papers. The complete TeX, README, and proof package
for each paper were read; their originals remain unchanged.

## Conversion evidence

All five full-abstract/body math sequences and normalized text roundtrips
pass: 336 math nodes, 52 raw-source display blocks, and 19 extracted PDF
pages. Each `CONVERSION_RECORD.md` contains source/PDF hashes, applicable
bibliography hashes, section-line/page maps, and formula locations. TPC348's
external bibliography and TPC349's source reference entry are retained.
TPC345–347 have no source bibliography; none is invented.

The automated map leaves two sections unresolved: TPC346's appendix
“Reproducibility record” and TPC347's “Finite audit” (hits on pages 2 and 3).
A separate read-only extraction of TPC346 PDF page 4 confirms the appendix
heading `A Reproducibility record` there. This manual observation supplements
the automated record; the current matcher does not strip alphabetic appendix
numbers. TPC347's multiple hits are not resolved by guessing.

Conversion checks establish mechanical preservation, not independent proof,
certificate, source-implementation, or rendered-PDF certification. No
scientific generator, production checker, or numerical experiment was run.

## Per-paper prerequisite and claim-boundary review

| Paper | Source formula / scope | Bounded review result |
|---|---|---|
| TPC345 | [principal angles and projection identity](../../papers/tpc-345-principal-angle-grassmann-audit/paper/main.tex#L90) | The two subspaces must inhabit the same protocol-aligned Euclidean response space; `Q_i` must have orthonormal columns. Exact invariance concerns column spaces and nonsingular changes of basis, not arbitrary floating-point rank-threshold stability. Pythagorean decomposition requires an orthogonal projector. The residual ratio and equal-row scaling require nonzero target norms. The observed ranks, angles, shear errors, and 18 LOO pairs are source-reported finite data, not recomputed here. |
| TPC346 | [frozen models](../../papers/tpc-346-third-panel-hostile-replication/paper/main.tex#L73); [finite identities](../../papers/tpc-346-third-panel-hostile-replication/paper/main.tex#L127) | `N_shared c = N_adaptive(c,c,c)` proves subspace inclusion and non-increasing **in-sample projection** residual under one common weighting. It does not bound held-out coefficient-prediction residuals. The target norm must be positive for a retention ratio. Projection identities are not silently applied to cross-fit predictions. The finite three-panel threshold failures do not prove a universal no-go theorem. |
| TPC347 | [mask factorisation](../../papers/tpc-347-convolution-mask-defect-interface/paper/main.tex#L71); [unmasked Fourier bounds](../../papers/tpc-347-convolution-mask-defect-interface/paper/main.tex#L99) | Both nondivisibility projections and diagonal deletion remain. Expanding `(P-I)KP+K(P-I)` gives `PKP-K`. The finite shell, fixed height, and declared exponents `s=1,2` give an absolutely summable unmasked kernel, so the Fourier multiplier statement applies to `K_e`, not directly to masked `A_I`. Restriction/zero extension are contractions; the mask-defect term remains in the triangle bound. The displayed sign-free tail proof is checked for integer truncation radius and signs of absolute value at most one; see the qualification below. |
| TPC348 | [coordinate formula and lower witness](../../papers/tpc-348-position-aware-mask-defect-lower-witness/paper/main.tex#L95) | The two cases `p|t` and `p∤t` retain respectively the right-mask and left-mask contribution. The coordinate vector on the right is understood through its zero extension. The maximum requires a nonempty active-shell hit set `J_I`; its lower-witness inequality follows from unit coordinate vectors without symmetry or common-sign assumptions. A nonempty hit set alone does not prove strictly positive response. Positivity on 192 rows remains a numerical source claim. |
| TPC349 | [balance, incidence, Gram expansion, and normalized witness](../../papers/tpc-349-prime-balanced-signed-defect-witness/paper/main.tex#L81) | Source signs `epsilon_p` and test coefficients `beta_j` are separate. Equal positive/negative index blocks give coefficient sum zero; multiply-divisible incidences must be added, not assigned to exclusive owners. The finite Gram expansion is algebraic; normalization requires `b_I != 0`. Zero coefficient sum alone does not imply a nonzero vector, positive response, or cross-prime cancellation. The numerical comparison is finite and not uniformly positive. The printed anchor's coverage is limited as described below. |

## Source qualifications retained, not silently repaired

TPC347 [TeX lines 133–139](../../papers/tpc-347-convolution-mask-defect-interface/paper/main.tex#L133)
states a tail bound for `R >= 1`, then uses
`sum_{d>R} d^(-2s) <= R^(1-2s)/(2s-1)`. That integral comparison is valid
as used for positive **integer** `R`; it is not generally valid for every real
`R >= 1` without an adjusted cutoff. For example, at `s=1`, `R=19/10`, even
the partial sum from `d=2` through `10` exceeds `10/19`. The manuscript's
actual audit uses the integer `R=65536`, so this qualification does not by
itself invalidate that finite protocol. No statement about arbitrary real
cutoffs is endorsed, and no source formula is edited.

TPC349 [TeX lines 213–229](../../papers/tpc-349-prime-balanced-signed-defect-witness/paper/main.tex#L213)
declares an anchor on `[1,14]` with shell primes `(5,7)` and describes it as
testing the incidence sum at positions divisible by both primes. The interval
contains occurrences of each prime, but no position divisible by both:
the first positive common multiple is 35. Therefore this anchor alone does
not exercise simultaneous multiple-divisibility handling or distinguish an
exclusive-owner shortcut at such a position. The displayed vector has four
unit-magnitude entries and squared norm 4 as stated. The larger numerical
panel and mutation suite were not rerun, so their coverage is not inferred
from this anchor description.

## Coverage and handoff

This batch adds five mechanical full-source conversions to the repaired
TPC350–418 set. Current coverage becomes 74 `full-source-md`, 0
`reliable-full-md`, 748 `partial-or-notes`, and 1 `source-inaccessible`, across
823 entries. Each new record links this bounded review. The
[earlier repair audit](TPC_MAINTENANCE_REPAIR_2026-09-07.md) remains a dated
69-paper snapshot, including the still-unresolved TPC352 operator mismatch.

The next existing source-priority batch is TPC340–344. No new paper directory
or number is authorized by maintenance. TPC418's scientific handoff remains
`NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`, with no arithmetic advance,
zero fixed-power credit, and full Gate B open.
