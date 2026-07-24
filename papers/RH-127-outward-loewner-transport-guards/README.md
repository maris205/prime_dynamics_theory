# RH-127: outward Loewner transport guards

RH-127 turns independently rounded matrix assemblies into rigorous RH-123
hypotheses.  If source and target matrices have spectral-norm radii, then
congruence by `S` amplifies source radii by exactly `||S||^2`.  A numerical
Gram slack is certified after subtracting

```text
r_G' + a ||S||^2 r_G,
```

and the tail slack after subtracting

```text
r_D' + ||S||^2 (b r_D + delta r_G).
```

The guards are sharp in dimension one.  The 4,096-instance audit has zero
false certifications.  Physical all-level radii remain to be constructed.

