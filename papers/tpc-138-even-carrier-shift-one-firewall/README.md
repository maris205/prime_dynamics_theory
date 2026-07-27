# TPC-138: Even-carrier shift-one firewall

Paper title:

> *Quantitative Shift-One Shadows of the Determinant-Two Frame:
> Exact Even-Carrier Transfer and the Active Odd-Carrier Firewall*

The unrestricted shift-two sign has the exact even-carrier identity

\[
\lambda(2m-2)\lambda(2m)=\lambda(m-1)\lambda(m).
\]

Thus proved quantitative results for the consecutive Liouville
correlation apply to the even part of an unrestricted shift-two
sum. However, TPC-127 proves that the simultaneous squarefree
determinant-two carrier has \(D,V\) odd, hence

\[
n=sV=aD+2
\]

is odd. The quantitative even-carrier shadow is therefore disjoint
from the actual active carrier.

The paper also proves a determinant invariant. On an odd residue
class \(n=r+Mt\), after extracting fixed contents \(c_-,c_+\) from
\(n-2,n\), the reduced determinant is

\[
\frac{2M}{c_-c_+},
\]

which is in fact divisible by four. It cannot become the
determinant-one pair
\((t,t+1)\).

The paper cites Helfgott--Radziwill and Pilatte only for their stated
shift-one conclusions. It does **not** attribute an arbitrary-affine
quantitative theorem to either source. It separately records the
new Tao--Teräväinen (2026) corridor: a power-of-log estimate for
positive affine data of sufficiently small polylogarithmic height,
outside a small logarithmic-density exceptional set. That corridor
can cover eligible determinant-two components, but does not by
itself provide full CRT reassembly or deterministic all-prefix
control.

Status:

- even-carrier transfer and determinant invariant: **L0**;
- active odd-carrier non-transfer: **proved firewall**;
- small-polylog determinant-two almost-scale estimate:
  **proved external input**;
- actual CRT/all-prefix physical return: **OPEN**;
- positive actual-family L2: **not proved**.

Reproduce:

```powershell
python experiments/tpc138_even_carrier_audit.py
python experiments/tpc138_even_carrier_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-138-even-carrier-shift-one-firewall.pdf`
