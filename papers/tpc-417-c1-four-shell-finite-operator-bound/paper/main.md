# TPC-417: A Finite Full-Operator Bound for the Four-Shell C1 Proxy

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 6, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

We extend the four-shell pooled C1 proxy from one adjacent entry to its full finite window matrix. For four complete prime shells and each of \(H\in\{16,32,66,128\}\), we derive the exact endpoint/interior diagonal energies and a block decomposition of the locally normalized matrix. A finite, explicit bound is obtained: \(\|Z\|_2\le 2/(a_{\min}\sqrt H)+16|A|/V_-\). The certificate and an independent aggregate replay use exact rational arithmetic and retain all \(75483\) primes. This is a finite synthetic-operator theorem only: it does not provide a growing bound, physical coefficient identification, arithmetic \(L^2\) saving, Route-B closure, or a twin-prime result.

# Finite model

Let \(I_o=\{o,\ldots,o+N-1\}\), \(N=4H\), and \(T_d=H^2/(H^2+d^2)\). Pool the complete shells \(Q<p\le2Q\) for \(Q=65536,131072,262144,524288\), with counts \(5709,10749,20390,38635\). Order the resulting primes and set \(a_i=p_i^3/[Q_i^2(p_i-1)]\). Even indices divide \(o\) and odd indices divide \(o+N\); the CRT gives such an \(o>B\) for every \(B\). Put \(P_-=\sum_{i\text{ odd}}a_i\), \(P_+=\sum_{i\text{ even}}a_i\), \(A=P_+-P_-\), and \(V_\pm=\sum_{i\,\text{of sign}\,\pm}a_i^2\).

# Exact matrix identities

For \(0\le r,s<N\) and \(r\ne s\), the diagonal-deletion identity gives \[M_{rs}=T_{r-s}\{-A+b_r+b_s\},
\qquad b_0=P_+,\quad b_r=0\ (r\ge1).\] Define \(S_r=\sum_{s\ne r}T_{r-s}^2\). The literal masks therefore give \[D_0=V_-S_0,\qquad D_r=V_-S_r+V_+(S_r-T_r^2)\quad(1\le r<N).\] After conjugation by \(D^{-1/2}\), the matrix has the block form \[Z=\begin{pmatrix}0&q^T\\q&C\end{pmatrix},\quad
 q_r={P_-T_r\over\sqrt{D_0D_r}},\quad
 C_{rs}={-AT_{r-s}\over\sqrt{D_rD_s}}\quad(r\ne s),\qquad C_{rr}=0.\]

# Bound

At least \(H\) distances on one side of every interior point are at most \(H\), so \(S_r\ge H/4\). Cauchy–Schwarz gives \(P_-^2\le m_-V_-\) and \(V_-\ge m_-a_{\min}^2\). Since \(\sum_{r=1}^{N-1}T_r^2\le S_0\), \[\|q\|_2^2\le {4P_-^2\over V_-^2H}\le {4\over a_{\min}^2H}.\] Also \(D_r\ge V_-H/4\). Splitting the kernel sum at \(H\) gives \(\sum_{d\ge1}T_d\le2H\) on each side, hence every absolute row sum of \(C\) is at most \(16|A|/V_-\). Symmetry gives the same \(2\)-norm bound. The triangle inequality applied to the star block and the bulk block proves \[\boxed{\|Z\|_2\le {2\over a_{\min}\sqrt H}+{16|A|\over V_-}}.\] The star certificate records the exact Cauchy–Schwarz envelope, not an exact spectral norm. All bound coefficients are exact rational quantities; no decimal observation enters the proof.

# Scope and audit

The four heights are independently recomputed from exact fractions. The certificate records shell hashes, all aggregate quantities, positivity of the local diagonals, and both components of the bound. The producer, independent replay, and mutation checker are run in normal and optimized modes. The result is a full finite matrix bound for the declared synthetic proxy, not a bound uniform in growing \(H,Q,N\) and not a statement about the physical source signs.

|                                         |                       |
| :-------------------------------------- | :-------------------- |
| finite full matrix bound                | `PROVED_EXACT_FINITE` |
| growing operator theorem                | `OPEN`                |
| physical \(h_0\)/arithmetic sign        | `OPEN`                |
| arithmetic advance / fixed-power credit | `NO` / 0              |
| Route-B / twin-prime result             | `OPEN` / `NONE`       |

# Reproduction

The project README lists the producer, independent replay, stress checker, and Bridge-B commands. The exact JSON certificate and proof package are part of the release.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
