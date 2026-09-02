# TPC-358 paper plan

## Question

Does the finite normalized operator cap observed on the TPC-356 selected
origins transfer to a fresh, widely separated origin panel?

## Frozen design

Fix origins `52001+100000j`, `j=0,1,2`, before reading any matrix.  Replay
counts `256,512,1024,2048`, shell anchors `24,54,80`, exponents `1,2`, and
the four inherited sign laws.  Record Schur and Frobenius envelopes on every
raw/normalized row and exact extreme eigenvalues for all-plus rows.

## Decision rule

The parent thresholds are `normalized Schur < 0.83` and `normalized all-plus
spectral < 0.64`.  If the fresh panel remains inside them, report finite
transfer only; if not, retain the first violation as an obstruction.  A
nonincreasing spectral ladder is separately tested with guard `10^-6`.

## Claim budget

The paper can establish finite parent-compatible transfer and a finite
monotonicity obstruction.  It cannot claim an origin-uniform bound, source
arithmetic `L2`, fixed-power credit, Route-B passage, or a twin-prime result.
