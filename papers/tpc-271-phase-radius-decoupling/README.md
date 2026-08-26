# TPC-271 — Phase–Radius Decoupling in a Finite V59 Residual

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
```

TPC-270 found a strong finite variation in the endpoint-normalized radius.
TPC-271 records the signed residual scalar and the two residual norm lanes in
the same finite interface. It proves the exact finite coordinates

```text
Xi=Xi_W*Xi_G; Xi/Xi_C=|kappa|^(-6)
```

and certifies that all six base rows and all three profile controls have
negative-real-axis scalar phase. At the same time, the dyadic normalized-radius
pattern is `DROP_RISE_RISE_DROP`; the `96->192` radius ratio is above `23` while
the source lane falls below `1/8` and the output lane rises above `230`.

This is a finite phase–radius decoupling and lane-attribution audit. It does not
prove an asymptotic phase theorem, a radius bound, statistical independence,
arithmetic `L2`, full Gate B, or the twin-prime conjecture.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-271-phase-radius-decoupling/code/tpc271_phase_radius_decoupling_certificate.py --check
python -O -B papers/tpc-271-phase-radius-decoupling/code/tpc271_phase_radius_decoupling_certificate.py --check
python -B papers/tpc-271-phase-radius-decoupling/experiments/tpc271_independent_checker.py --check
python -O -B papers/tpc-271-phase-radius-decoupling/experiments/tpc271_independent_checker.py --check
python -B papers/tpc-271-phase-radius-decoupling/experiments/tpc271_phase_radius_stress.py --check
python -O -B papers/tpc-271-phase-radius-decoupling/experiments/tpc271_phase_radius_stress.py --check
```

The required paper layout is present, including `paper/paper.pdf`.

## Claim firewall

```text
TPC271_LANE_FACTORIZATION = PROVED_EXACT_FINITE
TPC271_PHASE_SIGN_CENSUS = NUMERICALLY_CERTIFIED_FINITE
TPC271_PHASE_RADIUS_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE
TPC271_SOURCE_LANE_PROFILE_INVARIANCE = PROVED_EXACT_FINITE
TPC271_OUTPUT_LANE_SPIKE = NUMERICALLY_CERTIFIED_FINITE
TPC271_SOURCE_LEVEL_SIGNED_PHASE = OPEN_ASYMPTOTIC
TPC271_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC
TPC271_FIXED_POWER_CREDIT = 0
TPC271_ARITHMETIC_ADVANCE = NO
TPC271_L2 = NONE
TPC271_FULL_GATE_B = OPEN
TPC271_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC271_TWIN_PRIME_RESULT = NONE
TPC271_STATUS = NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_ROUND2_CLUE = TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
```
