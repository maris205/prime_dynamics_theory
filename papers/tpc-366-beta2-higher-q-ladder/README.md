# TPC-366 — Fixed beta=2 on a higher-Q scale ladder

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-366 freezes the beta=2 rule from TPC-364/365 and carries it to a new
geometry-selected panel and the five-anchor ladder
`Q={512,1024,2048,4096,8192}`.  The complete finite replay has 480 rows.
Beta=2 has zero spectral and Schur working-cap violations in all 240 of its
rows; its maximum normalized spectrum is `0.62448287758976528` and its
maximum normalized Schur value is `0.65368278287004711`.  The beta=0 control
has 60 spectral and 60 Schur violations in 240 rows.

This is a finite higher-Q scale audit.  It does not establish a uniform
operator bound, source-valid normalization, arithmetic `L2` estimate, or a
twin-prime result.

## Scientific contribution

TPC-365 showed that beta=2 transfers from a reused panel to a fresh
response-blind panel through `Q=512`.  TPC-366 keeps beta fixed and attacks
scale rather than refitting the weight.  On the 41 candidates
`620001+307j`, `0<=j<41`, a 256-point pilot uses only unsigned beta=2
weighted geometry.  The descending-spread, origin-tie-break, greedy rule
with minimum separation `2048` selects
`(623071,631360,629211)`.  The selection is complete before signed matrices
are evaluated.

The selected panel is then evaluated at counts `256,512`, exponents `1,2`,
all four fixed sign laws, and every declared Q anchor from 512 through 8192,
for both beta=0 and the frozen beta=2 rule.  Beta=2 remains below the
inherited finite working caps (`0.64` spectral and `0.83` Schur), while the
literal beta=0 control continues to fail at every Q anchor.  This extends a
finite structural signal, not an asymptotic theorem: the maximum beta=2
spectrum is slightly larger than the TPC-365 value by
`0.0081509924949620949`, and no monotonicity is asserted.

The result survives an independently written reverse-shell replay and a
23-mutation certificate stress test.  The origin selection is response-blind
but geometry-selected, so it is not a random independent sample or a
uniform-in-origin assertion.

## Claim firewall

```text
TPC366_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC366_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC366_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_480_ROWS
TPC366_HIGHER_Q_LADDER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC366_BETA2_HIGHER_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC366_BETA2_SCALE_UNIFORMITY = OPEN
TPC366_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC366_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC366_GROWING_OPERATOR_BOUND = OPEN
TPC366_SOURCE_UNIFORM_L2 = OPEN
TPC366_ARITHMETIC_ADVANCE = NO
TPC366_FIXED_POWER_CREDIT = 0
TPC366_FULL_GATE_B = OPEN
TPC366_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed finite evidence
only, not an official evaluator pass.

## Package

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable package.
The canonical certificate is
`results/tpc366_certificate.json`; the compiled manuscript is
`paper/paper.pdf`.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-366-beta2-higher-q-ladder/code/tpc366_beta2_higher_q_ladder.py --write
python -B papers/tpc-366-beta2-higher-q-ladder/code/tpc366_beta2_higher_q_ladder.py --check
python -O -B papers/tpc-366-beta2-higher-q-ladder/code/tpc366_beta2_higher_q_ladder.py --check
python -B papers/tpc-366-beta2-higher-q-ladder/experiments/tpc366_independent_checker.py --check
python -O -B papers/tpc-366-beta2-higher-q-ladder/experiments/tpc366_independent_checker.py --check
python -B papers/tpc-366-beta2-higher-q-ladder/experiments/tpc366_adversarial_certificate_stress.py --check
python -O -B papers/tpc-366-beta2-higher-q-ladder/experiments/tpc366_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc366_beta2_higher_q_ladder_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc366_beta2_higher_q_ladder_checker.py --check
```

## Round-2 clue

`TEST_BETA2_ON_LONGER_WINDOWS_AND_UNSELECTED_ORIGINS`.
