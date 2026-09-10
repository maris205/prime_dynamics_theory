# **Dyadic-Shadow Lifting from Good-Scale Möbius\ Correlations to Almost-Endpoint Prefixes**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-159-dyadic-shadow-prefix-lifting.pdf](../tpc-159-dyadic-shadow-prefix-lifting.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The TPC-149 determinant-two theorem controls periodic two-Möbius correlations on every nonexceptional interval $(N,2N]$ inside an ambient shell. We lift that estimate to cumulative prefixes by an exact dyadic telescoping. An endpoint is admissible when its first $J$ dyadic ancestors avoid the source exceptional set. The correlation error has no factor $J$, because the block lengths form a geometric series; the exceptional shadow has only a $J=O(\log\log X)$ measure cost. This proves a genuine almost-endpoint prefix theorem on the actual periodic Möbius core. It does not control every predetermined atomic endpoint.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** Möbius correlation; cumulative prefix; exceptional scale; dyadic shadow; determinant two.

# Source theorem and notation

Let $$q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az),$$ where $$a,s,R\ge1,\quad d,u\in\mathbb Z,\quad
 (a,s)=1,\quad as\ {\rm odd},\quad su-ad=2.$$ TPC-149 proves that there are absolute $\eta_0,\kappa_0>0$ and, for every sufficiently large $X$, a set $\mathcal E_X^\star\subset[\sqrt X,X]$ such that $$\frac1{\log X}\int_{\mathcal E_X^\star}\frac{dN}{N}
 \ll(\log X)^{-\kappa_0},
\label{eq:exception}$$ and, if $qR\le(\log X)^{\eta_0}$, $$\frac qN\left|
 \sum_{\substack{z\in\mathbb Z\\N<t(z)\le2N}}
 c_z\rho(z)\right|
 \ll\lVert\rho\rVert_\infty(\log X)^{-\kappa_0}
\label{eq:source}$$ for all $N\in[\sqrt X,X]\setminus\mathcal E_X^\star$ and every period-$R$ function $\rho$ `\citep{WangTPC149}`.

# The dyadic shadow

Fix $A>0$ and set $$J=\left\lceil A\log_2\log X\right\rceil,\qquad
 \mathcal S_{X,J}=\bigcup_{j=1}^J2^j\mathcal E_X^\star.
\label{eq:shadow}$$ Here $2^jE=\{2^jt:t\in E\}$.

> **Proposition: Shadow measure**<span id="prop:measure" label="prop:measure">\[prop:measure\]</span> One has $$\frac1{\log X}
>  \int_{\mathcal S_{X,J}\cap[2^J\sqrt X,X]}\frac{dT}{T}
>  \ll J(\log X)^{-\kappa_0}
>  =(\log X)^{-\kappa_0+o(1)}.
> \label{eq:shadowmeasure}$$

