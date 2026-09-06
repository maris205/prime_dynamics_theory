# TPC-414: Three-shell pooled extension

TPC-414 adds the complete shell at `Q=262144` to the TPC-411/412 pooled
profile.  The three shells contain `5709`, `10749`, and `20390` primes, for
`36848` total; at `H=66,N=264`, pooled alternating CRT has
`m_minus=m_plus=18424` and shell-local amplitudes are retained.

The exact rational certificate, fresh-sieve literal replay of every mask, and
9 mutation tests pass.  This is a finite synthetic adjacent normalized proxy
entry; full operator, physical `h_0`, arithmetic sign/`L2`, fixed-power,
Route-B, and twin-prime claims remain open or none.

Status: `PROVED_EXACT_FINITE_THREE_SHELL_POOLED_EXTENSION`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc414_c1_three_shell_pooled_extension.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc414_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc414_adversarial_certificate_stress.py --check

The next scoped question is `TEST_C1_THREE_SHELL_POOLED_EXTENSION`.
