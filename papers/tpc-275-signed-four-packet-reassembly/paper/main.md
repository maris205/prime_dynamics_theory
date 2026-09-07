# Signed Four-Packet Reassembly for the Literal V59 Output

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-274 showed that the projected Frobenius estimate is valid but can be more than a factor 50 larger than the actual output energy. We retain the signs of the four source-block contributions instead. For the literal V59 operator, let $V_j=(I-P_3)A\beta^{(j)}$, let $\Gamma$ be their 4-by-4 Gram matrix, and write $D=\operatorname{tr}\Gamma$ and $G=\|\sum_jV_j\|_2^2$. We prove the exact Gram, four-point DFT, and real two-probe polarization identities. On six registered growing-cutoff scales and two kernel exponents, an exact rational replay certifies $G-D<0$ on all 12 rows, $1<D/G<12/5$, and the older Frobenius ratio $F/G>50$. The packet-diagonal margin proxy remains below $1/4$ on every row. This is a source-attached finite signed-reassembly result, not an asymptotic cross-Gram theorem or a twin-prime proof.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim ceiling

The residual route has a signed scalar $C_{\perp}$, a source norm lane $W_{\perp}$, and an output norm lane $G_{\perp}$. TPC-274 tested the cancellation-free bound $$G_{\perp}\leq \|A_{\perp}\|_F^2\|\beta\|_2^2.$$ The present paper asks the next minimal question: what happens when the relative signs of the four source blocks are retained and reassembled through their signed cross terms?

The claim ceiling is $$\texttt{PROVED\_EXACT\_FINITE}\quad+\quad
 \texttt{NUMERICALLY\_CERTIFIED\_FINITE}.$$ The finite packet-diagonal route is marked `INSUFFICIENT_SCOPED`; no finite observation is promoted to a growing theorem, and no fixed-power credit is assigned.

# Frozen literal object and packet split

For $L=N/2$, let $\beta$ be the exact source vector in the released TPC-268 engine. On the shell $Q<q\leq 2Q$, the literal matrix is $$A_{u,t}=\mathbf 1_{u\ne t}\sum_q qK_{H,s}(u-t)
 \mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 \left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right),
 \qquad K_{H,s}(h)=\left(1+(h/H)^2\right)^{-s}.$$ The masks, deleted diagonal, prime shell, and beta are unchanged from the parent. The six scale triples are $$(64,15,4),(96,20,5),(128,24,5),
 (192,32,6),(256,38,6),(384,50,7),$$ with the registered growing cutoffs $4,4,4,5,5,5$, respectively.

Let $P_3$ be the orthogonal projection onto the three declared four-block Haar contrasts and set $A_{\perp}=(I-P_3)A$. Split $\beta$ into four consecutive blocks $\beta^{(0)},\ldots,\beta^{(3)}$, padding each block by zeros in the full source coordinate space. Define $$V_j=A_{\perp}\beta^{(j)},\qquad
 \Gamma_{jk}=\langle V_j,V_k\rangle,qquad
 D=\operatorname{tr}\Gamma,qquad
 G=\left\|\sum_{j=0}^3V_j\right\|_2^2.$$ All these quantities are rational on the registered rows.

# Exact signed reassembly identities

> **Theorem: Gram expansion and polarization** For real finite packets, $$G=D+2\sum_{0\leq j<k\leq3}\Gamma_{jk},
>  \qquad
>  \Gamma_{jk}=\frac{\|V_j+V_k\|_2^2-\|V_j-V_k\|_2^2}{4}.$$

> **Proof** Expand the squared norm of the packet sum. The diagonal terms are $\operatorname{tr}\Gamma$, and symmetry pairs the off-diagonal terms. Expanding the two squared norms in the second identity cancels the diagonal terms and leaves four copies of $\langle V_j,V_k\rangle$.

> **Theorem: four-point DFT ledger** Define $$\widehat V_k=\frac12\sum_{j=0}^3 i^{-jk}V_j,\qquad 0\leq k\leq3.$$ Then $$\sum_{k=0}^3\|\widehat V_k\|_2^2=D,
>  \qquad G=4\|\widehat V_0\|_2^2.$$ For real packets, the four mode energies used in the certificate are $$E_0=G/4,\quad E_2=\|V_0-V_1+V_2-V_3\|_2^2/4,$$ $$E_1=E_3=\bigl(\|V_0-V_2\|_2^2+\|V_3-V_1\|_2^2\bigr)/4.$$

> **Proof** The normalized four-point DFT is unitary, so Parseval gives the first identity. Fourier inversion at zero gives $\sum_jV_j=2\widehat V_0$, proving the second. Separating real and imaginary parts of the modes at frequencies one and three gives the displayed real-packet formulas.

