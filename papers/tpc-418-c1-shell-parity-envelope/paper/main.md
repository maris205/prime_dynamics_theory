# TPC-418: A Finite-Family Shell-Parity Envelope

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology
- **Source date:** September 7, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

We prove a finite-family synthetic envelope for disjoint ordered complete prime shells. The crucial parity variable is the actual signed-block sign \(\sigma_j=\epsilon_j(-1)^{n_j+1}\), where \(\epsilon_j\) is only the global starting sign. Exact rational replay records this distinction, including a mixed-parity regression on which grouping by \(\epsilon_j\) fails. Combining the envelope with the exact TPC417 endpoint-star/interior-bulk decomposition gives \(\|Z\|_2\le2/(a_{\min}\sqrt H)+16B_*/V_-\). The result is finite and synthetic only; no growing, physical, or arithmetic conclusion is asserted.

# Finite family and signs

Let \(P_j=\{p:Q_j<p\le2Q_j\}\) be disjoint ordered complete shells, with \(Q_j\ge2\), \(n_j=|P_j|\), \(L\ge2\), and all \(p>N=4H\). Set \(\alpha_{j,r}=p_{j,r}^3/[Q_j^2(p_{j,r}-1)]\). Global even indices are positive. The block start sign and actual block sign are \[\epsilon_j=(-1)^{\sum_{\ell<j}n_\ell},\qquad
\sigma_j=\epsilon_j(-1)^{n_j+1}.\] Define \(b_j=\alpha_{j,n_j}-\alpha_{j,1}\) for even \(n_j\) and \(b_j=\alpha_{j,n_j}\) for odd \(n_j\), and group by \(\sigma_j\): \(B_\sigma=\sum_{\sigma_j=\sigma}b_j\), \(B_* = \max(B_+,B_-)\).

# Scalar envelope

For \(f_Q(x)=x^3/[Q^2(x-1)]\), \(f'_Q(x)=x^2(2x-3)/[Q^2(x-1)^2]>0\). Also \(\alpha>1\). Since \(p\) is an odd prime and \(2Q\) is even, \(p\le2Q-1\), so \[\alpha\le\frac{(2Q-1)^3}{Q^2(2Q-2)}<4.\] For increasing \(x_1<\cdots<x_n\), adjacent pairing shows the alternating sum is positive and at most \(x_n\) for odd \(n\), and negative with absolute value at most \(x_n-x_1\) for even \(n\). Thus \(|A|\le B_*\). Even shells have \(b_j<3\), odd shells \(b_j<4\), and odd-shell signs alternate, yielding \[B_*<3E+4\lceil O/2\rceil\le3K+1.\]

# Exact matrix bound

With \(T_d=H^2/(H^2+d^2)\) and \(S_r=\sum_{s\ne r}T_{|s-r|}^2\), exact CRT masks and diagonal deletion give \[M_{0r}=P_-T_r,\quad M_{rs}=-AT_{r-s},\quad
D_0=V_-S_0,\quad D_r=V_-S_r+V_+(S_r-T_r^2).\] Therefore \(Z=D^{-1/2}MD^{-1/2}=\left[\begin{smallmatrix}0&q^T\\q&C\end{smallmatrix}\right]\). Since \(S_r\ge H/4\), \(P_-^2\le m_-V_-\), and \(V_-\ge m_-a_{\min}^2\), \(\|q\|_2\le2/(a_{\min}\sqrt H)\). The one-sided kernel sum is at most \(2H\), while \(D_r\ge V_-H/4\); hence symmetry gives \(\|C\|_2\le16B_*/V_-\). Consequently \[\boxed{\|Z\|_2\le\frac2{a_{\min}\sqrt H}+\frac{16B_*}{V_-}
<\frac2{\sqrt H}+\frac{16(3K+1)}{m_-}}.\]

# Audit and scope

The exact certificate contains a fixed four-shell replay, a small complete multi-shell replay, and a mixed odd/even regression. Producer and independent checker use exact rational strings; mutation tests cover the old sign grouping. This is a finite synthetic envelope, not a growing uniform theorem, and it does not identify physical \(h_0\), prove arithmetic signs or \(L^2\) savings, pay fixed-power credit, close Route-B, or imply twin primes.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
