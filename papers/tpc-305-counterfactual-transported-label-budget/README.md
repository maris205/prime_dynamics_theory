# TPC-305 - Counterfactual transported-label native budgets

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-304 identified `Q=60->70` as the unique overlap-label fracture supporting
all nine same-prefix parent budget descents, but could not separate target
switching from physical-shell change.  TPC-305 holds each full shell/operator
fixed, swaps only the optimally aligned neighboring label on the overlap (with
native labels off the overlap), and recomputes the finite profile budget.  The
18-case, 36-table atlas finds at the middle transition that the right-neighbor
label is cheaper on both fixed operators in 5/6 cases; the remaining case favors
the home operator.  All 3/3 inherited same-prefix cases are in the first class.

This is a finite partial counterfactual control, not a causal or asymptotic
theorem.

## What is new

For a fixed operator `V` and source Gram `M`, the native and transported targets
are evaluated by the same constrained quadratic program

```text
min c^T M c  subject to  ||V_k c-b|| <= tau ||b||,
```

at the common feasible prefix `k=max(k_native,k_transport)`.  This makes the
within-row target change explicit and auditable.  The central orientation
census is:

```text
Q=50->60: left-label cheaper 4, cross-target cheaper 2
Q=60->70: right-label cheaper 5, home-operator favored 1
Q=70->90: left-label cheaper 3, cross-target cheaper 1, home favored 2
```

All three normalizers give the same strict orientation in every case.

## Claim firewall

```text
PROVED_EXACT_FINITE = optimal binary alignment, transported-target protocol,
                      common-prefix feasibility, fixed-operator target-swap logic
NUMERICALLY_CERTIFIED_FINITE = 18 cases, 36 tables, central 5/6 and 3/3 census
MODELING_CHOICE = finite spine, native off-overlap extension, max-prefix rule
OPEN = cross-operator interaction/causal separation, uniform asymptotic budget,
       arithmetic L2, fixed-power credit, full Gate B, twin-prime conclusion
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = at the TPC-304 fracture, the neighboring right label
                            is cheaper on both fixed physical operators in 5/6 cases
STRONGEST_OBSTRUCTION = the two operators remain different, so this is not a
                        causal separation and outer transitions reverse orientation
OPEN_THEOREM = decompose the two-way operator/target table into home effects and
               an interaction term, with an operator holdout
REUSABLE_STRUCTURE = overlap alignment -> native off-overlap extension -> common
                     prefix -> fixed-operator quadratic budget -> orientation atlas
ROUND2_CLUE = TEST_TWO_WAY_OPERATOR_HOLDOUT_AND_INTERACTION_TERM_BEFORE_ANY_CAUSAL_TARGET_OPERATOR_CLAIM
```

## Reproduction

```text
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc305_counterfactual_transported_label_budget.py --write
python -B code/tpc305_counterfactual_transported_label_budget.py --check
python -B experiments/tpc305_independent_checker.py
python -B experiments/tpc305_transport_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc305_counterfactual_transported_label_budget_checker.py --check
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent; no official evaluator pass is
asserted.  The local theorem ledger, parent-locked certificate, independent
replay, stress suite, PDF audit, and Bridge-B checker are the fail-closed
validation path.
