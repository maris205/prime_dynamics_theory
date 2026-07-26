# RH-161: Packet-to-Riesz Relative-Determinant Assembly

RH-161 resolves the type gap between RH-160's reset-support packets and
RH-80's moving Riesz cloud. Its main analytic theorem says that if the block
resolvent on a contour is bounded by `M` and the off-packet coupling is at
most `epsilon`, then `M epsilon < 1` preserves the enclosed spectral rank.
Moreover,

```text
delta = |Gamma| M^2 epsilon / (2 pi (1 - M epsilon)) < 1
```

gives a stable graph bridge from the reset packet to the true same-rank Riesz
subspace.

The paper then combines this lift with:

- exact moving-cloud determinant division;
- a common-space Schatten-norm limit for the complementary block;
- a complete deterministic pole ledger;
- target-independent normalization and schedule independence;
- directed marked traces that retain temporal orientation.

The result is an abstract typed assembly theorem for an enhanced spectral
datum `(relative determinant, directed marked traces)`. It is stated for
both determinant types used upstream: `p=1` gives RH-80's two-step Fredholm
branch, while `p=2` gives the one-step regularized-determinant branch required
by RH-MVP1. The theorem does not identify these two branches.

## Current frontier

The all-level assembly formula is

```text
(S_native OR S_lagged) AND R AND Q AND U AND Z AND T.
```

It has two inclusion-minimal completion bundles:

```text
{S_native, R, Q, U, Z, T}
{S_lagged, R, Q, U, Z, T}
```

The two reset seeds have conditional formulas only; `R`, `Q`, `U`, `Z`, and
`T` remain open for the prime-dynamics family. RH-161 therefore sharpens Gate
`A` but does not close it.

## Claim boundary

The paper does not prove an eventual O/E/S/L law, a physical packet-to-Riesz
estimate, a cloud coefficient bridge, a uniform complement limit, a canonical
all-level determinant, a Hilbert--Polya operator, zeta-zero identification, or
the Riemann Hypothesis. The illustrative numerical table evaluates theorem
bounds only; it is not operator data.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_typed_assembly_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf packet-riesz-relative-determinant-assembly.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
