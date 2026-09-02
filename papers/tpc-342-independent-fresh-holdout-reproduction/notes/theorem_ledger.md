# TPC-342 theorem ledger

| ID | Claim | Status | Ceiling |
|---|---|---|---|
| T342-T1 | Orthogonal projection/Pythagorean identity | PROVED_EXACT_FINITE_DECLARED_MODEL | every finite Euclidean vector and declared nuisance span |
| T342-T2 | Residual fraction lies in [0,1] | PROVED_EXACT_FINITE_DECLARED_MODEL | finite nonzero target |
| T342-T3 | Three new rows are cutoff-safe and disjoint from the TPC-341 panel | NUMERICALLY_CERTIFIED_FINITE | declared source intervals |
| T342-T4 | 108 raw and 81 nonempty records replay | NUMERICALLY_CERTIFIED_FINITE | three rows, nine controls, four masks |
| T342-T5 | In-sample residual guard holds | NUMERICALLY_CERTIFIED_FINITE | three declared aggregate means |
| T342-T6 | Held-out residual guard holds in all 27 tests | NUMERICALLY_CERTIFIED_FINITE | nine controls per row |
| T342-T7 | Mean-only nuisance removal is control-stable | REFUTED_SCOPED | this finite reproduction panel |
| T342-T8 | Growing arithmetic cancellation estimate | OPEN | no asymptotic payment |

## Parent locks

~~~text
TPC341 producer (normalized LF) =
66269d586493a51adefeb8f17638df6b2eccf7e55aeab83e099b26c7768d52ac
TPC341 certificate (normalized LF) =
50f8f81f4c401924187ae90327cf787139489570cbda68707b846e3d89f36218
TPC340 producer (normalized LF) =
218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f
TPC340 certificate (normalized LF) =
0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d
~~~

ROUND2_CLUE = CROSS_PANEL_META_CERTIFICATE_OR_ALTERNATIVE_NUISANCE_BASIS.
