# TPC-408: Complete-shell C1 Q-scale extension

TPC-408 extends the TPC-407 complete-shell ladder to the next two scales,
`Q=65536` and `Q=131072`. The complete shells contain `5709` and `10749`
primes. Unlike TPC-407, the odd shell cardinalities are not discarded: the
explicit alternating index profile uses `m_minus=floor(r/2)` odd-index terms
and `m_plus=ceil(r/2)` even-index terms.

At fixed `H=66`, `N=264`, and origin lower bound `10^6`, the exact local
proxy entry satisfies

    0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.

The rational certificate, independent literal CRT replay, and nine mutation
tests all pass. Decimal values are finite float64 observations only. The
result remains one synthetic adjacent normalized proxy entry; full operator
norm, physical `h_0`, arithmetic sign/`L2`, fixed-power credit, Route B, and
twin-prime claims remain open or none.

Status: `PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_EXTENSION`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc408_c1_complete_shell_q_scale_extension.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc408_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc408_adversarial_certificate_stress.py --check

The next scoped question is `TEST_C1_COMPLETE_SHELL_Q_SCALE_EXTENSION`.
