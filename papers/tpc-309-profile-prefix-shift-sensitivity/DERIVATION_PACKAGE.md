# TPC-309 derivation package

## Frozen source object

The source indices are `I=[257,512]` and the height is `H=58`.  For a cutoff
`z`, the profile coordinate is the locked literal value

```text
beta(v;z) = lambda(v) - sum_{d|v, d<=z} mu(d),
```

with the prime-power term `lambda(v)` supplied by the frozen TPC-268 engine.
The physical shell row is the same deleted-diagonal, centered-residue kernel
used by TPC-308; only the profile matrix multiplying that row is changed.

## Profile ladders

Let

```text
P=(2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67).
```

The three ordered profile ladders are the contiguous windows

```text
LOW  = P[0:17] = (2,...,59)
BASE = P[1:18] = (3,...,61)
HIGH = P[2:19] = (5,...,67).
```

Every ladder is source-backed and has the same dimension.  The adjacent
windows share 16 of 17 coordinates; no new label or shell is introduced.

For a ladder `a`, write `B_a` for its 256-by-17 profile matrix and
`M_a=B_a^T B_a` for its source Gram.  For a shell union `U`, the physical
matrix is `V_{U,a}`.  The overlap matrix is the row restriction
`V_{O,a}`.

## Directional frontier

For each adjacent shell pair, the overlap labels are aligned by the sign of
their raw overlap inner product.  For a target `t` and tolerance `tau`, let
`k(t,a)` be the first ordered prefix for which the least-squares residual is
at most `tau^2 ||t||^2`.  The common comparison prefix is

```text
k_a=max(k(t_left,a), k(t_right,a)).
```

At that prefix, the frontier coefficient is the minimum-source-norm point on
the residual boundary.  Its source energy is `E_left,a` or `E_right,a`.
The primary budget ratio is the conservative enclosure of
`E_right,a/E_left,a`; the secondary audit compares the same holdout to the
TPC-308 budget class held fixed.

## Exclusive completion envelope

If `h` is a native binary exclusive target and `y` the fitted prediction on
the same exclusive rows, define

```text
C_r(h)={h' in {-1,+1}^m : d_H(h,h')<=r},
L^-_r=min_{h' in C_r(h)} mean((y-h')^2),
L^+_r=max_{h' in C_r(h)} mean((y-h')^2).
```

The reported holdout ratio interval is

```text
[ L^-_r(right)/L^+_r(left), L^+_r(right)/L^-_r(left) ].
```

All four extrema are enumerated exactly in the finite completion set.  The
three profile ladders and three radii yield `3*18*3=162` observations.

## Interpretation target

The question is not whether a profile choice proves twin primes.  It is
whether the finite budget/holdout class is invariant under the smallest
declared source-profile shift.  A change of strict discordance location, or a
systematic expansion of the unresolved band, is a valid obstruction to a
profile-independent preference claim.
