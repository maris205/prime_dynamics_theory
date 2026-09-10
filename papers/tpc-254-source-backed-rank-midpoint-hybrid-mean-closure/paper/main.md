# Source-Backed Rank-Midpoint Hybrid-Mean Closure\ and the Adjoint-Lane Source Gap

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Electronic Information and Communications, Huazhong University of Science and Technology (HUST),; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

For the literal V59 hybrid residual $w(u)=\Lambda(u+2)-b_x^{(Z_x)}(u)$ with fixed finite cutoff $Z_x=(\log x)^K$, we attach the source-backed maximal Type-I theorem to the coefficient-independent rank midpoint isolated in TPC-253. Freezing $\gamma_0=1/4$, nonnegativity of the maximal Type-I sum allows its unit-weight $m=1$ row to be extracted. The two rank children are active integer intervals for every real $x$, so for each fixed $M>0$ their sums are $O_{M,K}(x(\log x)^{-M})$. Exact cardinalities and Haar normalization then give $$|\langle z_{\mathrm{mid}},w\rangle|\ll_{M,K}x^{1/2}(\log x)^{-M}.$$ This is an arithmetic advance for the literal $w$ lane, but arbitrary fixed logarithmic saving is not a fixed power saving. The second moment remains the unestimated form $\langle A_x^*z_{\mathrm{mid}},\beta\rangle$; only Cauchy is supported. A real zero-diagonal derangement construction permits arbitrary signed scale, and at dimension two the Cauchy constant one is exact. These obstructions are synthetic, not literal V59 counterexamples. A canonical exact certificate, 82 rejected mutations, and 192 rational stress families reproduce only the finite algebra, endpoint rules, and source-contract typing.

<!-- SOURCE_BODY_BEGIN -->

# Frozen objects and typed source input

Fix a finite admissible $K$ and write $$Z_x=(\log x)^K,\qquad
 w(u)=\Lambda(u+2)-b_x^{(Z_x)}(u).                    \label{eq:residual}$$ The cutoff $Z_x$ is not the Haar vector below. On the real clock $x$, let $$I_x=(x/2,x]\cap\mathbb Z=\{n_1<\cdots<n_N\},\qquad
 N=\lfloor x\rfloor-\lfloor x/2\rfloor\geq2.          \label{eq:clock}$$ Put $\ell=\lfloor N/2\rfloor$, $r=N-\ell$, $L=\{n_1,\ldots,n_\ell\}$, $R=I_x\setminus L$, and $$\rho^2=\frac{\ell r}{N},\qquad
 z_{\mathrm{mid}}=\rho\left(\frac{\mathbf 1_L}{\ell}-\frac{\mathbf 1_R}{r}\right).       \label{eq:haar}$$ This split is fixed before $w$, $\beta$, a coefficient, or a sign is inspected. It is the source-frozen TPC-253 choice, not a claim of V59 canonicality `\cite{tpc253}`.

