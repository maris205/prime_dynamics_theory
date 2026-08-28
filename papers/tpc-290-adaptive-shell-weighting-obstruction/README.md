# TPC-290 — Adaptive shell weighting obstruction

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For the TPC-289 literal output Gram, nonnegative full-support reweighting is
still amplified on all 54 tested policy rows, while the only subunit
nonnegative witnesses are three equal two-prime supports arising from the
single early sign-flip row.

## What advances

- introduces the weighted physical Rayleigh quotient and its exact Gram
  expansion;
- proves that a nonnegative weight rule cannot create decay inside an
  all-positive Gram block;
- proves the effective-support version of the TPC-289 coherence lower bound;
- separates diffuse full-shell adaptation from sparse sign-flip escape;
- certifies uniform, inverse-diagonal, and linear-taper policies over the
  complete 18-row grid, plus all pair and leave-one-out probes.

## Claim ceiling

```text
PROVED_EXACT = weighted Gram identity and nonnegative no-decay lemma
PROVED_EXACT_CONDITIONAL = effective-support accumulation bound
NUMERICALLY_CERTIFIED_FINITE = 54/54 full-support policy rows amplified
NUMERICALLY_CERTIFIED_FINITE = 3 equal-pair subunit witnesses in one row
NUMERICALLY_CERTIFIED_FINITE = 18/18 leave-one-out minima amplified
REFUTED_FINITE = universal nonnegative no-decay claim on the declared grid
MODELING_CHOICE = three adaptive policies and finite support probes
OPEN = growing diffuse weighted theorem and source-native arithmetic L2
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite sparse witnesses do not imply decay for the full prime shell; they
identify the exact concentration mechanism that can exploit a sign flip.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc290_adaptive_shell_weighting_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc290_adaptive_shell_weighting_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc290_adaptive_shell_weighting_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc290_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc290_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc290_weighting_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  Session evaluator
files are absent from this checkout; the local proof, certificate, replay,
and stress audit are the fail-closed fallback.
