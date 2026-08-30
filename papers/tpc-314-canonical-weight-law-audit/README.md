# TPC-314 — Externally Motivated Weight-Law Audit

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-314 freezes the eight-row TPC-312 source--shell panel and audits three
declared positive weighting laws: counting weight 'w_p=1', reduced-residue
weight 'w_p=1/(p-1)', and prime von-Mangoldt weight 'w_p=log(p)'.  The first
two laws are rational.  The logarithm is enclosed by a rational range-reduced
atanh series with a positive tail bound, and all quadratic-form operations
are rounded outward on a '10^-36' decimal grid.

All 24 Gram-minimum cases lie strictly below one and all 24 all-positive
control cases lie strictly above one.  This is a finite robustness result for
the separation class, not a canonical-weight theorem.  The amplitude is
weight-law dependent: the minimum-law ordering has one finite
'counting < log(p) < 1/(p-1)' crossover among eight rows, while the positive
control has four distinct strict ordering types.

## Claim firewall

    PROVED_EXACT_FINITE = weighted Gram identity; positive diagonal normalizer;
                          scale invariance; rational atanh enclosure for log(p);
                          sound directed interval propagation
    NUMERICALLY_CERTIFIED_FINITE = 48 target/law cases; 24 minimum cases below
                                   one; 24 positive controls above one; all
                                   interval endpoints independently replayed
    STRONGEST_POSITIVE = all three declared positive laws preserve the finite
                         minimum-versus-positive classification on 8 rows
    STRONGEST_OBSTRUCTION = the weight law changes amplitudes and ordering; one
                            minimum crossover and four positive-order types
    MODELING_CHOICE = the three-law menu, trace-like weighted normalization,
                      source panel, and TPC-312 Gram-minimum target
    FRESHNESS_SCOPE = same locked physical engine and same TPC-312 source panel;
                      no external physical holdout
    TARGET_LEAKAGE = minimum labels are inherited from the physical Gram under
                     audit, so this is not predictive validation
    OPEN = canonical weighting selection; fresh source holdout; uniform growing
           weighted theorem; arithmetic L2; fixed-power credit; full Gate B;
           twin-prime conclusion

The Session-named propose.md and Route-A/Route-B evaluator files are absent
from this checkout.  notes/route_evaluation.md and the local Bridge-B checker
are therefore fail-closed fallbacks; no official evaluator pass is asserted.

## Reproduction

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc314_canonical_weight_law_audit.py --write
    python -B code/tpc314_canonical_weight_law_audit.py --check
    python -B experiments/tpc314_independent_checker.py --check
    python -B experiments/tpc314_exact_stress.py
    python -B research/tpc-big-road/tpc_bridge_b_tpc314_canonical_weight_law_audit_checker.py --check

Run the producer and replay with 'python -O -B' as an additional optimized
check.  The canonical certificate is
[results/tpc314_certificate.json](results/tpc314_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

PAPER_PLAN.md, DERIVATION_PACKAGE.md, PROOF_PACKAGE.md, notes/, code/,
experiments/, results/, and paper/ form the auditable project package.  The
next route question is whether this fixed weighting menu can be replayed on a
genuinely fresh source interval with weights locked before the target is
recomputed.
