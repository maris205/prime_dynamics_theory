# Roadmap after RH-358

RH-358 converts RH-357's endpoint localization into a probability law on
terminal lag.  The whole strict upper counterloop band is asymptotically
supported within (O(1)) coordinates of its terminal order, and the limiting
lag law is geometric with ratio (x^{-1}).  This is stronger than a pointwise
fixed-lag calculation: convergence holds in total variation and carries the
first two moments.

The truncation ledger is now exact.  Retaining the top (q) terminal
coordinates leaves relative error (P_k(q)/C_k).  A fixed width leaves the
nonzero limit (x^{-q}); the error vanishes exactly when (q\to\infty).
For sublinear widths the sharp error is (x^{-q}), while linear widths retain
the multiplier-drift factor (C_M^{q/k}), the denominator correction
(2/(2-q/k)), and the finite residual-depth factor near the lower endpoint.

The next read-only candidate is RH-359, **logarithmic terminal-window accuracy
thresholds**.  It should invert the RH-358 tail law at widths
(q_k=\lfloor a\log k/\log x+c\rfloor), retain the integer floor phase, and
classify polynomial target errors without promoting a finite deterministic
window to an actual-head spectral statement.

For physical transfer, the first blocker is unchanged: prove the original
unnormalized same-clock leaf (D_{4k}(R)\to0), or prove a typed direct/full
trace theorem with the correct open (q/E_{\rm off}) ledger.  RH-241 and
RH-288 remain open/inactive, Gates A--E remain false/open, and no statement
about Riemann zeros or RH follows.
