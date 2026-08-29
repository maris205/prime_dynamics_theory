# TPC-304 - Overlapping-shell sign-label transport

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-303 found 21 budget descents on a fixed-source moving-shell spine.  TPC-304
restricts the TPC-302 source-first weighted labels to adjacent-shell overlaps,
aligns their unavoidable global signs, and obtains six exact finite transport
rows.  The group means of the gauge-invariant overlap correlation are
`1/2, 1/11, 1/2` for `Q=50->60`, `60->70`, and `70->90`; the middle transition is
the unique low-correlation fracture.  The independently replayed TPC-303
budget descent counts are `3,15,3`, and its same-prefix descent counts are
`0,9,0`, so all nine same-prefix descents occur at that fracture.

## What is new

The exact identity

```text
rho_align = |sum_{p in overlap} a(p)b(p)| / |overlap|
d_align   = (1-rho_align)/2
```

removes the arbitrary global-sign gauge from cross-shell label comparisons.
The resulting crosswalk localizes a common transition of target-label change
and native-budget descent.  It is a finite association result, not a causal
separation: a counterfactual budget with a transported label is still needed to
decide whether the physical operator or the target switching is responsible.

## Claim firewall

    PROVED_EXACT_FINITE = gauge-invariant overlap identity and
    correlation/disagreement formula
    NUMERICALLY_CERTIFIED_FINITE = six transport rows; mean correlations
    1/2,1/11,1/2; unique Q=60->70 fracture; budget descents 3,15,3;
    same-prefix descents 0,9,0
    MODELING_CHOICE = fixed source spine and rho<=1/3 coarse fracture threshold
    OPEN = causal target/operator separation, uniform asymptotic budget growth,
    arithmetic L2, fixed-power credit, full Gate B, twin-prime conclusion

## Research extraction

    STRONGEST_POSITIVE_RESULT = the unique minimum transport correlation and
    maximum budget-descent concentration occur at the same Q transition.
    STRONGEST_OBSTRUCTION = this coincidence cannot by itself distinguish
    target-label switching from physical shell/operator change.
    OPEN_THEOREM = compute counterfactual transported-label native budgets and
    prove or refute a target/operator separation principle.
    REUSABLE_STRUCTURE = overlapping shell -> global-sign gauge alignment ->
    exact mismatch census -> parent budget crosswalk.
    ROUND2_CLUE = COMPUTE_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGETS_TO_SEPARATE_TARGET_SWITCHING_FROM_OPERATOR_CHANGE

## Reproduction

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc304_overlapping_shell_label_transport.py --write
    python -B code/tpc304_overlapping_shell_label_transport.py --check
    python -B experiments/tpc304_independent_checker.py
    python -B experiments/tpc304_transport_stress.py
    python -B research/tpc-big-road/tpc_bridge_b_tpc304_overlapping_shell_label_transport_checker.py --check

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent; no official evaluator pass is
asserted.  The local theorem ledger, parent-locked certificate, independent
replay, stress suite, PDF audit, and Bridge-B checker form the fail-closed
validation path.
