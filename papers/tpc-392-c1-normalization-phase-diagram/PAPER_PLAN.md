# TPC-392 paper plan

## Question

Does the finite forecast phase observed after TPC-391 depend materially on the
declared normalization, and can that dependence be separated from the frozen
parent slope interface?

## Predeclared design

* Use the fresh grid `3800001 + 401 j`, with indices `0,10,20,30,40`.
* Use the first three origins for calibration at `N=1024,1280` and the last
  two origins only for the terminal holdout `N=1536`.
* Keep the fixed-three-block band, both Q anchors, and all four sign laws.
* Compare local diagonal, pooled-train scalar, origin scalar, and frozen
  train-1024 scalar normalizations.
* Fit a log2 slope from the two calibration means and forecast the fixed
  terminal holdout.  A phase pass means absolute ratio error at most `0.03`.

## Claim-sized contribution

The contribution is a complete finite normalization phase diagram with a
response-blind role split, a coordinate-disjoint family, a reverse-shell
replay, and an adversarial mutation contract.  It identifies one scoped
high-$Q$ alternating/local-diagonal failure and a three-way scalar pass, while
preserving the distinction between a finite diagnostic and a source-valid
analytic normalization.

## Decision rule

If all normalizations agree, the next experiment should attack origin or
holdout uniformity.  If one normalization separates, first test whether the
separation survives a fresh adversarial family.  The observed outcome selects
the latter: `ROUND2_CLUE=TEST_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT`.

## Non-claims

No source-valid growing normalization, uniform operator estimate, arithmetic
L2 estimate, Route-A closure, Route-B reassembly, or twin-prime conclusion is
asserted.
