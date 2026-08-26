# TPC-257: Four-Block Haar Lift and a Transverse Norm Floor

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT
```

TPC-257 keeps the literal V59 twin-prime object and splits the two ordered-rank
children used by TPC-256 into four consecutive coordinate blocks.  The global
midpoint contrast `z0` and the two within-child contrasts `z1,z2` are chosen
before looking at any coefficient.  They form an exact orthonormal family.

For

```text
kappa0=log(32/27)/sqrt(2),
kappa1=log(3456/3125)/2,
kappa2=log(884736/823543)/2,
```

the same divisor-density cancellation, second-order PNT curvature, and
TPC-255 diagonal/boundary compiler give, in `C`,

```text
<zi,A_x beta>=-(9/2 kappa_i+o(1)) x^(7/6)/log^3(x),  i=0,1,2.
```

Consequently, for `Z=span(z0,z1,z2)` and the transverse plane
`T=span(z1,z2)`,

```text
||P_Z A_x beta||_2
 =((9/2)sqrt(kappa0^2+kappa1^2+kappa2^2)+o(1))x^(7/6)/log^3(x),

||P_T A_x beta||_2
 =((9/2)sqrt(kappa1^2+kappa2^2)+o(1))x^(7/6)/log^3(x).
```

The numerical factors before `9/2` are approximately `0.135096662713318`
and `0.061792126717520`.  The second display is a genuine same-order lower
floor for the component transverse to the TPC-256 midpoint.

This is an obstruction/lower-bound paper.  It is not an upper `L2` estimate,
not a full-output theorem, and not full Gate B.  The strict global `1/400`
budget, fixed-atom credit, and any twin-prime conclusion remain unpaid or
absent.

## Files and reproduction

Required project structure is present:

```text
README.md
paper/paper.pdf
code/
experiments/
results/
notes/
```

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-257-four-block-haar-transverse-norm-floor/code/tpc257_four_block_haar_certificate.py --check
python -O -B papers/tpc-257-four-block-haar-transverse-norm-floor/code/tpc257_four_block_haar_certificate.py --check
python -B papers/tpc-257-four-block-haar-transverse-norm-floor/experiments/tpc257_independent_checker.py --check
python -O -B papers/tpc-257-four-block-haar-transverse-norm-floor/experiments/tpc257_independent_checker.py --check
python -B papers/tpc-257-four-block-haar-transverse-norm-floor/experiments/tpc257_four_block_haar_stress.py --check
```

The finite programs verify rational rank/block geometry, orthonormality,
zero-extension variation, divisor endpoint cancellation, the three exact
logarithmic curvature identities, and the exponent ledger.  Finite beta
values are explicitly labelled `NUMERICAL_OBSERVATION`; they do not prove the
asymptotic theorem.

## Claim firewall

```text
TPC257_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT
TPC257_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_HAAR
TPC257_ARITHMETIC_ADVANCE = YES_SCOPED_TRANSVERSE_LOWER_FLOOR
TPC257_THREE_MODE_HAAR_ORTHOGONALITY = PROVED_EXACT
TPC257_BETA_CONTRASTS = PROVED_SOURCE_BACKED
TPC257_BOUNDED_VARIATION_ADJOINT = PROVED_SOURCE_BACKED
TPC257_TRANSVERSE_OUTPUT_FLOOR = PROVED_SOURCE_BACKED
TPC257_FULL_OUTPUT_NORM_FLOOR = PROVED_SOURCE_BACKED
TPC257_L2 = NONE
TPC257_FIXED_ATOM_CREDIT = 0
TPC257_FULL_GATE_B = OPEN
TPC257_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC257_TWIN_PRIME_RESULT = NONE
TPC257_STATUS = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR
```

`FULL_OUTPUT_NORM_FLOOR` means a lower bound for a finite projection, not a
claim of an upper bound for the full vector.  The result cannot be promoted to
arithmetic `L2` control or Gate B.

## Batch handoff fields

```text
STRONGEST_POSITIVE_RESULT = THE_SOURCE_ONLY_TWO_DIMENSIONAL_TRANSVERSE_HAAR_PLANE_HAS_AN_EXPLICIT_SAME_ORDER_LITERAL_ADJOINT_LOWER_FLOOR
STRONGEST_OBSTRUCTION = THE_TRANSVERSE_COMPONENT_CANNOT_BE_ASSUMED_LOWER_ORDER_AFTER_ONE_MIDPOINT_PROJECTION
OPEN_THEOREM = FIND_AND_CERTIFY_A_SOURCE_FROZEN_TRANSVERSE_NULL_DIRECTION_OR_PROVE_A_COLLECTIVE_UPPER_BOUND_WITH_ALL_LITERAL_MASKS_AND_BOUNDARIES_RETAINED
REUSABLE_STRUCTURE = FOUR_BLOCK_RANK_HAAR_FRAME_TO_EXACT_ORTHONORMALITY_TO_SECOND_ORDER_LI_CURVATURE_TABLE_TO_BQ_DIAGONAL_TO_BOUNDED_VARIATION_BOUNDARY_COMPILER_TO_PARSEVAL_FLOOR
ROUND2_CLUE = USE_THE_EXPLICIT_TWO_DIMENSIONAL_TRANSVERSE_HAAR_FLOOR_TO_SEARCH_FOR_A_SOURCE_FROZEN_DIAGONAL_NULL_DIRECTION_BEFORE_ATTEMPTING_ANY_FULL_GATE_B_UPPER_BOUND
```

The Route-B evaluator is recorded in `notes/route_evaluation.md`.  The
repository does not contain the separately named Session evaluator files, so
the available proof package, theorem ledger, bridge checker, and `AGENTS.md`
are the applied fail-closed authorities.
