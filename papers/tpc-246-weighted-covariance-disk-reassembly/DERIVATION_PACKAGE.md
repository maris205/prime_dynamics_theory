# TPC-246 derivation package

All complex Hilbert inner products in the source chain are conjugate-linear in
the first slot.

## 1. Weighted local geometry

For a finite index set `A`, suppose each local covariance lies in

```text
S_h = c_h + r_h Dbar,  c_h in C,  r_h >= 0.
```

For complex weights `lambda_h`, put

```text
C = sum_h lambda_h c_h,
a_h = |lambda_h| r_h,
R = sum_h a_h.
```

The triangle inequality gives containment in `C+R Dbar`.  Conversely, if
`R>0` and `d` satisfies `|d|<=R`, choose

```text
e_h = (conjugate(lambda_h)/|lambda_h|)(r_h/R)d
```

when `lambda_h != 0`, and `e_h=0` otherwise.  This reverse construction
requires blockwise product realizability.  Then `|e_h|<=r_h` and
`sum_h lambda_h e_h=d`.  If `R=0`, every weighted deviation vanishes.  Thus
the containment is an equality in every degenerate case as well.

## 2. Sharp aggregate consequences

For the exact disk `C+R Dbar`,

```text
zero is feasible iff |C| <= R,
min |Q| = max(|C|-R,0).
```

If `R<|C|`, all feasible values lie in the sharp sector about `C` with
half-angle `arcsin(R/|C|)`.

## 3. Common-multiplier specialization

TPC-244 gives the coefficient covariance

```text
Q = sum_h |M_h|^2 <w_h,b_h>.
```

If TPC-245 supplies exact local disks with centers `c_h` and radii `r_h`, and
the joint feasible family is their complete Cartesian product, then

```text
C_0 = sum_h |M_h|^2 c_h,
R_0 = sum_h |M_h|^2 r_h
```

are the exact aggregate center and radius.  TPC-245 supplies a full disk when
each active transverse dimension is at least two (or its radius is zero).
A positive-radius one-dimensional transverse block supplies only a circle and
does not satisfy the disk premise.

## 4. Hard-window inflation

Under the literal common TPC-243 synthesis attachment,

```text
|Q_I-Q| <= epsilon ||W|| ||B|| =: E.
```

Therefore every selected hard-window covariance obeys

```text
Q_I in C_0 + (R_0+E) Dbar,
|Q_I| >= max(|C_0|-R_0-E,0).
```

This is a containment, not an exact physical feasible-set identity: TPC-243
bounds the synthesis error but does not show that every error phase is
attained.  Robust nonvanishing follows if `|C_0|>R_0+E`.

## 5. Source boundary

The abstract product theorem is unconditional.  Its V59 reading is conditional
because the committed source does not provide a literal phasewise primitive
two-lane attachment, canonical local block directions, blockwise product
realizability, or payable moment/energy and norm bounds.  No arithmetic gate is
promoted.
