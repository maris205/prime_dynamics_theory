# TPC-268 paper plan

## Question

TPC-267 found a quarter contraction for a finite literal V59 residual using
the coarse z=2 shifted-prime comparison. Is that contraction stable under
the declared finite interface choices, or can a nearby cutoff/profile/clock
change reverse it?

## Object held fixed

The prime shell, outer q weight, unit masks, deleted diagonal, beta source,
four-block rank-three projection, and interval protocol are unchanged from
TPC-267. Only the comparison cutoff z, rounded clock H, and kernel exponent
s are varied in a declared finite family.

## Claim-bearing experiments

1. Six matched z=2 controls reproduce the TPC-267 first-profile rows.
2. Three H values at (N,Q,s,z)=(64,4,1,3) test local clock stability.
3. Matched z=3 rows at N=64 and N=96 test cutoff sensitivity.
4. An s=2,z=3 row is a kernel control, and an s=1,z=5 row tests a
   larger cutoff.
5. The remaining larger rows test whether the obstruction is universal.

## Intended result class

NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION.
The paper may refute a universal quarter bound on this finite parameter
family. It may not refute the source-specified growing V59 theorem, infer a
power saving, or claim a twin-prime result.

## Follow-up

The next paper must test the growing local cutoff and a source-specified
smooth profile before any finite phase behavior is promoted.
