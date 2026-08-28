# TPC-288 — Growing-shell Gram obstruction

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On a 34-row finite growth/control grid reaching 17 prime components, every
output Gram matrix is certified full rank (hence positive definite), six
selected aggregate physical matrices are full active rank, and 13 rows have
scalar retention upper bound below `1/10` while their exact vector output
energy ratio is greater than `1`.

## What advances

- lifts TPC-287's scalar prime-shell cancellation to the literal output-vector
  and Gram level;
- proves the finite operator, output, attachment, Gram-PSD, and energy
  identities exactly;
- separates shell growth from source-control variation with an eight-point
  path and an 18-row height/cutoff grid;
- supplies modular full-rank witnesses for every output Gram and six aggregate
  physical active matrices;
- closes a tempting but invalid bridge: small scalar attachment does not,
  on these literal rows, imply output-energy decay.

## Claim ceiling

```text
PROVED_EXACT = finite operator/output/attachment/Gram identities
NUMERICALLY_CERTIFIED_FINITE = 34/34 full-rank positive-definite output Grams
NUMERICALLY_CERTIFIED_FINITE = 6/6 selected aggregate physical active ranks
NUMERICALLY_CERTIFIED_FINITE = 13 scalar-energy mismatch rows
MODELING_CHOICE = finite growth path and control grid
OPEN = uniform growing-shell/source-control theorem
OPEN = literal arithmetic L2 and fixed-power credit
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The mismatch is a finite obstruction to one scalar-to-energy promotion.  It is
not an asymptotic counterexample to every collective prime-shell estimate.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc288_growing_shell_gram_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc288_growing_shell_gram_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc288_growing_shell_gram_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc288_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc288_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc288_gram_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The wider Session
evaluator files are absent from this checkout; `notes/route_evaluation.md`
records the fail-closed local Route-B fallback.
