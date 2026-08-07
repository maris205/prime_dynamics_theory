# RH-379 result and table trace

All paths below are relative to this paper directory.  Exact values are
stored as pairs `{"inv_pi2": u, "kappa2": v}`, meaning
`u/pi^2 + v*kappa2`.  Decimal intervals are diagnostic only.

| Manuscript object | Result-ledger path | Producer | Regression check | Theorem role |
|---|---|---|---|---|
| Five-cell `c11` histogram | `certificate.census.c11_histogram` | `canonical_census()` | `test_512_and_192_census` | Exhausts all 512 local tables and isolates 192 admissible rows |
| Nine `(c02,c22)` rows | `certificate.census.main_pair_histogram` | `canonical_census()` | exact expected histogram inside core; payload regeneration | Supplies every canonical dominance case; counts total 192 |
| Canonical counts `120/40/24/8` | `certificate.census.canonical_target_counts` | `canonical_census()` | `test_512_and_192_census` | Records targets `0/J/K/I` before `K -> I` |
| Canonical edge sets and coefficients | `certificate.census.canonical_edges`, `.canonical_coefficients` | `canonical_census()` | subset/dominance flags for all 192 rows | Connects truth tables to exact `J,K,I` weights |
| Four-state compatibility matrix | `certificate.census.compatibility_matrix` | exact edge composability | exact matrix fixture | Certifies full incoming/outgoing `K/I` equivalence after canonicalization |
| Reflection certificate | `certificate.census.input_reflection_pass`, `.reflection_neighbor_pair_checks`, `.reflection_neighbor_pair_failures` | all 512 coefficient checks and all `512^2` ordered neighbor checks | census test fixes `262144/0` | Converts positive optimum to maximum absolute score |
| Density normalizations | `certificate.density_normalization` | `density_vectors(q)` for `q=1,...,12` | core normalization test | Checks `sum delta=6/pi^2`, `sum theta=kappa2` |
| `q | Q` aggregation | `certificate.density_aggregation` | `density_aggregation_certificate()` | ten `Q=720` fiber fixtures | Certifies exact lift aggregation for odd and prime-power clocks |
| Small clocks `q=1,...,6` | `certificate.small_clocks` | `fixed_clock_certificate()` | DP/MWIS equality and exact fixtures | Covers self-loops and small cyclic cases |
| Exact manuscript clock table | `certificate.fixture_clocks` | `fixed_clock_certificate()` | frozen rows in `test_results.py` | Stores `q=36,180,900,44100` formulas and witness hashes |
| Square-clock rows | `certificate.square_clocks` | `square_clock_certificate()` | recurrence, strictness, even-run bound, formula fixtures | Certifies `G(q_y)=B_y+Delta_y` for `y=1,2,3` fixtures |
| `q=36` strict chain | `certificate.q36_strict_gain` | `q36_strict_gain_certificate()` | exact formula string and certified sign | Proves the exact square-clock strict gain |
| `q=1` orientation row | `certificate.q1_memory_gain_over_F1_zero` | fixed exact value | positive certified sign | Prevents calling `q=36` the first same-clock gain |
| Cofinal lift fixtures | `certificate.cofinal_protocol_rows` | `cofinal_lift_protocol()` | every row included in global `all_pass` | Checks finite retained/deleted mechanics without claiming same-support memory saturation |
| Certified constants | `certificate.certified_constants` | Machin interval and directed Euler product | exact small-product containment and ambiguous fail-closed comparison | Resolves exact Euler-symbol orderings; not asymptotic evidence |
| Source files and releases | `source_locks`, `source_commits` | `experiments/build_result.py` | full regenerated payload and digest loop | Freezes the complete repository evidence surface |

The 512-row census serialization has SHA-256
`aaae39b0af85b13e7cc75baa7170a29f1ac60355443d7b80f3fee06d4af56121`.
The four larger-clock action words also have individual SHA-256 values in
`certificate.source_hashes.fixture_action_sha256`.
