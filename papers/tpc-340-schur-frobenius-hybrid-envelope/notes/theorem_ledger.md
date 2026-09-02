# TPC-340 theorem ledger

| ID | Claim | Status | Ceiling |
|---|---|---|---|
| T340-T1 | Symmetric Schur envelope | `PROVED_EXACT_FINITE_DECLARED_MODEL` | every finite symmetric matrix |
| T340-T2 | Schur/Frobenius hybrid envelope | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite norm inequalities |
| T340-T3 | 216-record replay with zero violations | `NUMERICALLY_CERTIFIED_FINITE` | fixed panel |
| T340-T4 | Schur branch active in 54 records | `NUMERICALLY_CERTIFIED_FINITE` | declared masks/controls |
| T340-T5 | Zero-support Frobenius slack improves by factor `1.25--4.70` | `NUMERICALLY_CERTIFIED_FINITE` | finite panel |
| T340-T6 | Hybrid is factor-five tight on all broad masks | `REFUTED_SCOPED` | broad finite records |
| T340-T7 | Uniform arithmetic operator bound | `OPEN` | no growing payment |

## Parent lock

TPC-339 producer SHA-256 (normalized LF):
`df76022bfa5051477ec5bc04fef444aefc22abcb8f76fa02b339b7bc769fad18`.

TPC-339 certificate SHA-256 (normalized LF):
`af6636eb7c9d9c6cbc0d392ae0b9effbaa9610dedafa12ee8d1272163fd48372`.

`ROUND2_CLUE = TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT`.
