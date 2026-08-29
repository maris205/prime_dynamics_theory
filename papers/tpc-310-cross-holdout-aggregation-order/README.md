# TPC-310 — Cross-Holdout Aggregation Order and Profile Robustness

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-310 takes the locked TPC-309 finite profile/completion atlas and enumerates
all 49 nonempty profile-subset/radius-subset selectors.  Across 147 aggregate
rows, pooled MSE classifies the full selector as `RIGHT`, equal-case arithmetic
ratio as `LEFT`, and geometric ratio as `RIGHT`.  The first two intervals are
far from both strict thresholds, so aggregation order/weighting—not numerical
threshold noise—blocks an aggregation-independent preference claim.

This is a finite obstruction and an analytic weighting identity.  It is not a
causal, asymptotic, arithmetic, or twin-prime theorem.

## Claim firewall

```text
PROVED_EXACT_FINITE = 49-selector construction; independent pooled extrema;
                      positive arithmetic/geometric interval maps;
                      ratio-of-sums weighted-mean identity
NUMERICALLY_REPRODUCED_FINITE = 162 locked parent observations -> 147 aggregate
                                 observations over all nonempty selectors
FULL_SELECTOR = pooled [0.2423655855...,0.3112477031...] RIGHT;
                balanced [5.2417686281...,14.4871333703...] LEFT;
                geometric [0.1993188213...,0.8609189558...] RIGHT
CLASS_CENSUS = pooled R42/L1/U6; balanced R1/L32/U16; geometric R26/L0/U23
REFUTED_FINITE = universal claim that the declared aggregation maps share one
                 strict class on this finite atlas
MODELING_CHOICE = pooled MSE, equal-case arithmetic ratio, geometric ratio;
                  strict-majority budget anchor; all nonempty subset selectors
INHERITED_LEAKAGE = TPC-302 physical-Gram-dependent target labels
OPEN = canonical weighting law; directed rounding; causal identification;
       profile-independent growing preference; uniform budget; arithmetic L2;
       fixed-power credit; full Gate B; twin-prime conclusion
```

The finite `REFUTED` label is scoped to the declared universal aggregation
claim.  It does not rule out a future weighting theorem justified independently
of the observed atlas.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc310_cross_holdout_aggregation_order.py --check
python -B experiments/tpc310_independent_checker.py --check
python -B experiments/tpc310_aggregation_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc310_cross_holdout_aggregation_order_checker.py --check
```

The canonical certificate is
`results/tpc310_certificate.json`; the manuscript is
[paper/paper.pdf](paper/paper.pdf).  The Session-named evaluator files are
absent from this checkout, so no official evaluator pass is asserted.  The
local fail-closed evidence is the locked TPC-309 parent, independent replay,
exact rational stress suite, theorem ledger, claim firewall, PDF audit, and
Bridge-B checker.
