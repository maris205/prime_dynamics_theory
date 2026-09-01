# TPC-325 computational protocol

1. Freeze the origin, four endpoints, shell anchors, exponents, and sign laws
   before recomputation.
2. Build literal blocks in increasing prime order, with deleted diagonal and
   centered residue mask exactly as in the locked parent engine.
3. Accumulate direct and coherent Grams with forward, reverse, and einsum
   paths; require finite traces and path agreement.
4. Sort eigenvalues, normalize by each Gram trace, and classify every interior
   cumulative difference with tolerance `1e-10`.
5. Enclose path metrics outward by `1e-12`; require strict positive all-plus
   prefix lower endpoints.
6. Recompute the complete 32-row panel in the independent checker using a
   separate reverse/einsum implementation.
7. Run nesting, freshness, residue-perturbation, trend, and firewall stress
   checks under normal and optimized Python.
8. Compare normal/optimized stdout byte-for-byte in the Bridge-B checker.

The certificate is canonical JSON and contains the full row records, not only
aggregate counts.
