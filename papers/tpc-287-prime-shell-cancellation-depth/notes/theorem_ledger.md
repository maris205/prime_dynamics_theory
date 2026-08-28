# TPC-287 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T287.1 | `g_shell=sum_q g_q` | `PROVED_EXACT` | every finite shell |
| T287.2 | `C_shell=sum_q C_q` | `PROVED_EXACT` | every linear attachment |
| T287.3 | interval retention envelope bounds the exact ratio | `PROVED_CONDITIONAL` | component-separated enclosures |
| T287.4 | shell anchors have cardinalities 1 through 7 | `NUMERICALLY_CERTIFIED` | 7 declared anchors |
| T287.5 | all component intervals are sign-separated | `NUMERICALLY_CERTIFIED` | 336 components |
| T287.6 | mixed-sign shell rows | `NUMERICALLY_CERTIFIED` | 57 of 84 rows |
| T287.7 | retention upper thresholds | `NUMERICALLY_CERTIFIED` | 31 / 22 / 8 rows for 1/2, 1/4, 1/10 |
| T287.8 | leave-one-prime-out sign flips and zero remainders | `NUMERICALLY_CERTIFIED` | 48 flips, 12 zeros |
| T287.9 | growing-shell cancellation stability | `OPEN` | no asymptotic theorem |

```text
STRONGEST_POSITIVE_RESULT = EXACT_FINITE_SHELL_ADDITIVITY_PLUS_57_MULTI_SIGN_ROWS
STRONGEST_OBSTRUCTION = RETENTION_IS_FINITE_AND_SHELL_CONTROL_DEPENDENT
OPEN_THEOREM = GROWING_SHELL_AND_SOURCE_CONTROL_CANCELLATION_STABILITY
REUSABLE_STRUCTURE = PRIME_COMPONENTS -> SIGNED SUM -> RETENTION ENVELOPE -> LEAVE_ONE_OUT
ROUND2_CLUE = TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS
```
