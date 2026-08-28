# TPC-291 derivation package

## 1. Pair Gram normal form

For two nonzero physical component vectors `g_i,g_j`, write
`d_i=||g_i||^2`, `d_j=||g_j||^2`, and `G=<g_i,g_j>`.  Set
`Gamma=G^2/(d_i d_j)`.

## 2. Projection calculation

For a real coefficient `rho`,

```text
||g_i-rho g_j||^2 = d_i - 2 rho G + rho^2 d_j.
```

Completing the square gives the unique minimizer
`rho*=G/d_j` and

```text
min_rho ||g_i-rho g_j||^2 = d_i-G^2/d_j = d_i(1-Gamma).
```

Thus the normalized Schur residual is exactly `1-Gamma`.  The scale-normalized
coefficient cost satisfies
`|rho*| sqrt(d_j/d_i)=sqrt(Gamma)`.

## 3. Sign cost

If `G>0`, then `rho*>0` and the minimizing expression
`g_i-rho*g_j` uses opposite signs.  If `G<0`, then `rho*<0`, so the same
expression uses same-sign coefficients.  The latter is precisely why an
exceptional negative Gram pair can be accessed by nonnegative sparse support
after a change of orientation, while a positive coherent block requires a
signed subtraction.

## 4. Two-vector Rayleigh form

After normalizing by `sqrt(d_i),sqrt(d_j)`, the two-vector Gram matrix is
`[[1,c],[c,1]]`, where `c=G/sqrt(d_i d_j)`.  Its eigenvalues are
`1+-|c|=1+-sqrt(Gamma)`.  Consequently the best signed two-coordinate
normalized energy is `1-sqrt(Gamma)`; this is a geometric diagnostic, not a
full-shell estimate.

## 5. Route consequence

TPC-290 showed that diffuse positive weighting cannot cross an all-positive
coherence wall.  TPC-291 shows the complementary fact: high coherence creates
low-residual signed pair directions, but the sign of that direction is a
physical constraint.  The remaining problem is to determine whether such
pair directions can be assembled with the actual prime-shell signs and
source arithmetic without losing the required normalization.
