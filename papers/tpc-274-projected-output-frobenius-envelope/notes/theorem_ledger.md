# TPC-274 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T274.1 | `G_perp <= ||A_perp||_F^2 ||beta||_2^2` | PROVED_EXACT_FINITE | any finite matrix row |
| T274.2 | `m_F^2 <= m^2` when `G_F` is used | PROVED_EXACT_FINITE | positive finite lanes |
| T274.3 | `G_F/G_perp>50` | NUMERICALLY_CERTIFIED | all 12 registered rows |
| T274.4 | `m_F^2<1/64` | NUMERICALLY_CERTIFIED | all 12 registered rows |
| T274.5 | cancellation-free projected output route proves quarter margin | REFUTED_SCOPED | registered finite interface only |
| T274.6 | source-level signed output reassembly | OPEN | no theorem supplied |

```text
STRONGEST_POSITIVE_RESULT = PROVED_PROJECTED_FROBENIUS_ENVELOPE_PLUS_EXACT_MATRIX_REPLAY
STRONGEST_OBSTRUCTION = ENVELOPE_GAP_ABOVE_50_AND_ENVELOPE_MARGIN_BELOW_1_OVER_8
OPEN_THEOREM = SOURCE_LEVEL_SIGNED_OUTPUT_REASSEMBLY_BEYOND_NORM_ONLY_CONTROL
REUSABLE_STRUCTURE = OPERATOR -> PROJECTED_FROBENIUS_ENVELOPE -> CONSERVATIVE_MARGIN -> GAP_TEST
ROUND2_CLUE = TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES
```
