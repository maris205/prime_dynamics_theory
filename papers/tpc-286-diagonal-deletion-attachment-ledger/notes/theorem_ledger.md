# TPC-286 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T286.1 | `B_q(u,u)=m_q(u)(q-2)/(q-1)` | `PROVED_EXACT` | finite literal block |
| T286.2 | `g_phys=g_full-g_diag` with explicit `g_diag` | `PROVED_EXACT` | any finite shell/source vector |
| T286.3 | `C_phys=C_full-C_diag` | `PROVED_EXACT` | declared linear attachment |
| T286.4 | all three component intervals are sign-separated | `NUMERICALLY_CERTIFIED` | 72 registered controls |
| T286.5 | full-versus-physical sign flips | `NUMERICALLY_CERTIFIED` | 15 of 72 rows |
| T286.6 | diagonal correction opposes physical term | `NUMERICALLY_CERTIFIED` | 30 of 72 rows |
| T286.7 | diagonal magnitude strictly exceeds physical magnitude | `NUMERICALLY_CERTIFIED` | 21 of 72 rows |
| T286.8 | asymptotic diagonal dominance | `OPEN` | no growing theorem |
| T286.9 | signed full-shell arithmetic `L2` bound | `OPEN` | cross-prime cancellation required |

```text
STRONGEST_POSITIVE_RESULT = EXACT_OPERATOR_AND_ATTACHMENT_DIAGONAL_SPLIT
STRONGEST_OBSTRUCTION = FINITE_DIAGONAL_SENSITIVITY_AND_15_SIGN_FLIPS
OPEN_THEOREM = SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_SPLIT
REUSABLE_STRUCTURE = CENTERED_RESIDUE_BLOCK -> DELETED_DIAGONAL -> COMPONENT_LEDGER
ROUND2_CLUE = SEEK_SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_ATTACHMENT_LEDGER
```