> **Proof** For every $j$, the substitution $T=2^jN$ preserves logarithmic measure: $$\int_{2^j\mathcal E_X^\star}\frac{dT}{T}
>  =\int_{\mathcal E_X^\star}\frac{dN}{N}.$$ Use the union bound, [\[eq:exception\]](../main.tex#L79){reference-type="eqref" reference="eq:exception"}, and $J=O(\log\log X)$. Intersecting with the endpoint interval only decreases the measure.

# Cumulative prefix lifting

For bounded period-$R$ $\rho$, define $$A_\rho(T)=
 \sum_{\substack{z\in\mathbb Z\\0<t(z)\le T}}c_z\rho(z).$$

> **Theorem: Almost-endpoint cumulative prefix**<span id="thm:main" label="thm:main">\[thm:main\]</span> Suppose $$qR\le(\log X)^{\eta_0},\qquad
>  2^J\sqrt X\le T\le X,\qquad
>  T\notin\mathcal S_{X,J}.$$ Then $$\boxed{\;
>  \frac qT|A_\rho(T)|
>  \ll\lVert\rho\rVert_\infty
>  \left\{(\log X)^{-\kappa_0}+2^{-J}+\frac qT\right\}.\;}
> \label{eq:main}$$ Consequently, $$\frac qT|A_\rho(T)|
>  \ll\lVert\rho\rVert_\infty
>  (\log X)^{-\min\{\kappa_0,A\}+o(1)}$$ in the asymptotic determinant-two envelope.

> **Proof** Use the exact identity $$A_\rho(T)=
>  \sum_{j=1}^J
>  \sum_{\substack{z\\T/2^j<t(z)\le T/2^{j-1}}}
>  c_z\rho(z)
>  +A_\rho(T/2^J).
> \label{eq:telescoping}$$ Since $T\notin\mathcal S_{X,J}$, every $N_j=T/2^j$ avoids $\mathcal E_X^\star$. The endpoint assumptions put all $N_j$ in $[\sqrt X,X]$, so [\[eq:source\]](../main.tex#L87){reference-type="eqref" reference="eq:source"} gives $$\left|
>  \sum_{N_j<t(z)\le2N_j}c_z\rho(z)\right|
>  \ll\lVert\rho\rVert_\infty\frac{N_j}{q}
>  (\log X)^{-\kappa_0}.$$ After multiplying by $q/T$, the sum of these errors is at most $$\lVert\rho\rVert_\infty(\log X)^{-\kappa_0}
>  \sum_{j=1}^J2^{-j}
>  \le\lVert\rho\rVert_\infty(\log X)^{-\kappa_0}.$$ Thus there is no $J$ loss in the correlation term.
>
> The progression $t(z)=ad+qz$ has at most $T/(q2^J)+1$ positive points below $T/2^J$. Since $|c_z|\le1$, $$\frac qT|A_\rho(T/2^J)|
>  \le\lVert\rho\rVert_\infty\left(2^{-J}+\frac qT\right).$$ Combine the bounds. Finally $2^{-J}\le(\log X)^{-A}$.

> **Corollary: Intervals between good endpoints**<span id="cor:interval" label="cor:interval">\[cor:interval\]</span> If $T_0<T_1$ both satisfy the hypotheses of [\[thm:main\]](../main.tex#L133){reference-type="ref" reference="thm:main"}, then $$\sum_{T_0<t(z)\le T_1}c_z\rho(z)
>  =A_\rho(T_1)-A_\rho(T_0)$$ is bounded by the sum of the two corresponding right sides.

# Why this is not all-prefix control

> **Proposition: Atomic nonimplication**<span id="prop:atomic" label="prop:atomic">\[prop:atomic\]</span> The measure estimate [\[eq:shadowmeasure\]](../main.tex#L109){reference-type="eqref" reference="eq:shadowmeasure"}, by itself, does not imply that a prescribed finite or discrete endpoint set $\mathcal T_X$ is disjoint from $\mathcal S_{X,J}$.

> **Proof** This remains true even if the dyadic form of the shadow is preserved. Indeed, for endpoints in $[2^J\sqrt X,X]$, enlarge the source set by $$\left\{2^{-J}T:
>  T\in\mathcal T_X\cap[2^J\sqrt X,X]\right\}.$$ This is a finite or countable subset of $[\sqrt X,X]$, so it has zero continuous logarithmic measure. Removing these extra scales from the good set cannot invalidate the source estimate, while the new $j=J$ shadow copy contains every displayed endpoint. Thus the same measure bound is compatible with intersection; the measure bound alone supplies no avoidance statement.

This is the TPC-150 selector firewall in a sharper form `\citep{WangTPC150}`: the relevant bad set is now the explicit dyadic shadow required by cumulative telescoping. A pointwise theorem, proved exceptional avoidance, or a non-atomic selector crosswalk is still needed for deterministic all-prefix control.

# Audit and level

The standard-library certificate checks [\[eq:telescoping\]](../main.tex#L165){reference-type="eqref" reference="eq:telescoping"} exactly on a rational progression, checks the geometric block mass, and checks a union bound on intervals in logarithmic coordinates. It source-locks the TPC-149 theorem using canonical UTF-8/LF hashes; those hashes certify integrity only.

$$\boxed{
 \mathrm{TPC\mbox{-}159}
 =
 \mathrm{L1\_ACTUAL\_PREFIX\_ALMOST\_ENDPOINT}.}$$ This is strictly beyond a single source-native dyadic interval, but below deterministic all-prefix control and below every positive fixed-$X$-power target.

# Conclusion

The actual periodic Möbius core now reaches cumulative prefixes on a density-one logarithmic family of endpoints. The dyadic error does not accumulate a $\log\log X$ factor; only the exceptional shadow does. The remaining endpoint problem is no longer vague: one must control the intersection of that shadow with the literal endpoint registry.

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

@misc{WangTPC150,
  author = {Wang, Liang},
  title  = {{Returning the Determinant-Two M\"obius Corridor:
             Terminal-Window Loss, Atomic Prefixes, and Split Log/Power Ledgers}},
  year   = {2026},
  note   = {TPC-150 manuscript}
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
```

<!-- SOURCE_BODY_END -->
