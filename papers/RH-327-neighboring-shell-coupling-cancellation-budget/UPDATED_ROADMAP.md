# Roadmap after RH-327

RH-327 supplies the first actual cyclic data slots for the physical sibling
partition:

```text
T_(sigma,2k) = B_(sigma,k) + S_(sigma,k) + R_(sigma,k).
```

This is an exact basepoint-localized trace identity.  It is not yet a useful
asymptotic replacement because the shell magnitude and the far remainder are
uncontrolled.  In particular, RH-19's equal sibling `L2` mass and RH-323's
oriented affine probability law do not determine these cyclic observations.

The exchange completion makes the missing datum explicit.  At fixed
reference contrast `c0`, a proposed shell model

```text
X = L * (c^(2k) - c0^(2k))
```

can hit only

```text
I = [-L*|c0|^(2k), L*(1-|c0|^(2k))].
```

For the RH-326 demand

```text
D = A - P - B,
```

the best exchange-model residual is exactly `dist(D,I)`.  This is a
necessary best-case reachability test, not the actual mismatch at the
physical contrast.  Allowing `c0` to vary enlarges the information class but
is not a legitimate physical matching operation.

RH-328 should now attempt the fixed-reference joint equation while retaining
all of the following fields:

1. `sigma`, `k`, period `2k`, and target `k*R^(-2k)`;
2. phase `eta`, clearance `d`, and the RH-19 window radius;
3. `(V,U,W)`, orientation `(+,-,+)`, and shift `kappa_aff*d`;
4. the actual localized observations `B`, `S`, and `R`;
5. parity packet `P` and counterloop alias defect `A` with signs `+P-A`;
6. a fixed deterministic shell reference, not a freely optimized one;
7. the trace-observation norm and every RH-325 prefix/suffix Duhamel weight;
8. the necessary reachability screen

```text
dist(D,I) = o(k*R^(-2k)).
```

9. an identified physical contrast `c_phys` and the certified bounds

```text
|X(c_phys;c0)-D| = o(k*R^(-2k)),
R                 = o(k*R^(-2k)).
```

If the physical observation or contrast cannot be identified, RH-328 should
record a conditional matching equation or a scoped negative result.  It may
not infer matching from branch-blind probability accuracy, finite exchange
diagnostics, or separate absolute majorants.  Gates A--E remain false/open.
