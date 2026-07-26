# TPC-114: Residual grouping and the native Gram

Paper title:

> *Literal Residual Grouping and the Native Gram: Divisor-Collision
> Parametrization, Exact Coarea Singular Values, and a Provenance
> Intertwining*

## Core result

Source records first group by

```text
q(u) = (gamma_u, j_u, d(m_u) r_u)
```

and only then pass through the native-label map `pi`. For the weighted
grouping `R_a e_u = a_u e_q(u)`,

```text
R_a R_a^* = diag(W_y),
W_y = sum_{q(u)=y} |a_u|^2.
```

Thus the nonzero singular values are exactly `sqrt(W_y)`. The two
source-side Grams are

```text
G_res = R_a^* R_a,
G_nat = R_a^* P^* P R_a.
```

Their difference contains exactly unequal residual labels that share
one native label. For any upstream synthesis `S`,

```text
(P R_a S)^* (P R_a S) = S^* G_nat S.
```

The upper native factor is `k_max` in squared `l2` energy and
`sqrt(k_max)` in `l2` amplitude.  It is not automatically the H9
max-packet-to-scalar cost.  If a native fiber contains at least two
residual labels, a positive lower transfer fails on the full residual
space because the two labels can cancel exactly.  The Gram difference
is generally indefinite, not an automatic energy gain.

## Claim level

- The collision normal form and matrix identities are L0.
- The literal `s=d(m)r` provenance dictionary is L1.
- No growing fiber bound, native frame bound, prescribed-shift L2
  saving, parity breakthrough, or prime-pair theorem is claimed.

## Reproduce

```powershell
python experiments/tpc114_grouping_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`residual-grouping-native-gram.pdf`

SHA-256: `dab30939e149c37404ffc329d34edc28b292d00927464a51bb9e65dabf54eb91`
