# TPC-351 derivation package

Let `I={o,...,o+M-1}` and let `D_I=A_I-T_I` be the literal physical-minus-ideal
mask defect.  For the ordered shell `p_0<...<p_(r-1)`, define the rational
reciprocal-centered coefficients

```text
gamma_j = 1/p_j - (1/r) sum_(k=0)^(r-1) 1/p_k.
```

The sum is exactly zero and no coefficient vanishes because the shell primes
are distinct.  For `h_(p,I)(t)=1_(p divides t)`, define
`c_I=sum_j gamma_j h_(p_j,I)`.  This rule depends only on the shell and is
frozen before the origin, length, source law, or response is inspected.

Linearity gives

```text
D_I c_I = sum_j gamma_j D_I h_(p_j,I).
```

Taking the Euclidean square and expanding the finite sum gives the exact
prime-incidence Gram identity

```text
||D_I c_I||_2^2
 = sum_(j,k) gamma_j gamma_k
   <D_I h_(p_j,I), D_I h_(p_k,I)>.
```

When `c_I != 0`, `x_I=c_I/||c_I||_2` is a unit vector.  Therefore

```text
||D_I||_(2->2) >= ||D_I x_I||_2
                   = ||D_I c_I||_2 / ||c_I||_2.
```

TPC-351 adds only a finite parent-comparison and scale-series diagnostic.  For each fixed
`(o,Q,s,law)`, the four stored ratios are ordered by `M=256,512,1024,2048`;
the endpoint log-two slope is

```text
[log_2(rho_2048)-log_2(rho_256)]/3.
```

The parent comparison uses the locked TPC-350 balanced-step response with the
same row key.  These are descriptive finite statistics.  They are not a limit,
a monotonicity theorem, a universal floor, or an arithmetic estimate.
