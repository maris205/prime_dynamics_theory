# TPC-208 paper plan

## One-sentence contribution

For the standard-zero-hole reduced-residue BDH remainder, the nonzero
additive frequencies form a complete-graph tight frame whose edge cells
delete the mandatory coefficient diagonal exactly; this representation is
unique among scalar-weighted literal two-frequency differences and therefore
cannot be sparsified edge by edge.

## Claim--evidence matrix

| Claim | Status | Evidence |
|---|---|---|
| `V_0=q^{-1} y^*P_{q-1}y` and `rank(P)=q-2` | `PROVED` | Fourier inversion, Parseval, and the V60 leave-one-out identity |
| Complete-graph edge-frame formula for `V_0` | `PROVED` | `L(K_{q-1})=(q-1)P_{q-1}` |
| Exact edgewise distribution of the `(q-2)/(q-1)` diagonal | `PROVED` | edge-mass identity `sum_e |Delta_e(n)|^2=q(q-2)1_{q\nmid n}` |
| Polarized V59 scalar equals one signed average of edge cells | `PROVED` | edgewise complex polarization and physical-kernel crosswalk |
| Literal two-frequency edge representation cannot use a strict subset | `PROVED`, scoped | every off-diagonal projection entry forces its unique edge weight |
| Equal/off-equal frequencies may be estimated separately | `REFUTED` | a residue-zero spike has two nonzero opposite pieces and exact total zero |
| Edge pre-emitters satisfy a fixed-power prime-shell estimate | `OPEN` | no source-valid collective Poisson/Kloosterman compiler has been proved |

## Section plan

1. Introduction and claim firewall.
2. Frozen zero-hole row and additive Fourier convention.
3. Zero-hole frequency projection.
4. Complete-graph tight frame.
5. Edgewise diagonal deletion.
6. Polarized physical scalar and kernel crosswalk.
7. Oriented difference fibers and no-sparsification.
8. Sharp falsifiers and mutation boundaries.
9. Source boundary and bounded novelty statement.
10. Exact computational certificate.
11. Route consequence and open theorem.

No decorative figure is needed.  One status table will distinguish proved
structure from open arithmetic estimates.  All general proofs appear in the
main text; finite exact computations are explicitly described as QA only.
