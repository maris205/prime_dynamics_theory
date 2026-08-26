# TPC-261: A Strict Endpoint-Budget Compiler for the Literal V59 Four-Packet Interface

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY
```

TPC-260 showed that the known packet marginals and Haar/null projections do not
identify the four-packet residual: the exact finite witness permits full
residual energies `0` and `16`.  TPC-261 records the endpoint consequence in a
strict budget theorem.  On the current common clock,

```text
E0=5/3=2000/1200,
E*=1997/1200,
E0-E*=1/400.
```

For a finite lane `l`, a proved saving `delta_l` and a paid reassembly loss
`lambda_l` leave effective credit `sigma_l=delta_l-lambda_l`.  The exact
compiler says that the target closes only when

```text
min_l sigma_l > 1/400.
```

Equality is power-level borderline.  A bound with any fixed power of `log x`
in the denominator has zero fixed-power credit, so the TPC-258/259 log-only
null suppression cannot be silently entered as payment for this gap.

The scaled TPC-260 plus/alternating families give a structural synthetic
obstruction: they have the same packet diagonal, zero Haar/null projections,
and baseline-scale plus residual `16*x^(5/3)` versus zero alternating residual.
This does not constitute a growing prime-shell counterexample and does not prove
that the literal route is impossible.  It proves only that the current
marginal interface cannot certify a global fixed-power saving without a new
mode-zero or signed cross-Gram theorem.

## Claim firewall

```text
TPC261_MAXIMUM_CLAIM = PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY
TPC261_ROUTE_ADVANCE = YES_SCOPED_ENDPOINT_BUDGET_COMPILER
TPC261_BUDGET_IDENTITY = PROVED_EXACT
TPC261_STRICT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC261_BORDERLINE_EQUALITY = PROVED_EXACT_POWER_LEVEL_ONLY
TPC261_LOG_ONLY_TO_POWER_PROMOTION = REFUTED_SCOPED
TPC261_SCALED_NULL_COMPATIBLE_WITNESS = PROVED_STRUCTURAL_SYNTHETIC
TPC261_GLOBAL_FIXED_POWER_CREDIT = NONE
TPC261_LITERAL_MODE_ZERO_ESTIMATE = OPEN
TPC261_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC261_ARITHMETIC_ADVANCE = NO
TPC261_FIXED_ATOM_CREDIT = 0
TPC261_L2 = NONE
TPC261_FULL_GATE_B = OPEN
TPC261_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC261_TWIN_PRIME_RESULT = NONE
TPC261_STATUS = PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY
```

## Reproduction

From the repository root:

```bash
python -B papers/tpc-261-strict-endpoint-budget-compiler/code/tpc261_endpoint_budget_certificate.py --check
python -O -B papers/tpc-261-strict-endpoint-budget-compiler/code/tpc261_endpoint_budget_certificate.py --check
python -B papers/tpc-261-strict-endpoint-budget-compiler/experiments/tpc261_independent_checker.py --check
python -O -B papers/tpc-261-strict-endpoint-budget-compiler/experiments/tpc261_independent_checker.py --check
python -B papers/tpc-261-strict-endpoint-budget-compiler/experiments/tpc261_budget_stress.py --check
```

The release bridge checker additionally freezes the source provenance, project
manifest, certificate, and both PDF copies.  Exact rational arithmetic is used
for the budget identities; the scaled witness is explicitly synthetic.

## Batch handoff

```text
STRONGEST_POSITIVE_RESULT = EXACT_LANE_WISE_ENDPOINT_BUDGET_COMPILER_AND_MINIMUM_SUFFICIENT_MODE_ZERO_THRESHOLD
STRONGEST_OBSTRUCTION = LOG_ONLY_NULL_SUPPRESSION_AND_SCALED_NULL_COMPATIBLE_RESIDUAL_PREVENT_ANY_AUTOMATIC_GLOBAL_FIXED_POWER_CREDIT
OPEN_THEOREM = LITERAL_COMMON_CLOCK MODE ZERO OR SIGNED CROSS GRAM ESTIMATE WITH EFFECTIVE SAVING GREATER THAN 1 OVER 400
REUSABLE_STRUCTURE = E0_TO_TARGET_GAP -> LANEWISE_SAVING_MINUS_LOSS -> LOG_POWER_FIREWALL -> SCALED_TPC260_WITNESS -> MINIMUM_LITERAL_THEOREM
ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400
```

The named Session `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  The proof package, theorem ledger, exact certificate,
bridge checker, and `AGENTS.md` supply the available fail-closed local
authority; no route gate is promoted by their absence.
