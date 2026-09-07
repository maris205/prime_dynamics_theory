# Externally Motivated Weight Laws on a Finite Prime–Shell Diagnostic

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 30 August 2026
- Source repository commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`
- Converter: `source-markdown-audit-v2`

## Abstract

We audit the dependence of a finite prime–shell diagnostic on its weighting law. The physical panel is frozen from TPC-312: the source interval is $I=\{321,\ldots,640\}$, the kernel height is $H=66$, and the shells are $S_Q=\{p:Q<p\leq 2Q\}$ for $Q\in\{24,36,54,80\}$ and exponents $s\in\{1,2\}$. We compare counting weight $1$, reduced-residue weight $1/(p-1)$, and prime von-Mangoldt weight $\log p$. The first two laws are rational; the logarithm is enclosed by a rational range-reduced atanh series with a positive tail bound, followed by directed rounding on a $10^{-36}$ decimal grid. Across 48 target/law cases, every Gram-minimum target remains strictly below the normalized level one and every all-positive control remains strictly above it. The finite class is therefore robust across the declared positive laws. The amplitude is not law invariant: one minimum-order crossover occurs and the positive control has four strict law-order types. These are finite source-first facts, not a canonical-weight theorem, an external physical holdout, an asymptotic estimate, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and route position

The preceding TPC-312 release moved the physical calculation to a new source–shell panel and found exact finite sign separation. TPC-313 then closed a profile-budget interface on that panel using rational primal/dual witnesses and outward intervals. The remaining local question is whether the observed class is an artifact of an unexamined weight convention.

This paper makes the smallest useful audit. It declares three positive laws before evaluating the weighted quadratic forms, keeps the physical operator and the target labels fixed, and checks both the class relative to one and the ordering of the resulting amplitudes. The laws are externally motivated in the narrow sense that they occur naturally in arithmetic notation: prime tuple formulas use the von-Mangoldt function, while sieve and reduced-residue calculations use Euler-totient normalizations `\cite{cantarini2018,revesz2021,banksfordtao2023}`. Those references do not select a canonical law for this diagnostic.

# Frozen physical object and three laws

At scale $640$ the locked source rule supplies rational coefficients $\beta_t$. For $p\in S_Q$ define the deleted-diagonal output $$g_p(u)=\sum_{\substack{t\in I,\, t\ne u\\p\nmid ut}}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left({\bf1}_{u\equiv t\pmod p}-\frac1{p-1}\right)\beta_t.
 \label{eq:output}$$ The physical Gram matrix is $$G_{p,q}=\sum_{u\in I}g_p(u)g_q(u).
 \label{eq:gram}$$ All quantities in [\[eq:output\]](main.tex#L66){reference-type="eqref" reference="eq:output"}–[\[eq:gram\]](main.tex#L71){reference-type="eqref" reference="eq:gram"} are rational.

For a sign target $c\in\{-1,+1\}^{S_Q}$ and a positive weight vector $w$, we audit $$E_w(c)=\sum_{p,q\in S_Q}c_pc_qw_pG_{p,q}w_q,
 \qquad
 D_w=\sum_{p\in S_Q}w_p^2G_{p,p},
 \qquad R_w(c)=\frac{E_w(c)}{D_w}.
 \label{eq:weighted}$$ The three declared laws are $$w_p^{\rm C}=1,\qquad
 w_p^{\rm R}=\frac1{p-1}=\frac1{\varphi(p)},\qquad
 w_p^{\Lambda}=\log p.
 \label{eq:laws}$$ Here C means counting and R means reduced-residue normalization. The symbol $\Lambda$ only records the prime-support identity $\Lambda(p)=\log p$; it is not an assertion that the full von-Mangoldt source has been identified with the physical operator.

The lower target $c^-$ is the exact Gram-minimum sign vector inherited from TPC-312. The control $c^+=(1,\ldots,1)$ is fixed independently of the weight-law calculation. Thus this release audits weighting robustness, but it does not remove the target-Gram leakage of the inherited minimum.

# Exact identities and logarithmic enclosure

> **Lemma: Weighted Gram identity** For every finite coefficient vector $c$, $$E_w(c)=\left\|\sum_{p\in S_Q}c_pw_pg_p\right\|_2^2.
>  \label{eq:psd}$$ In particular $E_w(c)\geq0$.

> **Proof** Insert $G_{p,q}=\langle g_p,g_q\rangle$ into the right side of [\[eq:weighted\]](main.tex#L82){reference-type="eqref" reference="eq:weighted"} and expand the finite square. Positivity follows from the norm representation.

> **Lemma: Positive normalizer and scale invariance** If one physical component is nonzero and all $w_p>0$, then $D_w>0$. For $a>0$, $R_{aw}(c)=R_w(c)$.

> **Proof** The diagonal terms are $w_p^2\|g_p\|_2^2$, so at least one is strictly positive. Replacing $w$ by $aw$ multiplies both numerator and denominator in [\[eq:weighted\]](main.tex#L82){reference-type="eqref" reference="eq:weighted"} by $a^2$.

> **Proposition: Rational enclosure for $\log p$** Let $k=\lfloor\log_2p\rfloor$, $y=p/2^k$, and $z=(y-1)/(y+1)$. For $N\geq1$, $$\log p=k\log2+2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1}+\mathcal E_N(z),
>  \qquad
>  0\leq\mathcal E_N(z)\leq
>  \frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
>  \label{eq:logbound}$$ For the declared primes, $0\leq z\leq1/3$; the same formula with $z=1/3$ encloses $\log2$.

> **Proof** The range reduction gives $1\leq y<2$ and hence $0\leq z\leq1/3$. The identity $\log y=2\operatorname{atanh}z$ gives the positive series $$2\operatorname{atanh}z=2\sum_{j\geq0}\frac{z^{2j+1}}{2j+1}.$$ After the first $N$ terms, every denominator is at least $2N+1$ and the remaining powers form a geometric series. This proves the upper bound in [\[eq:logbound\]](main.tex#L135){reference-type="eqref" reference="eq:logbound"}; the lower bound is the partial sum.

The implementation fixes $N=120$. It stores the partial sum and the stated tail as rational numbers, then applies floor rounding to every lower endpoint and ceiling rounding to every upper endpoint on the grid $10^{-36}$. The four-endpoint product rule and the usual positive-denominator quotient rule are applied to the numerator and denominator in [\[eq:weighted\]](main.tex#L82){reference-type="eqref" reference="eq:weighted"}.

> **Proposition: Finite interval soundness** If the input intervals contain their exact values, the stored intervals for $E_w(c)$, $D_w$, and $R_w(c)$ contain the corresponding exact quantities.

> **Proof** For multiplication, the minimum and maximum of the four endpoint products enclose the product of two closed intervals. Addition and subtraction use the corresponding endpoint sums, and division is valid because the positive normalizer interval avoids zero. Rounding outward after each rational operation preserves containment. Induction over the finite expression tree proves the claim.

# Finite protocol and results

The panel has source interval $I=\{321,\ldots,640\}$, height $66$, and shell cardinalities $6,9,12,15$. There are eight $(Q,s)$ rows, three laws, and two targets per law, hence 48 cases. The producer and an independent checker rebuild all physical outputs. The checker loads only the frozen TPC-268 engine, copies the physical formula, reconstructs the logarithm enclosure, and verifies every stored endpoint and digest.

<div id="tab:ratios">

|  $Q$|  $s$|  $R_{\rm C}^-$|  $R_{\rm C}^+$|  $R_{\rm R}^-$|  $R_{\rm R}^+$|  $R_{\Lambda}^-$|  $R_{\Lambda}^+$|
|----:|----:|--------------:|--------------:|--------------:|--------------:|----------------:|----------------:|
|   24|    1|   0.5046844043|   2.7588516494|   0.5343019992|   2.7806283162|     0.4981386678|     2.7326955213|
|   24|    2|   0.4591169907|   2.7737466027|   0.4960763817|   2.7373946236|     0.4569513071|     2.7627568709|
|   36|    1|   0.4555424591|   3.8098670069|   0.5363040329|   3.7887642454|     0.4460812824|     3.7691270301|
|   36|    2|   0.3532719682|   4.5887285052|   0.4736646939|   4.2879868504|     0.3322688772|     4.6084942879|
|   54|    1|   0.3255776085|   5.5005051240|   0.3509816847|   5.2612264299|     0.3320366954|     5.5032145409|
|   54|    2|   0.1642611051|   8.6101405940|   0.2073805255|   7.9839715365|     0.1627341242|     8.6651313955|
|   80|    1|   0.2204253917|   8.6831893234|   0.3371229033|   8.0954955633|     0.2064153735|     8.7317475797|
|   80|    2|   0.0849742942|  13.5606805960|   0.2781066082|  12.9376217231|     0.0669524914|    13.5616765267|

: Weighted ratios. Entries are exact decimal renderings for C and R; the $\Lambda$ entries are centers of their directed intervals. Classification uses interval endpoints, not the displayed centers.

</div>

The certificate records 24/24 minimum intervals with upper endpoint below one and 24/24 positive-control intervals with lower endpoint above one. Thus all three declared positive laws preserve the finite separation class. The amplitude audit gives a different message. In ascending order, the minimum ratios are $\Lambda<C<R$ on seven rows, but $C<\Lambda<R$ on the $(Q,s)=(54,1)$ row. The positive-control ratios exhibit four strict order types: $$\Lambda<C<R,\quad R<\Lambda<C,\quad
 \Lambda<R<C,\quad R<C<\Lambda.$$ The interval endpoints are disjoint for every adjacent comparison, so these are not rounding ties.

# Interpretation and claim firewall

The positive result is narrow but useful: within this locked finite panel, the choice among three arithmetically recognizable positive laws does not decide whether the Gram-minimum target is below the normalized level while the all-positive control is above it. The rational logarithm certificate also removes an otherwise easy source of hidden floating-point dependence.

The obstruction is equally important. Weighting changes the geometry’s amplitude and can change its order even while preserving the coarse class. Consequently the experiment does not identify a canonical measure, and a future preference claim cannot silently select the law that produces the most convenient number. Moreover, the minimum label was selected from the same physical Gram matrix, and the panel is not an external holdout. No statement here controls a growing family of shells or source intervals. In particular, the certificate pays no arithmetic $L^2$ estimate, fixed-power credit, or Route-B Gate-B passage.

# Conclusion and next gate

TPC-314 establishes a finite, independently replayed weighting-law audit: three declared positive laws give 48 enclosed target cases, with strict below-one classification for all 24 minimum cases and strict above-one classification for all 24 positive controls. It also establishes a concrete finite obstruction to law-independent amplitude, consisting of one minimum crossover and four positive-order types.

The next minimal bridge is to freeze this law menu before moving to a fresh source interval, recompute the physical targets there, and test whether the class survives without reusing the present Gram-selected labels. That step would still be finite and would not, by itself, pay the growing arithmetic gate.

#### Route status.

The Session-named Route-A and Route-B evaluator files were absent from the checkout. The included route note is local and fail-closed; this paper makes no official evaluator-pass claim and makes no claim about the twin-prime conjecture.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@article{cantarini2018,
  author       = {Marco Cantarini},
  title        = {Explicit formula for the average of Goldbach and prime tuples representations},
  journal      = {arXiv preprint arXiv:1801.08475},
  year         = {2018},
  url          = {https://arxiv.org/abs/1801.08475}
}

@article{revesz2021,
  author       = {Szil{\'a}rd Gy. R{\'e}v{\'e}sz},
  title        = {A Riemann-von Mangoldt-type formula for the distribution of Beurling primes},
  journal      = {Mathematica Pannonica New Series},
  volume       = {27},
  number       = {1},
  pages        = {204--232},
  year         = {2021},
  url          = {https://arxiv.org/abs/2110.11463}
}

@article{banksfordtao2023,
  author       = {William Banks and Kevin Ford and Terence Tao},
  title        = {Large prime gaps and probabilistic models},
  journal      = {Inventiones Mathematicae},
  volume       = {233},
  pages        = {1471--1518},
  year         = {2023},
  doi          = {10.1007/s00222-023-01199-0},
  url          = {https://doi.org/10.1007/s00222-023-01199-0}
}

@misc{tpc312,
  author       = {Liang Wang},
  title        = {A New Source--Shell Separation Atlas for a Finite Prime-Shell Diagnostic},
  year         = {2026},
  note         = {TPC-312 project release, Huazhong University of Science and Technology}
}

@misc{tpc313,
  author       = {Liang Wang},
  title        = {Outward-Rounded Profile-Budget Interval Certificate},
  year         = {2026},
  note         = {TPC-313 project release, Huazhong University of Science and Technology}
}
```

<!-- SOURCE_BODY_END -->
