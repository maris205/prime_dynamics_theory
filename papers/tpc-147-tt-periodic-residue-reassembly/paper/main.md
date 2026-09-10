# **Periodic Reassembly Inside a Quantitative**\ **Multiplicative Correlation Corridor: Exact Quantifiers,**\ **Zero Residue-Census Loss, and Non-Prefix Scope**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-147-tt-periodic-residue-reassembly.pdf](../tpc-147-tt-periodic-residue-reassembly.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The quantitative two-point theorem of Tao and Teräväinen is uniform in the congruence modulus, residue and two shifts after its multiplicative functions and ambient scale have been fixed. We source-lock these quantifiers and derive a periodic reassembly principle that will be used on determinant-two Möbius fibers. If one progression of modulus $Q$ carries a bounded multiplier of period $R$, and $QR$ lies in the theorem’s small-polylogarithmic modulus envelope, then resolving the multiplier into $R$ residue classes creates no factor $R$. Each refined class has natural mass $N/(QR)$, so its $R$-fold census exactly returns the original mass $N/Q$.

This removes a spurious $\ell^1$ loss from structured periodic reassembly. It does not remove an outer coefficient-mass loss and does not cover a nonperiodic physical multiplier, a generic additive phase, an arbitrary interval origin, deterministic prefixes or a four-point kernel. The conclusion is a good-scale $\mathrm{L1}$ arithmetic interface, not positive $\mathrm{L2}$, not an $X$-power saving and not a prime-pair statement.

<!-- SOURCE_BODY_BEGIN -->

# The exact source contract

We use the general multiplicative-function form of `\citet[Theorem~3.1]{TaoTeravainen2026}`, not only its affine Liouville corollary. Let $X\ge2$, let $g_1,g_2:\mathbb N\to\mathbb C$ be one-bounded multiplicative functions, and let $$1\le\mathcal L\le\log X.$$ In the nonpretentious branch, $\delta_N=0$ and $$\exp M(g_1;X^2,\log^{1/125}X)\gg\mathcal L.
\label{eq:nonpret}$$ The equidistributed branch has a different hypothesis that will not be used in the quotient-Möbius application.

For a sufficiently small absolute $c>0$, the source chooses a set $$\mathcal E_X(g_1,g_2,\mathcal L)\subset[\sqrt X,X]$$ satisfying $$\frac1{\log X}\int_{\mathcal E_X}\frac{dt}{t}
 \ll \mathcal L^{-c}.
\label{eq:exception}$$ For every $N\in[\sqrt X,X]\setminus\mathcal E_X$, every $$1\le W\le\mathcal L^c,
 \qquad b,h_1,h_2=O(\mathcal L^c),
 \qquad h_1\ne h_2,$$ the conclusion is $$\frac WN\left|
 \sum_{\substack{N<n\le2N\\n\equiv b\ ({\rm mod}\ W)}}
 (g_1(n+h_1)-\delta_N)g_2(n+h_2)
 \right|
 \ll \mathcal L^{-c}.
\label{eq:source}$$ The exceptional set is selected before $W,b,h_1,h_2$; hence it is uniform in these parameters. The normalization $W/N$ is part of the theorem.

