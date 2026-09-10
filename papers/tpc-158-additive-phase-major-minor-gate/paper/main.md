# **An Exact Major-Arc Gate for Additive Phases:\ Periodic Projection and a Minor-Arc Route Obstruction**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-158-additive-phase-major-minor-gate.pdf](../tpc-158-additive-phase-major-minor-gate.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-157 transfers a periodic two-Möbius estimate to a literal multiplier at the cost of its normalized $L^1$ distance from a small-period subspace. We evaluate that gate for an additive phase. A phase within inverse-interval accuracy of an allowed rational has a phase-aligned periodic approximant and inherits logarithmic cancellation. On a complete residue rectangle, the orthogonal projection error is an exact Dirichlet-kernel expression; away from all allowed rationals it is bounded below, stopping the periodic approximation route. The obstruction concerns the approximation method, not the size of the original Möbius correlation.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** additive phase; major arcs; Dirichlet kernel; periodic approximation; Möbius correlation.

# Setup

Write $\mathrm e(x)=\exp(2\pi i x)$. Retain the determinant-two notation $$q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az),\qquad
 I_N=\{z:N<t(z)\le2N\}.$$ TPC-149 gives constants $\eta_0,\kappa_0>0$ and, for every sufficiently large $X$, one set $\mathcal E_X^\star\subset[\sqrt X,X]$ outside which the simultaneous estimate $$\frac qN\left|\sum_{z\in I_N}c_z\rho(z)\right|
 \ll\lVert\rho\rVert_\infty(\log X)^{-\kappa_0}
\label{eq:periodic}$$ holds for every period-$R$ function with $qR\le(\log X)^{\eta_0}$ `\citep{WangTPC149}`. TPC-157 adds the normalized $L^1$ approximation error for a nonperiodic multiplier `\citep{WangTPC157}`.

# The major-arc gate

Let $I=\{z_0,z_0+1,\ldots,z_0+L-1\}$ contain $I_N$; enlarging the error sum outside $I_N$ is harmless.

> **Lemma: Phase-aligned approximant**<span id="lem:aligned" label="lem:aligned">\[lem:aligned\]</span> For $\alpha\in\mathbb R$, $k\in\mathbb Z$, and $R\ge1$, put $$\rho_{z_0}(z)=\mathrm e(-\alpha z_0)\,
>                \mathrm e\!\left(-\frac{k}{R}(z-z_0)\right).$$ Then $\rho_{z_0}$ is period $R$, has modulus one, and $$\sup_{z\in I}|\mathrm e(-\alpha z)-\rho_{z_0}(z)|
>  \le 2\pi L\left|\alpha-\frac{k}{R}\right|.
> \label{eq:aligned}$$

> **Proof** Periodicity follows from $\mathrm e(-k)=1$. After removing the common factor $\mathrm e(-\alpha z_0)$, use $|\mathrm e(x)-\mathrm e(y)|\le2\pi|x-y|$ and $|z-z_0|\le L$.

> **Theorem: Actual-core major arc**<span id="thm:major" label="thm:major">\[thm:major\]</span> Fix $A>0$. Suppose $$qR\le(\log X)^{\eta_0},\qquad
>  L\left|\alpha-\frac{k}{R}\right|
>  \le(\log X)^{-A},$$ and $$N\in[\sqrt X,X]\setminus\mathcal E_X^\star.$$ Then $$\boxed{\;
>  \frac qN\left|
>  \sum_{z\in I_N}c_z\mathrm e(-\alpha z)
>  \right|
>  \ll(\log X)^{-\kappa_0}+(\log X)^{-A}.\;}
> \label{eq:major}$$

