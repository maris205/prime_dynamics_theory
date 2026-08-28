# TPC-291 — Signed Schur cancellation atlas

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For all 1,380 cross-prime pairs in the TPC-289 grid, the exact two-vector
Schur residual is nonnegative; 1,074, 852, and 477 pairs have residual at
most `1/2`, `1/4`, and `1/10`, respectively.  The 1,377 positive pairs require
opposite-sign cancellation, while the three negative pairs permit same-sign
sparse cancellation.

## What advances

- proves the exact projection/Schur identity `residual=1-Gamma`;
- derives the signed two-vector Rayleigh minimum `1-sqrt(Gamma)`;
- turns the sign of the Gram cross term into an explicit coefficient-sign
  cost;
- builds a finite coherence-to-cancellation atlas rather than treating
  coherence as merely an energy obstruction;
- identifies the globally most coherent tested pair and the three exceptional
  same-sign cancellation pairs.

## Claim ceiling

```text
PROVED_EXACT = two-prime Schur projection identity and signed Rayleigh minimum
NUMERICALLY_CERTIFIED_FINITE = 1,380 pair atlas with nonnegative residuals
NUMERICALLY_CERTIFIED_FINITE = residual counts 1,074 / 852 / 477
NUMERICALLY_CERTIFIED_FINITE = coherence counts 1,189 at 9/25 and 852 at 3/4
NUMERICALLY_CERTIFIED_FINITE = 1,377 opposite-sign and 3 same-sign pair directions
MODELING_CHOICE = finite TPC-289 row grid and thresholds
OPEN = multi-prime signed reassembly, growing theorem, and arithmetic L2
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The atlas quantifies pairwise cancellation geometry; it is not a full-shell
or asymptotic cancellation result.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc291_signed_schur_cancellation_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc291_signed_schur_cancellation_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc291_signed_schur_cancellation_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc291_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc291_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc291_schur_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  Session evaluator
files are absent from this checkout; the local proof, certificate, replay,
and stress audit are the fail-closed fallback.
