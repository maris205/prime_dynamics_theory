# TPC-410: Odd Complete-Shell Height Replication

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 6, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-409 tested a locally normalized adjacent-entry proxy over four heights on one odd complete shell. We now replicate that ladder on the second odd shell, $Q=131072$, with $H=16,32,66,128$ and $N=4H$. All $10749$ shell primes are retained, giving the explicit parity counts $m_-=5374$ and $m_+=5375$. The exact local identity and Cauchy–Schwarz proof give, at every height, $0\le z\le t_1/(a_{\min}\sqrt{S_0S_1})\le4/(a_{\min}H)\le4/H$. An exact rational certificate and independent literal CRT masked-energy replay verify all four rows. This remains a finite synthetic proxy result, with no arithmetic or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Odd-shell height ladder

Fix $Q=131072$. The complete shell $(Q,2Q]$ contains $r=10749$ primes $p_0<\cdots<p_{r-1}$. For each $H\in\{16,32,66,128\}$ set $N=4H$ and choose a CRT representative above $10^6$ satisfying $$o\equiv0\pmod {p_i}\quad(i\text{ even}),\qquad
 o\equiv-N\pmod {p_i}\quad(i\text{ odd}).$$ All shell primes are retained. Thus $m_-=\lfloor r/2\rfloor=5374$ and $m_+=\lceil r/2\rceil=5375$. Define $$t_d=\frac{H^2}{H^2+d^2},\quad S_0=\sum_{d=1}^{N-1}t_d^2,
 \quad S_1=\sum_{d=1}^{N-2}t_d^2+t_1^2,
 \quad a_i=\frac{p_i^3}{Q^2(p_i-1)}.$$ For the odd/even amplitude sums $P_-,V_-,V_+$, the TPC-404 local proxy is $$G_0=V_-S_0,\qquad G_1=V_-S_1+V_+(S_1-t_1^2),\qquad M=t_1P_-.$$ The height $H$ is a proxy parameter, not the physical $h_0$.

# Finite height theorem

**Theorem.** With $a_{\min}=\min_i a_i$ and $z=M/\sqrt{G_0G_1}$, $$0\le z\le\frac{t_1}{a_{\min}\sqrt{S_0S_1}}
 \le\frac4{a_{\min}H}\le\frac4H. \tag{1}$$

**Proof.** Since $p_i>Q>N$, the even class masks offset zero and the odd class first masks offset $N$; no prime masks offset one. Hence the displayed local identities hold. Cauchy–Schwarz and the odd-class lower bound give $P_-^2\le m_-V_-$ and $V_-\ge m_-a_{\min}^2$, while $G_1\ge V_-S_1$. Consequently $$z^2\le\frac{t_1^2m_-}{V_-S_0S_1}
\le\frac{t_1^2}{a_{\min}^2S_0S_1}.$$ For $1\le d\le H$, $t_d\ge1/2$ and those terms occur in both sums, so $S_0,S_1\ge H/4$. Also $a_i=(p_i/Q)^2p_i/(p_i-1)>1$. Taking square roots proves (1). $\square$

#  Exact certificate and observations

The exact producer enumerates the full shell and uses integer CRT and rational arithmetic. The resulting finite observations are $$\begin{array}{c|r|r|r|c|c}
H&N&m_-&m_+&z&Hz\\ \hline
16&64&5374&5375&0.021789988190137&0.348639811042192\\
32&128&5374&5375&0.010811618763339&0.345971800426854\\
66&264&5374&5375&0.005218048074517&0.344391172918121\\
128&512&5374&5375&0.002684549931314&0.343622391208160
\end{array}$$ The table contains float64 observations extracted from exact rational squares; it is not an asymptotic fit. The independent checker reconstructs the sieve and CRT for each height and literally visits every per-prime, per-coordinate mask before comparing both row energies and $M$.

#  Route boundary

This is a finite four-height result for one synthetic adjacent normalized proxy entry. It is not a full normalized operator estimate, physical $h_0$ theorem, arithmetic sign or $L^2$ theorem, fixed-power saving, Route-A or Route-B closure, or twin-prime result. The exact certificate status is the exact finite odd complete-shell height replication recorded in the certificate; arithmetic advance is `NO`, fixed-power credit is $0$, and full Gate B is `OPEN`.

# Reproduction

Run the producer, independent replay, and nine-mutation stress checker with `–check` in normal and optimized Python modes. Bridge-B repeats all checks, requires empty stderr and identical output, and locks the release artifacts by SHA-256.

<!-- SOURCE_BODY_END -->
