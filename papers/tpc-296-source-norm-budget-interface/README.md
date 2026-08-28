# TPC-296 — Least-norm source budget and native-ray obstruction

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

For the TPC-295 finite source-correlation map, the exact least source cost is

```text
S(b) = min_{A^T h=b} ||h||_2^2 = b^T G^(-1)b,
```

and it obeys the exact tradeoff
`S(b) (b^T G b) >= (b^T b)^2`.  A 70-digit independent replay finds that all
18 TPC-294 weighted minimizers are cheap in the unrestricted source space
under the declared diagnostic budget
`S(b)/||beta||_2^2 < 1e-3`, but all 18 remain at normalized RMS distance at
least `0.9` from the enlarged one-dimensional ray `span{A^T beta}`.  Thus the
finite obstruction is not raw unrestricted source norm; it is the dimension
and geometry of the admissible native source family.

## What advances

- proves the exact least-norm witness identity and an iff source-budget
  criterion;
- proves the exact source-cost/physical-energy tradeoff by Cauchy--Schwarz;
- completes a high-precision 18-row cost, conditioning, and one-ray profile
  atlas with an independent source-first replay;
- shows that unrestricted finite source cost is below the declared `1e-3`
  relative budget on 18/18 weighted-minimum rows;
- shows that the explicitly declared one-ray proxy misses all 18 weighted
  targets by normalized RMS at least `0.9`;
- moves the next theorem from ambient image existence to a
  profile-restricted dimension/budget theorem.

## Finite headline

```text
rows = 18
shell edges = 1,380
working precision = 70 decimal digits
weighted-minimum cost / ||beta||^2 < 1e-3 = 18 / 18
max-cut cost / ||beta||^2 < 1e-3 = 18 / 18
plus cost / ||beta||^2 < 1e-3 = 18 / 18
weighted-minimum span{beta} image RMS >= 0.9 = 18 / 18
max-cut span{beta} image RMS >= 0.9 = 18 / 18
plus span{beta} image RMS <= 0.4 = 18 / 18
maximum weighted-minimum budget ratio = 0.000584056544646...
minimum weighted-minimum profile-ray RMS = 0.912134981827...
maximum finite Gram condition number = 2497.29180077...
source-energy tradeoff failures = 0 / 54 targets
```

The threshold `1e-3` and the one-ray family `span{frozen_beta}` are explicit
finite diagnostic choices.  They are not arithmetic Gate-B hypotheses and
receive no exponent credit.

## Claim ceiling

```text
PROVED_EXACT_FINITE = least-norm identity, budget iff criterion, energy tradeoff
NUMERICALLY_CERTIFIED_FINITE = 70-digit 18-row cost/profile atlas with independent replay
NUMERICAL_OBSERVATION = all 18 weighted targets below the declared 1e-3 unrestricted budget
NUMERICAL_OBSERVATION = all 18 weighted targets at profile-ray RMS at least 0.9
MODELING_CHOICE = diagnostic budget 1e-3 and profile ray span{frozen_beta}
OPEN = actual native Mobius/comparison profile image and dimension
OPEN = growing-shell least-norm and condition-number control
OPEN = arithmetic L2, fixed-power credit, full Gate B
TWIN_PRIME_RESULT = NONE
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = EXACT_LEAST_NORM_BUDGET_COMPILER_PLUS_18_ROW_HIGH_PRECISION_COST_ATLAS
STRONGEST_OBSTRUCTION = CHEAP_UNRESTRICTED_WITNESSES_ARE_FAR_FROM_THE_FROZEN_NATIVE_RAY
OPEN_THEOREM = GROWING_RESTRICTED_PROFILE_IMAGE_WITH_A_PAYABLE_SOURCE_NORM_BUDGET
REUSABLE_STRUCTURE = GRAM_INVERSE -> LEAST_NORM_SOURCE_COST -> ENERGY_TRADEOFF -> PROFILE_PROJECTION
ROUND2_CLUE = TEST_RESTRICTED_PROFILE_DIMENSION_AND_GROWING_SOURCE_BUDGET
```

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc296_source_norm_budget_certificate.py --write
python -B code/tpc296_source_norm_budget_certificate.py --check
python -B experiments/tpc296_independent_checker.py
python -B experiments/tpc296_budget_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
Route-A/Route-B evaluator files are absent from this checkout; the local
proof package, canonical certificate, independent replay, stress test, and
Bridge-B checker are the available fail-closed validation path.
