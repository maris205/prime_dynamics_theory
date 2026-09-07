# TPC-416: Four-Shell Odd Pooled Extension

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 6, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We add the complete shell at $Q=524288$ to the pooled profile. The four shells retain $75483$ primes. At $H=66$, $N=264$, shell-local amplitudes and pooled alternating CRT give the explicit odd parity counts $m_-=37741,m_+=37742$. Exact arithmetic and an independent literal replay verify the finite row; no arithmetic theorem is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Four-shell profile

Let $\mathcal P$ be the increasing union of four consecutive dyadic shells from $65536$ through $1048576$. Set $a_i=p_i^3/[Q_i^2(p_i-1)]$ using each source-shell scale, and impose alternating CRT residues with $H=66,N=264=4H$. The total count is $5709+10749+20390+38635=75483$, so $m_-=37741,m_+=37742$. Every prime exceeds $N$, hence $$G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.$$ The same Cauchy–Schwarz argument gives $$0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}\le\frac4{a_{\min}H}\le\frac4H.\tag{1}$$

# Exact observation

The certificate stores all 75483 prime labels, shell scales, CRT data, and exact rational energies. The independent checker rebuilds the four sieves and literally visits every mask for every prime and coordinate before comparing $G_0$, $G_1$, and $M$.

# Scope and reproduction

This one finite synthetic adjacent normalized proxy entry does not prove a full operator estimate, physical $h_0$ or arithmetic signs, pay arithmetic $L^2$ or fixed-power credit, close Route A/B, or imply a twin-prime result. Run the producer, replay, and mutation stress with `–check` in normal and optimized modes; Bridge-B repeats and locks these checks.

<!-- SOURCE_BODY_END -->
