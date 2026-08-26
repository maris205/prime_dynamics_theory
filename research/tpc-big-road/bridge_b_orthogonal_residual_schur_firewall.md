# Bridge B: TPC-264 orthogonal-residual Schur firewall

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## Position after TPC-263

TPC-263 proves the source-backed rank-three channel

```text
C_3=<P_3 w,P_3 A_x beta>
  =O_(M,K)(x^(5/3)/(log x)^(M+3))
```

on the literal V59 clock, while retaining the exact residual

```text
C_perp=<(I-P_3)w,(I-P_3)A_x beta>.
```

TPC-264 asks what fixed projected data and residual norms say about this missing
scalar.  It is a finite Hilbert-space theorem, deliberately separated from the
unproved literal growing-shell estimate.

## Exact Schur theorem

Let `P` be an orthogonal projection, put

```text
p=Pw, q=Pg, u=(I-P)w, v=(I-P)g,
a=||u||, b=||v||, c=<p,q>, z=<u,v>.
```

Then

```text
<w,g>=c+z,
Gamma(z)=[[a^2,z],[conjugate(z),b^2]] >= 0,
|z| <= a b.
```

The inequality is sharp.  If `dim ker(P)>=2`, every point of the closed disk
`|z|<=ab` is realized while keeping `p,q,a,b` fixed.  If the complement has
dimension one and `ab>0`, the exact set is the circle `|z|=ab`; if the
complement is zero-dimensional or `ab=0`, it is the singleton `{0}`.  Translating
by `c` gives the complete feasible set for the full scalar.

The disk realization follows by choosing two orthonormal complement vectors and
setting `u=a e_1`,
`v=b(r exp(i theta)e_1+sqrt(1-r^2)e_2)`, where `r=|z|/(ab)`.  The one-dimensional
case is equality in Cauchy--Schwarz.  This is an exact Schur-complement
classification, not a numerical approximation.

## Endpoint firewall

The synthetic scale `a=b=x^(5/6)` gives radius `x^(5/3)`.  Hence a
logarithmically small TPC-263 center does not, from norm-only residual data,
imply a fixed-power saving.  To pay the inherited strict endpoint gap, a future
literal result must either prove a residual-radius saving with effective power
strictly larger than `1/400`, or control the signed residual phase/cross-Gram at
the same strength.

The scale family and its endpoint vectors are structural witnesses only:

```text
TPC264_MAXIMUM_CLAIM = PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
TPC264_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_SCHUR_FIREWALL
TPC264_PROJECTION_DATA = PROVED_EXACT
TPC264_RESIDUAL_GRAM_FEASIBLE_SET = PROVED_EXACT
TPC264_COMPLEMENT_DIMENSION_SPLIT = PROVED_EXACT
TPC264_FULL_SCALAR_FEASIBLE_SET = PROVED_EXACT
TPC264_ENDPOINT_SCALE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL
TPC264_FIXED_POWER_CREDIT = 0
TPC264_ARITHMETIC_ADVANCE = NO
TPC264_ACTUAL_V59_RESIDUAL = OPEN
TPC264_L2 = NONE
TPC264_FULL_GATE_B = OPEN
TPC264_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC264_TWIN_PRIME_RESULT = NONE
TPC264_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC264_STATUS = PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
TPC264_ROUND2_CLUE = TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE_INTO_A_LITERAL_V59_ESTIMATE
```

The certificate is in
`papers/tpc-264-orthogonal-residual-schur-firewall/results/tpc264_certificate.json`.
