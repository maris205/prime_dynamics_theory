# TPC-311 paper plan

## Title

Declared Stratification and Tolerance-Slice Holdout Replication in a Prime-Shell Diagnostic

## Question

TPC-310 showed that a global preference can reverse when the same finite rows
are aggregated with different weights.  Can one fixed, balanced design rule
survive a tolerance slice that is held out before aggregation?

## Frozen input

Use the released TPC-310/TPC-309 certificates only.  The numerical source is
the 162-observation TPC-309 envelope atlas: three profile ladders, three
adjacent transitions, two kernel exponents, three tolerances, and three
completion radii.  Do not regenerate target labels or alter shell partitions.

## Declared finite protocol

1. Fix a design stratum `(transition, exponent, tau, radius)`.
2. Pool the LOW/BASE/HIGH profile-ladder completion extrema within that
   stratum before taking the right/left ratio.
3. Give every resulting design stratum equal arithmetic weight.
4. Treat `tau={0.25,0.5}` as calibration and `tau={0.75}` as a held-out
   parameter slice.  Use radius zero as the primary native endpoint and
   radii one and two as adversarial stress controls.

## Claim target

Prove the two-stage interval protocol and the finite tau partition.  Reproduce
the primary native calibration/confirmation classes and record whether the
fixed rule replicates.  Add exponent, transition, and leave-one-profile
controls to locate the obstruction.

The protocol is declared inside this child project; it is not claimed to be
an externally timestamped preregistration.  The confirmation slice is also
not a new physical sample: it is a disjoint parameter slice of one locked
parent atlas.

## Deliverables

`README.md`, proof and derivation packages, theorem ledger, claim firewall,
computational protocol, citation note, producer, independent checker, exact
rational stress suite, canonical JSON certificate, Bridge-B checker, and
compiled `paper/paper.pdf`.
