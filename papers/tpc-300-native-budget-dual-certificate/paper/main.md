# Native Budget Dual Certificates:\ Exact Ridge–KKT Reciprocity and a Rational Supporting-Hyperplane Atlas

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 29 August 2026
- Source repository commit: `55240d2d7254cbf8bd7fc0b4755fa8f24254e424`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding finite native-profile study measured the source norm required to approximate signed prime-shell targets using literal Möbius cutoff profiles. We derive a target-space dual certificate for that budget frontier. If $M$ is the source Gram matrix and $V$ the physical image map, the ridge system $(V^{T}V+\rho M)c_\rho=V^{T}b$ yields, for every $\rho>0$, the lower bound $$D_\rho=\frac{\left\lVert b\right\rVert^2-R^2-b^TVc_\rho}{\rho}
 \leq \min_{\left\lVert Vc-b\right\rVert\leq R}c^TMc.$$ At an active finite frontier this is equality. We also isolate the reciprocal convention $\mu=1/\rho$ between the KKT multiplier and the ridge parameter, correcting a notation ambiguity in the preceding numerical release without changing its values. On the frozen 18-row grid, 72 twenty-digit rational ridge choices produce exact rational dual fractions; all are within the stated $0.999999999$ relative tightness floor. The result is a finite structural certificate, not an asymptotic estimate.

<!-- SOURCE_BODY_BEGIN -->

# Question and finite setting

The TPC-299 release `\cite{tpc299}` converted a finite profile-angle ladder into a native source-budget frontier. For a literal prefix $U_k$, a frozen physical shell matrix $A$, and $$V_k=A^TU_k,\qquad M_k=U_k^TU_k,$$ the normalized residual target is represented by $$B_R(b)=\min\{c^TM_kc:\left\lVert V_kc-b\right\rVert_2\leq R\}.                 \tag{1}$$ Here $R=\frac12\sqrt{|S|}$ on a shell $S$. The question in this paper is not whether (1) can be solved numerically, but whether its obstruction can be exported as a checkable target-space witness. Such a witness is useful because it separates the finite convex calculation from the choice of a primal optimizer.

All matrices in the declared fixture are rational. The source profiles are $$\beta_z(t)=\lambda(t)-\sum_{\substack{d\leq z\\d\mid t}}\mu(d),
\quad
 z\in\{3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61\}.
                                                               \tag{2}$$ The finite audit has 18 rows and 1,380 shell edges. It is deliberately restricted: no moving-shell limit or arithmetic $L^2$ statement is inferred.

# Dual formula

> **Theorem: weak native-budget dual** Let $M\succ0$, let $V$ and $b$ be finite real data, let $R\geq0$, and let $\rho>0$. Define $$(V^TV+\rho M)c_\rho=V^Tb.                                  \tag{3}$$ Then $$D_\rho=\frac{\left\lVert b\right\rVert_2^2-R^2-b^TVc_\rho}{\rho}                \tag{4}$$ is a lower bound for the value in (1), whenever (1) is feasible.

> **Proof** Set $\mu=1/\rho$ and consider $$L(c,\mu)=c^TMc+\mu\bigl(\left\lVert Vc-b\right\rVert_2^2-R^2\bigr).$$ Its quadratic part is positive definite. Its unique minimizer satisfies $$Mc+\mu V^T(Vc-b)=0,$$ which is exactly (3). Multiplying (3) by $c_\rho^T$ gives $$\inf_c L(c,\mu)
>  =\frac{\left\lVert b\right\rVert_2^2-R^2-b^TVc_\rho}{\rho}.$$ For any feasible $c$, $L(c,\mu)\leq c^TMc$; taking the infimum and then the primal minimum proves (4).

The formula is a supporting-hyperplane certificate in target space. Indeed, after whitening with $y=M^{1/2}c$ and $W=VM^{-1/2}$, the residual of the ridge point is $$e_\rho=Wy_\rho-b=-\rho(WW^T+\rho I)^{-1}b.                  \tag{5}$$ The normal vector $-e_\rho$ supports the radius-$R$ target ball when $\left\lVert e_\rho\right\rVert=R$. Thus the dual scalar is not an extra fitted statistic: it is the value of a target-space supporting functional.

> **Proposition: active strong duality** If $$\operatorname{dist}(b,\operatorname{range}V)<R<\left\lVert b\right\rVert_2$$ and $b$ has a visible component in $\operatorname{range}V$, there is a unique $\rho_\ast>0$ with $\left\lVert Vc_{\rho_\ast}-b\right\rVert_2=R$, and $$D_{\rho_\ast}=B_R(b)=c_{\rho_\ast}^TMc_{\rho_\ast}.          \tag{6}$$

