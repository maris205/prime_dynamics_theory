# TPC-307 — Common-Ambient Union-Shell Holdout

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-307 puts each adjacent prime-shell pair in one union ambient operator,
fits two aligned directional targets only on the overlap, and evaluates their
native exclusive pieces as withheld holdouts.  The finite replay contains 18
cases, 36 directional fits, and 54 normalizer rows: 13 budget/holdout
comparisons are concordant, 3 are discordant, and 2 are unresolved.  All three
discordances occur on `Q=70 -> 90`, exponent 1, at all three tolerances.

This is a finite diagnostic and a scoped obstruction to reading the budget
orientation as a stable extrapolation rule.  It is not causal, asymptotic,
arithmetic, or a twin-prime result.

## Claim firewall

```text
PROVED_EXACT_FINITE = union/overlap/exclusive partition; directional
                      overlap-only frontier; holdout separation; global-sign
                      invariance; common-prefix feasibility
NUMERICALLY_REPRODUCED_FINITE = 18 cases, 36 directional fits, 54 normalizer
                                 rows; 13 concordant, 3 discordant, 2 unresolved
NUMERICAL_OBSERVATION = all three discordances localize at Q=70->90, exponent 1
MODELING_CHOICE = native exclusive completions and fixed profile-prefix spine
INHERITED_LEAKAGE = TPC-302 physical-Gram-dependent target labels
OPEN = formal directed-rounding enclosure; causal identification; uniform
       asymptotic budget; arithmetic L2; fixed-power credit; full Gate B
       twin-prime conclusion
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = exact common-ambient directional holdout protocol
STRONGEST_OBSTRUCTION = 3/18 budget-vs-holdout discordances, all at 70->90,
                        exponent 1; 2 additional cells unresolved
OPEN_THEOREM = determine whether the localized discordance survives admissible
               off-overlap completion envelopes and profile-prefix perturbations
REUSABLE_STRUCTURE = U/O/E partition -> overlap constrained frontier ->
                     exclusive holdout -> ratio-classification census
ROUND2_CLUE = STRESS_COMMON_AMBIENT_HOLDOUT_AGAINST_EXCLUSIVE_COMPLETION_ENVELOPES_AND_PROFILE_PREFIX_PERTURBATIONS_BEFORE_ANY_CAUSAL_PREFERENCE_CLAIM
```

## Reproduction

```text
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc307_common_ambient_union_shell_holdout.py --write
python -B code/tpc307_common_ambient_union_shell_holdout.py --check
python -B experiments/tpc307_independent_checker.py
python -B experiments/tpc307_holdout_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc307_common_ambient_union_shell_holdout_checker.py --check
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
`propose.md` and Route-A/Route-B evaluator files are absent from this checkout;
no official evaluator pass is asserted.  The local fail-closed path consists
of the locked parent certificate, independent replay, stress suite, theorem
ledger, PDF audit, and Bridge-B checker.
