# TPC-344 derivation package

Let the six rows be ordered as the three TPC-341 rows followed by the three
TPC-342 rows.  For nuisance category `j`, let `n_{r,j}` be the row mean and
let

```text
b_j = (n_{1,j}, n_{2,j}, n_{3,j}, n_{4,j}, n_{5,j}, n_{6,j})^T,
d_j = (n_{1,j}, n_{2,j}, n_{3,j}, -n_{4,j}, -n_{5,j}, -n_{6,j})^T.
```

Here each displayed entry is itself a length-512 output vector, so the
notation denotes vertical concatenation.  Define

```text
u_1j = (b_j+d_j)/2 = (n_{1,j},n_{2,j},n_{3,j},0,0,0)^T,
u_2j = (b_j-d_j)/2 = (0,0,0,n_{4,j},n_{5,j},n_{6,j})^T.
```

Therefore

```text
span{b_j,d_j} = span{u_1j,u_2j}
```

for each nuisance category, and the six-column contrast span equals the
panel-adaptive shared span.  The equality is a change of coordinates, not a
claim that the panel coefficients are arithmetic invariants.

For a finite nuisance matrix `N`, let `P_N` be the orthogonal projector onto
its column space.  Then

```text
||Y||_2^2 = ||P_N Y||_2^2 + ||(I-P_N)Y||_2^2.
```

For equal-row weighting, each row target and all row nuisance columns are
divided by the same positive target norm before stacking.  This preserves
within-row spans but changes the meta-level weights.

For cross-fit, coefficients are obtained by least squares on the three
row-mean vectors of one panel and applied without refitting to the other
panel.  This is a prediction residual calculation; unlike an orthogonal
projection it has no Pythagorean identity.
