# TPC-253: Source-Frozen Rank-Midpoint Contrasts for the Literal V59 Scalar

Status:

```text
PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER
```

TPC-253 freezes a coefficient-independent two-block partition directly from
the ordered physical interval

```text
I_x=(x/2,x] intersect Z={n_1<...<n_N},  N>=2.
```

With `ell=floor(N/2)`, `r=N-ell`, `L={n_1,...,n_ell}`, and `R=I_x\L`, put

```text
rho^2=ell*r/N,
z=rho(1_L/ell-1_R/r).
```

The split is fixed before `beta`, `w`, `A_x beta`, a margin, or a sign is
inspected. It gives the exact identities

```text
M_mid=M_coarse+z tensor z,
C_long(mid)-C_long(coarse)=conjugate(<z,w>)<z,A_x beta>,
Q_trans(mid)-Q_trans(coarse)=-conjugate(<z,w>)<z,A_x beta>.
```

Both longitudinal terms and the midpoint transverse covariance have exact
partial-sum formulas. For integer `x=k>=3`, the last coordinate in `L` is
exactly `floor(3k/4)`. Substitution of the literal TPC-247 operator preserves
the output/input orientation, outer prime weight, both unit masks, deleted
diagonal, physical kernel, centered residue bracket, and literal `beta`. The
valid adjoint crosswalk is `<z,A_x beta>=<A_x^*z,beta>`; no self-adjointness is
used or claimed.

## Reproduce

Run from the repository root with bytecode disabled:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/code/tpc253_midpoint_contrast_certificate.py --check
python -O -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/code/tpc253_midpoint_contrast_certificate.py --check
python -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_independent_checker.py --check
python -O -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_independent_checker.py --check
python -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_midpoint_contrast_stress.py --check
python -O -B papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/experiments/tpc253_midpoint_contrast_stress.py --check
```

The producer emits one-line canonical strict JSON with exact rational and
Gaussian-rational data. Radical approximation is avoided by recording the
projector products `rho^2*h_i*h_j`. The independent checker imports no
producer code, uses exact integer type identity, rejects bool-as-int count and
coordinate mutations, and rejects 59 typed, semantic, source, firewall,
digest, duplicate-key, nonfinite-token, and noncanonical-byte mutations. The
stress suite checks 192 deterministic exact-rational families, including 96
nonintegral clocks and all four integer residue classes modulo four.

## Build

From `paper/`, run the required explicit passes:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

## Claim boundary

The exact-sample kernel fixture and the constant/sign controls are labeled
nonliteral. They do not replay the unknown physical `w` or actual Fourier
kernel data. The midpoint is a source-only modeling choice, not a canonical
V59 partition and not V59's smooth bounded-overlap partition. No sign,
nonzero value, scale, asymptotic estimate, arithmetic saving, L2, fixed-atom
credit, Gate-B closure, strict `1/400`, or twin-prime result follows.

Maximum supported claim:

```text
EXACT_SOURCE_FROZEN_RANK_MIDPOINT_PROJECTOR_PARTIAL_SUM_LONGITUDINAL_TRANSVERSE_LITERAL_TPC247_KERNEL_AND_SAFE_ADJOINT_COMPILER_WITH_NONLITERAL_SHARP_SIGN_CONTROLS
```
