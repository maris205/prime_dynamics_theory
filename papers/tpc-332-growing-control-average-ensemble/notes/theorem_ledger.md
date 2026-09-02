# TPC-332 theorem ledger

| ID | Claim | Status | Evidence / ceiling |
|---|---|---|---|
| T332-T1 | Five declared controls are bijections and preserve the source multiset and norm | `PROVED_EXACT_FINITE` | odd units modulo powers-of-two source counts |
| T332-T2 | Mean--centered identity for every finite quadratic form | `PROVED_EXACT_FINITE` | finite bilinear expansion |
| T332-T3 | Simultaneous identities for energy, coordinate diagonal, and off-diagonal response | `PROVED_EXACT_FINITE` | apply T332-T2 and subtract |
| T332-T4 | Source polarization `||Lambda-b||^2=||Lambda||^2+||b||^2-2<Lambda,b>` | `PROVED_EXACT_FINITE_DECLARED_MODEL` | exact algebra; replay error recorded |
| T332-T5 | 48 rows and 192 law-level decompositions have no unresolved classifications | `NUMERICALLY_CERTIFIED_FINITE` | producer, reverse replay, stress, local bridge |
| T332-T6 | All-plus control-average off-diagonal is positive in 48/48 rows | `NUMERICALLY_CERTIFIED_FINITE` | guarded census |
| T332-T7 | All-plus centered off-diagonal is positive in 48/48 rows | `NUMERICALLY_CERTIFIED_FINITE` | guarded census |
| T332-T8 | All-plus coherent mean is positive in 47/48 rows | `NUMERICALLY_CERTIFIED_FINITE` | one scoped negative row |
| T332-T9 | Unpermuted all-plus residual is 27 negative / 21 positive | `NUMERICALLY_CERTIFIED_FINITE` | source-native census; no sign theorem |
| T332-T10 | Source-uniform growing arithmetic `L2` or twin-prime conclusion | `OPEN` | finite panel cannot pay this gate |

## Locked parent

TPC-331 producer SHA-256 (normalized LF):
`c96095bd951d80e9147eeba99241761ba31a78b04a6b01bfcd120397f7e0eebc`.

TPC-331 certificate SHA-256 (normalized LF):
`eacd8b5e508956b362cbc0bb3c8da2b245a2155f91d8f48e794121f3e7a4997c`.

## Decision record

The mixed unpermuted sign and large centered energy share force the next
project to inspect the source cross term before another response bound.
`ROUND2_CLUE = SEPARATE_SOURCE_L2_CROSS_TERM_AND_TEST_CONTROL_COVARIANCE_SPECTRUM`.
