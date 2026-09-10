# **One Phase-Exceptional Set for Every Atomic Prefix:\ A Dyadic Maximal Parseval Theorem on Determinant-Two Fibers**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-169-maximal-prefix-phase-metric.pdf](../tpc-169-maximal-prefix-phase-metric.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-159 controls cumulative periodic-core sums outside a dyadic shadow of scales, while TPC-160 shows that a prefix cutoff places one variation atom exactly at its selected endpoint. We open a different route by averaging an additive phase. An elementary Rademacher–Menshov dyadic decomposition and Parseval prove an $L^2$ bound for the maximum over all fiber prefixes. Consequently one phase-exceptional set controls every atomic endpoint, including endpoints inside the scale shadow. The theorem is pointwise in the endpoint but averaged in phase; it does not control a specified phase such as zero. This is an actual-core phase-metric child, with a maximal $L^2$ analytic norm, of the bad-endpoint frontier; it is not the program’s positive-$L2$ gate or the pointwise fixed-phase closure.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** maximal inequality; Rademacher–Menshov decomposition; additive phase; atomic prefix; determinant-two fiber.

# Ordered fiber prefixes

Retain the determinant-two data $$q=as,\quad t(z)=ad+qz,\quad
 c_z=\mu(d+sz)\mu(u+az),$$ and let $\rho$ be any bounded function; in the inherited actual core it may be periodic. Order the positive fiber points $$0<t(z_1)<\cdots<t(z_L)\le T.$$ The $z_j$ are consecutive integers and $$L\le T/q+1.
\label{eq:count}$$ Put $$b_j=c_{z_j}\rho(z_j),\qquad
 S_k(\alpha)=\sum_{j=1}^kb_j\mathrm e(-\alpha z_j),$$ where $\mathrm e(x)=\exp(2\pi ix)$, and define $$D_L=1+\lceil\log_2L\rceil,\qquad
 G_T(\alpha)=\frac qT\max_{1\le k\le L}|S_k(\alpha)|.$$

# The dyadic maximal lemma

> **Theorem: Finite dyadic maximal Parseval**<span id="thm:abstract" label="thm:abstract">\[thm:abstract\]</span> For arbitrary $b_1,\ldots,b_L\in\mathbb C$, $$\boxed{\quad
>  \int_{\mathbb T}\max_{1\le k\le L}
>  \left|\sum_{j=1}^kb_j\mathrm e(j\alpha)\right|^2d\alpha
>  \le D_L^2\sum_{j=1}^L|b_j|^2.
>  \quad}
> \label{eq:abstract}$$

