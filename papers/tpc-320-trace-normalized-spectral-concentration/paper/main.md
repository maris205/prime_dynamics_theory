# Scale-Invariant Spectral Concentration and Participation Growth\ for a Literal Prime–Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 31 August 2026
- Source repository commit: `88c46824c79e9c202a698cf4db36fcaf98260537`
- Converter: `source-markdown-audit-v2`

## Abstract

We continue a finite audit of a deleted-diagonal, centered prime–shell operator used as a structural model in a twin-prime research route. The preceding project found a normalization flip: Ky Fan masses grew before division by the source count and fell afterwards. Here we remove that bookkeeping scale by normalizing the Gram spectrum by its own trace. For $C_k=\sum_{j\leq k}\lambda_j/\operatorname{tr}(G)$ and $k\in\{1,2,4,8,16\}$, a dual-path finite enclosure on 24 rows and 80 adjacent scale transitions certifies strict decrease in every case. Stable rank and participation rank increase on all 16 adjacent row transitions as finite observations, while normalized entropy is mixed (14 increases and 2 decreases). The scalar-invariance identities are exact, but the trends are finite and do not provide signed prime-shell cancellation, an asymptotic power saving, or a twin-prime proof. The main result is therefore a scale-invariant spectral obstruction and a reusable audit protocol.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The project stays inside one literal dynamical-system family. The operator, source intervals, prime shells, height, and kernel exponents are inherited unchanged from the preceding finite audits. TPC-319 read $F_k/N$, where $N$ is the number of source columns, and established that the direction can be reversed by the factor $N\mapsto2N$. That result leaves a more intrinsic question:

> Does the shape of the Gram spectrum change when its total mass, rather than the source count, is divided out?

We answer this question only on a declared finite panel. The answer is useful precisely because it is bounded: it identifies a spectral-shape obstruction without silently turning a finite slope into an arithmetic theorem.

# Frozen operator and readouts

For $I_X=(X/2,X]\cap\mathbb Z$, $H=66$, and $\mathcal S_Q=\{p\ {\rm prime}:Q<p\leq2Q\}$, define $$K_{p,s}(u,t)=\mathbf 1_{u\ne t}\mathbf 1_{p\nmid ut}
 \frac{pH^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{u\equiv t\pmod p}-\frac{1}{p-1}\right).
 \label{eq:kernel}$$ The matrix $A=A_{Q,s,X}$ has rows indexed by $(p,u)\in
\mathcal S_Q\times I_X$ and columns indexed by $t\in I_X$. Set $G=A^*A$ and write $$\lambda_1(G)\geq\lambda_2(G)\geq\cdots\geq\lambda_N(G)\geq0,\qquad
 T(G)=\operatorname{tr}(G),\qquad F_k(G)=\sum_{j=1}^k\lambda_j(G).$$ The trace-normalized spectral distribution and its cumulative mass are $$p_j(G)=\frac{\lambda_j(G)}{T(G)},\qquad
 C_k(G)=\sum_{j=1}^k p_j(G)=\frac{F_k(G)}{T(G)}.
 \label{eq:readout}$$ The other two shape diagnostics are $$r_{\rm st}(G)=\frac{T(G)}{\lambda_1(G)},\qquad
 r_{\rm part}(G)=\frac{T(G)^2}{\operatorname{tr}(G^2)}.
 \label{eq:ranks}$$ For comparison, the old source-count readout satisfies the exact factorization $$\frac{F_k(G)}{N}=\frac{T(G)}{N}C_k(G).
 \label{eq:sourcefactor}$$

# Exact algebraic firewall

> **Proposition: finite spectral bounds** For a finite PSD Gram matrix with $T(G)>0$, $$0\leq C_k(G)\leq1,\qquad r_{\rm st}(G)\geq1,\qquad
>  r_{\rm part}(G)\geq1.$$

> **Proof** The spectral theorem gives $T=\sum_j\lambda_j$, so the $p_j$ are nonnegative and sum to one. This proves the first bound and $T\geq\lambda_1>0$ proves the stable-rank bound. Finally, $$T^2=\left(\sum_j\lambda_j\right)^2
>  =\sum_j\lambda_j^2+2\sum_{i<j}\lambda_i\lambda_j
>  \geq\sum_j\lambda_j^2=\operatorname{tr}(G^2).$$

> **Theorem: positive-scalar invariance** For every $c>0$, $$C_k(cG)=C_k(G),\qquad r_{\rm st}(cG)=r_{\rm st}(G),\qquad
>  r_{\rm part}(cG)=r_{\rm part}(G).$$ Moreover the normalized entropy $$h(G)=-\frac{1}{\log N}\sum_{j:p_j>0}p_j\log p_j$$ also satisfies $h(cG)=h(G)$.

> **Proof** The eigenvalues of $cG$ are $c\lambda_j$ and $\operatorname{tr}(cG)=c\operatorname{tr}(G)$. The numerator and denominator of $C_k$ and $r_{\rm st}$ therefore acquire the same factor $c$, while those of $r_{\rm part}$ acquire $c^2$. The probabilities $p_j$ are unchanged, which proves the entropy assertion.

> **Proposition: outward quotient enclosure** If $0\leq F^-\leq F\leq F^+$ and $0<T^-\leq T\leq T^+$, then $$\frac{F^-}{T^+}\leq\frac{F}{T}\leq\frac{F^+}{T^-}.$$

> **Proof** The quotient is increasing in its nonnegative numerator and decreasing in its positive denominator.

