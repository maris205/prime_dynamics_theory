# **A Small-Polylogarithmic Determinant-Two**\ **Möbius Corridor: Uniform Actual-Core**\ **Cancellation with Bounded Periodic Data**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-149-small-polylog-determinant-two-mobius-corridor.pdf](../tpc-149-small-polylog-determinant-two-mobius-corridor.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We combine the general quantitative correlation theorem of Tao and Teräväinen with two exact interfaces. TPC-148 constructs multiplicative quotient lifts $G_c$ satisfying $G_c(cm)=\mu(m)$, and TPC-147 reassembles a bounded periodic multiplier without paying its number of residue classes. The result is a uniform theorem on the literal determinant-two Möbius periodic core.

There are absolute constants $\eta_0,\kappa_0>0$ such that, for each sufficiently large ambient $X$, outside a subset of $[\sqrt X,X]$ of normalized logarithmic measure $O((\log X)^{-\kappa_0})$, one has $$\frac{as}{N}
 \left|
 \sum_{N<ad+asz\le2N}
 \mu(d+sz)\mu(u+az)\rho(z)
 \right|
 \ll\|\rho\|_\infty(\log X)^{-\kappa_0}$$ uniformly for coprime odd $a,s$, determinant $su-ad=2$, and bounded periodic $\rho$ of period $R$, provided $asR\le(\log X)^{\eta_0}$. The exceptional union is taken only over the distinct pairs $(a,s)$; the source theorem is already uniform in residues and allowed moduli.

This is a proved $\mathrm{L1}$ actual-core theorem. The current frontier archive has not supplied its occurrence lift, and the theorem does not include a nonperiodic physical multiplier, a generic phase, arbitrary intervals, all prefixes or a four-point kernel. Hence it is not positive $\mathrm{L2}$, has zero fixed-$X$-power exponent and does not approach a prime-pair conclusion by itself.

<!-- SOURCE_BODY_BEGIN -->

# Inputs and notation

Let $$D(z)=d+sz,\qquad V(z)=u+az,\qquad su-ad=2,
\label{eq:fiber}$$ where $a,s$ are positive, coprime and odd. These are the literal determinant-two forms from the fixed-shift carrier `\citep{WangTPC127}`. Define $$Q_{\rm fib}=as,\qquad t(z)=aD(z)=ad+Q_{\rm fib}z.
\label{eq:t}$$ Then $t(z)+2=sV(z)$.

TPC-148 constructs one-bounded multiplicative functions $G_c$ satisfying $$G_c(cm)=\mu(m)
\label{eq:quotient}$$ and proves, uniformly for small-polylogarithmic $c$, $$\exp M(G_c;X^2,\log^{1/125}X)
 \gg(\log X)^\alpha
\label{eq:nonpret}$$ for some absolute $\alpha>0$ `\citep{WangTPC148,MatomakiRadziwillTao2015}`. Consequently $$\mu(D(z))\mu(V(z))=G_a(t(z))G_s(t(z)+2).
\label{eq:core}$$

TPC-147 shows that a bounded period-$R$ multiplier on the $Q_{\rm fib}$-progression may be resolved modulo $Q_{\rm fib}R$ without an $R$-census loss, provided this total modulus lies in the quantitative source envelope `\citep{WangTPC147}`.

# An individual-pair corridor

We first retain one fixed pair $(a,s)$ while allowing all intercepts, periods and periodic values.

