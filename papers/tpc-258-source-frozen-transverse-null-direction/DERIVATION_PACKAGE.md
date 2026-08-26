# TPC-258 derivation package

## 1. Target

TPC-257 produced two source-only descendant contrasts `z1,z2` with

```text
<zi,A_x beta>=-(9/2*kappa_i+o(1)) x^(7/6)/log^3(x),  i=1,2,
```

where `kappa1=L1/2`, `kappa2=L2/2`,
`L1=log(3456/3125)`, and `L2=log(884736/823543)`.  This paper asks whether
the explicit leading vector `(kappa1,kappa2)` can be removed by one fixed
linear combination.

## 2. Source-frozen null direction

For every real clock use exactly the four blocks and vectors of TPC-257.  Set

```text
L1=log(3456/3125),
L2=log(884736/823543),
LT=sqrt(L1^2+L2^2),
z_null=(L2*z1-L1*z2)/LT.
```

The coefficients are constants of the limiting block geometry.  They are
chosen before evaluating `beta`, `A_x beta`, a sign, a norm, or a finite
sample.  The only clock dependence is the source-only rank frame itself.

TPC-257 gives `<z1,z2>=0` and `||z1||=||z2||=1`.  Therefore

```text
||z_null||^2=(L2^2+L1^2)/LT^2=1,
<z_null,z0>=0.
```

The direction is thus a legitimate unit vector in the old midpoint-
transverse plane.

## 3. Exact leading cancellation

Write `S_x=x^(7/6)/log^3(x)` and

```text
c_i(x)=<zi,A_x beta>/S_x=-(9/2*kappa_i)+o(1).
```

Linearity and the definition of `z_null` give

```text
<z_null,A_x beta>/S_x
 = [L2*c_1(x)-L1*c_2(x)]/LT.
```

The limiting diagonal coefficient is

```text
L2*(-9/2)*(L1/2)-L1*(-9/2)*(L2/2)=0.
```

The two terms commute as real scalar logarithms, so this is an exact
symbolic cancellation, not a decimal coincidence.  The two boundary lanes
from TPC-257 are each `O_(psi,epsilon)(x^(55/48+epsilon))`; the null vector has
the same `O(x^(-1/2))` bounded variation because it is a fixed linear
combination of `z1,z2`.  Since `55/48<56/48`, those lanes are `o(S_x)` for
fixed `epsilon<1/48`.  Consequently

```text
<z_null,A_x beta>=o(S_x).
```

This is the unconditional source-backed statement inherited from the two
TPC-257 asymptotics.

## 4. Quantitative rate ledger

If the displayed TPC-257 `O(1/log x)` beta-contrast remainders and the
weighted-prime remainder are retained with the same rate, then

```text
<zi,A_x beta>=-(9/2*kappa_i)S_x
              +O(S_x/log x+x^(55/48+epsilon)).
```

The fixed null combination then satisfies

```text
|<z_null,A_x beta>|
  <<_{psi,epsilon,L1,L2} S_x/log x+x^(55/48+epsilon).
```

The proof package treats this as a rate compiler: the algebra is exact, but
the rate is conditional on reopening the source PNT error with an explicit
`O(1/log x)` interface.  No fixed-power saving follows from this line alone.

## 5. Why this is not Gate B

The cancellation removes one explicitly identified two-coordinate diagonal
vector.  It does not control:

```text
the rest of the infinite output,
the signed prime-shell reassembly,
the physical w lane,
the full arithmetic L2 norm,
or the global 1/400 budget.
```

An error sequence `e_i(x)=1/sqrt(log x)` is `o(1)` but produces a null
combination of size `S_x/sqrt(log x)`, which is larger than every fixed-power
saving `S_x*x^(-delta)`.  This adversarial model is not claimed to be the
literal V59 sequence; it is a quantifier firewall showing what the theorem
does not establish.

## 6. Route decision

The result is a genuine analytic structure: a source-frozen null direction
for the known transverse diagonal.  The next question is whether the same
direction cancels or controls the signed `w` coupling.  Until that is proved,
the route status remains `FULL_GATE_B=OPEN`, `L2=NONE`, and
`FIXED_ATOM_CREDIT=0`.
