# Derivation Package

## Target

Determine the exact feasible set of `<W,B>` after fixing one longitudinal
direction, the two longitudinal moments, and the two transverse energies.

## Status

`PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS`.

## Assumptions and orientation

- `H` is a complex Hilbert space.
- The inner product is conjugate-linear in the first slot.
- `u` is a unit vector and `K=u^perp`.
- `b=<u,B>` and `w=<u,W>`.
- Prescribed energies `E_B,E_W` are nonnegative.

There is no finite-dimensionality or separability assumption.  The only
dimension datum used is whether `dim_C K` is zero, one, or at least two.

## Exact decomposition

Set

```text
B_perp=B-bu,
W_perp=W-wu.
```

Then both transverse vectors lie in `K`, and

```text
||B_perp||^2=||B||^2-|b|^2=E_B,
||W_perp||^2=||W||^2-|w|^2=E_W,
<W,B>=conjugate(w)b+<W_perp,B_perp>.
```

Thus the longitudinal center and Cauchy radius are

```text
c=conjugate(w)b,
r=sqrt(E_B E_W).
```

## Feasible-set derivation

Cauchy--Schwarz gives `|<W_perp,B_perp>|<=r`.  If `dim K>=2`, choose
orthonormal `e1,e2`.  For every `q` with `|q|<=r` and `r>0`, take

```text
W_perp=sqrt(E_W)e1,
B_perp=sqrt(E_B)[(q/r)e1+sqrt(1-|q|^2/r^2)e2].
```

The prescribed energies hold and `<W_perp,B_perp>=q`.  Hence the containment
is the exact closed disk.  The `r=0` branch is the singleton center.

If `dim K=1`, nonzero vectors with fixed norms are collinear, so their inner
product has modulus exactly `r`; varying the relative phase fills the entire
circle.  If one energy vanishes, the transverse covariance is zero.  If
`dim K=0`, both energies must vanish or the data are unrealizable.

## Sharp consequences

For `dim K>=2`, distance from the origin to the disk gives

```text
min |<W,B>|=max(|c|-r,0),
0 is feasible iff |c|<=r.
```

For `dim K=1` and `r>0`, the corresponding formulas are

```text
min |<W,B>|=||c|-r|,
0 is feasible iff |c|=r.
```

If `0<=r<|c|`, rotate so `c=|c|>0`.  Writing a feasible covariance as
`rho exp(i theta)` gives

```text
|z-c|^2=(rho-|c|cos theta)^2+|c|^2 sin^2 theta<=r^2,
```

so the principal angular deviation is at most `arcsin(r/|c|)`.  Tangency makes
this bound sharp.

## Source relationship

TPC-244 names `<w_h,b_h>` as the next local object, so this derivation is its
natural structural continuation.  TPC-219 supplies a related orthogonal
projection pattern, but its longitudinal object is the constant-prime-label
subspace of `V^P`, generally of dimension `dim V`; it is not a source-defined
one-dimensional `u_h` in a TPC-244 block.

## Boundaries

- The direction `u` is abstract, not literal V59 data.
- Feasibility over all vectors does not prove cancellation for the actual vectors.
- No coefficient norm or transverse energy estimate is supplied.
- No arithmetic `L2`, fixed atom, strict endpoint, Gate-B, or twin-prime claim is made.
