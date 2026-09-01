# TPC-331 theorem ledger

| ID | Claim | Status | Evidence / ceiling |
|---|---|---|---|
| T331-T1 | `mean E(P_jv)=E(v_bar)+mean E(z_j)` | `PROVED_EXACT_FINITE` | finite quadratic-form expansion |
| T331-T2 | corresponding identities for `D` and `O=E-D` | `PROVED_EXACT_FINITE` | subtraction of T331-T1 instances |
| T331-T3 | five controls are bijective and preserve multiset/L2 | `PROVED_EXACT_FINITE` | odd units modulo `2^k` |
| T331-T4 | all-plus average off-diagonal positive in `32/32` rows | `NUMERICALLY_CERTIFIED_FINITE` | producer + independent replay + stress |
| T331-T5 | all-plus centered off-diagonal positive in `32/32` rows | `NUMERICALLY_CERTIFIED_FINITE` | same certificate |
| T331-T6 | all-plus coherent mean positive in `31/32` rows | `NUMERICALLY_CERTIFIED_FINITE` | one scoped negative row |
| T331-T7 | exact 16-point rational anchor | `PROVED_EXACT_FINITE` | four reduced-fraction digest triples |
| T331-T8 | source-uniform growing arithmetic `L2` bound | `OPEN` | not supplied by finite panel |
| T331-T9 | twin-prime conclusion | `NONE` | no endpoint theorem |

## Locked parent

TPC-330 producer SHA-256 (normalized LF):
`d9bd669bfde610a8caeaa5253c71486323b6c84ad2c783d424fc65a3a56915b5`.

TPC-330 certificate SHA-256 (normalized LF):
`5ade3c1429589fbf84660414f459e99c5de8694229e2f3a49de9540a04573097`.