These identities establish what the readout removes, not what it proves. In particular, [\[eq:sourcefactor\]](main.tex#L92){reference-type="eqref" reference="eq:sourcefactor"} still contains the uncontrolled quantity $T(G)/N$, and neither factor contains the signed reassembly needed at the arithmetic endpoint.

# Finite protocol

The declared panel uses $$X\in\{640,1280,2560\},\quad Q\in\{24,36,54,80\},\quad s\in\{1,2\}.$$ Thus there are 24 rows, each with $N=X/2$ source columns. We evaluate $k\in\{1,2,4,8,16\}$ and compare the two adjacent scale changes for each $(Q,s)$, giving $4\cdot2\cdot2\cdot5=80$ comparisons.

For each row the shell is accumulated in forward and reverse order. A SciPy symmetric solver supplies the top 17 eigenvalues and a NumPy full symmetric eigensolver supplies a second path. The producer records direct and spectral trace estimates. The declared literal bound $|K_{p,s}(u,t)|\leq160$ yields an entrywise binary64 guard; Weyl’s inequality is applied to the top-$k$ sum, and the resulting mass and positive trace intervals are divided outward as in the proposition above. The independent replay rebuilds the blocks in reverse order with an einsum accumulation and uses a fresh full eigensolve. A deterministic stress suite separately tests scalar invariance, PSD trace identities, quotient endpoints, and a Weyl perturbation.

# Results

Table [1](main.tex#L187){reference-type="ref" reference="tab:concentration"} reports the finite point ranges and the certified transition census. The ratio column is the upper-scale estimate divided by the lower-scale estimate; interval separation, rather than only this point ratio, is the certified condition.

<div id="tab:concentration">

| $k$ | range of $C_k$ |  ratio range  | $\log_2$ slope range | small gaps |
|:---:|:--------------:|:-------------:|:--------------------:|:----------:|
|  1  |  .00194–.16021 | .39756–.65140 |      -1.331—.618     |    10/24   |
|  2  |  .00386–.28678 | .42874–.64938 |      -1.222—.623     |    5/24    |
|  4  |  .00764–.40849 | .47463–.63026 |      -1.075—.666     |    2/24    |
|  8  |  .01492–.43268 | .50653–.85242 |      -.981—.230      |    4/24    |
|  16 |  .02869–.45573 | .52357–.90012 |      -.934—.152      |    13/24   |

: Trace-normalized concentration audit on 24 rows. All 16 transitions are counted for each $k$; the last column is the number of rows with $1-\lambda_{k+1}/\lambda_k<0.01$.

</div>

For every $k$, every $Q$, every exponent, and both adjacent scale changes, the upper-scale interval lies strictly below the lower-scale interval. Consequently all 80 trace-normalized concentration comparisons are NUMERICALLY CERTIFIED FINITE decreases. The smallest ratio is about 0.3976 and the largest is about 0.9001, so the effect is not a numerical rounding artifact at the reported precision.

The rank diagnostics tell a compatible but not complete story: $$\begin{array}{c|c|c|c}
\text{quantity} & \text{finite range} & \text{growth transitions}
 & \text{status}\\ \hline
r_{\rm st} & 6.242\text{--}516.450 & 16/16 & \text{observation}\\
r_{\rm part} & 19.466\text{--}1088.304 & 16/16 & \text{observation}\\
h & .7881\text{--}.9883 & 14\uparrow,\ 2\downarrow & \text{mixed control}
\end{array}$$ The first two rows suggest that spectral mass spreads as the source window grows on this panel. The entropy row is an intentional adversarial control: even after trace normalization, one should not replace the whole spectral profile by a single monotone slogan.

# Interpretation and route status

The strongest positive result is structural. Trace normalization removes global amplitude exactly, and the resulting cumulative top-$k$ shares still decrease in all 80 declared comparisons. This gives a cleaner obstruction than the source-count-normalized plot: the finite trend is not explained only by doubling $N$.

The strongest negative result is equally important. The panel does not identify a limiting spectral measure. The entropy control is mixed, the edge gaps can be small, and the certificate is tied to fixed $H$, finite $Q$-anchors, and three source scales. No uniform concentration theorem, asymptotic exponent, or theorem for $T(G)/N$ is established. Most importantly, the calculation never reassembles the centered prime-shell signs into the arithmetic quantity that would control twin primes.

The Session-named Route-A and Route-B evaluator files are absent from this checkout. We therefore record a local fail-closed assessment: scoped Route-B advance for a finite scale-invariant spectral readout, with the full Gate-B arithmetic endpoint still OPEN. The exact identities are labeled `PROVED_EXACT`; interval trends are `NUMERICALLY_CERTIFIED_FINITE`; ranks and entropy are `NUMERICAL_OBSERVATIONS`; the uniform and arithmetic claims are `OPEN`.

# Conclusion

The trace-normalized spectral measure is the natural next readout after the source-count normalization firewall. On the declared literal prime-shell panel, its top-$k$ cumulative mass decreases for all five tested cluster sizes, while stable and participation ranks increase as finite observations. This is a genuine scale-invariant spectral-shape signal, but it is not yet an arithmetic bridge. The next responsible test is stability of the full spectral profile across shell choices, followed only then by any attempt at a signed projector reassembly.

# References

9 K. Fan, *Maximum properties and inequalities for the eigenvalues of completely continuous operators*, Proc. Nat. Acad. Sci. USA 37 (1951), 760–766. H. Weyl, *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen*, Math. Ann. 71 (1912), 441–479. R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013. L. Wang, *Ky Fan Cluster Masses and the Normalization Firewall for a Literal Prime–Shell Operator*, TPC-319 project release, 2026.

<!-- SOURCE_BODY_END -->
