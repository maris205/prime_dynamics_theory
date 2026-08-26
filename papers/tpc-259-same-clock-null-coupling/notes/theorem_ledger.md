# TPC-259 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T259.1 | four source blocks are consecutive and cover `I_x` | `PROVED_EXACT` | every sufficiently large real clock |
| T259.2 | `z_null` is source-only, unit, and orthogonal to `z0` | `PROVED_EXACT` | inherited TPC-258 frame |
| T259.3 | `|<z_null,w>| << sqrt(x)/log^M x` | `PROVED_SOURCE_BACKED` | fixed `M,K` |
| T259.4 | exact rank-one/residual identity | `PROVED_EXACT` | every finite linear operator |
| T259.5 | null-channel is `o(x^(5/3)/log^(M+3) x)` | `PROVED_SOURCE_BACKED` | literal V59, fixed `M,K` |
| T259.6 | conditional `79/48` boundary refinement | `CONDITIONAL_THEOREM` | inherited explicit scalar rate |
| T259.7 | null-channel suppression implies full scalar suppression | `REFUTED_SYNTHETIC` | zero-diagonal finite witness |
| T259.8 | residual full scalar estimate | `OPEN` | no locked source theorem |
| T259.9 | arithmetic `L2` / full Gate B | `NONE / OPEN` | not supplied |
