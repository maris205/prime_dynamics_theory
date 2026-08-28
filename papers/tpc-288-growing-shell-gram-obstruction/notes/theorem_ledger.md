# TPC-288 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T288.1 | `A_S=sum_q A_q` | `PROVED_EXACT` | every finite shell |
| T288.2 | `g_S=sum_q g_q` and `C_S=sum_q C_q` | `PROVED_EXACT` | frozen source and linear attachment |
| T288.3 | output Gram is PSD and `1^T G 1=||g_S||^2` | `PROVED_EXACT` | every finite row |
| T288.4 | Gram has full rational rank | `NUMERICALLY_CERTIFIED_FINITE` | 34 rows |
| T288.5 | Gram spectrum is strictly positive | `NUMERICALLY_CERTIFIED_FINITE` | 34 rows, via PSD + rank |
| T288.6 | aggregate physical active matrix has full rank | `NUMERICALLY_CERTIFIED_FINITE` | 6 selected rows |
| T288.7 | scalar retention upper `<1/10` and energy ratio `>1` coexist | `NUMERICALLY_CERTIFIED_FINITE_OBSTRUCTION` | 13 rows |
| T288.8 | joint growing-shell/source-control stability | `OPEN` | no asymptotic theorem |

```text
STRONGEST_POSITIVE_RESULT = EXACT_OUTPUT_GRAM_IDENTITY_AND_FINITE_POSITIVE_SPECTRUM
STRONGEST_OBSTRUCTION = 13_ROWS_SCALAR_CANCELLATION_WITH_VECTOR_ENERGY_AMPLIFICATION
OPEN_THEOREM = SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUND_BEYOND_FINITE_FULL_RANK
REUSABLE_STRUCTURE = PRIME_COMPONENTS -> OUTPUT_GRAM -> ACTIVE_OPERATOR_RANK -> SCALAR/ENERGY FIREWALL
ROUND2_CLUE = TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_FULL_RANK_OBSTRUCTION
```
