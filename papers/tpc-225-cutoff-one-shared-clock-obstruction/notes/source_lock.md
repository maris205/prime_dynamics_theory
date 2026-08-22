# TPC-225 source lock

```text
clock = source_surrogate
x = Q^3
H = 4Q^2
h = 4Q
active labels = primes Q<q<=2Q
packet count = J=4
normalization = C_h=1/h
row support = m=+1 and m=-1 only
profile fixture = psi_j(t)=1+s_j t, s=(0,1,-1,2)/10
```

The source clock is inherited as a finite modeling choice from TPC-224. It is not asserted
to be the V46 asymptotic clock. The collision-stress clock from TPC-224 is not used here and
is not spliced into this audit.

The physical fixed atom remains `h0=2` in the global TPC route, but this paper does not claim
that the finite modulus `h=4Q` is that physical atom or that it controls the fixed-`h0`
carrier.
