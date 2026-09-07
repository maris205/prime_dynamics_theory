# Adaptive Shell Weighting and the\ Nonnegative Coherence Wall in a Literal Twin-Prime Dynamics

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 28 August 2026
- Source repository commit: `7bba57e68d04514ee33ab2192a507a1f4edfebab`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-289 found a finite late-shell block whose physical prime-component vectors have positive and quantitatively large cross-Gram terms, together with three early sign-flip pairs. We study the natural adaptive response: can nonnegative shell weights create energy decay? For vectors $g_q$ with Gram matrix $G$ and diagonal $d_q$, we introduce $$R(w)=\frac{\left\lVert \sum_q w_qg_q\right\rVert^2}{\sum_qw_q^2d_q},
 \qquad \kappa(w)=\frac{(\sum_qw_q)^2}{\sum_qw_q^2}.$$ We prove exactly that nonnegative weights cannot give $R(w)<1$ when all off-diagonal Gram entries are nonnegative. Under a positive coherence floor and diagonal balance we prove the sharper effective-support bound $R(w)\ge 1+\eta\delta(\kappa(w)-1)$. An exact-rational replay of the TPC-289 18-row grid tests uniform, inverse-diagonal, and linear-taper full-support policies, every equal two-prime support, and every leave-one-out support. All 54 full-support policy rows and all 18 leave-one-out minima are amplified. Exactly three subunit equal-pair witnesses occur, all in the one early sign-flip row. Thus positive diffuse adaptation remains behind the coherence wall; the only finite nonnegative escape is sparse concentration on a sign-flip pair. This is a structural obstruction, not an asymptotic weighted theorem or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Route position and question

We keep one literal prime-shell dynamical family throughout. TPC-288 lifted scalar cancellation to the physical output Gram and showed finite full-rank energy amplification `\cite{tpc288}`. TPC-289 then proved a conditional coherence accumulation bound and found an eight-row late positive block, but also found three negative pairs at the $(N,H,Q,z,s)=(256,38,27,5,1)$ crossover. The inherited coherence phase diagram is recorded in TPC-289 `\cite{tpc289}`.

The phrase “adaptive weighting” hides two different possibilities. A diffuse nonnegative reweighting preserves the physical sign cone, whereas a sparse rule may select an exceptional negative pair. The purpose of this paper is to separate these mechanisms with an exact weighted Gram identity and a finite certificate. We do not alter the source, kernel, deletion rule, or prime shell inherited from TPC-289.

# Frozen physical model

Let $I=I_N$ be the frozen integer interval and let $\beta$ be its rational source vector. For an odd prime $q$, write $$K_{H,s}(h)=\frac{H^{2s}}{(H^2+h^2)^s},\qquad
 B_q(u,t)=\mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 \left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right).$$ The deleted-diagonal component is $$(A_q)_{u,t}=qK_{H,s}(u-t)\mathbf 1_{u\ne t}B_q(u,t),
 \qquad g_q=A_q\beta.$$ For a shell $S$, set $$G_{q,r}=\langle g_q,g_r\rangle,\qquad d_q=G_{q,q}=\left\lVert g_q\right\rVert^2.$$ The finite computations have $d_q>0$. The unweighted physical ratio from the preceding release is $\left\lVert \sum_qg_q\right\rVert^2/\sum_qd_q$.

# Weighted Gram lemmas

> **Lemma: Weighted identity** For every nonzero $w\in\mathbb R^S$, $$R(w)=1+\frac{2\sum_{q<r}w_qw_rG_{q,r}}
>  {\sum_qw_q^2d_q}.
>  \label{eq:weighted}$$

> **Proof** Expand $\left\lVert \sum_qw_qg_q\right\rVert^2=w^TGw$. The diagonal part is the positive denominator and the off-diagonal terms occur twice by symmetry.

> **Proposition: Nonnegative coherence wall** If $w_q\ge0$ and $G_{q,r}\ge0$ for every distinct pair, then $R(w)\ge1$. If at least one pair has $w_qw_rG_{q,r}>0$, the inequality is strict.

