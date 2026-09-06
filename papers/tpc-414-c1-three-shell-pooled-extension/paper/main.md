# TPC-414: Three-Shell Pooled Extension

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 6, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

We add the complete shell at \(Q=262144\) to the pooled two-shell proxy. The three shells retain \(5709+10749+20390=36848\) primes. With shell-local amplitudes, \(H=66\), and \(N=264\), the pooled alternating CRT profile has \(m_-=m_+=18424\). Exact rational arithmetic and a fresh literal replay verify the resulting finite row; no arithmetic theorem is claimed.

# Three-shell profile

Let \(\mathcal P\) be the increasing union of \((65536,131072]\), \((131072,262144]\), and \((262144,524288]\). For \(p_i\in\mathcal P\), let \(Q_i\) be its source-shell scale and put \(a_i=p_i^3/[Q_i^2(p_i-1)]\). Set \(H=66\), \(N=264=4H\), and use CRT residues \(0\) on even indices and \(-N\) on odd indices. The pooled count is \(36848\), so \(m_-=m_+=18424\). Every prime exceeds \(N\); hence \[G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.\] Since \(P_-^2\le m_-V_-\), \(V_-\ge m_-a_{\min}^2\), \(G_1\ge V_-S_1\), and \(S_0,S_1\ge H/4\), \[0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}\le\frac4{a_{\min}H}\le\frac4H.\tag{1}\]

# Exact observation

The certificate contains all \(36848\) prime labels, their shell scales, the CRT residue and exact rational energies. Its decimal normalized observation is a finite numerical value, not an asymptotic claim. The independent checker rebuilds the three sieves and literally visits every per-prime/per-coordinate mask before comparing \(G_0\), \(G_1\), and \(M\).

# Scope and reproduction

This one finite synthetic adjacent normalized proxy entry does not prove a full operator estimate, physical \(h_0\) or arithmetic signs, pay arithmetic \(L^2\) or fixed-power credit, close Route A/B, or imply a twin-prime result. Run the producer, replay, and mutation stress with `–check` in normal and optimized modes; Bridge-B repeats and locks these checks.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
