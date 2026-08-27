# TPC-284 derivation package

## Frozen interface

For a registered baseline tuple `(X,H,Q,z)` and kernel exponent `s`, the
literal source engine defines comparison weights `w`, a rational prime-shell
operator `A`, source profile `beta`, and the three-contrast projection `P_3`.
The controlled attachment is

```text
C(X,H,Q,z,s) = <(I-P_3)w, (I-P_3)A beta>
rho^2(X,H,Q,z,s) = C^2/(W Y),
W = ||(I-P_3)w||^2,  Y = ||(I-P_3)A beta||^2.
```

The source intervals and prime-shell output use the frozen TPC-268 engine.
The interval class rounds every arithmetic operation down at the lower end
and up at the upper end on a fixed rational grid.  Thus an interval `[a,b]`
with `b<0` certifies a negative scalar, while `[a,b]` with `a>0` certifies a
positive scalar.

## Control map

For each baseline tuple, use the six maps

```text
(H,Q,z) -> (H-2,Q,z), (H+2,Q,z),
           (H,Q,z-1), (H,Q,z+1),
           (H,Q-1,z), (H,Q+1,z).
```

There are six baseline tuples, two exponents, and six controls, hence
`6*2*6=72` rows.  The baseline sign is read from the hash-locked TPC-283
source-scalar interval.  A controlled row is a `sign_flip` precisely when
its certified sign differs from this baseline sign.

## Why this is the right finite test

TPC-283 gives the exact distance to the zero-attachment hyperplane but permits
an arbitrary projected-space direction.  The present atlas tests the nearest
named changes already exposed by the literal implementation: clock scale,
comparison cutoff, and shell endpoint.  It consequently probes a source-level
control interface without pretending that the six directions are exhaustive.

## Recorded extrema

The smallest lower endpoint of `rho^2` occurs at the `X=192`, `s=1`, `H+2`
row and is approximately `1.4118389e-5`.  The largest upper endpoint occurs
at `X=64`, `s=2`, `z+1` and is approximately `0.1538985`.  These are finite
diagnostics only; neither is converted into an exponent or a uniform margin.
