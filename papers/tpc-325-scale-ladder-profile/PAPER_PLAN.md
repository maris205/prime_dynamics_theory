# TPC-325 paper plan

## Question

Does the TPC-323 all-plus profile-majorization readout persist when source
cardinality, rather than source location, is the controlled variable?

## Frozen design

Use the locked TPC-324 literal block engine, one new source origin `12001`, and
the nested source intervals `[12001,12000+N/2]` for
`N={320,640,1280,2560}`.  Cross this ladder with
`Q={24,36,54,80}`, exponents `{1,2}`, and four declared sign laws.

## Claim-bearing outputs

1. A finite 32-row all-plus majorization certificate.
2. A scale-by-scale census for the three alternative laws.
3. Outward lower TV and upper energy envelopes, with a strict four-rung trend
   if the computed gaps survive the numerical guard.
4. An exact rational 16-point anchor at the new source origin.

## Failure policy

Any unresolved row, nonpositive trace, path disagreement, broken nesting,
source overlap, or failed normal/optimized equality downgrades the intended
claim to an obstruction and prevents release markers from being asserted.

## Follow-up decision

If all-plus survives, the next minimal question is a disjoint second ladder or
a source-native signed arithmetic `L2` bridge.  If it fails, locate the first
scale and record the scale obstruction rather than fitting a trend.
