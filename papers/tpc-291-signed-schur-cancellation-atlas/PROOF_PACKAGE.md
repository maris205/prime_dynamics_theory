# TPC-291 proof package

## Lemma 1 — exact Schur projection

Let `g_i,g_j` be nonzero vectors, let `d_i=||g_i||^2`, `d_j=||g_j||^2`, and
`G=<g_i,g_j>`.  Then

```text
argmin_rho ||g_i-rho g_j||^2 = G/d_j,
min_rho ||g_i-rho g_j||^2/d_i = 1-G^2/(d_i d_j).
```

**Proof.** Expand the square as
`d_i-2rho G+rho^2d_j`.  Its derivative vanishes at `G/d_j`; the quadratic
coefficient `d_j` is positive.  Substitution gives the stated residual. ∎

## Lemma 2 — Cauchy residual nonnegativity

The Schur residual in Lemma 1 is nonnegative.

**Proof.** Cauchy--Schwarz gives `G^2<=d_i d_j`.  Equivalently, it is the
determinant condition for the two-by-two Gram matrix. ∎

## Proposition 3 — signed two-vector Rayleigh minimum

For real `(a,b)` not both zero,

```text
inf ||a g_i+b g_j||^2/(a^2d_i+b^2d_j)
 = 1-sqrt(G^2/(d_i d_j)).
```

**Proof.** Conjugate the two-by-two Gram matrix by
`diag(d_i^(-1/2),d_j^(-1/2))`.  The resulting symmetric matrix has diagonal
one and off-diagonal `c=G/sqrt(d_i d_j)`, hence eigenvalues `1+-|c|`. ∎

## Proposition 4 — sign interpretation

For the projection convention `g_i-rho*g_j`, the optimal coefficient has the
sign of `G`.  Positive `G` therefore requires opposite coefficient signs;
negative `G` permits same-sign coefficients.

**Proof.** `d_j>0`, so `sign(rho*)=sign(G)`. ∎

## Finite atlas consequences

The producer evaluates every pair on 18 declared rows.  There are 1,380
pairs: 1,377 positive and 3 negative, with no zero pair.  The exact Schur
residual is nonnegative for every pair.  Residual thresholds `1/2`, `1/4`,
and `1/10` contain respectively 1,074, 852, and 477 pairs; coherence
thresholds `9/25` and `3/4` contain 1,189 and 852 pairs.  The globally best
pair is `(173,179)` at `(N,H,Q,z,s)=(512,58,90,5,2)`, with residual about
`0.0151239493`.

These counts are finite observations.  They do not establish a multi-prime
signed null direction or an asymptotic cancellation theorem.
