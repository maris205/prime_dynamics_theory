# TPC-116: Complete high-frequency and ultra-tail closure

Paper title:

> *Complete High-Frequency and Ultra-Tail Closure at the Original
> Physical Normalization: An Exact Partition, an Optimal Hilbert
> Test, and a Sharp Phase-Blind Obstruction*

## Core result

Given a declared complete family of masks, the paper characterizes
exact one-fold partition of the physical atom set into the low window
and every high-frequency, ultra-tail, short, boundary and collision
complement. For a frequency class `E`, the optimal constant-one
estimate is

```text
|Tail_E|
 <= nu_X ||m_hat 1_E||_2 ||A_hat 1_E||_2.
```

It closes a class only when both energies include the complete outer
labels and the inherited normalization. Conversely, from atom
magnitudes alone,

```text
sup_phases |sum phase_omega a_omega| = sum a_omega.
```

Thus support sparsity, short fibers and bounded overlap do not
manufacture a power saving. A complete conditional theorem makes the
whole complement `o(X)` when every mask is present exactly once, all
soft classes are `o(X)` at original scale, and the aggregate retained
packet has a fixed power saving. To satisfy the retained-packet clause
of MVP1 H4, that raw saving must be at least `1/400`; later H9
reassembly costs are accounted for separately. The actual growing
mask archive and its bounds are not verified here.

## Claim level

- Exact partition, Hilbert inequality and phase-alignment obstruction:
  L0.
- Attachment to literal TPC labels and normalization: L1 interface.
- No complete growing TPC tail estimate, new L2 fixed-shift saving,
  parity breakthrough or twin-prime theorem is claimed.

## Reproduce

```powershell
python experiments/tpc116_tail_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`complete-tail-closure.pdf`

SHA-256: `485764f82282a52e2fc1a3f691cc9a46893d545334682cfa0a98d0b6fbe2af93`
