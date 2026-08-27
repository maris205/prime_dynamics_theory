# TPC-278 — Cross-scale signed-gain stability and a shell/clock counterexample

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On the same literal source and four-packet projection used by TPC-277, changing
only the declared prime-shell endpoint `Q` or the clock `H` flips the sign of
the net packet cross term in four of twelve exact finite rows.  For example,
at `N=192,s=2`, the natural `Q=6` row has `D/G≈1.006248`, while `Q=7` has
`D/G≈0.866928`.  Thus the finite statement `D/G>=1` is not stable under this
declared interface perturbation.

This is a finite stability obstruction, not an asymptotic counterexample: the
source-level Q/H schedule needed by the twin-prime route remains open.

## Claim ceiling

```text
NUMERICALLY_CERTIFIED_FINITE = 12 exact source rows and 4 sign flips
REFUTED_SCOPED = finite r>=1 stability under declared Q/H perturbations
OPEN = source-level uniform shell/clock stability and coherence theorem
FIXED_POWER_CREDIT = 0
ARITHMETIC_ADVANCE = NO
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc278_cross_scale_gain_stability_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc278_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc278_stability_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  TPC-277 is locked by
code and result hashes; no synthetic packet or floating-point classification is
used.
