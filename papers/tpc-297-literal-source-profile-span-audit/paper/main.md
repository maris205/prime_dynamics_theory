# A Literal Four-Direction Source-Profile Span for Finite Twin-Prime Shells

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 29 August 2026
- Source repository commit: `aa6a797b49ed462881998abf696440d164a0f74c`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-296 showed that unrestricted finite source witnesses can be cheap while the frozen source ray points in the wrong direction. We replace that ray by a source-side family that is still literal: the four cutoff profiles $\beta_z(t)=\lambda(t)-\sum_{d\leq z,\ d\mid t}\mu(d)$ for $z\in\{3,5,7,11\}$. If $A$ is the frozen physical shell matrix and $U$ contains these profiles, the restricted image is $V=A^{\mathsf T}U$. We prove the exact least-squares identity $\min_c\|Vc-b\|^2=b^{\mathsf T}(I-P_V)b$ and the monotonicity obtained by adding a source direction. Two modular replays give image rank $3$ on the three-prime row and rank $4$ on all other 17 rows of the inherited grid. A 70-digit atlas finds the all-positive target within RMS $0.15$ on all 18 rows, but the magnitude-weighted sign target remains at RMS at least $0.6$ on all 17 larger shells. This is a finite profile-dimension obstruction, not an asymptotic theorem: arithmetic $L^2$, fixed-power credit, Gate B, and the twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

# Position on the route

The finite prime-shell line has now separated three questions. TPC-294 found the physical weighted sign optimum, TPC-295 showed that every finite target has an unrestricted rational source preimage when the shell Gram is full rank, and TPC-296 quantified that unrestricted preimage cost while finding a strong obstruction for a frozen one-ray proxy `\cite{tpc295,tpc296}`. The present paper asks the smallest natural follow-up: does a few literal cutoff perturbations provide enough source geometry?

The answer is mixed. The four-direction image is genuinely richer than a ray and captures a positive control target, but it does not capture the weighted target on the larger registered shells. This narrows the next problem to a dimension or principal-angle theorem for the growing native profile, without pretending that the finite family exhausts it.

# Literal source family and physical map

For an integer $t$, define $$\lambda(t)=\begin{cases}1/k,&t=p^k\text{ for a prime }p,\\0,&\text{otherwise},\end{cases}
 \qquad
 \beta_z(t)=\lambda(t)-\sum_{\substack{d\leq z\\d\mid t}}\mu(d).$$ On the frozen interval $I=I_N$ form the rational source matrix $$U=[\beta_3\ \beta_5\ \beta_7\ \beta_{11}]\in\mathbb{Q}^{I\times4}.$$ The physical columns are inherited from the registered frozen source $\beta=\beta_{z_*}$: $$(g_q)_u=\sum_{\substack{t\in I\\t\ne u}}
 qK_{H,s}(u-t)B_q(u,t)\beta_t,
 \quad
 B_q(u,t)=\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}
 \left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right),$$ where $K_{H,s}(v)=H^{2s}/(H^2+v^2)^s$. Let $$A=[g_q]_{q\in S},\qquad V=A^{\mathsf T}U,
 \qquad S=\{q:Q<q\leq2Q\}.$$ The restricted source correlation problem is to approximate a target $b\in\mathbb{R}^S$ by $Vc=A^{\mathsf T}Uc$. All directions are chosen on the source side before seeing $b$.

> **Remark** The notation “literal” describes the finite formula and its source-side origin. It does not assert that the four cutoffs are the complete admissible V59 profile class, nor that they are stable as $N$ grows.

# Exact restricted projection theorem

> **Theorem: Restricted profile projection** For any real $A,U$ and $V=A^{\mathsf T}U$, let $P_V$ denote orthogonal projection onto $\operatorname{col}(V)$. For every target $b$, $$\min_{c}\left\lVert Vc-b\right\rVert_2^2
>  =\left\lVert (I-P_V)b\right\rVert_2^2=b^{\mathsf T}(I-P_V)b.
>  \label{eq:projection}$$ If $V$ has full column rank, then $P_V=V(V^{\mathsf T}V)^{-1}V^{\mathsf T}$.

> **Proof** The vector $P_Vb$ is the unique closest point to $b$ in the finite subspace $\operatorname{col}(V)$. For any $y\in\operatorname{col}(V)$, the vectors $P_Vb-y$ and $(I-P_V)b$ are orthogonal. Pythagoras therefore gives $$\left\lVert b-y\right\rVert_2^2=\left\lVert (I-P_V)b\right\rVert_2^2+\left\lVert P_Vb-y\right\rVert_2^2,$$ with equality at $y=P_Vb$. The inverse formula is the usual full-column-rank expression for the projection.

