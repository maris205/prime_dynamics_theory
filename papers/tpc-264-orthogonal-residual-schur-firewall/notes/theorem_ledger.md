# TPC-264 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T264.1 | orthogonal projection gives `<w,g>=<Pw,Pg>+<Pperp w,Pperp g>` | `PROVED_EXACT` | any complex Hilbert space |
| T264.2 | residual Gram matrix is PSD and `|z|<=ab` | `PROVED_EXACT` | fixed residual norms |
| T264.3 | disk/circle/singleton classification by complement dimension | `PROVED_EXACT` | finite or infinite dimension |
| T264.4 | full scalar is the translated feasible set | `PROVED_EXACT` | fixed projected data |
| T264.5 | endpoint-scale norm-only data permit full `x^(5/3)` residual | `NUMERICALLY_CERTIFIED_STRUCTURAL` | synthetic family only |
| T264.6 | actual V59 residual radius/phase estimate | `OPEN` | not supplied |
| T264.7 | strict `1/400` payment, arithmetic `L2`, full Gate B | `UNPAID_GLOBAL / NONE / OPEN` | no claim |

```text
STRONGEST_POSITIVE_RESULT = EXACT_SCHUR_DISK_CIRCLE_SINGLETON_FIREWALL
STRONGEST_OBSTRUCTION = NORM_ONLY_RESIDUAL_DATA_LEAVE_FULL_RADIUS_IN_DIMENSION_TWO
OPEN_THEOREM = LITERAL_V59_RESIDUAL_RADIUS_OR_SIGNED_PHASE_ESTIMATE
REUSABLE_STRUCTURE = P3_CENTER -> RESIDUAL_GRAM -> SCHUR_FEASIBLE_SET -> ENDPOINT_RADIUS TEST
ROUND2_CLUE = TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE_INTO_A_LITERAL_V59_ESTIMATE
```
