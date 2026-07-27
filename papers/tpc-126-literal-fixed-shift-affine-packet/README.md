# TPC-126: A literal fixed-shift generic-affine packet

This paper gives the exact invocation protocol for one complete
archived generic-affine packet at a prescribed nonzero shift.

For

```text
T_b = sum_(z in I_b) A_b(z) e(-alpha_b z),
s_b u_b - a_b d_b = h0,
```

it proves the literal lag identity

```text
|T_b|^2
  = sum_r e(-alpha_b r)
      sum_(z,z+r in I_b) A_b(z+r) conjugate(A_b(z)),
```

and the exact canonical-order Abel identity.  It also proves the
complete-family normalization

```text
|S_X| / sum_b |gamma_b| M_b
  <= (
       sum_b q_b |T_b|^2 / M_b^2
     )^(1/2).
```

Consequently, a future bound by `X^(-2 eta + o(1))` for the squared
right-hand side produces relative amplitude saving `eta`.  After a
separately proved outer loss `lambda_out`, the deliberately
termwise TPC-108 route has the stronger linear-window sufficient
condition

```text
eta - lambda_out >= 1/200.
```

This is not the exact quadratic-to-amplitude threshold of MVP1.
Recovering the packet-level `1/400` saving still requires the
separate physical `TT*` crosswalk and prefactor; a coherent route
could have a different sufficient condition.

The paper does **not** prove this growing bound.  Its exact finite
identities are L0; their attachment to a complete literal
TPC-123--125 archive is an L1 interface.  Finite regressions,
frozen blocks, averaged shifts, and surrogate signs are explicitly
excluded from H3/L2 status.

The bundled ordinary double-precision finite regression passes. Its
metadata check covers only a declared sample-key subset, not the
complete literal metadata archive. Accordingly its machine verdict
keeps both `GO_INTERFACE` and `GO_H3` false.

No parity breakthrough, prime-pair lower bound, Hardy--Littlewood
asymptotic, or twin-prime theorem is claimed.

## Reproduce

```powershell
python experiments/tpc126_literal_packet_audit.py --write --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-126-literal-fixed-shift-affine-packet.pdf`

SHA-256:

`f1802488aaa06ecdc3e62a2e452301a5376091e74f7f8c5744b1f1c86369775f`
