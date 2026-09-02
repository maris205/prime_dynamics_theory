# TPC-339 derivation package

Let `S` contain the support of a finite vector `x`, and let `A_S` be the
submatrix formed by the columns indexed by `S`.  Then

```text
||A x||_2^2 = ||A_S x_S||_2^2
           <= ||A_S||_2^2 ||x_S||_2^2
           <= ||A_S||_F^2 ||x_S||_2^2.                       (1)
```

Define

```text
F(S)^2 = ||A_S||_F^2 = sum_(t in S) sum_u |A(u,t)|^2.
```

Equation (1) is sign-free: it survives arbitrary signs in `A` and `x`, and
it does not use a covariance sign.  For a nonzero source norm, the observed
occupancy is

```text
eta(A,x) = (||A x||_2^2/||x||_2^2) / F(supp(x))^2 <= 1.     (2)
```

The numerator is the response gain and the denominator is a support-only
Frobenius gain.  Thus a small occupancy measures slack in the envelope rather
than cancellation credit.

The exact anchor uses `A=[[1,0],[2,1]]`, `x=(3,0)`.  Its response energy is
`45`, source norm is `9`, and `F({0})^2=5`, giving equality in (1).
