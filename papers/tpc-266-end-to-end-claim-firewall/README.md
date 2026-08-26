# TPC-266: Typed End-to-End Claim Firewall for the Residual Budget Chain

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL
```

TPC-263 paid a source-backed fixed-log rank-three center channel.  TPC-264
classified the remaining orthogonal residual as a Schur disk/circle/singleton.
TPC-265 converted that geometry into the sharp radial endpoint `|c|+R` and the
strict `1/400` budget.  TPC-266 audits the entire composition with an explicit
type system and hostile six-state matrix.

The new result is an exact compositional theorem: both the center and radius
must enter as genuinely paid `POWER` or `SIGNED_PHASE` lanes with effective
saving strictly larger than `1/400`, and the residual must remain present.
`FIXED_LOG`, `MISSING`, `DELETED`, equality, and subcritical lanes are rejected
or kept open.  This closes a real interface ambiguity, but it does not provide
the missing literal V59 estimate.

## Claim firewall

```text
TPC266_MAXIMUM_CLAIM = PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL
TPC266_ROUTE_ADVANCE = YES_SCOPED_END_TO_END_CLAIM_FIREWALL
TPC266_TYPED_COMPOSITION = PROVED_EXACT
TPC266_FIXED_LOG_NONPROMOTION = PROVED_EXACT
TPC266_RESIDUAL_RETENTION_FIREWALL = PROVED_EXACT
TPC266_FAILURE_MATRIX = PROVED_EXACT_SIX_STATE
TPC266_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC266_CENTER_CURRENT_TYPE = FIXED_LOG
TPC266_RESIDUAL_CURRENT_TYPE = SCHUR_SET_RADIUS_OPEN
TPC266_ACTUAL_V59_RADIUS = OPEN
TPC266_ACTUAL_V59_PHASE = OPEN
TPC266_FIXED_POWER_CREDIT = 0
TPC266_ARITHMETIC_ADVANCE = NO
TPC266_L2 = NONE
TPC266_FULL_GATE_B = OPEN
TPC266_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC266_TWIN_PRIME_RESULT = NONE
TPC266_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC266_STATUS = PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL
TPC266_ROUND2_CLUE = PROVE_A_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400
```

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-266-end-to-end-claim-firewall/code/tpc266_end_to_end_claim_firewall.py --check
python -O -B papers/tpc-266-end-to-end-claim-firewall/code/tpc266_end_to_end_claim_firewall.py --check
python -B papers/tpc-266-end-to-end-claim-firewall/experiments/tpc266_independent_checker.py --check
python -O -B papers/tpc-266-end-to-end-claim-firewall/experiments/tpc266_independent_checker.py --check
python -B papers/tpc-266-end-to-end-claim-firewall/experiments/tpc266_hostile_matrix.py --check
python -O -B papers/tpc-266-end-to-end-claim-firewall/experiments/tpc266_hostile_matrix.py --check
```

The required project layout is present, including `paper/paper.pdf`.
