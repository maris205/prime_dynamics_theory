# TPC-241 derivation package

## Scale identities

Using exact fractions,

```text
4Q/H=x^(-31/96),
UQ/H=x^(23/2400),
Q^4/H^2=x^(1/48),
U^4/N^2=x^(-67/100+o(1)).
```

The first two inequalities guarantee primitive support and a uniformly growing
lattice depth on the top shell.  The third is the collision power.  The fourth
makes the finite-window lower-frame defect negligible.

## Constant ledger

The shell-prime first moment contributes `3/2`.  Squaring contributes `9/4`.
The top-prime weighted average contributes `log(2)log U`.  Finally,

```text
log U/(log Q)^2
 =(399/400)(1/log Q)
 =(399/400)(3/log x).
```

Therefore

```text
(9/4)(399/400)3=10773/1600.
```

The normalized finite-window lower frame tends to `1/2`, so its leading
liminf constant is `10773/3200`.

## Order-of-operations firewall

The finite-window quadratic form has off-frequency cross terms.  They may have
either sign.  The legal argument is

```text
complete coefficient vector
 -> TPC-238 lower frame
 -> nonnegative complete coefficient norm
 -> restrict that norm to top primes.
```

The illegal argument would discard physical-window cross terms before applying
the frame.  No certificate may substitute the illegal order.

## Quantifier ledger

The theorem is profilewise.  For each fixed admissible `psi`, all Riemann-sum
constants are fixed and the asymptotics hold beyond a profile-dependent
threshold.  No uniform threshold over the entire infinite-dimensional profile
class is claimed.  The fixed-power refutation quantifies over each fixed
`psi`, each fixed `delta>0`, and each fixed real `A`.