> **Remark: Local and global exceptional sets are different** <span id="rem:local-global" label="rem:local-global">\[rem:local-global\]</span> also record a global Liouville affine special case, with one exceptional set for all sufficiently small polylogarithmic affine data. Equation [\[eq:exception\]](../main.tex#L100){reference-type="eqref" reference="eq:exception"} is the local set from the general theorem and may depend on $g_1,g_2,\mathcal L,X$. We never replace it by the global Liouville set.

# An exact periodic residue partition

Fix a base modulus $Q\ge1$, a residue $b_0\bmod Q$, and a period $R\ge1$. If $n\equiv b_0\pmod Q$, write $$z(n)=\frac{n-b_0}{Q}\in\mathbb Z.$$ Let $\rho:\mathbb Z/R\mathbb Z\to\mathbb C$.

> **Lemma: Row-separated periodic partition** <span id="lem:partition" label="lem:partition">\[lem:partition\]</span> For every finitely supported sequence $F(n)$, $$\sum_{n\equiv b_0\ ({\rm mod}\ Q)}
>  F(n)\rho(z(n))
>  =
>  \sum_{r\bmod R}\rho(r)
>  \sum_{n\equiv b_0+Qr\ ({\rm mod}\ QR)}F(n).
> \label{eq:partition}$$ The $R$ refined classes are pairwise disjoint and their union is the base class $b_0\bmod Q$.

> **Proof** The condition $z(n)\equiv r\pmod R$ is exactly $n\equiv b_0+Qr\pmod{QR}$. Distinct $r\bmod R$ give distinct classes modulo $QR$, and every integer in the base class has one such $r$.

This is a pathwise partition, not a scalar replacement by a periodic density. It retains the value $\rho(r)$ on every refined class.

# Periodic reassembly without a census loss

> **Theorem: Source-native periodic reassembly** <span id="thm:periodic" label="thm:periodic">\[thm:periodic\]</span> Assume the hypotheses of [\[eq:source\]](../main.tex#L115){reference-type="eqref" reference="eq:source"} for fixed $g_1,g_2$. Let $Q,R\ge1$ satisfy $$QR\le\mathcal L^c,
> \label{eq:height}$$ and suppose the residue representatives and shifts remain within the source’s $O(\mathcal L^c)$ envelope. Then, for every $N\in[\sqrt X,X]\setminus\mathcal E_X$, $$\begin{aligned}
>  \frac QN\bigg|
>  \sum_{\substack{N<n\le2N\\n\equiv b_0\ ({\rm mod}\ Q)}}
>  &(g_1(n+h_1)-\delta_N)g_2(n+h_2)
> \notag\\[-1mm]
>  &\times\rho\!\left(\frac{n-b_0}{Q}\right)
>  \bigg|
>  \ll \|\rho\|_\infty\mathcal L^{-c}.
> \label{eq:periodic}\end{aligned}$$ The same exceptional set works for every allowed $Q,R,b_0,\rho$.

> **Proof** Apply [\[lem:partition\]](../main.tex#L141){reference-type="ref" reference="lem:partition"}. Each inner sum is on one residue modulo $QR$. Choose its canonical representative in $\{0,\ldots,QR-1\}$; this remains inside the source height envelope because $QR\le\mathcal L^c$. Equation [\[eq:source\]](../main.tex#L115){reference-type="eqref" reference="eq:source"}, with $W=QR$, bounds its absolute value by $$\frac{N}{QR}\mathcal L^{-c}.$$ There are $R$ classes, and every coefficient has modulus at most $\|\rho\|_\infty$. Thus the unnormalized total is at most $$R\|\rho\|_\infty\frac{N}{QR}\mathcal L^{-c}
>  =
>  \|\rho\|_\infty\frac NQ\mathcal L^{-c}.$$ Multiplication by $Q/N$ proves [\[eq:periodic\]](../main.tex#L186){reference-type="eqref" reference="eq:periodic"}. Uniformity of the source set in $W,b,h_1,h_2$ shows that no union of $R$ exceptional sets is required.

> **Corollary: Products of periodic masks** <span id="cor:masks" label="cor:masks">\[cor:masks\]</span> Any finite product of bounded periodic masks may be combined into one bounded periodic function whose period divides the least common multiple of their periods. If the resulting $QR$ satisfies [\[eq:height\]](../main.tex#L173){reference-type="eqref" reference="eq:height"}, [\[thm:periodic\]](../main.tex#L168){reference-type="ref" reference="thm:periodic"} charges its supremum norm but no separate residue-count exponent.

This applies, for example, to an exactly periodic coprimality mask or a fixed-period coefficient. A rational additive phase is included only when its exact denominator is absorbed in $R$. No conclusion is made for a generic real phase.

# What is and is not an $\ell^1$ cost

The cancellation in [\[thm:periodic\]](../main.tex#L168){reference-type="ref" reference="thm:periodic"} is a normalization fact: $$R\times\frac{N}{QR}=\frac NQ.
\label{eq:density-cancel}$$ It does not say that every finite decomposition has no cost. If several distinct outer records carry coefficients $\gamma_\xi$, then a triangle-inequality return still involves the actual ratio $$\frac{
 \sum_\xi|\gamma_\xi|(N_\xi/Q_\xi)
 }{\text{declared physical comparison mass}}.$$ That ratio must be measured on the literal archive. Likewise, splitting a nonperiodic multiplier into unrelated pieces does not satisfy [\[eq:density-cancel\]](../main.tex#L232){reference-type="eqref" reference="eq:density-cancel"}.

> **Proposition: No prefix promotion** <span id="prop:no-prefix" label="prop:no-prefix">\[prop:no-prefix\]</span> Equations [\[eq:exception\]](../main.tex#L100){reference-type="eqref" reference="eq:exception"}–[\[eq:periodic\]](../main.tex#L186){reference-type="eqref" reference="eq:periodic"} do not imply a bound for a prescribed deterministic scale, an arbitrary interval $(A,B]$, or the maximum over all initial prefixes of such an interval.

> **Proof** The source conclusion is asserted only for $N\in[\sqrt X,X]\setminus\mathcal E_X$ and for the interval $(N,2N]$. A prescribed scale may lie in $\mathcal E_X$, while an arbitrary interval or prefix is not among the theorem’s quantified objects. None is created by the exact residue identity.

# Certificate and claim boundary

The deterministic certificate checks the row-separated partition, the native $W/N$ normalization and the exact mass identity [\[eq:density-cancel\]](../main.tex#L232){reference-type="eqref" reference="eq:density-cancel"}. It also rejects mutations that replace the local exceptional set by the global Liouville set, move $QR$ outside the source envelope, or attach unsupported weights and prefixes. These are finite consistency checks, not numerical evidence for [\[eq:source\]](../main.tex#L115){reference-type="eqref" reference="eq:source"}.

\@p0.48Y@ Statement & Level and status\
Periodic residue partition & Exact $\mathrm{L0}$, $\textnormal{\textsc{proved}}$.\
No $R$-census loss under $QR\le\mathcal L^c$ & Sourced good-scale $\mathrm{L1}$, $\textnormal{\textsc{proved}}$.\
One exceptional set for all residues and periods & $\textnormal{\textsc{proved}}$ for fixed $g_1,g_2,X,\mathcal L$.\
Nonperiodic physical multiplier or generic phase & $\textnormal{\textsc{open}}$; not in the theorem.\
Arbitrary origin or all-prefix maximum & $\textnormal{\textsc{open}}$; no implication.\
Positive $\mathrm{L2}$, fixed $X$-power or $1/400$ & Not proved.\
Prime-pair or twin-prime theorem & Not proved.\

TPC-147 therefore removes one false reassembly loss while preserving all source quantifiers. The next paper constructs multiplicative functions whose values on a determinant-two progression are the literal Möbius quotients.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{TaoTeravainen2026,
  author        = {Tao, Terence and Ter{\"a}v{\"a}inen, Joni},
  title         = {{Quantitative Correlations and Some Problems on Prime
                    Factors of Consecutive Integers}},
  year          = {2026},
  eprint        = {2512.01739v2},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT}
}

@article{MatomakiRadziwillTao2015,
  author  = {Matom{\"a}ki, Kaisa and Radziwi{\l}{\l}, Maksym and Tao, Terence},
  title   = {{An Averaged Form of Chowla's Conjecture}},
  journal = {Algebra \& Number Theory},
  volume  = {9},
  number  = {9},
  pages   = {2167--2196},
  year    = {2015},
  doi     = {10.2140/ant.2015.9.2167}
}

@misc{WangTPC139,
  author       = {Wang, Liang},
  title        = {{From Frozen Affine Pairs to Growing CRT Fibers}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-139-growing-affine-uniformity-phase-diagram}}
}

@misc{WangTPC140,
  author       = {Wang, Liang},
  title        = {{Exceptional Scales, Deterministic Selectors, and the Power-Saving Gate}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-140-exceptional-scale-selector-power-gate}}
}
```

<!-- SOURCE_BODY_END -->
