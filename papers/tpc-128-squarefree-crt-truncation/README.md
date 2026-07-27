# TPC-128: Squarefree Masks in the Shift-Two Frame

Paper title:

> *Squarefree Masks in the Shift-Two Frame: Exact CRT Fibers,
> Primitive Truncation Tails, and the Growing-Modulus Ledger*

For the TPC-127 determinant-two frame, define

\[
Q_R(m)=\sum_{\substack{k\le R\\k^2\mid m}}\mu(k).
\]

The truncated two-mask product is exactly a signed sum of compatible
CRT fibers:

\[
Q_R(D(z))Q_R(V(z))
=\sum_{\substack{k,\ell\le R\\
(k,s)=(\ell,a)=(k,\ell)=1}}
\mu(k)\mu(\ell)
\mathbf 1_{z\equiv r_{k,\ell}\pmod{k^2\ell^2}}.
\]

In the shift-two variable, each fiber has modulus
\(ask^2\ell^2\le asR^4\). For affine values at most \(Y\) on an
interval of length \(N\), the paper proves the elementary tail

\[
\ll \tau_*(Y)\left(\frac NR+\sqrt Y\right)
\]

and the component census \(O(N+R^2)\).

The exponent ledger is explicitly piecewise.  When
`R < sqrt(Y)`, the elementary tail is compared with the declared
actual absolute mass.  When `R >= sqrt(Y)`, the squarefree
truncation is exact and the tail is zero, but the effective CRT
range is capped at `sqrt(Y)` and its modulus/census costs remain.
The point census becomes a block-relative saving only under a
separate mass-comparability hypothesis; otherwise an actual weighted
census is required.

Status:

- CRT identities, tail, and census: **L0**;
- attachment to the literal fixed-2 frame: **L1**;
- uniform signed cancellation on the resulting fibers: **not
  proved**.

The paper gives a loss ledger and stop rules; it does not infer a
physical saving from squarefree density.

The audit separately tests the exact-tail regime
\(R\ge\sqrt Y\), the effective \(\sqrt Y\) cutoff cap, and the rule
that a nonpositive exponent must not be advertised as a saving.  Its
finite tail and census comparisons use integer majorants.

Reproduce:

```powershell
python experiments/tpc128_crt_audit.py
python experiments/tpc128_crt_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-128-squarefree-crt-truncation.pdf`

SHA-256:

`5d537e8415323e55f781346f664676f9bde708821b34bb3bcd00595069ef7df8`
