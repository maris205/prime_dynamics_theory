# Hard-Window Near-Isometry and Signed Bilinear Transfer\ for Primitive Rational Frequencies

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology; Wuhan, China; liang.wang@hust.edu.cn
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We prove a direct hard-window near-isometry for exponential synthesis over any finite separated subset of the circle. If the frequencies are $\delta$-separated and the window contains $N$ consecutive integers, the hard rectangular Gram matrix has diagonal $N$ and absolute off-diagonal row mass at most $R_\delta=\delta^{-1}H_{\lfloor1/(2\delta)\rfloor}$. Hence its normalized distance from the identity is at most $\varepsilon=R_\delta/N$. The same operator estimate yields both a two-sided frame bound and the signed bilinear transfer $$\left\lvert N^{-1}\left\langle Tz,Tw\right\rangle-\left\langle z,w\right\rangle\right\rvert
\leq\varepsilon\left\lVert z\right\rVert_2\left\lVert w\right\rVert_2.$$ For distinct primitive rational frequencies of height at most $U$, this gives $R_U=U^2H_{\lfloor U^2/2\rfloor}$. At the V59 scale $U=x^{133/400}$ and $N=x/2+O(1)$, the exact error is $(133/100+o(1))x^{-67/200}\log x$. This improves the repository’s direct hard-window lower baseline from $1/2-O(U^4/N^2)$ to $1-O(U^2\log U/N)$ and supplies the bilinear interface needed by the TPC-242 phase-selected mode. The result is structural: it proves neither physical coefficient attachment nor arithmetic cancellation.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Hard finite intervals do not automatically preserve coefficient geometry. Even when distinct frequencies are separated modulo one, the rectangular Gram matrix contains signed off-diagonal geometric sums. A lower frame bound must control those sums without replacing the physical window by a different object, while a polarization argument also needs the orientation of a complex cross term to survive.

The repository contains two complementary ingredients. TPC-217 applies the standard additive large sieve to obtain an upper finite-window estimate at the primitive-rational spacing scale `\cite{WangTPC217}`. TPC-238 minorizes the hard window by a triangular weight and proves a normalized lower baseline $1/2-O(U^4/N^2)$ `\cite{WangTPC238}`. TPC-242 then shows that the literal four-phase convention selects an oriented coefficient $F_1=\left\langle Y,X\right\rangle$ `\cite{WangTPC242}`. What remains between these results is a direct rectangular operator estimate that is two-sided and strong enough to transport an oriented bilinear form.

This paper supplies that analytic interface. Its contributions are:

1.  We prove that every off-diagonal row of the hard-window Gram matrix has absolute mass at most $\delta^{-1}H_{\lfloor1/(2\delta)\rfloor}$. The proof treats empty and singleton sets, $N=1$, and the antipodal tie explicitly.

2.  Hermitian Schur/Gershgorin converts the row estimate into a two-sided near-isometry and a signed bilinear estimate with the same error.

3.  For primitive frequencies at the V59 scale, we compute the leading coefficient $133/100$ and the power $-67/200$ exactly.

4.  We match the TPC-242 orientation: $F_1=N^{-1}\left\langle Tw,Tz\right\rangle$ approximates $\left\langle w,z\right\rangle$, not $\left\langle z,w\right\rangle$.

The theorem is an $L1$ structural advance in the program’s terminology. It does not bound the literal physical coefficient norms, identify the top-prime lanes, establish a signed $C_h$ theorem, or produce arithmetic $L2$ cancellation. These exclusions are part of the theorem contract rather than informal caveats.

