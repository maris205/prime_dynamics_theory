# TPC-409: Odd complete-shell height ladder

TPC-409 fixes the odd complete shell `Q=65536`, containing all `5709` primes
in `65536<p<=131072`, and tests the four heights `H=16,32,66,128` with
`N=4H`. Every prime is retained. The explicit alternating index profile has
`m_minus=2854` and `m_plus=2855`, so the proof does not silently assume an
even shell cardinality.

For each row the exact local proxy obeys

    0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.

The exact rational certificate, independent literal CRT replay, and nine
mutation tests pass. Decimal values are finite observations only. The result
is one synthetic adjacent normalized proxy entry, not a full operator,
physical `h_0`, arithmetic sign/`L2`, fixed-power, Route-B, or twin-prime
theorem.

Status: `PROVED_EXACT_FINITE_ODD_COMPLETE_SHELL_HEIGHT_LADDER`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc409_c1_odd_complete_shell_height_ladder.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc409_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc409_adversarial_certificate_stress.py --check

The next scoped question is `TEST_C1_ODD_COMPLETE_SHELL_HEIGHT_EXTENSION`.
