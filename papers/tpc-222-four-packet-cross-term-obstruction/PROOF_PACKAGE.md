# TPC-222 proof package

## Theorem 1: packet Gram positivity

For vectors `V_0,...,V_3` in a complex Hilbert space, `G_(j,l)=<V_j,V_l>` is Hermitian
positive semidefinite and `||sum_j c_jV_j||^2=c^*Gc`.

## Theorem 2: four-point polarization

For all `x,y`,

```text
<x,y> = 1/4 sum_(r=0)^3 i^(-r)||x+i^r y||^2.
```

This is an exact identity, not an estimate.

## Theorem 3: trace envelope and scoped non-identifiability

`0<=c^*Gc<=tr(G)||c||^2`. The upper endpoint is attained by a rank-one aligned Gram.
The two exact fixtures `s^+` and `s^-` have identical diagonal/trace but target energies
`16` and `0`; hence diagonal/trace information alone cannot certify signed reassembly.

All arithmetic in the certificate is exact Gaussian-rational arithmetic. No claim about the
growing prime shell is made.
