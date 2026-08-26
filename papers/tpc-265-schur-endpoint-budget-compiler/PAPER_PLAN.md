# TPC-265 paper plan

## Research question

TPC-264 identifies the exact Schur disk for the residual left by TPC-263.
TPC-265 asks how that disk enters the endpoint ledger: what is the sharp
worst-case size of the reassembled scalar, and exactly what power saving in the
radius is needed to pay the inherited `1/400` gap?

## New theorem

For a projected center `c` and an admissible residual disk of radius `R`, prove
that the worst-case full scalar is exactly `|c|+R` (and record the sharp lower
edge).  Combine this with the baseline/target exponents to obtain a
Schur-derived two-lane endpoint compiler.  The compiler must separately label
fixed-log center control, fixed-power radius control, and phase-restricted
control.

## Distinct contribution

TPC-261 gave an abstract finite-lane budget rule.  TPC-264 gave the residual
feasible set.  This paper is the exact interface theorem between them: it shows
that the Schur residual contributes a radius lane with no hidden cancellation
credit, and that a phase theorem is an additional datum rather than a
consequence of the Gram bound.

## Deliverables

1. Proof package and theorem ledger.
2. Exact Gaussian-rational radius/endpoint certificate.
3. Independent and stress checkers, including strict/borderline/loss cases.
4. PDF and claim firewall with no literal prime-shell or twin-prime upgrade.
