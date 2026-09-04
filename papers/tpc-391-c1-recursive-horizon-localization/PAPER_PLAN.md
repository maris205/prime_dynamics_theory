# TPC-391 paper plan

## Question

Does the TPC-390 frozen c=1 slope interface first fail at an intermediate
count horizon, or only at the terminal holdout horizon?  The answer must
separate a parent-interface error from a same-family local trajectory.

## Predeclared design

* Use the fresh grid "3400001 + 401 j", 0 <= j < 41, with indices
  0,10,20,30,40.
* Use origins 3400001,3404011,3408021 for calibration and
 3412031,3416041 as fixed terminal holdouts.
* Read calibration lengths 1024,1152,1280,1408; read holdouts only at
  1536.
* Freeze every TPC-390 cell slope before reading current responses.
* Retain both fixed_c3 and full_relative bands, both Q anchors, all four
  sign laws, and both existing normalizations.
* Define first crossing as the first declared horizon with absolute forecast
  error greater than 0.03.

## Claim-sized contributions

1. A fresh coordinate-disjoint family with a four-level calibration ladder.
2. A horizon trajectory that distinguishes intermediate stability from terminal
   failure.
3. A response-blind first-crossing census over all 32 parent cells.
4. A separate local-control trajectory and an exact staged/direct identity.
5. A reverse-shell replay, mutation firewall, and hashed parent interface.

## Decision rule

If a parent cell crosses before 1408, classify the obstruction as an
intermediate-horizon failure.  If crossings occur only at 1536, classify the
result as terminal-horizon localized.  If local controls cross in the same
locations, retain normalization/geometry as unresolved; if they do not, retain
the frozen parent slope as the scoped suspect.  These are finite diagnostic
labels, not asymptotic claims.

## Follow-up

The current follow-up is a normalization phase diagram: hold the trajectory and
parent interface fixed while varying the scalar normalization in a new,
response-blind panel.  Source-valid growing control and arithmetic L2 remain
open in either branch.
