# Phase–Radius Decoupling in a Finite V59 Residual

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-270 found a strong finite variation in an endpoint-normalized residual radius, but did not record its signed scalar phase and its two norm lanes in the same certificate. We introduce $C_{\perp}=\langle(I-P_3)w,(I-P_3)g\rangle$, $W_{\perp}=\|(I-P_3)w\|^2$, and $G_{\perp}=\|(I-P_3)g\|^2$, together with rational sixth-power coordinates $\mathsf{Xi}=(W_{\perp}G_{\perp})^3/N^{10}$, $\mathsf{Xi}_{W}=W_{\perp}^3/N^5$, $\mathsf{Xi}_{G}=G_{\perp}^3/N^5$, and $\mathsf{Xi}_{C}=|C_{\perp}|^6/N^{10}$. The exact identities $\mathsf{Xi}=\mathsf{Xi}_{W}\mathsf{Xi}_{G}$ and $\mathsf{Xi}/\mathsf{Xi}_{C}=|\kappa|^{-6}$ separate radius size, lane attribution, and phase alignment. On the registered TPC-269 finite interface, all six base rows and three matched profile controls have negative-real-axis scalar phase. Nevertheless the dyadic radius ratios have pattern DROP–RISE–RISE–DROP; the 96 to 192 ratio exceeds 23 while the source lane falls below 1/8 and the output lane rises above 230. This is a numerically certified finite phase–radius decoupling audit, not an asymptotic phase theorem, radius estimate, arithmetic $L^2$ result, or twin-prime proof.

<!-- SOURCE_BODY_BEGIN -->

# Position and claim firewall

The TPC chain studies a literal finite V59 physical operator containing the prime shell, outer $q$ weight, unit masks, deleted diagonal, source beta, registered cutoff $z_N=\lfloor\log N\rfloor$, and a rank-three four-block projection. TPC-269 added a convex path between two kernel profiles. TPC-270 then normalized the positive residual radius by the endpoint exponent $5/3$ and found a finite DROP–RISE–RISE–DROP pattern.

The status of the present paper is $$\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_PHASE\_RADIUS\_DECOUPLING\_AUDIT}.$$ The word “finite” is essential: the registered rows are a diagnostic interface, not a proved asymptotic sequence. No finite ratio is promoted to a power saving or a source-level counterexample.

# Projected residual coordinates

Let $P_3$ be the orthogonal projection onto the three declared block contrasts. On each finite row put $$C_{\perp}=\langle(I-P_3)w_N,(I-P_3)g_{N,\theta}\rangle,\qquad
 W_{\perp}=\|(I-P_3)w_N\|^2,\qquad
 G_{\perp}=\|(I-P_3)g_{N,\theta}\|^2.$$ The residual radius product and normalized signed coordinate are $$R^2=W_{\perp}G_{\perp},\qquad
 \kappa=\frac{C_{\perp}}{\sqrt{W_{\perp}G_{\perp}}}.$$ The producer certifies $W_{\perp}>0$ and $G_{\perp}>0$ on all nine rows. It also certifies that every displayed $C_{\perp}$ interval lies strictly below zero.

# Exact lane factorization

The algebraic number $N^{5/3}$ is unnecessary at finite scale. Define $$\mathsf{Xi}=\frac{(R^2)^3}{N^{10}},\qquad
 \mathsf{Xi}_{W}=\frac{W_{\perp}^3}{N^5},\qquad
 \mathsf{Xi}_{G}=\frac{G_{\perp}^3}{N^5},\qquad
 \mathsf{Xi}_{C}=\frac{|C_{\perp}|^6}{N^{10}}.$$

> **Lemma: finite identities** On every row with $W_{\perp},G_{\perp},C_{\perp}\ne0$, $$\mathsf{Xi}=\mathsf{Xi}_{W}\mathsf{Xi}_{G},
>  \qquad
>  \frac{\mathsf{Xi}}{\mathsf{Xi}_{C}}
>  =\frac{(W_{\perp}G_{\perp})^3}{|C_{\perp}|^6}=|\kappa|^{-6}.$$

