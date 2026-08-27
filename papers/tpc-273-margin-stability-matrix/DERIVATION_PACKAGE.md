# TPC-273 derivation package

## 1. Margin from the parent residual

The parent finite operator returns

```text
C = C_perp,  R^2 = W_perp G_perp,
rho^2 = |C|^2/R^2.
```

On every certified row, `R^2>0` and `C` is nonzero.  Therefore the TPC-272
margin obeys the exact identity

```text
m^2 = (|C|/R)^2 = rho^2.
```

The producer takes the parent outward `rho^2` interval and cubes it to obtain
the rational `m^6` interval.  No numerical square root is used.

## 2. Threshold logic

For a positive interval `[a,b]`,

```text
b < 1/64  => m < 1/8,
a > 1/16  => m > 1/4.
```

Rows between these separated tests receive the middle-band label.  Thus no
row is called low or high unless the stored interval itself separates the
threshold.

## 3. Matched transitions

The grid includes two cutoff-only transitions at fixed scale and exponent:

```text
N=64,  z=2 -> z=5: middle band -> m>1/4,
N=128, z=2 -> z=3: middle band -> m<1/8.
```

It also records a kernel-only transition at `N=96,z=3`; both endpoints stay
in the high band.  A separate phase census finds two positive-real rows at
`N=192,z=3,4,s=1`, while the other 30 rows are negative-real.

## 4. Scope

The parameter grid is a declared finite interface inherited from TPC-268; it
is not the actual growing V59 sequence.  The result refutes only the scoped
finite stability assertion and leaves source-level margin uniformity open.
