# RH-395 research audit

## Research question

For centered three-window rules that may read the future value `mu(n+1)`, can
finite-state memory enlarge the universally safe terminal-log capacity, and
if it can at individual clocks, does it enlarge the supremum over all fixed
finite clocks?

## Answer

Yes locally, no at the endpoint.

- At `q=2`, an exact optimizer needs a singleton-sign self-loop state.
- At `q=6`, the centered capacity exceeds the one-site value by
  `(2K2-K1)/4>0`.
- On the cofinal square-support family, a shared-coordinate marginal charge
  forces the centered capacity back to the one-site value.
- Therefore the all-clock supremum is exactly the RH-375 endpoint
  `B_infinity`, and no finite clock attains it.

## Novel contribution

The novelty is not another computation of the RH-375 endpoint.  RH-395 first
exhibits genuine finite-clock memory gain in a larger centered relation class,
then proves a new rigidity mechanism that removes that gain on a cofinal
family.  The mechanism consists of:

1. positive projection to center-`+1` relation cells;
2. an exact eight-subset tropical trace;
3. a coordinatewise equality between the outgoing and incoming mass on the
   shared ternary letter;
4. safety-driven splitting of shared-letter mass into disjoint left/right
   charges;
5. forced modulo-4/modulo-9 zero phases that break the phase cycles into
   finite runs;
6. a runwise independent-set bound with the same density scaling as the
   one-site problem.

The theorem is search-bounded by the frozen RH program corpus and the exact
source locks.  It does not claim that no analogous result exists outside that
corpus.

## Analytic versus finite evidence

| Layer | Role |
|---|---|
| RH-394 complete three-shift table law | proves fixed-table terminal limits and exact-support phase densities on every terminal clock |
| Manuscript relation and marginal proofs | prove projection, saturation, tropical optimization, square-support charge, and endpoint rigidity |
| RH-375 finite one-site results | supply squarefree phase densities, MWIS values, square-clock endpoints, lift, and same-support finite combinatorics |
| 72-row certificate | reproduces finite relation algebra, small clocks, interval comparisons, marginal interfaces, and firewalls |
| release tests | protect exact identities, schemas, source closure, replay, and scope metadata |

The certificate is deliberately not treated as an asymptotic proof.  RH-375's
ordinary-Cesàro statement is deliberately not treated as a terminal-clock
input.

## Adversarial questions resolved

| Question | Resolution |
|---|---|
| Can projection lower the signed score? | No; deleting a positive output at center `-1` changes score from `-1` to `+1`, and center `0` contributes zero. |
| Can saturation create an unsafe pair? | No; the source/target exclusion is preserved by `A_r=(T\Y_(r-2)) x Y_r`. |
| Is the four-state optimizer valid for every clock? | No; it is proved only for `q>=3`; `q=1,2` retain self-loops. |
| Does total marginal mass suffice? | No; the proof matches mass separately for each shared ternary value. |
| Could a finite clock attain the endpoint? | No; each finite `q` lifts below a strict RH-375 endpoint `B_y<B_infinity`. |
| Is the centered rule online? | No; it explicitly reads `mu(n+1)`. |
| Does the theorem cover growing data? | No; `q` and all tables are fixed before the terminal limit. |

## Research verdict

The exact theorem is supported in the declared centered fixed-clock data type.
It creates a reusable marginal-charge rigidity principle while leaving all
causal, growing-data, higher-correlation, operator, trace, zero, RH, and Gate
questions outside scope.
