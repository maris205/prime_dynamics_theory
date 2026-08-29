# TPC-297 theorem ledger

| ID | statement | status | evidence / boundary |
|---|---|---|---|
| T297.1 | `min_c ||A^T U c-b||^2=b^T(I-P_V)b` | `PROVED_EXACT_FINITE` | orthogonal projection |
| T297.2 | adding source profiles cannot increase the best residual | `PROVED_EXACT_FINITE` | nested image spaces |
| T297.3 | image rank is 3 on one row and 4 on 17 rows | `NUMERICALLY_CERTIFIED_FINITE` | two modular ranks |
| T297.4 | weighted residual `>=0.6` on all 17 large-shell rows | `NUMERICAL_OBSERVATION` | 70-digit replay |
| T297.5 | all-positive residual `<=0.15` on all 18 rows | `NUMERICAL_OBSERVATION` | 70-digit replay |
| T297.6 | four profiles suffice uniformly as `N` grows | `OPEN` | no asymptotic rank theorem |
| T297.7 | literal arithmetic `L2`, fixed-power credit, full Gate B | `OPEN` | not addressed |

## Reproducibility locks

The producer locks TPC-295 code/result and the frozen TPC-268 engine.  The
independent checker uses the same frozen inputs but an independent
source-first accumulation order.
