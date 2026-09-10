# **Periodic Approximation of Literal Multipliers on\ Determinant-Two Möbius Fibers**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-157-literal-weight-periodic-approximation.pdf](../tpc-157-literal-weight-periodic-approximation.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The determinant-two corridor of TPC-149 bounds every bounded periodic multiplier on a literal two-Möbius core, uniformly outside one exceptional set. We give the exact interface from that theorem to an arbitrary literal multiplier. The resulting bound is the sum of the periodic-core saving and a normalized $L^1$ approximation error. The unpenalized error term separates over residue fibers; its quadratic surrogate is solved by fiber means. The supremum-norm penalty in the full cost still couples those fibers. This is a positive actual-core weight-interface theorem. It is not yet a theorem for the missing physical occurrence registry, a generic phase or all prefixes, and its fixed-$X$-power exponent is zero.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** Möbius correlation; determinant two; periodic approximation; literal multiplier; exceptional scales.

# The inherited periodic corridor

Fix integers $$a,s,R\ge1,\qquad d,u\in\mathbb Z,\qquad
 (a,s)=1,\qquad as\ {\rm odd},\qquad su-ad=2,$$ and put $$q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az),$$ $$I_N=\{z\in\mathbb Z:N<t(z)\le2N\}.$$ TPC-149 proves the following consequence of the quantitative affine correlation theorem of `\citet{TaoTeravainen2026}`.

> **Theorem: TPC-149 periodic corridor**<span id="thm:149" label="thm:149">\[thm:149\]</span> There are absolute $\eta_0,\kappa_0>0$ such that for every sufficiently large $X$ there is $\mathcal E_X^\star\subset[\sqrt X,X]$ satisfying $$\frac1{\log X}\int_{\mathcal E_X^\star}\frac{dt}{t}
>  \ll(\log X)^{-\kappa_0}.$$ If $qR\le(\log X)^{\eta_0}$ and $N\in[\sqrt X,X]\setminus\mathcal E_X^\star$, then, simultaneously for every period-$R$ function $\rho$, $$\frac qN\left|\sum_{z\in I_N}c_z\rho(z)\right|
>  \ll\lVert\rho\rVert_\infty(\log X)^{-\kappa_0}.
> \label{eq:periodic}$$

The word “simultaneously” is essential: choosing an approximant after seeing $w$ does not require a union over its values.

# The literal-weight interface

> **Definition: Periodic approximation cost**<span id="def:cost" label="def:cost">\[def:cost\]</span> For $w:I_N\to\mathbb C$, define $$\mathfrak A_{R,N}(w)=
>  \inf_{\substack{\rho:\mathbb Z\to\mathbb C\\\rho(z+R)=\rho(z)}}
>  \left\{
>  \lVert\rho\rVert_\infty(\log X)^{-\kappa_0}
>  +\frac qN\sum_{z\in I_N}|w(z)-\rho(z)|
>  \right\}.
> \label{eq:cost}$$

