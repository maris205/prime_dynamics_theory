# TPC-272 proof package

## Theorem 1: conditional correlation-margin budget

Let `E0=5/3`, `E*=1997/1200`, and let `C(x)` and `R(x)` be nonzero residual
scalar and radius quantities with `m(x)=|C(x)|/R(x)`.  If `eta>=0` and

```text
|C(x)| <= A x^(E0-sigma+epsilon),
m(x) >= b x^(-eta-epsilon)
```

for fixed `A,b>0`, then

```text
|C(x)|+R(x) <= A(1+b^(-1)) x^(E0-sigma+eta+2epsilon).
```

Consequently any strict inequality `sigma-eta>1/400` gives a conditional
endpoint exponent below `E*` after choosing epsilon sufficiently small.

### Proof

The definition of `m` gives `R=|C|/m`.  Insert the two displayed bounds:

```text
R <= A b^(-1) x^(E0-sigma+eta+2 epsilon).
```

The same scalar bound is no larger than the right-hand side after increasing
the constant for `x>=1` and `eta+epsilon>=0`; alternatively retain the two
terms separately.  Adding them gives the asserted constant.  Since
`E0-E*=1/400`, the exponent is strictly below `E*` exactly when
`sigma-eta>1/400`, with epsilon chosen below the strict gap.  This is a
conditional theorem: neither hypothesis is proved for the growing V59 object
in this paper.

## Theorem 2: sharp sign-only obstruction

For every `W,G>0` and `0<m<=1`, the two-dimensional vectors

```text
w=(sqrt(W),0),
g=sqrt(G)*(-m,sqrt(1-m^2))
```

have negative scalar phase and correlation margin exactly `m`.  Therefore no
positive lower bound for `m` follows from the phase sign and the two norms.

### Proof

Direct multiplication gives `C=-sqrt(WG)m`; the two squared norms are `W`
and `G`, so `R=sqrt(WG)` and `|C|/R=m`.  Every displayed quantity is defined
for `m>0`, and the phase is strictly negative.  The parameter is arbitrary,
so the margin can approach zero.

## Theorem 3: finite rational certificate

On the nine TPC-271 rows the stored `m^6` intervals are outward rational
images of the parent `Xi_C` and `Xi` intervals.  All phase labels remain
`NEGATIVE_REAL_AXIS`.  The `96->192` interval lies below `(1/32)^6`, while
the `192->384` interval lies above `4^6`; all four dyadic records preserve the
phase sign.

This theorem is `NUMERICALLY_CERTIFIED` on the registered finite data.  It is
not a statement about a growing sequence.

## Status

```text
CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL
SIGN_ONLY_CONVERSE = PROVED_EXACT
FINITE_MARGIN_AUDIT = NUMERICALLY_CERTIFIED
SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC
FIXED_POWER_CREDIT = 0
ARITHMETIC_L2 = NONE
FULL_GATE_B = OPEN
```