Section [2](sections/2_setup_source_lock.tex#L1){reference-type="ref" reference="sec:setup"} fixes conventions and repository provenance. Sections [3](sections/3_harmonic_row_bound.tex#L1){reference-type="ref" reference="sec:row"} and [4](sections/4_near_isometry_bilinear.tex#L1){reference-type="ref" reference="sec:operator"} prove the row and operator estimates. Section [5](sections/5_primitive_v59.tex#L1){reference-type="ref" reference="sec:primitive"} specializes the result, and Section [6](sections/6_tpc242_transport.tex#L1){reference-type="ref" reference="sec:transport"} gives the phase-selected transfer. The final sections separate finite reproduction checks from the remaining route gates.

# Setup and source lock

Let $\mathcal{F}\subset\mathbb{R}/\mathbb{Z}$ be finite. Circular distance is denoted by $\left\lVert \theta\right\rVert_{\mathbb{R}/\mathbb{Z}}$. The set is $\delta$-separated when $\left\lVert \alpha-\beta\right\rVert_{\mathbb{R}/\mathbb{Z}}\geq\delta$ for every distinct $\alpha,\beta\in\mathcal{F}$, where $0<\delta\leq1/2$. Let $\mathcal{I}=\{M,\ldots,M+N-1\}$ with $N\geq1$, and define $$Tz(n)=\sum_{\alpha\in\mathcal{F}}z_\alpha\mathrm{e}^{2\pi\mathrm{i}n\alpha}.$$ All complex inner products are conjugate-linear in the first slot. Thus $$\left\langle Tz,Tw\right\rangle
  =\sum_{\alpha,\beta\in\mathcal{F}}
  \overline{z_\alpha}w_\beta
  \sum_{n\in\mathcal{I}}\mathrm{e}^{2\pi\mathrm{i}n(\beta-\alpha)}.$$ The order $\beta-\alpha$ fixes the Gram orientation used throughout.

Put $$K=\left\lfloor\frac1{2\delta}\right\rfloor,
\qquad
H_K=\sum_{j=1}^{K}\frac1j,
\qquad
R_{\delta}=\delta^{-1}H_K,
\qquad
\varepsilon=\frac{R_{\delta}}{N}.$$ The range of $\delta$ implies $K\geq1$. We retain the convention $H_0=0$ for completeness.

## Repository-relative position

The three source proof packages are locked by normalized-LF SHA-256 in the project certificate. Their roles are deliberately disjoint:

| Source  | Existing result                                                            | TPC-243 use and boundary                                   |
|:--------|:---------------------------------------------------------------------------|:-----------------------------------------------------------|
| TPC-217 | Standard upper large-sieve scale and V59 exponent ledger                   | Supplies provenance; the upper scale is not claimed as new |
| TPC-238 | Triangular-minorant lower baseline $1/2-O(U^4/N^2)$                        | Comparison with the direct rectangular lower baseline      |
| TPC-242 | $F_1=\left\langle Y,X\right\rangle$ for the literal $i^j$ phase convention | Fixes the selected orientation, not a physical attachment  |

The exact source locators and hashes appear in the reproducibility ledger. No external citation is used, and no source type is promoted across these boundaries.

# The hard-window harmonic row bound

The proof uses the rectangular window itself. Translation of the interval changes only phases and therefore does not affect entry magnitudes.

> **Lemma: Geometric-sum bound**<span id="lem:geometric" label="lem:geometric">\[lem:geometric\]</span> For $\theta\notin\mathbb Z$, $$\left\lvert \sum_{n=M}^{M+N-1}\mathrm{e}^{2\pi\mathrm{i}n\theta}\right\rvert
> \leq\frac1{2\left\lVert \theta\right\rVert_{\mathbb{R}/\mathbb{Z}}}.$$

> **Proof** After removing the unit factor $\mathrm{e}^{2\pi\mathrm{i}M\theta}$, the geometric-sum identity gives $$\left\lvert \sum_{r=0}^{N-1}\mathrm{e}^{2\pi\mathrm{i}r\theta}\right\rvert
> =\frac{\left\lvert \sin(\pi N\theta)\right\rvert}{\left\lvert \sin(\pi\theta)\right\rvert}
> \leq\frac1{\left\lvert \sin(\pi\theta)\right\rvert}.$$ For $t=\left\lVert \theta\right\rVert_{\mathbb{R}/\mathbb{Z}}\in(0,1/2]$, concavity on $[0,1/2]$ gives $\sin(\pi t)\geq2t$. Since $\left\lvert \sin(\pi\theta)\right\rvert=\sin(\pi t)$, the estimate follows.

> **Lemma: Two-sided harmonic packing**<span id="lem:packing" label="lem:packing">\[lem:packing\]</span> For every fixed $\alpha\in\mathcal{F}$, $$\sum_{\substack{\beta\in\mathcal{F}\\\beta\neq\alpha}}
> \frac1{2\left\lVert \beta-\alpha\right\rVert_{\mathbb{R}/\mathbb{Z}}}
> \leq\delta^{-1}H_K.$$

> **Proof** Represent each difference $\beta-\alpha$ in $(-1/2,1/2]$. Assign positive representatives to one oriented side and negative representatives to the other. An antipodal point has representative $1/2$ and is assigned to the positive side only, so it cannot be counted twice.
>
> On either side, list the distances as $d_1<\cdots<d_m$. Separation between successive points on that half-circle, including $\alpha$ at distance zero, implies $d_j\geq j\delta$. Since $d_j\leq1/2$, one also has $m\leq\lfloor1/(2\delta)\rfloor=K$. One side therefore contributes at most $$\sum_{j=1}^{m}\frac1{2d_j}
>   \leq\frac1{2\delta}\sum_{j=1}^{K}\frac1j
>   =\frac{H_K}{2\delta}.$$ Adding the two side bounds proves the claim. When $\delta=1/2$, there is at most one off-diagonal point and it is antipodal; the same one-side rule applies.

> **Proposition: Rectangular Gram rows**<span id="prop:rows" label="prop:rows">\[prop:rows\]</span> Let $G=T^*T$. Then $G_{\alpha\alpha}=N$, and every absolute off-diagonal row sum is at most $R_{\delta}$.

> **Proof** The Gram entries are $$G_{\alpha\beta}
> =\sum_{n\in\mathcal{I}}\mathrm{e}^{2\pi\mathrm{i}n(\beta-\alpha)}.$$ The diagonal equals $N$. For $\beta\neq\alpha$, separation makes $\beta-\alpha$ nonintegral. Lemma [\[lem:geometric\]](sections/3_harmonic_row_bound.tex#L6){reference-type="ref" reference="lem:geometric"} bounds the entry by $(2\left\lVert \beta-\alpha\right\rVert_{\mathbb{R}/\mathbb{Z}})^{-1}$, and Lemma [\[lem:packing\]](sections/3_harmonic_row_bound.tex#L27){reference-type="ref" reference="lem:packing"} sums these bounds.

If $\mathcal{F}$ is empty, Proposition [\[prop:rows\]](sections/3_harmonic_row_bound.tex#L55){reference-type="ref" reference="prop:rows"} is vacuous. If it is a singleton, $G=[N]$ and the row mass is zero. Lemma [\[lem:geometric\]](sections/3_harmonic_row_bound.tex#L6){reference-type="ref" reference="lem:geometric"} also allows $N=1$, so no hidden lower bound on the window length has entered.

# Near-isometry and signed bilinear transfer

> **Theorem: Hard-window operator estimate**<span id="thm:main" label="thm:main">\[thm:main\]</span> For every $z,w\in\ell^2(\mathcal{F})$, $$\left[1-\varepsilon\right]_{+}\left\lVert z\right\rVert_2^2
> \leq N^{-1}\left\lVert Tz\right\rVert_2^2
> \leq(1+\varepsilon)\left\lVert z\right\rVert_2^2,$$ and $$\left\lvert N^{-1}\left\langle Tz,Tw\right\rangle-\left\langle z,w\right\rangle\right\rvert
> \leq\varepsilon\left\lVert z\right\rVert_2\left\lVert w\right\rVert_2.$$

> **Proof** Set $A=G-NI$. Since $G=T^*T$, both $G$ and $A$ are Hermitian. Proposition [\[prop:rows\]](sections/3_harmonic_row_bound.tex#L55){reference-type="ref" reference="prop:rows"} gives $\left\lVert A\right\rVert_\infty\leq R_{\delta}$. Hermitian symmetry gives the same bound for the absolute column norm. Schur’s estimate yields $$\left\lVert A\right\rVert_{2\to2}
> \leq\sqrt{\left\lVert A\right\rVert_1\left\lVert A\right\rVert_\infty}
> \leq R_{\delta}.$$ Equivalently, Hermitian Gershgorin places the spectrum of $A$ in $[-R_{\delta},R_{\delta}]$.
>
> The identity $\left\lVert Tz\right\rVert_2^2=\left\langle z,Gz\right\rangle$ now gives the upper bound and the lower bound $(N-R_{\delta})\left\lVert z\right\rVert_2^2$. Independently, $G$ is positive semidefinite. Taking the stronger of this lower estimate and zero, then dividing by $N$, produces the positive part in the theorem.
>
> For the bilinear statement, the orientation fixed in Section [2](sections/2_setup_source_lock.tex#L1){reference-type="ref" reference="sec:setup"} gives $\left\langle Tz,Tw\right\rangle=\left\langle z,Gw\right\rangle$. Hence $$\begin{aligned}
> \left\lvert N^{-1}\left\langle Tz,Tw\right\rangle-\left\langle z,w\right\rangle\right\rvert
> &=\left\lvert \left\langle z,(N^{-1}G-I)w\right\rangle\right\rvert\\
> &\leq\left\lVert N^{-1}G-I\right\rVert_{2\to2}\left\lVert z\right\rVert_2\left\lVert w\right\rVert_2\\
> &\leq\varepsilon\left\lVert z\right\rVert_2\left\lVert w\right\rVert_2.
> \end{aligned}$$ The argument controls the complex bilinear quantity directly; it does not recover it from two separate unsigned estimates.

> **Remark: Comparison of lower regimes** TPC-238 obtains a hard-window lower estimate by inserting a triangular minorant. The normalized baseline is $1/2-O(U^4/N^2)$. Theorem [\[thm:main\]](sections/4_near_isometry_bilinear.tex#L3){reference-type="ref" reference="thm:main"} works with the rectangular Gram matrix and gives $1-O(U^2\log U/N)$ after primitive specialization. The former can become nontrivial with a smaller logarithmic requirement; the latter converges to the identity and also controls bilinear forms. These are different guarantees rather than contradictory bounds.

# Primitive rational specialization and V59 scale

> **Corollary: Primitive height**<span id="cor:primitive" label="cor:primitive">\[cor:primitive\]</span> Let the frequencies be distinct reduced fractions modulo one with denominators at most $U$, where $U\geq2$. Theorem [\[thm:main\]](sections/4_near_isometry_bilinear.tex#L3){reference-type="ref" reference="thm:main"} applies with $$\delta=U^{-2},\qquad
> K_U=\left\lfloor\frac{U^2}{2}\right\rfloor,
> \qquad
> R_U=U^2H_{K_U}.$$

> **Proof** For two distinct reduced fractions $a/h$ and $b/k$, choose an integer $m$ realizing their circular distance. The integer $ak-bh-mhk$ is nonzero, and therefore $$\left\lVert \frac ah-\frac bk\right\rVert_{\mathbb{R}/\mathbb{Z}}
> =\frac{\left\lvert ak-bh-mhk\right\rvert}{hk}
> \geq\frac1{hk}\geq U^{-2}.$$ Since $U\geq2$, the chosen separation lies in $(0,1/2]$. Substitution in the definitions of $K$ and $R_{\delta}$ proves the formulas.

For V59, the source interval and height are $$\mathcal{I}_x=(x/2,x]\cap\mathbb Z,\qquad
N=\left\lvert \mathcal{I}_x\right\rvert=\frac{x}{2}+O(1),\qquad
U=x^{133/400}.$$ Thus $U^2=x^{133/200}$ and $$H_{\lfloor U^2/2\rfloor}
=\log\!\left(\left\lfloor\frac{U^2}{2}\right\rfloor\right)+O(1)
=2\log U+O(1)
=\frac{133}{200}\log x+O(1).$$ It follows that $$\begin{aligned}
\varepsilon_U
&=\frac{U^2H_{\lfloor U^2/2\rfloor}}{N}\\
&=\frac{x^{133/200}\bigl((133/200)\log x+O(1)\bigr)}{x/2+O(1)}\\
&=\left(\frac{133}{100}+o(1)\right)x^{-67/200}\log x
=x^{-67/200+o(1)}.
\end{aligned}$$ The coefficient $133/100$ is exact: the harmonic logarithm contributes $133/200$, and the interval density contributes the reciprocal factor $2$.

TPC-217 already records the upper large-sieve estimate and this primitive spacing scale `\cite{WangTPC217}`. The new statement here is the direct rectangular two-sided operator estimate and its bilinear consequence, not the existence of the upper exponent.

# Transport of the TPC-242 selected mode

TPC-242 fixes a convention that cannot be suppressed in a complex argument. For phase energies $E_j=\left\lVert X+\mathrm{i}^jY\right\rVert^2$ and Fourier weights $\mathrm{i}^{kj}$, the selected mode is $F_1=\left\langle Y,X\right\rangle$ under the conjugate-linear-first inner product `\cite{WangTPC242}`.

Set $$X=N^{-1/2}Tz,\qquad Y=N^{-1/2}Tw.$$ Then $$F_1=\left\langle Y,X\right\rangle=N^{-1}\left\langle Tw,Tz\right\rangle.$$ Apply Theorem [\[thm:main\]](sections/4_near_isometry_bilinear.tex#L3){reference-type="ref" reference="thm:main"} with the ordered coefficient pair $(w,z)$ rather than $(z,w)$. The result is $$\label{eq:selected-transfer}
\left\lvert F_1-\left\langle w,z\right\rangle\right\rvert
\leq\varepsilon\left\lVert w\right\rVert_2\left\lVert z\right\rVert_2.$$ The target $\left\langle w,z\right\rangle$ is generally the complex conjugate of $\left\langle z,w\right\rangle$. Reversing the target would therefore change the theorem, not merely its notation.

Equation [\[eq:selected-transfer\]](sections/6_tpc242_transport.tex#L18){reference-type="eqref" reference="eq:selected-transfer"} is a signed bilinear interface. It says that a coefficient-space phase and sign survive the hard-window map up to an explicit norm-weighted error. It does not show that $F_1$ is small, large, nonzero, or of a prescribed sign. More importantly, the repository does not yet identify the two literal V59 top-prime lanes with $z$ and $w$ in this one common synthesis map. Such an attachment theorem and a coefficient norm bound are separate arithmetic requirements.

# Exact finite certificate

The executable package checks one orientation-sensitive fixture with exact Gaussian rational arithmetic. Its frequencies are $$\mathcal{F}_4=\left\{0,\frac14,\frac12,\frac34\right\},
\quad \delta=\frac14,
\quad K=2,
\quad H_K=\frac32,
\quad R_{\delta}=6.$$ On $\mathcal{I}=\{-3,\ldots,13\}$, so $N=17$, the exact maximum off-diagonal row mass is $3$ and $\varepsilon=6/17$. The fixture checks the full Gram matrix, quadratic bounds, a nonreal ordered coefficient pair, both bilinear orientations, and the exact V59 fraction ledger.

A separate stress program enumerates $81$ four-coordinate vectors from the alphabet $\{0,1,\mathrm{i}\}$. It checks four fixed intervals, $324$ quadratic forms, and all $6561$ ordered pairs on the length-$17$ interval. Among those pairs, the orientation census includes nonreal targets, so the order check is not vacuous.

The stored result is canonical compact JSON with a payload digest. Strict parsing rejects duplicate keys, nonfinite constants, nonminimal fractions, and Boolean substitutions for integers. The independent checker does not import the producer and binds every nested source, theorem, task, scope, and status field. Digest-rebound hostile variants attempt to replace the source lock, reverse the selected mode, promote arithmetic status, promote strict $1/400$, promote a twin-prime result, and inject an unread scope key.

All finite checks are `NUMERICAL_FINITE_ILLUSTRATION_ONLY`. Exact arithmetic removes rounding ambiguity from reproduction; it does not prove the general theorem. The symbolic argument in Sections [3](sections/3_harmonic_row_bound.tex#L1){reference-type="ref" reference="sec:row"}–[6](sections/6_tpc242_transport.tex#L1){reference-type="ref" reference="sec:transport"} is the theorem evidence.

# Route evaluation and claim boundary

The strongest positive result is the common operator interface $$\left\lVert N^{-1}T^*T-I\right\rVert_{2\to2}
\leq\frac{\delta^{-1}H_{\lfloor1/(2\delta)\rfloor}}{N}.$$ It simultaneously preserves quadratic energy and an oriented signed bilinear form. At the V59 height this error tends to zero with exact power $-67/200$ up to a logarithm.

The strongest obstruction is external to the operator estimate. The error in Equation [\[eq:selected-transfer\]](sections/6_tpc242_transport.tex#L18){reference-type="eqref" reference="eq:selected-transfer"} is multiplied by $\left\lVert w\right\rVert_2\left\lVert z\right\rVert_2$, while no current theorem supplies the required bound for the literal physical lanes. Absolute harmonic packing also contains no arithmetic cancellation.

The next open theorem is therefore source-typed: identify both polarized V59 lanes in one primitive-rational synthesis map and audit their literal $C_h$ multipliers. If one common multiplier acts on both lanes, the selected cross term may contain $\left\lvert C_h\right\rvert^2$, which would erase the sign of $C_h$. That possibility must be resolved before the sign can be used as a proposed cancellation mechanism.

The reusable structure is $$\begin{gathered}
\text{geometric entry bound}
\longrightarrow\text{two-sided harmonic packing}\\
\longrightarrow\text{Hermitian Gram perturbation}
\longrightarrow\text{quadratic and bilinear transfer}.
\end{gathered}$$ It is invariant under translation of the integer window and keeps analytic transport separate from arithmetic coefficient estimates.

In the program ledger, Route A is not applicable and Route B advances only at structural $L1$. Arithmetic $L2$, literal top-prime attachment, a signed $C_h$ theorem, fixed-atom credit, strict $1/400$, full Gate B, and a twin-prime conclusion all remain open or absent.

# Conclusion

The hard rectangular synthesis operator is an explicit near-isometry whenever $N$ dominates the harmonic packing scale $\delta^{-1}H_{\lfloor1/(2\delta)\rfloor}$. The proof requires only the geometric sum, two-sided circular separation, and a Hermitian operator bound, yet it retains enough information to transfer complex signed bilinear forms. For primitive V59 frequencies, the normalized error is $(133/100+o(1))x^{-67/200}\log x$.

The result connects the TPC-238 lower-frame line to the TPC-242 selected phase mode without promoting either source beyond its type. The remaining problem is arithmetic rather than geometric: the physical lanes and their coefficient norms must be attached to the common synthesis map. The narrow next step is a literal common-multiplier sign audit for $C_h$ in the two polarized lanes.

# Status and reproducibility ledger

| Field                  | Value                                               |
|:-----------------------|:----------------------------------------------------|
| Maximum theorem status | Structural $L1$ near-isometry and bilinear transfer |
| Arithmetic advance     | No                                                  |
| Route A                | Not applicable                                      |
| Route B                | Structural only                                     |
| Finite computation     | Illustration only                                   |
| Physical attachment    | Open                                                |
| Strict $1/400$         | Unpaid globally                                     |
| Full Gate B            | Open                                                |
| Twin-prime result      | None                                                |

The exact machine status is

PROVED\_STRUCTURAL\_L1\_HARD\_WINDOW\_NEAR\_ISOMETRY\_ BILINEAR\_TRANSFER.

The strongest positive result is the hard-window operator perturbation bound. The strongest obstruction is the missing physical coefficient norm and attachment theorem. The reusable structure is harmonic circular packing followed by Hermitian Schur/Gershgorin. The registered next clue is

COMMON\_MULTIPLIER\_SIGN\_AUDIT\_FOR\_LITERAL\_C\_H\_IN\_THE\_ TWO\_POLARIZED\_LANES.

The project README records exact normal and optimized reproduction commands. The producer, independent checker, and stress checker use no `assert` and create no theorem claim from their finite output.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@unpublished{WangTPC217,
  author = {Liang Wang},
  title  = {Finite-Window Attachment by Reduced Rational-Frequency Large Sieve},
  note   = {TPC-217 repository manuscript and proof package},
  year   = {2026}
}

@unpublished{WangTPC238,
  author = {Liang Wang},
  title  = {A Finite-Window Lower Frame Obstruction for Primitive Rational Frequencies},
  note   = {TPC-238 repository manuscript and proof package},
  year   = {2026}
}

@unpublished{WangTPC242,
  author = {Liang Wang},
  title  = {Phase-Fourier Separation of Unsigned Collision Energy from the Signed Four-Packet Channel},
  note   = {TPC-242 repository manuscript and proof package},
  year   = {2026}
}
```

# Non-content font-mapping input (preserved command)

Original paper/main.tex line 8: glyphtounicode.tex, SHA-256 395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851. This audited PDF glyph-to-Unicode map is not manuscript content. Its command is retained without executing TeX or expanding the mapping table.

``` {.latex}
\input{glyphtounicode}
```

<!-- SOURCE_BODY_END -->
