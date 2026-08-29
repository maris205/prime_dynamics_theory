# TPC-303 - Fixed-source cardinality monotonicity obstruction

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-302 established a growing-grid budget gap but left the growth law of the
weighted native budget open.  TPC-303 freezes the source scale (`512`), height
(`58`), comparison cutoff (`5`), and tests the shell spine `Q=50,60,70,90`,
whose cardinalities are `10,13,15,17`.  Across two kernel exponents, three
tolerances, and three normalizations there are 54 adjacent transitions: 21
are interval-certified descents, 33 are ascents, and none are unresolved.
All 18 parameter series are certified nonmonotone.  Nine descents occur with
the same common profile prefix; the strongest same-prefix contraction has
right/left ratio below `0.284422` (the strongest descent overall is below
`0.224974`).

## What is new

This is a scoped negative result against a tempting cardinality-only shortcut:
larger finite prime shells do not force a larger native weighted budget, even
when the source scale and the common profile prefix are unchanged.  The
interval criterion is exact; the numerical input is inherited from the frozen
TPC-302 certificate.  The result does not refute an eventual asymptotic lower
bound and does not claim shell inclusion, since the Q-spine shells are moving
intervals rather than nested sets.

## Claim firewall

    PROVED_EXACT_FINITE = interval descent/ascent criterion and the logical
    finite refutation of a nondecreasing law from one certified descent
    NUMERICALLY_CERTIFIED_FINITE = 54 adjacent transitions; 21 descents,
    33 ascents, zero unresolved; 18/18 nonmonotone series; 9 same-prefix
    descents
    NUMERICAL_OBSERVATION = contraction ratios and selected witness values
    MODELING_CHOICE = fixed-source Q-spine, two exponents, three tolerances,
    three source normalizers, and use of TPC-302 common-prefix budgets
    OPEN = uniform asymptotic budget growth, arithmetic L2, fixed-power credit,
    full Gate B, and the twin-prime conjecture

## Research extraction

    STRONGEST_POSITIVE_RESULT = every declared exponent/tolerance/normalizer
    series has a certified descent and ascent, so the obstruction is not a
    single normalization accident.
    STRONGEST_OBSTRUCTION = Q=60 -> 70 produces a same-prefix native-budget
    contraction below 0.284422 at exponent 2 and tau=3/4.
    OPEN_THEOREM = characterize the source/profile/target mechanism causing
    budget descents and determine whether any uniform growth law survives.
    REUSABLE_STRUCTURE = frozen-source shell spine -> interval-certified
    adjacent transition -> same-prefix confounder firewall.
    ROUND2_CLUE = LOCALIZE_BUDGET_DESCENTS_BY_TRANSPORTING_SIGN_LABELS_ACROSS_OVERLAPPING_SHELLS

## Reproduction

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc303_cardinality_monotonicity_obstruction.py --write
    python -B code/tpc303_cardinality_monotonicity_obstruction.py --check
    python -B experiments/tpc303_independent_checker.py
    python -B experiments/tpc303_stress.py
    python -B research/tpc-big-road/tpc_bridge_b_tpc303_cardinality_monotonicity_obstruction_checker.py --check

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent; no official evaluator pass is
asserted.  Local proof, interval replay, stress, PDF, and Bridge-B checks are
the fail-closed validation path.
