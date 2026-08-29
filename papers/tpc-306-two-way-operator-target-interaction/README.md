# TPC-306 - Two-way operator/target interaction decomposition

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-305 produced four budget cells per adjacent shell pair but left the
cross-operator interaction implicit.  TPC-306 arranges those cells as an
`operator x target` table and defines the two log target-switch effects
`d_L=log(B_LR/B_LL)` and `d_R=log(B_RR/B_RL)`.  Their mean `m` is the target-main
contrast and their half-difference `i` is the operator interaction contrast;
the exact identity `m^2-i^2=d_L*d_R` decides which dominates.  On all 18
TPC-305 cases (54 normalizer rows), target-main dominance occurs in `12/18`
cases and interaction dominance in `6/18`, with no unresolved case.  At the
central `Q=60->70` fracture the split is `5/6` versus `1/6`, and all `3/3`
same-prefix cases are target-main dominant.

The main-dominant interaction/main magnitude ratio is always below `0.88`, the
interaction-dominant ratio is always above `1.2`, and the central same-prefix
maximum is below `0.64`.  These are finite diagnostics, not causal or
asymptotic claims.

## What is new

The decomposition exposes the exact information content of the TPC-305
counterfactual.  A stable neighboring-label preference has same-sign row
effects and therefore `|m|>|i|`; a mixed preference has opposite-sign effects
and therefore `|i|>|m|`.  Independent positive row normalizations cancel from
the effects.  Thus the central signal is target-main-dominant in five cases,
while six outer/mixed cases demonstrate that interaction cannot be ignored.

## Claim firewall

```text
PROVED_EXACT_FINITE = four-cell log decomposition, squared dominance identity,
                      positive row-scaling invariance
NUMERICALLY_CERTIFIED_FINITE = 54 derived rows; target-main 12/18;
                                interaction 6/18; middle 5/6; same-prefix 3/3
MODELING_CHOICE = shell-specific target completion and finite log table
OPEN = common-ambient causal identification, uniform asymptotics, arithmetic L2,
       fixed-power credit, full Gate B, twin-prime conclusion
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = exact contrast identity plus a clean finite gap:
                            main q<0.88 versus interaction q>1.2
STRONGEST_OBSTRUCTION = 6/18 cases are interaction-dominant, including 1/6 at
                        the central fracture; the two rows use different operators
OPEN_THEOREM = build a common-ambient union-shell holdout and test interaction
               stability under alternative off-overlap completions
REUSABLE_STRUCTURE = four-cell budget table -> log effects -> main/interaction
                     identity -> dominance atlas
ROUND2_CLUE = TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM
```

## Reproduction

```text
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc306_two_way_operator_target_interaction.py --write
python -B code/tpc306_two_way_operator_target_interaction.py --check
python -B experiments/tpc306_independent_checker.py
python -B experiments/tpc306_interaction_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc306_two_way_operator_target_interaction_checker.py --check
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent; no official evaluator pass is
asserted.  The theorem ledger, parent-locked certificate, independent replay,
stress suite, PDF audit, and Bridge-B checker provide the local fail-closed
validation path.
