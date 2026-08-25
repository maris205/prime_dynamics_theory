# TPC-243: Hard-Window Near-Isometry and Signed Bilinear Transfer

This project proves a direct two-sided frame estimate for exponential synthesis
on a hard interval. If `F` is a finite `delta`-separated subset of the circle,
`I` consists of `N` consecutive integers, and

```text
Tz(n) = sum_(alpha in F) z_alpha e(n alpha),
R_delta = delta^(-1) H_floor(1/(2 delta)),
epsilon = R_delta/N,
```

then

```text
[1-epsilon]_+ ||z||_2^2
  <= N^(-1)||Tz||_2^2
  <= (1+epsilon)||z||_2^2,

|N^(-1)<Tz,Tw>-<z,w>|
  <= epsilon ||z||_2 ||w||_2.
```

The proof uses the literal rectangular Gram matrix. Its diagonal is `N`, and
two-sided circular packing plus the geometric-sum bound gives an absolute
off-diagonal row sum at most `R_delta`. Hermitian Schur/Gershgorin then yields
both the near-isometry and the signed bilinear estimate.

For distinct reduced rational frequencies of height at most `U`, one may take
`delta=U^(-2)`. On the V59 interval with
`U=x^(133/400)` this gives

```text
epsilon_U
  = (133/100+o(1)) x^(-67/200) log x
  = x^(-67/200+o(1)).
```

The coefficient `133/100` is recorded exactly. Relative to TPC-238, the lower
baseline improves from a triangular-minorant `1/2-O(U^4/N^2)` statement to a
hard-rectangular `1-O(U^2 log U/N)` statement, and the same operator estimate
also transfers signed bilinear forms. TPC-217 already contains the standard
upper large-sieve scale, so no novelty is claimed for that upper scale.

TPC-242 transports with a fixed orientation: for
`X=N^(-1/2)Tz` and `Y=N^(-1/2)Tw`, its selected mode is
`F_1=<Y,X>=N^(-1)<Tw,Tz>`, which approximates `<w,z>`. This is a
structural interface, not arithmetic cancellation or a literal physical
attachment theorem.

## Artifacts

- `PROOF_PACKAGE.md`: complete proof, including empty, singleton, and
  antipodal cases.
- `DERIVATION_PACKAGE.md`: invariant-object derivation and the exact V59
  exponent ledger.
- `results/tpc243_certificate.json`: canonical exact certificate.
- `code/tpc243_hard_window_certificate.py`: mutually exclusive producer and
  checker.
- `experiments/tpc243_independent_checker.py`: separately implemented strict
  checker binding the complete nested schema.
- `experiments/tpc243_hard_window_stress.py`: finite exact stress census.
- `paper/paper.pdf`: compiled manuscript.

## Reproduction

Run from this project directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc243_hard_window_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc243_hard_window_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O code/tpc243_hard_window_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc243_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc243_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc243_hard_window_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc243_hard_window_stress.py --check
```

The finite certificate and stress census are classified
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`. The theorem is proved symbolically.

## Maximum status

`PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER`.

`ARITHMETIC_ADVANCE = NO`. Coefficient norm bounds, literal top-prime
attachment, a signed `C_h` theorem, arithmetic `L2`, fixed-atom credit, the
strict `1/400` endpoint, full Gate B, and every twin-prime conclusion remain
open.
