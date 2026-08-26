# TPC-258: Source-Frozen Transverse Null Direction

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT
```

TPC-257 found a same-order two-dimensional floor in the descendant Haar plane
`span(z1,z2)`.  TPC-258 uses only the limiting curvature constants, not any
observed coefficient, to define

```text
L1=log(3456/3125), L2=log(884736/823543),
z_null=(L2 z1-L1 z2)/sqrt(L1^2+L2^2).
```

The vector is exactly unit and orthogonal to the old midpoint.  Because
`kappa1=L1/2` and `kappa2=L2/2`, the explicit TPC-257 diagonal vector cancels:

```text
<z_null,A_x beta>=o(x^(7/6)/log^3(x)).
```

This is a real new cancellation theorem for a finite, source-frozen
projection.  If the inherited `O(1/log x)` scalar rate is reopened, the same
algebra gives a conditional `O(x^(7/6)/log^4 x+x^(55/48+epsilon))` bound.  The
released unconditional claim deliberately stops at `o(1)` and does not claim
a fixed-power saving.

## Project structure and reproduction

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
python -B papers/tpc-258-source-frozen-transverse-null-direction/code/tpc258_null_certificate.py --check
python -O -B papers/tpc-258-source-frozen-transverse-null-direction/code/tpc258_null_certificate.py --check
python -B papers/tpc-258-source-frozen-transverse-null-direction/experiments/tpc258_independent_checker.py --check
python -O -B papers/tpc-258-source-frozen-transverse-null-direction/experiments/tpc258_independent_checker.py --check
python -B papers/tpc-258-source-frozen-transverse-null-direction/experiments/tpc258_null_stress.py --check
```

The finite programs verify exact frame geometry, the formal logarithmic
cancellation, source provenance, and the adversarial rate firewall.  Finite
beta evaluations are labelled `NUMERICAL_OBSERVATION` and carry no proof
credit.

## Claim firewall

```text
TPC258_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_NULL
TPC258_ARITHMETIC_ADVANCE = YES_SCOPED_LOG_CANCELLATION
TPC258_NULL_DIRECTION = PROVED_SOURCE_FROZEN_UNIT_VECTOR
TPC258_LEADING_DIAGONAL_CANCELLATION = PROVED_SOURCE_BACKED
TPC258_RATE_REFINEMENT = CONDITIONAL_THEOREM_LOG_ONE_OVER_X
TPC258_FIXED_POWER_SAVING = NONE
TPC258_L2 = NONE
TPC258_FULL_GATE_B = OPEN
TPC258_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC258_FIXED_ATOM_CREDIT = 0
TPC258_TWIN_PRIME_RESULT = NONE
```

## Batch handoff fields

```text
STRONGEST_POSITIVE_RESULT = A_SOURCE_FROZEN_UNIT_VECTOR_IN_THE_TRANSVERSE_HAAR_PLANE_CANCELS_THE_EXPLICIT_TPC257_BQ_DIAGONAL_MAIN
STRONGEST_OBSTRUCTION = THE_UNCONDITIONAL_RESULT_IS_ONLY_o_ONE_AND_DOES_NOT_IMPLY_A_FIXED_POWER_SAVING_WITHOUT_A_RATE_INTERFACE
OPEN_THEOREM = COUPLE_THE_NULL_DIRECTION_TO_THE_LITERAL_SIGNED_W_LANE_OR_PROVE_A_COLLECTIVE_UPPER_BOUND_FOR_THE_REMAINDER
REUSABLE_STRUCTURE = CURVATURE_VECTOR_TO_EXACT_ORTHONORMAL_FRAME_TO_FIXED_NULL_COMBINATION_TO_BOUNDARY_GAP_TO_RATE_FIREWALL
ROUND2_CLUE = TEST_THE_SOURCE_FROZEN_NULL_DIRECTION_AGAINST_THE_LITERAL_SIGNED_W_BETA_COUPLING_ON_THE_SAME_CLOCK_BEFORE_ANY_FULL_REASSEMBLY
```

The Session-specific evaluator files named in the planning note are not in
this checkout; `notes/route_evaluation.md` records the local fallback review.
