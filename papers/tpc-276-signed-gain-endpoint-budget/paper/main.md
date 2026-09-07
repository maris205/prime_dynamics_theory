# Signed-Gain Margin Recovery and the Strict Endpoint Budget

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding TPC-275 audit retained the signs of four actual source-block packets and found a finite diagonal-to-signed energy gain $r=D/G>1$. This paper proves the exact margin identity $m^2=r m_D^2$, where $m_D$ is the margin computed with the packet diagonal and $m$ is the margin computed with the signed output. A conditional endpoint compiler then shows that a uniform source-level gain $D/G\geq b x^\gamma$ contributes $\gamma/2$ to the margin budget. The strict target condition is $\sigma-\max(0,\eta_D-\gamma/2)>1/400$. Exact rational transfer of all 12 TPC-275 rows gives $r>1$ everywhere, three signed rows above the quarter margin threshold, and five above the eighth threshold. The finite table is not an asymptotic gain theorem and supplies zero fixed-power credit.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim ceiling

TPC-275 decomposed the projected literal V59 output into four actual source-block packets $V_j$, with packet diagonal energy $$D=\sum_{j=0}^3\|V_j\|_2^2,
 \qquad G=\left\|\sum_{j=0}^3V_j\right\|_2^2.$$ Its exact signed Gram audit found $G<D$ on every registered row. The present question is narrower and useful for the endpoint ledger: how does the ratio $r=D/G$ change the correlation margin, and what would a growing lower bound for $r$ actually buy?

The claim ceiling is $$\texttt{PROVED\_CONDITIONAL}\;+
 \texttt{PROVED\_EXACT\_FINITE}\;+
 \texttt{NUMERICALLY\_CERTIFIED\_FINITE}.$$ No finite ratio is promoted to a power saving, and no arithmetic $L^2$ or twin-prime conclusion is asserted.

# Exact margin recovery

Let $C_{\perp}$ be the signed residual scalar and $W_{\perp}>0$ its source norm lane. Define $$m_D^2=\frac{|C_{\perp}|^2}{W_{\perp}D},
 \qquad
 m^2=\frac{|C_{\perp}|^2}{W_{\perp}G},
 \qquad r=\frac{D}{G}.$$

> **Theorem: signed-gain margin identity** Whenever $D,G,W_{\perp}>0$, $$m^2=r\,m_D^2.$$ In particular, $r>1$ makes the diagonal margin proxy strictly conservative.

> **Proof** Since $G=D/r$, direct substitution gives $$\frac{|C_{\perp}|^2}{W_{\perp}G}
>  =\frac{|C_{\perp}|^2}{W_{\perp}(D/r)}
>  =r\frac{|C_{\perp}|^2}{W_{\perp}D}.$$ All denominators are positive, so this is an exact identity rather than an interval or square-root approximation.

# Conditional strict endpoint compiler

Write the baseline and target exponents as $$E_0=\frac53,\qquad E_*=\frac{1997}{1200},\qquad
 E_0-E_* = \frac1{400}.$$

> **Theorem: signed-gain budget** Suppose that for sufficiently large $x$, with constants $A,b,c>0$, $\gamma\geq0$, and arbitrarily small $\epsilon>0$, $$|C_{\perp}(x)|\leq A x^{E_0-\sigma+\epsilon},\qquad
>  m_D(x)\geq c x^{-\eta_D-\epsilon},\qquad
>  \frac{D(x)}{G(x)}\geq b x^\gamma.$$ Set $$\eta_{\mathrm{eff}}=\max\left(0,\eta_D-\frac\gamma2\right).$$ Then, for sufficiently large $x$, $$|C_{\perp}(x)|+R(x)
>  \leq A\left(1+\frac1{c\sqrt b}\right)
>  x^{E_0-\sigma+\eta_{\mathrm{eff}}+2\epsilon},
>  \qquad R=\frac{|C_{\perp}|}{m}.$$ Consequently the endpoint is strictly beaten if $$\sigma-\eta_{\mathrm{eff}}>\frac1{400}.$$ In the non-overcompensated regime $\gamma/2\leq\eta_D$, this is the equivalent condition $\sigma-\eta_D+\gamma/2>1/400$.

