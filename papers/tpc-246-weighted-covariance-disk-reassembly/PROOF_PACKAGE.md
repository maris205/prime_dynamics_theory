# TPC-246 proof package

## Proposition 0: aggregate containment without product realizability

Let `J` be any nonempty jointly feasible family of tuples `(z_h)_h` such that
`z_h in c_h+r_h Dbar` for every tuple and every `h`.  Then

```text
{sum_h lambda_h z_h : (z_h)_h in J} subset C+R Dbar.
```

This follows from the triangle inequality exactly as in the first paragraph of
Theorem A below.  No blockwise product premise is needed for containment.

## Theorem A: exact weighted disk reassembly

Let `A` be finite.  For `h in A`, let `c_h in C`, `r_h>=0`, and
`S_h=c_h+r_h Dbar`.  Assume **blockwise product realizability**, meaning the
joint feasible set is the complete Cartesian product of these nonempty disks.
The aggregate feasible set is

```text
S = {sum_h lambda_h z_h : z_h in S_h for every h},
```

where `lambda_h in C`.  Define

```text
C = sum_h lambda_h c_h,
R = sum_h |lambda_h| r_h.
```

Then `S=C+R Dbar` exactly.

### Proof

Write `z_h=c_h+e_h`, where `|e_h|<=r_h`.  Then

```text
|sum_h lambda_h e_h| <= sum_h |lambda_h|r_h = R,
```

so `S` is contained in `C+R Dbar`.

For the reverse inclusion, first suppose `R=0`.  Every nonnegative summand
`|lambda_h|r_h` is zero, hence every weighted deviation `lambda_h e_h`
vanishes and `S={C}`.

Now suppose `R>0`.  Given `d in C` with `|d|<=R`, set

```text
e_h = 0                                                   if lambda_h=0,
e_h = (conjugate(lambda_h)/|lambda_h|)(r_h/R)d            otherwise.
```

The second formula also gives zero when `r_h=0`.  In all cases
`|e_h|<=r_h`.  Moreover,

```text
sum_h lambda_h e_h
  = sum_(lambda_h!=0) (|lambda_h|r_h/R)d
  = d.
```

Thus `C+d` is feasible.  This proves equality, including the empty-index,
zero-weight, and zero-radius cases.  QED.

## Corollary B: sharp cancellation and phase geometry

Under Theorem A,

```text
0 in S iff |C|<=R,
min_(Q in S)|Q| = max(|C|-R,0).
```

If `R<|C|`, every `Q in S` satisfies

```text
|arg(Q)-arg(C)| <= arcsin(R/|C|),
```

with the angular difference chosen in `[-pi,pi]`; the bound is sharp.

### Proof

The zero and distance formulas are the elementary distance from the origin to
the closed disk.  When the origin lies outside the disk, its two tangent rays
form a right triangle with hypotenuse `|C|` and opposite side `R`, yielding
the stated half-angle.  Tangency proves sharpness.  QED.

## Corollary C: TPC-245 to TPC-244 aggregate disk

For each block, fix a TPC-245 unit direction and fixed longitudinal moments and
transverse energies, with local disk

```text
<w_h,b_h> in c_h+r_h Dbar.
```

Assume every positive-radius active block has complex transverse dimension at
least two and that the choices have blockwise product realizability.  Under the
TPC-244 common multiplier `M_h` in both lanes, the exact aggregate coefficient
covariance set is

```text
C_0+R_0 Dbar,
C_0=sum_h |M_h|^2 c_h,
R_0=sum_h |M_h|^2 r_h.
```

### Proof

TPC-245 makes every local set an exact disk under the dimension assumption.
TPC-244 gives weights `lambda_h=|M_h|^2`.  Theorem A applies.  QED.

## Theorem D: hard-window robust margin

In addition to Corollary C, assume all coefficient vectors lie in one finite
`delta`-separated frequency space and use the common TPC-243 synthesis map on
`N` consecutive integers.  Put

```text
epsilon = delta^(-1) H_floor(1/(2delta))/N.
```

Assume the fixed local moments and energies make the coefficient norms
`N_B=||B||` and `N_W=||W||` independent of the allowed local transverse
orientation.  For the selected covariance

```text
Q_I=N^(-1)<TW,TB>,
E=epsilon N_W N_B,
```

one has

```text
Q_I in C_0+(R_0+E)Dbar,
|Q_I| >= max(|C_0|-R_0-E,0).
```

Consequently, `|C_0|>R_0+E` implies uniform nonvanishing.  In that case all
selected covariances lie in the phase sector of half-angle
`arcsin((R_0+E)/|C_0|)` about `C_0`.

### Proof

TPC-243, with the orientation fixed by TPC-242, gives

```text
|Q_I-<W,B>| <= epsilon||W||||B||=E.
```

Corollary C places `<W,B>` in `C_0+R_0 Dbar`.  The triangle and reverse-triangle
inequalities place `Q_I` in the inflated disk and give the lower bound.
The strict condition makes that lower bound positive.  The phase claim is
Corollary B applied to the containing disk; it is a valid bound but is not
claimed sharp for the physical image.  QED.

## Proposition E: moment-data insufficiency obstruction

Within the blockwise product full-disk model of Corollary C, if
`|C_0|<=R_0`, the
fixed local longitudinal moments and transverse energies admit a realization
with aggregate coefficient covariance exactly zero.  Hence those data alone
cannot prove a uniform positive lower bound.

### Proof

Theorem A makes the aggregate feasible set the entire disk, and Corollary B
places zero in that disk.  QED.

## Exclusions and maximum status

A positive-radius circle is not silently replaced by a disk.  For example,
the sum of circles of radii two and one centered at zero is the annulus
`1<=|z|<=3`, not the radius-three disk.  Likewise, a coupled arithmetic source
need not realize the Cartesian product of its local projections.

Maximum status:

`PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY`.

The literal V59 two-lane attachment, canonical block directions, blockwise
product source realizability, payable moment/energy and norm bounds, arithmetic `L2`,
fixed-atom credit, strict `1/400`, full Gate B, and twin-prime conclusions are
all open.
