# TPC-250: Coherence-Controlled Gram Quadratic Bounds and Sharpness

TPC-250 converts the exact shared-lane Gram quadratic from TPC-249 into a
finite structural envelope controlled by weighted \(\ell^1\) mass and active
coherence.  For

```text
g = sum_i lambda_i v_i,
a_i = |lambda_i| ||v_i||,
D = sum_i a_i^2,
L = sum_i a_i,
```

the proved estimate is

```text
| ||g||^2 - D | <= mu (L^2-D).
```

The definition of `mu` is total: it is `0` when at most one index is active,
and otherwise it is the maximum normalized off-diagonal Gram entry over the
active set.  The ratio `kappa=L^2/D` is formed only when `D>0`.

The coefficient in the upper estimate and the coefficient in the signed
lower estimate are universally sharp.  The nonnegative floor is necessary.
These are universal sharpness statements, not an assertion that every
arbitrary parameter tuple has a saturating Gram family.

## Reproduce

Run from this project directory:

```bash
python -B code/tpc250_coherence_certificate.py
python -B code/tpc250_coherence_certificate.py --check
python -B experiments/tpc250_independent_checker.py --check
python -O -B experiments/tpc250_independent_checker.py --check
python -B experiments/tpc250_coherence_stress.py --check
python -O -B experiments/tpc250_coherence_stress.py --check
cd paper && latexmk -pdf -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

The certificate is exact rational arithmetic.  The stress run is a
`NUMERICAL_FINITE_ILLUSTRATION_ONLY` only in the logical sense that finitely
many examples cannot prove an asymptotic statement; its individual arithmetic
comparisons are exact over `fractions.Fraction`.

## Claim boundary

```text
TPC250_ACTUAL_V59_COHERENCE_ASYMPTOTIC=OPEN
TPC250_ARITHMETIC_ADVANCE=NO
TPC250_FIXED_ATOM_CREDIT=0
TPC250_L2=NONE
TPC250_FULL_GATE_B=OPEN
TPC250_FULL_GATE_B_STRICT_1_OVER_400=UNPAID_GLOBAL
TPC250_TWIN_PRIME_RESULT=NONE
```

Maximum supported claim:

```text
PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS
```
