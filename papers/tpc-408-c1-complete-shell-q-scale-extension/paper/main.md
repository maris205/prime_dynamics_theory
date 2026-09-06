# TPC-408: Complete-Shell C1 Q-Scale Extension

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

TPC-407 tested a locally normalized adjacent-entry proxy on four even complete prime shells. This note extends the finite audit to the next two scales, \(Q=65536\) and \(131072\), whose complete shells contain respectively \(5709\) and \(10749\) primes. The odd cardinalities are retained in full by using the explicit alternating index profile with \(m_- = \lfloor r/2\rfloor\) and \(m_+=\lceil r/2\rceil\). The exact local identity and Cauchy–Schwarz proof still give \(0\le z\le t_1/(a_{\min}\sqrt{S_0S_1})\le4/(a_{\min}H)\le4/H\). An exact rational certificate and independent literal CRT masked-energy replay verify both rows. This remains one synthetic proxy entry and makes no arithmetic or twin-prime claim.

# Odd complete-shell extension

Fix \(H=66\) and \(N=264=4H\). For \(Q>N\), let the complete shell \((Q,2Q]\) contain \(r\ge2\) primes \(p_0<\cdots<p_{r-1}\). We retain all of them, including odd \(r\), and impose \[o\equiv0\pmod {p_i}\quad(i\text{ even}),\qquad
 o\equiv-N\pmod {p_i}\quad(i\text{ odd}).\] Choose the CRT representative above \(10^6\). Put \[t_d=\frac{H^2}{H^2+d^2},\quad S_0=\sum_{d=1}^{N-1}t_d^2,
 \quad S_1=\sum_{d=1}^{N-2}t_d^2+t_1^2,\] and \(a_i=p_i^3/[Q^2(p_i-1)]\). If \(m_-=\lfloor r/2\rfloor\) and \(m_+=\lceil r/2\rceil\), let \(P_-\) be the odd-index amplitude sum and \(V_-,V_+\) the odd/even square sums. The TPC-404 local proxy gives \[G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.\] The height \(H\) here is a proxy parameter, not the physical \(h_0\).

# Finite theorem

**Theorem.** With \(a_{\min}=\min_i a_i\) and \(z=M/\sqrt{G_0G_1}\), \[0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}
 \le\frac4{a_{\min}H}\le\frac4H. \tag{1}\]

**Proof.** Since \(p_i>Q>N\), an even prime masks offset zero and an odd prime first masks offset \(N\); no shell prime masks offset one. Thus the three identities above hold whether \(r\) is even or odd. In particular \(G_1\ge V_-S_1\). Cauchy–Schwarz and the odd-index lower bound give \(P_-^2\le m_-V_-\) and \(V_-\ge m_-a_{\min}^2\). Therefore \[z^2\le\frac{t_1^2m_-}{V_-S_0S_1}
 \le\frac{t_1^2}{a_{\min}^2S_0S_1}.\] For \(1\le d\le H\), \(t_d\ge1/2\), and those terms occur in both sums, so \(S_0,S_1\ge H/4\). Also \(a_i=(p_i/Q)^2p_i/(p_i-1)>1\). Taking square roots proves (1). \(\square\)

#  Exact certificate

The producer enumerates every prime in each declared shell and performs integer CRT and rational arithmetic. The two shell counts are \[\begin{array}{c|r|r|r|r}
Q&r&m_-&m_+&\text{normalized entry}\\ \hline
65536&5709&2854&2855&0.005213967369619\\
131072&10749&5374&5375&0.005218048074517
\end{array}\] The corresponding \(Hz\) observations are \(0.344121846394880\) and \(0.344391172918121\). These decimals are finite float64 observations only; the certificate stores exact rational squares, CRT periods, and all shell primes. The independent checker reconstructs the sieve and literally replays every per-prime, per-coordinate mask before comparing both row energies and the adjacent coefficient.

#  Route boundary

This is a finite extension of one synthetic adjacent normalized proxy entry. It is not a full normalized operator estimate, a physical \(h_0\) theorem, an arithmetic sign or \(L^2\) theorem, a fixed-power saving, Route-A or Route-B closure, or a twin-prime result. The claim status is the exact finite complete-shell Q-scale extension recorded in the certificate; arithmetic advance is `NO`, fixed-power credit is \(0\), and full Gate B is `OPEN`.

# Reproduction

Run the producer, independent replay, and adversarial stress checker with `–check` in both normal and optimized Python modes. Bridge-B repeats these checks, requires empty stderr and identical output, and locks every release artifact by SHA-256.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
