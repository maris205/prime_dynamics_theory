# TPC-265: Schur Radius to Endpoint-Budget Compiler

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
```

TPC-264 gave the exact feasible set of the residual left by TPC-263.  TPC-265
now compiles that geometry into the endpoint ledger.  If the projected center
is `c` and the Schur residual has radius `R`, then

```text
sup |c+z| = |c|+R       (|z|<=R),
inf |c+z| = max(|c|-R,0).
```

The upper equality is sharp, so norm-only residual information supplies no
automatic cancellation credit.  Combining the two lanes with
`E0=5/3`, `E*=1997/1200` gives the exact strict payment condition
`delta-lambda>1/400` for each lane.  Fixed logarithmic suppression remains
zero fixed-power credit.

This is a budget interface theorem, not an arithmetic estimate for the actual
V59 residual.  It identifies the two valid next routes: prove a literal
residual-radius saving, or prove a signed phase/cross-Gram restriction strong
enough to replace the disk envelope.

## Claim firewall

```text
TPC265_MAXIMUM_CLAIM = PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
TPC265_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_RADIUS_BUDGET_COMPILER
TPC265_SCHUR_RADIAL_ENVELOPE = PROVED_EXACT
TPC265_DISK_WORST_CASE = PROVED_EXACT
TPC265_CIRCLE_WORST_CASE = PROVED_EXACT
TPC265_TWO_LANE_ENDPOINT_COMPILER = PROVED_EXACT_CONDITIONAL
TPC265_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC265_LOG_CENTER_CREDIT = 0
TPC265_LOG_RADIUS_CREDIT = 0
TPC265_ACTUAL_V59_RADIUS = OPEN
TPC265_ACTUAL_V59_PHASE = OPEN
TPC265_FIXED_POWER_CREDIT = 0
TPC265_ARITHMETIC_ADVANCE = NO
TPC265_L2 = NONE
TPC265_FULL_GATE_B = OPEN
TPC265_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC265_TWIN_PRIME_RESULT = NONE
TPC265_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC265_STATUS = PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
TPC265_ROUND2_CLUE = TEST_LITERAL_RESIDUAL_RADIUS_OR_PHASE_AGAINST_THE_TWO_LANE_BUDGET
```

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-265-schur-endpoint-budget-compiler/code/tpc265_endpoint_budget_certificate.py --check
python -O -B papers/tpc-265-schur-endpoint-budget-compiler/code/tpc265_endpoint_budget_certificate.py --check
python -B papers/tpc-265-schur-endpoint-budget-compiler/experiments/tpc265_independent_checker.py --check
python -O -B papers/tpc-265-schur-endpoint-budget-compiler/experiments/tpc265_independent_checker.py --check
python -B papers/tpc-265-schur-endpoint-budget-compiler/experiments/tpc265_budget_stress.py --check
python -O -B papers/tpc-265-schur-endpoint-budget-compiler/experiments/tpc265_budget_stress.py --check
```

The required project layout is present, including `paper/paper.pdf`.
