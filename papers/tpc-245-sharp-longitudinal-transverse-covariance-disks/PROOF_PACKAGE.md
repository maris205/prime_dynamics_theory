# Proof Package

## Main theorem

Let `H` be a complex Hilbert space with inner product conjugate-linear in the
first slot, let `u` be a unit vector, and put `K=u^perp` and
`m=dim_C K`.  Fix `b,w in C` and `E_B,E_W>=0`.  Let `S` be the set of all
covariances `<W,B>` over vectors satisfying

```text
<u,B>=b,  <u,W>=w,
||B||^2-|b|^2=E_B,
||W||^2-|w|^2=E_W.
```

Write `c=conjugate(w)b` and `r=sqrt(E_B E_W)`.

1. If `m>=2`, then `S={z in C: |z-c|<=r}`.
2. If `m=1` and `r>0`, then `S={z in C: |z-c|=r}`.
3. If `m=1` and `r=0`, then `S={c}`.
4. If `m=0` and `E_B=E_W=0`, then `S={c}`.  If `m=0` and
   `E_B+E_W>0`, the prescribed data are unrealizable and `S` is empty.

Consequently, for `m>=2`,

```text
min_(z in S)|z|=max(|c|-r,0),
0 in S iff |c|<=r.
```

For `m=1,r>0`, the minimum is `||c|-r|` and zero is feasible exactly when
`|c|=r`.  In every realizable branch,
`|<W,B>|>=max(|c|-r,0)`.  If `0<=r<|c|`, every feasible covariance has
principal angular distance from `c` at most `arcsin(r/|c|)`; the bound is sharp
whenever the radius-`r` circle is feasible.

## Proof of the decomposition and upper disk

Define

```text
B_perp=B-bu,  W_perp=W-wu.
```

Because `<u,B>=b` and the second slot is linear, both vectors are orthogonal to
`u`.  Pythagoras gives their squared norms `E_B,E_W`.  Orthogonality and
sesquilinearity give

```text
<W,B>=<wu+W_perp,bu+B_perp>
     =conjugate(w)b+<W_perp,B_perp>.
```

Cauchy--Schwarz proves `|<W_perp,B_perp>|<=r`, so every feasible covariance
lies in the claimed disk.

## Proof of exact disk filling

Assume `m>=2`.  If `r=0`, at least one transverse vector is zero, so the only
transverse covariance is zero and the disk is the singleton `{c}`.

If `r>0`, choose orthonormal `e1,e2 in K`.  Given any `q` with `|q|<=r`, set

```text
W_perp=sqrt(E_W)e1,
B_perp=sqrt(E_B)[(q/r)e1+sqrt(1-|q|^2/r^2)e2].
```

The square root is real and nonnegative.  The two prescribed norms hold, and
conjugate-linearity in the first slot gives

```text
<W_perp,B_perp>=sqrt(E_W E_B)q/r=q.
```

Adding `bu` and `wu` realizes `c+q`.  Thus every point in the disk is feasible.

## Proof of low-dimensional branches

If `m=1`, choose a unit vector `e` spanning `K`.  When both energies are
positive, write

```text
W_perp=sqrt(E_W)xi e,
B_perp=sqrt(E_B)eta e,
```

where `|xi|=|eta|=1`.  Their inner product is
`r conjugate(xi)eta`, which fills exactly the unit circle times `r`.  If one
energy vanishes, one transverse vector is zero and the contribution is zero.

If `m=0`, then `K={0}`.  Positive prescribed transverse energy is impossible;
when both energies vanish, the unique covariance is the center.

## Distance and phase corollaries

The minimum-modulus and zero-feasibility formulas are the exact distances from
the origin to a translated disk, circle, or singleton.  The universal lower
bound also follows directly from the reverse triangle inequality.

For the phase bound, rotate so that `c=a>0` and write a nonzero feasible point
as `z=rho exp(i theta)`, where `theta` is the principal angular deviation.  Since

```text
|z-a|^2=(rho-a cos theta)^2+a^2 sin^2 theta<=r^2,
```

we have `|sin theta|<=r/a`.  The disk misses the origin because `r<a`, so
`|theta|<pi/2`, and therefore `|theta|<=arcsin(r/a)`.  The two tangent points
from the origin satisfy equality.  They lie on the radius-`r` circle, proving
sharpness both for `m>=2` and for the nondegenerate `m=1` branch.

## Hostile controls

- In `H=C^2`, with `u=e0`, `b=w=0`, and `E_B=E_W=1`, transverse dimension one
  gives the unit circle, not the disk; zero is not feasible.
- In `H=Cu`, take `B=u,W=iu`.  Then `<W,B>=-i=conjugate(w)b`, while
  `conjugate(b)w=i`; reversing the conjugation fails.
- Positive transverse energy in dimension zero is not a singleton branch; it
  is unrealizable.
- At `r=|c|`, zero may occur and has no phase; the strict phase hypothesis is
  necessary.

## Claim boundary

This proves exact abstract Hilbert geometry only.  It does **not** prove a
literal V59 two-lane coefficient attachment, a source-native canonical block
direction, a coefficient norm or energy estimate, signed arithmetic
cancellation, arithmetic `L2`, fixed-atom credit, strict `1/400`, full Gate B,
or a twin-prime result.

## Reusable structure and next theorem

The reusable structure is

```text
longitudinal center + transverse disk/circle
  -> exact cancellation margin
  -> exact phase cone when the margin is positive.
```

The next minimal problem is to aggregate independently realizable local disks
with the nonnegative common-multiplier weights `|C_h|^2`, then compare the
aggregate margin against the TPC-243 hard-window error.  This is the TPC-246
candidate and remains structural until the physical attachment is proved.
