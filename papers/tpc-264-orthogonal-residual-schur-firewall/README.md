# TPC-264: Orthogonal-Residual Schur Firewall

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
```

TPC-263 paid the rank-three projected channel but left the exact residual
`C_perp`.  TPC-264 computes the missing finite-dimensional information exactly.
For `p=P_3w`, `q=P_3g_x`, residual norms
`a=||(I-P_3)w||`, `b=||(I-P_3)g_x||`, and `c=<p,q>`, the residual Gram entry
`z=< (I-P_3)w,(I-P_3)g_x >` has the following sharp feasible set:

```text
|z| <= ab       if dim ker(P_3) >= 2,
|z| =  ab       if dim ker(P_3) = 1 and ab>0,
z = 0           if dim ker(P_3) = 0 or ab=0.
```

Thus the full scalar is a disk centered at `c` in the two-dimensional
complement case, a circle in the one-dimensional case, or a singleton.  This
is an exact Schur-complement theorem and a genuine new obstruction: controlling
the rank-three channel does not identify the orthogonal residual.

The endpoint-scale witness takes `a=b=x^(5/6)`, so its feasible radius is
`x^(5/3)`.  That scale is explicitly a synthetic modeling choice.  It is not a
literal growing prime-shell counterexample and it does not claim arithmetic
progress.

## Claim firewall

```text
TPC264_MAXIMUM_CLAIM = PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
TPC264_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_SCHUR_FIREWALL
TPC264_PROJECTION_DATA = PROVED_EXACT
TPC264_RESIDUAL_GRAM_FEASIBLE_SET = PROVED_EXACT
TPC264_COMPLEMENT_DIMENSION_SPLIT = PROVED_EXACT
TPC264_FULL_SCALAR_FEASIBLE_SET = PROVED_EXACT
TPC264_ENDPOINT_SCALE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL
TPC264_FIXED_POWER_CREDIT = 0
TPC264_ARITHMETIC_ADVANCE = NO
TPC264_ACTUAL_V59_RESIDUAL = OPEN
TPC264_L2 = NONE
TPC264_FULL_GATE_B = OPEN
TPC264_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC264_TWIN_PRIME_RESULT = NONE
TPC264_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC264_STATUS = PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
TPC264_ROUND2_CLUE = TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE_INTO_A_LITERAL_V59_ESTIMATE
```

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-264-orthogonal-residual-schur-firewall/code/tpc264_schur_firewall_certificate.py --check
python -O -B papers/tpc-264-orthogonal-residual-schur-firewall/code/tpc264_schur_firewall_certificate.py --check
python -B papers/tpc-264-orthogonal-residual-schur-firewall/experiments/tpc264_independent_checker.py --check
python -O -B papers/tpc-264-orthogonal-residual-schur-firewall/experiments/tpc264_independent_checker.py --check
python -B papers/tpc-264-orthogonal-residual-schur-firewall/experiments/tpc264_schur_stress.py --check
python -O -B papers/tpc-264-orthogonal-residual-schur-firewall/experiments/tpc264_schur_stress.py --check
```

The project contains the required `README.md`, `paper/`, `code/`,
`experiments/`, `results/`, and `notes/` directories, including
`paper/paper.pdf`.
