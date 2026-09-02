# TPC-341 theorem ledger

| ID | Claim | Status | Ceiling |
|---|---|---|---|
| T341-T1 | Orthogonal projection/Pythagorean decomposition | `PROVED_EXACT_FINITE_DECLARED_MODEL` | every finite Euclidean vector and nuisance span |
| T341-T2 | Residual fraction lies in `[0,1]` | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite nonzero target |
| T341-T3 | Fresh replay: 108 raw records, 90 nonempty | `NUMERICALLY_CERTIFIED_FINITE` | three declared windows |
| T341-T4 | In-sample nuisance removal on three rows | `NUMERICALLY_CERTIFIED_FINITE` | nine-control mean panel |
| T341-T5 | Leave-one-control-out retention exceeds `0.40` in all 27 tests | `NUMERICALLY_CERTIFIED_FINITE` | declared controls and windows |
| T341-T6 | Mean-only removal is control-stable | `REFUTED_SCOPED` | finite fresh holdout |
| T341-T7 | Growing arithmetic cancellation estimate | `OPEN` | no asymptotic payment |

## Parent lock

TPC-340 producer SHA-256 (normalized LF):
`218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f`.

TPC-340 certificate SHA-256 (normalized LF):
`0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d`.

`ROUND2_CLUE = INDEPENDENT_REPRODUCTION_OR_FREEZE_NUISANCE_PROJECTION`.