Indeed, the first equality is direct multiplication and the second follows from $(\sqrt{W_{\perp}G_{\perp}}/|C_{\perp}|)^6=|\kappa|^{-6}$. Thus a radius change can be attributed to the source lane $\mathsf{Xi}_{W}$ and output lane $\mathsf{Xi}_{G}$, while the ratio to $\mathsf{Xi}_{C}$ measures phase misalignment. For positive outward intervals, cubing is monotone and division uses the lower numerator over upper denominator and vice versa. The certificate stores these outward images.

# Certified finite result

The base registry is $$(N,H,Q)=(64,15,4),(96,20,5),(128,24,5),
 (192,32,6),(256,38,6),(384,50,7).$$ The cutoff is $z_N=\lfloor\log N\rfloor$ on these rows. The four dyadic lane records are shown below; all endpoints are outward decimal enclosures.

|     pair     | $\mathsf{Xi}_{W}$ ratio | $\mathsf{Xi}_{G}$ ratio |  $\mathsf{Xi}$ ratio  |
|:------------:|:-----------------------:|:-----------------------:|:---------------------:|
|  64$\to$ 128 |  \[0.365585,0.365733\]  |  \[0.633926,0.633926\]  | \[0.231754,0.231847\] |
|  96$\to$ 192 |  \[0.103825,0.103864\]  |  \[230.7698,230.7699\]  |  \[23.9597,23.9686\]  |
| 128$\to$ 256 |  \[0.466740,0.466928\]  |   \[15.3653,15.3654\]   |  \[7.17162,7.17449\]  |
| 192$\to$ 384 |   \[1.10084,1.10125\]   |  \[0.729362,0.729363\]  | \[0.802913,0.803208\] |

: Source, output, and endpoint-normalized radius lane ratios.

> **Theorem: finite phase–radius decoupling** On the six base rows, all scalar intervals $C_{\perp}$ are strictly negative, so the phase label is negative real throughout. Simultaneously, the four dyadic radius ratios have classifications $$\text{DROP}_{<1/4},\quad \text{RISE}_{>23},\quad
>  \text{RISE}_{>7},\quad \text{DROP}_{(3/4,1)}.$$ The $96\to192$ rise is output-lane dominated: its source-lane ratio is below $1/8$ and its output-lane ratio is above $230$.

The classifications are separated from their thresholds by the stored intervals. In particular, the largest radius spike occurs while the signed phase label is unchanged. This is an attribution statement about the finite registry, not a claim that phase and radius are statistically independent.

At $N=96,128,256$, the matched $\theta=1/2$ controls preserve the negative phase and leave the source lane unchanged because $w_N$ is unchanged. Their output-lane ratios are respectively below $0.9$, while their radius ratios are enclosed in $(1/2,3/4)$. This provides a profile control for the lane interpretation.

# Interpretation and limits

The second identity in Lemma 1 explains why a small signed scalar can coexist with a large radius envelope: the phase coordinate $|\kappa|$ can be small, and the amplification factor is exactly $|\kappa|^{-6}$. The lane identity then separates two mechanisms that a radius-only table conflates. At $96\to192$, the output norm lane supplies the large factor even though the source-normalized lane decreases. At $64\to128$, both normalized lanes decrease and the radius drops below $1/4$ without a phase sign change.

Four promotions are explicitly disallowed. The six rows do not establish a uniform source-level sequence; the phase sign does not establish an eventual phase sector; the radius ratios do not prove or refute a bound $R_N\ll N^{5/3-\delta}$; and the radius product is not an arithmetic $L^2$ estimate or a signed four-packet reassembly. Accordingly the fixed-power credit is zero and full Gate B remains open.

# Conclusion

TPC-271 adds a joint coordinate system to the TPC-267–270 finite chain. The exact lane factorization and the independently audited records show a clean finite phase–radius decoupling: negative-real scalar phase persists while the normalized radius rises by more than 23, driven by the output residual lane. The next source-level task is a uniform signed-phase estimate coupled to an explicit radius-lane bound. Until that estimate is proved, no asymptotic or twin-prime conclusion follows.

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. H. L. Montgomery and R. C. Vaughan, *Multiplicative Number Theory I*, Cambridge University Press, 2007. L. Wang, “Cross-scale endpoint-normalized radius in a finite V59 residual,” TPC-270 project release, 2026.

<!-- SOURCE_BODY_END -->
