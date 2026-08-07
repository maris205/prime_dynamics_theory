# RH-385 Table and Claim Trace

| Manuscript object | Result path | Generator or checker | Test surface |
|---|---|---|---|
| Lemma 1.2 coefficient census | `certificate.truth_tables`, `certificate.coefficient_contract` | `_table_rows()`, `coefficient_vector()` | truth enumeration, histogram, alphabets, norms, multiplicities |
| 4,608 interpolation identities | `certificate.interpolation_evaluations` | `_table_rows()` | every expected/actual row and pass bit |
| Legal `c21=-2` witness | `certificate.coefficient_contract.c21_minus_two_self_compatible_witness` | `plus_edges()`, `compatible()` | table 40, edge set, exact vector |
| Cutoff period contract | `certificate.period_contract` | `primorial_square()` and LCM fixtures | periods `4/36/900/44100`, coprime/noncoprime rows |
| Nonminimal-period firewall | `certificate.period_contract.lcm_fixtures[2]` | exact fixture | `q=5,P=3,Q=180`, relevant minimal period 36 |
| Normalized DFT bound | `certificate.dft_contract` | exact Q=4 DFT | channel norms `1/1/2`, L1=3, sup-norm factor retained |
| One-site and pair mask means | `certificate.square_means` | `_square_mean_rows()` | counts `(3,2),(24,14),(576,322),(27648,15134)` |
| Proposition 3.1 master ledger | `certificate.tail_and_padding.ledger` | `_tail_fixture()` and semantic verifier | exact `4/13/6/4`, tail split `8+5`, difference count 118 |
| Zero-padding endpoints | `certificate.tail_and_padding.padding_rows` | semantic verifier | two site-1 costs of 2; `eta(0)=0`, `eta(-1)=1` |
| Diagnostic triangular max lemma | `certificate.small_clock_triangular_dp` | `finite_clock_extrema()` | `N=96`, q=1..3 extrema and running maximum |
| Square-clock empty convention | `certificate.diagonal_sentinel` | semantic verifier | first clock 36, exact sentinel, no substitution |
| Fixed-`B` firewall | `certificate.analytic_firewall` | semantic verifier | clock string, `A>B/2`, all prohibited promotions false |
| Twenty-four certificate mutations | `mutations` | `apply_mutation()`, `verify_certificate()` | all are genuine digest changes and fail field-level semantic verification |
| Source-release lock | `source_locks` | `build_source_locks()` | 67 live/release blobs, path safety, group and aggregate digests |
| Theorem statement | `theorem_contract` | `build_result.py` | exact finite score, limit, cutoff, ledger, optimizers, diagonal |
| Route and Gates | `claim_boundary`, `forbidden_claims`, `gates` | result builder | `GO` / `STOP_SCOPED`, all promotions false |

## Certificate row counts

| Ledger | Count |
|---|---:|
| Truth tables | 512 |
| Interpolation evaluations | 4,608 |
| Phasewise `c11=0` tables | 192 |
| Distinct zero-score coefficient vectors | 24 |
| Cutoff-period rows | 4 |
| DFT channels | 3 |
| Diagnostic triangular-clock rows | 3 |
| Negative certificate mutations | 24 |

The finite rows are explicitly `reproduction_not_analytic_proof`. The
uniform limit is proved in `main.tex` from the exact ledger and RH-366
Davenport input, not inferred from enumeration or small-clock computation.

## Source groups

| Group | Files | Frozen release | Group digest |
|---|---:|---|---|
| RH-384 immutable closure | 51 | recursively released inputs | `a070fef658256fa4744d88faa7bf56f1308979e8ee20393c2fd78d84a127c970` |
| RH-384 standard eight | 8 | `386b66a55c9263353c7d407fd712be7e6279f1e6` | `82bbab8d99ae27b4629aeab53c8681c2c4e8b8bfa713b728fda3d9b320027aae` |
| RH-366 standard eight | 8 | `0396fab97bbe3348c8237f8734dec0e1893fd3bf` | `9ecb03f818a94fa9fc25fb2a21e477fc662f85ab011a0c2fb0c660d182395f5c` |

The 67 paths are unique. Mutable `AGENTS.md` and `RH_HANDOFF.md` files are
excluded from the immutable closure.
