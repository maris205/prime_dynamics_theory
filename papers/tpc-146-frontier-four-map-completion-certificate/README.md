# TPC-146: Frontier four-map completion certificate

This paper assembles the exact map-route contract for frontier
totalization.  The certificate keeps the two legitimate routes
separate:

1. a fully typed map route with a conservative occurrence lift,
   total `Q_D`, `Q_Z`, `G`, downstream `P_h0`, compatibility squares,
   physical cover, reconnection, and occurrence registry;
2. an independent theorem proving the complete original-scale
   frontier scalar is `o(X)`, together with a theorem-backed
   disposition of every `ELIGIBLE_TAIL_OPEN` path.

The map route is represented by the zero-defect vector

```text
(D_L, D_QD, D_QZ, D_G, D_P, D_DZ, D_GP, D_cover, D_rec)
```

All components need theorem-backed exact matrices before they can be
evaluated.  Unknown is not zero.  The audited domain is exactly
`ALL_NONSOFT = ELIGIBLE_TAIL_OPEN + FRONTIER_UNMAPPED`; a finite empty
eligible-tail census is not an asymptotic theorem.

The current verdict is:

```text
H1.frontier_totalization = NOT_TESTABLE
first missing = H1.frontier_occurrence_lift
```

The current-schema-only derivation is a scoped stopped route.  The
occurrence-augmented route and the scalar-plus-eligible-tail route are
not stopped.

Run:

```bash
python experiments/tpc146_frontier_completion_audit.py
python experiments/tpc146_frontier_completion_audit.py --check
```
