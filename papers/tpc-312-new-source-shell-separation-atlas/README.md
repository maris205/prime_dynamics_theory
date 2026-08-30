# TPC-312 — New Source-Shell Gram and Sign-Separation Atlas

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-312 moves the finite Bridge-B audit to eight previously unused physical
rows: the literal source interval `I=(320,640]`, `H=66`, shell anchors
`Q={24,36,54,80}`, and exponents `s={1,2}`.  Exact rational Gram construction
and exhaustive global-sign enumeration give a unique minimum modulo global
sign and a unique all-positive maximum in every row.  The minimum ratio is
strictly below `1` and the positive ratio strictly above `1` in all 8 rows;
along each four-anchor Q spine the minimum ratio decreases while the positive
ratio increases, with exponent two strengthening both inequalities.

This is a new source-shell panel inside the same locked physical engine.  It
is not an external independent sample, a growing-shell theorem, an arithmetic
`L2` estimate, or a twin-prime result.

## Claim firewall

```text
PROVED_EXACT_FINITE = literal Gram identity; PSD identity; modular full-rank
                      implication; global-sign reduction; Gray enumeration;
                      exact finite Q/exponent order comparisons
NUMERICALLY_REPRODUCED_FINITE = 8 new rows; 84 shell targets; 37,440 sign
                                 classes; independent exact replay
STRONGEST_POSITIVE = 8/8 strict weighted-vs-positive separation and 8/8
                     modular full-rank rows on the new source panel
OBSTRUCTION = the finite separation does not select a canonical weighting or
              produce a uniform growing-shell bound
FRESHNESS_SCOPE = new source indices and new parameter rows in the same engine
EXTERNAL_INDEPENDENCE = NONE
TARGET_LEAKAGE = source-first Gram-dependent sign labels, inherited in spirit
OPEN = outward-rounded profile budgets; externally justified weighting; fresh
       external physical holdout; uniform asymptotic budget; arithmetic L2;
       fixed-power credit; full Gate B; twin-prime conclusion
```

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  `notes/route_evaluation.md` is therefore a local,
fail-closed assessment; no official evaluator pass is asserted.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc312_new_source_shell_separation.py --check
python -B experiments/tpc312_independent_checker.py --check
python -B experiments/tpc312_exact_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc312_new_source_shell_separation_checker.py --check
```

Run the same commands with `python -O -B` where applicable.  The canonical
certificate is [results/tpc312_certificate.json](results/tpc312_certificate.json),
and the compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Files

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next minimal question is whether the profile-budget layer can be
certified with outward-rounded rational intervals on these same new rows.
