# An Additive-Leakage Compiler for Signed Gain and Endpoint Budgets

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding four-packet analysis identifies a normalized deficit of the reassembled energy as the exact input needed for a power gain, but it leaves open how a non-multiplicative error should be charged. We prove a conditional two-term compiler. If $D\ge dX^a$ and $$G\le B X^{-\gamma}D+\ell X^{a-\delta},$$ then $$\frac GD\le B X^{-\gamma}+\frac\ell dX^{-\delta}
 \quad\text{and}\quad
 \frac DG\ge\left(B X^{-\gamma}+\frac\ell dX^{-\delta}\right)^{-1}.$$ The usual one-exponent summary has exponent $\kappa=\min(\gamma,\delta)$ and constant $B+\ell/d$. Combining this with the exact signed-margin identity gives the effective loss $\max(0,\eta_D-\kappa/2)$ and the strict endpoint test $\sigma-\eta_{\rm eff}>1/400$. An equality family proves that the two-term denominator is sharp under the stated hypotheses; in particular, a slower additive leakage term cannot be silently assigned the main-term exponent. Six exact rational budget fixtures, four margin fixtures, four endpoint fixtures, and a twelve-row transfer from the TPC-279 parent are independently certified. No arithmetic $L^2$ estimate or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# The source interface

Let $X\ge1$ be the scale, let $D>0$ denote the packet-diagonal source energy, and let $G\ge0$ denote the energy after signed reassembly. The previous structural criterion uses the ratio $q=G/D$ and gain $r=D/G$ when $G>0$; see the exact four-packet identities in the TPC-279 release `\cite{tpc279}`. In an actual analytic estimate it is natural to separate a main term, proportional to $D$, from a leakage term which is bounded only in absolute scale. We therefore assume $$D\ge dX^a,\qquad
 G\le B X^{-\gamma}D+\ell X^{a-\delta},
 \label{eq:raw}$$ where $d>0$ and $B,\ell,\gamma,\delta\ge0$. The exponent $a$ is deliberately left symbolic; the intended source interface may have $a=5/3$.

The distinction between the two terms matters. A multiplicative estimate can be normalized by $D$ directly, whereas an additive estimate must first use the lower bound on $D$. The next theorem records exactly that operation.

# The two-term compiler

