# TPC-108: Literal generic-affine Möbius dispersion

Paper title:

> *Literal Generic-Affine Möbius Dispersion: Exact `TT*` Kernels, a
> Chowla-Level Uniformity Barrier, and the Restricted Arithmetic
> Hypothesis*

## Main exact results

For one actual TPC-93 generic block,

```text
D(z) = d + s z
V(z) = u + a z
s u - a d = h0 != 0
N ||alpha|| > 1,
```

the literal block transform has the exact identity

```text
|sum_z A(z)e(-alpha z)|^2
  = sum_h e(-alpha h)
      sum_z A(z+h) conjugate(A(z)).
```

The off-diagonal contains four actual Möbius values. Both shifted
affine pairs still have determinant `h0`.

For an invertible phase slope modulo the no-wrap prime,

```text
sum_r |sum_z A(z)e_q(-r omega z)|^2
  = q sum_(u mod q) |sum_(z = u mod q) A(z)|^2.
```

This is an exact complete-frequency theorem with an explicit aliasing
ledger. It does not select the literal low-frequency filter.

## Two barriers

1. `N||alpha|| > 1` alone gives only a constant geometric-series
   gain and can be saturated by bounded phase-matched coefficients.
2. A broad prefix-uniform power-saving theorem for every generic
   twist of `lambda(n)lambda(n+h0)` would imply a power-saving
   ordinary two-point Chowla estimate by Abel summation.

Therefore the desired theorem must exploit the restricted actual TPC
coefficient family. It cannot be replaced by a convenient
arbitrary-form statement without importing a very deep open input.

## Exact exponent ledger

If every actual block saves `X^(-eta)` relative to its literal
absolute mass and the outer reassembly costs `X^ell_out`, then the net
termwise saving is

```text
X^(-(eta-ell_out)).
```

This route reaches the H3 quadratic target only if
`eta-ell_out >= 1/200`. The physical `TT*` crosswalk is still
separate, and neither input is proved.

## Honest status

- Exact `TT*`, determinant, full-frequency, Abel, and obstruction
  statements: **L0**.
- Crosswalk to the TPC-93 literal blocks: **L1**.
- The growing restricted fixed-`h0` Möbius estimate H3: **L2**, not
  proved.

No parity breakthrough, prime-pair lower bound, or twin-prime
conclusion is claimed.

## Reproduce

```powershell
python experiments/tpc108_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`literal-generic-affine-mobius-dispersion.pdf`

SHA-256:

`375F110F421E99A01620FCF4B09F90606441E9F9E84E388831DFA334569854E7`
