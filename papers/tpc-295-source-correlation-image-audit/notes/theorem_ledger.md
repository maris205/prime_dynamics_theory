# TPC-295 theorem ledger

| ID | statement | status | evidence / boundary |
|---|---|---|---|
| T295.1 | $G=A^{\mathsf T}A$ and $A^{\mathsf T}$ is the source-correlation map | `PROVED_EXACT_FINITE` | definitions |
| T295.2 | nonsingular $G$ implies surjectivity with witness $AG^{-1}b$ | `PROVED_EXACT_FINITE` | linear algebra proof |
| T295.3 | nonzero modular determinant implies rational full rank | `PROVED_EXACT_FINITE` | denominator-clearing lemma |
| T295.4 | all 18 rows have full rank at both declared moduli | `NUMERICALLY_CERTIFIED_FINITE` | exact rational construction + modular certificates |
| T295.5 | all TPC-294 weighted minimizer signs are unrestricted-source attainable | `NUMERICALLY_CERTIFIED_FINITE` | 18/18 target residual checks |
| T295.6 | the witnesses satisfy the native Mobius/comparison profile constraints | `OPEN` | not encoded |
| T295.7 | source witness norms are uniformly affordable | `OPEN` | next audit |
| T295.8 | growing weighted source-image theorem, arithmetic $L^2$, Gate B | `OPEN` | no credit paid |

## Reproducibility locks

The producer locks TPC-294 code/result and the frozen TPC-268 engine.  The
independent checker does not import the TPC-295 producer and repeats the
physical accumulation and modular rank calculation in source-first order.
