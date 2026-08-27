# TPC-273 — Finite margin-stability matrix

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On a 32-row declared grid for the locked literal V59 finite operator, outward
intervals certify 12 rows with `m<1/8`, 11 in the middle band, and 9 with
`m>1/4`; fixed-scale cutoff-only changes cross both bands, so finite uniform
margin stability is `REFUTED_SCOPED` while growing uniformity remains open.

## Concrete progress

- proves the exact transfer `m^2=rho^2` from the parent residual;
- audits 4 scales, 4 cutoff values, and 2 kernel exponents (32 rows);
- certifies cutoff-only flips at `N=64` and `N=128`;
- records 30 negative-real and 2 positive-real phase rows instead of dropping
  the sign changes;
- provides independent upstream-engine replay, hostile mutation rejection,
  and normal/optimized reproducibility.

The finite grid is a declared interface inherited from TPC-268.  It is not the
actual growing V59 sequence, so no asymptotic counterexample or fixed-power
credit is claimed.

## Claim ceiling

```text
PROVED_EXACT_FINITE = m^2=rho^2 and m^6=(rho^2)^3
NUMERICALLY_CERTIFIED = 32-row margin and phase matrix
REFUTED_SCOPED = uniform stability of this finite parameter family
OPEN = source-level margin uniformity, arithmetic L2, full Gate B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc273_margin_stability_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc273_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc273_margin_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  Route evaluator files
named by the Session are absent in this checkout; the local fail-closed
fallback is documented in `notes/route_evaluation.md`.
