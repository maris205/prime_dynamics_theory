# TPC-311 — Declared Stratification and Tolerance-Slice Holdout Replication

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-311 fixes a two-stage design rule on the locked TPC-309 atlas: pool the
three profile ladders inside each `(transition, exponent, tau, radius)` cell,
then give each design cell equal arithmetic weight.  On the primary native
endpoint `r=0`, calibration `tau={0.25,0.5}` is
`[4.0615814676...,4.0617439341...]` (`LEFT_COMPLETION_LOWER`), while the
held-out parameter slice `tau={0.75}` is
`[0.6818442327...,0.6818715070...]` (`RIGHT_COMPLETION_LOWER`).  The strict
class therefore reverses.  With radii `0,1,2` included, calibration remains
LEFT but confirmation becomes unresolved.

This is a finite parameter-slice obstruction, not fresh physical-data
replication, an externally timestamped preregistration, an asymptotic result,
or a twin-prime theorem.

## Claim firewall

```text
PROVED_EXACT_FINITE = 54-cell factorial protocol; profile-pooled extrema;
                      equal-stratum interval map; tau partition
NUMERICALLY_REPRODUCED_FINITE = 54 strata; 6 primary/control blocks;
                                 22 sensitivity blocks
PRIMARY_OBSTRUCTION = native calibration LEFT vs confirmation RIGHT
STRESS_OBSTRUCTION = all-radius confirmation UNRESOLVED
ROBUSTNESS_OBSTRUCTION = BASE omission changes native calibration to RIGHT;
                         exponent 1 is LEFT while exponent 2 is RIGHT
REFUTED_FINITE = strict replication of the declared native class on this atlas
MODELING_CHOICE = profile pooling, equal design-cell weights, native r=0,
                  tau=.75 confirmation
REGISTRATION_LIMIT = child declaration is not externally timestamped
HOLDOUT_LIMIT = same locked parent atlas, not a fresh physical sample
INHERITED_LEAKAGE = TPC-302 physical-Gram-dependent target labels
OPEN = directed rounding; external weight law; fresh physical holdout; causal
       identification; uniform asymptotic budget; arithmetic L2; fixed-power
       credit; full Gate B; twin-prime conclusion
```

The Session-named evaluator files are absent from this checkout.  No official
Route-A or Route-B pass is asserted; `notes/route_evaluation.md` records the
local fail-closed fallback.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc311_stratified_tau_holdout_replication.py --check
python -B experiments/tpc311_independent_checker.py --check
python -B experiments/tpc311_stratification_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc311_stratified_tau_holdout_replication_checker.py --check
```

Run each command once with `python -O -B` as well.  The canonical certificate
is [results/tpc311_certificate.json](results/tpc311_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Files

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` contain the full audit
package.  The immediate next theorem is not another weighting variant: it is
an externally justified weighting law tested on a genuinely fresh physical
holdout.
