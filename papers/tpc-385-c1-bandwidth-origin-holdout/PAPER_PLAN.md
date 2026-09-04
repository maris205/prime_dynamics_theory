# TPC-385 paper plan

## Research question

Does the high-bandwidth `c=2,3` phase observed in TPC-384 survive a genuinely
fresh, response-blind origin holdout when the pooled normalization scalar is
estimated only from a predeclared calibration subset?

## Design

Freeze five origins on a new affine grid. Designate the first three as the
calibration subset and the last two as the holdout subset before any response
or geometry readout. Keep `N=512`, four blocks, beta `2`, exponent `1`, height
`66`, four sign laws, and the high-bandwidth/Q menu `c=2,3`, `Q=2048,8192`.
Compare local-diagonal normalization with a pooled scalar built only from the
calibration origins. Lock the TPC-384 all-plus high-Q values as forecasts.

## Claim-bearing outputs

1. Exact finite selection protocol, role split, and coordinate-disjointness.
2. A 160-row complete calibration/holdout certificate and 32 cell census.
3. Calibration-only pooled normalization, excluding holdout geometry.
4. Four predeclared all-plus high-Q parent-forecast errors.
5. Independent reverse-shell replay, rational anchor, mutation firewall, and
   fail-closed local Bridge-B checker.

## Anticipated boundary

The audit can test finite transfer of a declared numerical profile. It cannot
prove a source-valid normalization, select an arithmetic law, establish
bandwidth/origin/count uniformity, pay a fixed-power saving, or yield a
twin-prime conclusion.

## Next decision rule

If all-plus high-Q transfer remains under the predeclared cap but signed laws
remain unstable, test a count holdout at fixed high bandwidth. If the new
count breaks transfer, preserve that as the scale obstruction rather than
retuning the normalizations.
