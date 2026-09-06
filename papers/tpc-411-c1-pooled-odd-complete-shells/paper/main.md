# TPC-411: Pooled Odd Complete-Shells

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 6, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

TPC-409 and TPC-410 audited odd complete shells separately. We now pool the two full shells at \(Q=65536\) and \(Q=131072\), retaining all \(5709+10749=16458\) primes. At fixed \(H=66\), \(N=264=4H\), the pooled profile has equal parity counts \(m_-=m_+=8229\). Shell-local amplitude normalizations are kept, and the exact local identity plus Cauchy–Schwarz gives \(0\le z\le t_1/(a_{\min}\sqrt{S_0S_1})\le4/(a_{\min}H)\le4/H\). An exact rational certificate and an independent literal CRT replay verify the pooled row. This is a synthetic finite proxy result, not an arithmetic or twin-prime theorem.

# Pooled complete-shell profile

Let \(\mathcal P\) be the increasing concatenation of the complete shells \((65536,131072]\) and \((131072,262144]\). Their counts are \(5709\) and \(10749\), so \(|\mathcal P|=16458\). For \(p_i\in\mathcal P\), let \(Q_i\) denote its shell scale and set \[H=66,\quad N=264=4H,\qquad
 a_i=\frac{p_i^3}{Q_i^2(p_i-1)}.\] Choose a CRT representative \(o>10^6\) satisfying \[o\equiv0\pmod {p_i}\quad(i\text{ even}),\qquad
 o\equiv-N\pmod {p_i}\quad(i\text{ odd}).\] All primes are retained; hence \(m_-=m_+=8229\). With \[t_d=\frac{H^2}{H^2+d^2},\quad S_0=\sum_{d=1}^{N-1}t_d^2,
 \quad S_1=\sum_{d=1}^{N-2}t_d^2+t_1^2,\] the local proxy has \[G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.\] The parameter \(H\) is a proxy height, not the physical \(h_0\).

# Finite pooled theorem

**Theorem.** If \(a_{\min}=\min_i a_i\) and \(z=M/\sqrt{G_0G_1}\), then \[0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}
\le\frac4{a_{\min}H}\le\frac4H. \tag{1}\]

**Proof.** Every pooled prime is larger than \(N\). The even class masks offset zero and the odd class first hits offset \(N\), so no prime masks offset one and the three displayed identities follow. Since \(m_-=8229\), we have \(P_-^2\le m_-V_-\) and \(V_-\ge m_-a_{\min}^2\); moreover \(G_1\ge V_-S_1\). Thus \[z^2\le\frac{t_1^2m_-}{V_-S_0S_1}
 \le\frac{t_1^2}{a_{\min}^2S_0S_1}.\] The terms \(1\le d\le H\) occur in both sums and satisfy \(t_d\ge1/2\), hence \(S_0,S_1\ge H/4\). Finally \(a_i=(p_i/Q_i)^2p_i/(p_i-1)>1\). Taking square roots proves (1). \(\square\)

# Exact certificate and observation

The producer enumerates both full shells, records each prime’s \(Q_i\), and uses integer CRT and exact rational arithmetic. The pooled row has \[\begin{array}{c|c|c|c|c}
\text{shells}&|\mathcal P|&m_-&m_+&z\\ \hline
65536,131072&16458&8229&8229&0.005216872683870
\end{array}\] and the finite observation \(Hz=0.344313597135425\). This decimal is derived from an exact rational square and is not an asymptotic claim. The independent checker rebuilds both sieves and the pooled CRT, then literally visits every per-prime, per-coordinate mask for both local rows before comparing \(G_0\), \(G_1\), and \(M\).

# Route boundary

This is one finite pooled synthetic adjacent normalized proxy entry. It does not prove a full normalized operator estimate, identify physical \(h_0\) or arithmetic signs, pay arithmetic \(L^2\) or fixed-power credit, close Route A/B, or imply a twin-prime result. The exact finite pooled odd complete-shell status is recorded in the certificate; arithmetic advance is `NO`, fixed-power credit is \(0\), and full Gate B is `OPEN`.

# Reproduction

Run the producer, independent replay, and nine-mutation stress checker with `–check` in normal and optimized modes. Bridge-B repeats these checks, requires empty stderr and identical output, and locks the release artifacts by SHA-256.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