These identities keep exactly the information discarded by a columnwise Frobenius bound. They are algebraic identities, not estimates for the arithmetic source.

# Literal finite certificate

The producer reconstructs $A$, $P_3$, and every $V_j$ with rational arithmetic. It checks the unprojected multiplication against the frozen engine, computes the complete Gram matrix, verifies all six plus/minus polarization probes, and verifies DFT Parseval and the mode-zero identity. The parent TPC-274 payload is digest-locked; its decimal output lane is kept as a reference, while the matrix multiplication supplies the exact signed output.

The packet-diagonal envelope is $D$, whereas the TPC-274 envelope is $$F=\|A_{\perp}\|_F^2\|\beta\|_2^2.$$ For positive $W_{\perp}$, define the conservative diagonal proxy $$m_D^2=\frac{|C_{\perp}|^2}{W_{\perp}D}.$$ When $G<D$, it is indeed conservative: $m_D^2\leq m^2$.

| $N$ | $s$ |  lower $D/G$|  lower $F/G$|  upper $m_D^2$|   phase  |
|:---:|:---:|------------:|------------:|--------------:|:--------:|
|  64 |  1  |       1.4656|        63.25|       0.051052| negative |
|  64 |  2  |       1.1443|        51.35|       0.053711| negative |
|  96 |  1  |       1.9819|       128.83|       0.045318| negative |
| 128 |  1  |       2.3138|       237.09|       0.006735| negative |
| 192 |  2  |       1.0062|       141.75|       0.001531| negative |
| 256 |  2  |       1.0587|       247.09|       0.000032| positive |
| 384 |  1  |       1.3667|       479.52|       0.000708| negative |

: Selected exact-rational ratios and transferred interval bounds. The complete certificate has 12 rows and 72 polarization probes.

> **Theorem: registered signed packet audit** On all 12 registered rows, $$G-D<0,\qquad 1<\frac{D}{G}<\frac{12}{5},\qquad
>  \frac{F}{G}>50,\qquad m_D^2<\frac1{16}.$$ The packet Gram is symmetric, all 72 polarization probes are exact, and DFT Parseval holds on every row.

> **Proof** The exact rational values are generated from the frozen matrix and beta source. The independent checker reconstructs the matrix and projection in a separate implementation, compares every Gram entry, packet energy, signed cross sum, mode energy, and polarization probe, and recomputes the interval for $m_D^2$. The strict inequalities are applied as rational comparisons. The six rows are paired with $s=1,2$, giving 12 keys; the stored theorem counts are therefore the complete registered audit.

The net cross term is negative even though individual Gram entries have mixed signs. Thus signed reassembly materially sharpens the finite envelope from a factor above 50 to a factor below $12/5$. It does not make the diagonal envelope sufficient for a quarter-sector margin: $m_D^2<1/16$ means only that this conservative diagonal proof cannot certify $m>1/4$. The exact signed output itself is retained, so no conclusion about the actual margin is drawn from the proxy.

# Route evaluation and limits

TPC-260 supplied a generic DFT and a synthetic null-compatible completion obstruction. The new content here is different: the four packets are the actual source-block contributions of the literal V59 matrix and exact beta. The result is consequently a finite source attachment, but not a source-level cross-Gram theorem. In particular, $$\begin{gathered}
 \texttt{SOURCE\_LEVEL\_SIGNED\_CROSS\_GRAM}=\texttt{OPEN\_ASYMPTOTIC}\\
 \texttt{ARITHMETIC\_L2}=\texttt{NONE}\\
 \texttt{FIXED\_POWER\_CREDIT}=0.
 \end{gathered}$$ No finite ratio is an exponent in $N$, and the one positive phase row is retained. The strict $1/400$ endpoint payment and full Gate B remain open.

The next legitimate bridge is to turn the signed cross-Gram quantity into a source-level estimate on the registered growing cutoff, while carrying the margin loss explicitly. That is a new theorem target, not a consequence of the present finite table.

# Conclusion

The literal four-packet decomposition contains substantial cancellation that a Frobenius envelope erases: every registered row has negative net cross coupling, and the packet-diagonal envelope is at most $12/5$ times the exact signed output, versus more than 50 for the Frobenius envelope. The improvement is real and independently reproducible, but the diagonal proxy still cannot pay the quarter-margin condition on these rows. TPC-275 therefore opens the correct signed source-level question while keeping the arithmetic and asymptotic claim ceiling explicit.

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. L. Wang, “Null-Compatible Four-Packet Residual Reassembly,” TPC-260 project release, 2026. L. Wang, “A Projected Frobenius Envelope Gap for the Literal V59 Output Lane,” TPC-274 project release, 2026.

<!-- SOURCE_BODY_END -->
