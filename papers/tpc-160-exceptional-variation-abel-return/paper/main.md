# **Exceptional-Variation Abel Return:\ Literal Weights, Almost-Prefixes, and the Atomic All-Prefix Barrier**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-160-exceptional-variation-abel-return.pdf](../tpc-160-exceptional-variation-abel-return.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-159 controls cumulative determinant-two Möbius sums at every endpoint outside a low range and an explicit dyadic exceptional shadow. We combine that result with exact Abel summation. A literal weight is charged by its variation on good and bad endpoints: good variation receives the logarithmic correlation saving, while bad variation receives only the trivial bound. This gives a sharp conditional route for physical weights. For a prefix cutoff the Abel derivative is one atom, so uniform all-prefix control requires the actual endpoint registry to avoid the shadow or a new pointwise theorem. Exceptional-set density alone cannot provide this.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** Abel summation; Möbius correlation; literal weight; exceptional variation; atomic prefix.

# Ordered fiber and the bad set

Retain $$q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az),$$ and a bounded period-$R$ function $\rho$. Let $$0<t_1<t_2<\cdots<t_m\le T$$ be the points $t(z_i)$, and put $$\sigma_i=c_{z_i}\rho(z_i),\qquad
 A_i=\sum_{j=1}^i\sigma_j.$$ TPC-159 fixes $$J=\lceil A\log_2\log X\rceil,\qquad
 \mathcal S_{X,J}=\bigcup_{j=1}^J2^j\mathcal E_X^\star$$ and proves a prefix estimate outside that shadow `\citep{WangTPC159}`. Define $$\mathcal B_{X,J}=[1,2^J\sqrt X)\cup\mathcal S_{X,J}.
\label{eq:bad}$$

# Exact Abel summation

For arbitrary literal weights $w_1,\ldots,w_m\in\mathbb C$, set $$d_i=w_i-w_{i+1}\quad(1\le i<m),\qquad d_m=w_m.
\label{eq:difference}$$

> **Lemma: Finite Abel identity**<span id="lem:abel" label="lem:abel">\[lem:abel\]</span> $$\sum_{i=1}^m\sigma_iw_i=\sum_{i=1}^mA_id_i.
> \label{eq:abel}$$

> **Proof** The coefficient of $\sigma_j$ on the right is $$\sum_{i=j}^{m-1}(w_i-w_{i+1})+w_m=w_j.$$

> **Definition: Exceptional variation**<span id="def:variation" label="def:variation">\[def:variation\]</span> Set $$V_{\rm good}(w)=
>  \sum_{\substack{1\le i\le m\\t_i\notin\mathcal B_{X,J}}}|d_i|,
>  \qquad
>  V_{\rm bad}(w)=
>  \sum_{\substack{1\le i\le m\\t_i\in\mathcal B_{X,J}}}|d_i|.$$

# The weighted return

Put $$\varepsilon_X=(\log X)^{-\kappa_0}+2^{-J}+\frac qT.
\label{eq:epsilon}$$

> **Theorem: Exceptional-variation return**<span id="thm:main" label="thm:main">\[thm:main\]</span> Assume the determinant-two and period envelope of TPC-159 and $T\le X$. Then $$\boxed{\;
>  \frac qT\left|\sum_{i=1}^m\sigma_iw_i\right|
>  \ll\lVert\rho\rVert_\infty
>  \left\{
>  \varepsilon_XV_{\rm good}(w)
>  +\left(1+\frac qT\right)V_{\rm bad}(w)
>  \right\}.\;}
> \label{eq:main}$$

