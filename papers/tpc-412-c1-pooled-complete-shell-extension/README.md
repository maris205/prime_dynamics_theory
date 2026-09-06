# TPC-412: Pooled complete-shell extension

TPC-412 extends the TPC-411 pooled two-shell profile from `H=66` to
`H=16,32,66,128`, always with `N=4H`.  The two complete shells contain
`5709+10749=16458` primes; shell-local amplitudes are retained and pooled
alternating CRT has `m_minus=m_plus=8229`.

The exact rational certificate, fresh-sieve literal replay of every mask, and
11 mutation tests pass.  The observed `z` values are respectively
`0.021785036050694`, `0.010809175951931`, `0.005216872683870`, and
`0.002683946067759`; these are finite numerical observations.

Status: `PROVED_EXACT_FINITE_POOLED_COMPLETE_SHELL_EXTENSION`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.
This remains one synthetic adjacent normalized proxy entry, with full
operator, physical `h_0`, arithmetic sign/`L2`, Route-B and twin-prime claims
open or none.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc412_c1_pooled_complete_shell_extension.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc412_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc412_adversarial_certificate_stress.py --check

The next scoped question is `TEST_C1_POOLED_COMPLETE_SHELL_EXTENSION`.
