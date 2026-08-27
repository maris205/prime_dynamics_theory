# TPC-278 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T278.1 | `E<0` iff `D/G>1` | `PROVED_EXACT` | positive finite `D,G` |
| T278.2 | 12-row exact source Q/H census | `NUMERICALLY_CERTIFIED` | declared finite grid |
| T278.3 | four shell/clock sign flips | `NUMERICALLY_CERTIFIED` | finite paths |
| T278.4 | finite `r>=1` stability | `REFUTED_SCOPED` | Q/H perturbation family |
| T278.5 | growing source-level stability | `OPEN` | no asymptotic promotion |

```text
STRONGEST_POSITIVE_RESULT = EXACT_12_ROW_SOURCE_CENSUS_WITH_4_SIGN_FLIPS
STRONGEST_OBSTRUCTION = SHELL_OR_CLOCK_CHANGE_CAN_REVERSE_SIGNED_GAIN
OPEN_THEOREM = MINIMAL_SOURCE_LEVEL_COHERENCE_TO_GAIN_HYPOTHESIS
REUSABLE_STRUCTURE = Q/H perturbation -> E sign -> gain stability test
ROUND2_CLUE = FORMULATE_MINIMAL_SOURCE_LEVEL_COHERENCE_TO_GAIN_THEOREM
```
