# **A Finite-Window Lower Frame Obstruction\ for Primitive Rational Frequencies**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: Aug 24 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We prove a lower-frame obstruction for finite exponential sums on primitive rational frequencies. Let $I$ be any interval of $N$ consecutive integers, set $L=\lfloor(N+1)/2\rfloor$, and let $z_{h,a}$ be supported on distinct reduced fractions $a/h\pmod 1$ with $h\leq U$. A translated triangular minorant of $1_I$, primitive Farey spacing, Fejér-kernel decay, and a circular packing estimate give $$\sum_{n\in I}\left|\sum_{h,a}z_{h,a}\mathrm{e}(na/h)\right|^2
\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_{+}\sum_{h,a}|z_{h,a}|^2.$$ Consequently, the normalized lower-frame constant is at least $\left[1/2-\pi^2U^4/(6N^2)\right]_{+}$. In the V59 regime $U=x^{133/400}$, $N\asymp x$, its defect is $x^{-67/100+o(1)}$; hence the constant is $1/2-o(1)$. This proves a scoped structural obstruction: after all $q$-variables have been collapsed into one coefficient at each reduced frequency, interference between distinct frequencies cannot supply a fixed-power saving relative to the collapsed coefficient energy. The theorem does not address cancellation inside a $q$-bucket, the literal signed construction of $C_h$, or the signed four-packet projection.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Finite-window reassembly often turns arithmetic packet estimates into an exponential sum whose frequencies are reduced rational points. Once the prime variable $q$ has been collapsed, the remaining question is geometric: can coefficients placed at distinct primitive fractions cancel strongly on a long interval? Upper-frame estimates of large-sieve type are classical; see, for example, `\cite{montgomery1994ten}`. The present paper requires the reverse direction for a separated finite family.

We give a uniform lower bound with an explicit defect. The proof inserts a translated triangular window below the hard interval. Its Fourier transform is a Fejér kernel, so the weighted Gram matrix has diagonal $L$ and nonnegative off-diagonal magnitudes. Reduced fractions of height at most $U$ are $U^{-2}$-separated. Fejér decay and a one-dimensional circular packing argument then bound the entire off-diagonal row by $\pi^2U^4/(12L)$.

The paper makes three falsifiable contributions.

1.  We prove the exact finite-window inequality $$\mathcal{E}_I(z)\geq
    \left[L-\frac{\pi^2U^4}{12L}\right]_{+}\left\lVert z\right\rVert_{2}^{\,2}.$$

2.  We derive the normalized form $$\frac{\mathcal{E}_I(z)}{N}\geq
    \left[\frac 12-\frac{\pi^2U^4}{6N^2}\right]_{+}\left\lVert z\right\rVert_{2}^{\,2},$$ including all parity and positive-part cases.

3.  We specialize the defect to V59 and obtain $U^4/N^2=x^{-67/100+o(1)}$, which rules out a fixed-power gain arising only from interference between distinct reduced frequencies after $q$-collapse.

