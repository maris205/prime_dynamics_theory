# TPC-338 theorem ledger

| ID | Claim | Status | Ceiling |
|---|---|---|---|
| T338-T1 | Mean/centered identity for each nested ensemble | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite bilinearity |
| T338-T2 | Five- and nine-control covariance matrices are PSD | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite Gram algebra |
| T338-T3 | Nested replay on six windows | `NUMERICALLY_CERTIFIED_FINITE` | fixed source/operator |
| T338-T4 | Centered energy dominance in both ensembles | `NUMERICALLY_CERTIFIED_FINITE_6_OF_6` | finite panel |
| T338-T5 | Normalized covariance spectra are close in the scoped comparison | `NUMERICALLY_CERTIFIED_FINITE_6_ROWS` | descriptive finite distance |
| T338-T6 | Twin--zero covariance sign is invariant under orbit growth | `REFUTED_SCOPED` | sign reversal on 6 rows |
| T338-T7 | A canonical signed covariance law follows from the source mask | `REFUTED_SCOPED` | nested control test |
| T338-T8 | Sign-free uniform masked envelope | `OPEN` | next project |

## Parent lock

TPC-337 producer SHA-256 (normalized LF):
`e74d621fa48fe7c15ff4e520dc2a051e5b195a5045c706592f275a6ead6b384d`.

TPC-337 certificate SHA-256 (normalized LF):
`558f9a2dc60cd6616230785b46934a415459211a2e1bc31083447c53dd40e1d2`.

`ROUND2_CLUE = REPLACE_SIGN_HEURISTICS_BY_A_UNIFORM_MASKED_OPERATOR_ENVELOPE`.
