# TPC-287 — Prime-shell cancellation depth

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The physical attachment is exactly additive over prime-shell components.  On a
declared ladder containing exactly 1 through 7 primes, all 336 component
intervals are separated from zero; 57 of 84 shell rows contain mixed signs,
and the certified shell-to-unsigned-mass retention upper bound is below
`1/2` in 31 rows, below `1/4` in 22 rows, and below `1/10` in 8 rows.

## What advances

- proves the finite prime-by-prime attachment decomposition after TPC-286's
  diagonal split;
- replaces the old atlas's mostly two-term cancellation picture with a
  declared cardinality ladder reaching seven simultaneous prime components;
- records a conservative interval envelope for signed cancellation rather than
  treating a small resultant as proof of asymptotic savings;
- identifies leave-one-prime-out sensitivity: 48 omission events reverse the
  certified shell sign and 12 single-prime rows collapse to zero;
- makes the next gap precise: cancellation depth must be tested under growing
  shells and source controls before it can feed an arithmetic $L^2$ estimate.

## Claim ceiling

```text
PROVED_EXACT = C_shell = sum_q C_q for every finite shell and linear attachment
NUMERICALLY_CERTIFIED_FINITE = 84 shell rows with cardinalities 1,...,7
NUMERICALLY_CERTIFIED_FINITE = 336/336 component intervals sign-separated
NUMERICALLY_CERTIFIED_FINITE = 57 mixed-sign shell rows
NUMERICALLY_CERTIFIED_FINITE = retention upper < 1/2, 1/4, 1/10 in 31/22/8 rows
NUMERICALLY_CERTIFIED_FINITE = 48 leave-one-prime-out sign flips and 12 zero remainders
MODELING_CHOICE = declared shell-cardinality ladder, not an admissible growing family
OPEN = growing-shell cancellation stability
OPEN = literal arithmetic L2 and fixed-power credit
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite retention envelope is a diagnostic: it is bounded using interval
lower and upper masses and is not a statement about a limiting proportion of
the shell sum.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc287_prime_shell_cancellation_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc287_prime_shell_cancellation_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc287_prime_shell_cancellation_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc287_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc287_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc287_cancellation_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The certificate locks
TPC-286 and the frozen TPC-268 engine.  The Session evaluator files named in
the wider workflow are absent from this checkout; `notes/route_evaluation.md`
records the fail-closed local Route-B fallback.
