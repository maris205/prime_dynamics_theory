# TPC-246 paper plan

## Question

What is the exact aggregate feasible set when the independently realizable
local covariance disks from TPC-245 are combined with arbitrary complex
weights, and what survives after the TPC-243 hard-window error is paid?

## Main contribution

1. Prove the exact finite weighted Minkowski identity
   `sum_h lambda_h(c_h+r_h Dbar)=C+R Dbar` with
   `C=sum_h lambda_h c_h` and `R=sum_h |lambda_h|r_h`.
2. Derive exact aggregate cancellation, minimum-modulus, and phase-sector
   criteria.
3. Specialize to the TPC-244 common-multiplier weights `|C_h|^2`.
4. Inflate the aggregate radius by the TPC-243 hard-window bilinear error and
   prove a conditional robust nonvanishing margin.
5. Prove an insufficiency obstruction: local moment/energy data alone cannot
   force nonvanishing when the aggregate disk contains zero.

## Claim boundary

The exact identity requires a Cartesian product of local feasible disks.  A
one-dimensional transverse block supplies a circle rather than a disk, and an
arithmetic source may couple blocks.  The V59 two-lane attachment, source-native
block directions, payable norms, and a positive arithmetic margin remain open.