The analytic input is the hybrid H2 theorem frozen in the local comparison compiler `\cite{compiler}`. For each fixed $\gamma<1/2$ and each requested fixed logarithmic strength, it supplies $$\sum_{m\leq x^\gamma}\tau(m)^B\max_J
 \left|\sum_{\substack{x/2<ms\leq x\\s\in J}}w(ms)\right|
 \ll_{B,K,\gamma}\frac{x}{(\log x)^B},                \label{eq:h2}$$ where $J$ ranges over active integer intervals. The compiler obtains its prime-progression side from maximal Bombieri–Vinogradov/large-sieve inputs `\cite{Bombieri1965,MontgomeryVaughan1973}`, and its hybrid comparison side from Rosser–Iwaniec fundamental-lemma weights `\cite{Iwaniec1980Rosser}`. TPC-254 is a deterministic corollary attachment to [\[eq:h2\]](main.tex#L83){reference-type="eqref" reference="eq:h2"}; it does not reprove those inputs. Ford–Maynard supplies the upstream prime-producing sieve architecture and parameter order `\cite{FordMaynard2024}`. Vaughan’s identity belongs to the upstream Type-I/Type-II extraction context `\cite{Vaughan1977}`; it is not used here to strengthen the resulting scale.

# Rank children and the literal $w$ moment

The endpoint issue is small but decisive. If $a=\lfloor x/2\rfloor$ and $b=\lfloor x\rfloor$, then $$I_x=\{a+1,\ldots,b\},\quad
 L=\{a+1,\ldots,a+\ell\},\quad
 R=\{a+\ell+1,\ldots,b\}.                            \label{eq:endpoints}$$ Thus both children are consecutive active integer intervals for every real $x$. The integer crosswalk $\lfloor3x/4\rfloor$ is not used for nonintegral $x$; for example, $x=27/2$ gives $L=\{7,8,9\}$ although $\lfloor3x/4\rfloor=10$.

Write $W_J=\sum_{u\in J}w(u)$. We now state the arithmetic conclusion.

> **Theorem: Rank-midpoint hybrid-mean closure**<span id="thm:main" label="thm:main">\[thm:main\]</span> Fix a finite admissible $K$. For every fixed $M>0$ and all sufficiently large real $x$, $$\begin{aligned}
>  \max(|W_L|,|W_R|)&\ll_{M,K}\frac{x}{(\log x)^M},                    \label{eq:child}\\
>  \left|\frac{W_L}{\ell}-\frac{W_R}{r}\right|
>    &\ll_{M,K}(\log x)^{-M},                                         \label{eq:means}\\
>  |\langle z_{\mathrm{mid}},w\rangle|&\ll_{M,K}x^{1/2}(\log x)^{-M}.                         \label{eq:moment}\end{aligned}$$

> **Proof** Freeze $\gamma_0=1/4$ in [\[eq:h2\]](main.tex#L83){reference-type="eqref" reference="eq:h2"} and choose its integer log-saving parameter sufficiently strongly for the target $M$. Every summand on the left of [\[eq:h2\]](main.tex#L83){reference-type="eqref" reference="eq:h2"} is nonnegative. For sufficiently large $x$, the row $m=1$ is present and has weight $\tau(1)^B=1$. Hence its maximum over consecutive $J\subset I_x$ is bounded by the full sum. Applying this to the two intervals in [\[eq:endpoints\]](main.tex#L102){reference-type="eqref" reference="eq:endpoints"} proves [\[eq:child\]](main.tex#L115){reference-type="eqref" reference="eq:child"}.
>
> The exact cardinalities satisfy $$N=x/2+O(1),\qquad \ell=x/4+O(1),\qquad r=x/4+O(1).$$ Dividing the two child bounds and using the triangle inequality proves [\[eq:means\]](main.tex#L117){reference-type="eqref" reference="eq:means"}. Finally, TPC-253’s exact partial-sum identity is $$\langle z_{\mathrm{mid}},w\rangle=\rho\left(\frac{W_L}{\ell}-\frac{W_R}{r}\right).         \label{eq:partial}$$ Since $\ell r\leq N^2/4$, we have $\rho\leq\sqrt N/2\ll\sqrt x$. Equations [\[eq:means\]](main.tex#L117){reference-type="eqref" reference="eq:means"} and [\[eq:partial\]](main.tex#L137){reference-type="eqref" reference="eq:partial"} yield [\[eq:moment\]](main.tex#L118){reference-type="eqref" reference="eq:moment"}.

The normalization has the parity-exact form $$\rho^2=\begin{cases}
 N/4,&N\text{ even},\\[2pt]
 N/4-1/(4N),&N\text{ odd},
 \end{cases}
 \qquad
 \rho^2=x/8+O(1).                                      \label{eq:rho}$$ Consequently $\rho=x^{1/2}/(2\sqrt2)+O(x^{-1/2})$.

# Quantifier and scale firewalls

The isolated corollary uses the order $$\boxed{K\text{ fixed}}\ \longrightarrow\ \gamma_0=\tfrac14
 \longrightarrow M\longrightarrow B_{\mathrm{H2}}
 \longrightarrow \delta<1-\gamma_0
 \longrightarrow x\geq x_0(M,K).                     \label{eq:quantifiers}$$ The omitted middle choices are the divisor-tail cutoff and stronger Bombieri–Vinogradov/fundamental-lemma savings. Constants are not uniform as $K\to\infty$ or $\gamma\to1/2$. In the full upstream compiler the separate order is target $(A,\varpi)$, then Ford–Maynard $B_{\mathrm{FM}}$, then a fixed $K=K(B_{\mathrm{FM}})$, and only then $x\geq x_0$.

Arbitrary fixed logarithmic saving is not a fixed power saving. Indeed, for fixed $\eta,M>0$, $$\frac{x^{1/2}(\log x)^{-M}}{x^{1/2-\eta}}
 =\frac{x^\eta}{(\log x)^M}\longrightarrow\infty.       \label{eq:logpower}$$ Neither [\[eq:moment\]](main.tex#L118){reference-type="eqref" reference="eq:moment"} nor its proof gives a sign or a nonzero value.

# The open adjoint lane

Keep the literal TPC-247 operator orientation and put $g=A_x\beta$. The exact identity is $$\langle z_{\mathrm{mid}},A_x\beta\rangle=\langle A_x^*z_{\mathrm{mid}},\beta\rangle,\qquad
 (A_x^*z_{\mathrm{mid}})(t)=\sum_{u\in I_x}\overline{A_x(u,t)}z_{\mathrm{mid}}(u).     \label{eq:adjoint}$$ Cauchy and Theorem [\[thm:main\]](main.tex#L111){reference-type="ref" reference="thm:main"} give only $$\begin{aligned}
 |\langle z_{\mathrm{mid}},A_x\beta\rangle|&\leq\|A_x^*z_{\mathrm{mid}}\|_2\|\beta\|_2,             \label{eq:cauchy}\\
 |\overline{\langle z_{\mathrm{mid}},w\rangle}\langle z_{\mathrm{mid}},A_x\beta\rangle|
 &\ll_{M,K}x^{1/2}(\log x)^{-M}\|A_x^*z_{\mathrm{mid}}\|_2\|\beta\|_2.        \label{eq:transfer}\end{aligned}$$

| Locked result         | Test object                                     | TPC-254 role                 |
|:----------------------|:------------------------------------------------|:-----------------------------|
| hybrid maximal Type I | every active integer interval                   | pays $w$ children by $m=1$   |
| V21 AP errors         | full-shell residue fibers averaged in $q$       | no hard-child adjoint test   |
| V21 paid mean         | complete prime-modulus average with raw $\beta$ | not $A_x^*z_{\mathrm{mid}}$  |
| whole-shell mean      | one total sum                                   | cannot control a Haar moment |
| TPC-247/TPC-253       | exact operator and adjoint identities           | algebra only, no estimate    |

For the whole-shell warning, $f=\lambda z_{\mathrm{mid}}$ has total sum zero but $\langle z_{\mathrm{mid}},f\rangle=\lambda$. The source-gap conclusion is restricted to this frozen corpus; it is not a universal literature-absence claim.

> **Proposition: Sharp norm-only obstruction**<span id="prop:sharp" label="prop:sharp">\[prop:sharp\]</span> For every $N\geq2$, every real unit vector $z$, every real $\lambda$, and any derangement $\sigma$, there is a real zero-diagonal matrix $A$ with $\beta=\mathbf 1$ such that $A\beta=\lambda z$ and $\langle z,A\beta\rangle=\lambda$. At $N=2$, equality holds in [\[eq:cauchy\]](main.tex#L188){reference-type="eqref" reference="eq:cauchy"}.

> **Proof** Set $A_{i,\sigma(i)}=\lambda z_i$ and all other entries to zero. The derangement deletes the diagonal, while the $i$th row sum is $\lambda z_i$. Thus $A\mathbf 1=\lambda z$ and the moment is $\lambda\|z\|_2^2=\lambda$.
>
> For $N=2$, take $$z=\frac1{\sqrt2}(1,-1),\qquad
>  A=\begin{pmatrix}0&\lambda/\sqrt2\\-\lambda/\sqrt2&0\end{pmatrix},
>  \qquad \beta=(1,1).$$ Then $A^*z=(\lambda/2,\lambda/2)$, so $\|A^*z\|_2^2=\lambda^2/2$, $\|\beta\|_2^2=2$, and $|\langle z,A\beta\rangle|^2=\lambda^2$.

Proposition [\[prop:sharp\]](main.tex#L214){reference-type="ref" reference="prop:sharp"} is synthetic. It does not assert that this matrix is the literal V59 operator, but it proves that reality, a deleted diagonal, and norm geometry alone cannot improve Cauchy.

# Executable scope and route verdict

The released certificate uses canonical rational and Gaussian-rational data. It checks a nonintegral rank split, the rational projector products $\rho^2h_ih_j$, nonnegative $m=1$ logic, a whole-shell counterexample, adjoint orientation, derangement scale, and the squared $N=2$ equality. The independent checker imports no producer, rejects bool-as-int fields, and rejects 82 mutations. The stress suite checks 192 exact families, including 96 nonintegral clocks, balanced rank parity, and both derangement signs. Normal and optimized Python runs agree. None of these finite tests is evidence for [\[eq:h2\]](main.tex#L83){reference-type="eqref" reference="eq:h2"} or any asymptotic theorem.

The exact release status is

`PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_ADJOINT_LANE_SOURCE_GAP`.

The strongest positive result is the literal $w$-lane estimate [\[eq:moment\]](main.tex#L118){reference-type="eqref" reference="eq:moment"}. The strongest obstruction is the unestimated literal form $\langle A_x^*z_{\mathrm{mid}},\beta\rangle$, with norm-only control sharp. The next theorem is therefore a same-clock estimate of this exact $\beta$-linear form retaining the prime shell, outer $q$ weight, both unit masks, deleted diagonal, $K_H$, centered residue bracket, and hard rank midpoint.

The claim ledger remains $$\text{arithmetic advance: scoped $w$ lane};\quad
 \text{fixed-atom credit: }0;\quad L2:\text{ none};\quad
 \text{Gate B: open}.$$ The global strict $1/400$ budget is unpaid, and no twin-prime result follows.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@article{Bombieri1965,
  author  = {Bombieri, Enrico},
  title   = {On the Large Sieve},
  journal = {Mathematika},
  volume  = {12},
  number  = {2},
  pages   = {201--225},
  year    = {1965},
  doi     = {10.1112/S0025579300005313}
}

@article{MontgomeryVaughan1973,
  author  = {Montgomery, Hugh L. and Vaughan, Robert C.},
  title   = {The Large Sieve},
  journal = {Mathematika},
  volume  = {20},
  number  = {2},
  pages   = {119--134},
  year    = {1973},
  doi     = {10.1112/S0025579300004708}
}

@article{Iwaniec1980Rosser,
  author  = {Iwaniec, Henryk},
  title   = {Rosser's Sieve},
  journal = {Acta Arithmetica},
  volume  = {36},
  number  = {2},
  pages   = {171--202},
  year    = {1980},
  doi     = {10.4064/aa-36-2-171-202}
}

@article{Vaughan1977,
  author  = {Vaughan, R. C.},
  title   = {Sommes Trigonom\'etriques sur les Nombres Premiers},
  journal = {Comptes Rendus de l'Acad\'emie des Sciences de Paris, S\'erie A-B},
  volume  = {285},
  number  = {16},
  pages   = {A981--A983},
  year    = {1977}
}

@misc{FordMaynard2024,
  author        = {Ford, Kevin and Maynard, James},
  title         = {On the Theory of Prime-Producing Sieves},
  year          = {2024},
  eprint        = {2407.14368},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT},
  url           = {https://arxiv.org/abs/2407.14368}
}

@misc{compiler,
  author = {Wang, Liang},
  title  = {Tensor-Local {Ford--Maynard} Redesign: Local Comparison Compiler},
  year   = {2026},
  note   = {Repository source-locked working artifact, SHA-256 4f7537ff5a10d53634638afff508ee6e3401364dab7970852b327470918c644f}
}

@misc{tpc253,
  author = {Wang, Liang},
  title  = {Source-Frozen Rank-Midpoint Contrasts for the Literal {V59} Scalar},
  year   = {2026},
  note   = {TPC-253 project-local repository paper, August 26, 2026}
}
```

<!-- SOURCE_BODY_END -->
