# TPC-332 proof and scope package

## Proposition 1 — mean/centered quadratic identity

For finite vectors `w_j`, let `vbar=mean_j w_j` and `z_j=w_j-vbar`.  For any
real matrix `A`,

```text
mean_j ||A w_j||_2^2
  = ||A vbar||_2^2 + mean_j ||A z_j||_2^2.
```

**Proof.** Expand `A w_j=A vbar+A z_j`, sum the squared norms, and use
`mean_j z_j=0` to cancel the cross term.  ∎

## Proposition 2 — signed-Gram specialization

Taking `A=C_e` gives the energy identity.  Taking the diagonal matrix whose
`t`-th entry is `sum_u C_e(u,t)^2` gives the coordinate-diagonal identity.
Subtracting the latter from the former gives the off-diagonal identity.  All
three statements are exact finite algebra.

## Proposition 3 — source polarization

For the finite source vectors `lambda`, `b`, and `beta=lambda-b`,

```text
||beta||_2^2 = ||lambda||_2^2 + ||b||_2^2 - 2 <lambda,b>.
```

This is an exact finite inner-product identity.  The producer and independent
checker evaluate the four terms on six source windows; the largest replay
identity error is `1.4551915228366852e-11`.  The status is
`PROVED_EXACT_FINITE_FLOAT64_REPLAY` for the recorded implementation, with the
underlying source formula remaining a declared finite model.

## Proposition 4 — finite growing-ensemble certificate

The TPC-332 certificate contains 48 unique rows (`2*3*4*2`) and 192
law-level decompositions.  The independently recomputed component census is:

| law | average | coherent | centered |
|---|---:|---:|---:|
| all-plus | 0− / 48+ | 1− / 47+ | 0− / 48+ |
| alternating index | 31− / 17+ | 38− / 10+ | 29− / 19+ |
| mod-4 character | 48− / 0+ | 44− / 4+ | 47− / 1+ |
| half split | 48− / 0+ | 39− / 9+ | 48− / 0+ |

There are no unresolved observations under the declared guard.  This
proposition is `NUMERICALLY_CERTIFIED_FINITE`; it is not a growing theorem.

## Scope boundary and obstruction

The all-plus average and centered components are positive throughout this
finite ensemble, but the unpermuted residual sign is mixed (`27−/21+`).  Thus
the exact control-orbit decomposition survives the new windows while a
canonical residual sign does not.  The source `L2` growth factors are finite
descriptors only.  No source-uniform estimate, fixed-power credit, Route-A or
Route-B pass, or twin-prime conclusion follows.

## Reproducibility evidence

The producer rebuilds the certificate from the TPC-331 hash lock.  The
independent checker uses a separate reverse shell accumulation and independent
factorization path.  The stress suite checks canonical JSON, row geometry,
source-L2 fields, exact-anchor digests, claim firewall, and five deliberate
mutations.  The local Bridge-B wrapper repeats the checks in normal and
optimized modes and requires identical stdout with empty stderr.
