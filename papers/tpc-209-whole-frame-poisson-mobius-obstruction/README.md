# TPC-209: Whole-Frame Poisson Reindexing and the Möbius-Dilation Obstruction

## Result

TPC-209 tests the TPC-208 proposal to apply Möbius/Poisson to the complete
oriented additive edge frame before any edge or fiber triangle inequality.

For a fixed unit dilation ((D,q)=1), Poisson gives the exact reindexing

```text
(k,r) -> n = q r + k D,
Y_D(k) = sum_(n = kD mod q) Fhat_D(n/q).
```

Thus one dual integer is shared across every edge for that fixed (D).  After
summing divisor components, however, the dual residue packet is acted on by
the multiplicative permutation (U_D:b(k)mapsto b(kD)).  The complete frame
therefore has the exact vector form

```text
Y = sum_D c_D U_D B_D.
```

Multiplicative Fourier diagonalizes the permutations and produces one shared
nonprincipal character coordinate, but with divisor-dependent profiles
(mathcal M B_D(chi)).  For the physical additive vector, a Gauss-sum
calculation returns exactly to the V59 nonprincipal character interface.

The sharp operator identity

```text
|| P sum_D c_D U_D B_D ||_2
  <= (sum_D |c_D|^2)^(1/2) (sum_D ||B_D||_2^2)^(1/2)
```

has equality for aligned profiles.  A (q=5), (D=2,3) fixture has coherent
energy ratio (2), and the quadratic character multiplier equals the full
(ell^1) coefficient mass.  Consequently frame geometry alone cannot
collapse the divisor profiles into one scalar Kloosterman packet or supply a
power saving.

This is a precise `STOP_SCOPED` obstruction, not a global impossibility result.
The actual profile-aware prime-only theorem remains open.

## Claim firewall

```text
TPC209_ROUTE_ADVANCE = YES
TPC209_STRUCTURAL_THRESHOLD_A = PASS
TPC209_SHARED_DUAL_PER_FIXED_DIVISOR = PROVED_EXACT
TPC209_WHOLE_FRAME_VECTOR_COVARIANCE = PROVED_EXACT
TPC209_MULTIPLICATIVE_CHARACTER_DIAGONALIZATION = PROVED_EXACT
TPC209_RETURN_TO_V59_CHARACTER_INTERFACE = PROVED_EXACT
TPC209_SCALAR_COMMON_DUAL_COLLAPSE = REFUTED_SCOPED
TPC209_FRAME_ONLY_POWER_SAVING = STOP_SCOPED
TPC209_SOURCE_VALID_KLOOSTERMAN_ATTACHMENT = OPEN
TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC209_ARITHMETIC_ADVANCE = NO
TPC209_FIXED_ATOM_CREDIT = 0
TPC209_L2 = NONE
TPC209_TPC_TRIGGER = true
```

## Project layout

```text
README.md
PAPER_PLAN.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/whole_frame.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/gaussian_poisson_sanity.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

## Reproduce the exact certificate

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/gaussian_poisson_sanity.py
```

The certificate checks 5 moduli, 1500 dual reindex rows, and 3016 permutation
matrix rows.  These are finite QA checks, not asymptotic evidence.

## Compile the paper

Use an external scratch directory for LaTeX intermediates:

```bash
scratch=$(mktemp -d)
cp papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex "$scratch/"
cp papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/references.bib "$scratch/"
cd "$scratch"
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Author: Liang Wang, Huazhong University of Science and Technology.
