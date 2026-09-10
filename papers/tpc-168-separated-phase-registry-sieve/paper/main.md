# **Separated Phase Registries for Direct Core Twists:\ A Finite Large-Sieve Gate and a Selector Firewall**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-168-separated-phase-registry-sieve.pdf](../tpc-168-separated-phase-registry-sieve.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-167 gives exact phase-$L^2$ cancellation for direct additive twists on the literal determinant-two core. We transfer that continuous statement to arbitrary finite separated phase registries. An elementary sampling inequality bounds the registry energy by the coefficient energy times $\delta^{-1}+4\pi(L-1)$. For a quasi-uniform registry of at least interval-scale size, all but a quantitatively sparse set of phases inherit a fixed-$X$ power saving. A sharp selector example shows why density-one registry control does not identify one distinguished production phase. Thus the finite-registry route genuinely advances, but the original pointwise phase node remains open.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** large sieve; additive phase; finite registry; selector firewall; Möbius correlation.

# A separated sampling inequality

Put $\mathrm e(x)=\exp(2\pi i x)$ and let $$P(\alpha)=\sum_{n=0}^{L-1}b_n\mathrm e(n\alpha),\qquad
 E=\sum_{n=0}^{L-1}|b_n|^2.$$ A finite set $\{\alpha_1,\ldots,\alpha_M\}\subset\mathbb T$ is $\delta$-separated, for a declared $0<\delta\le1$, if $$\lVert\alpha_j-\alpha_k\rVert_{\mathbb T}\ge\delta\qquad(j\ne k).$$

> **Theorem: Elementary finite phase sieve**<span id="thm:sampling" label="thm:sampling">\[thm:sampling\]</span> For every $0<\delta\le1$ and every $\delta$-separated registry, $$\boxed{\quad
>  \sum_{j=1}^M|P(\alpha_j)|^2
>  \le
>  \{\delta^{-1}+4\pi(L-1)\}E.
>  \quad}
> \label{eq:sampling}$$

