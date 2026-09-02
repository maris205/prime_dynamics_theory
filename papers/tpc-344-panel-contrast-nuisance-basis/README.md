# TPC-344 — Panel-contrast nuisance basis audit

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

Adding one predeclared panel-contrast direction for each nuisance category
reduces the pooled raw-energy residual retention to `0.29621892474890171`
(a scoped pass of the inherited `<0.30` guard), but the same six-column basis
retains `0.31865066996095742` under equal-row weighting.  The repair is
therefore finite and weighting-sensitive, not a stable canonical nuisance law.

## Why this is a separate paper

TPC-343 showed that one nuisance coefficient vector across the two locked
panels is too rigid.  TPC-344 tests the smallest structured relaxation that
still shares coefficients within each panel: for each nuisance category `j`,
the base column `b_j` is supplemented by a signed panel contrast `d_j`.
This is a new basis/model comparison, not an extra row appended to TPC-343.
The exact reparameterization is

```text
u_1j = (b_j + d_j)/2,    u_2j = (b_j - d_j)/2,
```

so the six declared columns are equivalent to one shared nuisance vector per
panel.  The equivalence is finite linear algebra; it does not identify a
canonical arithmetic decomposition.

## Frozen protocol

```text
TPC341 rows = [48097,48608], [48609,49120], [49217,49728]
TPC342 rows = [40097,40608], [40609,41120], [41121,41632]
scale       = 1024
operator    = all-plus, Q=54, exponent=1, H=66
controls    = nine TPC-338/TPC-340 coordinate controls
categories  = twin, non-twin prime shift, prime-power shift, zero
raw records = 2 x 3 x 9 x 4 = 216 (171 nonempty)
holdouts    = 2 x 3 x 9 = 18 contrast projections
crossfits   = 2 directions x 2 weightings = 4
```

The panel signs are `(+1,-1)`.  All shifted source arguments remain below the
locked cutoff `50000`.  The TPC-342 prime-power nuisance column is zero on its
three rows, so the six declared columns have observed rank `5`; this
degeneracy is recorded rather than silently removed.

## Certified finite readout

| quantity | finite result |
|---|---:|
| rows / raw records / nonempty records | 6 / 216 / 171 |
| row-block raw residual retention | 0.2325429101 |
| one-vector shared raw retention | 0.3198013104 |
| panel-contrast raw retention | 0.2962189247 |
| panel-contrast equal-row retention | 0.3186506700 |
| panel-contrast positive rank / condition (raw) | 5 / 141.9850 |
| contrast holdout retention range (both weights) | 0.6372238668--0.9128543547 |
| cross-fit prediction retention range | 0.3759486734--0.6342934197 |
| fixed-power credit | 0 |

The raw pass has margin about `0.0037810753` below `0.30`.  Equal-row
normalization reverses the decision.  Cross-fit means are trained on all three
rows of one panel and predicted on all three rows of the other; every direction
has prediction residual retention above `0.30`, so no low-residual cross-panel
transfer is certified.

## Claim firewall

```text
TPC344_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT
TPC344_CONTRAST_SPAN_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC344_RAW_CONTRAST_GUARD = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS
TPC344_EQUAL_ROW_CONTRAST_GUARD = REFUTED_SCOPED
TPC344_WEIGHTING_STABILITY = REFUTED_SCOPED
TPC344_CROSSFIT_TRANSFER = REFUTED_SCOPED
TPC344_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_18_RECORDS
TPC344_ARITHMETIC_ADVANCE = NO
TPC344_FIXED_POWER_CREDIT = 0
TPC344_SOURCE_UNIFORM_L2 = OPEN
TPC344_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC344_FULL_GATE_B = OPEN
TPC344_TWIN_PRIME_RESULT = NONE
```

The official Session Route-A/Route-B evaluator files are absent in this
checkout.  The local Bridge-B wrapper is fail-closed and is not an official
evaluator pass.  No finite certificate here pays an asymptotic arithmetic
loss, a strict `1/400` endpoint, or a twin-prime conclusion.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-344-panel-contrast-nuisance-basis/code/tpc344_panel_contrast_nuisance_basis.py --write
python -B papers/tpc-344-panel-contrast-nuisance-basis/code/tpc344_panel_contrast_nuisance_basis.py --check
python -O -B papers/tpc-344-panel-contrast-nuisance-basis/code/tpc344_panel_contrast_nuisance_basis.py --check
python -B papers/tpc-344-panel-contrast-nuisance-basis/experiments/tpc344_independent_checker.py --check
python -O -B papers/tpc-344-panel-contrast-nuisance-basis/experiments/tpc344_independent_checker.py --check
python -B papers/tpc-344-panel-contrast-nuisance-basis/experiments/tpc344_meta_stress.py --check
python -O -B papers/tpc-344-panel-contrast-nuisance-basis/experiments/tpc344_meta_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc344_panel_contrast_nuisance_basis_checker.py --check
```

The canonical certificate is
[results/tpc344_certificate.json](results/tpc344_certificate.json), and the
audited manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next decision

The panel-contrast basis repairs the raw pooled guard only marginally and loses
that repair under a declared weighting sensitivity; cross-fit transfer also
fails the low-residual criterion.  The next natural question is geometric:
measure principal angles between the two panel nuisance subspaces and test
whether the apparent repair is a stable subspace relation or merely a
coordinate/weighting artifact.  This is the TPC-345 trigger.
