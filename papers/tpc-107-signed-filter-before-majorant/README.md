# TPC-107: Signed filter before positive majorization

Paper title:

> *Signed Filtering before Majorization: Exact Literal
> Reconstruction, a Canonical Signed Energy, and Sharp Separation from
> Positive Resonance*

## Main result

The fully opened literal resonant contribution is written exactly as

```text
S_res = sum_r m_X(r) sum_p alpha_p psi_p(r) 1_E(r omega_p),
```

where each atom retains:

- both Möbius signs;
- the extracted `mu(B)` and coprimality mask;
- the exact reconstruction and determinant phases;
- both polarizations, all native keys, fixed `h0`, and one global
  normalization.

Filtering before taking absolute values gives

```text
S_res = sum_p alpha_p K_p,
K_p   = sum_r m_X(r) psi_p(r) 1_E(r omega_p),
```

and the exact domination chain

```text
|S_res|
 <= sum_p |alpha_p| |K_p|
 <= sum_p |alpha_p| sum_r |m_X(r)| 1_E(r omega_p).
```

The canonical unfiltered signed frequency energy is

```text
E_sig = sum_r |sum_p alpha_p psi_p(r) 1_E(r omega_p)|^2.
```

It has an exact positive-semidefinite `TT*` Gram formula and yields

```text
|S_res| <= ||m_X||_2 sqrt(E_sig).
```

## Sharp boundary

- Oppositely signed identical atom profiles can cancel completely
  while the positive carrier remains nonzero.
- A phase gauge can also saturate the positive carrier.

Thus signed filtering preserves a genuine cancellation channel, but
does not itself prove cancellation.

## Proof levels

- Finite reordering, Gram identities, inequalities, and sharp
  examples: **L0**.
- Exact attachment to the imported TPC-93 dictionary: **L1**.
- The growing fixed-`h0` bound for `E_sig`: **L2**, not proved.

No parity breakthrough, prime-pair lower bound, or twin-prime
conclusion is claimed.

## Reproduce

```powershell
python experiments/tpc107_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`signed-filter-before-majorant.pdf`

SHA-256:

`771DC6B23327B6BE3DDFDFD6FB01E426C9F27E4E50AD6D669F45FFB5B723CFA0`
