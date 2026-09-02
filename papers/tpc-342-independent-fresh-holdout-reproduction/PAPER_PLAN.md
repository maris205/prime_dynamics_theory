# TPC-342 paper plan

## Research question

Does the TPC-341 aggregate-versus-holdout obstruction survive on a source panel
that is disjoint from every window used to form the original certificate?

## Frozen protocol

1. Lock the TPC-341 producer and certificate by normalized SHA-256.
2. Retain the TPC-340 all-plus Q=54, exponent-one, H=66 operator, source
   masks, nine coordinate bijections, SVD rank rule, and two decision guards.
3. Use only the new rows (40097,1024), (40609,1024), and (41121,1024).
4. Form the nine-control nuisance mean projection and all 27 leave-one-control-
   out projections exactly as in TPC-341.
5. Recompute the result with a reverse-shell independent engine and mutate the
   certificate's geometry, guards, rank census, and semantic firewall.

## Decision rule

The reproduction is successful if all exact finite identities, source/cutoff
checks, rank checks, and replay checks pass and the two predeclared guards hold:

~~~text
max(in-sample retention) < 0.30
min(held-out retention) > 0.40
~~~

If the guards hold, report a replicated finite obstruction.  If they fail,
report the precise scoped non-replication and do not average it away.  In both
cases, arithmetic advance, fixed-power credit, source-uniform L2, and Gate B
remain unchanged until a source-backed theorem pays them.

## Stop conditions

Do not enlarge the panel opportunistically, change controls after seeing the
readout, or treat a finite holdout as random independence.  A missing parent
hash, nonzero checker, stale certificate, or failed PDF audit invalidates the
release rather than being repaired by claim weakening.

## Deliverables

The project contains a canonical JSON certificate, producer, reverse-shell
independent checker, mutation stress, proof/derivation packages, route notes,
and a LaTeX manuscript compiled to paper/paper.pdf.
