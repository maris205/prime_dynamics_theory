# TPC-296 proof package

## Theorem 1 — least-norm source budget

Let `A in R^(n x m)` have full column rank and let `G=A^T A`.  For every
`b in R^m`,

```text
min_{A^T h=b} ||h||_2^2 = b^T G^(-1)b,
```

with unique minimizer `h_b=A G^(-1)b`.  Consequently a budget `B>=0` admits
the target exactly when `b^T G^(-1)b<=B`.

**Proof.** Direct substitution gives `A^T h_b=b`.  Every solution is
`h_b+v` with `v in ker(A^T)`.  Since `h_b in col(A)=ker(A^T)^perp`,
Pythagoras gives `||h_b+v||^2=||h_b||^2+||v||^2`.  Finally,
`||h_b||^2=b^T G^(-1)A^T A G^(-1)b=b^T G^(-1)b`.  The budget criterion
follows from minimality. ∎

## Theorem 2 — source-cost/physical-energy tradeoff

Under the same hypotheses,

```text
(b^T G^(-1)b)(b^T G b) >= (b^T b)^2.
```

**Proof.** Apply Cauchy--Schwarz to `G^(-1/2)b` and `G^(1/2)b`; their inner
product is `b^T b`. ∎

## Proposition 3 — one-ray residual

For nonzero `v` and target `b`,

```text
min_alpha ||alpha v-b||_2^2
 = ||b||_2^2 - (v^T b)^2/||v||_2^2.
```

**Proof.** Complete the square in the scalar quadratic
`alpha^2||v||^2-2 alpha v^T b+||b||^2`. ∎

## Finite certificate consequence

The TPC-295 modular certificates make the hypotheses valid on all 18 rows.
The high-precision atlas then observes:

```text
weighted minimizer tau(b)<1e-3 = 18 / 18
weighted minimizer one-ray RMS>=0.9 = 18 / 18
source-energy tradeoff failures = 0 / 54 target evaluations
```

These inequalities are finite numerical observations under declared
normalizations, not an arithmetic or asymptotic theorem.
