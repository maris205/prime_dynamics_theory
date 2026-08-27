# TPC-285 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T285.1 | `B_q=R_q(I-11^T/(q-1))R_q^T` | `PROVED_EXACT` | any odd prime and finite index set |
| T285.2 | `rank(B_q)<=q-2`, with equality under full class coverage | `PROVED_EXACT` | centered block |
| T285.3 | deleted-diagonal `D_q` has full active rank under full class coverage | `PROVED_EXACT` | all class sizes positive |
| T285.4 | all registered rows have full class coverage | `NUMERICALLY_CERTIFIED` | 20 prime/exponent rows |
| T285.5 | `K_H o D_q` has full active rational rank | `NUMERICALLY_CERTIFIED` | same 20 rows, modular witness |
| T285.6 | centered low rank transfers to literal arithmetic `L2` | `REFUTED_AS_DIRECT_SHORTCUT` | diagonal deletion destroys rank bound |
| T285.7 | useful signed/full-shell arithmetic `L2` estimate | `OPEN` | cross-prime and source structure needed |

```text
STRONGEST_POSITIVE_RESULT = EXACT_DELETED_DIAGONAL_FULL_ACTIVE_RANK_THEOREM
STRONGEST_OBSTRUCTION = CENTERED_Q_MINUS_2_RANK_DOES_NOT_SURVIVE_PHYSICAL_DIAGONAL_DELETION
OPEN_THEOREM = SIGNED_FULL_SHELL_SPECTRAL_OR_L2_BOUND_USING_MORE_THAN_RANK
REUSABLE_STRUCTURE = RESIDUE_FACTOR -> DIAGONAL_SPLIT -> CLASS_SUBSPACE_DECOMPOSITION
ROUND2_CLUE = SEPARATE_RESIDUE_MODE_FACTORIZATION_FROM_DELETED_DIAGONAL_AND_KERNEL_RANK_BEFORE_LITERAL_L2
```
