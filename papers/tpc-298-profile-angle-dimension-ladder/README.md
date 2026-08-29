# TPC-298 — Literal source-profile angle and dimension ladder

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-298 replaces the fixed four-profile snapshot of TPC-297 by an ordered
literal cutoff ladder

```text
Z = {3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61}.
```

For the prefix source space `U_k` and its physical image `V_k=A^T U_k`, the
least-squares residual is exactly the sine of the principal angle from a
target to `range(V_k)`, and these residuals decrease along the nested ladder.
On the inherited 18-row, 1,380-edge grid, every prefix has the expected rank
`min(k,|S|)` under both declared moduli.  The weighted target needs at least
`2/3` of the shell dimension to reach normalized RMS `1/2` on every row,
whereas the all-positive control reaches the same threshold in at most six
profiles on every row.

This is a finite dimension/angle atlas.  It does not prove a growing native
profile theorem, arithmetic `L2`, a fixed-power saving, Gate B, or the twin
prime conjecture.

## What advances

- proves the exact principal-angle and nested-prefix identities for any finite
  restricted source ladder;
- upgrades the four-cutoff audit to all 17 declared literal cutoff prefixes;
- certifies the complete prefix-rank ladder with two independent modular
  replays;
- separates a diffuse weighted target from a rapidly captured all-positive
  control using one common threshold;
- turns the next obstruction into a quantitative question about dimension,
  conditioning, and source budget rather than an unspecified source image.

## Finite headline

```text
profile cutoffs = 17 literal cutoffs through 61
rows = 18
shell edges = 1,380
prefix-rank ladder = expected min(k, shell size), 18/18 rows, both moduli
weighted half-RMS dimension ratio >= 2/3 = 18/18
all-positive half-RMS dimension <= 6 = 18/18
full prefix reaches the finite target space = 18/18
fixed-power credit = 0
```

The ratio `2/3`, threshold `1/2`, and cutoff list are declared finite
diagnostics/modeling choices.  They are not uniform asymptotic constants.

## Claim ceiling

```text
PROVED_EXACT_FINITE = projection, principal-angle, and nested-prefix identities
NUMERICALLY_CERTIFIED_FINITE = two-modulus 18-row complete prefix-rank ladder
NUMERICAL_OBSERVATION = weighted/all-positive finite dimension separation
MODELING_CHOICE = literal cutoff ladder and half-RMS diagnostic
OPEN = growing profile dimension, angle lower bounds, condition/budget growth
OPEN = arithmetic L2, fixed-power credit, full Gate B
TWIN_PRIME_RESULT = NONE
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = COMPLETE_EXPECTED_RANK_LADDER_AND_EXACT_FINITE_TARGET_CAPTURE
STRONGEST_OBSTRUCTION = WEIGHTED_TARGET_REQUIRES_AT_LEAST_TWO_THIRDS_OF_SHELL_DIMENSION_FOR_HALF_RMS
OPEN_THEOREM = GROWING_NATIVE_PROFILE_DIMENSION_OR_PRINCIPAL_ANGLE/CONDITIONING_BOUND
REUSABLE_STRUCTURE = NESTED_LITERAL_SOURCE_PREFIX -> IMAGE -> PRINCIPAL_ANGLE -> DIMENSION THRESHOLD
ROUND2_CLUE = TEST_WEIGHTED_PROFILE_DIMENSION_AGAINST_LEAST_NORM_SOURCE_BUDGET_AND_CONDITIONING
```

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc298_profile_angle_dimension_certificate.py --write
python -B code/tpc298_profile_angle_dimension_certificate.py --check
python -B experiments/tpc298_independent_checker.py
python -B experiments/tpc298_ladder_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
theorem ledger, canonical certificate, independent source-first replay,
adversarial ladder fixtures, PDF audit, and Bridge-B checker are the available
fail-closed validation path.
