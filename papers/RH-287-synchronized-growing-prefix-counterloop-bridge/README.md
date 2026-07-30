# RH-287: Synchronized growing-prefix counterloop bridge

RH-272 gives convergence at every fixed trace order.  A diagonal selection
argument upgrades this to a genuine, but rate-free, growing prefix.

Let `c_(sigma,n)` be the actual noisy parity-extracted trace coefficients,
let `s_(k,n)` be the finite-radius monodromy counterloop moments, and let
`a_n` be the deterministic numerator anchor.  There exist clocks
`h_sigma -> infinity` and `k_sigma -> infinity`, with
`h_sigma < 2 k_sigma`, such that

```text
max_(2 <= n <= h_sigma)
|c_(sigma,n) - s_(k_sigma,n) - a_n| -> 0.
```

The proof synchronizes the fixed-order small-noise limit with the finite
monodromy radius law.  It uses no finite fit and is an asymptotic theorem for
the actual noisy trace sequence.

The clock has no explicit rate, and an unweighted maximum on a growing prefix
does not control the exponentially weighted sum required on a disk with
radius greater than one.  It therefore strengthens the graded coefficient
bridge without identifying a noisy spectral cloud or completing Gate A.
