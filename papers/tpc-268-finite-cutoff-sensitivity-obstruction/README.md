# TPC-268 — Finite Cutoff-Sensitivity Obstruction for the V59 Residual Phase

Author: Liang Wang

Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

~~~text
NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION
~~~

TPC-267 observed |C_perp|/R<1/4 on twelve finite rows with the z=2
comparison. TPC-268 performs the next hostile test while preserving the
physical prime shell, masks, deleted diagonal, beta source, kernel operator,
and rank-three projection.

The matched central rows are especially diagnostic:

~~~text
(N,H,Q,s,z)=(64,15,4,1,2): rho <= 0.2320126753
(N,H,Q,s,z)=(64,15,4,1,3): rho >= 0.2735126949
~~~

The first is a certified contraction and the second is a certified
obstruction. The obstruction persists at H=13 and H=17, and the
z=5,s=1 row reaches rho <= 0.3851247936 as a finite stress point. Across
the 16 rows there are 10 contractions and 6 obstructions.

This is a scoped finite refutation of a universal quarter-sector claim over
the tested parameter family. It is not an asymptotic counterexample, gives
zero fixed-power credit, and does not advance arithmetic L2 or full Gate B.

## Reproduce

~~~bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py --check
python -O -B papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py --check
python -B papers/tpc-268-finite-cutoff-sensitivity-obstruction/experiments/tpc268_independent_checker.py --check
python -O -B papers/tpc-268-finite-cutoff-sensitivity-obstruction/experiments/tpc268_independent_checker.py --check
python -B papers/tpc-268-finite-cutoff-sensitivity-obstruction/experiments/tpc268_adversarial_stress.py --check
python -O -B papers/tpc-268-finite-cutoff-sensitivity-obstruction/experiments/tpc268_adversarial_stress.py --check
~~~

The required paper layout is present, including paper/paper.pdf.