> **Proof** In singular coordinates of $W$, the squared residual is $$\left\lVert b_\perp\right\rVert_2^2+
>  \sum_j\left(\frac{\rho}{\sigma_j^2+\rho}\right)^2a_j^2.$$ It is continuous, begins at the least-squares residual, and increases to $\left\lVert b\right\rVert_2^2$. The stated hypotheses give a unique crossing. At the crossing, $\mu=1/\rho_\ast$ satisfies the convex KKT conditions; Slater duality gives (6).

# The reciprocal parameter correction

There are two positive parameters in common presentations of this path. The ridge parameter $\rho$ appears in (3), while the KKT multiplier $\mu$ multiplies the squared residual constraint. Stationarity gives $$\rho=\frac1\mu.                                             \tag{7}$$ The TPC-299 producer used the matrix in (3), so its stored field `lagrange_multiplier` is numerically a ridge parameter. TPC-300 records this as a scoped notation erratum. None of the source budgets or finite obstruction counts changes. The distinction matters when comparing dual values: substituting $\rho$ where $\mu$ is required changes the stationarity equation and generally misses the active residual.

# Exact rational certificate compiler

For rational $V,M,b,R^2$ and rational $\rho>0$, equation (3) is a rational linear system. Exact Gaussian elimination over $\mathbb{Q}$ produces $c_\rho\in\mathbb{Q}^k$, and (4) is an exact rational number. The compiler therefore stores two layers:

1.  the numerator and denominator of the selected rational $\rho$;

2.  decimal enclosures for the dual budget and hashes of the exact dual fraction and coefficient vector.

The selected $\rho$ is the 20-significant-digit rational midpoint of the frozen TPC-299 ridge interval. This is not claimed to be the exact irrational optimizer; it is a weak-dual point whose exact fraction can be replayed without a floating-point optimizer. Its tightness is measured against the parent certificate’s outward presentation enclosure.

# Finite audit

The audit replays three threshold targets (weighted minimum, unit-edge max-cut, and all-positive) and the full available prefix for the weighted minimum on every row. This gives $18(3+1)=72$ cases. Table [1](main.tex#L181){reference-type="ref" reference="tab:atlas"} summarizes the claim-bearing counts.

<div id="tab:atlas">

| quantity                                  |      certified count/value|
|:------------------------------------------|--------------------------:|
| rows / shell edges                        |             $18$ / $1,380$|
| exact rational dual cases                 |                    $72/72$|
| dual/primal ratio lower bound             |  $>0.999999999$ in $72/72$|
| weighted threshold ratio $>9\cdot10^{-5}$ |                    $18/18$|
| weighted threshold ratio $>5\cdot10^{-4}$ |                    $15/18$|
| weighted threshold ratio $>10^{-3}$       |                    $14/18$|
| weighted full-prefix ratio $>10^{-3}$     |                    $11/18$|

: TPC-300 finite rational dual atlas.

</div>

The smallest recorded dual-to-parent-primal lower bound is $0.999999999999962310666478$. The exact-fraction hashes and coefficient hashes are recomputed by a producer-independent source-first checker in normal and optimized Python modes. Scalar and two-coordinate exact stress fixtures separately verify weak duality, equality at an active point, and the reciprocal correction.

# What this does and does not close

The strongest positive result is a reusable conversion $$\text{native profile prefix}
 \longrightarrow
 \text{ridge system}
 \longrightarrow
 \text{exact rational target-space dual witness}.$$ It turns the TPC-299 budget obstruction into a lower-bound certificate that does not trust the primal source coefficients as its final evidence. The strongest obstruction is unchanged but independently transported: on 14 of 18 threshold rows, and 11 of 18 full-prefix rows, the weighted target still requires more than $10^{-3}$ of the frozen source norm squared.

The finite profile family, shell grid, target tolerance, and normalization remain modeling choices. No growing profile-budget theorem, arithmetic $L^2$ estimate, fixed-power credit, full Gate B closure, or twin-prime result is claimed. The natural next test is hostile variation of tolerance and source normalization, so that the dual gap cannot be attributed to one finite convention.

# Reproducibility and claim status

The project contains the exact-fraction producer, an independent replay, an exact stress suite, a canonical JSON certificate, and a Bridge-B checker. The Session-named Route-A/Route-B evaluator files are absent from the checkout; consequently this paper reports local fail-closed validation only. The status is $$\texttt{PROVED\_EXACT\_FINITE\_NATIVE\_BUDGET\_DUALITY\_AND\_RECIPROCAL\_}$$ $$\texttt{MULTIPLIER\_CORRECTION\_PLUS\_NUMERICALLY\_CERTIFIED\_FINITE\_}$$ $$\texttt{RATIONAL\_DUAL\_WITNESS\_ATLAS}.$$

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc299,
  author       = {Liang Wang},
  title        = {Native Profile Budget Frontier},
  year         = {2026},
  note         = {TPC-299 project release in the accompanying repository}
}
```

<!-- SOURCE_BODY_END -->
