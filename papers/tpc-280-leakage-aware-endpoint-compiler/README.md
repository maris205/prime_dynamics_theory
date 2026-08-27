# TPC-280 — An additive-leakage compiler for signed gain and endpoint budgets

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

If `D >= d X^a` and
`G <= B X^(-gamma)D + ell X^(a-delta)`, then the exact normalized bound is

`G/D <= B X^(-gamma) + (ell/d)X^(-delta)`,

so the gain has a sharp two-term lower bound and a collapsed exponent
`kappa=min(gamma,delta)`.  The same compiler gives
`eta_eff=max(0,eta_D-kappa/2)` for the inherited signed-margin lane.

The result is conditional and structural.  A slower additive leakage term
(`delta<gamma`) is an explicit bottleneck, and the equality family shows that
the two-term denominator cannot be uniformly improved from the stated inputs.
Six exact rational budget cases, four margin cases, four endpoint cases, and
the twelve TPC-279 parent rows are independently certified.

## Claim ceiling

```text
PROVED_CONDITIONAL = two-term gain, dominant-exponent, and margin compilers
NUMERICALLY_CERTIFIED_FINITE = exact fixtures plus 12-row parent transfer
REFUTED_SCOPED = treating slower additive leakage as if it had the main exponent
OPEN = literal growing source decomposition, arithmetic L2, full Gate B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc280_leakage_aware_endpoint_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc280_leakage_aware_endpoint_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc280_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc280_leakage_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The finite transfer is
coordinate bookkeeping from TPC-279 and is not an arithmetic estimate.
