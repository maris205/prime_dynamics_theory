# TPC-273 proof and certificate package

## Lemma 1: exact finite margin transfer

On each positive parent row,
`m=|C_perp|/sqrt(W_perp G_perp)` and the parent defines
`rho^2=|C_perp|^2/(W_perp G_perp)`.  Hence `m^2=rho^2` and
`m^6=(rho^2)^3`.

**Proof.** Square the definition of `m` and substitute the definition of
`rho^2`.  Positivity of the denominator is certified by the parent interval
engine.  Cubing is monotone on the positive half-line.  ∎

## Theorem 2: finite margin-stability obstruction

On the registered 32-row grid, the outward intervals certify:

```text
margin below 1/8: 12 rows
middle band:      11 rows
margin above 1/4:  9 rows
negative phase:   30 rows
positive phase:    2 rows
```

At fixed `(N,s)=(64,1)`, changing only `z:2->5` moves the margin from the
middle band to above `1/4`.  At fixed `(N,s)=(128,1)`, changing only
`z:2->3` moves it from the middle band to below `1/8`.  The two transitions
are threshold-separated by the stored intervals.  Thus the universal
stability claim for this declared finite parameter family is
`REFUTED_SCOPED`.

## Theorem 3: finite phase census

The same grid has exactly two positive-real scalar rows, `(192,3,1)` and
`(192,4,1)`, and 30 negative-real rows.  This is a finite phase census only;
it neither supplies an eventual phase sector nor links phase sign to a
positive margin lower bound.

## Status firewall

```text
FINITE_MARGIN_MATRIX = NUMERICALLY_CERTIFIED
FINITE_STABILITY = REFUTED_SCOPED
SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC
GROWING_UNIFORMITY = OPEN_ASYMPTOTIC
FIXED_POWER_CREDIT = 0
ARITHMETIC_L2 = NONE
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
