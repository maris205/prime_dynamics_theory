# **Multiplicative Quotient Lifts on**\ **Determinant-Two Fibers: Exact Möbius**\ **Recovery and Stable Nonpretentiousness**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-148-quotient-mobius-fiber-lift.pdf](../tpc-148-quotient-mobius-fiber-lift.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The determinant-two pullback previously represented $\mu(D)\mu(V)$ as a Liouville shift-two product multiplied by two quotient-squarefree masks. We give a different exact representation. For every positive integer $c$, an explicit one-bounded multiplicative function $G_c$ satisfies $$G_c(cm)=\mu(m).$$ If $D(z)=d+sz$, $V(z)=u+az$, and $su-ad=2$, then with $t=aD(z)=ad+asz$, $$\mu(D(z))\mu(V(z))=G_a(t)G_s(t+2).$$ Thus the full squarefree information is already inside two multiplicative functions; no prime-square cutoff or CRT squarefree tail is needed for this two-point core.

At prime arguments, $G_c$ differs from the Liouville function only at primes $p$ with $p\parallel c$. Its pretentious distance is therefore bounded below by the Liouville distance minus $2\sum_{p\parallel c}p^{-1}$. For small-polylogarithmic $c$ this loss is lower order than the known logarithmic lower bound. The construction supplies an exact $\mathrm{L0}$ lift and a uniform $\mathrm{L1}$ nonpretentious input. It does not supply physical weights, generic phases, all prefixes, a four-point estimate, positive $\mathrm{L2}$, or a prime-pair theorem.

<!-- SOURCE_BODY_BEGIN -->

# The quotient lift

For a prime $p$, write $e_p=v_p(c)$. We define the local values of $G_c$ before taking their multiplicative product.

> **Definition: Quotient-Möbius lift** <span id="def:Gc" label="def:Gc">\[def:Gc\]</span> For $c\ge1$, let $G_c:\mathbb N\to\{-1,0,1\}$ be the multiplicative function determined by $$G_c(p^j)=
>  \begin{cases}
>   (-1)^j,&0\le j<e_p,\\
>   \mu(p^{j-e_p}),&j\ge e_p.
>  \end{cases}
> \label{eq:local}$$

The two cases agree with $G_c(1)=1$. This is a multiplicative definition through independent prime-power factors. It is generally not completely multiplicative.

> **Theorem: Exact quotient recovery** <span id="thm:quotient" label="thm:quotient">\[thm:quotient\]</span> For every $c,m\ge1$, $$\boxed{G_c(cm)=\mu(m).}
> \label{eq:quotient}$$

