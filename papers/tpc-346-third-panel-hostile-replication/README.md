# TPC-346 — Third-panel hostile replication and finite route freeze

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

A genuinely fresh third panel does not support a weighting-stable
panel-adaptive nuisance law. Its own pooled residual retention is
`0.3159173453264` under raw weighting and `0.3294074740697` under equal-row
weighting. The three-panel adaptive model crosses the raw threshold only
narrowly (`0.2999630725662`) and returns to `0.3222362713305` after
equal-row normalization.

## Why this is a separate paper

TPC-343 and TPC-344 showed that a shared nuisance coefficient can fail and
that a panel-contrast reparameterization can produce a narrow raw-weighted
repair. TPC-345 removed the coordinate choice and found a weighting-sensitive
Grassmann geometry. TPC-346 asks the next minimal question: does the
panel-specific relaxation survive a new panel that was not used to define the
parent geometry?

The fresh panel uses the disjoint origins `[44097,44609,45217]`. It is
cutoff-safe, and its operator, scale, controls, and source categories are
unchanged from the parent protocol.

## Frozen protocol

```text
parent panels = TPC341: [48097,48609,49217]
                TPC342: [40097,40609,41121]
fresh panel  = TPC346: [44097,44609,45217]
scale        = 1024
rows         = 9 blocks of length 512
operator     = all-plus, Q=54, exponent=1, H=66
controls     = 9 fixed bijective coordinate controls
records      = 324 raw records, 261 nonempty
weightings   = raw and equal-row
```

The shared model uses one nuisance coefficient vector across all three panels.
The adaptive model uses one vector per panel. A third diagnostic trains on
two panels and predicts the held-out panel. The hostile control-LOO diagnostic
uses each omitted control's twin output as target and the mean of the other
eight controls as nuisance input on the fresh panel.

## Certified finite readout

| quantity | raw | equal-row |
|---|---:|---:|
| fresh-panel own-fit retention | 0.3159173453 | 0.3294074741 |
| shared three-panel retention | 0.3419067441 | 0.3564123507 |
| panel-adaptive three-panel retention | 0.2999630726 | 0.3222362713 |
| minimum directed prediction retention | 0.3543123948 | 0.3416324137 |
| minimum leave-one-panel-out retention | 0.3712128254 | 0.3783318336 |
| minimum fresh control-LOO retention | 0.7435404822 | 0.7574228742 |

All six directed single-panel predictions, all three leave-one-panel-out
predictions, and all nine fresh control-LOO projections exceed `0.30` for
each declared weighting. The raw adaptive crossing is therefore a finite
model observation, not a transferable law.

Pairwise principal cosines for the fresh panel are also retained in the
certificate. For example, TPC-341 versus TPC-346 has raw cosines
`0.9968572419,0.1620463946,0.03856023954`, while equal-row weighting gives
`0.9350969661,0.2484090871,0.02402578867`. This continues the parent
weighting-sensitivity signal without asserting a universal angle theorem.

## Claim firewall

```text
TPC346_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION
TPC346_NESTED_MODEL_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC346_FRESH_PANEL_OWN_FIT = REFUTED_SCOPED
TPC346_SHARED_THREE_PANEL = REFUTED_SCOPED
TPC346_PANEL_ADAPTIVE_RAW = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS
TPC346_PANEL_ADAPTIVE_EQUAL_ROW = REFUTED_SCOPED
TPC346_PANEL_ADAPTIVE_WEIGHTING_STABILITY = REFUTED_SCOPED
TPC346_THIRD_PANEL_TRANSFER = REFUTED_SCOPED
TPC346_ARITHMETIC_ADVANCE = NO
TPC346_FIXED_POWER_CREDIT = 0
TPC346_SOURCE_UNIFORM_L2 = OPEN
TPC346_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC346_FULL_GATE_B = OPEN
TPC346_TWIN_PRIME_RESULT = NONE
TPC346_ROUND2_CLUE = FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2
```

The finite freeze applies only to this declared panel-adaptive branch. It is
not a universal impossibility result for every future nuisance model, and it
does not pay any asymptotic arithmetic gate.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-346-third-panel-hostile-replication/code/tpc346_third_panel_hostile_replication.py --write
python -B papers/tpc-346-third-panel-hostile-replication/code/tpc346_third_panel_hostile_replication.py --check
python -O -B papers/tpc-346-third-panel-hostile-replication/code/tpc346_third_panel_hostile_replication.py --check
python -B papers/tpc-346-third-panel-hostile-replication/experiments/tpc346_independent_checker.py
python -O -B papers/tpc-346-third-panel-hostile-replication/experiments/tpc346_independent_checker.py
python -B papers/tpc-346-third-panel-hostile-replication/experiments/tpc346_hostile_stress.py
python -O -B papers/tpc-346-third-panel-hostile-replication/experiments/tpc346_hostile_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc346_third_panel_hostile_replication_checker.py --check
```

The canonical certificate is
[results/tpc346_certificate.json](results/tpc346_certificate.json), and the
audited manuscript is [paper/paper.pdf](paper/paper.pdf).
