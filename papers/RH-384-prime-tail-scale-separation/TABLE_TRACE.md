# RH-384 Table and Claim Trace

| Manuscript object | Result ledger path | Generator | Test surface |
|---|---|---|---|
| Theorem 2.2 fixed-r law | `certificate.fixed_r` | `fixed_r_rows()` | `test_fixed_r_and_partition_compilers_are_algebraic` |
| Strict endpoint/successor identity | `certificate.successors` | `successor_rows()` | `test_48_strict_successor_rows_are_exact_interface_checks` |
| Corollary 3.1 partition compiler | `certificate.partitions` | `partition_rows()` | algebraic reconstruction in `test_core.py` |
| Proposition 3.2 scale dictionary | `certificate.scale_separation` | `scale_separation_ledger()` | constants and quotient identities reconstructed |
| Theorem 4.1 five gap limits | `certificate.gap_limits` | `gap_limit_rows()` | exact-subtraction membership checks |
| First-order PNT surrogate firewall | gap L2 and mutation `PNT-surrogate-second-subtraction` | `gap_subtraction_contract()` | genuine mutated term rejected |
| Quadratic PNT surrogate firewall | gap L3 and mutation `PNT-surrogate-quadratic-subtraction` | `gap_subtraction_contract()` | genuine mutated term rejected |
| Proposition 5.1 positive contrast | `certificate.numeric_interval` | `numeric_interval_certificate()` | precision, counts, endpoints, upper tail-loss inequalities |
| Published 19-place interval | `certificate.numeric_interval.published_lower/upper` | outward quantization | exact string fixtures |
| Twenty adversarial mutations | `certificate.negative_mutations.rows` | `negative_mutation_rows()` | all rejected; fixed count 20 |
| Decimal context independence | whole certificate | fresh directed contexts | three hostile ambient contexts, altered `Emin/Emax` and traps |
| PNT provenance | source entries for RH-2 and predecessor checks | `validate_pnt_provenance()`, `build_source_locks()` | release/main/ref/DOI flips |
| 51-file immutable closure | `source_locks` | `build_source_locks()` | membership, release blob, declared SHA, group/all digests |
| Gates A–E false | `gates` | `build_result.py` | recursive schema mutation and boundary tests |
| Route A/Route B boundary | `claim_boundary` | certificate | exact `GO` / `STOP_SCOPED` assertions |

## Certificate row counts

| Ledger | Count |
|---|---:|
| Fixed-r | 8 |
| Partitions, degrees 1–8 | 66 |
| Exact successor witnesses | 48 |
| Scale relations | 5 |
| Gap limits | 5 |
| Numeric intervals (`u_2`–`u_8`, `Y`, `m`, `Y-2m`) | 10 |
| Negative mutations | 20 |

The finite fixed-r and partition rows freeze compiler outputs only. The all-`y` asymptotic theorem is proved in `main.tex` from PNT and Abel summation.

## Source groups

| Group | Files | Release |
|---|---:|---|
| RH-374 | 7 | `2bb3baa6...` |
| RH-379 | 8 | `9ae9802e...` |
| RH-380 | 8 | `dd94b9cf...` |
| RH-381 | 8 | `b6a6355b...` |
| RH-382 | 8 | `32afe961...` |
| RH-383 | 8 | `bea5c88c...` |
| RH-MVP2 | 2 | `c0aed13a...` |
| RH-2 PNT | 2 | `83642654...` |

All paths, commits, live hashes, release-blob hashes, group digests, and the aggregate digest are stored in `results/result.json` and recursively frozen by `results/result.schema.json`.
