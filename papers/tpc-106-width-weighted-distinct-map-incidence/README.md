# TPC-106: Width-weighted distinct-map incidence

Paper title:

> *Width-Weighted Incidence after the Canonical Affine Quotient:
> Exact Character Coherence, Sharp Alignment Obstructions, and the
> Positive-Route Decision*

## Main result

After the TPC-105 quotient, each canonical map

```text
phi(j) = A_phi (m_phi j + h0)
```

retains its full opened-atom input profile. If `f_phi` is its exact
output pushforward, the genuinely distinct-map cross excess has the
three equivalent forms

```text
X_dist
  = sum_(phi != psi) <f_phi^circ, f_psi^circ>
  = 1/(q-1) sum_(chi != 1) sum_(phi != psi)
      fhat_phi(chi) conjugate(fhat_psi(chi))
  = ||a_H^circ||_2^2 - sum_phi ||f_phi^circ||_2^2.
```

Writing

```text
E_H     = sum_phi ||f_phi^circ||_2^2
kappa_H = |X_dist| / E_H,
```

the exact TPC-106 gate is

```text
sum_H g_q(H) sqrt(kappa_H E_H) <= X^o(1) Q_X^2.
```

The universal bound `kappa_H <= number_of_maps - 1` is sharp. A
finite construction shows that pairwise distinct maps of the actual
shape `A(mj+h0)` can all send one active input to one common output.
Therefore distinctness, injectivity, and width weighting alone give
no dispersion theorem.

## Honest verdict

- Exact Fourier/Gram identities and the alignment countermodel are
  **L0**.
- Their crosswalk to the provenance-preserving TPC-105 profiles is
  an **L1** interface.
- The actual growing width-weighted character-coherence bound is not
  proved, so there is no **L2** fixed-`h0` advance.

The result stops geometry-only arguments. It does not prove that the
literal positive route fails. A polynomial obstruction on the
actual profiles would trigger TPC-107's signed-filter route.

## Reproduce

```powershell
python experiments/tpc106_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`width-weighted-distinct-map-incidence.pdf`

SHA-256:

`D1451724FD0DEBE1A314EF3D3915530AE02619E1D0A9C17B1D30EFBF09A4BED2`
