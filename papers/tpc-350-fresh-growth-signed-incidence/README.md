# TPC-350 — Fresh-growth and shell-scale replication of signed incidence witnesses

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-350 moves the TPC-349 zero-sum prime-incidence witness to three fresh
origins, four interval lengths, and a shell ladder reaching `Q=256`.  The exact
Gram expansion and induced-norm lower witness remain valid.  All `192/192`
locked rows have positive response; the response/defect ratio is
`0.0657381187306--0.8797933448`, `70/192` rows beat the coordinate baseline,
and `91/192` reach one half of the defect norm.  Only `24/48` length series are
nondecreasing, while every `Q=256` row lies below one half.  Thus fresh
replication succeeds, but a universal quarter-floor is `REFUTED_SCOPED`.

The word “growth” is deliberately finite: no asymptotic theorem is claimed.
The claim firewall leaves source-uniform arithmetic `L2`, a uniform masked
operator bound, fixed-power credit, and the twin-prime endpoint open.

## Package

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project.
The canonical certificate is
`results/tpc350_certificate.json`; the compiled manuscript is
`paper/paper.pdf`.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-350-fresh-growth-signed-incidence/code/tpc350_fresh_growth_signed_incidence.py --write
python -B papers/tpc-350-fresh-growth-signed-incidence/code/tpc350_fresh_growth_signed_incidence.py --check
python -O -B papers/tpc-350-fresh-growth-signed-incidence/code/tpc350_fresh_growth_signed_incidence.py --check
python -B papers/tpc-350-fresh-growth-signed-incidence/experiments/tpc350_independent_checker.py --check
python -O -B papers/tpc-350-fresh-growth-signed-incidence/experiments/tpc350_independent_checker.py --check
python -B papers/tpc-350-fresh-growth-signed-incidence/experiments/tpc350_growth_stress.py
python -O -B papers/tpc-350-fresh-growth-signed-incidence/experiments/tpc350_growth_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc350_fresh_growth_signed_incidence_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc350_fresh_growth_signed_incidence_checker.py --check
```

The official Session-named evaluator files are absent, so the local Bridge-B
assessment is fail-closed and is not an official Route-A/Route-B pass.

## Claim readout

```text
TPC350_FRESH_GROWTH_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
TPC350_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
TPC350_SIGNED_TO_DEFECT_FLOOR = NUMERICALLY_CERTIFIED_FINITE_0.0657381187306
TPC350_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_70_OF_192
TPC350_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_91_OF_192
TPC350_NONDECREASING_GROWTH_SERIES = NUMERICALLY_CERTIFIED_FINITE_24_OF_48
TPC350_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
TPC350_ARITHMETIC_ADVANCE = NO
TPC350_FIXED_POWER_CREDIT = 0
TPC350_FULL_GATE_B = OPEN
TPC350_TWIN_PRIME_RESULT = NONE
```
