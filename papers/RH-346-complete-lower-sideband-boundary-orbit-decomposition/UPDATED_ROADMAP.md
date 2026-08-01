# Roadmap after RH-346

RH-346 completes the physical period-`2(k-1)` boundary-orbit extraction at
the first lower sideband while retaining the original `(sigma,k)` noise
clock.

The exact direct coefficient is

    p_(sigma,k,2m)
      = Y_m^- + P_(sigma,2m) - S_m^-,

where

    m=k-1,
    Y_m^-=T_(k,m)^rest-d_(sigma,k,2m),
    S_m^-=F_m^orb+A_(k,2m).

The complete orbit dominates its radial correction only relatively:

    S_m^-/F_m^orb -> 1,
    A_(k,2m)/F_m^orb=(C_M-1)/m+o(1/m).

This does not make the radial term target-negligible.  The single point
omitted by RH-339 is definitely super-target, so neither the partial orbit nor
the radial term may be dropped from a target-scale identity.

The next RH-347 scalar interface is

    P_(sigma,2m)/S_m^- -> C_* C_M lambda^(eta-1).

The unique symbolic lower scalar balance is therefore

    eta_- = 1 - log(C_* C_M)/log(lambda).

RH-347 may prove a scoped scalar-only obstruction off this phase and an exact
information-class underdetermination at the balance phase, analogous in
logic but not normalization to RH-345.  It must keep the radial sideband in
the exact demand and must not claim actual lower nonclosure without a theorem
for `Y_m^-`.

After RH-347, RH-348 must return to the punctured aggregate containing every
remaining order in `2<=n<4k`, `n notin {2k,2k-2}`.  Closing the critical and
first lower scalar mechanisms would still not control that aggregate.

Actual critical compensation, actual lower compensation, `E_off,(4k)`, head
transport, the direct prefix, RH-288, and Gates A--E remain open.
