# TPC-284 — A finite control atlas for literal source attachment

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

Starting from the twelve TPC-283 baseline rows, six explicitly declared local
schedule controls (`H±2`, `z±1`, and `Q±1`) give a 72-row finite atlas.  Every
control row has a sign-separated literal source attachment: 60 are negative,
12 are positive, and none crosses zero.  Eight rows flip sign relative to the
baseline, so finite non-vanishing does not imply even finite sign stability.

## What advances

- replaces the unrestricted Hilbert-space zeroing direction of TPC-283 by a
  reproducible finite family of small, named schedule controls;
- replays the frozen literal prime-shell operator on all 72 controlled rows
  with outward interval arithmetic;
- certifies the exact sign census and the eight baseline sign flips;
- records a weakest controlled normalized attachment of about
  `1.4118e-5` and a largest upper endpoint of about `0.1539`;
- sharpens the next theorem request: first define and constrain the literal
  control class, then prove sign/magnitude stability on a growing schedule.

The controls are **declared finite schedule controls**, not a theorem that all
physically admissible source perturbations have been exhausted.  The result is
therefore an atlas and a scoped obstruction, not an asymptotic stability claim.

## Claim ceiling

```text
NUMERICALLY_CERTIFIED_FINITE = 72 declared control rows, all sign-separated
NUMERICALLY_CERTIFIED_FINITE = 60 negative, 12 positive, 0 zero-crossing
NUMERICALLY_CERTIFIED_FINITE = 8 sign flips against the TPC-283 baseline
OPEN = asymptotic control stability on a growing schedule
OPEN = characterization of the full admissible literal-source class
OPEN = literal arithmetic L2 estimate
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc284_admissible_source_control_atlas_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc284_admissible_source_control_atlas_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc284_admissible_source_control_atlas_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc284_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc284_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc284_atlas_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The certificate binds
the TPC-283 result and the frozen TPC-268 source engine by normalized SHA-256
hashes.  All decimal interval endpoints in the JSON release are parsed as
exact rational numbers by the checkers.
