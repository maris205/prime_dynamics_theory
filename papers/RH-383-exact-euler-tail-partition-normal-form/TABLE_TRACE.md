# RH-383 table and formula trace

This file maps every displayed theorem component and every protocol count to
its exact implementation. The manuscript proof is primary; executable rows
are reproduction and adversarial checks.

| Manuscript object | Exact implementation | Result location |
|---|---|---|
| finite `E_m,U_m,u_m` ratios | `finite_euler_values`, `normalized_euler_ratios` | `certificate.sections.endpoint_normal_form` |
| `C(V),W(V)` | `c_polynomial`, `w_polynomial` | endpoint normal-form rows |
| `U_m=u_m exp(Phi_c)`, `H=(4/pi^2)exp(-Phi_1)` | finite product ratios and `direct_a_coefficients` / elementary product | endpoint and `A/F` sections |
| exact endpoint gap | `endpoint_normal_form_pi2` vs `finite_gap_pi2` | 67/67 endpoint rows |
| partitions and `z_lambda` | `partitions_of`, `partition_z`, `power_monomial` | 271 partitions through degree 12 |
| canonical `gamma_lambda` | `cw_gamma_vector` | 1084 endpoint-labeled rows |
| direct `A/F` gamma | `af_gamma_vector` | `gamma_equivalence` |
| `A_c` coefficients | `direct_a_coefficients`, `h_a_coefficient`, `phi_a_coefficient` | 432 of the 864 A/F rows |
| `F_c` coefficients | `direct_f_coefficients`, `he_f_coefficient`, `phi_f_coefficient` | 432 of the 864 A/F rows |
| partition-length `Q` sign | partition sum vs `(-1)^n e_n` | 432 labeled rows = 72 unique identities x 6 inert labels |
| increment `Gamma/h/e/Phi` | `ordered_increment_channel_vectors` | 144 channel rows |
| direct channel telescope | `endpoint_increment_channel_vectors` | same 144 rows |
| all-order `m=2` cancellation | `cw_gamma_vector[2]`, `af_gamma_vector[2]`, direct functional cancellation | 1084 labeled symbolic + 67 finite rows |
| RH-381/RH-382 coefficient layers | `low_order_expected_vectors` | 33 endpoint-labeled bundles of the same three symbolic identities |
| cubic formulas | `CUBIC_VECTORS`, `cubic_certificate` | 12 labeled symbolic + 67 direct rows |
| `35/4`, `14`, `5/2`, `4/3`, `92/3` | `remainder_ledger` using only `XI/ETA` | `certificate.sections.remainder_ledger` |
| arbitrary-order remainder | `remainder_certificate` | 804 rows = 67 tails x 12 degrees |
| strict successor `j+1` | `finite_increment_pi2`, ordered memory channel | 7 telescopes plus current-tail mutation |
| terminal `R8/E9/no-E10` | `square_run_counts`, `terminal_certificate` | four terminal rows |
| exact `D>=1` and `rho` domain | `require_truncation_degree`, `remainder_bound_pi2_from_rho` | tests and negative rows |
| real wrong compilers/formulas | `negative_mutation_certificate` | 20/20 rejected with digests or exceptions |
| source locks | `experiments/build_result.py` | 41 entries, `7/8/8/8/8/2` groups |
| Gates and forbidden claims | closed `result.json` fields | every Gate and forbidden-claim Boolean is false |

The canonical certificate is 12245 bytes with SHA-256
`9e2742fcdb2f626909eeb528c5081c9ace5414a1e6466c15b8b6800f427b6f16`.