The conclusion is deliberately scoped. It redirects the search for saving into the collapsed coefficient itself; it does not prove arithmetic cancellation there. Section [2](sections/2_setup.tex#L2){reference-type="ref" reference="sec:setup"} fixes notation. Section [3](sections/3_lower_frame.tex#L2){reference-type="ref" reference="sec:theorem"} proves the lower frame. Section [4](sections/4_route_consequence.tex#L2){reference-type="ref" reference="sec:route"} records the route consequence and claim firewall. Section [5](sections/5_finite_audit.tex#L2){reference-type="ref" reference="sec:audit"} describes the finite audit.

# Finite-window setup

Write $\mathrm{e}(t)=\exp(2\pi i t)$, and let $\left\lVert \theta\right\rVert=\min_{m\in\mathbb Z}|\theta-m|$ be circular distance to the nearest integer. A fraction $a/h\pmod1$ is *primitive* when $\gcd(a,h)=1$. We use a finite set $$\mathcal{F}_{U}=\left\{\frac ah\pmod1:\ 1\leq h\leq U,\ \gcd(a,h)=1\right\},$$ or any subset consisting of distinct points of $\mathbb{R}/\mathbb{Z}$. The theorem also applies to finitely supported coefficient families without taking the full set.

Let $$I=\{M,M+1,\ldots,M+N-1\},\qquad
L=\left\lfloor\frac{N+1}{2}\right\rfloor,$$ and define $$\mathcal{E}_I(z)=
\sum_{n\in I}\left|\sum_{\alpha\in\mathcal{F}_{U}}z_\alpha\mathrm{e}(n\alpha)\right|^2.$$ The norm $\left\lVert z\right\rVert_{2}^{\,2}$ means $\sum_{\alpha\in\mathcal{F}_{U}}|z_\alpha|^2$.

> **Theorem: finite-window lower frame** <span id="thm:lower-frame" label="thm:lower-frame">\[thm:lower-frame\]</span> For every $N\geq1$, $U\geq1$, interval $I$ as above, and finite coefficient vector on distinct primitive fractions of height at most $U$, $$\mathcal{E}_I(z)\geq
> \left[L-\frac{\pi^2U^4}{12L}\right]_{+}\left\lVert z\right\rVert_{2}^{\,2}.$$

> **Corollary: normalized lower frame** <span id="cor:normalized" label="cor:normalized">\[cor:normalized\]</span> Under the hypotheses of Theorem [\[thm:lower-frame\]](sections/2_setup.tex#L29){reference-type="ref" reference="thm:lower-frame"}, $$\frac{\mathcal{E}_I(z)}{N}\geq
> \left[\frac 12-\frac{\pi^2U^4}{6N^2}\right]_{+}\left\lVert z\right\rVert_{2}^{\,2}.$$

> **Corollary: V59 specialization** <span id="cor:v59" label="cor:v59">\[cor:v59\]</span> If $U=x^{133/400}$ and $N\asymp x$, then $$\frac{U^4}{N^2}=x^{-67/100+o(1)}.$$ The normalized lower-frame constant in Corollary [\[cor:normalized\]](sections/2_setup.tex#L39){reference-type="ref" reference="cor:normalized"} is therefore $1/2-o(1)$.

No sharpness assertion is attached to either constant. The role of the explicit constants is to separate a vanishing defect from a fixed-power saving at the V59 scale.

# Triangular-window proof

## The exact Fejér Gram matrix

> **Lemma: triangular minorant** <span id="lem:triangle" label="lem:triangle">\[lem:triangle\]</span> Set $c=M+L-1$ and $$w(c+k)=
> \begin{cases}
> 1-|k|/L,& |k|<L,\\
> 0,& |k|\geq L.
> \end{cases}$$ Then $0\leq w\leq1_I$, and $$\sum_n w(n)\mathrm{e}(n\theta)=\mathrm{e}(c\theta)F_L(\theta),
> \qquad
> F_L(\theta)=\frac1L\left|\sum_{r=0}^{L-1}\mathrm{e}(r\theta)\right|^2.$$ In particular $F_L(0)=L$.

> **Proof** The support of $w$ is $\{M,\ldots,M+2L-2\}$. Since $2L-1\leq N$, it lies in $I$. All weights lie in $[0,1]$. Expanding the square and grouping pairs $(r,s)$ according to $k=r-s$ gives $$\frac1L\left|\sum_{r=0}^{L-1}\mathrm{e}(r\theta)\right|^2
> =\sum_{|k|<L}\left(1-\frac{|k|}{L}\right)\mathrm{e}(k\theta).$$ Translation supplies the factor $\mathrm{e}(c\theta)$.

The parity point in this lemma is useful. For odd $N$, the support has length $N$; for even $N$, it has length $N-1$. Both cases preserve the minorant inequality in the required direction.

## Spacing and packing

> **Lemma: primitive spacing** <span id="lem:spacing" label="lem:spacing">\[lem:spacing\]</span> If $a/h$ and $b/k$ are distinct modulo $1$, primitive, and $h,k\leq U$, then $$\left\lVert \frac ah-\frac bk\right\rVert\geq U^{-2}.$$

> **Proof** Choose $m\in\mathbb Z$ that realizes the circular distance. The integer $ak-bh-mhk$ is nonzero, so $$\left|\frac ah-\frac bk-m\right|
> =\frac{|ak-bh-mhk|}{hk}\geq\frac1{hk}\geq U^{-2}.$$

> **Lemma: Fejér off-diagonal decay** <span id="lem:fejer" label="lem:fejer">\[lem:fejer\]</span> For $\theta\notin\mathbb Z$, $$F_L(\theta)\leq\frac1{4L\left\lVert \theta\right\rVert^{\,2}}.$$

> **Proof** The sine representation of the geometric sum gives $$F_L(\theta)
> =\frac1L\left|\frac{\sin(\pi L\theta)}{\sin(\pi\theta)}\right|^2
> \leq\frac1{L|\sin(\pi\theta)|^2}.$$ For $t=\left\lVert \theta\right\rVert\in(0,1/2]$, concavity on $[0,1/2]$ gives $\sin(\pi t)\geq2t$. Substitution proves the claim.

> **Lemma: circular inverse-square packing** <span id="lem:packing" label="lem:packing">\[lem:packing\]</span> If a finite subset $\mathcal X\subset\mathbb{R}/\mathbb{Z}$ is $\delta$-separated, then for every $x\in\mathcal X$, $$\sum_{\substack{y\in\mathcal X\\y\ne x}}
> \frac1{\left\lVert x-y\right\rVert^{\,2}}\leq\frac{\pi^2}{3\delta^2}.$$

> **Proof** Assign each $y\ne x$ to a shortest clockwise or counterclockwise arc from $x$, assigning an antipodal tie once. In either direction the $j$-th distance is at least $j\delta$; otherwise $j+1$ points in an arc shorter than $j\delta$ would force a neighboring gap below $\delta$. Therefore $$\sum_{y\ne x}\frac1{\left\lVert x-y\right\rVert^{\,2}}
> \leq2\sum_{j\geq1}\frac1{(j\delta)^2}
> =\frac{\pi^2}{3\delta^2}.$$

## Spectral conclusion

> **Proof: Proof of Theorem [\[thm:lower-frame\]](sections/2_setup.tex#L29){reference-type="ref" reference="thm:lower-frame"}** Lemma [\[lem:triangle\]](sections/3_lower_frame.tex#L7){reference-type="ref" reference="lem:triangle"} and $0\leq w\leq1_I$ give $$\mathcal{E}_I(z)\geq
> \sum_nw(n)\left|\sum_\alpha z_\alpha\mathrm{e}(n\alpha)\right|^2
> =z^\ast Gz,$$ where $$G_{\alpha,\beta}
> =\mathrm{e}\!\left(c(\beta-\alpha)\right)F_L(\beta-\alpha).$$ The order $\beta-\alpha$ is forced by the expansion $\overline{z_\alpha}z_\beta\mathrm{e}(n(\beta-\alpha))$; reversing it would conjugate the Gram form and is invalid for general complex coefficients. This Hermitian matrix has diagonal $L$. Lemmas [\[lem:spacing\]](sections/3_lower_frame.tex#L44){reference-type="ref" reference="lem:spacing"}–[\[lem:packing\]](sections/3_lower_frame.tex#L81){reference-type="ref" reference="lem:packing"}, with $\delta=U^{-2}$, give $$\sum_{\beta\ne\alpha}|G_{\alpha,\beta}|
> \leq\frac1{4L}
> \sum_{\beta\ne\alpha}\frac1{\left\lVert \alpha-\beta\right\rVert^{\,2}}
> \leq\frac{\pi^2U^4}{12L}.$$ Schur’s test, equivalently the Hermitian Gershgorin bound, yields $$z^\ast Gz\geq
> \left(L-\frac{\pi^2U^4}{12L}\right)\left\lVert z\right\rVert_{2}^{\,2}.$$ Combining this inequality with $\mathcal{E}_I(z)\geq0$ inserts the positive part and proves the theorem.

> **Proof: Proof of Corollary [\[cor:normalized\]](sections/2_setup.tex#L39){reference-type="ref" reference="cor:normalized"}** Because $L\geq N/2$, $$\frac LN-\frac{\pi^2U^4}{12LN}
> \geq\frac12-\frac{\pi^2U^4}{6N^2}.$$ The positive-part map is monotone, and division by $N>0$ commutes with it.

> **Proof: Proof of Corollary [\[cor:v59\]](sections/2_setup.tex#L48){reference-type="ref" reference="cor:v59"}** The exponent calculation is exact: $$4\cdot\frac{133}{400}-2
> =\frac{532}{400}-\frac{800}{400}
> =-\frac{67}{100}.$$ The relation $N\asymp x$ contributes only $x^{o(1)}$ at the exponent ledger level.

# Route consequence and claim firewall

Suppose a preceding arithmetic decomposition has already collapsed all $q$-variables contributing to the same primitive frequency into coefficients $$z_{h,a}=C_h\sum_{q\sim Q}B_{h,q}(a).$$ Theorem [\[thm:lower-frame\]](sections/2_setup.tex#L29){reference-type="ref" reference="thm:lower-frame"} applies to these coefficients without using their origin. At V59 it gives $$\frac{\mathcal{E}_I(z)}{N\left\lVert z\right\rVert_{2}^{\,2}}\geq\frac12-o(1)$$ whenever $z\ne0$. Thus a proposed estimate of the form $$\frac{\mathcal{E}_I(z)}{N}\ll x^{-\eta}\left\lVert z\right\rVert_{2}^{\,2},
\qquad \eta>0,$$ cannot be obtained from interference among the distinct reduced frequencies. The two inequalities are incompatible for sufficiently large $x$.

This is a structural obstruction, not an arithmetic estimate. In particular, the norm $$\left\lVert z\right\rVert_{2}^{\,2}
=\sum_{\substack{h\leq U\\(a,h)=1}}
\left|C_h\sum_{q\sim Q}B_{h,q}(a)\right|^2$$ may still be substantially smaller than an unsigned or uncollapsed packet baseline. Such a reduction would occur inside the coefficient bucket and is not constrained by the lower frame.

> **Proposition: scoped refutation** At the V59 scale, a fixed-power saving relative to the collapsed coefficient energy cannot be attributed solely to cancellation between distinct primitive frequencies. Cancellation inside the $q$-bucket, inside the literal signed construction of $C_h$, and after the signed four-packet projection remains open.

> **Proof** The first statement follows from Corollary [\[cor:v59\]](sections/2_setup.tex#L48){reference-type="ref" reference="cor:v59"}. The three open mechanisms occur before or after the coefficient vector to which the theorem is applied, so the theorem contains no implication about them.

Accordingly, this paper records $$\begin{gathered}
\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
\texttt{C\_H\_SIGNED\_CANCELLATION=NONE},\\
\texttt{L2=NONE},\qquad
\texttt{FULL\_GATE\_B=OPEN},\\
\texttt{STRICT\_1\_OVER\_400=UNPAID\_GLOBAL},\qquad
\texttt{FIXED\_ATOM=0}.
\end{gathered}$$ Every Route-A component $A0,\ldots,A4$ remains false. No sharpness claim is made for $\pi^2/12$ or $1/2$.

The next theorem should therefore control the literal same-frequency $C_h$-weighted $q$-collision energy. This target is smaller and more arithmetic than any further optimization of cross-frequency signs.

# Finite certificate and independent audit

The analytic proof is independent of computation. We nevertheless provide a deterministic finite certificate to test the identities, matrix directions, translation invariance, and claim firewall.

## Exact fixture

The main fixture is $$(U,N,L)=(4,41,21)$$ and uses all six primitive fractions of height at most $4$: $$0,\quad\frac14,\quad\frac13,\quad\frac12,\quad\frac23,\quad\frac34.$$ Their exact minimum circular spacing is $1/12$, stronger than the theorem floor $1/16$. The triangular window has 41 positive coefficients and exact mass 21. The exact symbolic lower bounds are $$21-\frac{64\pi^2}{63}
\quad\text{and}\quad
\frac12-\frac{128\pi^2}{5043}.$$

<div id="tab:fixture">

|  start|  theorem lower|  triangular $\lambda_{\min}$|  hard-window $\lambda_{\min}$|
|------:|--------------:|----------------------------:|-----------------------------:|
|  $-20$|    $10.973735$|                  $20.571429$|                   $36.000000$|
|    $0$|    $10.973735$|                  $20.571429$|                   $36.000000$|
|   $17$|    $10.973735$|                  $20.571429$|                   $36.000000$|
|  $103$|    $10.973735$|                  $20.571429$|                   $36.000000$|

: Finite checks on four translated $41$-point intervals. The eigenvalues are numerical checks; they are not used to prove the theorem.

</div>

The certificate separates three classes. Rational identities and theorem strings are labeled `EXACT_THEOREM_LEDGER`. Matrix checks are labeled `NUMERICALLY_CERTIFIED_FINITE_CHECK`. The observed excess over the universal theorem bound is labeled `NUMERICAL_OBSERVATION`; it carries no sharpness conclusion.

## Independent implementation and stress

The independent checker does not import the producer. It separately enumerates primitive fractions, reconstructs triangular and hard Gram matrices entry by entry, verifies the certificate digest, and rejects three mutations: a denominator above $U$, a duplicate frequency, and a nonprimitive fraction.

The stress experiment covers $$(U,N)\in\{(2,9),(3,25),(4,41),(5,81)\}$$ with four translations for each parameter pair. Across 16 windows, the smallest triangular-minus-theorem margin is $2.43189450696$, the smallest hard-minus-triangular margin is $3.2$, and the largest translation spectral drift is $1.24\times10^{-11}$. Producer, independent checker, and stress test each produce byte-identical standard output under ordinary and optimized Python, with empty standard error.

# Conclusion

A translated triangular minorant converts finite-window energy into a Fejér Gram form whose diagonal and off-diagonal geometry can be controlled explicitly. Primitive Farey spacing and circular packing then give the lower frame $$\mathcal{E}_I(z)\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_{+}\left\lVert z\right\rVert_{2}^{\,2}.$$ At V59, the normalized defect decays as $x^{-67/100+o(1)}$. Distinct reduced frequencies therefore preserve a positive proportion of the collapsed coefficient energy, uniformly in the coefficient vector.

The obstruction sharpens the next research target. A fixed-power gain, if available, must enter the literal $C_h$-weighted $q$-collision buckets or the later signed packet projection. The present theorem neither proves nor refutes those arithmetic mechanisms. Its reusable contribution is the finite-window lower-frame module and its fail-closed boundary.

# Status ledger and reproduction markers

The exact release markers are:

-   `TPC238_ROUTE_ADVANCE = YES`

-   `TPC238_TRIANGULAR_WINDOW_LOWER_FRAME = PROVED_EXACT`

-   `TPC238_PRIMITIVE_FAREY_SPACING = PROVED_U_TO_MINUS_2`

-   `TPC238_FEJER_OFFDIAGONAL = PROVED_LE_1_OVER_4L_DISTANCE_SQUARED`

-   `TPC238_CIRCULAR_PACKING_ROW_SUM = PROVED_LE_PI_SQUARED_U_FOUR_OVER_3`

-   `TPC238_LOWER_FRAME = PROVED_L_MINUS_PI_SQUARED_U_FOUR_OVER_12L_POSITIVE_PART`

-   `TPC238_NORMALIZED_LOWER_FRAME = PROVED_HALF_MINUS_PI_SQUARED_U_FOUR_OVER_6N_SQUARED_POSITIVE_PART`

-   `TPC238_V59_FRAME_DEFECT = PROVED_X_MINUS_67_OVER_100`

-   `TPC238_CROSS_REDUCED_FREQUENCY_FIXED_POWER_SAVING = REFUTED_SCOPED_AFTER_Q_COLLAPSE`

-   `TPC238_WITHIN_Q_BUCKET_CANCELLATION = OPEN`

-   `TPC238_STATUS = PROVED_STRUCTURAL_OBSTRUCTION_L1`

-   `TPC238_ROUND2_CLUE = MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS`

The machine certificate has payload SHA-256

8af87fa72672eff8b9b5553d620fdbfe4127fdb5ee0fdc7c6b32ef604ec0fe26.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{montgomery1994ten,
  author    = {Montgomery, Hugh L.},
  title     = {Ten Lectures on the Interface between Analytic Number Theory and Harmonic Analysis},
  series    = {CBMS Regional Conference Series in Mathematics},
  volume    = {84},
  publisher = {American Mathematical Society},
  address   = {Providence, RI},
  year      = {1994},
  isbn      = {978-0-8218-0737-8}
}
```

<!-- SOURCE_BODY_END -->
