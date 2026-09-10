# **Returning the Determinant-Two Möbius**\ **Corridor: Terminal-Window Loss, Atomic**\ **Prefixes, and Split Log/Power Ledgers**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-150-actual-corridor-window-selector-ledger.pdf](../tpc-150-actual-corridor-window-selector-ledger.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-149 proves power-of-log cancellation for the actual determinant-two Möbius periodic core at all scales outside a local exceptional set. We determine exactly what is lost when this theorem is restricted to a terminal window and then sampled by a physical prefix rule. If the source exceptional exponent is $\kappa_{\rm src}$ and $\log\omega=(\log X)^{\theta+o(1)}$, then its normalized terminal-window restriction directly certifies only $$\kappa_{\rm exc}=\kappa_{\rm src}+\theta-1.$$ A positive source density saving may therefore disappear on a short window.

We also give a sharp deterministic-prefix firewall. Adding any finite list of requested endpoints to an exceptional set does not change its logarithmic measure. Hence exceptional density alone cannot certify a prescribed discrete prefix family. A pointwise theorem, proved exceptional avoidance, or a quantitative smoothing and selector crosswalk is required.

Finally, we separate the power-of-log return ledger from the fixed-$X$-power ledger. Even a positive logarithmic exponent has $\sigma_{\rm power}=0$, so it cannot pay a positive physical endpoint loss or $1/400$. Because the frontier occurrence lift is still missing, the current actual return is $\textnormal{\textsc{not-testable}}$, not positive $\mathrm{L2}$ and not a prime-pair result.

<!-- SOURCE_BODY_BEGIN -->

# The sourced core and the missing occurrence lift

TPC-149 proves that there are constants $\eta_0,\kappa_{\rm src}>0$ and, for every ambient $X$, a set $$\mathcal E_X^\star\subset[\sqrt X,X]$$ such that $$\frac1{\log X}\int_{\mathcal E_X^\star}\frac{dt}{t}
 \ll(\log X)^{-\kappa_{\rm src}},
\label{eq:source-density}$$ and the literal determinant-two Möbius periodic core has power-of-log cancellation at each $N\in[\sqrt X,X]\setminus\mathcal E_X^\star$ `\citep{WangTPC149,TaoTeravainen2026}`.

This core theorem is uniform under a small-polylogarithmic bound on the product of the progression modulus and exact periodic period. It does not include a nonperiodic physical multiplier, a generic phase, an arbitrary interval or every prefix. In particular, it is not the four-sign Fejér input required by TPC-130 `\citep{WangTPC130}`.

Moreover, the current TPC-143–146 frontier interface has not yet constructed the occurrence records carrying $$(a,s,d,u),\quad as,\quad\text{residue},\quad\text{ordered interval},
 \quad R,\quad\text{masks, prefixes and coefficient mass}.$$ These fields are `REQUIRED_MISSING`. Thus $$\boxed{\mathsf{H1.frontier\_occurrence\_lift}=\textnormal{\textsc{not-testable}}.}
\label{eq:first-missing}$$ The results below give the legal return once those records exist; they do not manufacture them.

# A local exceptional set on a terminal window

Let $$J_X=[X/\omega,X],
 \qquad
 m_{J_X}(E)
 =
 \frac1{\log\omega}\int_{E\cap J_X}\frac{dt}{t}.$$ We first use one ambient shell, so we explicitly require $$J_X\subset[\sqrt X,X],
 \qquad\text{equivalently}\qquad 1<\omega\le\sqrt X.
\label{eq:containment}$$ A longer window needs a declared shell decomposition and the union of all shell-level exceptional sets.

> **Proposition: Local shell to terminal window** <span id="prop:window" label="prop:window">\[prop:window\]</span> Under [\[eq:source-density\]](../main.tex#L92){reference-type="eqref" reference="eq:source-density"} and [\[eq:containment\]](../main.tex#L134){reference-type="eqref" reference="eq:containment"}, $$\boxed{
>  m_{J_X}(\mathcal E_X^\star)
>  \ll
>  \min\left\{
>  1,\frac{(\log X)^{1-\kappa_{\rm src}}}{\log\omega}
>  \right\}.}
> \label{eq:window}$$ If $$\log\omega=(\log X)^{\theta+o(1)},
> \label{eq:theta}$$ then the exponent supplied by this estimate is $$\boxed{\kappa_{\rm exc}
>  =\kappa_{\rm src}+\theta-1.}
> \label{eq:exception-exponent}$$ It is positive only if $\kappa_{\rm src}+\theta>1$.