> **Proposition: One quotient-pair exceptional set** <span id="prop:pair" label="prop:pair">\[prop:pair\]</span> There is an absolute $\beta>0$ such that the following holds for all sufficiently large $X$. For every coprime odd pair $(a,s)$ with $$as\le(\log X)^\beta,$$ there is a set $\mathcal E_{a,s;X}\subset[\sqrt X,X]$ satisfying $$\frac1{\log X}\int_{\mathcal E_{a,s;X}}\frac{dt}{t}
>  \ll(\log X)^{-\beta}.
> \label{eq:pair-exception}$$ If $$N\in[\sqrt X,X]\setminus\mathcal E_{a,s;X},
>  \qquad asR\le(\log X)^\beta,$$ then, uniformly in all integral $d,u$ obeying [\[eq:fiber\]](../main.tex#L92){reference-type="eqref" reference="eq:fiber"} and all period-$R$ functions $\rho$, $$\frac{as}{N}
>  \left|
>  \sum_{\substack{z\in\mathbb Z\\N<ad+asz\le2N}}
>  \mu(D(z))\mu(V(z))\rho(z)
>  \right|
>  \ll\|\rho\|_\infty(\log X)^{-\beta}.
> \label{eq:pair-bound}$$

> **Proof** Use [\[eq:nonpret\]](../main.tex#L113){reference-type="eqref" reference="eq:nonpret"} with $\mathcal L=(\log X)^\alpha$, decreasing $\alpha$ if needed. The nonpretentious branch of `\citet[Theorem~3.1]{TaoTeravainen2026}` then gives an absolute source exponent $c>0$, an exceptional set of normalized measure $\ll\mathcal L^{-c}$, and a correlation estimate with the same saving for all moduli $W\le\mathcal L^c$. Put $\beta=\alpha c$, decreasing it harmlessly to absorb source constants.
>
> Invoke the source with $$g_1=G_a,\quad g_2=G_s,\quad h_1=0,\quad h_2=2.$$ On $t\equiv ad\pmod{as}$, equation [\[eq:core\]](../main.tex#L119){reference-type="eqref" reference="eq:core"} is exact. TPC-147 reassembles $\rho$ by using the refined modulus $W=asR$; the period count cancels against the density of each refined progression. The source exceptional set is uniform in $W$, its residue and the two shifts, so it is independent of $d,u,R,\rho$. This proves [\[eq:pair-bound\]](../main.tex#L162){reference-type="eqref" reference="eq:pair-bound"}.

> **Remark: Why the intercepts have no source-height cost** The source variable is $t$, and $ad$ enters only through its representative modulo $asR$. Theorem 3.1 is uniform in that residue. This differs from calling the affine Liouville special case, where all four affine coefficients and constants must lie in the small-polylogarithmic envelope.

# One set for all small pairs

The set in [\[prop:pair\]](../main.tex#L134){reference-type="ref" reference="prop:pair"} may depend on $(a,s)$. We now pay this dependence exactly once.

> **Lemma: Unique quotient-pair census** <span id="lem:pairs" label="lem:pairs">\[lem:pairs\]</span> For $Q\ge2$, $$\#\{(a,s)\in\mathbb N^2:as\le Q\}
>  =
>  \sum_{a\le Q}\left\lfloor\frac Qa\right\rfloor
>  \le Q(1+\log Q).
> \label{eq:pairs}$$ The same bound holds after imposing coprimality and oddness.

> **Proof** Drop the restrictions and use $\sum_{a\le Q}a^{-1}\le1+\log Q$.

> **Theorem: Uniform determinant-two Möbius-periodic corridor** <span id="thm:main" label="thm:main">\[thm:main\]</span> There are absolute constants $\eta_0,\kappa_0>0$ such that for every sufficiently large $X$ there is a set $\mathcal E_X^\star\subset[\sqrt X,X]$ with $$\boxed{
>  \frac1{\log X}\int_{\mathcal E_X^\star}\frac{dt}{t}
>  \ll(\log X)^{-\kappa_0}}
> \label{eq:main-exception}$$ for which the following is true. Uniformly over all data satisfying $$\begin{aligned}
>  &a,s,R\in\mathbb N,\qquad d,u\in\mathbb Z,\qquad
>  (a,s)=1,\qquad as\ {\rm odd},\qquad su-ad=2,\notag\\
>  &asR\le(\log X)^{\eta_0},\qquad
>  N\in[\sqrt X,X]\setminus\mathcal E_X^\star,
> \label{eq:envelope}\end{aligned}$$ and all $\rho:\mathbb Z/R\mathbb Z\to\mathbb C$, $$\boxed{
>  \frac{as}{N}
>  \left|
>  \sum_{\substack{z\in\mathbb Z\\N<ad+asz\le2N}}
>  \mu(d+sz)\mu(u+az)\rho(z)
>  \right|
>  \ll
>  \|\rho\|_\infty(\log X)^{-\kappa_0}.}
> \label{eq:main}$$

> **Proof** Let $\beta$ be as in [\[prop:pair\]](../main.tex#L134){reference-type="ref" reference="prop:pair"}, and choose $$0<\eta_0<\beta/4.$$ Take the union of $\mathcal E_{a,s;X}$ over all ordered pairs with $as\le(\log X)^{\eta_0}$. By \[[lem:pairs](../main.tex#L203),[eq:pair-exception](../main.tex#L146)\], its normalized logarithmic measure is $$\ll
>  (\log X)^{\eta_0+o(1)}(\log X)^{-\beta}
>  =
>  (\log X)^{-(\beta-\eta_0)+o(1)}.$$ Choose, for example, $\kappa_0=\beta/2$, after increasing the lower threshold for $X$. Outside this union, the estimate [\[eq:pair-bound\]](../main.tex#L162){reference-type="eqref" reference="eq:pair-bound"} holds for every pair. Its $(\log X)^{-\beta}$ right side is stronger than $(\log X)^{-\kappa_0}$.
>
> No union over $d,u,R$, residue classes or values of $\rho$ is made: for fixed $G_a,G_s$, the source exceptional set is already uniform in every allowed modulus and residue, and TPC-147 uses this same set for the full periodic reassembly.

# Squarefree and periodic reassembly audit

> **Proposition: Where the previous CRT costs went** <span id="prop:costs" label="prop:costs">\[prop:costs\]</span> Within [\[thm:main\]](../main.tex#L221){reference-type="ref" reference="thm:main"}:
>
> 1.  the two full Möbius factors are represented exactly by $G_a,G_s$, so there is no squarefree cutoff and no squarefree tail;
>
> 2.  the $R$ periodic residue classes have total native mass $R\cdot N/(asR)=N/(as)$, so there is no $R$-census exponent;
>
> 3.  the exceptional-set union is charged only to distinct multiplicative-function pairs $(G_a,G_s)$, equivalently to distinct $(a,s)$ in the declared range.

> **Proof** Part (i) is [\[eq:core\]](../main.tex#L119){reference-type="eqref" reference="eq:core"}, part (ii) is the TPC-147 periodic reassembly identity, and part (iii) is the construction of $\mathcal E_X^\star$ in [\[thm:main\]](../main.tex#L221){reference-type="ref" reference="thm:main"}.

Products of literal bounded periodic factors may be absorbed in $\rho$ if their exact combined period keeps $asR$ inside [\[eq:envelope\]](../main.tex#L237){reference-type="eqref" reference="eq:envelope"}. This can include a proved periodic coprimality mask, a fixed-period factor, or a rational phase whose exact denominator is small enough. It does not include a generic real phase or a nonperiodic physical multiplier.

# Actual-core scope versus the actual archive

The adjective “actual-core” means that the two Möbius forms and the determinant $2$ are literal; it does not assert that every frontier path has been lifted to such a record. The current TPC-143–146 interface leaves the occurrence-level fields $$(a,s,d,u),\quad as,\quad\text{residue},\quad\text{ordered interval},
 \quad R,\quad\text{masks and coefficient mass}$$ as `REQUIRED_MISSING`. Therefore the present frontier consumption remains $$\boxed{\mathsf{H1.frontier\_occurrence\_lift}=\textnormal{\textsc{not-testable}}.}$$ The machine certificate accepts these missing obligations; it does not manufacture numerical affine data from the finite cut sample.

Even after an occurrence lift is supplied, [\[thm:main\]](../main.tex#L221){reference-type="ref" reference="thm:main"} has the source interval $$N<ad+asz\le2N$$ at a nonexceptional scale. A different interval must come with an exact source-interval decomposition and an exceptional-set return. All initial prefixes are not automatic.

# Claim boundary

\@p0.50Y@ Statement & Level and status\
Exact quotient-Möbius determinant-two core & $\mathrm{L0}$, $\textnormal{\textsc{proved}}$.\
Uniform small-polylog periodic core theorem [\[eq:main\]](../main.tex#L249){reference-type="eqref" reference="eq:main"} & Actual-core $\mathrm{L1}$, $\textnormal{\textsc{proved}}$.\
Full squarefree return in this two-point core & Exact; no truncation tail.\
Bounded periodic return inside $asR$ envelope & $\mathrm{L1}$, $\textnormal{\textsc{proved}}$, no $R$ loss.\
Complete current frontier occurrence lift & $\textnormal{\textsc{not-testable}}$; required fields are absent.\
Nonperiodic physical weight or generic phase & $\textnormal{\textsc{open}}$.\
All prefixes or four-point Fejér input & $\textnormal{\textsc{open}}$.\
Positive $\mathrm{L2}$, fixed $X$-power, $1/400$ & Not proved.\
Prime-pair or twin-prime theorem & Not proved.\

The theorem is forward arithmetic progress: it replaces a squarefree-CRT shadow by a complete Möbius core on the correct fixed-two geometry. Its next legal consumer must solve the local exceptional-window and deterministic-prefix return without promoting logarithmic cancellation to an $X$-power.

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

@misc{WangTPC127,
  author       = {Wang, Liang},
  title        = {{The Determinant-Two Liouville Pullback}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-127-determinant-two-liouville-pullback}}
}

@misc{WangTPC140,
  author       = {Wang, Liang},
  title        = {{Exceptional Scales, Deterministic Selectors, and the Power-Saving Gate}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-140-exceptional-scale-selector-power-gate}}
}

@misc{WangTPC147,
  author = {Wang, Liang},
  title  = {{Periodic Reassembly Inside a Quantitative Multiplicative Correlation Corridor}},
  year   = {2026},
  note   = {TPC-147 manuscript}
}

@misc{WangTPC148,
  author = {Wang, Liang},
  title  = {{Multiplicative Quotient Lifts on Determinant-Two Fibers}},
  year   = {2026},
  note   = {TPC-148 manuscript}
}
```

<!-- SOURCE_BODY_END -->
