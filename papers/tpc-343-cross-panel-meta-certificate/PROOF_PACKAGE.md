# TPC-343 proof and scope package

## Proposition 1 — stacked projection identity

For any finite real matrix `N` and finite vector `Y`, let `P_N` be the
orthogonal projector onto `col(N)`.  Then

```text
||Y||_2^2 = ||P_N Y||_2^2 + ||(I-P_N)Y||_2^2.
```

**Proof.** `P_NY` belongs to `col(N)` and `(I-P_N)Y` belongs to its orthogonal
complement.  Their sum is `Y`; Pythagoras gives the identity.  `QED`.

## Proposition 2 — row-block additivity

If `N_block` is block diagonal and `Y` is the concatenation of `y_r`, then the
projection and residual energies are the sums of the corresponding row
energies.

**Proof.** The block columns have disjoint supports, so the column space is the
orthogonal direct sum of the row column spaces.  The orthogonal projector is
the direct sum of the row projectors.  Summing the six Pythagorean identities
proves the claim.  `QED`.

## Proposition 3 — finite decision

In the declared six-row panel, the row-block raw-energy residual retention is
`0.2325429101`, whereas the shared-coefficient raw and equal-row retentions are
`0.3198013104` and `0.3549335801`.  Thus the row-block guard `<0.30` passes and
both shared variants fail it.  The nine shared cross-panel holdout tests have
retention `0.6408306196--0.9090948298`.

**Evidence.** The producer and reverse-shell checker independently recompute
the source arrays, operator responses, projections, ranks, raw records, and
meta energies under hash-locked TPC-340/341/342 parents.  The mutation suite
rejects seven resealed semantic mutations.

## Scope boundary

This is a finite model-comparison certificate.  `REFUTED_SCOPED` applies only to
the tested single shared nuisance coefficient model and its two declared
weightings.  It does not refute every possible nuisance basis, prove a source-
uniform `L2` estimate, close Route A or Route B, or imply the twin-prime
conjecture.  The official Session evaluator files are absent; local Bridge-B is
fail-closed only.
