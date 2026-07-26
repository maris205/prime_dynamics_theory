# TPC-119: Original Hard-Packet Reconnection

This paper audits MVP1 Hypothesis H8 against the original TPC-15
fixed-shift scalar packet.

The TPC-15 packet has the exact opened native-atom form

\[
B_{h_0,\delta}(X)
=
\sum_{\alpha=(\ell,k,d)\in\mathcal A_X}c_X(\alpha).
\]

For a chosen canonical leaf archive with coefficient matrix `M_X`, retained
matrix `M_ret`, and soft matrix `M_soft`, the proof-carrying
reconnection test is

\[
M_X=M_X^{\rm can},\qquad
M_X=M_{\rm ret}+M_{\rm soft},\qquad
\mathbf 1^T M_X=\mathbf 1^T.
\]

It gives the exact identity

\[
B_{h_0,\delta}(X)
=
\mathbf 1^TM_{\rm ret}c_X+
\mathbf 1^TM_{\rm soft}c_X.
\]

The certificate must also retain the same fixed `h0`, one physical
normalization, native provenance, and the canonical leaf set. A scalar
numerical equality alone does not exclude deletion, duplication,
surrogate atoms, or null-pair inflation.

The audit verdict is:

`canonical-leaf H8 audit = NOT_TESTABLE_FROM_CURRENT_ARTIFACTS`.

This is a repository snapshot verdict for the explicitly enumerated
series through TPC-118, audited on 2026-07-26. The canonical matrix is
a strong sufficient proof-carrying certificate, not a logically
necessary format for every possible H8 proof; an alternative exact
composite intertwining could also close H8.

TPC-15 proves the scalar anchor, and several later papers prove local
lossless transformations, but the current series does not contain one
complete machine-readable canonical leaf archive from every opened
TPC-15 atom through the final retained/soft synthesis. This is an
explicit missing certificate, not an impossibility theorem.

No L2 fixed-shift estimate, parity breakthrough, Hardy--Littlewood
asymptotic, prime-pair lower bound, or twin-prime theorem is proved.

## Reproduction

```powershell
python experiments/tpc119_reconnection_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-119-original-hard-packet-reconnection.pdf`

SHA-256:

`791476c4feccc00ec45b2eff075eb27d9d2e9fd71a2f530dddbe76c352bb54ba`
