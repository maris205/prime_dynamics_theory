# TPC265–269 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`524af4ad2c623e839511e915db5d85e6c41c7c9e`. All five complete TeX
manuscripts, README files, proof packages, and bibliography sidecars were
read. Original scientific sources, hand-edited materials, code, certificates,
and local build products remain unchanged.

## Conversion evidence

All five mechanical reading layers pass abstract/body formula-sequence and
normalized-text roundtrips: 359 math nodes and 71 raw-source display blocks
across 21 extracted PDF pages. Every source section has a unique heading-text
page match. All manuscripts use inline bibliography items, retained in the
reading layers; unused external BibTeX sidecars remain unchanged. No
bibliographic verification, visual PDF certification, or proof of PDF/TeX
synchronization is claimed. The converter did not require modification.

No physical producer, original stress suite, full interval replay, or
publication cascade was executed. Checks below comprise bounded algebra,
exact comparisons of saved decimal strings, and read-only source inspection.
Only the isolated serialization functions from TPC267 and TPC268 were
executed on a synthetic fraction; no scientific certificate was regenerated.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC265 | [Schur set](../../papers/tpc-265-schur-endpoint-budget-compiler/paper/main.tex#L79); [radial envelopes](../../papers/tpc-265-schur-endpoint-budget-compiler/paper/main.tex#L111); [compiler](../../papers/tpc-265-schur-endpoint-budget-compiler/paper/main.tex#L153) | P must be an orthogonal projection on the same complex Hilbert space; disk realizability needs complement dimension at least two and fixed nonnegative residual norms. Dimension one gives the circle, with a different lower edge. The upper bound does not need positive radius, but phase formulas dividing by abs(c) need the c=0 branch. Power hypotheses must hold for all sufficiently small epsilon on one common growing clock; the proof package makes this quantifier explicit. |
| TPC266 | [paid-lane interface](../../papers/tpc-266-end-to-end-claim-firewall/paper/main.tex#L135); [soundness hypotheses](../../papers/tpc-266-end-to-end-claim-firewall/paper/main.tex#L142); [six fixtures](../../papers/tpc-266-end-to-end-claim-firewall/paper/main.tex#L229) | A type descriptor is not an analytic estimate. Soundness assumes actual magnitude bounds for both abs(c) and R, not merely a phase name or saved paid flag. The strictness test is a sufficient conditional rule; a rejected weak upper bound does not imply that the actual scalar fails the target. Six displayed cases do not prove a general minimality or exhaustive classification theorem for all combinations of missing/deleted lanes. |
| TPC267 | [source and matrix](../../papers/tpc-267-literal-v59-residual-radius-census/paper/main.tex#L62); [projection](../../papers/tpc-267-literal-v59-residual-radius-census/paper/main.tex#L105); [enclosures](../../papers/tpc-267-literal-v59-residual-radius-census/paper/main.tex#L145) | Four equal blocks require positive N divisible by eight, not only even; all listed scales qualify. There are three contrasts, not four, and their span excludes the block-constant mean direction. The printed cross-Gram formula is real-valued here; complex extensions require conjugation. Positive residual norm factors justify division and the nonnegative square-root threshold transfer. Internal outward grid operations and serialized decimal displays have different guarantees. |
| TPC268 | [comparison zeroing rule](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/paper/main.tex#L51); [threshold decision](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/paper/main.tex#L111); [matched pair](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/paper/main.tex#L127) | The following prose zeroing rule is part of the comparator definition. With N,H,Q,s fixed, changing z changes w, not beta, A, or P3. Changing H or s does change matrix entries, so the entire 16-row grid does not use one unchanged matrix. Strict classification requires an interval wholly on one side of 1/16; the inspected function rejects unresolved intervals. A large displayed upper endpoint alone would not certify an obstruction. |
| TPC269 | [cutoff registry](../../papers/tpc-269-growing-cutoff-profile-transfer/paper/main.tex#L67); [affine identity](../../papers/tpc-269-growing-cutoff-profile-transfer/paper/main.tex#L103); [profile flip](../../papers/tpc-269-growing-cutoff-profile-transfer/paper/main.tex#L134) | The six-entry registry agrees with floor(natural log N) at those six scales, but its implementation is a lookup, not a growing-scale theorem. Fixed w,beta,P3 and a common inner product give affine output and cross-Gram. The squared radius is a polynomial of degree at most two and the normalized ratio is generally non-affine/non-monotone; every quotient needs a nonzero radius. Convexity of the profile needs 0≤theta≤1. Matrix structure is preserved while the matrix entries vary with theta. |

## TPC265–266: boundary cases and actual lane semantics

Exact fraction checks give
`5/3−1997/1200=1/400` and
`1/320−1/1200=11/4800<1/400<1/320`.
For the manuscript fixture c=2,R=3, the disk upper/lower edges are 5 and 0;
the circle edges are 5 and 1. Independently free disks with radii 1,2,3 have
sum radius 6 and upper edge 8 over the same center. Independence here means
freely selectable residuals, not stochastic independence.

TPC265's [lower-edge proof](../../papers/tpc-265-schur-endpoint-budget-compiler/paper/main.tex#L123)
chooses `−Rc/abs(c)` when `abs(c)≥R`; the corner c=R=0 must instead use
z=0. The theorem is valid at that corner, but the written division is
undefined. The literal `qquad` at
[TeX line 97](../../papers/tpc-265-schur-endpoint-budget-compiler/paper/main.tex#L97)
remains unchanged. The borderline power estimate carries epsilon loss;
it must not be paraphrased as an established `O(x^E*)` bound. Nor does an
unpaid upper-bound lane prove non-decay of the actual scalar.

TPC266's [lane builder and composer](../../papers/tpc-266-end-to-end-claim-firewall/code/tpc266_end_to_end_claim_firewall.py#L98)
operate on descriptors and rational saving/loss numbers. A `SIGNED_PHASE`
label is paid by the same exponent test as a `POWER` label; this does not
establish the theorem's radius inequality. Orthogonal unit residual vectors
can have cross-Gram zero and radius one, so a small signed scalar need not
bound the norm-product radius. A phase theorem may instead replace the
feasible-set envelope, but that is a separately identified argument.

Likewise, a newly paid radius alone does not complete the stated two-lane
compiler while the center remains only fixed-log. The
[next-input prose](../../papers/tpc-266-end-to-end-claim-firewall/paper/main.tex#L277)
must be read as a possible next input, not a sufficient closure contract.
TPC265's [proof-package corollary](../../papers/tpc-265-schur-endpoint-budget-compiler/PROOF_PACKAGE.md#L77)
correctly requires paying both lanes or replacing the disk envelope by
new signed information. None of these interface checks supplies that input.

## TPC267–269: saved decimals are not the internal rational intervals

The inspected interval constructors use rational endpoint arithmetic and
outward rounding to a 10^-30 grid. However, TPC267's
[decimal serializer](../../papers/tpc-267-literal-v59-residual-radius-census/code/tpc267_literal_residual_radius_certificate.py#L129)
and TPC268's [serializer](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py#L111)
format both endpoints with the same 12-significant-digit general format;
square roots use 10 significant digits. They do not specify directed
lower/upper rounding. TPC269 [reuses these functions](../../papers/tpc-269-growing-cutoff-profile-transfer/code/tpc269_growing_cutoff_profile_certificate.py#L116).

Executing only those isolated serialization functions on the exact singleton
`2500000000001/2500000000000 = 1.0000000000004` yields
`["1.00000000000","1.00000000000"]` in both implementations.
The saved interval excludes the input. Therefore outward internal arithmetic
does not by itself make the serialized decimal endpoints outward enclosures.
In particular, TPC267's [caption](../../papers/tpc-267-literal-v59-residual-radius-census/paper/main.tex#L202)
should not be interpreted as preservation of the full internal rational
endpoints in JSON. Originals and saved strings remain unchanged.

Exact comparisons also show that the saved `rho_upper` squared lies below
the saved upper endpoint of `rho_squared_interval` in 6/12 TPC267 rows,
8/16 TPC268 rows, and 6/12 TPC269 rows. For example, the TPC269 central
theta=24/25 display `0.2495257250` has square less than the saved squared
upper endpoint `0.0622630874560`, by exactly `30759/1600000000000000`.
These are inconsistencies with treating both saved numbers as an exact
upper-endpoint/square-root pair, not proof that the physical value lies
outside either number. Square-root displays were not used to re-prove a
physical threshold.

A read-only fraction census of the saved squared intervals does reproduce:

| Saved result | Rows below 1/16 | Rows above 1/16 | Saved residual sign census |
|---|---:|---:|---|
| TPC267 | 12 | 0 | 10 negative, 2 positive |
| TPC268 | 10 | 6 | 14 negative, 2 positive |
| TPC269 | 8 | 4 | 12 negative |

All saved radius-square lower endpoints are positive. These statements
concern stored strings only. The logarithm guards, accumulated decimal
Euler-product rounding error, true-real containment, independent floating
replay, and the original claim-bearing interval computations were not
revalidated. TPC267's [guard constant](../../papers/tpc-267-literal-v59-residual-radius-census/code/tpc267_literal_residual_radius_certificate.py#L32)
is 10^-25 as stated in the manuscript; its
[nearby logarithm comment](../../papers/tpc-267-literal-v59-residual-radius-census/code/tpc267_literal_residual_radius_certificate.py#L199)
still says 10^-70. That stale comment is not the executed constant.

## TPC267–268: projection, cutoff, and fixed-object scope

An exact four-coordinate dot-product check gives the contrast Gram matrix
diag(4,2,2); repeating each coordinate B times gives diag(4B,2B,2B).
All three contrasts are orthogonal to (1,1,1,1), so removing them does not
remove the block mean. TPC267's
[proof-package wording](../../papers/tpc-267-literal-v59-residual-radius-census/PROOF_PACKAGE.md#L11)
says “four block contrasts” where the formulas and implementation use three
contrasts over four blocks. Its literal `qquad` at
[TeX line 87](../../papers/tpc-267-literal-v59-residual-radius-census/paper/main.tex#L87)
is preserved. The real even kernels make the saved phase labels real signs;
absolute normalized correlation is not merely the argument of a complex scalar.

TPC268's actual [beta loop](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py#L190)
uses `U=max{d:d^400≤N^133}`. Its
[metadata expression](../../papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py#L335)
instead maximizes k under `(k+1)^400≤N^133`, recording U−1. All sixteen
saved rows exhibit this off-by-one metadata error:

| N | Actual divisor cutoff from the inequality | Saved TPC268 cutoff |
|---|---:|---:|
| 64 | 3 | 2 |
| 96 | 4 | 3 |
| 128 | 5 | 4 |
| 192 | 5 | 4 |
| 256 | 6 | 5 |
| 384 | 7 | 6 |

TPC267's saved cutoff metadata agrees with the same inequality in all twelve
rows. The six matched TPC267/TPC268 z=2 controls agree exactly in saved
output-block summaries, output squared norm, residual scalar interval,
radius-square interval, and squared-correlation interval. The metadata error
does not establish a beta/output mismatch; the source computation and its
recorded label must be kept separate.

## TPC269: affine transfer is not affine correlation

The three printed central squared intervals at theta=9/10,24/25,1 agree
exactly with the saved strings. Their threshold separation is a finite
endpoint comparison, subject to the serialization limitation above.
The [cutoff implementation](../../papers/tpc-269-growing-cutoff-profile-transfer/code/tpc269_growing_cutoff_profile_certificate.py#L38)
has only six registered scales, all of which agree with a separate
high-precision natural-log evaluation. Cutoffs 3 and 4 involve the same
set of small primes, explaining the repeated central TPC268 z=3 and
TPC269 z=4 base values without identifying either with an asymptotic cutoff.

For a generic exact illustration of non-monotonicity, use w=(1,0) and the
nonzero affine output v(theta)=(1−2theta,1). Its squared normalized
correlation is `(1−2theta)^2/((1−2theta)^2+1)`, taking values
1/2,0,1/2 at theta=0,1/2,1. This is not a literal V59 example. A statement
about an intermediate real crossing of a quotient must keep track of
nonvanishing denominators; affine identities alone are not a sampled
certificate for the whole continuum. The source correctly makes no general
monotonicity claim. Its “same physical operator” wording describes a shared
construction, not an unchanged matrix along the varying-kernel path.

## Supplemental locks and continuation

All inspected supplemental files equal the source-commit bytes:

| Artifact | SHA-256 |
|---|---|
| TPC266 inspected descriptor code | `d4bc0d243aa926d229eed6b53d9765e8eaf0b531b877dc953b9daf822da585f6` |
| TPC267 saved result | `adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9` |
| TPC267 inspected producer | `d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750` |
| TPC268 saved result | `19b629425c4e64ec3e9638bb8e9f5baee304a7340d764fb32dfa2c31d49c907d` |
| TPC268 inspected producer | `e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3` |
| TPC269 saved result | `67dcce57acbb025e2af4cfe7920e16e9db4f7fb4046fe6d397a8aa7573d052ac` |
| TPC269 inspected producer | `4a173db746f13172c34845e37351fd003b253442aa983c95a7d695e0856d22c9` |

This batch raises mechanical full-source coverage from 149 to 154 and
reduces partial/notes entries from 673 to 668. The contiguous converted
range is TPC265–418, with 8,339 mechanically preserved math nodes.
Across all 823 entries, `reliable-full-md=0` and
`source-inaccessible=1` remain unchanged.

Bounded prerequisite checks and mechanical roundtrips are not independent
full-content mathematical verification. No original theorem, certificate,
claim grade, or TPC418 STOP condition is changed; no new paper number is
created and no source-repair authority is inferred from this maintenance.
