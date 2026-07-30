# RH-285: Uniform `det_2` tail derivative envelope

The RH-282 trace estimate controls more than the scalar logarithmic tail.  If

```text
|tau_n(sigma)| <= M_sigma q^(n-2),
M_sigma <= C sigma^(-alpha),
q R < 1,
```

then every fixed derivative of

```text
E_(sigma,m)(z) = sum_(n>=m) tau_n(sigma) z^n/n
```

has the uniform bound

```text
sup_|z|<=R |E^(s)(z)|
 <= C_(s,qR) M_sigma q^(-2) R^(-s)
    m^(s-1) (qR)^m.
```

Thus any logarithmic clock strictly above the RH-283 critical slope forces
the tail canonical product to converge to `1` in every fixed `C^s` norm on
the closed disk.  With `alpha=1`, `q=1/2`, `R=7/5`, and slope `4`, the
power gain is `sigma^0.426699...`, up to logarithms.

This is a theorem for every fixed derivative order; its constants are not
uniform in the derivative order.  It controls the projection-free
complementary factor, not the finite spectral head or its relation to the
monodromy counterloop.
