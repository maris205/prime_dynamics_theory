# TPC-285 — Prime-shell residue factorization and rank obstruction

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For each prime shell block, the centered residue matrix factors exactly as
`B_q=R_q(I-11^T/(q-1))R_q^T` and therefore has rank at most `q-2`.  However,
after deleting the diagonal—the physical operator convention—the active block
has full rank whenever every nonzero residue class occurs.  All 20 registered
prime/exponent rows also retain full active rank after the rational kernel
Schur product, certified by exact modular witnesses.

## What advances

- isolates the exact `q-2` dimensional centered residue-mode structure;
- proves a general deleted-diagonal full-rank theorem by decomposing into
  within-class zero-sum and block-constant subspaces;
- identifies the precise structural reason that the attractive low-rank
  residue shortcut does not transfer to the physical off-diagonal matrix;
- independently certifies all 20 registered prime-shell rows, including the
  kernel-weighted matrices, over the prime field `F_1000000007`;
- turns the eight sign flips of TPC-284 into a concrete operator warning:
  source controls act through a high-rank physical block, not only through
  `q-2` centered residue modes.

## Claim ceiling

```text
PROVED_EXACT = centered residue factorization and rank <= q-2
PROVED_EXACT = deleted-diagonal block has full active rank when all classes occur
NUMERICALLY_CERTIFIED_FINITE = 20/20 kernel-Schur blocks have full active rational rank
OPEN = useful cancellation or spectral bound for the full signed shell sum
OPEN = literal arithmetic L2 estimate
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc285_prime_shell_residue_rank_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc285_prime_shell_residue_rank_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc285_prime_shell_residue_rank_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc285_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc285_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc285_rank_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The modular rank
certificate is an exact finite witness: because every rational denominator is
invertible modulo the declared prime, full rank after reduction implies full
rank over the rationals.  It does not by itself provide an operator-norm gain.