> **Proof** Use $\rho_{z_0}$ in the TPC-157 interface. The periodic term gives the first summand. Since $|I_N|\ll N/q+1$, [\[eq:aligned\]](../main.tex#L100){reference-type="eqref" reference="eq:aligned"} gives the second, after absorbing the harmless endpoint term in the asymptotic range.

The alignment at $z_0$ matters. Comparing directly with $\mathrm e(-kz/R)$ would incorrectly charge the absolute coordinate rather than the interval length.

# Exact projection on a residue rectangle

Let $$I_{K,R}=\{z_0,\ldots,z_0+KR-1\},\qquad
 f_\alpha(z)=\mathrm e(\alpha z),$$ and let $\mathcal P_R$ be the space of period-$R$ functions restricted to this interval.

> **Theorem: Dirichlet projection identity**<span id="thm:projection" label="thm:projection">\[thm:projection\]</span> For every $K,R\ge1$, $$\frac1{KR}\inf_{\rho\in\mathcal P_R}
>  \sum_{z\in I_{K,R}}|f_\alpha(z)-\rho(z)|^2
>  =
>  1-\left|
>  \frac1K\sum_{j=0}^{K-1}\mathrm e(\alpha Rj)
>  \right|^2.
> \label{eq:projection}$$ Equivalently, with the continuous value $1$ for the ratio when $R\alpha\in\mathbb Z$, the squared mean on the right is $$\left|
>  \frac{\sin(\pi KR\alpha)}
>  {K\sin(\pi R\alpha)}
>  \right|^2.$$ Moreover, $$\frac1{KR}\inf_{\rho\in\mathcal P_R}
>  \sum_{z\in I_{K,R}}|f_\alpha(z)-\rho(z)|
>  \ge
>  \frac12\left[
>  1-\left|
>  \frac1K\sum_{j=0}^{K-1}\mathrm e(\alpha Rj)
>  \right|^2\right].
> \label{eq:l1lower}$$

> **Proof** On each residue fiber $z=z_0+r+jR$, the orthogonal projection is the fiber mean $$\mathrm e(\alpha(z_0+r))\frac1K
>  \sum_{j=0}^{K-1}\mathrm e(\alpha Rj).$$ Pythagoras gives [\[eq:projection\]](../main.tex#L163){reference-type="eqref" reference="eq:projection"}, and summing the geometric progression gives the sine quotient. An $L^1$ minimizer may be projected into the closed unit disk without increasing distance from unit-modulus data. There $|f_\alpha-\rho|\le2$, hence $|f_\alpha-\rho|^2\le2|f_\alpha-\rho|$. Infimizing proves [\[eq:l1lower\]](../main.tex#L182){reference-type="eqref" reference="eq:l1lower"}.

> **Corollary: Uniform minor-arc route stop**<span id="cor:stop" label="cor:stop">\[cor:stop\]</span> Let $I_n$ be cells of $L_n$ consecutive integers, let $\alpha_n\in\mathbb R$, and let $\mathcal R_n$ be a nonempty set of allowed periods. Put $$K_{n,R}=\left\lfloor\frac{L_n}{R}\right\rfloor
>  \qquad(R\in\mathcal R_n).$$ If $$\inf_{R\in\mathcal R_n}K_{n,R}\longrightarrow\infty,
>  \qquad
>  \inf_{R\in\mathcal R_n}
>  K_{n,R}\lVert R\alpha_n\rVert_{\mathbb R/\mathbb Z}
>  \longrightarrow\infty,
> \label{eq:uniform-minor}$$ then, uniformly over all allowed periods, $$\inf_{R\in\mathcal R_n}\frac1{L_n}
>  \inf_{\rho\ {\rm period}\ R}
>  \sum_{z\in I_n}|f_{\alpha_n}(z)-\rho(z)|
>  \ge\frac12-o(1).$$ Consequently, the TPC-157 small-period approximation route cannot yield a decaying bound on those cells.

> **Proof** For each $R\in\mathcal R_n$, retain a complete $K_{n,R}R$-subinterval of $I_n$. Restriction and [\[eq:l1lower\]](../main.tex#L182){reference-type="eqref" reference="eq:l1lower"} give the lower bound $$\frac{K_{n,R}R}{L_n}\,
>  \frac12\left[
>  1-
>  \min\left\{1,
>  \frac{1}{
>   2K_{n,R}\lVert R\alpha_n\rVert_{\mathbb R/\mathbb Z}}
>  \right\}^{\!2}
>  \right].$$ The first infimum in [\[eq:uniform-minor\]](../main.tex#L216){reference-type="eqref" reference="eq:uniform-minor"} makes $K_{n,R}R/L_n=1+o(1)$ uniformly, and the second makes the squared term $o(1)$ uniformly.

The uniform infima in [\[eq:uniform-minor\]](../main.tex#L216){reference-type="eqref" reference="eq:uniform-minor"} are essential. A pointwise assertion for every fixed $R$ does not stop a sequence of periods $R=R_n$ drifting with $n$.

# Route semantics

The positive result is labeled $\mathrm{L1\_ACTUAL\_CORE\_MAJOR\_ARC}$. The negative result is a scoped route stop: $$\text{small-period approximation fails}
 \;\not\Rightarrow\;
 \text{the M\"obius correlation is large}.$$ A direct additive-twist theorem, a larger admissible period range, or a different physical crosswalk remains logically open. The accompanying audit checks the projection identity numerically against the direct orthogonal projection and checks a nonzero-start phase-aligned fixture. These finite checks support implementation; the proofs above establish the identities.

# Conclusion

The phase question now has a sharp gate. Near an allowed rational, the existing actual-core theorem genuinely advances to an additive phase. Away from all allowed rationals, the exact Dirichlet projection shows that periodic approximation cannot be the missing argument. This narrows the next arithmetic input without pretending to resolve generic phases.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC149,
  author = {Wang, Liang},
  title  = {{A Small-Polylogarithmic Determinant-Two M\"obius Corridor}},
  year   = {2026},
  note   = {TPC-149 manuscript}
}

@misc{WangTPC157,
  author = {Wang, Liang},
  title  = {{Periodic Approximation of Literal Multipliers on
             Determinant-Two M\"obius Fibers}},
  year   = {2026},
  note   = {TPC-157 manuscript}
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
