# TPC-345 — Principal-angle / Grassmann stability audit

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The two hash-locked nuisance subspaces share one strongly aligned direction
but have a nearly orthogonal second direction: the raw principal cosines are
`0.99570180102754502` and `0.079945679326165323`, while equal-row weighting
changes them to `0.91445198603192213` and `0.078708449294248611`.  The first
principal angle therefore moves from `5.3141837613` degrees to
`23.8719787000` degrees.  This is a finite, basis-invariant geometric
obstruction to treating the TPC-344 repair as a weighting-stable common law.

## Why this is a separate paper

TPC-344 tested a particular base-plus-contrast coordinate system.  TPC-345
removes that coordinate choice: it compares the column spaces themselves by
positive-SVD orthonormal bases, principal angles, and orthogonal projectors.
A fixed nonsingular shear of the nuisance coordinates leaves both projectors
and principal cosines unchanged to numerical tolerance.  The paper also
tests mutual target transfer between the two subspaces and repeats the angle
calculation for all nine leave-one-control-out fits.

The comparison is made in the protocol-aligned response space obtained by
stacking the three length-512 rows in each panel.  It is not a claim that a
finite nuisance subspace is an arithmetic invariant of all source windows.

## Frozen protocol

`text
TPC341 rows = [48097,48608], [48609,49120], [49217,49728]
TPC342 rows = [40097,40608], [40609,41120], [41121,41632]
scale       = 1024
operator    = all-plus, Q=54, exponent=1, H=66
controls    = nine fixed coordinate bijections
categories  = twin, non-twin prime shift, prime-power shift, zero
records     = 216 raw records, 171 nonempty
angle pairs = 2 main weightings + 18 leave-one-control-out pairs
`

Raw weighting stacks rows without rescaling.  Equal-row weighting divides
each row target and its nuisance columns by that row's twin-target
`L2` norm.  The rank rule is the positive-SVD threshold
`max(shape)*eps*largest_singular_value`.  The observed ranks are 3 for
TPC-341 and 2 for TPC-342; the latter loses the prime-power column because
that column is identically zero on its three rows.

## Certified finite readout

| quantity | raw | equal-row |
|---|---:|---:|
| principal cosine 1 | 0.9957018010 | 0.9144519860 |
| principal cosine 2 | 0.0799456793 | 0.0787084493 |
| principal angle 1 (degrees) | 5.3141837613 | 23.8719787000 |
| principal angle 2 (degrees) | 85.4145566103 | 85.4856687739 |
| projector Frobenius distance | 1.7333127887 | 1.8207594818 |
| TPC341 target on TPC342 basis retention | 0.2306119635 | 0.2745950088 |
| TPC342 target on TPC341 basis retention | 0.3588770900 | 0.3234520500 |

The mutual-transfer criterion requires both directions to have residual
retention below `0.30`; it fails in both declared weightings.  The raw
leave-one-control-out dominant cosine minimum is `0.9947001951`, while the
transverse cosine maximum is `0.1549751276`; the equal-row transverse maximum
is `0.1675760096`.  Thus the near-orthogonal transverse direction is not
removed by the control omission, even though the dominant alignment is
weight-sensitive.

## Claim firewall

`text
TPC345_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT
TPC345_PRINCIPAL_ANGLE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC345_BASIS_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC345_RAW_DOMINANT_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC345_TRANSVERSE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC345_WEIGHTING_STABILITY = REFUTED_SCOPED
TPC345_MUTUAL_TRANSFER = REFUTED_SCOPED
TPC345_RANK_MISMATCH = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC345_ARITHMETIC_ADVANCE = NO
TPC345_FIXED_POWER_CREDIT = 0
TPC345_SOURCE_UNIFORM_L2 = OPEN
TPC345_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC345_FULL_GATE_B = OPEN
TPC345_TWIN_PRIME_RESULT = NONE
`

The Session-named Route-A/Route-B evaluator files are absent in this
checkout.  The local Bridge-B wrapper is fail-closed and is not an official
evaluator pass.  No finite angle certificate pays an asymptotic arithmetic
loss, the strict `1/400` endpoint, or a twin-prime conclusion.

## Reproduction

`bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-345-principal-angle-grassmann-audit/code/tpc345_principal_angle_grassmann_audit.py --write
python -B papers/tpc-345-principal-angle-grassmann-audit/code/tpc345_principal_angle_grassmann_audit.py --check
python -O -B papers/tpc-345-principal-angle-grassmann-audit/code/tpc345_principal_angle_grassmann_audit.py --check
python -B papers/tpc-345-principal-angle-grassmann-audit/experiments/tpc345_independent_checker.py
python -O -B papers/tpc-345-principal-angle-grassmann-audit/experiments/tpc345_independent_checker.py
python -B papers/tpc-345-principal-angle-grassmann-audit/experiments/tpc345_geometry_stress.py
python -O -B papers/tpc-345-principal-angle-grassmann-audit/experiments/tpc345_geometry_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc345_principal_angle_grassmann_audit_checker.py --check
`

The canonical certificate is
[results/tpc345_certificate.json](results/tpc345_certificate.json), and the
audited manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next decision

The coordinate-invariant audit confirms a stable transverse mismatch and a
weight-sensitive dominant direction.  The next minimal question is a finite
no-go/freeze test for the panel-adaptive route: quantify whether adding more
panel-specific degrees of freedom yields a robust model class or only
overfits the locked panels.  This is the TPC-346 trigger.
