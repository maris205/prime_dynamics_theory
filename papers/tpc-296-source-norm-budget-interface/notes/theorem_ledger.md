# TPC-296 theorem ledger

| ID | statement | status | evidence / boundary |
|---|---|---|---|
| T296.1 | `S(b)=b^T G^(-1)b` with witness `A G^(-1)b` | `PROVED_EXACT_FINITE` | orthogonal decomposition |
| T296.2 | budget `B` is feasible iff `S(b)<=B` | `PROVED_EXACT_FINITE` | Theorem 1 |
| T296.3 | `S(b)(b^T G b)>=(b^T b)^2` | `PROVED_EXACT_FINITE` | Cauchy--Schwarz |
| T296.4 | exact one-ray least-squares residual formula | `PROVED_EXACT_FINITE` | scalar quadratic minimization |
| T296.5 | 18/18 weighted targets have `S/||beta||^2<1e-3` | `NUMERICAL_OBSERVATION` | 70-digit dual-order finite replay |
| T296.6 | 18/18 weighted targets have one-ray RMS at least `0.9` | `NUMERICAL_OBSERVATION` | declared proxy `span{frozen_beta}` |
| T296.7 | the actual native source family has only one dimension | `OPEN` | not claimed; one ray is a proxy |
| T296.8 | growing least-norm/condition control | `OPEN` | 18 rows do not imply uniformity |
| T296.9 | arithmetic `L2`, fixed-power credit, full Gate B | `OPEN` | no literal source theorem |

## Reproducibility locks

The producer locks TPC-295 code/result and the frozen TPC-268 engine.  The
independent checker imports only the engine, accumulates columns source-first,
and checks every stored high-precision enclosure.