> **Proof** Let $I_j$ be the circular interval of length $\delta$ centered at $\alpha_j$. These intervals have disjoint interiors. With $g=|P|^2$, for $x\in I_j$, $$g(\alpha_j)\le g(x)+\int_{I_j}|g'(y)|\,dy.$$ Integrate in $x$ over $I_j$, sum in $j$, and divide by $\delta$: $$\sum_jg(\alpha_j)
>  \le\delta^{-1}\int_{\mathbb T}|P|^2
>  +\int_{\mathbb T}|(|P|^2)'|.$$ Parseval gives $\int|P|^2=E$, while Cauchy–Schwarz gives $$\int_{\mathbb T}|(|P|^2)'|
>  \le2\lVert P'\rVert_2\lVert P\rVert_2
>  \le4\pi(L-1)E.$$ This proves [\[eq:sampling\]](../main.tex#L84){reference-type="eqref" reference="eq:sampling"}.

The constant is not optimized; the point is an explicit standard-library-auditable inequality. Classical large-sieve inequalities can sharpen constants without changing the route semantics `\citep{MontgomeryVaughan2007}`.

# The determinant-two registry theorem

Retain $$q=as,\quad t(z)=ad+qz,\quad
 c_z=\mu(d+sz)\mu(u+az),$$ $$I_N=\{z:N<t(z)\le2N\},\quad
 L_N=|I_N|,\quad E_N=\sum_{I_N}|c_z|^2,$$ and $$F_N(\alpha)=\frac qN\sum_{z\in I_N}c_z\mathrm e(-\alpha z).$$ Translation of the consecutive exponent interval changes only a unit-modulus factor, so [\[thm:sampling\]](../main.tex#L75){reference-type="ref" reference="thm:sampling"} applies.

> **Corollary: Bad-phase count**<span id="cor:count" label="cor:count">\[cor:count\]</span> For every $\lambda>0$, the number $B_\lambda$ of registry phases with $|F_N(\alpha_j)|>\lambda$ satisfies $$B_\lambda
>  \le
>  \frac{q^2E_N}{N^2\lambda^2}
>  \{\delta^{-1}+4\pi(L_N-1)\}.
> \label{eq:count}$$

> **Proof** Each bad phase contributes more than $\lambda^2$ to the sampled normalized energy. Apply [\[thm:sampling\]](../main.tex#L75){reference-type="ref" reference="thm:sampling"}.

> **Corollary: Quasi-uniform registry density**<span id="cor:density" label="cor:density">\[cor:density\]</span> Suppose $$\delta\ge\frac cM,\qquad M\ge\theta L_N$$ for fixed $c,\theta>0$. Then $$\frac{B_\lambda}{M}
>  \le
>  \left(c^{-1}+\frac{4\pi}{\theta}\right)
>  \frac{q/N+q^2/N^2}{\lambda^2}.
> \label{eq:density}$$ If $q/N\to0$, the choice $\lambda=(q/N)^{1/4}$ makes the bad proportion $O_{c,\theta}((q/N)^{1/2})$.

> **Proof** Divide [\[eq:count\]](../main.tex#L142){reference-type="eqref" reference="eq:count"} by $M$, use $\delta^{-1}/M\le c^{-1}$, $L_N/M\le\theta^{-1}$, and $$E_N\le L_N\le N/q+1.$$

In the small-polylogarithmic envelope with $N\ge\sqrt X$, this threshold is at most $$X^{-1/8}(\log X)^{\eta_0/4}.$$ The theorem therefore has the typed program status $$\mathsf{PROVED\_L1\_ACTUAL\_CORE\_
 PHASE\_METRIC\_FINITE\_REGISTRY}.$$ $$\begin{array}{c|c}
\text{axis}&\text{value}\\ \hline
\mathsf{analytic\_norm}&\mathsf{L2\_PHASE\_REGISTRY}\\
\mathsf{program\_positive\_L2}&\mathsf{false}\\
\mathsf{fixed\_atom}&\mathsf{false}
\end{array}$$ The power is a density statement on a certified registry, not a uniform pointwise estimate.

# The selector firewall

> **Proposition: Density does not select**<span id="prop:selector" label="prop:selector">\[prop:selector\]</span> There are quasi-uniform registries and coefficient sequences for which the bad proportion tends to zero while a distinguished registry phase has normalized value one at every length.

> **Proof** Take $b_n=1$ for $0\le n<L$ and the complete grid $\alpha_r=r/L$. Finite Fourier orthogonality gives $$\frac1L\left|\sum_{n=0}^{L-1}\mathrm e(n\alpha_r)\right|
>  =\mathbf1_{\{r=0\}}.$$ Thus the bad proportion at any fixed threshold in $(0,1)$ is $1/L$, but the named phase $\alpha_0=0$ remains maximally bad.

This is a scoped logical stop: $$\text{density-one registry control}
 \not\Rightarrow
 \text{control of a named selector}.$$ The coefficients in [\[prop:selector\]](../main.tex#L201){reference-type="ref" reference="prop:selector"} are not asserted to be the literal Möbius coefficients. The proposition stops only a coefficient-blind selection inference. It does not say that any minor-arc Möbius twist is large, just as the projection obstruction in TPC-158 stops only its declared approximation route `\citep{WangTPC158}`.

# Route decision and next object

TPC-167 supplied continuous phase $L^2$ `\citep{WangTPC167}`; TPC-168 now supplies finite separated-registry $L^2$. This is useful if the production observable averages over a certified phase population. A distinguished phase requires one of the following additional objects:

1.  a source-locked selector crosswalk proving that the chosen phase avoids the sparse bad subset;

2.  a random or equidistributed selector theorem with the exact quantifiers needed by the application;

3.  a pointwise additive-twist theorem.

None is currently present. The original parent-ready pointwise node therefore remains open rather than stopped.

# Reproducible audit

The accompanying script source-locks TPC-167, checks [\[eq:sampling\]](../main.tex#L84){reference-type="eqref" reference="eq:sampling"} and [\[eq:count\]](../main.tex#L142){reference-type="eqref" reference="eq:count"} on a nonuniform separated fixture, and realizes [\[prop:selector\]](../main.tex#L201){reference-type="ref" reference="prop:selector"} on a complete grid. Executable bad-snapshot mutations reject missing separation, promotion from density one to all phases, and interpretation of the selector fixture as a Möbius lower bound. Hashes have integrity semantics only.

# Conclusion

Phase averaging now survives discretization: a sufficiently dense separated registry has only a quantitatively sparse set of large direct twists. The result is a new actual-core phase-metric gate whose analytic norm is $L^2$ in the registry variable; it is not the program’s positive-$L2$ parity gate. The selector firewall identifies the exact remaining gap, rather than hiding it in an average. TPC-169 turns to the other open door and asks whether one common phase-exceptional set can control every atomic prefix endpoint.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC158,
  author = {Wang, Liang},
  title  = {{An Exact Major-Arc Gate for Additive Phases:
             Periodic Projection and a Minor-Arc Route Obstruction}},
  year   = {2026},
  note   = {TPC-158 manuscript}
}

@misc{WangTPC167,
  author = {Wang, Liang},
  title  = {{A Parseval Corridor for Direct Additive Twists on the
             Determinant-Two M\"obius Core}},
  year   = {2026},
  note   = {TPC-167 manuscript}
}

@book{MontgomeryVaughan2007,
  author    = {Montgomery, Hugh L. and Vaughan, Robert C.},
  title     = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  year      = {2007}
}
```

<!-- SOURCE_BODY_END -->