> **Proof** For each prime $p$, the exponent of $p$ in $cm$ is $e_p+v_p(m)$, which lies in the second case of [\[eq:local\]](../main.tex#L95){reference-type="eqref" reference="eq:local"}. Its local factor is $\mu(p^{v_p(m)})$. Multiplication over primes gives $\mu(m)$.

> **Remark: Why the first case is retained** Only values on multiples of $c$ are needed for [\[eq:quotient\]](../main.tex#L108){reference-type="eqref" reference="eq:quotient"}; the values below $e_p$ may therefore be chosen. The choice $(-1)^j$ makes the prime values agree with $\lambda(p)=-1$ unless $e_p=1$, which minimizes the pretentious-distance perturbation used below.

# The determinant-two fiber

Let $$D(z)=d+sz,\qquad V(z)=u+az,\qquad su-ad=2,
\label{eq:fiber}$$ with positive integral values on the interval under consideration. In the TPC carrier, $a,s$ are positive, odd and coprime `\citep{WangTPC127}`. Put $$Q_{\rm fib}=as,\qquad t(z)=aD(z)=ad+Q_{\rm fib}z.
\label{eq:t}$$

> **Theorem: Exact determinant-two Möbius lift** <span id="thm:fiber" label="thm:fiber">\[thm:fiber\]</span> For every integer $z$ on which the forms are positive, $$\begin{aligned}
>  t(z)+2&=sV(z),\label{eq:shift}\\
>  t(z)&\equiv ad\pmod{Q_{\rm fib}},\label{eq:progression}\\
>  \mu(D(z))\mu(V(z))
>  &=\boxed{G_a(t(z))G_s(t(z)+2)}
> \label{eq:fiber-lift}\end{aligned}$$

> **Proof** The determinant equation gives $$sV(z)-aD(z)=su-ad=2,$$ which proves [\[eq:shift\]](../main.tex#L146){reference-type="eqref" reference="eq:shift"}; [\[eq:progression\]](../main.tex#L147){reference-type="eqref" reference="eq:progression"} follows from [\[eq:t\]](../main.tex#L139){reference-type="eqref" reference="eq:t"}. Both $a\mid t(z)$ and $s\mid t(z)+2$. gives $$G_a(t(z))=\mu(t(z)/a)=\mu(D(z)),
>  \quad
>  G_s(t(z)+2)=\mu((t(z)+2)/s)=\mu(V(z)).$$

> **Corollary: No squarefree truncation in the two-point core** <span id="cor:no-tail" label="cor:no-tail">\[cor:no-tail\]</span> The right side of [\[eq:fiber-lift\]](../main.tex#L150){reference-type="eqref" reference="eq:fiber-lift"} contains the full Möbius values. Applying a two-point theorem directly to $G_a(t)G_s(t+2)$ requires neither quotient-squarefree masks nor a prime-square cutoff. Consequently it creates no squarefree truncation tail.

This is a new representation of the same literal core; it does not delete the remaining coprimality, periodic, physical or prefix factors of the full packet.

# Pretentious distance under the lift

For one-bounded multiplicative functions, write $$M(g;Y,Q)
 =
 \inf_{\substack{|v|\le Y\\q\le Q\\\chi\ ({\rm mod}\ q)}}
 \sum_{p\le Y}
 \frac{1-\operatorname{Re}(g(p)\overline{\chi(p)}p^{-iv})}{p}.$$ The convention is the squared pretentious distance used in `\citet{TaoTeravainen2026}`.

> **Lemma: Prime-level perturbation** <span id="lem:prime" label="lem:prime">\[lem:prime\]</span> For every prime $p$, $$G_c(p)=
>  \begin{cases}
>   1,&p\parallel c,\\
>   -1,&p\nparallel c.
>  \end{cases}$$ Thus $G_c(p)\ne\lambda(p)$ precisely when $p\parallel c$.

> **Proof** If $v_p(c)=0$, the second line of [\[eq:local\]](../main.tex#L95){reference-type="eqref" reference="eq:local"} gives $\mu(p)=-1$. If $v_p(c)=1$, it gives $\mu(1)=1$. If $v_p(c)\ge2$, the first line gives $(-1)^1=-1$.

> **Proposition: Uniform nonpretentious stability** <span id="prop:distance" label="prop:distance">\[prop:distance\]</span> For all $Y,Q\ge2$, $$\boxed{
>  M(G_c;Y,Q)
>  \ge M(\lambda;Y,Q)
>  -2\sum_{\substack{p\le Y\\p\parallel c}}\frac1p.}
> \label{eq:distance}$$

> **Proof** Fix one $\chi$ and $v$ in the defining infimum. By [\[lem:prime\]](../main.tex#L195){reference-type="ref" reference="lem:prime"}, the two prime sums agree outside $p\parallel c$. At an exceptional prime, changing one unit-disc value to another changes the real part by at most two. Hence the $G_c$ sum is at least the $\lambda$ sum minus the displayed error. Taking the infimum proves [\[eq:distance\]](../main.tex#L221){reference-type="eqref" reference="eq:distance"}.

> **Lemma: Small-polylogarithmic perturbations are lower order** <span id="lem:reciprocal" label="lem:reciprocal">\[lem:reciprocal\]</span> For $c\ge3$, $$\sum_{p\mid c}\frac1p\ll1+\log_3^+ c,
>  \qquad
>  \log_3^+c:=\max\{0,\log\log\log c\}.$$ In particular, if $c\le(\log X)^A$ for fixed $A$, then this sum is $o(\log_2X)$.

> **Proof** For fixed size of the product of the distinct prime divisors, the reciprocal sum is maximized by the smallest primes. The standard primorial and Mertens estimates then give $\sum_{p\mid c}p^{-1}\ll1+\log_3^+c$. The stated consequence is immediate.

prove, uniformly for characters of modulus at most a fixed small power of $\log X$, $$M(\lambda;X^2,\log^{1/125}X)
 \ge\left(\frac13-o(1)\right)\log_2X.
\label{eq:lambda-distance}$$ Combining the preceding results gives the needed source condition.

> **Corollary: Callable nonpretentious branch** <span id="cor:callable" label="cor:callable">\[cor:callable\]</span> There is an absolute $\alpha>0$ such that, for every fixed $A>0$ and all sufficiently large $X$ depending on $A$, uniformly for $c\le(\log X)^A$, $$\exp M(G_c;X^2,\log^{1/125}X)
>  \gg(\log X)^\alpha.$$ After decreasing $\alpha$, the nonpretentious hypothesis of `\citet[Theorem~3.1]{TaoTeravainen2026}` holds with $\mathcal L=(\log X)^\alpha$.

> **Proof** Equations [\[eq:distance\]](../main.tex#L221){reference-type="eqref" reference="eq:distance"}–[\[eq:lambda-distance\]](../main.tex#L259){reference-type="eqref" reference="eq:lambda-distance"} and [\[lem:reciprocal\]](../main.tex#L235){reference-type="ref" reference="lem:reciprocal"} give $$M(G_c;X^2,\log^{1/125}X)
>  \ge(1/3-o(1))\log_2X.$$ Exponentiate and choose any fixed $\alpha<1/3$, with room for the implicit source constant.

# Scope and machine certificate

The deterministic script evaluates [\[eq:local\]](../main.tex#L95){reference-type="eqref" reference="eq:local"} exactly, verifies [\[eq:quotient\]](../main.tex#L108){reference-type="eqref" reference="eq:quotient"} for thousands of integer pairs, checks ordinary multiplicativity on coprime inputs, and verifies [\[eq:fiber-lift\]](../main.tex#L150){reference-type="eqref" reference="eq:fiber-lift"} on several determinant-two fibers. It records the prime modification set $\{p:p\parallel c\}$. These finite checks are regressions for the algebra; they do not numerically prove [\[eq:lambda-distance\]](../main.tex#L259){reference-type="eqref" reference="eq:lambda-distance"}.

\@p0.48Y@ Statement & Level and status\
$G_c(cm)=\mu(m)$ & Exact $\mathrm{L0}$, $\textnormal{\textsc{proved}}$.\
Determinant-two identity [\[eq:fiber-lift\]](../main.tex#L150){reference-type="eqref" reference="eq:fiber-lift"} & Exact $\mathrm{L0}$, $\textnormal{\textsc{proved}}$.\
Pretentious stability [\[eq:distance\]](../main.tex#L221){reference-type="eqref" reference="eq:distance"} & Unconditional comparison, $\textnormal{\textsc{proved}}$.\
Small-polylog source condition & Sourced quantitative $\mathrm{L1}$, $\textnormal{\textsc{proved}}$.\
Bounded periodic reassembly & Available through TPC-147 `\citep{WangTPC147}`.\
Physical multiplier, generic phase, all prefixes & $\textnormal{\textsc{open}}$; not supplied.\
Four-point input or positive $\mathrm{L2}$ & Not proved.\
Fixed $X$-power, $1/400$, prime pairs & Not proved.\

The lift therefore removes the squarefree-CRT gate for the two-point Möbius core without claiming that a two-point good-scale theorem is the complete H3 input.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{TaoTeravainen2026,
  author        = {Tao, Terence and Ter{\"a}v{\"a}inen, Joni},
  title         = {{Quantitative Correlations and Some Problems on Prime
                    Factors of Consecutive Integers}},
  year          = {2026},
  eprint        = {2512.01739v2},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT}
}

@article{MatomakiRadziwillTao2015,
  author  = {Matom{\"a}ki, Kaisa and Radziwi{\l}{\l}, Maksym and Tao, Terence},
  title   = {{An Averaged Form of Chowla's Conjecture}},
  journal = {Algebra \& Number Theory},
  volume  = {9},
  number  = {9},
  pages   = {2167--2196},
  year    = {2015},
  doi     = {10.2140/ant.2015.9.2167}
}

@misc{WangTPC127,
  author       = {Wang, Liang},
  title        = {{The Determinant-Two Liouville Pullback}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-127-determinant-two-liouville-pullback}}
}

@misc{WangTPC147,
  author = {Wang, Liang},
  title  = {{Periodic Reassembly Inside a Quantitative Multiplicative Correlation Corridor}},
  year   = {2026},
  note   = {TPC-147 manuscript}
}
```

<!-- SOURCE_BODY_END -->
