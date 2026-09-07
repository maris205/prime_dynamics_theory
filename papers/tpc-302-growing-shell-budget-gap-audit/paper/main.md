# Source-First Growing-Shell Stability of the Native Weighted/Positive Budget Gap

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

The preceding finite native-profile audit found a robust budget separation between a signed weighted target and an all-positive control, but its target labels were available on only 18 inherited rows. We extend the hostile test to the 34-row growing/control grid of the prime-shell dynamical model and recompute the weighted target from the physical output Gram matrix on every row. The finite Gram and sign-enumeration identities are exact. At relative RMS tolerances $1/4$, $1/2$, and $3/4$, the common-prefix weighted/positive budget gap exceeds $10$ on all 34 rows; its minima are $85.3204$, $38.2187$, and $39.2637$. The common weighted budget exceeds $10^{-5}$ in all 102 row–tolerance cases under each of three source normalizations. This is a source-first finite growing-grid certificate. It does not prove uniform profile-budget growth, arithmetic $L^2$, or the twin-prime conjecture.

<!-- SOURCE_BODY_BEGIN -->

# Question and finite model

TPC-301 showed that a finite native obstruction survives a tolerance ladder, a common-prefix comparison, and three source normalizations `\cite{tpc301}`. The unresolved question was whether that obstruction depended on the inherited 18-row target atlas. Here the target itself is regenerated on the complete TPC-288 growth/control grid.

Let $S$ be a finite prime shell and let $g_q$ be the exact literal physical output vector attached to $q\in S$. Put $$G_{q,r}=\langle g_q,g_r\rangle,\qquad
 R(a)=\frac{a^TGa}{\operatorname{tr}G},\quad a_q\in\{\pm1\}.$$ The weighted target $a_w$ is the exact minimizer of $R$ after fixing one global sign; the positive control is $a_+=(1,\ldots,1)$. The source profiles are the first 17 literal cutoff profiles $$u_z(t)=\lambda(t)-\sum_{d\le z,\ d\mid t}\mu(d),
 \quad z=3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61.$$

For the first $k$ profiles, write $V_k=A^TU_k$ and $M_k=U_k^TU_k$. We use the relative target budget $$B_{k,\tau}(b)=\min\{c^TM_kc:\left\lVert V_kc-b\right\rVert_2\leq\tau\left\lVert b\right\rVert_2\}.
 \tag{1}$$ The grid has 16 growth-path rows and 18 source-control rows. Their shell lists contain 430 explicit targets. The parent metadata also contains a 1,380-edge count for a different inherited census; we keep the two numbers separate.

# Exact finite identities

> **Proposition: Gram identity and global signs** For every finite shell, $G$ is positive semidefinite and $R(a)=R(-a)$. Fixing the first sign to $+1$ therefore represents every global-sign class.

> **Proof** For any coefficient vector $c$, $$c^TGc=\sum_{q,r}c_qc_r\langle g_q,g_r\rangle
>        =\left\|\sum_qc_qg_q\right\|_2^2\geq0.$$ The quadratic form contains each sign twice, so replacing every sign by its negative leaves it unchanged.

> **Proposition: Finite enumeration** After clearing a common positive denominator, a reflected Gray traversal of the $2^{|S|-1}$ tail bit strings gives the exact minimum of $R$ on the equal-sign domain.

> **Proof** The traversal flips one tail coordinate at a time and visits every tail bit string once. The incremental quadratic update is an algebraic rearrangement of the direct integer quadratic form, so no floating-point comparison is used in selecting the minimum.

> **Proposition: Budget monotonicity and normalization** Relaxing $\tau$ or enlarging a profile prefix cannot increase (1). At a common prefix, a positive target-independent source normalizer cancels from the weighted/positive budget ratio.

> **Proof** Both statements follow by inclusion of feasible sets. For normalization, divide both numerator and denominator by the same positive scalar.

# Source-first audit

For every row we rebuild the source weights and all physical output vectors with rational arithmetic, form $G$, and enumerate $2^{|S|-1}$ sign classes. The resulting $a_w$ is then inserted into (1), alongside $a_+$. At each $\tau\in\{1/4,1/2,3/4\}$ we retain three contexts: the smallest common feasible prefix, target-specific first feasible prefixes, and the full prefix. The primary comparison is the common-prefix ratio. The source normalizers are $\left\lVert \beta\right\rVert_2^2$, $\operatorname{tr}(M_k)/k$, and $M_k[1,1]$.

The frontier is solved by 60-digit ridge-parameter bisection. Decimal intervals are written outward; exact rational labels and ratios are retained in the canonical certificate. An independent checker rebuilds all 34 Gram matrices without importing this producer.

# Results

| relative RMS $\tau$ |  common prefix|    full prefix|  common $>10$|
|:--------------------|--------------:|--------------:|-------------:|
| $1/4$               |  85.3203517096|  85.3203517096|       $34/34$|
| $1/2$               |  38.2186652435|  38.2186652435|       $34/34$|
| $3/4$               |  39.2637006403|  26.0731501545|       $34/34$|

: Minimum weighted/positive budget gap over the 34 rows.

All 34 source-first weighted ratios are below one and all 34 positive ratios are above one. The common weighted budget is above $10^{-5}$ in $102/102$ cases for each source normalizer. The common-prefix normalization identity is replayed in 102 cases, and full-prefix tolerance monotonicity in 68 target–row checks. These counts include the declared source controls and do not mean that all admissible profiles or shells have been tested.

The finite result is stronger than a mere reuse of the old target atlas: the 17-prime endpoint row, for example, is assigned its label by enumerating all $2^{16}$ global-sign classes on its own physical Gram matrix. The result is still only a stability map. In particular, the displayed minima do not constitute a lower bound uniform in shell size, source scale, or profile cutoff.

# Claim firewall and next question

The exact claims are finite Gram positivity, global-sign reduction, exhaustive enumeration, budget monotonicity, and normalization cancellation. The atlas claims only the 34 declared rows, 430 explicit shell targets, 17 profiles, three tolerances, and two target classes. A uniform native profile-budget theorem and literal arithmetic $L^2$ estimate remain open; the fixed-power credit is zero and no full Gate-B or twin-prime result is claimed. The natural next project is to test whether the native budget has a uniform growth law, or to construct the first growing-shell counterexample.

# Reproducibility

The repository contains the canonical certificate, an independent source-first replay, exact theorem stress fixtures, and a fail-closed local Bridge-B checker. The Session-named Route-A/Route-B evaluator files are not present in this checkout, so no official evaluator pass is asserted.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc301,
  author = {Liang Wang},
  title = {Tolerance and Source-Normalization Robustness of the Native Budget Gap},
  year = {2026},
  note = {TPC-301 project release in the accompanying repository}
}
```

<!-- SOURCE_BODY_END -->
