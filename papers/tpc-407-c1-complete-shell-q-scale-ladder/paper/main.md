# TPC-407: A Complete-Shell C1 Q-Scale Ladder

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

TPC-406 extended a locally normalized adjacent-entry bound from a small selected-prime prefix to the complete shell at one value of \(Q\). We next test its scale dependence. At fixed \(H=66\) and \(N=264\), we select every prime in complete shells at \(Q=4096,8192,16384,32768\); their counts are \(464,872,1612,3030\). The exact local identity and the same Cauchy–Schwarz argument give, at every scale, \(0\leq z\leq t_1/(a_{\min}\sqrt{S_0S_1})\leq4/(a_{\min}H)\leq4/H\). An exact rational certificate and an independent literal CRT masked-energy replay verify all four scales. The observed normalized entries remain near \(0.0052\) and \(H z\) remains near \(0.344\), but these are finite float64 observations, not an asymptotic assertion. The result concerns one synthetic proxy entry and makes no arithmetic or twin-prime claim.

# Complete-shell Q ladder

Fix \(H=66\) and \(N=264\). Let \(Q>N\) and assume that the complete shell \((Q,2Q]\) has even cardinality \(2m\), with primes \(p_0<\cdots<p_{2m-1}\). Impose the explicit congruences \[o\equiv0\pmod {p_i}\ (i\ \mathrm{even}),\qquad
 o\equiv-N\pmod {p_i}\ (i\ \mathrm{odd}),\] and choose a CRT representative above \(10^6\). Since \(p_i>Q>N\), the residues determine the masked hits in \(\{o,\ldots,o+N-1\}\).

Set \[t_d=\frac{H^2}{H^2+d^2},\quad
 S_0=\sum_{d=1}^{N-1}t_d^2,\quad
 S_1=\sum_{d=1}^{N-2}t_d^2+t_1^2,\] and \(a_i=p_i^3/[Q^2(p_i-1)]\). Define \[P_- =\sum_{i\ \mathrm{odd}}a_i,\qquad
 V_- =\sum_{i\ \mathrm{odd}}a_i^2,\qquad
 V_+ =\sum_{i\ \mathrm{even}}a_i^2.\] The complete-shell local proxy has \[G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.\] This is a finite proxy model; \(H\) is not the physical \(h_0\).

# Finite Q-scale theorem

**Theorem.** With \(a_{\min}=\min_i a_i\) and \(z=M/\sqrt{G_0G_1}\), \[0\leq z\leq\frac{t_1}{a_{\min}\sqrt{S_0S_1}}
 \leq\frac{4}{a_{\min}H}\leq\frac4H. \tag{1}\]

**Proof.** The CRT residues and \(p_i>N\) give the displayed formulas: even primes hit offset zero, odd primes first hit offset \(N\), and no prime hits offset one. Thus \(G_1\geq V_-S_1\). Cauchy–Schwarz gives \(P_-^2\leq mV_-\), while \(V_-\geq ma_{\min}^2\). Therefore \[z^2\leq\frac{t_1^2mV_-}{(V_-S_0)(V_-S_1)}
 =\frac{t_1^2m}{V_-S_0S_1}
 \leq\frac{t_1^2}{a_{\min}^2S_0S_1}. \tag{2}\] For \(1\leq d\leq H\), \(t_d\geq1/2\), and these terms occur in both sums; hence \(S_0,S_1\geq H/4\). Finally \(a_i=(p_i/Q)^2p_i/(p_i-1)>1\). Taking square roots proves (1). \(\square\)

# Exact certificate and observations

The producer fixes \(H=66,N=264\) and enumerates the complete shell at each declared \(Q\). All shell counts are even, while the next tested value \(Q=65536\) is excluded because its shell count is 5709, so it cannot satisfy the alternating \(2m\)-index profile. The certificate stores exact rational energies, the full CRT period, and the literal masks. The independent checker reconstructs the sieve and replays every masked row without importing the producer’s formulas.

| \(Q\) | shell primes |  normalized entry |           \(H z\) |
| ----: | -----------: | ----------------: | ----------------: |
|  4096 |          464 | 0.005232441353796 | 0.345341129350530 |
|  8192 |          872 | 0.005213845896508 | 0.344113829169525 |
| 16384 |         1612 | 0.005220518636918 | 0.344554230036614 |
| 32768 |         3030 | 0.005230768022488 | 0.345230689484187 |

The table is a finite numerical observation extracted from exact rational squares. It is not a fit, a growing bound, or evidence for arithmetic cancellation.

# Route boundary

TPC-407 establishes a finite complete-shell Q-scale ladder for one adjacent entry. It does not bound all entries or the complete normalized matrix, does not allow arbitrary origins or odd shell profiles, and does not identify the physical \(h_0\) or an arithmetic sign law. Consequently it pays no arithmetic \(L^2\) estimate, fixed-power \(1/400\) credit, Route A, Route B, or twin-prime conclusion.

|                                         |                          |
| :-------------------------------------- | :----------------------- |
| complete-shell Q-scale ladder           | `PROVED_EXACT_FINITE`    |
| four exact rational Q rows              | `PROVED_EXACT_FINITE`    |
| decimal Q-scale values                  | `NUMERICAL_OBSERVATION`  |
| full normalized operator theorem        | `OPEN`                   |
| arithmetic advance / fixed-power credit | `NO` / 0                 |
| Route-A / Route-B / twin-prime result   | `OPEN` / `OPEN` / `NONE` |

The next scoped question is `TEST_C1_COMPLETE_SHELL_Q_SCALE_EXTENSION`.

# Reproduction

The project contains the exact producer, independent literal replay, eight-mutation stress checker, certificate, proof package, route notes, and this PDF. Both normal and optimized Python executions are required.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