> **Proof** If $t_i\notin\mathcal B_{X,J}$, then it lies in the endpoint range of TPC-159 and avoids the shadow. That theorem gives $$\frac q{t_i}|A_i|
>  \ll\lVert\rho\rVert_\infty
>  \left\{(\log X)^{-\kappa_0}+2^{-J}+\frac q{t_i}\right\}.$$ Since $t_i\le T$, this implies $$\frac qT|A_i|\ll\lVert\rho\rVert_\infty\varepsilon_X.$$ At a bad endpoint, use only $$|A_i|\le\lVert\rho\rVert_\infty\left(\frac Tq+1\right).$$ Insert these two estimates into [\[eq:abel\]](../main.tex#L105){reference-type="eqref" reference="eq:abel"} and separate the variation according to [\[def:variation\]](../main.tex#L116){reference-type="ref" reference="def:variation"}.

> **Corollary: Conditional logarithmic promotion**<span id="cor:promotion" label="cor:promotion">\[cor:promotion\]</span> Suppose $$2^J\sqrt X\le T\le X$$ and an actual source-locked registry proves, for some $\beta,\gamma>0$, $$V_{\rm good}(w)\le(\log X)^{\beta+o(1)},\qquad
>  V_{\rm bad}(w)\le(\log X)^{-\gamma+o(1)}$$ and $$\beta<\min\{\kappa_0,A\}.$$ Then the literal weighted periodic core has logarithmic exponent $$\min\{\min(\kappa_0,A)-\beta,\gamma\}+o(1).$$

Indeed, $q\le(\log X)^{\eta_0}$ and the terminal-scale lower bound make $q/T$ smaller than every fixed negative power of $\log X$. The conclusion then follows by inserting the two variation estimates in [\[eq:main\]](../main.tex#L146){reference-type="eqref" reference="eq:main"}. Without a terminal-scale lower bound, the factor $1+q/T$ in the bad-variation term cannot simply be discarded.

The corollary is a promotion rule. The current occurrence archive does not supply the literal $w$, its variation, or the required support theorem. Its fixed-$X$-power exponent remains zero, even when the displayed logarithmic exponent is positive.

# The atomic all-prefix barrier

For $1\le k\le m$, consider the literal prefix cutoff $$w_i^{(k)}=\mathbf1_{\{i\le k\}}.$$

> **Proposition: One-atom derivative**<span id="prop:atom" label="prop:atom">\[prop:atom\]</span> The differences in [\[eq:difference\]](../main.tex#L99){reference-type="eqref" reference="eq:difference"} satisfy $$d_i^{(k)}=\mathbf1_{\{i=k\}},$$ and hence $$V_{\rm bad}(w^{(k)})
>  =\mathbf1_{\{t_k\in\mathcal B_{X,J}\}}.
> \label{eq:badatom}$$

> **Proof** The step is constant except for its single drop after index $k$; when $k=m$, the terminal term $d_m=w_m$ is the same atom.

Let $\mathcal T_X$ be the actual registry of requested prefix endpoints. To obtain a uniform saving for all its step cutoffs from [\[thm:main\]](../main.tex#L135){reference-type="ref" reference="thm:main"}, one must prove $$\boxed{\quad
 \mathcal T_X\cap\mathcal B_{X,J}=\varnothing,
 \quad}
\label{eq:avoid}$$ or add a pointwise theorem covering the intersection. The logarithmic measure of the shadow cannot imply [\[eq:avoid\]](../main.tex#L234){reference-type="eqref" reference="eq:avoid"}. More precisely, enlarging the source exceptional set by $$\left\{2^{-J}T:
 T\in\mathcal T_X\cap[2^J\sqrt X,X]\right\}$$ does not change its continuous logarithmic measure, does not invalidate the source theorem outside the enlarged set, and places the displayed registry endpoints in the $j=J$ shadow copy. This is the atomic firewall of TPC-150 `\citep{WangTPC150}`, now tied to the exact dyadic shadow forced by the prefix proof.

# Phase and ledger interactions

A rational or sufficiently major-arc phase may enter the periodic factor using TPC-158 `\citep{WangTPC158}`; a generic phase remains outside this theorem. Alternatively, TPC-157 may charge a literal multiplier through periodic approximation `\citep{WangTPC157}`. These costs must be counted once. None converts a power of $\log X$ into a positive fixed-$X$ exponent.

The accompanying exact-rational audit verifies Abel summation, the good/bad variation partition, and the one-atom prefix derivative. It records the production weight and endpoint registry as $\mathrm{NOT\mbox{-}TESTABLE}$.

# Conclusion

The almost-endpoint theorem can now consume a literal weight through one precise quantity: its variation on the dyadic bad set. Smooth or well-distributed weights may pass this interface; atomic prefixes expose the unresolved endpoint directly. The next advance must therefore come from actual provenance plus a variation certificate, proved shadow avoidance, or a genuinely pointwise fixed-two theorem.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC150,
  author = {Wang, Liang},
  title  = {{Returning the Determinant-Two M\"obius Corridor:
             Terminal-Window Loss, Atomic Prefixes, and Split Log/Power Ledgers}},
  year   = {2026},
  note   = {TPC-150 manuscript}
}

@misc{WangTPC157,
  author = {Wang, Liang},
  title  = {{Periodic Approximation of Literal Multipliers on
             Determinant-Two M\"obius Fibers}},
  year   = {2026},
  note   = {TPC-157 manuscript}
}

@misc{WangTPC158,
  author = {Wang, Liang},
  title  = {{An Exact Major-Arc Gate for Additive Phases}},
  year   = {2026},
  note   = {TPC-158 manuscript}
}

@misc{WangTPC159,
  author = {Wang, Liang},
  title  = {{Dyadic-Shadow Lifting from Good-Scale M\"obius
             Correlations to Almost-Endpoint Prefixes}},
  year   = {2026},
  note   = {TPC-159 manuscript}
}
```

<!-- SOURCE_BODY_END -->
