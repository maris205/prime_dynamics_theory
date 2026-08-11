# RH-396 research audit

## Research question

For a centered Möbius rule with arbitrary fixed lag `h`, what is the exact
universally safe terminal-log capacity at a fixed finite clock, what endpoint
is approached over all finite clocks, and how do those endpoints sit across
fixed lags?

## Answer

- Every fixed clock has an exact full eight-state tropical formula.
- Four-state compression holds when `q` does not divide `2h`, but is false in
  general on self-loop clocks.
- On square supports containing `p0(h)`, centered capacity equals the
  normalized one-site MWIS value.
- Exact bracketed squarefree-run densities give a finite Euler-run formula
  for the cofinal square-clock endpoints.
- Fresh-prime steps are strict exactly when an even run is present; plateaus
  can occur, but CRT forces a later strict step.
- Therefore `sup_q C_h(q)=B_infinity(h)` and no finite `q` attains it.
- Every fixed-lag endpoint is strictly above `3/pi^2`, while their infimum is
  `3/pi^2` and is not attained.

## Novel contribution

The novelty is the fixed-lag Euler-run spectrum and its strictness mechanism,
not a numerical extrapolation.  The proof combines:

1. a collision-aware instantiation of the RH-394 three-shift density law;
2. an exact full-eight relation optimizer with a sharply delimited four-state
   compression theorem;
3. a per-shared-state marginal identity valid even when shifts collide
   modulo prime squares;
4. qualified square-support equality between centered capacity and weighted
   one-site MWIS;
5. exact finite and infinite bracketed-run densities;
6. a fresh-prime recurrence whose even-run excess is precisely the strict
   normalized gain;
7. CRT creation of an exact length-two run;
8. a boundary-prime tail argument for the lag infimum.

The theorem is search-bounded by the frozen RH program corpus and exact
source locks.  It does not claim absence of analogous work outside that
corpus.

## Analytic versus finite evidence

| Layer | Role |
|---|---|
| RH-394 complete three-shift table law | proves fixed-table terminal limits and exact-support phase densities on every terminal clock |
| Manuscript proofs | prove relation optimization, marginal charge, Euler-run formula, strictness, and lag landscape |
| RH-395 and RH-375 | finite combinatorial precedent only |
| 96-row certificate | reproduces finite identities, counterexamples, recurrences, intervals, and firewalls |
| release tests | protect exact identities, source closure, schema, replay, and scope |

The certificate is not asymptotic evidence.  Ordinary-Cesaro statements in a
predecessor are not substituted for the terminal-log theorem.

## Adversarial questions resolved

| Question | Resolution |
|---|---|
| Do local residue collisions permit replacing `kappa_h(S)` by `K_|S|`? | No; the theorem and artifact deduplicate shift residues prime by prime. |
| Is four-state compression valid on every clock? | No; it is proved only for `q` not dividing `2h`, and `h=2,q=4` is a strict obstruction. |
| Is `alpha` already a weighted capacity? | No; `alpha` is raw and `M=K1 alpha/N` is weighted. |
| Does total marginal mass suffice? | No; equality is proved separately for `t=0,+1,-1`. |
| Does same-support scaling require a coprime cover degree? | No; path-cover lifting proves it without that condition after the `p0` base gate. |
| Is every fresh-prime step strict? | No; the `h=9` plateau is exact.  Even-run excess is the iff criterion. |
| Can a finite clock attain the endpoint? | No; eventual strictness and the arbitrary-clock bridge give a strict bound. |
| Are endpoints monotone in the lag? | No such claim is made. |

## Research verdict

The exact theorem is supported in the declared fixed-lag, fixed-clock,
centered data type.  All growing-parameter, causal, larger-window, generic
graph, analytic trace/operator, zero, RH, and Gate questions remain outside
scope.
