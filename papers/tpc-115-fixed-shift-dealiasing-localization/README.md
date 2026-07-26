# TPC-115: Fixed-shift de-aliasing and localization

Paper title:

> *Fixed-\(h_0\) De-Aliasing after Frozen Averaging: Exact Evaluation
> Norms, Christoffel Costs, and a Sharp Localization Obstruction*

## Core result

For an observation `A`, weight matrix `Omega`, and target functional
`ell(x)=b0^* x`, put

```text
G = A^* Omega A.
```

A finite localization inequality exists exactly when `b0` lies in
`range(G)`, equivalently when the target annihilates the weighted
observation kernel. Its sharp constant is

```text
K_loc = b0^* G^dagger b0.
```

For a declared shift-profile basis `B`, the prescribed-shift cost is

```text
K_V(h0) = b(h0)^* (B^* Omega B)^dagger b(h0).
```

Exact regimes:

- unrestricted profiles: `K=1/p_h0`;
- constant profiles: `K=1`;
- any `d` distinct cyclic characters under uniform averaging: `K=d`;
- target nonzero on the observation kernel: `K=infinity`.

Thus an averaged estimate transfers to one fixed shift only after the
actual profile space and its Christoffel cost are certified.

## Claim level

- The pseudoinverse formula and obstruction are L0.
- Their attachment to a literal physical profile is a conditional L1
  bridge.
- No low-dimensional model for the actual TPC shift profile, fixed
  shift L2 saving, parity breakthrough, or prime-pair theorem is
  claimed.

## Reproduce

```powershell
python experiments/tpc115_localization_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`fixed-shift-dealiasing-localization.pdf`

SHA-256: `21a4bb1c68094ae813ed808f43960ab45a93c9935df17bda6c79810eadec4b8b`
