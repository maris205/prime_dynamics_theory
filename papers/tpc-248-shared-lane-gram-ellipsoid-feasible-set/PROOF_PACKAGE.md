# Proof package

## Theorem T248.1: ball image

Let `rho>=0`.  With `V`, `G=V*V`, and `y=V*W` as in the derivation package,

```text
V*{W:||W||<=rho}
 = {y in ran(G): y*G^dagger y<=rho^2}.
```

Proof.  Finite-dimensional range identities give `ran(V*)=ran(G)`.  For
`y in ran(G)`, `W_0=VG^dagger y` satisfies `V*W_0=y`.  Moreover

```text
||W_0||^2=(G^dagger y)*G(G^dagger y)=y*G^dagger y.
```

Since `W_0 in ran(V)=(ker V*)^perp`, every other preimage is the orthogonal sum
`W_0+k`, `k in ker(V*)`.  Thus the displayed quadratic form is the exact
minimum squared norm, proving both inclusions.  This includes `rho=0` and
rank-zero `G`.

## Theorem T248.2: exact sphere

For `S_rho={W:||W||=rho}`:

- if `ker(V*)` is nonzero, `V*(S_rho)` is the full solid ellipsoid from T248.1;
- if `ker(V*)={0}`, it is the equality shell
  `y*G^dagger y=rho^2` inside `ran(G)`.

Proof.  In the first case choose a unit `k in ker(V*)` and add the missing
orthogonal norm.  In the second case each feasible `y` has the unique preimage
`W_0`, so its norm must equal `rho`.  The statements remain valid at `rho=0`.

## Corollary T248.3: physical orientation

For `z_i=<W,v_i>`, conjugate symmetry gives `z=conjugate(y)`.  Conjugating the
range and energy identities gives the same classification with
`conjugate(G)` and its pseudoinverse.

## Theorem T248.4: grouped budgets

For a declared Cartesian product of lane balls, the joint image is the
Cartesian product of the local Gram ellipsoids.  For the global direct-sum
budget `sum_c||W_c||^2<=rho^2`, the exact image is instead

```text
y_c in ran(G_c) for every c,
sum_c y_c*G_c^dagger y_c<=rho^2.
```

This follows by adding the independent minimum-preimage energies.

## Obstructions

If `v_1=v_2=e_1`, the unit-ball image is `{(t,t):|t|<=1}`, although both
marginals are unit disks.  If `v_1=e_1,v_2=e_2`, the image is the Euclidean
unit ball, not the bidisk.  Likewise two scalar groups with one global unit
budget cannot realize `(1,1)` even though it lies in the product of the local
unit disks.

No statement here bounds the physical V59 probes, attaches primitive
frequencies, or creates arithmetic cancellation.
