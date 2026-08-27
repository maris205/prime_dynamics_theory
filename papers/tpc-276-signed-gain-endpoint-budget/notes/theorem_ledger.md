# TPC-276 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T276.1 | `m^2=(D/G)m_D^2` | `PROVED_EXACT_FINITE` | positive finite rows |
| T276.2 | signed gain exponent contributes `gamma/2` to margin budget | `PROVED_CONDITIONAL` | growing hypotheses stated in Theorem 2 |
| T276.3 | strict target condition `sigma-eta_eff>1/400`, `eta_eff=max(0,eta_D-gamma/2)` | `PROVED_CONDITIONAL` | `E0=5/3`, `E*=1997/1200` |
| T276.4 | signed-margin transfer and threshold classification | `NUMERICALLY_CERTIFIED` | all 12 TPC-275 rows |
| T276.5 | finite gain table gives no fixed-power credit | `REFUTED_SCOPED` | finite-to-asymptotic promotion |
| T276.6 | uniform source-level signed gain lower bound | `OPEN` | literal growing source |

```text
STRONGEST_POSITIVE_RESULT = EXACT_SIGNED_GAIN_MARGIN_IDENTITY_AND_CONDITIONAL_COMPILER
STRONGEST_OBSTRUCTION = FINITE_GAIN_HAS_ZERO_FIXED_POWER_CREDIT
OPEN_THEOREM = UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND_WITH_MARGIN_CONTROL
REUSABLE_STRUCTURE = D_OVER_G -> MARGIN_SQUARED -> HALF_EXPONENT -> STRICT_BUDGET
ROUND2_CLUE = SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND
```
