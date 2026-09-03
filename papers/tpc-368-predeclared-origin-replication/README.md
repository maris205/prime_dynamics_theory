# TPC-368 — Second predeclared origin-family replication

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-368 repeats the TPC-367 long-window audit on a distinct, predeclared
origin family.  The grid is `810001+353j`, `0<=j<41`, with indices
`(0,20,40)` fixed before any response or geometry is evaluated, giving
origins `(810001,817061,824121)`.  With counts `512,1024`,
`Q={512,2048,8192}`, exponent one, four fixed laws, and beta `0,2`, the
complete replay has 144 rows.  Beta=2 again has exactly six spectral-cap
violations: the count-1024, high-`Q`, all-plus rows at all three origins.
It has no Schur-cap violations.  The beta=0 control has 18 spectral and 18
Schur violations.  This is a finite replication and obstruction audit, not an
asymptotic theorem or a twin-prime result.

## Scientific contribution

TPC-367 showed that a geometry-unselected long-window panel could break the
working beta=2 spectral cap.  TPC-368 tests whether that pattern was tied to
the first origin family.  The second grid and its three indices are frozen in
the protocol; no signed response, source vector, law score, or geometry rank
is consulted.  The beta=2 rule and the count-1024/exponent-one stress point
are held fixed, while beta=0 remains a literal control.

| beta | count | Q | spectral failures | Schur failures |
|---:|---:|---:|---:|---:|
| 0 | 512 or 1024 | 512, 2048, 8192 | 18 total | 18 total |
| 2 | 512 | 512, 2048, 8192 | 0 | 0 |
| 2 | 1024 | 512 | 0 | 0 |
| 2 | 1024 | 2048, 8192 | 6 total | 0 |

The six beta=2 failures are exactly the same finite key pattern as in
TPC-367: all-plus law, exponent one, count 1024, and `Q` equal to 2048 or
8192, once at each of the three predeclared origins.  The replicated beta=2
maximum is `0.674101905927736`, compared with the parent maximum
`0.67410738070824539`; the difference is a finite comparison only.  The
largest beta=2 Schur value is `0.70009251108512549`, below the working Schur
cap `0.83`.  The positive result is replication of the localized pattern;
the obstruction is that the pattern still prevents a finite long-window cap
transfer.

## Claim firewall

```text
TPC368_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC368_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC368_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC368_SECOND_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC368_BETA2_LONG_WINDOW_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC368_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC368_ORIGIN_UNIFORMITY = OPEN
TPC368_WINDOW_UNIFORMITY = OPEN
TPC368_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC368_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC368_GROWING_OPERATOR_BOUND = OPEN
TPC368_SOURCE_UNIFORM_L2 = OPEN
TPC368_ARITHMETIC_ADVANCE = NO
TPC368_FIXED_POWER_CREDIT = 0
TPC368_FULL_GATE_B = OPEN
TPC368_TWIN_PRIME_RESULT = NONE
```

`NUMERICALLY_CERTIFIED_FINITE_SCOPED` refers only to the declared 144-row
panel.  It does not imply uniformity in origins, windows, shell scale, or a
limit.  The Session-named official Route-A/Route-B evaluator files are absent
from this checkout; the local Bridge-B checker is fail-closed repository
evidence, not an official evaluator pass.

## Auditable package

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical certificate is
`results/tpc368_certificate.json`; the manuscript is `paper/paper.pdf`.
The producer accumulates the prime shell in increasing order and evaluates
all four laws from one component calculation per setting.  The independent
checker has its own sieve and descends through the shell before rebuilding
all 144 rows.  The stress checker rejects 29 protocol, data, audit, and
claim-firewall mutations.  A small rational anchor checks symmetry and
positive geometry exactly.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-368-predeclared-origin-replication/code/tpc368_predeclared_origin_replication.py --write
python -B papers/tpc-368-predeclared-origin-replication/code/tpc368_predeclared_origin_replication.py --check
python -O -B papers/tpc-368-predeclared-origin-replication/code/tpc368_predeclared_origin_replication.py --check
python -B papers/tpc-368-predeclared-origin-replication/experiments/tpc368_independent_checker.py --check
python -O -B papers/tpc-368-predeclared-origin-replication/experiments/tpc368_independent_checker.py --check
python -B papers/tpc-368-predeclared-origin-replication/experiments/tpc368_adversarial_certificate_stress.py --check
python -O -B papers/tpc-368-predeclared-origin-replication/experiments/tpc368_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc368_predeclared_origin_replication_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc368_predeclared_origin_replication_checker.py --check
```

## Route decision and ROUND2_CLUE

The second predeclared origin family reproduces the finite failure pattern,
so the next minimal attack is a third response-blind family or a count-2048
window.  The former tests whether the pattern survives another residue phase;
the latter tests whether the observed window boundary moves.  Neither is an
asymptotic claim.

```text
ROUND2_CLUE = TEST_BETA2_THIRD_ORIGIN_FAMILY_OR_COUNT_2048
```
