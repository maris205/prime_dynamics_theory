# Roadmap after RH-347

RH-347 closes only the scalar parity mechanism at the mandatory lower
sideband `2m=2k-2`.

The exact physical coefficient remains

    p_(sigma,k,2m)=Y_m^-+P_(sigma,2m)-S_m^-,

with

    Y_m^-=T_(k,m)^rest-d_(sigma,k,2m),
    S_m^-=F_m^orb+A_(k,2m),
    S_m^-/F_m^orb->1.

If the actual `Y_m^-` is target-negligible, parity misses the complete lower
demand at every fixed phase away from

    eta_-=1-log(C_*C_M)/log(lambda),

and the single weighted lower term diverges at the exact leading rate proved
in the paper.  At the balance phase, the available relative `o(1)` law is
exponentially too weak, and two exact scalar parity envelopes with the same
square-root law give zero versus divergent target behavior.

This does not decide the actual lower coefficient.  The scalar envelopes are
not noisy operators, and no theorem estimates the physical signed remainder
`Y_m^-`.  The decimal phase value is not a directed interval result and does
not itself remove the balance phase from the canonical window.

The next RH-348 route is the punctured one-alias aggregate on the identical
physical clock and strict prefix:

    2<=n<4k,  n notin {2k,2k-2}.

RH-348 must keep all remaining signed physical orders together.  It may:

- prove an alias-inclusive aggregate theorem on the punctured prefix; or
- isolate an additional physical sideband atom and its exact signed
  compensation demand.

It may not infer punctured closure from the two selected-order analyses,
split mandatory atoms from their signed complements by separate absolute
values, or substitute scalar completions for actual noisy operators.

Critical compensation, lower compensation, `E_off,(4k)`, head transport,
the direct prefix, RH-288, and Gates A--E remain open.
