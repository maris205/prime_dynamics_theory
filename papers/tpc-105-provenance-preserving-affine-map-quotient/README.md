# TPC-105: Provenance-preserving affine-map quotient

Paper title:

> *A Provenance-Preserving Quotient of Literal Affine Maps:
> Exact Collision Splitting and the Identical-Map Concentration
> Ledger*

## Exact result

Each actual invertible opened atom carries

```text
phi_p(x) = s_p x + t_p,
s_p = A_p m_p,
t_p = A_p h0,
omega_p = phi_p(j_p).
```

Atoms are quotiented by identical `(s_p,t_p)`. A lossless analytic
quotient must retain the input profile

```text
nu_phi(j) = sum_{p: phi_p=phi, j_p=j} w_p,
```

while a full provenance bag is retained for source recovery. The
total map weight alone is not sufficient; the paper gives an exact
two-point counterexample.

The TPC-100 cross ledger splits exactly into

```text
X_H^circ = K_H^circ + Y_H^circ,
```

where `K` contains identical maps and `Y` genuinely distinct maps.
If `U_X` is the maximum total weight of one map class, then

```text
|K_H^circ| <= U_X M_H
```

and

```text
sum_H g_q(H) sqrt(|K_H^circ|)
 <= sqrt(U_X |H_X| (q_X-1) P_X).
```

Thus TPC-106 should attack the width-weighted `Y` ledger while
carrying `U_X` as a separate concentration gate.

## Claim level

- Map classification, quotient identities, collision splitting and
  countermodels are L0.
- Their exact attachment to the actual fixed-`h0` opened carrier is
  an L1 reduction.
- No actual `U_X`, principal-mass, or distinct-map bound is proved.
  No L2 fixed-power saving, parity breakthrough, or prime-pair
  theorem is claimed.

## Reproduce

```powershell
python experiments/tpc105_map_quotient_audit.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`provenance-preserving-affine-map-quotient.pdf`

SHA-256:

`3066B19F07DBBFADDDB50D04C65C978AD61700D5795D880AAC82DA28A50989E3`
