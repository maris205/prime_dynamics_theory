# Roadmap after RH-325

RH-325 proves that moving order alone is not the obstruction for unweighted
Markov path laws.  With retained coordinates and errors evaluated against the
correct transported incoming laws, `O(k)` phase-matched `O(sigma)` rows sum to
`O(k*sigma)`, which is negligible at the first-alias target.

This criterion does not yet apply to the physical cycle:

1. RH-324 supplies the required remainder for only the first physical leg.
2. The second critical physical leg is still unresolved.
3. Phase transport must control every incoming profile, not just one fixed
   entrance seed.
4. A trace requires a separately bounded observation functional and
   intermediate operator products; Markov contraction does not provide them.
5. Parity and neighboring-shell terms cannot be replaced by separate absolute
   majorants.

RH-326 should derive the parity-renormalized first-alias packet identity while
retaining the combined sign and phase information needed later.  RH-327 then
adds the neighboring shell, and RH-328 formulates their joint matching
equation.  The present Duhamel criterion becomes an actual bridge only after
those local identities and the missing trace-observation bounds are supplied.

Gates A--E remain false/open.
