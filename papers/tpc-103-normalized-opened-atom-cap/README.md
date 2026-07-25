# TPC-103: Normalized opened-atom cap

Paper title:

> *The Normalized Opened-Atom Cap in the Literal Resonance Carrier:
> A Pointwise Factor Audit and Diagonal Transfer*

## Exact result

For every actual invertible opened atom `p=(beta,z)` in the
TPC-100 census, the paper pulls its coefficient back through the
lossless TPC-93 source inverse and charges every factor exactly once.
The two literal row coefficients are pointwise logarithmic; the
opened logarithmic leg, matched prefix, projector, exact-content,
smooth and mask factors are bounded by a fixed product of logarithms
and divisor functions of integers of size `X^O(1)`. No second
fiber or column normalization is introduced.

Thus, for a fixed `A`,

```text
W_X <= (log X)^A max_{n <= X^A} tau(n)^A = X^o(1).
```

This closes Gate W from TPC-102. Combined with the exact TPC-101
principal-to-diagonal transfer, it means that the positive
width-weighted diagonal ledger follows from the still-unproved
principal-mass gate.

## Claim level

- The finite factor and provenance identities are L0.
- The cap on the actual fixed-`h0` opened atoms is L1 bookkeeping
  progress.
- No principal-mass bound, cross-map estimate, signed Mobius
  cancellation, L2 fixed-power saving, parity breakthrough, or
  prime-pair theorem is claimed.

The paper keeps one prescribed nonzero `h0`, both polarizations,
actual support, all source/content/projector/mask labels, and the
single inherited physical normalization. It does not specialize to
`h0=2`.

## Reproduce

```powershell
python experiments/tpc103_atom_cap_audit.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`normalized-opened-atom-cap.pdf`

SHA-256:

`3C692D0322508FB1AFD793DB1A039414EC61877A057BE276127633FC3D9BCD7C`
