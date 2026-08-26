# TPC-270 derivation package

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST)

Let `w_N`, `g_(N,theta)`, and `P_3` be the finite literal objects of TPC-269.
For every listed row the projected residual norms are positive and the interval
engine supplies an outward rational enclosure

```text
[r_-,r_+] contains R_(N,theta)^2,
0 < r_- <= r_+.
```

The new endpoint-normalized observable is

```text
Xi_(N,theta) = (R_(N,theta)^2)^3 / N^10.
```

Because the cube is increasing on the positive half-line, exact interval
arithmetic gives

```text
Xi_(N,theta) in [r_-^3/N^10, r_+^3/N^10].
```

For two positive interval enclosures, division gives the outward ratio

```text
[a_-,a_+] / [b_-,b_+]
  = [a_-/b_+, a_+/b_-].
```

Thus the dyadic observable

```text
D(a,b) = Xi_(b,0) / Xi_(a,0)
```

is certified without taking a square root or introducing a floating-point
power. The identity

```text
Xi = (R^2)^3/N^10 = (R/N^(5/3))^6
```

is algebraic for positive `R`; the sixth-power representation is chosen solely
to make the finite certificate rational. A ratio below one and a ratio above
one therefore have their literal endpoint-normalized meanings, but neither is
an asymptotic monotonicity theorem.

The profile-control ratio uses the same scale, clock, cutoff, shell, and
projection in numerator and denominator. It isolates the finite effect of the
`theta=1/2` profile from the cross-scale effect.
