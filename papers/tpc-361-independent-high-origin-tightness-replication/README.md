# TPC-361 — Independent high-origin tightness replication

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a new geometry-selected high-origin panel, the complete finite replay has
288 operator rows and 180 recorded spectra.  The normalized Schur maximum is
`0.80830232610282304`, the normalized spectral maximum is
`0.62690716242733457`, and the largest spectral/Schur ratio is
`0.77585950058997`.

## Scientific contribution

TPC-361 is an independent replication of the TPC-360 tightness ledger on a
fresh panel.  The candidate origins are exactly `310001+233j`,
`0<=j<=50`.  At pilot count 256, only the six unsigned geometry spreads
`(Q,s) in {24,54,80} x {1,2}` are used.  Candidates are sorted by decreasing
spread (then origin) and retained greedily with separation 1536.  This
response-blind rule selects `(313030,311166,321651)` before any signed matrix
or spectrum is evaluated.

The replay uses counts `256,512,1024,2048`, the three shell anchors, two
kernel exponents, and four fixed sign laws.  Schur and Frobenius envelopes are
recorded for all 288 rows.  True spectra are recorded for all four laws at
counts 256 and 512, and for all-plus at counts 1024 and 2048.  All 180
recorded spectra are below `0.64`; the four-law short-panel comparisons have
winner census all-plus `30`, mod-4 `6`, alternating `0`, half-split `0`.

The strongest obstruction is unchanged: the all-plus normalized ladder has
`12` increases, `36` decreases, and `6` flats across its 54 adjacent count
transitions.  Finite replication therefore does not supply a monotone decay
law or a growing operator estimate.

## Claim firewall

```text
TPC361_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC361_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC361_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC361_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC361_TIGHTNESS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC361_LAW_UNIFORM_SHORT_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC361_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC361_GROWING_OPERATOR_BOUND = OPEN
TPC361_SOURCE_UNIFORM_L2 = OPEN
TPC361_ARITHMETIC_ADVANCE = NO
TPC361_FIXED_POWER_CREDIT = 0
TPC361_FULL_GATE_B = OPEN
TPC361_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed finite evidence and
is not an official evaluator pass.  No source response is used, no arithmetic
reassembly is attempted, and no fixed-power credit is claimed.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-361-independent-high-origin-tightness-replication/code/tpc361_independent_high_origin_tightness_replication.py --write
python -B papers/tpc-361-independent-high-origin-tightness-replication/code/tpc361_independent_high_origin_tightness_replication.py --check
python -O -B papers/tpc-361-independent-high-origin-tightness-replication/code/tpc361_independent_high_origin_tightness_replication.py --check
python -B papers/tpc-361-independent-high-origin-tightness-replication/experiments/tpc361_independent_checker.py --check
python -O -B papers/tpc-361-independent-high-origin-tightness-replication/experiments/tpc361_independent_checker.py --check
python -B papers/tpc-361-independent-high-origin-tightness-replication/experiments/tpc361_adversarial_certificate_stress.py --check
python -O -B papers/tpc-361-independent-high-origin-tightness-replication/experiments/tpc361_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc361_independent_high_origin_tightness_replication_checker.py --check
```

The canonical certificate is `results/tpc361_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.  The protocol and route decision are in
`experiments/protocol.md` and `notes/route_evaluation.md`.

## Round-2 clue

`TEST_SCALE_LADDER_AND_SIGN_LAW_INTERACTION_ON_A_NEW_PANEL`.
