# RH-111: tail-energy exterior concentration

This directory contains:

> *Tail-Energy Exterior Concentration: Reducing the Trace-to-Spectral
> Four-Volume Penalty*

For `kappa4=e4(K*K)/(s1^2 s2^2 s3^2 s4^2)`, the universal bound is
`1 <= kappa4 <= binom(r,4)`.  RH-111 bounds the unobserved exterior
multiplicity from recent Frobenius tail energy and replaces the generic
`sqrt(binom(r,4))` trace penalty by `sqrt(kappa4_upper)`.

Archived fine results:

- actual `kappa4` lies between `1.0000000003` and `2.29093`, while the
  universal dimension reaches `35`;
- refined trace counts are `78/78`, `69/78`, `55/78` at
  `1e-8`, `1e-6`, `1e-4`;
- generic trace counts were `78/78`, `65/78`, `42/78`;
- the `1e-4` refined trace count now equals the spectral exterior count.

The result reduces the combinatorial loss but does not prove an all-level
physical concentration law.
