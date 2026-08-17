# TPC-207: Critical Moving-Hole BDH Defect

## Result

This project proves an exact moving-hole compiler for translated
reduced-residue Barban--Davenport--Halberstam rows and a deterministic block
bound at the V59 critical scale.

For a row `z` indexed by `Z/qZ`, deleting residue `h` gives

```text
V_h = V_all - q/(q-1) |z_h - mean(z)|^2.
```

The change from hole `0` to hole `h` is a rank-two quadratic form with exact
nonzero spectrum

```text
+/- sqrt(q(q-2))/(q-1).
```

After the mandatory `(q-2)/(q-1)` diagonal subtraction, the same identity
acquires the exact energy correction

```text
R_h - R_0
  = q/(q-1)(|z_0-mean(z)|^2-|z_h-mean(z)|^2)
    + (q-2)/(q-1)(E_h-E_0).
```

With the physical convention `n=s+m`, the moving hole is `h_q=-s mod q`.
The four-packet polarization remains exact with weights `i^j/4`.

For length-`O(H)` bounded-overlap blocks, `2 <= Q <= H`, and `J` effective
blocks, integrating the kernel first and retaining Schwartz block separation
gives

```text
sum_{b,c} |M_bc| << A_beta A_w J (H^2 + H Q + Q^2).
```

Thus at

```text
H=x^(21/32), Q=x^(1/3), J=x/H*x^o(1),
```

the translation defect is `O(x^(53/32+o(1)))`, exactly
`x^(5/3-1/96+o(1))`.  The translation subgate therefore pays the required
strict margin for every fixed `1/400 < delta' < 1/96`.

## Claim firewall

```text
V60_ROUTE_ADVANCE=YES
V60_TRANSLATION_SUBGATE_DELTA=1_OVER_96_PROVED
V60_TRANSLATION_SUBGATE_STRICT_1_OVER_400=PAID
V60_FULL_GATE_B_STRICT_1_OVER_400=UNPAID
V60_ARITHMETIC_ADVANCE=NO
V60_FIXED_ATOM_CREDIT=0
V60_L2=NONE
TPC_207_TRIGGER=true
```

This is `PROVED_STRUCTURAL_L1`.  It is not a full Gate-B estimate, an
arithmetic advance, an `L^2` theorem, fixed-atom credit, or a twin-prime
theorem.  The first remaining fatal gate is the zero-hole, prime-only,
`q`-weighted, kernel-localized, exact-diagonal-subtracted signed four-packet
BDH theorem and its collective reassembly.

## Project layout

```text
README.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/moving_hole.py
experiments/run_certificate.py
experiments/independent_checker.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce the exact certificate

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-207-critical-moving-hole-bdh-defect/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-207-critical-moving-hole-bdh-defect/experiments/independent_checker.py --check
```

To regenerate the canonical JSON:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-207-critical-moving-hole-bdh-defect/experiments/run_certificate.py --write
```

The two checkers use separate implementations.  They verify exact
Gaussian-rational finite fixtures; they are QA artifacts, not proof of the
general theorems.

## Compile the paper

Compile in a scratch directory so LaTeX intermediates do not enter the
repository:

```bash
scratch=$(mktemp -d)
cp papers/tpc-207-critical-moving-hole-bdh-defect/paper/main.tex "$scratch/"
cp papers/tpc-207-critical-moving-hole-bdh-defect/paper/references.bib "$scratch/"
cd "$scratch"
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Author: Liang Wang, Huazhong University of Science and Technology.