> **Theorem: Literal-weight periodic approximation**<span id="thm:main" label="thm:main">\[thm:main\]</span> Under the hypotheses of [\[thm:149\]](../main.tex#L81){reference-type="ref" reference="thm:149"}, $$\boxed{\;
>  \frac qN\left|\sum_{z\in I_N}c_zw(z)\right|
>  \ll \mathfrak A_{R,N}(w).\;}
> \label{eq:main}$$ The exceptional set is exactly the one in [\[thm:149\]](../main.tex#L81){reference-type="ref" reference="thm:149"}.

> **Proof** For any admissible $\rho$, $$\sum_{I_N}c_zw(z)
>  =
>  \sum_{I_N}c_z\rho(z)
>  +\sum_{I_N}c_z\{w(z)-\rho(z)\}.$$ The first term is controlled by [\[eq:periodic\]](../main.tex#L95){reference-type="eqref" reference="eq:periodic"}. Since $|c_z|\le1$, the normalized modulus of the second is at most $$\frac qN\sum_{z\in I_N}|w(z)-\rho(z)|.$$ Take the infimum. No exceptional-set operation occurs.

> **Corollary: A usable promotion rule**<span id="cor:promotion" label="cor:promotion">\[cor:promotion\]</span> Suppose an independently source-locked physical registry supplies $w=w_X$, a period $R_X$ with $qR_X\le(\log X)^{\eta_0}$, and an approximant satisfying $$\lVert\rho_X\rVert_\infty\ll1,\qquad
>  \frac qN\sum_{I_N}|w_X-\rho_X|
>  \ll(\log X)^{-\gamma}.$$ Then the weighted actual core has a logarithmic saving with exponent $\min\{\kappa_0,\gamma\}$.

> **Remark** The corollary is an implication, not a claim that the current frontier archive supplies $w_X$. That occurrence-level input remains unavailable.

# Residue-fiber error optimization

For $r\in\mathbb Z/R\mathbb Z$, write $$I_{N,r}=\{z\in I_N:z\equiv r\pmod R\}.$$

> **Proposition: Exact separation**<span id="prop:separate" label="prop:separate">\[prop:separate\]</span> For every $w$, $$\inf_{\rho\ {\rm period}\ R}\sum_{I_N}|w(z)-\rho(z)|
>  =
>  \sum_{r\bmod R}\inf_{\zeta\in\mathbb C}
>  \sum_{z\in I_{N,r}}|w(z)-\zeta|.$$ For the squared error, the unique minimizing value on every nonempty fiber is $$\bar w_r=\frac1{|I_{N,r}|}\sum_{z\in I_{N,r}}w(z).$$

> **Proof** A period-$R$ function has one independent value on each residue fiber, proving the first identity. Expanding $$\sum_{I_{N,r}}|w(z)-\zeta|^2
>  =
>  \sum_{I_{N,r}}|w(z)-\bar w_r|^2
>  +|I_{N,r}|\,|\zeta-\bar w_r|^2$$ proves the second.

By Cauchy–Schwarz, the fiber-mean quadratic certificate gives the explicit upper bound $$\sum_{I_N}|w-\rho|
 \le |I_N|^{1/2}
 \left(\sum_{r\bmod R}\sum_{I_{N,r}}|w-\bar w_r|^2\right)^{1/2}.$$ Thus the interface is finite and auditable whenever literal values of $w$ are known.

# Products, phases and precise limitations

> **Proposition: Exact-period products**<span id="prop:product" label="prop:product">\[prop:product\]</span> If $w=\prod_{j=1}^m w_j$ and every $w_j$ is bounded periodic of period $R_j$, then $w$ is periodic of period $\operatorname{lcm}(R_1,\ldots,R_m)$. It may be inserted directly in [\[thm:149\]](../main.tex#L81){reference-type="ref" reference="thm:149"} when $$q\operatorname{lcm}(R_1,\ldots,R_m)
>  \le(\log X)^{\eta_0}.$$

Rational additive phases fall in this proposition. A generic additive phase need not be well approximated by a small-period function. TPC-158 tests that boundary exactly. Likewise, [\[thm:main\]](../main.tex#L117){reference-type="ref" reference="thm:main"} treats one interval $(N,2N]$; it does not convert exceptional-scale density into control of predetermined prefix endpoints, the obstruction isolated in TPC-150.

# Audit and progress classification

The accompanying standard-library audit source-locks the TPC-149 theorem and certificate using `CANONICAL_UTF8_LF_V2`, checks exact residue-fiber quadratic minimization on rational data, and checks the triangle decomposition on a signed fixture. Hashes serve only as integrity checks.

| Statement                                               | Status                         |
|:--------------------------------------------------------|:-------------------------------|
| Periodic-to-literal interface on the actual Möbius core | $\mathrm{PROVED}_{L1}$         |
| Production physical multiplier and approximation rate   | $\mathrm{NOT\mbox{-}TESTABLE}$ |
| Generic phase or all prefixes                           | not proved                     |
| Positive fixed-$X$-power saving                         | not proved                     |

# Conclusion

The periodic theorem now has an exact literal-weight consumer: arithmetic cancellation is lost only through a normalized approximation cost whose unpenalized error term is residue-fiber-separable. This closes a genuine actual-core interface while exposing the next factual question: whether the eventual occurrence registry produces small cost. It does not answer that question by schema, numerics or notation.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC149,
  author = {Wang, Liang},
  title  = {{A Small-Polylogarithmic Determinant-Two M\"obius Corridor:
             Uniform Actual-Core Cancellation with Bounded Periodic Data}},
  year   = {2026},
  note   = {TPC-149 manuscript}
}

@misc{TaoTeravainen2026,
  author        = {Tao, Terence and Ter{\"a}v{\"a}inen, Joni},
  title         = {{Quantitative Correlations and Some Problems on Prime
                    Factors of Consecutive Integers}},
  year          = {2026},
  eprint        = {2512.01739v2},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT}
}

@misc{WangTPC150,
  author = {Wang, Liang},
  title  = {{Returning the Determinant-Two M\"obius Corridor:
             Terminal-Window Loss, Atomic Prefixes, and Split Log/Power Ledgers}},
  year   = {2026},
  note   = {TPC-150 manuscript}
}
```

<!-- SOURCE_BODY_END -->
