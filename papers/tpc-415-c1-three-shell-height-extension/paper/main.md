# TPC-415: Three-Shell Height Extension

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 6, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We extend the three-shell pooled complete-shell proxy to $H=16,32,66,128$, with $N=4H$. The shells at $Q=65536,131072,262144$ retain 36848 primes, use shell-local amplitudes, and have equal pooled parity counts 18424/18424. Exact arithmetic and an independent literal replay verify all four rows. This is finite synthetic evidence, not an arithmetic theorem.

<!-- SOURCE_BODY_BEGIN -->

# Profile and bound

Let $\mathcal P$ be the increasing union of $(65536,131072]$, $(131072,262144]$, and $(262144,524288]$. For $p_i\in\mathcal P$, set $a_i=p_i^3/[Q_i^2(p_i-1)]$ using its source-shell scale. For each listed $H$, put $N=4H$ and use alternating CRT residues. All primes exceed the largest $N=512$, so $$G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.$$ The pooled count is 36848, hence $m_-=m_+=18424$. Cauchy–Schwarz and $S_0,S_1\ge H/4$ give $$0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}\le\frac4{a_{\min}H}\le\frac4H.\tag{1}$$

# Exact observations

The certificate contains all prime and source-shell labels and exact rational rows. The normalized observations at the four heights are, to seven decimal places, $0.0217692$, $0.0108013$, $0.0052131$, and $0.0026820$. The independent checker rebuilds the three sieves and literally visits every mask for every prime and coordinate before comparing $G_0$, $G_1$, and $M$.

# Scope and reproduction

This finite four-height synthetic adjacent proxy does not prove a full operator estimate, physical $h_0$ or arithmetic signs, pay arithmetic $L^2$ or fixed-power credit, close Route A/B, or imply a twin-prime result. Run the producer, replay, and stress with `–check` in normal and optimized modes; Bridge-B repeats and locks these checks.

<!-- SOURCE_BODY_END -->
