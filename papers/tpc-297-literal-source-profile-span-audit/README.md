# TPC-297 — Literal source-profile span audit

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

The natural four-profile family
\[
 \beta_z(t)=\lambda(t)-\sum_{d\leq z,\ d\mid t}\mu(d),
 \qquad z\in\{3,5,7,11\},
\]
has a rigorously defined restricted correlation image.  The exact least
square residual in that image is the orthogonal projection residual
`b^T(I-P_V)b`, where `V=A^T U` and `U` contains the four literal profiles.
On the inherited 18-row grid, two-modulus rank checks give image dimension
`3` on the 3-prime shell and `4` on all 17 larger shells.  A 70-digit replay
finds all-positive targets within RMS `0.138`, while the TPC-294 weighted
targets remain at RMS at least `0.626` on all 17 larger shells.

This is a finite restricted-profile advance, not an asymptotic native-profile
theorem: no arithmetic `L2`, fixed-power credit, Gate B, or twin-prime
conclusion is claimed.

## What advances

- defines a non-arbitrary source family from four literal local Möbius
  cutoffs, rather than selecting directions from the ambient target space;
- proves the exact projection and nested-span identities for any restricted
  source matrix;
- certifies the finite image rank with two independent modular replays;
- records a positive control: the four-profile image captures the
  all-positive target very well on every registered row;
- records a negative control: the weighted sign optimum remains separated
  from the four-profile image on every shell with at least five primes;
- isolates the next obstruction as profile dimension/angle, rather than
  unrestricted source existence.

## Finite headline

```text
profile cutoffs = {3,5,7,11}
rows = 18
shell edges = 1,380
image rank = 3 on 1 row, 4 on 17 rows (both moduli)
weighted RMS >= 0.6 on large shells = 17 / 17
all-positive RMS <= 0.15 = 18 / 18
four-profile residual never exceeds one-ray residual = 18 / 18
fixed-power credit = 0
```

The thresholds `0.6` and `0.15` are declared finite diagnostics.  The
profile family itself is a modeling choice motivated by the literal cutoff
formula; neither choice implies uniformity in `N`.

## Claim ceiling

```text
PROVED_EXACT_FINITE = restricted projection formula and nested-span monotonicity
NUMERICALLY_CERTIFIED_FINITE = two-modulus rank and 70-digit 18-row atlas
NUMERICAL_OBSERVATION = weighted separation and all-positive capture on the registered grid
MODELING_CHOICE = four cutoff profiles and finite residual thresholds
OPEN = growing profile dimension, principal-angle lower bounds, source budget growth
OPEN = arithmetic L2, fixed-power credit, full Gate B
TWIN_PRIME_RESULT = NONE
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = FOUR_LITERAL_CUTOFF_PROFILES_HAVE_RANK_4_AND_CAPTURE_ALL_POSITIVE_TARGETS
STRONGEST_OBSTRUCTION = WEIGHTED_TARGETS_STAY_OUTSIDE_THE_FOUR_PROFILE_IMAGE_ON_17_LARGE_SHELLS
OPEN_THEOREM = GROWING_NATIVE_PROFILE_DIMENSION_OR_PRINCIPAL_ANGLE_BOUND
REUSABLE_STRUCTURE = SOURCE_PROFILE_MATRIX -> CORRELATION IMAGE -> ORTHOGONAL PROJECTION -> TARGET RESIDUAL
ROUND2_CLUE = TEST_NATIVE_PROFILE_PRINCIPAL_ANGLES_AND_MINIMUM_DIMENSION
```

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc297_literal_source_profile_span_certificate.py --write
python -B code/tpc297_literal_source_profile_span_certificate.py --check
python -B experiments/tpc297_independent_checker.py
python -B experiments/tpc297_profile_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
proof package, canonical certificate, independent replay, stress test,
PDF audit, and Bridge-B checker are the available fail-closed validation
path.
