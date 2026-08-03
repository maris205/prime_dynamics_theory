# Roadmap after RH-354

RH-354 closes the parity-free high-order direct channel at the normalized
near-alias scale.  For every sublinear depth `L_k=o(k)`, one theorem now
controls the actual coefficient `p=tau-a` at all orders from `2k-L_k` onward.
Thus all odd and even orders above the moving cut, including the critical and
eventually the first-lower coordinate for growing depth, no longer require
separate normalized modulus-cap arguments.

The theorem is deliberately a direct-coefficient statement.  It does not
close the full-trace channel because

    p_(sigma,k,n) = q_(sigma,k,n) - d_(sigma,k,n).

The next narrow positive routes are therefore:

1. a same-clock normalized head-defect theorem on the near-alias band,
   permitting transfer from the new direct budget to the corresponding
   full-trace budget;
2. a theorem for the low-order direct prefix `2<=n<2k-L_k` that can be joined
   to RH-354 without changing data type or normalization;
3. a direct physical annular theorem strong enough to control the whole
   complement-to-anchor prefix at once.

The separate absolute source bounds cannot remove the `x^(-k)` normalization:
their noisy root is already superunit at `L_k=o(k)`.  Any unnormalized advance
must use cancellation or finer spectral information about the actual
difference `tau-a`.

RH-288 remains inactive until the complete direct prefix and both analytic
tails close in one physical determinant data type.  RH-241's moving noisy
all-order envelope and coefficient bridge remain open.  Gates A--E remain
false/open, and no conclusion about the Riemann Hypothesis follows.