> **Proposition: Adding a source direction cannot hurt** If $\operatorname{col}(U_1)\subseteq\operatorname{col}(U_2)$, then $\operatorname{col}(A^{\mathsf T}U_1)\subseteq
> \operatorname{col}(A^{\mathsf T}U_2)$ and the residual in [\[eq:projection\]](main.tex#L105){reference-type="eqref" reference="eq:projection"} for $U_2$ is no larger than that for $U_1$.

> **Proof** Linear maps preserve inclusion of subspaces. The distance from a fixed vector to a larger subspace cannot increase.

For a sign target $b\in\{-1,1\}^{|S|}$, the normalized RMS reported below is $$r_U(b)=\frac{\min_c\left\lVert A^{\mathsf T}Uc-b\right\rVert_2}{\sqrt{|S|}}.$$ The theorem is exact over the reals; the finite certificate uses rational entries followed by high-precision arithmetic.

# Finite audit

The audit inherits eight growth rows, four exponent-crossover rows, and six source-control rows from TPC-295. Each physical column is accumulated exactly as a rational number. The profile-image matrix $V$ is then checked for rank modulo $1000000007$ and $998244353$. For the full-rank prefix of the four columns, a 70-digit QR solve computes the residuals for the TPC-294 weighted minimum, the unit-edge max-cut, and the all-positive target. The independent replay uses source-first accumulation and does not import the producer. Exact small fixtures test projection and nesting.

<div id="tab:headline">

| quantity                               |       count|
|:---------------------------------------|-----------:|
| literal cutoff profiles                |           4|
| rows / shell edges                     |  18 / 1,380|
| rank $3$ / rank $4$ rows               |      1 / 17|
| weighted RMS $\geq0.6$ on large shells |     17 / 17|
| all-positive RMS $\leq0.15$            |     18 / 18|
| profile no worse than frozen ray       |     18 / 18|
| fixed-power credit                     |           0|

: TPC-297 finite profile-span headline.

</div>

Table [2](main.tex#L183){reference-type="ref" reference="tab:representative"} gives representative midpoint values. The three-prime row is exactly covered because the image has full dimension three; this is a small-shell degeneracy, not evidence for a growing theorem. On the larger rows, the all-positive control is close to the four-profile image, whereas the weighted target is not.

<div id="tab:representative">

|  $N$|  $H$|  $Q$|  $s$|  $|S|$|     weighted|  all-positive|
|----:|----:|----:|----:|------:|------------:|-------------:|
|  128|   24|    9|    2|      3|  $<10^{-55}$|   $<10^{-55}$|
|  192|   32|   16|    2|      5|       0.7642|        0.0162|
|  256|   38|   27|    2|      7|       0.7051|        0.1229|
|  384|   50|   40|    2|     10|       0.9931|        0.0188|
|  512|   58|   60|    2|     13|       0.9501|        0.0205|
|  512|   58|   90|    2|     17|       0.7853|        0.0054|
|  256|   38|   27|    1|      7|       0.6265|        0.1375|
|  384|   52|   70|    2|     15|       0.8653|        0.0117|

: Representative normalized RMS residuals.

</div>

The minimum weighted residual over the 17 large-shell rows is approximately $0.6264866641$, while the largest all-positive residual is approximately $0.1374841558$. Since $\beta_5$ or $\beta_7$ is included on every registered row, the nested-span proposition explains the observed non-increase relative to the TPC-296 ray; the strict gain is not asserted on the three-prime degeneracy row.

# Interpretation and obstruction

This finite experiment changes the geometry of the route in a useful way. The one-ray negative result could have been an artifact of freezing one source direction. Four source directions remove that concern for the all-positive control: the target is almost in the restricted image on every row. They do not remove it for the weighted sign optimum. On every shell with at least five primes, a normalized distance of at least $0.6$ remains.

The distinction matters. The weighted target is selected by the physical Gram magnitudes and need not share the residue/cutoff geometry of a positive source profile. A finite rank-four result also does not say that the native profile dimension is four asymptotically. The next theorem should therefore measure principal angles or the minimum dimension needed to reduce the weighted residual, together with the source norm required by those added directions.

# Claim boundary and conclusion

The projection and nesting statements are exact. The rank and residual counts are numerically certified finite observations under a declared four-cutoff model. They do not pay arithmetic $L^2$ credit, a fixed power, or a Gate-B endpoint. In particular, this paper proves neither a positive lower bound for twin primes nor an asymptotic obstruction for all native profiles.

The reusable interface is $$\text{source profiles }U
 \longrightarrow V=A^{\mathsf T}U
 \longrightarrow P_V
 \longrightarrow \text{target residual and dimension audit}.$$ The next route question is a principal-angle/minimum-dimension audit for the weighted target, followed by a growing source-budget estimate.

# Reproducibility

From the project directory run:

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc297_literal_source_profile_span_certificate.py --check
    python -B experiments/tpc297_independent_checker.py
    python -B experiments/tpc297_profile_stress.py

The Session-named Route-A/Route-B evaluator files are absent from this checkout. The proof package, canonical certificate, independent replay, stress test, PDF audit, and Bridge-B checker are the available fail-closed validation path.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc268,
  author = {Liang Wang},
  title = {Finite Cutoff Sensitivity Obstruction in a Literal Twin-Prime Operator},
  year = {2026},
  note = {TPC-268 project record}
}
@misc{tpc295,
  author = {Liang Wang},
  title = {Source-Correlation Image Audit for Finite Prime Shells},
  year = {2026},
  note = {TPC-295 project record}
}
@misc{tpc296,
  author = {Liang Wang},
  title = {Least-Norm Source Budgets and Native-Ray Obstruction},
  year = {2026},
  note = {TPC-296 project record}
}
```

<!-- SOURCE_BODY_END -->
