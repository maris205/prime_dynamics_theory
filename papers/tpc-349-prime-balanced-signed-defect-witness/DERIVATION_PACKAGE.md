# TPC-349 derivation package

## 1. Literal defect

Retain the TPC-347/TPC-348 finite object

```text
A_I = sum_p epsilon_p R_I P_p K_p P_p E_I,
T_I = R_I (sum_p epsilon_p K_p) E_I,
D_I = A_I - T_I.
```

All masks, shell signs, kernel height, exponent, and interval conventions are
locked by the parent certificate.  TPC-349 changes only the test vector.

## 2. Prime-balanced incidence vector

Let the ordered active shell be `p_0 < ... < p_(r-1)`.  Define

```text
beta_j = +1                 (j < floor(r/2)),
          0                  (floor(r/2) <= j < r-floor(r/2)),
         -1                  (j >= r-floor(r/2)).
```

The positive and negative coefficient counts are equal, so `sum beta_j=0`.
For the interval incidence vectors `h_(p_j,I)`, define

```text
b_I = sum_j beta_j h_(p_j,I),     x_I = b_I / ||b_I||_2.
```

Positions divisible by several active primes receive the algebraic sum of all
their coefficients.  Thus this is an incidence contrast, not an owner-class
partition and not a fitted eigenvector.

## 3. Exact Gram interface

Linearity gives

```text
D_I b_I = sum_j beta_j D_I h_(p_j,I).
```

Taking the Euclidean square gives the symmetric prime-incidence Gram expansion

```text
||D_I b_I||_2^2
  = sum_(j,k) beta_j beta_k
      <D_I h_(p_j,I), D_I h_(p_k,I)>.
```

This identity separates same-prime energy from cross-prime interference.  It is
exact finite algebra; it does not prescribe the sign of any cross term.

## 4. Norm interface and comparison

For any nonzero finite vector `b_I`, the induced norm gives

```text
||D_I||_(2->2) >= ||D_I (b_I/||b_I||_2)||_2.
```

The TPC-348 coordinate baseline is
`C_I=max_(t in J_I)||D_I e_t||_2`, where `J_I` is the mask-hit set.  The ratio
of the new response to `C_I` is a diagnostic comparison; it is not part of the
norm theorem and is not an asymptotic claim.

## 5. Frozen numerical interface

The declared panel has two origins, three source counts, four shell anchors,
two exponents, and four source sign laws, hence 192 rows.  The exact anchor uses
`I=[1,14]`, `Q=4`, exponent one, all-plus source signs, shell `{5,7}`, and
balanced coefficients `(1,-1)`.  Its incidence vector is

```text
(0,0,0,0,1,0,-1,0,0,1,0,0,0,-1),
```

with squared norm `4`; the exact squared norm of its defect image is recorded
in the canonical certificate.
