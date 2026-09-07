# A Projected Frobenius Envelope Gap for the Literal V59 Output Lane

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-273 showed that a finite correlation margin can move across quantitative bands when a declared cutoff is changed. We next test the standard cancellation-free response: apply a Frobenius norm envelope after the same three-block Haar projection. On the locked literal V59 operator, let $A_{\perp}=(I-P_3)A$, $g= A\beta$, and $G_{\perp}=\|A_{\perp}\beta\|_2^2$. We prove the exact finite inequality $G_{\perp}\leq\|A_{\perp}\|_F^2\|\beta\|_2^2=:G_F$. Exact rational construction and independent replay on six registered growing-cutoff scales and two kernel exponents certify $G_F/G_{\perp}>50$ and the envelope margin proxy $m_F^2<1/64$ on all 12 rows. This is a quantitative, scoped insufficiency of a norm-only output proof; it is not an upper bound on the actual margin, an asymptotic counterexample, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim ceiling

The residual route separates a signed scalar $C_{\perp}$ from two norm lanes. If $W_{\perp}=\|(I-P_3)w\|_2^2$ and $G_{\perp}=\|(I-P_3)g\|_2^2$, then the correlation margin is $$m^2=\frac{|C_{\perp}|^2}{W_{\perp}G_{\perp}}.$$ TPC-272 converted a signed saving and a margin loss into an endpoint budget; TPC-273 then demonstrated finite cutoff sensitivity. The present paper asks whether a simple output estimate can pay that missing margin cost.

Our claim ceiling is $$\texttt{PROVED\_EXACT\_FINITE} \quad+\quad
\texttt{NUMERICALLY\_CERTIFIED\_FINITE},$$ with a scoped ‘`INSUFFICIENT_SCOPED`‘ verdict for the tested cancellation-free route. No fixed-power credit is assigned.

# The locked finite operator

For a physical scale $N$, put $L=N/2$, and let $\beta$ be the exact source vector supplied by the released TPC-268 engine. On the prime shell $Q<q\leq 2Q$, its literal matrix is $$A_{u,t}=\mathbf 1_{u\ne t}\sum_q qK_{H,s}(u-t)
 \mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 \left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right),$$ where $K_{H,s}(h)=(1+(h/H)^2)^{-s}$. The diagonal deletion, unit masks, prime shell, beta, and four consecutive blocks are frozen; only the registered kernel exponent $s\in\{1,2\}$ is paired as a control.

The six growing-cutoff rows are $$(N,H,Q)=(64,15,4),(96,20,5),(128,24,5),
 (192,32,6),(256,38,6),(384,50,7),$$ with comparison cutoff $z_N=4,4,4,5,5,5$, respectively. Let $P_3$ denote the orthogonal projection onto the three declared four-block Haar contrasts and set $$A_{\perp}=(I-P_3)A,\qquad g_{\perp}=A_{\perp}\beta,qquad
 G_{\perp}=\|g_{\perp}\|_2^2.$$ All entries of $A$, $P_3$, and $\beta$ are rational on these rows.

# The projected Frobenius theorem

> **Theorem: projected Frobenius envelope** For every finite real or complex matrix $B$ and vector $v$, $$\|Bv\|_2^2\leq \|B\|_F^2\|v\|_2^2.$$ Consequently, on every registered row, $$G_{\perp}\leq G_F:=\|A_{\perp}\|_F^2\|\beta\|_2^2.$$

> **Proof** For each row $i$, Cauchy–Schwarz gives $$\left|\sum_jB_{ij}v_j\right|^2
>  \leq\left(\sum_j|B_{ij}|^2\right)\left(\sum_j|v_j|^2\right).$$ Summing over $i$ yields the first inequality. Substitution of $B=A_{\perp}$ and $v=\beta$ gives the second. In particular, the theorem does not use an independence or probabilistic assumption; its cost is that it discards cancellation between the columns of $A_{\perp}$.

For positive finite lanes define the conservative proxy $$m_F^2=\frac{|C_{\perp}|^2}{W_{\perp}G_F}.$$ The theorem implies $m_F^2\leq m^2$. Thus a small $m_F$ is not a counterexample to a large actual margin: it only says that this envelope cannot certify one.

