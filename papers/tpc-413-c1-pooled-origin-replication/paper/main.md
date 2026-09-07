# TPC-413: Pooled CRT-Origin Replication

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 6, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We audit CRT-period invariance of the pooled complete-shell proxy at three distinct representatives. The full shells at $Q=65536,131072$ retain 16458 primes, and each representative is tested at $H=16,32,66,128$, $N=4H$. Exact arithmetic and a fresh literal replay verify all 12 rows. This is a finite synthetic invariance result, not an arithmetic or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Representative replication

Let $\mathcal P$ be the increasing union of $(65536,131072]$ and $(131072,262144]$. Use $a_i=p_i^3/[Q_i^2(p_i-1)]$ and alternating residues $0,-N$ in the pooled order. If $r$ is the CRT residue and $L$ its period, set $o_s=r+sL$ for $s=1,2,3$. Then $o_s\equiv r\pmod {p_i}$ for every prime. For each $H\in\{16,32,66,128\}$, all primes exceed $N=4H$ and hence $$G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.$$ The pooled cardinality is even, so $m_-=m_+=8229$. Cauchy–Schwarz and $S_0,S_1\ge H/4$ give, in every representative and height, $$0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}\le\frac4{a_{\min}H}\le\frac4H.\tag{1}$$

# Exact result

The 12 certificate rows are the Cartesian product of representatives $s=1,2,3$ and heights $16,32,66,128$. To seven decimal places, the values at these four heights are $0.0217850$, $0.0108092$, $0.0052169$, and $0.0026839$; the certificate records the full decimal strings for every representative. The independent checker rebuilds both sieves and the CRT, then literally visits every mask for each prime and coordinate in every row.

# Scope and reproduction

This finite CRT-period invariance audit does not prove a full normalized operator estimate, physical $h_0$, arithmetic signs or $L^2$, a fixed-power saving, Route A/B closure, or a twin-prime result. Run the producer, replay, and mutation stress with `–check` in normal and optimized modes; Bridge-B repeats and locks these checks.

<!-- SOURCE_BODY_END -->
