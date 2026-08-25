# Computational Protocol

## Exact certificate

The producer uses `fractions.Fraction` for every real and imaginary
component. Complex scalars are encoded as pairs of canonical rational
strings. For odd rank, it never approximates `rho`; it records
`rho^2=ell*r/N`, the rational step vector `h`, and every projector entry as
`rho^2*h_i*h_j`.

The released JSON is one-line, key-sorted, ASCII, strict JSON with a terminal
newline. `NaN`, infinities, duplicate keys, noncanonical fractions, and
noncanonical whitespace are rejected. The SHA-256 payload digest is computed
over the same compact canonical encoding.

The independent checker imports no producer code. It independently checks:

- exact integer identity with `type(value) is int` for all integer/count fields;
- rejection of bool-as-int count, rank, coordinate, and crosswalk mutations;
- ordered coordinates, `N=#I_x`, `ell`, `r`, `h`, and `rho^2`;
- the exact rational coarse, midpoint, and contrast projector matrices;
- partial sums, both longitudinal formulas, first-slot conjugation, the
  opposite transverse update, and within-child covariance;
- exact integer `floor(3x/4)` crosswalk rows covering all classes modulo four;
- the literal TPC-247 `beta` and sampled kernel compiler with outer prime
  weight, masks, deleted diagonal, orientation, kernel, and centered bracket;
- `<h,A beta>=<A^*h,beta>`, hence the common-`rho` safe adjoint identity;
- non-self-adjoint sample detection without a claim about the literal operator;
- nonliteral constant-annihilation and `w=z,g=+-z` controls;
- 59 typed, semantic, source, firewall, digest, duplicate-key,
  nonfinite-token, and canonical-byte mutations.

## Deterministic stress

The stress suite checks 192 seeded exact Gaussian-rational families. It uses
96 integer clocks and 96 nonintegral rational clocks. The integer clocks give
24 cases in each residue class modulo four. Every family checks the ordered
rank construction, exact rational projector update and idempotence,
coarse/contrast orthogonality, partial-sum formulas, conjugate-first
covariance transfer, opposite `Q` update, within-child covariance, arbitrary
matrix adjoint identity, two constant-zero controls, and two sign controls.
No floating-point arithmetic or optimization-sensitive `assert` statement is
used.

## Release commands

Run from the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/code/tpc253_midpoint_contrast_certificate.py --check
python -O -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/code/tpc253_midpoint_contrast_certificate.py --check
python -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_independent_checker.py --check
python -O -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_independent_checker.py --check
python -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_midpoint_contrast_stress.py --check
python -O -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_midpoint_contrast_stress.py --check
```

Normal and optimized output must be byte-identical for each script.

Compile from `paper/` with the required explicit passes:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

Audit the complete `paper.log` for errors, warnings, undefined references or
citations, and bad boxes. Use `pdfinfo`, `pdffonts`, and `pdftotext` for page,
font, and text checks. Render every page with `pdftoppm -png -r 160` into one
unique `/tmp/tpc253-render-*` directory and retain it for visual QA.

All executable evidence is finite structural reproduction, not actual V59
numerical, asymptotic, arithmetic, L2, Gate-B, or twin-prime evidence.
