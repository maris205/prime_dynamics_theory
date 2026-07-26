# TPC-117: TPC-18 full-block physical cover

Paper title:

> *The TPC-18 Full-Block Physical Remainder: Exact Range Tests,
> Canonical Residuals, and Literal Dual Stop Certificates*

## Core result

For the literal physical vector `w` and the synthesis matrix `B` of
actual TPC-18 blocks,

```text
w in ran(B)
  iff (I - B B^dagger) w = 0
  iff <y,w> = 0 for every y in ker(B*).
```

The canonical coefficients and residual are

```text
c* = B^dagger w,
r* = (I - B B^dagger) w.
```

For physical evaluation `a` and inherited normalization `nu_X`,

```text
nu_X <a,w> = nu_X <B* a,c*> + nu_X <a,r*>.
```

A dual witness `B* y=0`, `<y,w> != 0` sharply disproves exact cover.
It does not by itself prove that the physical residual is large:
TPC-18 may still close if the literal pairing `<a,r*>` is proved
`o(X)`. Exact cover also carries the actual canonical
coefficient/conditioning cost.

## Current verdict

TPC-18 states the required global all-block cover as an additional
hypothesis. This paper supplies an exact executable certificate
format, but no machine-readable growing TPC-18 matrix and physical
vector are available here. H6 is mathematically `OPEN`, and the
current executable range decision is
`NOT-TESTABLE-FROM-CURRENT-ARTIFACTS`.

## Claim level

- Range, residual and dual identities: L0.
- Literal archive and original-scale test: L1 interface.
- No new L2 fixed-shift saving, parity breakthrough or twin-prime
  theorem.

## Reproduce

```powershell
python experiments/tpc117_cover_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`full-block-physical-cover.pdf`

SHA-256: `00d950a1e0a962ab60984a482088a5f48e227e5173325aca04b8185030e032c6`
