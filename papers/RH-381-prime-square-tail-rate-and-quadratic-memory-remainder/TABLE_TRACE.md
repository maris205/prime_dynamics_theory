# RH-381 claim-to-evidence trace

| Manuscript claim | Symbolic evidence | Executable evidence | Frozen source |
|---|---|---|---|
| Run formula and `A_y=P_yE_1^(y)` | Stable labels `eq:finite-euler` and `eq:run-formula` | `square_run_counts`, canonical rows 1--6 | RH-374 release |
| `X_j` Euler form | Lemma “Exact finite Euler form”, label `lem:X-euler` | `normalized_x`; run/Euler equality raises on drift | RH-374 + RH-380 releases |
| `X_infinity>=6e8/e1>0` | Run second-difference decomposition, label `eq:X-positive` | Positive outward `X_infinity` diagnostic, not used as proof | RH-374 release |
| `abs(X_j-Xinf)<=170T_j` | Lemma “Factorwise tail bound”, label `lem:X-bound` | Six outward rows; exact ledger `6+16+30+48+70` | RH-374/RH-380 releases |
| Exact `H` tail product | Lemma “Exact H product and its tail loss”, label `lem:H-tail` | Directed product enclosure | RH-379 release |
| `0<=M_j/A_j<=1` | Lemma “Quadratic-memory normalization”, label `lem:M-bound` | Exact `M/A` rows 1--6 | RH-374/RH-380 releases |
| Two tail identities | Lemma “Tail algebra”, label `lem:tail-algebra` | Four exact finite `Fraction` identity rows | Internal exact artifact |
| Infinite telescope | Proposition “Exact infinite increment sum”, label `prop:infinite-sum` | Exact increment telescoping fixtures | RH-379 limit + RH-380 increment |
| 342 remainder | Theorem “Prime-square tail rate”, label `thm:rate`; ledger `340+2` | Six fail-closed outward rows | All three predecessor releases |
| Ratio limit | Divide only after `T_y>0`; integer tail gives `T_y->0` | Boundary assertions in result ledger | Symbolic proof |
| Gates A--E false | Scope section | Closed result booleans | RH-MVP2 archive |

The artifact is a reproduction and mutation layer. All-order statements are
proved in the manuscript, not inferred from these finite rows.