> **Proof** Every summand in the numerator of the correction term in [\[eq:weighted\]](main.tex#L94){reference-type="eqref" reference="eq:weighted"} is nonnegative, and its denominator is positive.

> **Proposition: Effective-support accumulation** Suppose $w_q\ge0$, $G_{q,r}\ge\eta\sqrt{d_qd_r}$ for $q\ne r$, and $d_{\min}/d_{\max}\ge\delta$, with $\eta,\delta\ge0$. Then $$R(w)\ge1+\eta\delta\bigl(\kappa(w)-1\bigr),qquad
>  \kappa(w)=\frac{(\sum_qw_q)^2}{\sum_qw_q^2}.
>  \label{eq:effective}$$

> **Proof** The hypotheses give $G_{q,r}\ge\eta d_{\min}$. Hence the correction in [\[eq:weighted\]](main.tex#L94){reference-type="eqref" reference="eq:weighted"} is at least $$\frac{2\eta d_{\min}\sum_{q<r}w_qw_r}
>  {d_{\max}\sum_qw_q^2}.$$ Use $2\sum_{q<r}w_qw_r=(\sum_qw_q)^2-\sum_qw_q^2$ and the diagonal ratio.

> **Lemma: Equal-pair probe** For weights supported equally on $i,j$, $$R_{i,j}=1+\frac{2G_{i,j}}{d_i+d_j}.
>  \label{eq:pair}$$ Thus a negative cross term is an explicit nonnegative subunit witness.

> **Proof** Substitute $w_i=w_j=1$ and all other coordinates zero in [\[eq:weighted\]](main.tex#L94){reference-type="eqref" reference="eq:weighted"}.

For uniform weights, $\kappa(w)=|S|$, so [\[eq:effective\]](main.tex#L119){reference-type="eqref" reference="eq:effective"} recovers the TPC-289 lower bound. The new parameter records the cost of concentration: it is one for a single component and at most $|S|$ for nonnegative weights.

# Finite protocol

The certificate replays eight $s=2$ growth anchors, four $s=1$ crossover rows, and six $s=2$ source controls, for 18 rows and 1,380 unordered Gram pairs. All arithmetic is rational ‘Fraction‘ arithmetic. The three full-support policies are $$w_q=1,\qquad w_q=d_q^{-1},\qquad w_q=2Q-q,$$ respectively called uniform, inverse-diagonal, and linear taper. Scaling a weight vector does not change $R(w)$. In addition, the certificate evaluates the equal-pair ratio [\[eq:pair\]](main.tex#L137){reference-type="eqref" reference="eq:pair"} for every pair and the uniform ratio after omitting each one prime.

The positive-block thresholds are the inherited finite values $\eta=3/5$, $\delta=4/5$. The producer locks the TPC-289 code and result and the TPC-268 engine by normalized-LF SHA-256. A reverse-order independent replay reconstructs the rows without importing the producer. A ten-case mutation audit and normal/optimized byte-identical checks complete the local fail-closed validation.

# Results

<div id="tab:policies">

| axis    |  $N$|  $H$|  $Q$|  $s$|  $k$|     $R(1)$|  $R(d^{-1})$|  $R(2Q-q)$|
|:--------|----:|----:|----:|----:|----:|----------:|------------:|----------:|
| growth  |  128|   24|    9|    2|    3|   2.124905|     2.117289|   1.751140|
| growth  |  192|   32|   16|    2|    5|   3.443701|     3.435108|   2.517680|
| growth  |  256|   38|   27|    2|    7|   2.622578|     2.753184|   2.054584|
| growth  |  512|   58|   60|    2|   13|  10.992677|    10.967816|   8.115423|
| growth  |  512|   58|   90|    2|   17|  16.439313|    16.422993|  12.172859|
| cross   |  256|   38|   27|    1|    7|   2.166576|     2.163534|   1.903891|
| cross   |  512|   58|   70|    1|   15|   8.900964|     8.916827|   6.009915|
| control |  384|   48|   70|    2|   15|  14.322934|    14.297999|  10.463816|
| control |  384|   52|   70|    2|   15|  14.107249|    14.075231|  10.228418|

: Representative exact-rational rows; decimals are display only.

</div>

All 54 full-support policy rows are amplified, including the exceptional crossover row. All 18 leave-one-out minima are also greater than one. The equal-pair scan is different: exactly three subunit records occur, namely the pairs $(29,53)$, $(31,53)$, and $(41,53)$ in the exceptional row. The minimum is $$R_{29,53}\approx0.8975237303.$$ These are nonnegative weights, but they have effective support two and do not represent the full physical shell. The other 17 rows have no subunit equal-pair probe. The eight TPC-289 strong-block rows satisfy the conditional bound [\[eq:effective\]](main.tex#L119){reference-type="eqref" reference="eq:effective"} for every one of the three policies.

# Interpretation and claim firewall

The exact theorem closes a tempting local escape: on an all-positive Gram block, changing positive coefficients cannot manufacture cancellation. The finite scan refines this statement rather than universalizing it. An early sign flip permits sparse nonnegative cancellation, while the full-support policies and leave-one-out tests remain amplified. In route-map language, adaptive weighting has split into a positive diffuse branch and a sparse exception branch.

The following claims are deliberately not made:

-   no theorem is asserted for a growing shell or every admissible source;

-   the three policies are not an optimization over all weighting rules;

-   the sparse witnesses are not a full-shell $L^2$ saving;

-   no arithmetic $L^2$ estimate, fixed-power credit, Gate-B conclusion, or twin-prime conclusion follows.

The next minimal attack is signed two-prime Schur cancellation, which can measure exactly how much cancellation a high-coherence pair offers and what sign cost it incurs. A complementary route is to seek a source restriction that makes the positive diffuse block stable.

# Reproducibility

The project README, proof package, canonical JSON certificate, independent replay, stress audit, and Bridge-B checker are included with the source. The Session-named Route-A/Route-B evaluator files are absent from this checkout; no official evaluator pass is claimed. The local status is

    EXACT: weighted Gram identity; nonnegative coherence wall
    CONDITIONAL: effective-support accumulation bound
    FINITE: 54/54 full-support policies amplified; 18/18 drop-one amplified
    FINITE: 3 sparse equal-pair subunit witnesses in one sign-flip row
    OPEN: growing diffuse weighted theorem and arithmetic L2
    NONE: twin-prime conclusion

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc289,
  author       = {Liang Wang},
  title        = {Cross-Prime Gram Coherence in a Literal Twin-Prime Dynamics},
  year         = {2026},
  note         = {TPC-289 project release in the same research repository}
}

@misc{tpc288,
  author       = {Liang Wang},
  title        = {Growing-Shell Gram Obstruction},
  year         = {2026},
  note         = {TPC-288 project release in the same research repository}
}
```

<!-- SOURCE_BODY_END -->
