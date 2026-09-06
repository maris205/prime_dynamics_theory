# TPC-411: Pooled odd complete shells

TPC-411 pools the full odd shells at `Q=65536` and `Q=131072`, retaining all
`5709+10749=16458` primes.  At fixed `H=66`, `N=264`, the pooled ordered
profile has `m_minus=m_plus=8229`; each amplitude uses the shell scale of its
own prime.  The exact local proxy satisfies `0<=z<=4/H`.

The rational certificate, independent literal pooled CRT replay, and nine
mutation tests pass.  This is one finite synthetic adjacent normalized proxy
entry; full operator norm, physical `h_0`, arithmetic sign/`L2`, fixed-power,
Route-B, and twin-prime claims remain open or none.

Status: `PROVED_EXACT_FINITE_POOLED_ODD_COMPLETE_SHELLS`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc411_c1_pooled_odd_complete_shells.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc411_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc411_adversarial_certificate_stress.py --check

The next scoped question is `TEST_C1_POOLED_COMPLETE_SHELL_EXTENSION`.
