# Derivation package

Use a finite-dimensional complex Hilbert space `H` with inner product
conjugate-linear in the first slot.  Given ordered probes `v_1,...,v_m`, define

```text
V:C^m -> H,       Va=sum_i a_i v_i,
V*:H -> C^m,      (V*W)_i=<v_i,W>,
G=V*V,            G_ij=<v_i,v_j>.
```

For `y in ran(G)`, put `W_0=VG^dagger y`.  The Moore--Penrose identities give

```text
V*W_0=GG^dagger y=y,
||W_0||^2=y*G^dagger y.
```

Every other preimage is uniquely `W_0+k` with `k in ker(V*)`, and the two
summands are orthogonal.  Hence

```text
min {||W||^2:V*W=y}=y*G^dagger y.
```

This proves the ball image.  It also proves the exact-sphere dichotomy: if
`ker(V*)` contains a unit vector, add orthogonal slack of length
`sqrt(rho^2-y*G^dagger y)`; without such slack the minimum preimage is the only
preimage and equality is required.

For physical covariances `z_i=<W,v_i>=conjugate(y_i)`, the exact condition is

```text
z in ran(conjugate(G)),
z* (conjugate(G))^dagger z <= rho^2.
```

For independent lane budgets `||W_c||<=rho_c`, images multiply.  For one
global budget `sum_c||W_c||^2<=rho^2`, minimum energies add and the exact image
is

```text
sum_c y_c*G_c^dagger y_c <= rho^2.
```

The next contraction should not optimize each marginal separately.  It should
first combine weighted probes within each shared lane and only then sum the
resulting sharp group radii.
