# TPC-255: Exact Adjoint Diagonal Return and Hard-Boundary Decomposition for the Literal V59 Haar Lane

Status:

```text
PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER
```

TPC-255 pushes the ordered rank-midpoint Haar vector through the literal V59
operator adjoint.  For every prime `q` in the frozen shell and every input
`t` with `q` not dividing `t`, the complete-lattice unit-centered row vanishes
by the V43 band-limited Poisson theorem when `H>2Q`.  Deleting the physical
diagonal then returns a nonzero local term; the hard endpoints of `I_x` and
the jump between the two rank children produce two further exact lanes.

The resulting literal scalar is

```text
<z_mid,A_x beta>
 = -B_Q<z_mid,beta> + input-unit correction
   - hard-window leakage + child-jump leakage.
```

All outer `q` weights, both unit masks, the deleted diagonal, kernel
conjugations, and the ordered-rank definition for real `x` are retained.  The
output mask is essential: its raw-centered and `q|u` pieces have opposite
Poisson zero modes and cancel only together.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/code/tpc255_adjoint_diagonal_boundary_certificate.py --check
python -O -B papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/code/tpc255_adjoint_diagonal_boundary_certificate.py --check
python -B papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/experiments/tpc255_independent_checker.py --check
python -O -B papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/experiments/tpc255_independent_checker.py --check
python -B papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/experiments/tpc255_adjoint_diagonal_boundary_stress.py --check
python -O -B papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/experiments/tpc255_adjoint_diagonal_boundary_stress.py --check
```

The certificate uses exact Gaussian-rational kernels and finite lattices.  It
reproduces algebra, masks, signs, and adjoint orientation only.  It is not
numerical evidence for the asymptotic Poisson attachment or for an arithmetic
saving.

## Build

From `paper/`:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

## Claim boundary

`ROUTE_ADVANCE=YES_EXACT_LITERAL_STRUCTURE` and
`LITERAL_ARITHMETIC_STRUCTURE_ADVANCE=YES`, because the actual V59
coefficient and operator now appear in one exact normal form.
`ARITHMETIC_ADVANCE=NO`: no lane is estimated, no sign or nonzero value is
proved, `FIXED_ATOM_CREDIT=0`, `L2=NONE`, `FULL_GATE_B=OPEN`, the strict
`1/400` budget is unpaid, and no twin-prime conclusion follows.