> **Proof** The identity in Theorem 1 and the two lower bounds imply $$m=m_D\sqrt{D/G}
>  \geq c\sqrt b\,x^{-\eta_D-\epsilon+\gamma/2}
>  \geq c\sqrt b\,x^{-\eta_{\mathrm{eff}}-\epsilon}.$$ Therefore $$R\leq \frac{A}{c\sqrt b}
>  x^{E_0-\sigma+\eta_{\mathrm{eff}}+2\epsilon}.$$ Because $\eta_{\mathrm{eff}}\geq0$, the assumed scalar bound is no larger than the same power after increasing the constant. Adding the two bounds proves the first claim. If $\sigma-\eta_{\mathrm{eff}}>1/400$, choose $\epsilon$ so small that $\sigma-\eta_{\mathrm{eff}}-2\epsilon>1/400$; the resulting exponent is strictly below $E_*$. The gain enters with coefficient one half because it is a squared margin identity.

# Finite signed-margin transfer

The TPC-275 certificate is the frozen source object. Its rows provide an exact rational $r=D/G$ and a positive rational interval for $m_D^2$. Multiplying that interval by $r$ gives the signed-margin interval in the table. Displayed decimals are for readability; the JSON certificate stores the rational endpoints and performs all threshold comparisons exactly.

| $N$ | $s$ |   $r=D/G$|  upper $m_D^2$|  signed $m^2$ interval| $m>1/4$? |
|:---:|:---:|---------:|--------------:|----------------------:|:--------:|
|  64 |  1  |  1.465603|       0.051052|      0.074809–0.074822|    yes   |
|  64 |  2  |  1.144371|       0.053711|      0.061451–0.061464|    no    |
|  96 |  1  |  1.981948|       0.045317|      0.089804–0.089816|    yes   |
|  96 |  2  |  1.577020|       0.052847|      0.083329–0.083341|    yes   |
| 128 |  1  |  2.313882|       0.006735|      0.015579–0.015583|    no    |
| 128 |  2  |  1.873826|       0.013418|      0.025136–0.025142|    no    |
| 192 |  1  |  1.111292|       0.000048|      0.000053–0.000053|    no    |
| 192 |  2  |  1.006248|       0.001531|      0.001539–0.001540|    no    |
| 256 |  1  |  1.161215|       0.000986|      0.001144–0.001145|    no    |
| 256 |  2  |  1.058744|       0.000032|      0.000034–0.000034|    no    |
| 384 |  1  |  1.366701|       0.000707|      0.000966–0.000967|    no    |
| 384 |  2  |  1.124747|       0.000241|      0.000270–0.000271|    no    |

: Signed recovery from the 12 exact TPC-275 rows. The quarter threshold is $m^2=1/16$; the eighth threshold is $m^2=1/64$.

> **Proposition: registered finite counts** All 12 rows have $r>1$, while the diagonal proxy is below $1/16$ on all 12 rows. Signed recovery places 3 rows above $1/16$ and 5 rows above $1/64$, with no interval crossing either threshold.

> **Proof** The producer and independent checker parse the parent rational intervals, multiply by the exact positive ratio, and compare the resulting endpoints with $1/16$ and $1/64$. The stored theorem counts are respectively $12,12,3,5,0$, and the hostile mutation audit rejects changes to each of these fields.

# Why the finite gain is not power credit

The conditional theorem requires a quantified lower bound $D/G\geq b x^\gamma$ for all sufficiently large $x$. A finite list of values at $N=64,96,128,192,256,384$ has no such quantifier: outside those points the gain can be extended by an arbitrary positive function. Thus the finite table proves a useful threshold recovery but assigns $$\texttt{TPC276\_FIXED\_POWER\_CREDIT}=0.$$ This is a scoped finite-to-asymptotic obstruction, not a negative theorem about the literal growing source. The missing result is a uniform source-level signed-gain lower bound coupled to the margin lane.

# Conclusion and route evaluation

TPC-276 adds one precise edge to the route map. Signed packet cancellation is not merely an output-energy curiosity: exactly, it multiplies the squared margin by $D/G$, and a genuine polynomial gain would enter the strict budget with half its exponent. The finite literal audit recovers the quarter margin on three rows and the eighth margin on five rows, but it does not establish a growing lower bound. Therefore the source-level signed gain, arithmetic $L^2$, full Gate B, and the twin-prime conclusion remain open.

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. L. Wang, “Signed Four-Packet Reassembly for the Literal V59 Output,” TPC-275 project release, 2026. L. Wang, “Correlation-Margin to Endpoint-Budget Compiler,” TPC-272 project release, 2026.

<!-- SOURCE_BODY_END -->
