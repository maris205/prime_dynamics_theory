# Ky Fan Cluster Masses and the Normalization Firewall\ for a Literal Prime–Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 31 August 2026
- Source repository commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`
- Converter: `source-markdown-audit-v2`

## Abstract

We continue a finite spectral audit of a deleted-diagonal, centered prime–shell operator. The preceding audit read only its largest Gram eigenvalue and found small top gaps. Here we use the Ky Fan mass $F_k=\sum_{j\leq k}\lambda_j$ for $k\in\{1,2,4,8,16\}$ and keep both the unnormalized mass $F_k$ and the source-normalized mass $F_k/N$. On 24 rows at $X\in\{640,1280,2560\}$, with four prime shells and two kernel exponents, all 80 adjacent normalized comparisons are strictly decreasing under a dual-path finite interval audit, while all 80 unnormalized comparisons are strictly increasing. The exact identity $(F_k(2N)/(2N))/(F_k(N)/N)=\tfrac12 F_k(2N)/F_k(N)$ explains the apparent paradox: every observed unnormalized ratio lies between one and two. The result is a useful normalization firewall and a finite cluster diagnostic, not an arithmetic cancellation theorem or a twin-prime proof.

<!-- SOURCE_BODY_BEGIN -->

# Motivation and scope

The working operator is a literal finite model for a prime-shell component of the twin-prime route. Earlier finite releases successively compared a Frobenius envelope, a Schatten–4 envelope, and the top Gram eigenvalue. The last step is not automatically robust: if the top eigenvalue is close to the second one, a single eigenvector is not a canonical object. Moreover, a quantity divided by the source count can fall simply because the source count doubles.

This paper addresses exactly those two issues. We do not alter the operator, introduce a new weight law, or reassemble prime-shell signs. The contribution is a variational cluster readout together with a deliberately adversarial comparison of normalized and unnormalized scale laws.

# The frozen finite operator

For $I_X=(X/2,X]\cap\mathbb Z$, $H=66$, and $\mathcal S_Q=\{p\text{ prime}:Q<p\leq 2Q\}$, define $$K_{p,s}(u,t)=\mathbf 1_{u\ne t}\mathbf 1_{p\nmid ut}
 \frac{pH^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{u\equiv t\pmod p}-\frac{1}{p-1}\right).
 \label{eq:kernel}$$ The matrix $A=A_{Q,s,X}$ has rows indexed by $(p,u)\in\mathcal S_Q\times I_X$ and columns indexed by $t\in I_X$, with entries given by [\[eq:kernel\]](main.tex#L64){reference-type="eqref" reference="eq:kernel"}. We use the Gram matrix $G=A^*A$ and write $$\lambda_1(G)\geq\lambda_2(G)\geq\cdots\geq0,
 \qquad F_k(G)=\sum_{j=1}^k\lambda_j(G),
 \qquad M_k(G)=F_k(G)/N,$$ where $N=|I_X|=X/2$.

> **Proposition: finite Ky Fan principle** For every rank-$k$ orthogonal projection $P$, $$\operatorname{tr}(PG)\leq F_k(G),\qquad
>  F_k(G)=\max_{P^2=P=P^*,\,\operatorname{rank}P=k}\operatorname{tr}(PG).$$ In particular, $0\leq F_k(G)\leq\operatorname{tr}(G)$.

> **Proof** Diagonalize $G=U\operatorname{diag}(\lambda_1,\ldots,\lambda_N)U^*$. If $q_j=(U^*PU)_{jj}$, then $0\leq q_j\leq1$ and $\sum_jq_j=k$. Thus $\operatorname{tr}(PG)=\sum_j\lambda_jq_j\leq\sum_{j\leq k}\lambda_j$; the projection onto the first $k$ eigenvectors gives equality. Positivity gives the final bound.

# The normalization firewall

The finite scale comparison has an elementary but decisive algebraic constraint.

> **Theorem: normalization-flip identity** Suppose the source count changes from $N$ to $2N$ and $F_k(N),F_k(2N)>0$. Then $$\frac{M_k(2N)}{M_k(N)}=\frac{1}{2}\frac{F_k(2N)}{F_k(N)}.
>  \label{eq:flip}$$ Consequently, $1<F_k(2N)/F_k(N)<2$ is exactly the regime in which the unnormalized cluster mass grows while its source-normalized version decreases.

> **Proof** Substitute $M_k(N)=F_k(N)/N$ and cancel $N$.

Equation [\[eq:flip\]](main.tex#L100){reference-type="eqref" reference="eq:flip"} is not an asymptotic estimate. Its role here is to prevent a finite normalized plot from being misread as a power saving. A separate normalization law, justified by the arithmetic interface, would be needed before any such interpretation.

# Certified finite protocol

We use $X=640,1280,2560$, $Q=24,36,54,80$, and $s=1,2$, giving 24 rows. For each row the shell is accumulated in forward and reverse order. SciPy’s symmetric solver reads the top 17 eigenvalues, while a NumPy full `eigvalsh` path supplies an independent scalar spectrum. The literal entries obey the safe declared bound $|K_{p,s}(u,t)|\leq160$ on this panel. The interval construction combines solver spread, an a-posteriori residual, and the finite Weyl estimate $$\|E\|_2\leq\|E\|_F\leq N\max_{i,j}|E_{ij}|.$$ For $F_k$ the spectral term is multiplied by $k$, as required by applying Weyl to each of the $k$ eigenvalues. All claims below concern this finite declared error model.

<div id="tab:clusters">

| $k$ | gap $<.01$ |   gap range   | effective-rank range |  trend pairs  |
|:---:|:----------:|:-------------:|:--------------------:|:-------------:|
|  1  |    10/24   | .00170–.20995 |      1.000–1.000     | 16/16 + 16/16 |
|  2  |    5/24    | .00289–.35993 |      1.973–2.000     | 16/16 + 16/16 |
|  4  |    2/24    | .00451–.64886 |      3.305–4.000     | 16/16 + 16/16 |
|  8  |    4/24    | .00360–.43838 |      3.729–7.999     | 16/16 + 16/16 |
|  16 |    13/24   | .00118–.26506 |     4.132–15.965     | 16/16 + 16/16 |

: Finite cluster audit. Gap means $1-\lambda_{k+1}/\lambda_k$; effective rank is $F_k^2/\sum_{j\leq k}\lambda_j^2$.

</div>

<span id="tab:clusters" label="tab:clusters">\[tab:clusters\]</span>

# Results

For each of the five values of $k$ and each of the 16 adjacent row pairings, the normalized intervals are strictly separated in the decreasing direction. The unnormalized intervals are simultaneously strictly separated in the increasing direction. Thus the certificate contains 80 normalized decreases and 80 unnormalized increases, not merely a trend inferred from plotted point estimates. The unnormalized base-two slope ranges by $k$ are

| $k$ | $\log_2(M_k(2N)/M_k(N))$ | $\log_2(F_k(2N)/F_k(N))$ |
|:---:|:------------------------:|:------------------------:|
|  1  |    $[-.99724,-.42385]$   |     $[.00276,.57615]$    |
|  2  |    $[-.99340,-.42833]$   |     $[.00660,.57167]$    |
|  4  |    $[-.97972,-.44628]$   |     $[.02028,.55372]$    |
|  8  |    $[-.91957,-.02335]$   |     $[.08043,.97665]$    |
|  16 |    $[-.88387,-.00971]$   |     $[.11613,.99029]$    |

The two columns differ by exactly $-1$ at every transition, as predicted by Theorem 1. In particular, the smallest unnormalized increase is still positive, while the largest is below the factor two needed to overcome source normalization.

The cluster diagnostics in Table [1](main.tex#L146){reference-type="ref" reference="tab:clusters"} add a second warning. The top eigenvalue is not uniformly isolated: ten of 24 rows have a top/second gap below one percent. Enlarging the cluster does not remove all small edge gaps; at $k=16$ the count is 13/24. Effective rank varies substantially, especially for larger shells, so a fixed one-dimensional eigendirection is not a stable canonical surrogate on this panel.

# Interpretation and limitations

The strongest positive statement is variational: $F_k$ measures the maximum energy captured by a rank-$k$ subspace, and the finite certificate tracks this object over five cluster sizes. The strongest negative statement is equally precise: source-count normalization reverses the direction of every tested finite transition. This blocks credit for a growing arithmetic power saving.

Several gates remain open. The calculation does not prove a uniform law as $X\to\infty$, identify a canonical limiting spectral projector, or connect a cluster projector to signed prime-shell cancellation. It also uses the same locked finite engine rather than an external physical holdout. The Session-named Route-A/Route-B evaluator files are absent from the checkout, so this report records a local fail-closed Bridge-B assessment only. In particular, no claim about the twin-prime conjecture follows.

# Conclusion

The top-eigenvalue question is better expressed through Ky Fan cluster masses, but the resulting finite data makes the normalization issue impossible to ignore: all tested unnormalized masses grow, whereas all source-normalized masses fall. The next mathematically responsible step is to find a scale-invariant spectral measure or to prove the source normalization law before attempting any arithmetic cancellation promotion.

# References

9 Ky Fan, *Maximum properties and inequalities for the eigenvalues of completely continuous operators*, Proc. Nat. Acad. Sci. USA 37 (1951), 760–766. H. Weyl, *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen*, Math. Ann. 71 (1912), 441–479. R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013. L. Wang, *Finite Top-Eigenvalue Readout for a Literal Prime–Shell Operator*, TPC-318 project release, 2026.

<!-- SOURCE_BODY_END -->
