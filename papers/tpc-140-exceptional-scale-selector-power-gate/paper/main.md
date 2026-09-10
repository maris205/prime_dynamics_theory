# **Exceptional-Scale Selection and the Actual Fixed-Two Power Gate**\ A Carleson Return Interface for H3

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-140-exceptional-scale-selector-power-gate.pdf](../tpc-140-exceptional-scale-selector-power-gate.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

An arithmetic theorem valid at almost all logarithmic scales need not control a deterministically selected physical prefix. We give two noncircular return interfaces for a fixed-two TPC packet. The first is a direct uniform all-prefix theorem. The second requires the actual selector measure $\nu_X$ to be dominated by normalized logarithmic measure $m_X$: $$\nu_X(E)\le K_Xm_X(E)$$ for every Borel set $E$. An arithmetic scale-average error $\varepsilon_X$ then returns as $K_X\varepsilon_X$. Combining this with squarefree-tail, component-census and bounded-variation losses gives the exact amplitude ledger $$\sigma_{\rm raw}
 =
 \min\{\eta_{\rm tail},
 \sigma_{\rm aff}-\ell_{\rm sel}-\ell_{\rm cen}-\ell_{\rm BV}\}.$$ TPC-131 closes only if $\sigma_{\rm raw}>\Lambda_{\rm phys}$. Atomic selectors are singular with respect to continuous logarithmic measure, so a discrete all-prefix family requires a pointwise theorem or a proved smoothing crosswalk. Current fixed-data logarithmic inputs have no positive $X$-power exponent. Tao–Teräväinen’s 2026 small-polylog affine theorem does add a genuine power-of-log almost-scale corridor. Its cumulative exceptional-set estimate is not automatically the same power-of-log estimate on an arbitrary terminal window: that conversion has a separate exact loss. After this window loss, selector loss and reassembly losses, it can yield qualitative cancellation only if the full logarithmic exponent ledger stays positive. It still has $X$-power exponent zero. The actual selector and all-prefix gates remain open; no positive $\mathrm{L2}$, H3, or $1/400$ conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Why almost all scales are not all prefixes

For a bounded arithmetic coefficient $b(n)$, write $$C(t)=\frac1t\sum_{t<n\le2t}b(n).$$ An almost-scale theorem has the shape $$\frac1{\log\omega}
 \int_{x/\omega}^{x}|C(t)|\frac{dt}{t}
 \le\varepsilon_X.
\label{eq:almost-scale}$$ Helfgott and Radziwiłł prove a quantitative almost-all-scale conclusion for the consecutive Liouville correlation `\citep{HelfgottRadziwill2021}`. We use [\[eq:almost-scale\]](../main.tex#L87){reference-type="eqref" reference="eq:almost-scale"} as an abstract normalized interface rather than attributing this exact continuous formulation to that source. TPC-138 separates its even-carrier shift-one consequence from the active odd carrier and also records the newer Tao–Teräväinen small-polylog affine corridor `\citep{WangTPC138,TaoTeravainen2026}`. The remaining logical issue is independent of determinant: a theorem outside a small exceptional set is still not a deterministic all-prefix theorem. Moreover, a cumulative exceptional-set bound up to $x$ is not automatically a normalized bound on every shorter terminal window.

TPC-130 requires the declared actual block-prefix family `\citep{WangTPC130}`. A deterministic list of its endpoints may lie inside the exceptional scale set unless a return theorem prevents that concentration.

> **Proposition: Average-to-maximum inference is invalid** <span id="prop:no-max" label="prop:no-max">\[prop:no-max\]</span> From [\[eq:almost-scale\]](../main.tex#L87){reference-type="eqref" reference="eq:almost-scale"} alone one cannot deduce $$\sup_{x/\omega\le t\le x}|C(t)|=o(1).$$ The failure persists even for bounded measurable $C$.

> **Proof** Choose a set $E_X$ of normalized logarithmic measure $\varepsilon_X$, and put $C=\mathbf 1_{E_X}$. Then [\[eq:almost-scale\]](../main.tex#L87){reference-type="eqref" reference="eq:almost-scale"} holds, while the supremum is one.

This counterexample is analytic, not a construction of Liouville values. It proves that an additional selector or pointwise premise is logically necessary.

# Two legal return interfaces

Let $$J_X=[x/\omega,x],\qquad
 m_X(E)=\frac1{\log\omega}\int_{E\cap J_X}\frac{dt}{t}.$$ Thus $m_X$ is a probability measure on $J_X$.

> **Proposition: Global exceptional density versus a terminal window** <span id="prop:global-to-window" label="prop:global-to-window">\[prop:global-to-window\]</span> Suppose an exceptional set $\mathcal E\subset[1,\infty)$ satisfies $$\frac1{\log y}
>  \int_{[1,y]\cap\mathcal E}\frac{dt}{t}
>  \ll(\log y)^{-c_0}
>  \qquad(y\ge2).
> \label{eq:global-exceptional}$$ Then $$\boxed{
>  m_X(\mathcal E)
>  \ll
>  \min\left\{
>  1,\frac{(\log x)^{1-c_0}}{\log\omega}
>  \right\}.}
> \label{eq:window-exceptional}$$ In particular, [\[eq:global-exceptional\]](../main.tex#L144){reference-type="eqref" reference="eq:global-exceptional"} alone does not give $m_X(\mathcal E)\ll(\log x)^{-c_0}$ for an arbitrary $\omega=\omega(x)$.

> **Proof** The numerator defining $m_X(\mathcal E)$ is bounded by the integral over $[1,x]\cap\mathcal E$, which is $O((\log x)^{1-c_0})$ by [\[eq:global-exceptional\]](../main.tex#L144){reference-type="eqref" reference="eq:global-exceptional"}. Divide by $\log\omega$, and also use $m_X(\mathcal E)\le1$.

> **Remark: Window exponent** <span id="rem:window-exponent" label="rem:window-exponent">\[rem:window-exponent\]</span> If $\log\omega=(\log x)^{\theta+o(1)}$, then the sourced cumulative bound proves a positive power-of-log saving for the exceptional mass only when $\theta+c_0>1$; the available exponent is then $\theta+c_0-1$. At or below that threshold the source bound by itself gives no decay on the terminal window. If several endpoint dilates or CRT pullbacks are required, the corresponding union must be bounded before an exceptional-window exponent is entered.

> **Definition: Pointwise interface** <span id="def:pointwise" label="def:pointwise">\[def:pointwise\]</span> For an actual component family $\mathcal F_X$, the pointwise interface with error $\varepsilon_X$ is $$\sup_{f\in\mathcal F_X}
>  \sup_{T\in I_f}
>  \frac{|S_f(T)|}{V_f(T)}
>  \le\varepsilon_X,$$ after zero-mass prefixes have been discharged. Every mask, weight, phase, origin and prefix belongs to the theorem statement.

> **Definition: Selector domination** <span id="def:selector" label="def:selector">\[def:selector\]</span> Let $\nu_X$ be the probability measure with which the literal physical synthesis samples the scale variable. It has selector constant $K_X\ge1$ if $$\nu_X(E)\le K_Xm_X(E)
> \label{eq:domination}$$ for every Borel $E\subseteq J_X$.

> **Theorem: Carleson selector return** <span id="thm:selector" label="thm:selector">\[thm:selector\]</span> Suppose [\[eq:almost-scale\]](../main.tex#L87){reference-type="eqref" reference="eq:almost-scale"} holds for a nonnegative measurable function $|C|$, and [\[def:selector\]](../main.tex#L196){reference-type="ref" reference="def:selector"} holds. Then $$\boxed{
>  \int_{J_X}|C(t)|\,d\nu_X(t)
>  \le K_X\varepsilon_X.}
> \label{eq:return}$$

> **Proof** The measure inequality [\[eq:domination\]](../main.tex#L202){reference-type="eqref" reference="eq:domination"} is equivalent to $\nu_X\ll m_X$ with Radon–Nikodym derivative at most $K_X$ almost everywhere. Integrate $|C|$ against that derivative and use [\[eq:almost-scale\]](../main.tex#L87){reference-type="eqref" reference="eq:almost-scale"}.

> **Proposition: Atomic selector stop** <span id="prop:atomic" label="prop:atomic">\[prop:atomic\]</span> If $\nu_X$ has an atom of positive mass, then [\[eq:domination\]](../main.tex#L202){reference-type="eqref" reference="eq:domination"} fails for every finite $K_X$.

> **Proof** For an atom $t_0$, one has $\nu_X(\{t_0\})>0$, while $m_X(\{t_0\})=0$.

Therefore a literal discrete prefix maximum cannot be called a Carleson-distributed scale family. One must instead prove [\[def:pointwise\]](../main.tex#L182){reference-type="ref" reference="def:pointwise"}, or prove a smoothing identity that replaces each atom by an absolutely continuous window and bounds the resulting stability error.

> **Remark: Family-level use** <span id="rem:family-selector" label="rem:family-selector">\[rem:family-selector\]</span> controls the $\nu_X$-average of one nonnegative error; it does not control a supremum. For a component family, one needs either a uniform arithmetic error and uniform selector constant component by component, or one joint domination statement on component–scale space. The total absolute component mass is then charged exactly once as the census loss below.

# Power transport

Assume now that every input is expressed at amplitude scale. Let $$\varepsilon_X=X^{-\sigma_{\rm aff}+o(1)}$$ be either a pointwise arithmetic rate or an almost-scale rate. For the selector route put $$K_X=X^{\ell_{\rm sel}+o(1)};$$ for the pointwise route set $\ell_{\rm sel}=0$. Let $\ell_{\rm cen}$ be the theorem-backed weighted component census, $\ell_{\rm BV}$ the cost of returning the literal physical weight and phase from the arithmetic coefficient, and let the squarefree tail save $X^{-\eta_{\rm tail}+o(1)}$. All loss exponents in this paragraph are nonnegative and every input is already normalized at amplitude scale.

> **Theorem: Typed raw exponent** <span id="thm:raw" label="thm:raw">\[thm:raw\]</span> Under the preceding proved premises, the returned raw amplitude saving is $$\boxed{
>  \sigma_{\rm raw}
>  =
>  \min\left\{
>  \eta_{\rm tail},
>  \sigma_{\rm aff}
>  -\ell_{\rm sel}
>  -\ell_{\rm cen}
>  -\ell_{\rm BV}
>  \right\}.}
> \label{eq:raw}$$ It is a positive power only if both entries of the minimum are positive.

> **Proof** The tail is bounded separately. On the retained part, [\[thm:selector\]](../main.tex#L208){reference-type="ref" reference="thm:selector"} costs $X^{\ell_{\rm sel}+o(1)}$, while the weighted census and BV return cost $X^{\ell_{\rm cen}+\ell_{\rm BV}+o(1)}$. Multiplying these bounds subtracts their exponents from $\sigma_{\rm aff}$. Adding the tail selects the weaker saving.

> **Corollary: Endpoint gate** <span id="cor:endpoint" label="cor:endpoint">\[cor:endpoint\]</span> If the complete physical occurrence loss of TPC-131 is $\Lambda_{\rm phys}$, then the selected route proves the final $o(X)$ conclusion only under the strict inequality $$\sigma_{\rm raw}>\Lambda_{\rm phys}.
> \label{eq:endpoint}$$ Equality is a stop. If the local MVP1 raw target is fixed to $1/400$, every upstream loss must be included before that target is recorded. The exact remaining endpoint margin is $$\sigma_{\rm final}
>  :=
>  \sigma_{\rm raw}-\Lambda_{\rm phys}.$$

> **Proof** Insert [\[eq:raw\]](../main.tex#L288){reference-type="eqref" reference="eq:raw"} into the typed synthesis theorem of TPC-131 `\citep{WangTPC131}`.

# The logarithmic corridor and its separate ledger

TPC-137 gives a qualitative fixed-data logarithmic theorem `\citep{WangTPC137}`. TPC-139 shows that only a non-effective slow growing data envelope follows from that theorem automatically, but also records Tao–Teräväinen’s explicit small-polylog affine estimate outside a small logarithmic-density exceptional set `\citep{WangTPC139,TaoTeravainen2026}`. After the literal component and scale normalization has been matched, boundedness turns their good-scale estimate plus the exceptional-set density bound into an interface of the form [\[eq:almost-scale\]](../main.tex#L87){reference-type="eqref" reference="eq:almost-scale"} with a power-of-log error. That matching is one of the eligibility checks, not an automatic property of the physical archive. If $$\varepsilon_X=(\log\log X)^{-c}$$ or $(\log X)^{-c}$, or merely $o(1)$, then the largest fixed $X$-power exponent certified by that statement is $$\sigma_{\rm aff}=0.$$ Indeed, for every fixed $\sigma>0$, $(\log\log X)^{-c}$ is eventually larger than $X^{-\sigma}$. Thus a logarithmic rate is real cancellation but cannot be entered as $1/400$.

Even a qualitative conclusion after selector transport requires the explicit product $K_X\varepsilon_X\to0$. The labels $K_X=X^{o(1)}$ and $\varepsilon_X=o(1)$, without rates, do not imply that product tends to zero.

There is nevertheless a useful logarithmic ledger. Separate the nonexceptional correlation rate from the exceptional-window mass. Suppose $$\varepsilon_X^{\rm corr}
 =(\log X)^{-\kappa_{\rm corr}+o(1)},\qquad
 m_X(\mathcal E_{\rm tot})
 =(\log X)^{-\kappa_{\rm exc}+o(1)},$$ where $\mathcal E_{\rm tot}$ is the union of every required pulled-back exceptional set, and put $$\kappa_{\rm aff}
 =
 \min\{\kappa_{\rm corr},\kappa_{\rm exc}\}.
\label{eq:effective-log-aff}$$ Indeed, boundedness and the split into $\mathcal E_{\rm tot}$ and its complement give an arithmetic scale-average error of order $\varepsilon_X^{\rm corr}+m_X(\mathcal E_{\rm tot})$. Also suppose $$K_X=(\log X)^{\kappa_{\rm sel}+o(1)}.$$ Write $\kappa_{\rm cen},\kappa_{\rm BV}$ for the power-of-log census and return losses, while the tail saves $(\log X)^{-\kappa_{\rm tail}+o(1)}$. The same proof as [\[thm:raw\]](../main.tex#L274){reference-type="ref" reference="thm:raw"} gives $$\boxed{
 \kappa_{\rm raw}
 =
 \min\left\{
 \kappa_{\rm tail},
 \kappa_{\rm aff}-\kappa_{\rm sel}
 -\kappa_{\rm cen}-\kappa_{\rm BV}
 \right\}.}
\label{eq:log-ledger}$$ If $\kappa_{\rm raw}>0$, this closes a qualitative almost-scale/selector return. It still records $\sigma_{\rm raw}=0$ in the $X$-power ledger and therefore cannot pay any fixed positive $\Lambda_{\rm phys}$. show that $\kappa_{\rm exc}$ cannot simply be copied from the source’s global-density exponent for an arbitrary terminal window.

# Certificate schema and current verdict

A route record must contain at least $$\begin{array}{ll}
\texttt{carrier}:&\text{actual fixed-two carrier hash},\\
\texttt{arithmetic}:&\sigma_{\rm aff}\text{ and theorem source},\\
\texttt{return\_mode}:&\texttt{pointwise}\text{ or }\texttt{selector},\\
\texttt{selector}:&K_X\text{ and domination source if used},\\
\texttt{losses}:&\eta_{\rm tail},\ell_{\rm cen},\ell_{\rm BV},\\
\texttt{endpoint}:&\Lambda_{\rm phys}\text{ and strict comparison},\\
\texttt{evidence}:&\text{proved, conditional, finite, or open}.
\end{array}$$ The deterministic script checks this ledger with exact rational arithmetic. It includes a hypothetical strict pass solely to test the formula, an equality case that must stop, and the current zero-power case. The hypothetical record is not evidence about an actual coefficient.

| Statement                                                                                                            | Level and status                                                |
|:---------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------|
| Selector implication [\[eq:return\]](../main.tex#L215){reference-type="eqref" reference="eq:return"}                 | Exact measure theorem ($\mathrm{L0}$).                          |
| Atomic selector obstruction                                                                                          | Exact firewall ($\mathrm{L0}$).                                 |
| Raw exponent formula [\[eq:raw\]](../main.tex#L288){reference-type="eqref" reference="eq:raw"}                       | Conditional typed synthesis ($\mathrm{L1}$).                    |
| Logarithmic exponent formula [\[eq:log-ledger\]](../main.tex#L398){reference-type="eqref" reference="eq:log-ledger"} | Conditional qualitative return ($\mathrm{L1}$); zero $X$-power. |
| Actual growing determinant-two power theorem                                                                         | Open.                                                           |
| Actual pointwise prefixes or selector domination                                                                     | Open / not supplied.                                            |
| Positive fixed-$h_0$ L2, H3, or $1/400$                                                                              | Not proved.                                                     |

The present arithmetic subgraph therefore emits no <span class="smallcaps">arithmetic frontier</span> certificate. Without a complete actual archive it remains <span class="smallcaps">not testable</span>; even after that archive arrives, the first arithmetic missing item is a growing determinant-two rate together with either a pointwise all-prefix theorem or a valid selector crosswalk.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{HelfgottRadziwill2021,
  author = {Helfgott, Harald Andr{\'e}s and Radziwi{\l}{\l}, Maksym},
  title  = {{Expansion, Divisibility and Parity}},
  year   = {2021},
  eprint = {2103.06853},
  archivePrefix = {arXiv},
  primaryClass = {math.NT}
}

@misc{TaoTeravainen2026,
  author = {Tao, Terence and Ter{\"a}v{\"a}inen, Joni},
  title  = {{Quantitative Correlations and Some Problems on Prime
             Factors of Consecutive Integers}},
  year   = {2026},
  eprint = {2512.01739v2},
  archivePrefix = {arXiv},
  primaryClass = {math.NT}
}

@misc{WangTPC130,
  author = {Wang, Liang},
  title  = {{A Fej{\'e}r Four-Sign Gate for H3}},
  year   = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-130-fejer-four-sign-h3-gate}}
}

@misc{WangTPC131,
  author = {Wang, Liang},
  title  = {{End-to-End Endpoint Synthesis on the Literal
             Fixed-Shift Carrier}},
  year   = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-131-end-to-end-typed-exponent-synthesis}}
}

@misc{WangTPC137,
  author = {Wang, Liang},
  title  = {{Prime-Square Closure of the Frozen Determinant-Two
             Logarithmic Shadow}},
  year   = {2026},
  note   = {TPC-137 manuscript}
}

@misc{WangTPC138,
  author = {Wang, Liang},
  title  = {{Quantitative Shift-One Shadows of the
             Determinant-Two Frame}},
  year   = {2026},
  note   = {TPC-138 manuscript}
}

@misc{WangTPC139,
  author = {Wang, Liang},
  title  = {{From Frozen Affine Pairs to Growing CRT Fibers}},
  year   = {2026},
  note   = {TPC-139 manuscript}
}
```

<!-- SOURCE_BODY_END -->
