# TPC-242: Phase-Fourier Collision Separation

This directory contains the manuscript and exact certificate for **Phase-Fourier
Separation of Unsigned Collision Energy from the Signed Four-Packet Channel**.
The proved result is structural: for

```text
E_j = ||X+i^jY||^2,
F_k = (1/4) sum_(j=0)^3 i^(kj) E_j,
```

in a complex Hilbert space whose inner product is conjugate-linear in the first
slot, the complete spectrum is

```text
F_0=||X||^2+||Y||^2,  F_1=<Y,X>,  F_2=0,  F_3=<X,Y>.
```

At fixed `S=F_0`, the exact feasible set of `F_1` is the closed disk
`|F_1|<=S/2`, including `S=0`, and the phase defect has the exact decomposition

```text
S^2-4|F_1|^2
 = (||X||^2-||Y||^2)^2
   +4(||X||^2||Y||^2-|<Y,X>|^2).
```

The source-type conclusion is equally important: TPC-241 proves an unsigned
standalone common-profile norm floor, but supplies no identification with the
literal V59 packet marginals or phase-labelled energies. It therefore gives
zero direct quantitative implication for `F_1`. This paper does **not** claim
that the physical top-prime mode vanishes.

## Exact artifacts

- `PROOF_PACKAGE.md`: self-contained proofs and typed corollary.
- `DERIVATION_PACKAGE.md`: convention-sensitive algebra and construction.
- `results/tpc242_certificate.json`: canonical exact certificate.
- `code/tpc242_phase_fourier_certificate.py`: mutually exclusive producer/checker.
- `experiments/tpc242_independent_checker.py`: independent strict JSON checker
  with full nested-schema rebinding and four hostile status/source-lock controls.
- `experiments/tpc242_phase_stress.py`: exhaustive bounded Gaussian-integer illustration.
- `paper/paper.pdf`: compiled manuscript.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc242_phase_fourier_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc242_phase_fourier_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc242_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc242_phase_stress.py --check
cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=paper main.tex
```

The finite fixtures and census are classified
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`; the theorem is proved symbolically.

## Maximum status

`PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER`.

Arithmetic `L2`, signed `C_h` cancellation, physical top-prime attachment,
fixed-atom credit, the strict `1/400` endpoint, full Gate B, and any twin-prime
conclusion remain open.