> **Proof** Pad the coefficient sequence by zeros to length $H=2^{\lceil\log_2L\rceil}$. At each of the $D_L$ dyadic levels, partition $\{1,\ldots,H\}$ into aligned blocks of the corresponding power-of-two length. The binary expansion of $k$ decomposes every prefix $\{1,\ldots,k\}$ into disjoint aligned blocks, with at most one block from each level.
>
> Let $B_I(\alpha)=\sum_{j\in I}b_j\mathrm e(j\alpha)$. Cauchy–Schwarz on the at most $D_L$ selected blocks gives, for every $k$, $$\left|\sum_{j\le k}b_j\mathrm e(j\alpha)\right|^2
>  \le D_L\sum_{\text{all dyadic }I}|B_I(\alpha)|^2.$$ The right side is independent of $k$. At a fixed level the blocks partition the coefficient indices, and Parseval gives $$\sum_{I\ {\rm at\ that\ level}}
>  \int_{\mathbb T}|B_I(\alpha)|^2d\alpha
>  =\sum_{j=1}^L|b_j|^2.$$ There are $D_L$ levels, proving [\[eq:abstract\]](../main.tex#L102){reference-type="eqref" reference="eq:abstract"}.

This is the finite dyadic maximal argument commonly associated with Rademacher–Menshov estimates; no convergence theorem is imported `\citep{Zygmund2002}`.

# One phase set for all actual-core endpoints

> **Theorem: Maximal direct-twist core theorem**<span id="thm:core" label="thm:core">\[thm:core\]</span> For the determinant-two fiber above, $$\boxed{\quad
>  \int_{\mathbb T}G_T(\alpha)^2d\alpha
>  \le
>  D_L^2\lVert\rho\rVert_\infty^2
>  \left(\frac qT+\frac{q^2}{T^2}\right).
>  \quad}
> \label{eq:core}$$ Hence for every $\lambda>0$, $$\operatorname{meas}\{\alpha:G_T(\alpha)>\lambda\}
>  \le
>  \frac{D_L^2\lVert\rho\rVert_\infty^2}{\lambda^2}
>  \left(\frac qT+\frac{q^2}{T^2}\right).
> \label{eq:measure}$$

> **Proof** The common exponent shift from $z_j$ to $j$ has unit modulus. Apply [\[thm:abstract\]](../main.tex#L94){reference-type="ref" reference="thm:abstract"}, use $$\sum_j|b_j|^2
>  \le\lVert\rho\rVert_\infty^2L,$$ then use [\[eq:count\]](../main.tex#L79){reference-type="eqref" reference="eq:count"}. Chebyshev gives [\[eq:measure\]](../main.tex#L153){reference-type="eqref" reference="eq:measure"}.

> **Corollary: Every endpoint in a terminal shell**<span id="cor:shell" label="cor:shell">\[cor:shell\]</span> Outside the phase set in [\[eq:measure\]](../main.tex#L153){reference-type="eqref" reference="eq:measure"}, every fiber endpoint $U=t(z_k)\in[\theta T,T]$, $0<\theta\le1$, satisfies $$\frac qU|S_k(\alpha)|\le\theta^{-1}\lambda.
> \label{eq:shell}$$

> **Proof** The numerator is one of the prefix sums in $G_T$, and $T/U\le\theta^{-1}$.

The exceptional set in [\[eq:measure\]](../main.tex#L153){reference-type="eqref" reference="eq:measure"} is common to all $k$. Therefore [\[cor:shell\]](../main.tex#L167){reference-type="ref" reference="cor:shell"} includes endpoints lying in the dyadic scale shadow of TPC-159 `\citep{WangTPC159}`. It does not assert that those endpoints are good for a fixed phase.

# Power envelope and exact status

If $$q\le(\log X)^{\eta_0},\qquad
 \sqrt X\le T\le X,\qquad \lVert\rho\rVert_\infty\ll1,$$ then $D_L=O(\log X)$ and $$\lVert G_T\rVert_{L^2(\mathbb T)}
 \ll X^{-1/4}(\log X)^{1+\eta_0/2}.
\label{eq:power}$$ This is a positive fixed-$X$ power in a maximal phase-$L^2$ analytic norm. The exact program progress label is $$\mathsf{PROVED\_L1\_ACTUAL\_CORE\_
 PHASE\_METRIC\_MAXIMAL\_PREFIX}.$$ $$\begin{array}{c|c}
\text{axis}&\text{value}\\ \hline
\mathsf{analytic\_norm}&\mathsf{L2\_PHASE\_MAXIMAL}\\
\mathsf{program\_positive\_L2}&\mathsf{false}\\
\mathsf{fixed\_atom}&\mathsf{false}
\end{array}$$ It is stronger than one-endpoint phase Parseval because the maximum is inside the integral, at the cost of $D_L^2$.

# Relation to the atomic endpoint barrier

TPC-160 proves that a literal prefix cutoff has one Abel derivative atom and that continuous scale-exceptional density cannot decide whether the selected endpoint is bad `\citep{WangTPC160}`. The present theorem changes the averaging variable: $$\begin{array}{c|c|c}
 \text{route}&\text{pointwise variable}&\text{exceptional variable}\\
 \hline
 \text{TPC-159/160}&\text{phase / multiplier}&\text{scale}\\
 \text{TPC-169}&\text{all prefix endpoints}&\text{phase}.
 \end{array}$$ Thus TPC-169 creates a feasible phase-metric child of $\mathsf{O161.bad\_endpoint\_pointwise\_core}$. It does not close the original node, because nothing proves that a source-locked production phase avoids the exceptional phase set. In particular, [\[eq:measure\]](../main.tex#L153){reference-type="eqref" reference="eq:measure"} cannot be evaluated at $\alpha=0$.

# Reproducible audit

The standard-library certificate source-locks TPC-160 and TPC-167. It verifies the aligned dyadic decomposition, including at most one block of each size, for every prefix of a non-power-of-two fixture. It evaluates the maximal function on a finite Fourier grid as an implementation check; the analytic proof certifies the continuous integral. Executable bad-snapshot mutations reject deletion of the squared depth cost, confusion of terminal and small-endpoint normalization, and promotion from endpoint-pointwise to phase-pointwise. Hashes certify integrity only.

# Conclusion

One common phase-exceptional set now controls every atomic prefix on the actual determinant-two core. This crosses the scale-shadow barrier in a genuinely different norm, with an explicit positive fixed-$X$ phase-$L^2$ power. The remaining selector gap is honest and sharp. TPC-170 asks whether a fixed phase outside one null set can be followed along an entire prescribed sequence of cores and then returned through Abel summation.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC159,
  author = {Wang, Liang},
  title  = {{Dyadic-Shadow Lifting from Good-Scale M\"obius
             Correlations to Almost-Endpoint Prefixes}},
  year   = {2026},
  note   = {TPC-159 manuscript}
}

@misc{WangTPC160,
  author = {Wang, Liang},
  title  = {{Exceptional-Variation Abel Return:
             Literal Weights, Almost-Prefixes, and the Atomic
             All-Prefix Barrier}},
  year   = {2026},
  note   = {TPC-160 manuscript}
}

@misc{WangTPC167,
  author = {Wang, Liang},
  title  = {{A Parseval Corridor for Direct Additive Twists on the
             Determinant-Two M\"obius Core}},
  year   = {2026},
  note   = {TPC-167 manuscript}
}

@book{Zygmund2002,
  author    = {Zygmund, Antoni},
  title     = {Trigonometric Series},
  edition   = {Third},
  publisher = {Cambridge University Press},
  year      = {2002}
}
```

<!-- SOURCE_BODY_END -->
