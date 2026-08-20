# Theorem Ledger

## PROVED

`T214.1` - For `h|d`, the smooth reciprocal emitter is dilation-covariant:
`B_d((d/h)r)=B_h(r)`.

`T214.2` - On a complete `lcm(D)` period, the common-source physical Gram is
exactly diagonal in reduced rational-frequency denominator clusters.

`T214.3` - The coefficient of a reduced denominator `h` is the Mobius-log tail
`C_h=sum_(d in D:h|d) mu(d)log(d)/d`.

`T214.4` - If `max(Q)<H`, all zero-frequency rows vanish.

`T214.5` - The exact four-packet polarization identity commutes with the cluster
reduction and preserves the signed coefficients.

## PROVED_EXACT_FINITE_SIGN

With `psi(t)=(1+t^2)^(-2)`, `Q={11,13,17}`, and `H=40`, the exact rational
rows prove that `D={5,7,35}` has a strictly negative total cross term: the
only nonzero cross-Gram pairs join the negative prime coefficients to the
positive two-prime coefficient.  For `D={3,5,7,105}`, every coefficient is
negative and at least one cross-Gram is positive, so the total cross term is
strictly positive.

## NUMERICAL_OBSERVATION

Numerical evaluation of the logarithms gives the reported finite energy ratios.
The decimal values are reproduction diagnostics, not theorem certificates.

## REFUTED_SCOPED

`T214.R1` - The shared-frequency cluster reduction does not have a universal
favorable sign.  The first fixture has ratio below one; the composite-quotient
fixture has ratio above one.

## OPEN

Uniformly bound the actual V46 cluster sum in
`Y0<d<=U`, with the prime shell, smooth physical profile, four-packet
reassembly, and all endpoint normalizations retained.

## Status

```text
CLAIM_LEVEL = PROVED_STRUCTURAL_L1_MOBIUS_CLUSTER_REDUCTION
TPC214_ROUTE_ADVANCE = YES
TPC214_ARITHMETIC_ADVANCE = NO
TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC214_FIXED_ATOM_CREDIT = 0
TPC214_L2 = NONE
```
