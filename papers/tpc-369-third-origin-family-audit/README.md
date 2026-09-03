# TPC-369 — Third predeclared origin-family audit

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-369 tests a third response-blind origin family after the TPC-367 and
TPC-368 finite long-window obstructions.  The candidate grid is
`1010001+401j`, `0<=j<41`; indices `(0,20,40)` are fixed before any signed
response or geometry score is evaluated, giving origins
`(1010001,1018021,1026041)`.  With counts `512,1024`,
`Q={512,2048,8192}`, exponent one, four fixed laws, and beta `0,2`, the
complete replay has 144 rows.  Beta=2 again has exactly six spectral-cap
violations: count 1024, `Q=2048` or `8192`, all-plus law, at each origin.
There are no beta=2 Schur-cap violations.  The beta=0 control has 18
spectral and 18 Schur violations.  This is a finite third-family audit, not
an asymptotic theorem or a twin-prime result.

## Scientific contribution

TPC-368 showed that TPC-367's six-key beta=2 failure pattern survives a second
predeclared family.  TPC-369 repeats that test on a third deterministic grid
with a new start and step.  The family and all main-panel parameters are
fixed independently of signed response, source data, sign-law scores, and
geometry ranking.  The observed six failure keys agree exactly with the
parent pattern, so the explanation “the obstruction is unique to one origin
family” is not supported by these three finite families.

| beta | count | Q | spectral failures | Schur failures |
|---:|---:|---:|---:|---:|
| 0 | 512 or 1024 | 512, 2048, 8192 | 18 total | 18 total |
| 2 | 512 | 512, 2048, 8192 | 0 | 0 |
| 2 | 1024 | 512 | 0 | 0 |
| 2 | 1024 | 2048, 8192 | 6 total | 0 |

The third-family beta=2 maximum is `0.67410489800609708`, only
`2.9920783610748458e-06` above the TPC-368 maximum
`0.674101905927736`.  Its maximum Schur value is
`0.7000873870755715`, below the working cap `0.83`.  The strongest positive
result is exact finite failure-key replication; the strongest obstruction is
that the same long-window cap failure remains present after a third origin
phase change.

## A small exact-anchor obstruction

The first proposed exact anchor `[1010342,1010355)` has zero geometry rows
for both beta values.  This was detected before any main-panel spectrum was
computed.  The family and main protocol were retained, and a deterministic
response-blind repair rule selected the first consecutive 13-point interval
to its right with positive exact geometry for both betas, namely
`[1010346,1010359)`.  The initial failure, the rule, and the selected anchor
are all recorded in the canonical certificate and independently checked.

## Claim firewall

```text
TPC369_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC369_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC369_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC369_THIRD_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC369_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC369_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC369_INITIAL_ANCHOR_POSITIVITY = REFUTED_SCOPED
TPC369_REPAIRED_ANCHOR_RULE = PROVED_EXACT_FINITE
TPC369_ORIGIN_UNIFORMITY = OPEN
TPC369_WINDOW_UNIFORMITY = OPEN
TPC369_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC369_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC369_GROWING_OPERATOR_BOUND = OPEN
TPC369_SOURCE_UNIFORM_L2 = OPEN
TPC369_ARITHMETIC_ADVANCE = NO
TPC369_FIXED_POWER_CREDIT = 0
TPC369_FULL_GATE_B = OPEN
TPC369_TWIN_PRIME_RESULT = NONE
```

The finite statuses apply only to the declared three origins, two counts,
three shell anchors, exponent one, and four laws.  They do not imply
origin/window uniformity, a growing operator estimate, source-valid
normalization, arithmetic `L2`, shell reassembly, or an asymptotic statement.
The Session-named official Route-A/Route-B evaluator files are absent from
this checkout; local Bridge-B is fail-closed repository evidence only.

## Auditable package

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical certificate is
`results/tpc369_certificate.json`; the manuscript is `paper/paper.pdf`.
The producer uses increasing shell accumulation and the independent checker
uses a separate sieve with descending shell accumulation.  The stress suite
checks protocol, anchor-repair, row, phase, audit, and claim-firewall
mutations.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-369-third-origin-family-audit/code/tpc369_third_origin_family_audit.py --write
python -B papers/tpc-369-third-origin-family-audit/code/tpc369_third_origin_family_audit.py --check
python -O -B papers/tpc-369-third-origin-family-audit/code/tpc369_third_origin_family_audit.py --check
python -B papers/tpc-369-third-origin-family-audit/experiments/tpc369_independent_checker.py --check
python -O -B papers/tpc-369-third-origin-family-audit/experiments/tpc369_independent_checker.py --check
python -B papers/tpc-369-third-origin-family-audit/experiments/tpc369_adversarial_certificate_stress.py --check
python -O -B papers/tpc-369-third-origin-family-audit/experiments/tpc369_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc369_third_origin_family_audit_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc369_third_origin_family_audit_checker.py --check
```

## Route decision and ROUND2_CLUE

The third family reproduces the six-key pattern.  The next minimal finite
attack is therefore a count-2048 window, while a later third-family residue
comparison can test phase dependence without changing beta.  No arithmetic
credit is paid by this result.

```text
ROUND2_CLUE = TEST_COUNT_2048_ORIGIN_PHASE_OR_RESIDUE_PHASE
```