# Exact finite audit

The producer constructs every matrix entry and projection coefficient as a ‘`Fraction`‘. It checks $A\beta=g$ against the parent engine, computes $\|A_{\perp}\|_F^2$, $\|\beta\|_2^2$, and $G_F$ exactly, and transfers only the parent outward intervals for $C_{\perp}$, $W_{\perp}$, and $G_{\perp}$. A separate checker repeats the matrix construction without importing the producer. A five-mutation stress audit rejects altered theorem counts, envelope values, threshold metadata, operator status, and fixed-power credit.

| $N$ | $s$ | $z_N$ |  lower gap $G_F/G_{\perp}$|  upper $m_F^2$|   phase  |
|:---:|:---:|:-----:|--------------------------:|--------------:|:--------:|
|  64 |  1  |   4   |                      63.25|       0.001183| negative |
|  64 |  2  |   4   |                      51.35|       0.001197| negative |
|  96 |  1  |   4   |                     128.83|       0.000698| negative |
| 128 |  1  |   4   |                     237.09|       0.000066| negative |
| 192 |  1  |   5   |                     174.15|       0.000001| negative |
| 256 |  2  |   5   |                     247.09|       0.000001| positive |
| 384 |  1  |   5   |                     479.52|       0.000003| negative |

: Selected outward finite bounds. The complete certificate has 12 rows; displayed decimals are only for readability.

> **Theorem: registered finite gap** On all 12 rows, the exact envelope satisfies $G_F/G_{\perp}>50$ and the transferred conservative proxy satisfies $m_F^2<1/64$. The phase intervals are separated from zero: 11 are on the negative real axis and one is on the positive real axis.

> **Proof** The six scale rows are paired with $s=1,2$, giving 12 distinct keys. The certificate stores the exact rational Frobenius energy and beta energy, then divides the resulting exact $G_F$ by the parent outward interval for $G_{\perp}$. It also divides the squared scalar interval by the positive $W_{\perp}$ interval and exact $G_F$. The lower and upper endpoints pass the strict thresholds on every row. Independent reconstruction reproduces all exact fields and interval transfers. The phase count is a direct sign count of the stored scalar intervals.

The gap is not a claim about a limiting sequence. It is a finite diagnostic that the rowwise norm envelope can be much looser than the actual output for the locked source. The exponent control is similarly descriptive: the six envelope ratios for the transition $s=1\to2$ range from about $0.62$ to $0.63$, while the actual output ratios remain distinct, so the envelope does not reproduce the source cancellation.

# Route evaluation and limits

The exact inequality is a reusable structural lemma, and the finite gap is a new numerical certificate. Its negative conclusion is deliberately narrow: the cancellation-free projected Frobenius route is insufficient on the registered interface. It does not refute a signed estimate using the actual coefficient phases. In particular, the following gates remain open: $$\begin{gathered}
 \texttt{SOURCE\_LEVEL\_OUTPUT\_BOUND}=\texttt{OPEN\_ASYMPTOTIC}\\
 \texttt{SIGNED\_FOUR\_PACKET\_REASSEMBLY}=\texttt{OPEN}\\
 \texttt{ARITHMETIC\_L2}=\texttt{NONE}.
 \end{gathered}$$ The finite rows also contain one positive phase, which is retained rather than removed by a sign convention. No row count is converted into a power saving, and the required strict $1/400$ endpoint payment remains unpaid.

# Conclusion

TPC-274 closes one low-cost proof attempt: after the physical projection, a valid Frobenius envelope loses more than a factor of 50 on every registered row and yields a margin proxy below $1/8$ everywhere. The natural next question is signed output reassembly, where the coefficient phases are kept instead of discarded. That question is not answered here; the present result is a finite, reproducible obstruction to the norm-only shortcut.

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. L. Wang, “Finite Cutoff-Sensitivity Obstruction for a V59 Residual,” TPC-268 project release, 2026. L. Wang, “A Finite Margin-Stability Matrix for the Literal V59 Residual,” TPC-273 project release, 2026.

<!-- SOURCE_BODY_END -->
