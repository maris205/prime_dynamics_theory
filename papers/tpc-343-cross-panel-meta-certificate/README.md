# TPC-343 — Cross-panel shared-nuisance meta-certificate

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The row-local nuisance fit survives pooling of the TPC-341 and TPC-342 panels
(residual retention `0.2325429101`), but a single shared nuisance coefficient
vector fails the inherited `<0.30` fit guard under both raw-energy weighting
(`0.3198013104`) and equal-row weighting (`0.3549335801`).

## Why this is a separate paper

TPC-342 independently reproduced the TPC-341 aggregate-versus-holdout split.
TPC-343 asks the next natural question: do the two panels admit one common
nuisance law, or only row-specific fits?  It is a finite model comparison, not
an appended sample count and not an arithmetic theorem.

## Frozen panels and models

```text
TPC341 rows = [48097,48608], [48609,49120], [49217,49728]
TPC342 rows = [40097,40608], [40609,41120], [41121,41632]
scale       = 1024
operator    = all-plus, Q=54, exponent=1, H=66
controls    = nine TPC-338/TPC-340 coordinate controls
categories  = twin, non-twin prime shift, prime-power shift, zero
raw records = 2 x 3 x 9 x 4 = 216
holdouts    = 2 x 3 x 9 = 54
```

The `row-block` model gives each source row its own three nuisance
coefficients.  The `shared` model concatenates corresponding nuisance means
and forces one coefficient vector across all six rows.  The equal-row variant
divides each row's target and nuisance columns by that row's target norm; it is
included as a declared weighting sensitivity, not a canonical normalization.

## Certified finite readout

| quantity | finite result |
|---|---:|
| rows / raw records / nonempty records | 6 / 216 / 171 |
| in-sample row-block residual retention | 0.2325429101 |
| shared raw-energy residual retention | 0.3198013104 |
| shared equal-row residual retention | 0.3549335801 |
| shared cross-panel holdout range | 0.6408306196--0.9090948298 |
| all individual holdout range | 0.4435267486--0.9429165296 |
| fixed-power credit | 0 |

The row-block and shared projections each satisfy the exact finite stacked
Pythagorean identity.  The shared-coefficient obstruction is scoped to this
declared basis and these two panels; it does not refute alternative bases.

## Claim firewall

```text
TPC343_STACKED_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC343_ROW_BLOCK_META = NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION
TPC343_SHARED_COEFFICIENT_RAW = NUMERICAL_OBSERVATION_0.319_TO_0.320
TPC343_SHARED_COEFFICIENT_EQUAL_ROW = NUMERICAL_OBSERVATION_0.354_TO_0.355
TPC343_SHARED_COEFFICIENT_STABILITY = REFUTED_SCOPED
TPC343_HOLDOUT_META = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
TPC343_ARITHMETIC_ADVANCE = NO
TPC343_FIXED_POWER_CREDIT = 0
TPC343_SOURCE_UNIFORM_L2 = OPEN
TPC343_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC343_FULL_GATE_B = OPEN
TPC343_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent in this checkout.  The local
Bridge-B wrapper is fail-closed and is not an official Route-A or Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py --write
python -B papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py --check
python -O -B papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py --check
python -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_independent_checker.py --check
python -O -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_independent_checker.py --check
python -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_meta_stress.py --check
python -O -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_meta_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc343_cross_panel_meta_certificate_checker.py --check
```

The canonical finite certificate is
[results/tpc343_certificate.json](results/tpc343_certificate.json), and the
audited manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next decision

The shared coefficient law is too rigid for this finite two-panel comparison,
while row-local projection remains numerically strong.  The next smallest
non-duplicative question is whether a predeclared alternative nuisance basis or
principal-angle description explains the mismatch.  No arithmetic credit is
carried forward.
