# TPC-337 theorem ledger

| ID | Claim | Status | Ceiling |
|---|---|---|---|
| T337-T1 | Mean/centered class-output identity | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite bilinearity |
| T337-T2 | Four-class covariance matrix is PSD | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite Gram algebra |
| T337-T3 | Six-row five-control replay | `NUMERICALLY_CERTIFIED_FINITE` | fixed panel and operator |
| T337-T4 | Full centered fraction exceeds `0.75` in 6/6 | `NUMERICALLY_CERTIFIED_FINITE` | fixed panel |
| T337-T5 | twin/background covariance positive in 6/6 | `NUMERICALLY_CERTIFIED_FINITE` | fixed panel |
| T337-T6 | twin/zero and background/zero covariance negative in 6/6 | `NUMERICALLY_CERTIFIED_FINITE` | fixed panel |
| T337-T7 | Control averaging uniformly removes output interference | `REFUTED_SCOPED` | finite six-row test |
| T337-T8 | Growing covariance stability | `OPEN` | next project |

## Parent lock

TPC-336 producer SHA-256 (normalized LF):
`0c2febd76d6bfdc5af4b58145739bcc04b435303f15c66b31e2d0b2e63497442`.

TPC-336 certificate SHA-256 (normalized LF):
`926859be38cc601ef728363328899d4e9ab2001f77e7e1106ab028d64cf2814a`.

`ROUND2_CLUE = GROW_THE_CONTROL_ORBIT_AND_TEST_COVARIANCE_SPECTRUM_STABILITY`.
