# TPC-279 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T279.1 | `0<=G/D<=4`, `G-D=2E`, exact deficit identity | `PROVED_EXACT` | four Hilbert-space packets |
| T279.2 | power gain iff `G/D` has the matching upper bound | `PROVED_EXACT` | `D>0,G>0` (zero-sum endpoint extended) |
| T279.3 | `G/D<=min(4,1+3mu)` | `PROVED_EXACT` | pairwise absolute coherence |
| T279.4 | reciprocal pairwise gain floor is sharp | `PROVED_EXACT` | equicorrelation Gram family |
| T279.5 | coherence-only positive-power promotion | `REFUTED_EXACT` | orthogonal witness |
| T279.6 | TPC-278 coordinate transfer | `NUMERICALLY_CERTIFIED` | 12 finite parent rows |
| T279.7 | growing source-level deficit estimate | `OPEN` | asymptotic arithmetic interface |

```text
STRONGEST_POSITIVE_RESULT = EXACT_NECESSARY_AND_SUFFICIENT_DEFICIT_CRITERION
STRONGEST_OBSTRUCTION = ABSOLUTE_PAIRWISE_COHERENCE_CANNOT_PAY_POWER
OPEN_THEOREM = SCHEDULE_SPECIFIC_AGGREGATE_G_OVER_D_DEFICIT_BOUND
REUSABLE_STRUCTURE = D,G,E -> q -> Delta -> exact power criterion -> endpoint compiler
ROUND2_CLUE = COMPILE_COHERENCE_DEFICIT_WITH_MARGIN_AND_ARITHMETIC_L2
```