> **Proof** The numerator defining $m_{J_X}$ is at most the integral over $\mathcal E_X^\star$, which is $O((\log X)^{1-\kappa_{\rm src}})$ by [\[eq:source-density\]](../main.tex#L92){reference-type="eqref" reference="eq:source-density"}. Divide by $\log\omega$, and also use $m_{J_X}\le1$. Substitution of [\[eq:theta\]](../main.tex#L154){reference-type="eqref" reference="eq:theta"} gives [\[eq:exception-exponent\]](../main.tex#L160){reference-type="eqref" reference="eq:exception-exponent"}.

> **Remark: No duplicated pair census** TPC-149 already forms one exceptional set by unioning over all allowed $(a,s)$ in its universal envelope. Its pair census must not be charged again in [\[eq:window\]](../main.tex#L149){reference-type="eqref" reference="eq:window"}. A record-aware variant may instead union only the actually occurring pairs and endpoint dilates, but then those counts must be entered exactly once.

# A sharp deterministic-prefix firewall

> **Theorem: Discrete endpoints are invisible to density** <span id="thm:atomic-set" label="thm:atomic-set">\[thm:atomic-set\]</span> Let $T_X\subset[\sqrt X,X]$ be any finite set of deterministic scales. For every measurable $E_X\subset[\sqrt X,X]$, $$\int_{E_X\cup T_X}\frac{dt}{t}
>  =
>  \int_{E_X}\frac{dt}{t}.$$ Consequently, an exceptional-set density theorem alone cannot imply that even one prescribed endpoint in $T_X$ lies outside the exceptional set.

> **Proof** Every finite set has Lebesgue, hence logarithmic, measure zero. Therefore adjoining $T_X$ leaves the integral unchanged. Both $E_X$ and $E_X\cup T_X$ obey exactly the same density bound, while the latter contains every requested endpoint.

This is a logical nonimplication, not a claim that the arithmetic exceptional set actually contains the endpoints. It shows that density information cannot decide the question.

Let $\nu_X$ be the probability measure with which a proposed physical synthesis samples $J_X$. TPC-140 uses the domination condition $$\nu_X(A)\le K_Xm_{J_X}(A)
\label{eq:selector}$$ for every Borel set $A$ `\citep{WangTPC140}`.

> **Corollary: Atomic selector stop** <span id="cor:atomic" label="cor:atomic">\[cor:atomic\]</span> If $\nu_X$ gives positive mass to any deterministic endpoint, no finite $K_X$ satisfies [\[eq:selector\]](../main.tex#L214){reference-type="eqref" reference="eq:selector"}.

> **Proof** Apply [\[eq:selector\]](../main.tex#L214){reference-type="eqref" reference="eq:selector"} to the singleton endpoint. Its $m_{J_X}$-measure is zero, while its $\nu_X$-mass is positive.

There are three legal exits:

1.  a pointwise theorem uniform in every actual prefix;

2.  an independent theorem proving that the requested endpoints avoid the actual exceptional sets; or

3.  an exact smoothing identity, a quantitative stability bound and selector domination for the smoothed measure.

# The power-of-log return ledger

Suppose all occurrence records and normalizations have been supplied. Write $$\begin{aligned}
 \varepsilon_{\rm corr}
 &\ll(\log X)^{-\kappa_{\rm corr}+o(1)},\notag\\
 m_{J_X}(\mathcal E_{\rm tot})
 &\ll(\log X)^{-\kappa_{\rm exc}+o(1)}.
\label{eq:two-errors}\end{aligned}$$ Boundedness and the good/bad split give $$\kappa_{\rm aff}
 =
 \min\{\kappa_{\rm corr},\kappa_{\rm exc}\}.
\label{eq:aff}$$

Let the ratio of the literal outer absolute reassembly mass to the declared physical comparison mass cost $(\log X)^{\kappa_{\rm cen}+o(1)}$. Let selector and nonperiodic weight/Abel return cost respectively $(\log X)^{\kappa_{\rm sel}+o(1)}$ and $(\log X)^{\kappa_{\rm BV}+o(1)}$. Unknown costs are not zero. If a separate remaining tail saves $(\log X)^{-\kappa_{\rm tail}+o(1)}$, then:

> **Theorem: Typed logarithmic return** <span id="thm:log-ledger" label="thm:log-ledger">\[thm:log-ledger\]</span> Under the preceding proved inputs, the exponent certified by their triangle-inequality return is $$\boxed{
>  \kappa_{\rm returned}^{\rm cert}
>  =
>  \min\left\{
>  \kappa_{\rm tail},
>  \kappa_{\rm aff}
>  -\kappa_{\rm cen}
>  -\kappa_{\rm sel}
>  -\kappa_{\rm BV}
>  \right\}.}
> \label{eq:log-ledger}$$ For the exact quotient-Möbius core of TPC-149 there is no squarefree tail, so the first entry is omitted unless another literal remainder is present.

> **Proof** On good scales, sum the component estimates against the actual outer absolute mass. On bad scales, use boundedness and their normalized mass. This gives [\[eq:aff\]](../main.tex#L254){reference-type="eqref" reference="eq:aff"}; the three multiplicative return costs subtract their exponents. A separately bounded tail is added, so the weaker of the two savings survives.

Periodic residue classes inside one TPC-149 record have already been reassembled with their native densities and do not contribute to $\kappa_{\rm cen}$. Distinct outer records and the mismatch between their arithmetic and physical comparison masses may do so. The displayed exponent is a guaranteed ledger output, not a claim that the true error has exactly this order; it gives decay only when it is strictly positive.

# The separate fixed-$X$-power ledger

> **Proposition: Logarithmic saving has zero $X$-power** <span id="prop:zero-power" label="prop:zero-power">\[prop:zero-power\]</span> For every fixed $\kappa>0$, the largest fixed $\sigma\ge0$ certified by $$(\log X)^{-\kappa+o(1)}
>  \le X^{-\sigma+o(1)}$$ is $\sigma=0$.

> **Proof** For every fixed $\sigma>0$, $$X^\sigma(\log X)^{-\kappa}\longrightarrow\infty.$$ Thus a power of logarithm decays more slowly than every positive power of $X$.

Consequently, $$\boxed{\sigma_{\rm power}=0}
\label{eq:power}$$ for the present corridor, even when $\kappa_{\rm returned}^{\rm cert}>0$. It cannot pay a positive physical occurrence loss, the local $1/400$ target, or a strict endpoint. This is a scale comparison, not a theorem that a future stronger arithmetic estimate is impossible.

# Actual status and machine contract

The deterministic audit imports TPC-147–149 by content hashes for integrity only, records every occurrence field required from TPC-143–146, and preserves [\[eq:first-missing\]](../main.tex#L115){reference-type="eqref" reference="eq:first-missing"}. Its rational ledger contains a hypothetical positive log case and an equality case that must stop. Neither is evidence about the actual packet. The actual record retains unknown values and is $\textnormal{\textsc{not-testable}}$.

\@p0.50Y@ Statement & Level and status\
Terminal-window estimate [\[eq:window\]](../main.tex#L149){reference-type="eqref" reference="eq:window"} & Exact measure theorem, $\textnormal{\textsc{proved}}$.\
Deterministic-prefix nonimplication & Exact firewall, $\textnormal{\textsc{proved}}$.\
Logarithmic ledger [\[eq:log-ledger\]](../main.tex#L281){reference-type="eqref" reference="eq:log-ledger"} & Conditional typed $\mathrm{L1}$.\
TPC-149 actual Möbius periodic core & $\mathrm{L1}$, $\textnormal{\textsc{proved}}$.\
Frontier occurrence lift & $\textnormal{\textsc{not-testable}}$, first structural missing item.\
Physical weight, generic phase, all-prefix return & $\textnormal{\textsc{open}}$ after occurrence lift.\
Four-point H3 or positive $\mathrm{L2}$ & Not proved.\
Positive $X$-power, $1/400$, endpoint pass & Not proved.\
Prime-pair or twin-prime theorem & Not proved.\

Thus the new corridor is mathematically real but remains upstream of the decisive physical and all-prefix gates. Its correct output is a stronger $\mathrm{L1}$ arithmetic node plus an explicit return obstruction, not an H3 or endpoint certificate.

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

@misc{WangTPC130,
  author       = {Wang, Liang},
  title        = {{A Fejer Four-Sign Gate for the Literal H3 Packet}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-130-fejer-four-sign-h3-gate}}
}

@misc{WangTPC140,
  author       = {Wang, Liang},
  title        = {{Exceptional Scales, Deterministic Selectors, and the Power-Saving Gate}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-140-exceptional-scale-selector-power-gate}}
}

@misc{WangTPC141,
  author       = {Wang, Liang},
  title        = {{Source-Locked Integration at the First Unsupported Carrier}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-141-source-locked-cut-arithmetic-integration}}
}

@misc{WangTPC149,
  author = {Wang, Liang},
  title  = {{A Small-Polylogarithmic Determinant-Two Mobius Corridor}},
  year   = {2026},
  note   = {TPC-149 manuscript}
}
```

<!-- SOURCE_BODY_END -->
