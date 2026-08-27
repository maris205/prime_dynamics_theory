# TPC-274 derivation package

## 1. The finite operator

Write `L=N/2` for the length of the physical source interval and let
`β=(β_t)_{t}` be the exact beta vector.  For a prime shell
`Q<q<=2Q`, define the real matrix

```text
A_(u,t) = 1_(u!=t) sum_q q K_(H,s)(u-t)
          1_(q does not divide u) 1_(q does not divide t)
          (1_(u=t mod q) - 1/(q-1)).
```

The released finite engine computes `g=A beta`.  Let `P_3` be the orthogonal
projection onto the three declared four-block Haar contrast vectors and put

```text
A_perp = (I-P_3) A,
g_perp = A_perp beta,
G_perp = ||g_perp||_2^2.
```

All entries of `A` and `beta` are rational on a registered row.  The comparison
weight `w` may have interval endpoints because it contains logarithms; that
uncertainty is used only for the residual scalar and source norm intervals.

## 2. Projected Frobenius envelope

For every finite matrix `B` and vector `v`, rowwise Cauchy--Schwarz gives

```text
||Bv||_2^2
 = sum_i |sum_j B_(i,j) v_j|^2
 <= sum_i (sum_j |B_(i,j)|^2)(sum_j |v_j|^2)
 = ||B||_F^2 ||v||_2^2.
```

Taking `B=A_perp` and `v=beta` proves the exact finite inequality

```text
G_perp <= G_F,
G_F := ||A_perp||_F^2 ||beta||_2^2.
```

This estimate is projection-aware, but it is cancellation-free with respect to
the beta vector: it discards the relative phases and signs between columns.

## 3. Margin consequence

On a row with positive `W_perp` and `G_perp`, define the conservative envelope
margin

```text
m_F^2 := |C_perp|^2/(W_perp G_F).
```

Since `G_perp<=G_F`, one has `m_F^2<=m^2` at the underlying finite value.
Consequently an upper bound on `m_F` is not a counterexample to a large actual
margin; it is a certificate that this particular envelope cannot prove one.

The producer computes `||A_perp||_F^2`, `||beta||_2^2`, and `G_F` exactly as
rational numbers, then combines them with the parent outward intervals for
`C_perp` and `W_perp`.  It also stores the exact interval for `G_F/G_perp`,
where the denominator is the parent output-residual interval.

## 4. Why this is a new interface test

TPC-273 varied declared cutoffs and found finite margin instability.  TPC-274
does not vary that interface.  It asks whether a standard norm-only proof step
could control the output lane after the same projection.  The answer on the
registered rows is negative in a scoped, quantitative sense: the envelope is
valid, but its gap from the actual output residual exceeds 50 on every row and
its induced margin proxy lies below `1/8` on every row.

No claim is made that the actual growing V59 output has a large gap, or that a
signed reassembly cannot improve the bound.  Such improvement is precisely the
next open question.
