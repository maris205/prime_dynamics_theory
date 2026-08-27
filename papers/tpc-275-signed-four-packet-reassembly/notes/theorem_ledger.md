# TPC-275 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T275.1 | signed packet Gram expansion | `PROVED_EXACT_FINITE` | every finite real/complex packet family |
| T275.2 | four-point DFT Parseval and mode-zero identities | `PROVED_EXACT_FINITE` | every finite Hilbert space |
| T275.3 | two-probe real polarization | `PROVED_EXACT_FINITE` | real finite packets |
| T275.4 | net cross term `G-D<0` | `NUMERICALLY_CERTIFIED` | all 12 literal rows |
| T275.5 | `1<D/G<12/5` and `F/G>50` | `NUMERICALLY_CERTIFIED` | all 12 literal rows |
| T275.6 | packet-diagonal margin proxy `<1/16` | `NUMERICALLY_CERTIFIED` | all 12 literal rows |
| T275.7 | growing signed cross-Gram estimate | `OPEN` | source-level theorem absent |

```text
STRONGEST_POSITIVE_RESULT = EXACT_SIGNED_GRAM_DFT_POLARIZATION_PLUS_LITERAL_REPLAY
STRONGEST_OBSTRUCTION = DIAGONAL_ENVELOPE_CANNOT_CERTIFY_QUARTER_MARGIN_ON_12_ROWS
OPEN_THEOREM = SOURCE_LEVEL_SIGNED_CROSS_GRAM_WITH_EFFECTIVE_SAVING
REUSABLE_STRUCTURE = PACKET_GRAM -> POLARIZATION -> DFT_MODE_ZERO -> MARGIN_BUDGET
ROUND2_CLUE = COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET
```
