# RH-395 updated roadmap

## Closed route

RH-395 closes the centered three-window capacity route for every fixed finite
clock:

1. RH-394 supplies the complete fixed three-shift terminal-log table law on
   every admissible terminal clock.
2. Positive projection turns the 27-cell sign table into a 9-cell relation
   without decreasing the score.
3. Safety and nonnegative saturation reduce the relation family to eight
   subset states.
4. The full eight-state tropical trace is exact for every finite clock.
5. Multi-affinity compresses an optimizer to four states only for `q>=3`;
   the `q=1,2` self-loops are separately solved.
6. The square-support marginal charge forces equality with the RH-375
   one-site value on a cofinal family.
7. Divisibility lift and embedded one-site witnesses prove
   `sup_q C(q)=B_infinity`, with strict nonattainment at finite `q`.

This route is complete.  Fixed-clock memory gain does not create a larger
all-clock endpoint.

## New theorem edge

The reusable edge created here is the distinction between local finite-clock
gain and cofinal endpoint rigidity:

```text
centered memory gain at q=2 and q=6
                |
                v
same-support marginal-charge saturation on square clocks
                |
                v
all-clock one-site endpoint, strict finite nonattainment.
```

The marginal identity is coordinatewise: it matches the outgoing and
incoming mass for each shared ternary value.  Any future memory model that
admits a comparable coordinatewise charge and sufficiently frequent forced
zero phases may be tested for the same rigidity mechanism.

## Admissible next work

The following are legitimate research questions, not claims of RH-395:

- characterize other fixed, noncausal local relation types for which a
  coordinatewise marginal charge yields endpoint rigidity;
- determine which larger finite windows possess an analytic table law strong
  enough to make their fixed-table terminal limits unconditional;
- isolate exact hypotheses under which a finite-state optimizer admits a
  cofinal square-support saturation theorem;
- study causal models only under their own online information constraint,
  without importing centered access to `mu(n+1)`;
- investigate higher odd-support channels only after a source theorem covers
  the exact parity/order required.

No next paper number follows merely from this list.  A new route requires a
repository-backed theorem edge and fresh source/proof locks.

## Permanent stops

Do not infer any of the following from RH-395:

- a result for `q=q(X)` or an `X`-dependent table family;
- an effective or uniform convergence rate;
- an ordinary Cesàro statement;
- equality after taking a finite-prefix maximum before the limit;
- a causal/online implementation of the centered rule;
- the RH-378 window-end capacity theorem as a centered theorem, or vice versa;
- a generic graph-capacity theorem;
- a result for even odd-support size at least four;
- a Hilbert--Pólya operator, von Mangoldt trace, zeta-zero identification,
  completed-zeta divisor equality, or the Riemann hypothesis.

Gates A--E remain false and are not activated by this finite-state endpoint.
