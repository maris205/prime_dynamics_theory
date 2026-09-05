# TPC-393 paper plan

## Question

Does the high-$Q$ alternating-index/local-diagonal separation exposed by
TPC-392 survive a fresh, response-blind coordinate family, and which part of
the finite signal is forecast instability versus origin instability?

## Predeclared design

* Use the fresh grid `4200001 + 401 j`, with selected indices
  `0,10,20,30,40`.
* Use the first three origins for calibration at `N=1024,1280` and the last
  two only for the terminal holdout `N=1536`.
* Keep the fixed-three-block band and all four normalization definitions.
* Restrict the adversarial panel to `Q=8192` and the all-plus control versus
  alternating-index target.
* Fit a log2 slope from the two calibration means and forecast the terminal
  holdout.  A forecast pass means absolute ratio error at most `0.03`.
* Record the one-percent origin-spread diagnostic and the fixed spectral and
  Schur envelope flags without promoting either to an analytic estimate.

All choices above were fixed before current responses were read.  The TPC-392
certificate is a frozen provenance/interface parent only; no parent response
or slope enters the current fit.

## Claim-sized contribution

The contribution is a fresh finite adversarial replication with an explicit
negative result: the prior forecast-cap separation does not recur on this
family, but the alternating law remains origin-unstable at the one-percent
level and the spectral cap fails universally.  This separates a failed
forecast anomaly from a persistent finite origin diagnostic while retaining a
fully auditable positive control.

## Decision rule for the next project

If the forecast separation is not reproduced, stop treating it as a robust
normalization phase and test the remaining origin-uniformity signal directly.
If it is reproduced, use a fresh family again before any analytic
interpretation.  The observed result selects the first branch:
`ROUND2_CLUE=TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION`.

## Non-claims

No source-valid growing normalization, uniform operator estimate, arithmetic
$L^2$ estimate, Route-A closure, Route-B reassembly, fixed-power credit, or
twin-prime conclusion is asserted.
