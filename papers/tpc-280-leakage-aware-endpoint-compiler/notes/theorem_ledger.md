# TPC-280 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T280.1 | `G/D <= B X^(-gamma)+(ell/d)X^(-delta)` | `PROVED_CONDITIONAL` | source floor plus raw two-term bound |
| T280.2 | reciprocal two-term gain compiler | `PROVED_CONDITIONAL` | `G>0`, zero case separated |
| T280.3 | dominant exponent `kappa=min(gamma,delta)` compiler | `PROVED_CONDITIONAL` | `X>=1`, `B+ell/d>0` |
| T280.4 | inherited margin-square compiler | `PROVED_CONDITIONAL` | exact parent identity assumed |
| T280.5 | equality family sharpness | `PROVED_CONDITIONAL` | abstract hypotheses |
| T280.6 | `delta<gamma` leakage bottleneck | `PROVED_CONDITIONAL` | positive leakage coefficient |
| T280.7 | six budget, four margin, four endpoint fixtures | `NUMERICALLY_CERTIFIED` | exact rational bookkeeping |
| T280.8 | TPC-279 twelve-row coordinate transfer | `NUMERICALLY_CERTIFIED` | finite parent rows only |

```text
STRONGEST_POSITIVE_RESULT = EXACT_TWO_TERM_ADDITIVE_LEAKAGE_GAIN_AND_MARGIN_COMPILER
STRONGEST_OBSTRUCTION = SLOWER_LEAKAGE_EXPONENT_CAPS_THE_GAIN_EXPONENT
OPEN_THEOREM = LITERAL_GROWING_SOURCE_DECOMPOSITION_WITH_ARITHMETIC_L2
REUSABLE_STRUCTURE = SOURCE_FLOOR -> NORMALIZE_TWO_TERMS -> DOMINANT_EXPONENT -> ENDPOINT_BUDGET
ROUND2_CLUE = AUDIT_TYPED_ARITHMETIC_L2_INTERFACE_FOR_FULL_GATE_B
```
