# TPC-284 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T284.1 | The six control maps are a deterministic finite enumeration | `PROVED_EXACT_DEFINITION` | declared schedule controls only |
| T284.2 | Every one of 72 controlled attachment intervals is sign-separated | `NUMERICALLY_CERTIFIED` | frozen finite source engine |
| T284.3 | The sign census is 60 negative, 12 positive, 0 crossing | `NUMERICALLY_CERTIFIED` | 72 rows |
| T284.4 | Eight controlled rows flip sign against TPC-283 baseline | `NUMERICALLY_CERTIFIED` | finite comparison |
| T284.5 | The weakest controlled lower `rho^2` is about `1.4118e-5` | `NUMERICALLY_CERTIFIED` | minimum over 72 rows |
| T284.6 | Uniform control stability on a growing schedule | `OPEN` | no asymptotic theorem |
| T284.7 | Full admissible literal-source class is captured by six controls | `OPEN` | not claimed |

```text
STRONGEST_POSITIVE_RESULT = FINITE_72_ROW_CONTROL_ATLAS_ALL_SIGN_SEPARATED
STRONGEST_OBSTRUCTION = 8_BASELINE_SIGN_FLIPS_UNDER_NAMED_CONTROLS
OPEN_THEOREM = GROWING_SCHEDULE_CONTROL_STABILITY_WITH_A_DECLARED_SOURCE_CLASS
REUSABLE_STRUCTURE = BASELINE_SOURCE_LOCK -> CONTROL_MAP -> INTERVAL_SIGN_ATLAS
ROUND2_CLUE = COMPILE_PRIME_SHELL_CONTROL_CONSTRAINTS_BEFORE_ANY_ASYMPTOTIC_STABILITY_CLAIM
```
