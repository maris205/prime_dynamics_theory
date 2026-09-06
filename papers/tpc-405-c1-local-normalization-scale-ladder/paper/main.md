# TPC-405: An Inverse-Height Bound in the C1 Local-Normalization Proxy

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`

## Abstract

TPC-404 identified the exact local geometry of a CRT-generated signed deletion profile but tested only four finite configurations. We prove the next scoped statement: under explicit integer window and shell hypotheses, the locally normalized adjacent entry of the selected-prime CRT proxy is at most \(t_1/(a_{\min}\sqrt{S_0S_1})\leq4/(a_{\min}H)\leq4/H\). The proof is a Cauchy–Schwarz estimate combined with the two local energy identities. An exact rational certificate independently audits five heights and four multiplicities, while its decimal scale ladder is recorded only as a finite numerical observation. This is a uniform bound for one synthetic proxy entry, not a bound on the complete operator and not an arithmetic or twin-prime theorem.

# Scope and model

Let \(H,N,Q\) be integers with \(H\geq1\), \(N\geq H+2\), and \(Q>N\). Let \(p_0<\cdots<p_{2m-1}\) be distinct primes in \((Q,2Q]\), with \(m\geq1\). Choose a CRT solution \(o\) satisfying \[o\equiv0\pmod {p_i}\quad(i\ {\rm even}),\qquad
 o\equiv-N\pmod {p_i}\quad(i\ {\rm odd}).\] The origin may be chosen above any prescribed lower bound. The half-open window is \(I_o=\{o,\ldots,o+N-1\}\).

Set \[t_d=\frac{H^2}{H^2+d^2},\quad
 S_0=\sum_{d=1}^{N-1}t_d^2,\quad
 S_1=\sum_{d=1}^{N-2}t_d^2+t_1^2,\] and \(a_i=p_i^3/[Q^2(p_i-1)]\). Write \[P_-=\sum_{i\ {\rm odd}}a_i,\qquad
 V_-=\sum_{i\ {\rm odd}}a_i^2,\qquad
 V_+=\sum_{i\ {\rm even}}a_i^2.\] The local selected-prime proxy inherited from TPC-404 has \[G_0=V_-S_0,\qquad
 G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.\] Here \(H\) is the kernel height of the proxy; it is not the physical \(h_0\).

# Uniform adjacent-entry theorem

**Theorem.** Under the hypotheses above, put \(a_{\min}=\min_i a_i\) and \(z=M/\sqrt{G_0G_1}\). Then \[0\leq z\leq\frac{t_1}{a_{\min}\sqrt{S_0S_1}}
 \leq\frac{4}{a_{\min}H}\leq\frac4H. \tag{1}\]

**Proof.** Every quantity defining the amplitudes and kernel is positive. Moreover \[S_1-t_1^2=\sum_{d=1}^{N-2}t_d^2\geq0,\] so \(G_1\geq V_-S_1\). Cauchy–Schwarz and the \(m\) odd indices give \(P_-^2\leq mV_-\) and \(V_-\geq ma_{\min}^2\). Hence \[z^2=\frac{t_1^2P_-^2}{G_0G_1}
 \leq\frac{t_1^2mV_-}{(V_-S_0)(V_-S_1)}
 =\frac{t_1^2m}{V_-S_0S_1}
 \leq\frac{t_1^2}{a_{\min}^2S_0S_1}. \tag{2}\] For \(1\leq d\leq H\) we have \(t_d\geq1/2\). Since \(N\geq H+2\), these terms occur in both \(S_0\) and \(S_1\), giving \(S_0,S_1\geq H/4\). Finally, \[a_i=\left(\frac{p_i}{Q}\right)^2\frac{p_i}{p_i-1}>1\] because \(p_i>Q\). Taking square roots in (2) proves (1). \(\square\)

# Exact scale ladder

The certificate uses \(Q=8192\), the first eight primes in \((Q,2Q]\), and the five heights \(H=16,32,66,128,256\) with \(N=4H\). For every height it audits \(m=1,2,3,4\), giving 20 exact rational cases. The CRT origin is reconstructed above \(10^6\) and the independent checker recomputes the literal masked row energies, rather than importing the producer’s local formulas.

| \(H\) | \(m=1\) observation | \(m=4\) observation |
| ----: | ------------------: | ------------------: |
|    16 |   0.057270350454587 |   0.057018931354529 |
|    32 |   0.028416761665929 |   0.028292078588366 |
|    66 |   0.013715058563593 |   0.013654898530787 |
|   128 |   0.007056083219706 |   0.007025136252874 |
|   256 |   0.003523723340942 |   0.003508269858201 |

The table contains float64 square-root evaluations of exact rational normalized squares and is therefore a *NUMERICAL OBSERVATION*. It illustrates the inverse-height scale, whereas the theorem is the symbolic inequality (1).

# Route boundary

The theorem is a real extension of TPC-404, but its object is deliberately narrow. It bounds one adjacent entry of a selected-prime synthetic CRT proxy. It does not control the complete prime shell, unselected primes, arbitrary origins, the arithmetic sign source, or the physical \(h_0\). Accordingly it does not pay an arithmetic \(L^2\) estimate, fixed-power \(1/400\) credit, Route A, Route B, or a twin-prime conclusion. In particular, an upper bound for this entry is not a full operator-norm estimate.

|                                         |                          |
| :-------------------------------------- | :----------------------- |
| uniform proxy-entry bound               | `PROVED_UNIFORM`         |
| finite rational certificate             | `PROVED_EXACT_FINITE`    |
| scale-ladder decimals                   | `NUMERICAL_OBSERVATION`  |
| full normalized operator theorem        | `OPEN`                   |
| arithmetic advance / fixed-power credit | `NO` / 0                 |
| Route-A / Route-B / twin-prime result   | `OPEN` / `OPEN` / `NONE` |

The next scoped question is `TEST_C1_LOCAL_NORMALIZATION_COMPLETE_SHELL_ENTRY_BOUNDARY`.

# Reproduction

The project contains README, code, experiments, results, notes, proof package, route evaluation, and `paper/paper.pdf`. The README lists the exact producer, independent literal replay, and seven-mutation stress commands.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
