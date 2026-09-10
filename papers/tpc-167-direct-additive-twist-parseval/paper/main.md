# **A Parseval Corridor for Direct Additive Twists\ on the Determinant-Two Möbius Core**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-167-direct-additive-twist-parseval.pdf](../tpc-167-direct-additive-twist-parseval.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The periodic-approximation route to an additive phase has a sharp minor-arc obstruction. We open a different, direct route by treating the phase as an $L^2$ variable. On the literal determinant-two two-Möbius core, Parseval gives an exact mean-square identity for the normalized additive twist, at every scale and without a scale-exceptional set. The same identity holds on every complete Fourier grid at least as long as the fiber interval. In the small-polylogarithmic envelope this is a positive fixed-$X$ power in phase $L^2$. It is not a pointwise theorem for a specified production phase, and therefore does not close the original pointwise additive-twist frontier.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** Möbius correlation; additive twist; Parseval identity; phase average; determinant two.

# The literal core and its phase transform

Put $\mathrm e(x)=\exp(2\pi i x)$. Retain the determinant-two data $$a,s\ge1,\quad d,u\in\mathbb Z,\quad
 (a,s)=1,\quad as\ {\rm odd},\quad su-ad=2,$$ $$q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az).$$ For $N>0$, let $$I_N=\{z\in\mathbb Z:N<t(z)\le2N\},\quad
 L_N=|I_N|,\quad E_N=\sum_{z\in I_N}|c_z|^2.$$ The interval $I_N$ consists of consecutive integers, and $$E_N\le L_N\le\frac Nq+1.
\label{eq:count}$$ Define the normalized direct additive twist $$F_N(\alpha)=\frac qN\sum_{z\in I_N}c_z\mathrm e(-\alpha z),
 \qquad \alpha\in\mathbb T=\mathbb R/\mathbb Z.
\label{eq:transform}$$

