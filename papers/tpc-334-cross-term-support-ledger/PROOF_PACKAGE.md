# TPC-334 proof and scope package

## Proposition 1 — finite support partition

For the declared source model, every nonzero summand of
`<Lambda,b> = sum_t Lambda(t+2)b(t)` belongs to exactly one of
`twin_prime`, `non_twin_prime_shift`, or `prime_power_shift`.

**Proof.**  The comparison factor contains `1_{2 not divide t}`, so an even
`t` contributes zero.  The von Mangoldt factor is nonzero only when
`t+2=p^k`.  If `k=1`, primality of `t` gives the twin class and failure of
primality gives the non-twin class.  If `k>=2`, the coordinate is in the
prime-power class.  These cases are disjoint and exhaustive; all other
coordinates have zero product. `QED`.

## Proposition 2 — additive mass identity

Writing `X_C` for the sum of the cross summands in class `C`,

```text
<Lambda,b> = X_twin + X_non_twin + X_prime_power + X_zero,
```

with `X_zero=0`.

**Proof.**  Sum the disjoint finite partition from Proposition 1. `QED`.

## Proposition 3 — certified finite obstruction

On the six declared windows, the twin fraction is below `0.10` and the
non-twin fraction is above `0.90` in every row.

**Evidence.**  The canonical producer, independent replay, and mutation
stress suite agree on all six category ledgers.  This proposition is
`NUMERICALLY_CERTIFIED_FINITE`; it is not a statement about arbitrary
origins, scales, or the twin-prime counting function.
