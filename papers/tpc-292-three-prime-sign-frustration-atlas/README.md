# TPC-292 — Three-prime sign frustration in a physical Gram shell

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The exact triangle parity rule says that three pairwise cancellation
preferences can be realized by coefficient signs if and only if the product
of the three nonzero Gram-edge signs is negative.  On the inherited 18-row
literal grid, 5,718 of 5,727 prime triples are therefore sign-frustrated and
only 9 are simultaneously anti-alignable; every tested triple has positive
normalized Gram volume.

## What advances

- proves the exact signed-triangle parity criterion;
- proves the three-vector Schur projection residual and normalized-volume
  identities;
- builds an exact-rational atlas over every three-prime combination in the
  TPC-291 grid;
- turns the pairwise cancellation signal into a finite multi-prime
  compatibility obstruction;
- supplies a reverse-order replay and an independent integer-vector stress
  test covering both parity classes.

## Claim ceiling

```text
PROVED_EXACT_CONDITIONAL = triangle sign parity criterion
PROVED_EXACT_FINITE = three-vector Schur projection identity
PROVED_EXACT_FROM_GRAM_PSD = normalized volume nonnegativity
NUMERICALLY_CERTIFIED_FINITE = 5,727 triples on the declared grid
NUMERICALLY_CERTIFIED_FINITE = 5,718 frustrated and 9 anti-alignable
NUMERICALLY_CERTIFIED_FINITE = residual counts 5,313 / 4,413 / 3,620
MODELING_CHOICE = frozen literal source, rows, shells, and thresholds
OPEN = growing triangle compatibility and source-native arithmetic L2
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The 5,718/5,727 count is a finite obstruction, not an asymptotic theorem.
It does not rule out a special structured multi-prime direction, nor does it
provide the missing arithmetic $L^2$ estimate.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc292_three_prime_sign_frustration_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc292_three_prime_sign_frustration_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc292_three_prime_sign_frustration_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc292_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc292_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc292_frustration_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  Session evaluator
files are absent from this checkout; the local proof, canonical certificate,
reverse-order replay, and stress audit are the fail-closed fallback.