TPC-158 controls explicit major arcs through periodic approximation and proves that this approximation route is expensive on a uniform minor-arc family `\citep{WangTPC158}`. The definition [\[eq:transform\]](../main.tex#L87){reference-type="eqref" reference="eq:transform"} does not approximate the phase.

# Exact phase mean square

> **Theorem: Direct additive-twist Parseval identity**<span id="thm:parseval" label="thm:parseval">\[thm:parseval\]</span> For every $N>0$, $$\boxed{\quad
>  \int_{\mathbb T}|F_N(\alpha)|^2\,d\alpha
>  =\frac{q^2}{N^2}E_N.
>  \quad}
> \label{eq:parseval}$$ In particular, $$\lVert F_N\rVert_{L^2(\mathbb T)}^2
>  \le\frac qN+\frac{q^2}{N^2}.
> \label{eq:l2bound}$$ No exceptional set of scales is required.

> **Proof** Expanding the square and using character orthogonality gives $$\int_{\mathbb T}\mathrm e\bigl(-\alpha(z-z')\bigr)\,d\alpha
>  =\mathbf1_{\{z=z'\}}.$$ Thus every off-diagonal term vanishes and the diagonal equals $q^2E_N/N^2$. Apply [\[eq:count\]](../main.tex#L81){reference-type="eqref" reference="eq:count"}.

> **Corollary: Exceptional phases**<span id="cor:measure" label="cor:measure">\[cor:measure\]</span> For every $\lambda>0$, $$\operatorname{meas}\{\alpha\in\mathbb T:|F_N(\alpha)|>\lambda\}
>  \le
>  \frac{q^2E_N}{N^2\lambda^2}
>  \le
>  \frac{q/N+q^2/N^2}{\lambda^2}.
> \label{eq:chebyshev}$$

> **Proof** This is Chebyshev’s inequality applied to [\[eq:parseval\]](../main.tex#L104){reference-type="eqref" reference="eq:parseval"}.

The identity is stronger than a logarithmic estimate in its own declared norm, but weaker than a bound at any named $\alpha$. It holds equally for arbitrary bounded coefficients; the Möbius form identifies the actual core rather than supplying the orthogonality.

# A finite exact Fourier registry

Write $I_N=\{z_0,\ldots,z_0+L_N-1\}$.

> **Proposition: Complete-grid identity**<span id="prop:grid" label="prop:grid">\[prop:grid\]</span> If $M\ge L_N$, then $$\frac1M\sum_{r=0}^{M-1}
>  \left|F_N\left(\frac rM\right)\right|^2
>  =\frac{q^2}{N^2}E_N.
> \label{eq:grid}$$ Consequently the number of grid phases for which $|F_N(r/M)|>\lambda$ is at most $$\frac{Mq^2E_N}{N^2\lambda^2}.$$

> **Proof** After expansion, the finite character average is one precisely when $M\mid z-z'$. Since $|z-z'|\le L_N-1<M$, this occurs precisely on the diagonal. The counting assertion follows by summing $|F_N|^2>\lambda^2$ over bad grid points.

The condition $M\ge L_N$ is structural. For a shorter grid, distinct exponents may collide modulo $M$, so [\[eq:grid\]](../main.tex#L157){reference-type="eqref" reference="eq:grid"} need not hold.

# Interpretation of the power envelope

Suppose the small-polylogarithmic envelope $$q\le(\log X)^{\eta_0},\qquad N\ge\sqrt X$$ holds. For sufficiently large $X$, $q\le N$, and [\[eq:l2bound\]](../main.tex#L110){reference-type="eqref" reference="eq:l2bound"} gives $$\boxed{\quad
 \lVert F_N\rVert_{L^2(\mathbb T)}
 \le\sqrt2\,X^{-1/4}(\log X)^{\eta_0/2}.
 \quad}
\label{eq:power}$$ Thus TPC-167 has the precise program status $$\mathsf{PROVED\_L1\_ACTUAL\_CORE\_
 PHASE\_METRIC\_SINGLE\_CELL}.$$ Its analytic norm is $\mathsf{L2\_PHASE}$, while $\mathsf{program\_positive\_L2=false}$ and $\mathsf{fixed\_atom=false}$. The positive exponent in [\[eq:power\]](../main.tex#L190){reference-type="eqref" reference="eq:power"} belongs to a phase-averaged norm. It cannot be entered as a production fixed-phase or endpoint-V3 payment.

# Why pointwise selection remains open

The implication $$\lVert F_N\rVert_{L^2(\mathbb T)}\ll N^{-1/2}q^{1/2}
 \quad\Longrightarrow\quad
 |F_N(\alpha_\star)|=o(1)$$ is false without information about the selected phase $\alpha_\star$. At the coefficient level, take $c_z=1$ on an interval and $\alpha_\star=0$. Then $$|F_N(0)|=\frac{qL_N}{N},$$ which is of constant order when $L_N\sim N/q$, while Parseval still has mean square of order $q/N$. This example is a logical nonimplication for coefficient-blind phase averaging; it is not a claim that the literal Möbius coefficients realize the example.

Accordingly, the parent-ready direct-twist node is advanced only to a typed child: $$\mathsf{direct\ additive\ twist}
 \longrightarrow
 \mathsf{phase\mbox{-}L^2\ direct\ twist}.$$ The original pointwise node still needs a source-locked phase registry plus an avoidance or selection theorem, or a genuinely pointwise arithmetic estimate.

# Reproducible certificate

The standard-library audit source-locks TPC-158, checks Parseval on a shifted signed/zero fixture using two complete Fourier grids of different sizes, and verifies the normalization bound. These are finite implementation checks; the proof above establishes the continuous identity. Its executable mutation contract rejects promotion from phase $L^2$ to a fixed phase, from a phase power to endpoint V3, or from orthogonality to Möbius-specific cancellation. Hashes certify artifact integrity only.

# Conclusion

The minor-arc obstruction to small-period approximation does not stop every direct route. Parseval gives an exact, exceptional-scale-free direct additive-twist theorem on the actual core, with a positive fixed-$X$ power in phase $L^2$. The cost of this advance is equally exact: a distinguished physical phase remains outside the theorem. TPC-168 asks how much of this phase-average information survives on a finite source-locked phase registry.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC149,
  author = {Wang, Liang},
  title  = {{A Small-Polylogarithmic Determinant-Two M\"obius Corridor}},
  year   = {2026},
  note   = {TPC-149 manuscript}
}

@misc{WangTPC158,
  author = {Wang, Liang},
  title  = {{An Exact Major-Arc Gate for Additive Phases:
             Periodic Projection and a Minor-Arc Route Obstruction}},
  year   = {2026},
  note   = {TPC-158 manuscript}
}

@book{Katznelson2004,
  author    = {Katznelson, Yitzhak},
  title     = {An Introduction to Harmonic Analysis},
  edition   = {Third},
  publisher = {Cambridge University Press},
  year      = {2004}
}
```

<!-- SOURCE_BODY_END -->
