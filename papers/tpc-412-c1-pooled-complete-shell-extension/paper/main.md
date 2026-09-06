# TPC-412: Pooled Complete-Shell Extension

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 6, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

We extend the pooled odd complete-shell proxy from one height to \(H=16,32,66,128\), always with \(N=4H\). The complete shells at \(Q=65536\) and \(Q=131072\) retain all \(5709+10749=16458\) primes, use shell-local amplitudes, and have equal pooled parity counts \(m_-=m_+=8229\). Exact rational arithmetic and an independent literal replay verify all four rows. This is finite synthetic evidence, not an arithmetic or twin-prime theorem.

# Profile and theorem

Let \(\mathcal P\) be the increasing union of \((65536,131072]\) and \((131072,262144]\). For \(p_i\in\mathcal P\), let \(Q_i\) be its shell scale and set \(a_i=p_i^3/[Q_i^2(p_i-1)]\). For each listed \(H\), put \(N=4H\) and choose an origin above \(10^6\) with residues \(0\) on even indices and \(-N\) on odd ones. All primes exceed the largest \(N=512\), so the even class masks offset zero, the odd class first hits offset \(N\), and no prime masks offset one. Therefore \[G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.\] **Theorem.** For every \(H\in\{16,32,66,128\}\), \[0\le z=\frac{M}{\sqrt{G_0G_1}}\le
\frac{t_1}{a_{\min}\sqrt{S_0S_1}}\le\frac4{a_{\min}H}\le\frac4H.\tag{1}\] Indeed, \(P_-^2\le m_-V_-\), \(V_-\ge m_-a_{\min}^2\), and \(G_1\ge V_-S_1\); also \(S_0,S_1\ge H/4\) and \(a_i>1\). This proves (1).

# Exact observations

The exact pooled certificate reports \[\begin{array}{c|c|c}
H&N&z\\\hline
16&64&0.021785036050694\\
32&128&0.010809175951931\\
66&264&0.005216872683870\\
128&512&0.002683946067759
\end{array}\] The independent checker rebuilds both sieves and the CRT, then literally visits every per-prime/per-coordinate mask for both local rows at every height.

# Scope and reproduction

This finite four-height synthetic proxy does not prove a full normalized operator estimate, identify physical \(h_0\) or arithmetic signs, pay arithmetic \(L^2\) or fixed-power credit, close Route A/B, or imply a twin-prime result. Run the producer, independent replay, and mutation stress with `–check` in normal and optimized modes; Bridge-B repeats and locks these checks.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
