# TPC-315 — Fresh-Source Locked-Weight Holdout

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-315 freezes the three-law menu released by TPC-314 *before* reading any
new target labels, moves the locked literal rational engine to the fresh
source interval `I={641,...,1280}`, and recomputes the Gram minimum and the
all-positive control on all eight `(Q,s)` rows.  The finite class replicates:
all 24 minimum/law cases are strictly below one and all 24 positive-control
cases are strictly above one.  The fine amplitude law is not stable: minimum
orders have three strict types and positive-control orders have two.

This is a same-engine fresh-source holdout, not an externally independent
physical dataset.  It gives no growing theorem, arithmetic `L2` estimate,
fixed-power credit, Route-B Gate-B passage, or twin-prime conclusion.

## What is new relative to TPC-314

* The source panel changes from `I={321,...,640}` to `I={641,...,1280}`.
* The three laws (`1`, `1/(p-1)`, and `log(p)`) and their 120-term logarithm
  enclosure are verified from the TPC-314 certificate before target
  recomputation.
* Every fresh Gram minimum is found by exact rational exhaustive sign-class
  enumeration; the target is not inherited from TPC-312 or TPC-314.
* The 48 resulting weighted cases are enclosed by directed rational intervals
  on a `10^-36` grid and independently replayed.
* The minimum-law order census is `L<C<R` on six rows, `R<C<L` on one, and
  `C<L<R` on one.  The positive-control census is `R<C<L` on six rows and
  `L<R<C` on two.  Here `C=COUNTING`, `R=REDUCED_RESIDUE`, and
  `L=VON_MANGOLDT`.

The order shifts are a concrete obstruction to treating the finite amplitude
as a canonical weighting law, even though the coarse below/above-one class
survives the source change.

## Claim firewall

    PROVED_EXACT_FINITE = physical rational formula; exhaustive finite sign
                          enumeration; weighted Gram identity; positive
                          normalizer; scale invariance; 120-term rational
                          logarithm enclosure; directed interval propagation
    NUMERICALLY_CERTIFIED_FINITE = 8 fresh target rows; 48 law/target cases;
                                   24 below-one minima; 24 above-one controls;
                                   three minimum order types; two positive order
                                   types; independent replay and stress checks
    MODELING_CHOICE = TPC-314 three-law menu; same locked TPC-268 engine;
                      source interval; shells; height; weighted diagonal
                      normalizer; fresh Gram-minimum target rule
    FRESHNESS_SCOPE = fresh source interval under the same literal engine;
                      no external physical data independence
    TARGET_GENERATION = labels are recomputed from the fresh Gram only after
                        the law menu is locked; this still has target/Gram
                        dependence and is not predictive validation
    STRONGEST_POSITIVE = 8/8 fresh rows replicate the finite class under all
                         three declared positive laws
    STRONGEST_OBSTRUCTION = law ordering changes on the fresh panel; no
                            canonical amplitude law is identified
    OPEN = canonical weighting; external physical holdout; uniform growing
           weighted estimate; literal arithmetic L2; fixed-power credit; full
           Gate B; twin-prime endpoint

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  `notes/route_evaluation.md` and the local Bridge-B
checker are fail-closed fallbacks; no official evaluator pass is asserted.

## Reproduction

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc315_fresh_source_locked_weight_holdout.py --write
    python -B code/tpc315_fresh_source_locked_weight_holdout.py --check
    python -B experiments/tpc315_independent_checker.py --check
    python -B experiments/tpc315_holdout_stress.py
    python -B research/tpc-big-road/tpc_bridge_b_tpc315_fresh_source_locked_weight_holdout_checker.py --check

Set `TPC315_WORKERS=1` or `TPC315_CHECK_WORKERS=1` for a serial audit.  The
canonical certificate is
[results/tpc315_certificate.json](results/tpc315_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next route question is whether the literal fresh-panel outputs
can be connected to an arithmetic `L2` estimate without importing a growth
claim.
