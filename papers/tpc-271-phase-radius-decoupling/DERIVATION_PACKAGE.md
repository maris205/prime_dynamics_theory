# TPC-271 derivation package

## 1. Projected residual coordinates

Let `P_3` be the orthogonal projection onto the three declared block
contrasts. On a finite row define

```text
C_perp = <(I-P_3)w_N,(I-P_3)g_(N,theta)>,
W_perp = ||(I-P_3)w_N||^2,
G_perp = ||(I-P_3)g_(N,theta)||^2.
```

The radius product and normalized phase coordinate are

```text
R^2 = W_perp G_perp,
kappa = C_perp / sqrt(W_perp G_perp).
```

All nine registered rows have positive `W_perp` and `G_perp`; the signed
scalar interval is strictly negative on every row.

## 2. Rational endpoint coordinates

To avoid an algebraic number in a finite certificate, define

```text
Xi   = (R^2)^3/N^10,
Xi_W = W_perp^3/N^5,
Xi_G = G_perp^3/N^5,
Xi_C = |C_perp|^6/N^10.
```

Direct multiplication gives the exact identities

```text
Xi = (W_perp G_perp)^3/N^10 = Xi_W Xi_G,
Xi/Xi_C = (W_perp G_perp)^3/|C_perp|^6 = |kappa|^(-6).
```

The first identity attributes a radius change to source and output lanes. The
second identity records how much the radius envelope exceeds the signed scalar
because of phase misalignment. Neither identity asserts that the finite rows
form an asymptotic sequence.

## 3. Interval transfer

For a positive outward interval `[a_-,a_+]`, cubing is monotone and gives
`[a_-^3,a_+^3]`. Positive interval division gives
`[a_-,a_+]/[b_-,b_+] = [a_-/b_+,a_+/b_-]`. The producer applies these rules to
`W_perp`, `G_perp`, `|C_perp|`, and `R^2`; the independent replay checks that
its floating-point point estimates lie inside every stored interval.

For two scales `a<b`, the lane ratios satisfy the exact product relation at
the underlying finite values

```text
Xi_b/Xi_a = (Xi_W,b/Xi_W,a)(Xi_G,b/Xi_G,a).
```

The stored intervals are allowed to widen because the same upstream quantities
occur in both factors.

## 4. Interpretation of the certificate

The four dyadic records show a concrete finite attribution pattern. In the
`96->192` record, the source lane drops below `1/8` while the output lane rises
above `230`; their product forces the radius ratio above `23`. At both endpoints
the scalar phase is negative real. This is the scoped phase--radius
decoupling statement.
