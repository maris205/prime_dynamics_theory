# RH-288: Prefix-tail determinant gluing criterion

Let

```text
F_sigma(z) = exp(-sum_(n>=2) b_(sigma,n) z^n/n),
F(z)       = exp(-sum_(n>=2) a_n z^n/n).
```

For a moving cut `m_sigma`, define on radius `R`:

```text
P_sigma = sum_(2<=n<m) |b_(sigma,n)-a_n| R^n/n,
S_sigma = sum_(n>=m) |b_(sigma,n)| R^n/n,
T_sigma = sum_(n>=m) |a_n| R^n/n.
```

If all three quantities tend to zero, then

```text
sup_|z|<=R |F_sigma(z)/F(z)-1|
 <= exp(P_sigma+S_sigma+T_sigma)-1 -> 0.
```

For the typed spectral application, `b_(sigma,n)` is the modulus-complement
trace `tau_(sigma,n)`.  If `c=h+tau` is the total noisy trace split into head
and complement, `s` is the finite-radius counterloop moment, and `a` is the
target anchor, then

```text
tau-a = (c-s-a) - (h-s).
```

Thus `P_sigma` can be proved directly, or bounded by two weighted budgets:
the total-trace/counterloop/anchor error and the head/counterloop error.
RH-285 supplies the complement tail and RH-267/RH-268 supply the target tail.
RH-287 supplies only an unweighted, rate-free version of the first prefix
error; the second weighted error is also open.  The gluing theorem is not yet
activated.

No finite coefficient fit or head transport alone can substitute for the
typed vanishing prefix and the two tail budgets.
