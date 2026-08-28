# TPC-289 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T289.1 | `G=(<g_q,g_r>)` is PSD | `PROVED_EXACT` | every finite shell |
| T289.2 | `0<=Gamma_(q,r)<=1` | `PROVED_EXACT` | nonzero component energies |
| T289.3 | positive coherence plus diagonal balance implies `R_E>=1+eta delta(k-1)` | `PROVED_EXACT_CONDITIONAL` | finite vector family |
| T289.4 | 17/18 rows are pairwise positive | `NUMERICALLY_CERTIFIED_FINITE` | 1,380 pair comparisons |
| T289.5 | three negative pairs occur at the early `s=1` crossover | `NUMERICALLY_CERTIFIED_FINITE_OBSTRUCTION` | one declared row |
| T289.6 | eight rows satisfy `eta=3/5,delta=4/5` | `NUMERICALLY_CERTIFIED_FINITE` | late-shell block |
| T289.7 | all 18 rows have `R_E>1` | `NUMERICALLY_CERTIFIED_FINITE` | declared grid |
| T289.8 | source-restricted/growing-shell coherence theorem | `OPEN` | no asymptotic proof |

```text
STRONGEST_POSITIVE_RESULT = EXACT_CONDITIONAL_COHERENCE_ACCUMULATION_ENVELOPE_PLUS_8_ROW_LATE_BLOCK
STRONGEST_OBSTRUCTION = THREE_EXACT_NEGATIVE_CROSS_PRIME_PAIRS_AND_NEAR_ZERO_COHERENCE_AT_N256_S1
OPEN_THEOREM = SOURCE_RESTRICTED_OR_GROWING_SHELL_COHERENCE_BOUND
REUSABLE_STRUCTURE = OUTPUT_GRAM -> SIGN_CENSUS -> NORMALIZED_COHERENCE -> CONDITIONAL_ENERGY_ENVELOPE
ROUND2_CLUE = TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_FINITE_BLOCK
```
