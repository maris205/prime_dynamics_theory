# TPC-273 paper plan

## Question

After TPC-272 identified the correlation margin as a required endpoint input,
is that margin stable under the declared finite cutoff, clock, and kernel
choices on the same literal V59 physical operator?

## Experiment

Freeze `(N,H,Q)` at `(64,15,4)`, `(96,20,5)`, `(128,24,5)`, and `(192,32,6)`.
Enumerate `z in {2,3,4,5}` and kernel exponents `s in {1,2}`.  The parent
engine supplies outward intervals for the residual scalar and radius.  Since
`m^2=|C_perp|^2/R^2=rho^2`, classify the margin using exact thresholds
`m<1/8` (`m^2<1/64`) and `m>1/4` (`m^2>1/16`).

## Claim ceiling

- `NUMERICALLY_CERTIFIED_FINITE`: 32 rows, their margin bands, and phase
  census;
- `REFUTED_SCOPED`: uniform stability of this declared finite parameter family;
- `OPEN_ASYMPTOTIC`: growing-cutoff margin uniformity and source-level theorem.

No finite flip is promoted to an asymptotic counterexample, fixed-power
credit, arithmetic `L2`, full Gate B closure, or a twin-prime result.
