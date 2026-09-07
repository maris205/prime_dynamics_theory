# Cross-Holdout Aggregation Order and Profile Robustness\ in a Prime-Shell Diagnostic

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 29 August 2026
- Source repository commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`
- Converter: `source-markdown-audit-v2`

## Abstract

We audit a finite common-ambient prime-shell holdout experiment under an explicit family of aggregation rules. The input is the released TPC-309 atlas: three adjacent source-backed profile windows, 18 shell cases per window, and three exclusive-completion radii. Rather than select one profile, we enumerate all 49 nonempty profile-subset/radius-subset selectors and compute 147 aggregate intervals. A pooled mean-square-error ratio, an equal-case arithmetic mean of row ratios, and an equal-case geometric mean give different finite classes. On the full selector the pooled interval is $[0.2423655855,0.3112477031]$ (right lower), while the arithmetic interval is $[5.2417686281,14.4871333704]$ (left lower); the geometric interval is $[0.1993188213,0.8609189559]$ (right lower). We prove the finite interval algebra and the identity that pooled ratios are denominator-weighted means of row ratios. The result is a scoped aggregation-order obstruction, not a causal, asymptotic, arithmetic, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and position on the route

The recent finite diagnostics separate increasingly precise sources of instability. TPC-307 introduced a common ambient operator with overlap-only fits and exclusive holdouts `\cite{tpc307}`. TPC-308 enumerated binary completion envelopes on those holdouts `\cite{tpc308}`. TPC-309 shifted a source-backed 17-coordinate profile window through a fixed 19-prime pool and found that the location of strict discordance changes with the window `\cite{tpc309}`.

The next minimal question is whether cross-holdout aggregation removes this sensitivity in a way that is independent of a hidden weighting convention. The answer matters before interpreting any finite preference as structural: a pooled loss and an equal-case ratio answer different questions. TPC-310 makes that distinction explicit and audits it exhaustively on the locked parent record.

All numerical inputs below are read from the canonical TPC-309 certificate. No labels, shell partitions, physical source rows, or completion balls are regenerated or changed.

# Finite protocol

Let $i$ index one of the 162 TPC-309 envelope observations. Its parent certificate supplies a positive ratio interval $$I_i=[\rho_i^-,\rho_i^+],\qquad
 \rho_i=\frac{\text{right holdout loss}}
                 {\text{left holdout loss}},$$ and positive extrema bounds. Write $r_i^-$ and $r_i^+$ for the lower bound of the right minimum and the upper bound of the right maximum, respectively; write $\ell_i^-$ and $\ell_i^+$ analogously for the left minimum and maximum.

The profile labels are $\mathcal L=\{\mathrm{LOW},\mathrm{BASE},
\mathrm{HIGH}\}$ and the completion radii are $\mathcal R=\{0,1,2\}$. We enumerate every pair $(L,R)$ of nonempty subsets of $\mathcal L$ and $\mathcal R$. There are $7\times7=49$ selectors. If $S(L,R)$ is the set of parent observations selected by $(L,R)$, three aggregate maps are declared: $$\begin{aligned}
 P(S)&=\left[
 \frac{\sum_{i\in S}r_i^-}{\sum_{i\in S}\ell_i^+},
 \frac{\sum_{i\in S}r_i^+}{\sum_{i\in S}\ell_i^-}\right], \label{eq:pooled}\\
 A(S)&=\left[
 \frac1{|S|}\sum_{i\in S}\rho_i^- ,
 \frac1{|S|}\sum_{i\in S}\rho_i^+\right], \label{eq:arith}\\
 G(S)&=\left[
 \exp\!\left(\frac1{|S|}\sum_{i\in S}\log\rho_i^-\right),
 \exp\!\left(\frac1{|S|}\sum_{i\in S}\log\rho_i^+\right)\right]. \label{eq:geom}\end{aligned}$$ Here $P$ aggregates losses before division, whereas $A$ and $G$ give each parent observation equal weight. An interval is classified as right lower if its upper endpoint is below $0.9$, left lower if its lower endpoint is above $1.1$, and unresolved otherwise. The budget reference used only for a finite agreement diagnostic is the strict majority of the profile-budget classes in the selected ladders; ties are unresolved.

# Finite algebra

> **Lemma: Independent finite extrema** Let $X_i$ be nonempty finite sets with extrema $x_i^-$ and $x_i^+$. If the choices $x_i\in X_i$ are independent, then $$\min\sum_i x_i=\sum_i x_i^-,\qquad
>  \max\sum_i x_i=\sum_i x_i^+.$$

> **Proof** Every summand is bounded by its corresponding endpoint, giving the two inequalities. Choosing all lower endpoints, respectively all upper endpoints, attains them.

> **Proposition: Soundness of the three maps** For every nonempty selector $S$, equations [\[eq:pooled\]](main.tex#L82){reference-type="eqref" reference="eq:pooled"}–[\[eq:geom\]](main.tex#L88){reference-type="eqref" reference="eq:geom"} are positive interval enclosures for their declared finite aggregation rules.

> **Proof** The pooled numerator and denominator extrema add by the lemma. Since all denominators are positive, quotient order reverses only in the denominator, giving [\[eq:pooled\]](main.tex#L82){reference-type="eqref" reference="eq:pooled"}. Arithmetic averaging is coordinatewise monotone. On $(0,\infty)$, both $\log$ and $\exp$ are increasing, so applying them to the two endpoint sums gives [\[eq:geom\]](main.tex#L88){reference-type="eqref" reference="eq:geom"}. The threshold classification is sound whenever an endpoint lies strictly beyond its declared threshold.

> **Proposition: Aggregation-order identity** For positive point values $a_i,b_i$ and $q_i=a_i/b_i$, $$\frac{\sum_i a_i}{\sum_i b_i}
>  =\frac{\sum_i b_iq_i}{\sum_i b_i}.
>  \label{eq:weighted}$$ Thus a pooled ratio is a $b_i$-weighted mean of row ratios, while an equal-case arithmetic ratio is an unweighted mean.

> **Proof** Substitute $a_i=b_iq_i$ and divide by the positive sum $\sum_i b_i$.

The identity does not select either map as canonical. It instead predicts that aggregation can reverse a threshold class when row denominators are correlated with row ratios. This is an analytic structure reusable beyond the present finite data.

# Results

The producer and an independent parser/replay agree on all 49 selectors and 147 aggregate rows. The inherited parent contains 54 profile cases, 162 envelope observations, and 2,106 completion-candidate evaluations.

<div id="tab:census">

| Aggregation map     |  Right|  Left|  Unresolved|
|:--------------------|------:|-----:|-----------:|
| Pooled MSE $P$      |     42|     1|           6|
| Balanced ratio $A$  |      1|    32|          16|
| Geometric ratio $G$ |     26|     0|          23|

: Class census over all 49 selectors (147 aggregate rows).

</div>

The full selector uses all three ladders and all three radii. Its intervals are shown in Table [2](main.tex#L174){reference-type="ref" reference="tab:full"}. The first two are separated from both thresholds by a wide margin, so their reversal is not a decimal-boundary effect.

<div id="tab:full">

| Map |             Interval             |    Class    |
|:----|:--------------------------------:|:-----------:|
| $P$ |  $[0.2423655855,\ 0.3112477031]$ | Right lower |
| $A$ | $[5.2417686281,\ 14.4871333704]$ |  Left lower |
| $G$ |  $[0.1993188213,\ 0.8609189559]$ | Right lower |

: Full-selector aggregate intervals.

</div>

The profile-singleton slices (all radii) give $P=$ right, right, unresolved for LOW, BASE, HIGH; $A=$ unresolved, left, unresolved; and $G=$ right, right, unresolved. The radius-singleton slices (all profiles) give $P=$ right at each radius and $A=$ left at each radius, while $G$ is right at radius zero and unresolved at radii one and two. Leave-one-ladder-out pooled slices are all right, but the HIGH-only pooled slice is unresolved and the LOW-only radius-zero slice is right while the HIGH-only radius-zero slice is left.

For a more direct comparison, the pairwise class table over the 49 selectors is:

<div id="tab:pairs">

| Pair      |  R$\mid$R|  R$\mid$L|  R$\mid$U|  L$\mid$L|  L$\mid$U|  U$\mid$U|
|:----------|---------:|---------:|---------:|---------:|---------:|---------:|
| $P\mid A$ |         1|        29|        12|         1|         0|         4|
| $P\mid G$ |        26|         0|        16|         0|         1|         6|
| $A\mid G$ |         1|        19|        13|         0|         0|        10|

: Pairwise class counts; entries are “first $\mid$ second”.

</div>

The omitted pair categories have count zero. In particular, $P$ and $A$ are oppositely strict on 29 selectors, and the full selector is one of those reversals.

# Interpretation and obstruction

The pooled result is dominated by the denominator weights implicit in the loss sum. Using interval midpoints only as a descriptive diagnostic, the full selector has a pooled ratio near $0.5072$ but an equal-case ratio near $9.8645$; the largest five left-loss weights account for about $38.1\%$ of the total weight, while the largest single radius-zero weight accounts for about $25.7\%$ of that radius slice. These midpoint summaries are not additional theorem claims; they illustrate equation [\[eq:weighted\]](main.tex#L131){reference-type="eqref" reference="eq:weighted"}.

The finite obstruction is therefore two-layered. First, TPC-309 already showed that changing a profile prefix moves local discordance. Second, cross-holdout aggregation can erase, preserve, or reverse the apparent global orientation depending on whether rows are weighted by loss scale or equally. Consequently, a statement such as “the right completion is preferred” is incomplete until the aggregation measure and its arithmetic justification are fixed before inspecting the data.

# Claim firewall and conclusion

The exact part of this paper is the selector enumeration, finite extrema rule, positive interval algebra, and weighted-mean identity. The 49-selector atlas is a numerical reproduction of padded parent intervals, not a directed-rounding certificate. Target-generation leakage inherited from TPC-302 remains explicit. We obtain no arithmetic $L^2$ estimate, no fixed-power credit, no uniform asymptotic budget, no causal identification, no full Gate B passage, and no twin-prime conclusion.

The scoped conclusion is:

> On the locked finite TPC-309 atlas, the declared pooled, equal-case arithmetic, and geometric aggregation maps do not share a universal strict class. The full-selector pooled and arithmetic classes reverse. Any future preference claim therefore requires a pre-registered weighting or stratification theorem and an independent holdout replication.

#### Reproducibility.

The canonical certificate is `results/tpc310_certificate.json`. The producer, independent checker, exact rational stress suite, and Bridge-B checker are included with this manuscript. The Session-named Route-A/Route-B evaluator files were absent from the checkout, so no official evaluator pass is asserted.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc307,
  author       = {Liang Wang},
  title        = {Common-Ambient Union-Shell Holdout in a Prime-Shell Diagnostic},
  year         = {2026},
  note         = {TPC-307 project release, Huazhong University of Science and Technology}
}

@misc{tpc308,
  author       = {Liang Wang},
  title        = {Adversarial Exclusive-Completion Envelopes for a Prime-Shell Holdout},
  year         = {2026},
  note         = {TPC-308 project release, Huazhong University of Science and Technology}
}

@misc{tpc309,
  author       = {Liang Wang},
  title        = {Profile-Prefix Shift Sensitivity in a Common-Ambient Prime-Shell Holdout},
  year         = {2026},
  note         = {TPC-309 project release, Huazhong University of Science and Technology}
}
```

<!-- SOURCE_BODY_END -->
