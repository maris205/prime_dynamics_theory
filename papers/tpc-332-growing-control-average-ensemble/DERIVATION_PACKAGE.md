# TPC-332 derivation package

## 1. Finite control-orbit identity

Let `P_1,...,P_m` be the five permutation matrices, `w_j=P_jv`,
`vbar=m^(-1) sum_j w_j`, and `z_j=w_j-vbar`.  Then `sum_j z_j=0`.  For any
real matrix `A`,

```text
q_A(x)=||Ax||_2^2 = x^T A^T A x
```

satisfies

```text
mean_j q_A(w_j) = q_A(vbar) + mean_j q_A(z_j).
```

Indeed, expand `q_A(vbar+z_j)`.  The cross term is
`2 vbar^T A^T A mean_j(z_j)`, hence vanishes.  This is an exact finite
identity and uses no arithmetic estimate.

## 2. Three signed-Gram forms

For a coherent shell matrix `C_e`, define

```text
E_e(x) = ||C_e x||_2^2
D_e(x) = sum_t x_t^2 sum_u C_e(u,t)^2
O_e(x) = E_e(x)-D_e(x).
```

The identity in §1 applies to `E_e` and to the diagonal form `D_e`; subtraction
gives the identity for `O_e`.  Ratios are formed after the quadratic values
are computed.  No ratio is averaged.

## 3. Source polarization ledger

The declared source vectors are midpoint evaluations of

```text
beta(t) = Lambda(t+2)-b^(2)(t).
```

For every finite window, ordinary inner-product expansion gives

```text
||beta||_2^2 = ||Lambda||_2^2 + ||b^(2)||_2^2
               - 2 <Lambda,b^(2)>.
```

The producer records all four scalar terms and the residual identity error.
Because the finite model has nonnegative `Lambda` and `b^(2)`, the cross term
is nonnegative in this declared model.  This observation is not promoted to a
prime-pair asymptotic statement.

## 4. Nested source windows

For each origin, scales `2048,4096,8192` form nested intervals.  The source
quantities do not depend on `Q` or the kernel power, so the certificate checks
that the eight operator rows attached to each window reproduce the same source
ledger.  Adjacent residual-energy ratios and their base-2 logarithms are
descriptive finite statistics only.

## 5. Numerical enclosure

The Euler product is truncated at `50000`, with the inherited positive tail
multiplier; logarithms use 100-digit Decimal midpoints and a rational
`10^(-70)` guard.  Matrix responses use float64.  A ratio is classified as
negative only when its outward `5e-8` interval lies below one, positive only
when it lies above one, and unresolved otherwise.

## 6. Exact anchor

At `[44001,44016]`, `Q=4`, shell `{5,7}`, and `s=1`, the source is replaced by
the exact rational vector
`1_(t+2 is prime)-1_(t is odd)`.  The literal matrix, five placements, mean,
and centered vectors are evaluated with `Fraction` arithmetic.  The identity,
control-average, coherent, and centered triples are stored through
reduced-fraction digests.