> **Theorem: two-term additive-leakage compiler** Assume [\[eq:raw\]](main.tex#L61){reference-type="eqref" reference="eq:raw"} and set $$c_\ell=\frac\ell d,\qquad \kappa=\min(\gamma,\delta),
>  \qquad C=B+c_\ell.$$ If $C>0$, then $$\begin{aligned}
>  q=\frac GD&\le B X^{-\gamma}+c_\ell X^{-\delta},
>  \label{eq:two-term}\\
>  q&\le C X^{-\kappa}.
>  \label{eq:collapsed}\end{aligned}$$ Consequently, if $G>0$, $$\begin{aligned}
>  r=\frac DG&\ge
>  \left(B X^{-\gamma}+c_\ell X^{-\delta}\right)^{-1}
>  \label{eq:gain-two}\\
>  &\ge C^{-1}X^\kappa.
>  \label{eq:gain-collapsed}\end{aligned}$$ If $C=0$, the hypotheses force $G=0$.

> **Proof** Divide the second inequality in [\[eq:raw\]](main.tex#L61){reference-type="eqref" reference="eq:raw"} by $D$ and use $D^{-1}\le d^{-1}X^{-a}$ for the additive term. This gives [\[eq:two-term\]](main.tex#L81){reference-type="eqref" reference="eq:two-term"}. Since $X\ge1$ and both exponents are at least $\kappa$, $X^{-\gamma},X^{-\delta}\le X^{-\kappa}$, proving [\[eq:collapsed\]](main.tex#L83){reference-type="eqref" reference="eq:collapsed"}. Positive reciprocal reversal gives [\[eq:gain-two\]](main.tex#L89){reference-type="eqref" reference="eq:gain-two"} and [\[eq:gain-collapsed\]](main.tex#L91){reference-type="eqref" reference="eq:gain-collapsed"}. If $C=0$, both terms on the right of [\[eq:raw\]](main.tex#L61){reference-type="eqref" reference="eq:raw"} vanish.

The two-term form is the useful one at finite scales: it retains the crossover between the main and leakage lanes. The collapsed form is the version that can be inserted into an exponent ledger. Notice that the slower decay wins: if $\delta<\gamma$ and $\ell>0$, the leakage term has exponent $\delta$, not $\gamma$.

# Margin and endpoint accounting

The signed four-packet interface carries an exact identity $$m^2=\frac DG m_D^2,
 \label{eq:margin-identity}$$ where $m_D$ is the diagonal margin and $m$ is the margin after reassembly. Equation [\[eq:margin-identity\]](main.tex#L117){reference-type="eqref" reference="eq:margin-identity"} is an interface assumption for this compiler, not a new arithmetic estimate.

> **Corollary: margin compiler** Under the hypotheses of Theorem 1 and [\[eq:margin-identity\]](main.tex#L117){reference-type="eqref" reference="eq:margin-identity"}, $$m^2\ge
>  \frac{m_D^2}{B X^{-\gamma}+c_\ell X^{-\delta}}.
>  \label{eq:margin-two}$$ If, in addition, $m_D\ge cX^{-\eta_D-\varepsilon}$ with $c>0$, then $$m\ge c C^{-1/2}X^{-\eta_D+\kappa/2-\varepsilon}.
>  \label{eq:margin-collapsed}$$ In a ledger which records only nonnegative losses, one may use $$\eta_{\rm eff}=\max(0,\eta_D-\kappa/2).$$

> **Proof** Substitute the gain bound from Theorem 1 into [\[eq:margin-identity\]](main.tex#L117){reference-type="eqref" reference="eq:margin-identity"}. Taking square roots after using [\[eq:collapsed\]](main.tex#L83){reference-type="eqref" reference="eq:collapsed"} gives [\[eq:margin-collapsed\]](main.tex#L133){reference-type="eqref" reference="eq:margin-collapsed"}. If the exponent of $X$ is positive, replacing the corresponding negative loss by zero weakens the lower bound for $X\ge1$.

Suppose the remaining scalar lane has the inherited form $|S|\le A X^{E_0-\sigma+\varepsilon}$. The endpoint ledger then receives the effective saving $\sigma-\eta_{\rm eff}$, so the strict target is $$\sigma-\eta_{\rm eff}>\frac1{400}.
 \label{eq:endpoint}$$ The strict inequality is essential: equality is a borderline unpaid case. The constant $C^{-1/2}$ affects constants, while $\kappa$ controls the power lane.

# Sharpness and the leakage obstruction

> **Proposition: sharpness under the information model** For any admissible $X,d,B,\ell,a,\gamma,\delta$ with $C>0$, the formal choices $$D=dX^a,qquad
>  G=B X^{-\gamma}D+\ell X^{a-\delta}$$ satisfy the hypotheses and make [\[eq:two-term\]](main.tex#L81){reference-type="eqref" reference="eq:two-term"} and [\[eq:gain-two\]](main.tex#L89){reference-type="eqref" reference="eq:gain-two"} equalities. If $\delta<\gamma$ and $\ell>0$, the gain has asymptotic order $X^\delta$ up to constants, so a universal exponent $\gamma$ conclusion is false under these inputs.

> **Proof** Substitution gives $D=dX^a$ and $G/D=BX^{-\gamma}+c_\ell X^{-\delta}$ exactly. When $\delta<\gamma$, the ratio of the main term to the leakage term tends to zero, and the latter determines the order of the sum.

Thus the compiler identifies a precise failure mode for a tempting shortcut: one may not normalize an additive remainder by an upper or nominal source scale. Its actual payment is determined by the available lower bound on $D$. The equality family is an information-model adversary, not a claim that the literal TPC source realizes equality.

# Exact fixtures and parent transfer

The release certificate uses rational arithmetic throughout. Table [1](main.tex#L209){reference-type="ref" reference="tab:budget"} shows representative normalized bounds; “two” is the exact sum in [\[eq:two-term\]](main.tex#L81){reference-type="eqref" reference="eq:two-term"}, while “collapsed” is the coarser right side of [\[eq:collapsed\]](main.tex#L83){reference-type="eqref" reference="eq:collapsed"}.

<div id="tab:budget">

| case                 |  $X$|    $B$|  $\ell/d$|  $\gamma$|  $\delta$|            two / collapsed|
|:---------------------|----:|------:|---------:|---------:|---------:|--------------------------:|
| balanced             |    8|  $1/2$|     $1/3$|         2|         3|       $13/1536\; /\;5/384$|
| slow leak            |   16|      1|         2|         4|         1|     $8193/65536\; /\;3/16$|
| equal exponents      |   10|  $3/5$|     $1/5$|         2|         2|         $1/125\; /\;1/125$|
| no leakage           |    9|  $7/4$|         0|         3|         5|       $7/2916\; /\;7/2916$|
| leakage only         |   32|      0|     $1/2$|         5|         1|           $1/64\; /\;1/64$|
| fractional constants |   25|  $2/3$|     $4/5$|         1|         3|  $6262/234375\; /\;22/375$|

: Exact rational two-term and collapsed normalized bounds.

</div>

The first two rows make the bottleneck visible: in the slow-leakage row the nominal main exponent is $4$, but the certified collapsed exponent is $1$. The leakage-only row is an exact no-main-term adversary. Four margin fixtures replay [\[eq:margin-two\]](main.tex#L128){reference-type="eqref" reference="eq:margin-two"}; their two-term lower bounds are never smaller than the collapsed lower bounds. Four endpoint fixtures classify strict, leakage-limited, borderline, and unpaid cases, including the exact equality in [\[eq:endpoint\]](main.tex#L153){reference-type="eqref" reference="eq:endpoint"}.

As a separate provenance check, the twelve TPC-279 parent rows are copied only in their already-certified $(q,\Delta)$ coordinates. The transfer preserves eight positive-deficit and four negative-deficit rows. This finite census validates the coordinate interface; it does not assert that the literal source has an additive leakage decomposition or a growing deficit.

# Route consequence and claim firewall

The new result is a conditional compiler, not an arithmetic payment. To use it on the twin-prime route one still needs a literal estimate of the form [\[eq:raw\]](main.tex#L61){reference-type="eqref" reference="eq:raw"}, including a source lower bound and a typed identification of the leakage term. In particular, the theorem does not convert a finite table of favorable gains into a power estimate.

| claim                                        | status                                               |
|:---------------------------------------------|:-----------------------------------------------------|
| two-term normalization and gain              | <span class="smallcaps">proved conditional</span>    |
| dominant exponent $\min(\gamma,\delta)$      | <span class="smallcaps">proved conditional</span>    |
| equality-family sharpness                    | <span class="smallcaps">proved conditional</span>    |
| finite rational fixtures and parent transfer | <span class="smallcaps">numerically certified</span> |
| literal growing source decomposition         | <span class="smallcaps">open</span>                  |
| arithmetic $L^2$ / full Gate B               | <span class="smallcaps">open</span>                  |
| fixed-power credit / twin-prime result       | $0$ / <span class="smallcaps">none</span>            |

The Session-named Route A/Route B evaluator files are absent from the checkout; the project proof package, exact certificate, independent checker, stress audit, and fail-closed Bridge-B checker supply the scoped local evaluation.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc279,
  author       = {Liang Wang},
  title        = {A Minimal Coherence-to-Gain Criterion for Four-Packet Reassembly},
  note         = {TPC-279 project release, 2026},
  year         = {2026}
}

@book{hardywright,
  author       = {G. H. Hardy and E. M. Wright},
  title        = {An Introduction to the Theory of Numbers},
  edition      = {6},
  publisher    = {Oxford University Press},
  year         = {2008}
}
```

<!-- SOURCE_BODY_END -->
