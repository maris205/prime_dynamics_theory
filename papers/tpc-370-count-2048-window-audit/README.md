# TPC-370 — Count-2048 finite-window audit

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-370 takes the next predeclared finite-window step after the TPC-369
third-origin audit. It keeps the same response-blind grid and the three
origins `(1010001,1018021,1026041)`, fixes count `2048`,
`Q={512,2048,8192}`, exponent one, four fixed sign laws, and beta `0,2`, and
replays all 72 rows. Beta=2 has six spectral-cap violations: at each origin,
`Q=2048` and `8192`, under the all-plus law. It has no Schur-cap violation.
The beta=0 control has nine spectral and nine Schur violations. The six-key
origin/Q/law signature agrees with the TPC-369 parent signature after the
count coordinate is removed, but the maximum beta=2 value rises to
`0.71099989528234753`. This is a finite audit, not an asymptotic theorem or
a twin-prime result.

## Scientific contribution

The experiment isolates the next window scale without selecting origins or
parameters from the observed response. The parent TPC-369 failure keys were
declared as a comparison target, while the count-2048 failure keys were
recorded from the replay itself. The result separates two facts that must
not be conflated:

1. the high-Q/all-plus failure *support* persists across the count change and
   all three inherited origins; and
2. the normalized maximum is not numerically stable across the two finite
   counts, increasing by `0.036894997276250452` relative to TPC-369.

| beta | count | Q | spectral failures | Schur failures |
|---:|---:|---:|---:|---:|
| 0 | 2048 | 512, 2048, 8192 | 9 total | 9 total |
| 2 | 2048 | 512 | 0 | 0 |
| 2 | 2048 | 2048 | 3 total | 0 |
| 2 | 2048 | 8192 | 3 total | 0 |

The beta=2 spectral maximum is `0.71099989528234753`, while the maximum
beta=2 Schur value is `0.72908109638522522`, below the working Schur cap
`0.83`. The parent maximum was `0.67410489800609708`; the difference is a
finite comparison only. The strongest positive result is exact finite
support replication of the parent six-key signature. The strongest
obstruction is that the same support is accompanied by a materially
different maximum at the larger count, so a constant-level extrapolation is
unsupported.

## Inherited exact anchor

TPC-370 does not reselect or repair the proof anchor. It inherits the exact
unsigned anchor `[1010346,1010359)` at `Q=4`, exponent one, and shell `{5,7}`
from TPC-369. The certificate records the inheritance declaration and
recomputes the exact rational symmetry and positivity witness. No main-panel
response is used to choose this anchor.

## Claim firewall

```text
TPC370_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC370_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC370_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC370_COUNT_2048_WINDOW = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC370_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC370_BETA2_PARENT_SIGNATURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC370_ORIGIN_UNIFORMITY = OPEN
TPC370_WINDOW_UNIFORMITY = OPEN
TPC370_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC370_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC370_GROWING_OPERATOR_BOUND = OPEN
TPC370_SOURCE_UNIFORM_L2 = OPEN
TPC370_ARITHMETIC_ADVANCE = NO
TPC370_FIXED_POWER_CREDIT = 0
TPC370_FULL_GATE_B = OPEN
TPC370_TWIN_PRIME_RESULT = NONE
```

All finite statuses apply only to the declared three origins, count 2048,
three shell anchors, exponent one, four laws, and two beta values. They do
not imply origin/window uniformity, a growing operator estimate, source-valid
normalization, arithmetic `L2`, prime-shell reassembly, an asymptotic repair,
or any twin-prime conclusion. The Session-named official Route-A/Route-B
evaluator files are absent from this checkout; local Bridge-B is fail-closed
repository evidence only.

## Auditable package

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`. The canonical certificate is
`results/tpc370_certificate.json`; the manuscript is `paper/paper.pdf`.
The producer accumulates shells in increasing order. The independent checker
uses a separate sieve and descending shell accumulation, verifies the parent
certificate signature, and recomputes all 72 rows. The stress suite mutates
protocol, count, row, signature, anchor-inheritance, firewall, and clue
fields.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-370-count-2048-window-audit/code/tpc370_count_2048_window_audit.py --write
python -B papers/tpc-370-count-2048-window-audit/code/tpc370_count_2048_window_audit.py --check
python -O -B papers/tpc-370-count-2048-window-audit/code/tpc370_count_2048_window_audit.py --check
python -B papers/tpc-370-count-2048-window-audit/experiments/tpc370_independent_checker.py --check
python -O -B papers/tpc-370-count-2048-window-audit/experiments/tpc370_independent_checker.py --check
python -B papers/tpc-370-count-2048-window-audit/experiments/tpc370_adversarial_certificate_stress.py --check
python -O -B papers/tpc-370-count-2048-window-audit/experiments/tpc370_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc370_count_2048_window_audit_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc370_count_2048_window_audit_checker.py --check
```

The local Bridge-B checker reruns the producer, independent replay, and
stress suite in normal and optimized Python modes, requires empty stderr, and
requires byte-identical stdout. Its result is not an official Route-A or
Route-B verdict.

## Route decision and ROUND2_CLUE

The parent six-key support survives the count-2048 replay, but the magnitude
does not remain stable. The next minimal question is therefore to localize
the count-2048 phase (origin, residue, and high-Q component) under a new
predeclared partition, rather than assign any asymptotic meaning to the
maximum. Arithmetic advance remains `NO` and fixed-power credit remains
zero.

```text
ROUND2_CLUE = TEST_COUNT_2048_PHASE_LOCALIZATION
```
