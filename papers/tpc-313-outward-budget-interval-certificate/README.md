# TPC-313 — Outward-Rounded Profile-Budget Interval Certificate

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-313 closes the next finite interface on the TPC-312 panel.  For each of
the eight source--shell rows, it finds the least literal profile prefix for
which the TPC-312 Gram-minimizing sign target has normalized residual at most
`1/2`.  On that same prefix, an exact rational ridge witness gives a feasible
primal upper bound and a weak-dual lower bound.  Both are propagated through
a `10^-36` decimal grid with floor/ceiling endpoint rounding.

The weighted (Gram-minimum) target has a dual budget ratio strictly above
`5e-5` in all 8 rows, while the all-positive control has a feasible primal
budget ratio strictly below `1e-5` in all 8 rows.  These are finite,
independently replayed certificates on the new source interval
`I=(320,640]`; they do not imply a growing profile-budget theorem or a
twin-prime result.

## Claim firewall

```text
PROVED_EXACT_FINITE = profile-prefix least-feasibility scan; rational ridge
                      linear systems; primal feasibility; weak-dual lower
                      bound; directed decimal-grid interval propagation
NUMERICALLY_CERTIFIED_FINITE = 8 common prefixes and 16 budget cases; every
                               weighted lower and positive upper threshold
                               is separated by an outward interval
STRONGEST_POSITIVE = weighted dual ratio > 5e-5 and positive primal ratio
                     < 1e-5 on the same prefix in all 8 rows
OBSTRUCTION = the target label is selected from the same physical Gram, and
              the finite budget separation has no external weight law
FRESHNESS_SCOPE = new source-shell panel inherited from TPC-312, not external
                  physical data
OPEN = externally justified weighting; genuinely fresh physical holdout;
       uniform growing-shell budget; arithmetic L2; fixed-power credit;
       full Gate B; twin-prime conclusion
```

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  `notes/route_evaluation.md` and the local Bridge-B
checker are therefore fail-closed fallbacks; no official evaluator pass is
asserted.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc313_outward_budget_interval_certificate.py --write
python -B code/tpc313_outward_budget_interval_certificate.py --check
python -B experiments/tpc313_independent_checker.py --check
python -B experiments/tpc313_exact_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc313_outward_budget_interval_certificate_checker.py --check
```

The canonical certificate is
[results/tpc313_certificate.json](results/tpc313_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable paper
project.  The next route question is no longer whether finite profile
budgets can be enclosed: it is whether an externally defensible weighting
law survives a genuinely fresh physical holdout.
