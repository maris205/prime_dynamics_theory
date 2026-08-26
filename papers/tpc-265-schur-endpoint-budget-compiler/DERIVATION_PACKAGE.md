# TPC-265 derivation package

## 1. Schur output as a scalar feasible set

TPC-264 supplies, for fixed projected data,

```text
F_x = {c_x + z : |z| <= R_x},
R_x = ||(I-P_3)w|| ||(I-P_3)g_x||
```

when the unobserved complement has dimension at least two.  The circle and
singleton variants are treated separately.  The present paper studies the
support function of `F_x`, not a new estimate for the literal vectors.

## 2. Exact radial envelope

For any `c in C` and `R>=0`,

```text
sup_{|z|<=R} |c+z| = |c|+R,
inf_{|z|<=R} |c+z| = max(|c|-R,0).
```

For the full circle `|z|=R`, the supremum remains `|c|+R` and the infimum is
`||c|-R|`.  The upper equality is attained by aligning `z` with `c`; hence
norm-only residual information gives no cancellation discount in a uniform
upper bound.

## 3. Endpoint compiler

Set

```text
E0=5/3, E*=1997/1200, Delta*=E0-E*=1/400.
```

If a center lane and a residual-radius lane have bounds

```text
|c_x| <= C_c x^(E0-delta_c+lambda_c+epsilon),
R_x    <= C_r x^(E0-delta_r+lambda_r+epsilon),
```

then the exact Schur envelope is bounded by their sum.  The finite two-lane
compiler pays the endpoint whenever both effective savings
`delta_j-lambda_j` are strictly greater than `Delta*`.  Equality is only
borderline, and a smaller effective saving fails to close the target.

This is an interface theorem: it does not assert that the literal V59 center
or radius satisfies either power bound.

## 4. Logarithmic firewall

The TPC-263 center has arbitrary fixed logarithmic suppression but no proved
fixed-power credit.  Since

```text
x^(E0)/(log x)^M / x^(E0-delta) = x^delta/(log x)^M -> infinity,
```

the center lane cannot be silently counted as a positive `delta`.  The same
logic applies to a residual radius controlled only by logarithms.

## 5. Phase datum

If a future theorem restricts `z` to an anti-aligned ray, the lower edge rather
than the disk supremum may become relevant.  Such a phase restriction is extra
information: it is not implied by `Gamma(z)>=0`.  Thus there are two legitimate
routes after TPC-264:

```text
radius route: prove R_x has effective saving > 1/400,
phase route: prove a signed/sector cross-Gram theorem of that strength.
```
