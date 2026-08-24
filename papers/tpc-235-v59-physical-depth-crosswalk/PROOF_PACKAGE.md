# TPC-235 proof package

## Theorem 1: physical-depth crosswalk

For every physical denominator `h`, define `lambda_h=hQ/H`.  Then the V59/TPC-218 row
is exactly

\[
B_{h,q}(a)=\sum_{0<|m|\le\lfloor\lambda_hq/Q\rfloor}
\psi(mQ/(\lambda_hq))\mathbf1_{mq^{-1}=a\ (h)}.
\]

The modulus remains `h=(H/Q)lambda_h`; it is not determined by depth alone.

### Proof

The cutoff identity is `hq/H=(hQ/H)(q/Q)=lambda_hq/Q`.  The profile identity is
`Hm/(hq)=mQ/(lambda_hq)`.  The residue condition is unchanged.  ∎

## Theorem 2: single-clock iff criterion

The physical row at modulus `h` and the TPC-226 row at depth `L`, modulus `4LQ`, have
the same modulus and the same cutoff/profile scale for all multipliers and shell primes
if and only if

\[
h=4LQ,\qquad H=4Q^2.
\]

### Proof

Modulus equality gives `h=4LQ`.  Equality of the dimensionless profile arguments
`Hm/(hq)` and `mQ/(Lq)` for nonzero `m` gives `H/h=Q/L`.  Substituting the first
identity into the second yields `H=4Q^2`.  Conversely these two identities make the
modulus, cutoff, profile argument, and residue condition identical.  ∎

At V59 scales,

\[
4Q^2/H=4x^{2/3-21/32}=4x^{1/96}\to\infty.
\]

Therefore exact attachment to the TPC-226 one-clock family is refuted in this scope.

## Corollary: physical depth range and denominator-grid density

An active row has `hq/H>=1` for some `q<=2Q`, hence `h>=H/(2Q)`.  With `h<=U`,

\[
1/2\le\lambda_h\le UQ/H=x^{23/2400}.
\]

Since consecutive integer denominators differ in depth by `Q/H`, an interval of unit
depth contains `H/Q+O(1)=x^{31/96+o(1)}` available grid points.  The subset with
nonzero `C_h` is source-weighted and is not counted here.  The physical object is
therefore a weighted many-clock family, not one clock per integer depth.

## Theorem 3: output normalization breaks polarization

Let `T` be a common linear transform and suppose all four vectors
`T(beta+i^j w)` are nonzero.  Replacing each by its unit normalization makes the V59
signed quadratic sum zero:

\[
\frac14\sum_{j=0}^3i^j
\left\|\frac{T(\beta+i^jw)}{\|T(\beta+i^jw)\|}\right\|^2=0.
\]

This cannot equal `inner(T beta,T w)` in general.

### Proof

Every squared norm in the displayed sum equals one and `sum_j i^j=0`.  Taking the
one-dimensional transform `T=1`, `beta=1`, `w=2` gives target `2`, proving failure. ∎

## Consequence

TPC-234 remains a correct normalized-row theorem, but its output-dependent unit
normalization cannot be inserted into the V59 four-packet source identity.  A legal
next compiler must retain the complete physical `h`-fiber, the coefficients `C_h`, and
one common packet transform with any fixed linear weights shown explicitly.
