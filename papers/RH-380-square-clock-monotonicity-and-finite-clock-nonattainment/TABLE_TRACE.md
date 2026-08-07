# RH-380 result and table trace

All paths below are relative to this paper directory. An Euler pair
`{"inv_pi2": u, "kappa2": v}` denotes `u/pi^2+v*kappa2`.

| Manuscript object | Result-ledger path | Producer | Regression check | Theorem role |
|---|---|---|---|---|
| Per-run deletion ledger | `certificate.deletion_ledger` | `deletion_ledger()` | eight lengths at `s=25,49,121` | Finite reproduction of Lemma 2.1; manuscript proves all `s` |
| Direct run rows | `certificate.direct_run_rows` | `direct_square_run_counts()` and `square_run_counts()` | `y=1,2,3` exact equality | Cross-checks the locked RH-374 Euler-product formula |
| Run statistics | implicit in `certificate.square_transitions` | `run_statistics()` | exact `E,L,M,X` fixtures | Supplies recurrence and increment anchors |
| Even-run recurrence | `certificate.square_transitions[*].mathcal_E_*` | `square_transition()` | equality for `y=1,...,4` | Reproduces the all-order identity |
| Odd-run recurrence | `certificate.square_transitions[*].O_*` | `square_transition()` | equality for `y=1,...,4` | Locks the RH-374 predecessor input |
| Exact increment | `certificate.square_transitions[*].increment_*` | exact Euler-pair subtraction | direct/formula equality | Reproduces Theorem 3.1 |
| Strictness anchors | `.L_minus_2E`, `.R8_y`, `.quantitative_lower_inv_pi2` | exact run statistics | `X>=6`, `R8>=1` | Locks the positive first term |
| Same-support density scaling | `certificate.same_support_saturation[*].density_scaling_pass` | every-residue local-density formula | nine refinements, all fine phases | Certifies exact `1/R` scaling |
| Separator causes | `.base_separator_certificate`, `.fine_separator_certificate` | addition-by-two cycle scan | mod-4 even / mod-9 odd flags | Prevents a generic-cover interpretation |
| Run replication | `.base_run_histogram`, `.fine_run_histogram` | support-word cycle scan | fine histogram equals `R` times base | Checks path-copy structure |
| Independent max-plus value | `.direct_dp_G_Q`, `.direct_dp_pass` | generic three-state cyclic DP | nine exact refinements | Independent optimizer cross-check |
| Same-support exact values | `.G_Q`, `.G_q_y`, `.saturation_pass` | run formula and DP | `Q=72,108,144,216,288,324,1800,2700,4500` | Finite saturation fixtures |
| New-prime negative control | `predecessor_checks.negative_control` | locked RH-379 fixtures and H bound | `36`, `180`, `900` exact values | Blocks general-multiple promotion |
| Lcm exponent fixtures | `certificate.lcm_gap_rows` | `lcm_gap_row()` | seven finite clocks | Reproduces divisibility/support/gap bookkeeping |
| Fail-closed H interval | `predecessor_checks.h_interval_from_rh379` | locked RH-379 rational enclosure | strict containment in `(3.18,3.19)` | Certifies DP comparisons |
| Source files and releases | `source_locks`, `source_commits` | `experiments/build_result.py` | live SHA plus release-blob identity | Freezes 24 immutable predecessor inputs |
| Claim firewalls | `certificate.claim_boundary`, `claim_boundary`, `gates` | closed ledger | exact booleans and notes | Prevents `Delta`, cover, growing-clock, capacity, Gate, or RH promotion |

Finite rows are exact reproduction fixtures. They do not replace the
symbolic all-order proofs.
