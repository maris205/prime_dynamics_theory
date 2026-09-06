# TPC-416: Four-shell odd pooled extension

TPC-416 adds the complete shell at `Q=524288` to the three-shell pooled
profile.  The four shells contain `5709`, `10749`, `20390`, and `38635` primes,
for `75483` total.  At `H=66,N=264`, shell-local amplitudes and pooled
alternating CRT give the explicit odd counts `m_minus=37741,m_plus=37742`.

The exact rational certificate, fresh-sieve literal replay of every mask, and
10 mutation tests pass.  This is a finite synthetic adjacent normalized proxy
entry; full operator, physical `h_0`, arithmetic sign/`L2`, fixed-power,
Route-B, and twin-prime claims remain open or none.

Status: `PROVED_EXACT_FINITE_FOUR_SHELL_ODD_POOLED_EXTENSION`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc416_c1_four_shell_odd_pooled_extension.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc416_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc416_adversarial_certificate_stress.py --check
