# TPC-403: A CRT-Origin Proxy Obstruction for the Signed Deletion Profile

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `9a2bab8588f5a81316ac3c6b6435e691e84ae8b7`

## Abstract

We give an exact adversarial construction for the finite signed coefficient model isolated in TPC-402. For alternating signs on any finite set of primes larger than the window length, the congruences \(o=0\pmod {p_{2k}}\) and \(o=-N\pmod {p_{2k+1}}\) separate the positive and negative mask profiles. Consequently the adjacent raw coefficient is \(T_1P_-\) rather than a quantity controlled by the small global scalar \(A_\sigma=P_+-P_-\). Four exact cases are certified. This is a proxy-level obstruction: no normalized growing bound, arithmetic sign identification, or twin-prime conclusion follows.

# Finite object

Let \(I_o=\{o,o+1,\ldots,o+N-1\}\) and \(T_{uv}=H^2/(H^2+(u-v)^2)\). The TPC-402 production identity for an off-diagonal pair is \[M_\sigma(u,v)=T_{uv}\bigl[-A_\sigma+b_\sigma(u)+b_\sigma(v)\bigr],
\quad A_\sigma=\sum_i\sigma_i a_i,\quad
 b_\sigma(u)=\sum_{p_i\mid u}\sigma_i a_i,\] where \(a_i=p_i^3/(Q^2(p_i-1))\). Here \(Q=8192\), \(N=1024\), and \(H=66\); the signs are the declared synthetic law \(\sigma_i=(-1)^i\).

# CRT construction

Choose distinct primes \(p_0<\cdots<p_{2m-1}\) with \(p_i>N\). Impose \[o\equiv0\pmod {p_{2k}},\qquad o\equiv-N\pmod {p_{2k+1}}. \tag{1}\] The Chinese remainder theorem gives a residue class modulo \(P=\prod_i p_i\). Adding a sufficiently large multiple of \(P\) gives \(o>B\) for every prescribed bound \(B\).

For \(0\le r<N\), an even prime divides \(o+r\) only at \(r=0\). An odd prime would first divide \(o+r\) at \(r=N\), outside \(I_o\). Thus \[b_\sigma(o)=P_+:=\sum_{i\text{ even}}a_i,\qquad
 b_\sigma(o+1)=0.\] The pair difference is \(-1\), so no selected prime divides it. The exact identity therefore gives \[M_\sigma(o,o+1)=T_1[-(P_+-P_-)+P_+]=T_1P_-,
 \quad P_-:=\sum_{i\text{ odd}}a_i. \tag{2}\] This is an exact raw-coefficient obstruction. In particular, the CRT mask profile is not determined by the global scalar \(A_\sigma\).

# Exact certificate

The producer and independent reverse-order replay use the first primes in the fixed shell \(8192<p\le16384\) and \(B=10^6\). The results are:

| \(m\) | \(2m\) primes | digits in CRT period | \(T_1P_-/|A_\sigma|\) |
| ----: | ------------: | -------------------: | --------------------: |
|     1 |             2 |                    8 |   411.130774097471742 |
|     2 |             4 |                   16 |   411.430924042908952 |
|     3 |             6 |                   24 |   514.632609073478964 |
|     4 |             8 |                   32 |   374.421682115702654 |

All CRT residues, masks, and coefficient identities are exact rational equalities. The largest case uses primes \(8209,8219,8221,8231,8233,8237,8243,8263\) and has a CRT period with 32 decimal digits. The independent checker uses reverse CRT accumulation and reverse coefficient order; both producer and checker also use a strict response-blind contract stress test.

# Scope and obstruction

The theorem is parameterized by a finite prime set and an unbounded positive origin class. It does not say that a predeclared bounded interval, including the TPC-400 origins near \(7.6\times10^6\), contains one of these CRT origins. It also does not lower-bound a locally normalized entry: the geometry denominator can absorb the raw profile. Most importantly, alternating-index signs remain a synthetic modeling choice rather than the arithmetic source sign. Therefore the route ledger is \[\begin{gathered}
\texttt{PROVED\_EXACT\_FINITE},\qquad
\texttt{ARITHMETIC\_ADVANCE=NO},\\
\texttt{FIXED\_POWER\_CREDIT=0},\qquad
\texttt{FULL\_GATE\_B=OPEN}.
\end{gathered}\]

# Reproduction

The project includes the required README, code, experiments, results, notes, proof package, and PDF. No arithmetic sign theorem or twin-prime result is claimed.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
