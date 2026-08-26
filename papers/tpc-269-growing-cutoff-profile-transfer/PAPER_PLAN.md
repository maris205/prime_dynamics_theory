# TPC-269 paper plan

## Question

TPC-268 showed that a fixed finite comparison cutoff can flip the quarter
classification. The next minimal question is whether the flip survives when the
cutoff follows a declared scale rule and the kernel is moved along a convex
family of nonnegative normalized profiles.

## Frozen object

The prime shell, outer q weight, unit masks, deleted diagonal, beta source and
rank-three four-block projection are inherited from TPC-268. The only new
interface is the finite growing proxy

```text
z_N = floor(log N)
psi_theta = (1-theta) psi_1 + theta psi_2, 0 <= theta <= 1
K_theta = (1-theta) K_(H,1) + theta K_(H,2).
```

The registered scales use z_N=(4,4,4,5,5,5) for
N=(64,96,128,192,256,384).

## Claim-bearing rows

Six theta=0 rows test the growing-cutoff proxy across scale. Six additional
rows test the profile path at theta=9/10, 24/25, 1, and 1/2.

## Intended result class

`NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER`.
The result is allowed to refute a universal claim over the declared finite proxy
family. It cannot be promoted to the source-level growing V59 theorem, an
asymptotic radius estimate, a fixed-power saving, or a twin-prime result.

## Follow-up

If the profile path remains threshold-sensitive, the next paper should test
cross-scale normalization and radius growth rather than add more finite profile
choices.
