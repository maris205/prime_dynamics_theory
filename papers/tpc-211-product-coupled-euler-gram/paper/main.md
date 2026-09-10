# **Product-Coupled Euler Profiles\ and the Möbius–Logarithmic Gram Constraint**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-210 showed that independent Schwartz/Poisson profiles can realize a Möbius-aligned cross-divisor Gram obstruction, while explicitly leaving open the literal physical coupling of the twin-prime coefficients. This paper freezes the product-coupled local profiles from the V46 transition compiler and studies that interface exactly at finite modulus. For active primes $p>z$, lift every squarefree divisor profile to the common CRT space modulo $M=\prod p$. We prove an exact product cocycle and show, by a Fourier-support triangularity argument, that the nonempty defect profiles are linearly independent: literal product coupling has full divisor rank and therefore does not itself imply a low-rank saving. In the opposite direction, a complete squarefree divisor packet has an exact logarithmic Möbius derivative: the $\mu(d)\log d$ weighted profile sum collapses to one marked-prime Euler atom per active prime, while the common product-frozen endpoint cancels for packets with at least two primes. The actual transition interval is a truncated packet, so the missing-subset boundary and the reciprocal emitter remain unpaid. Finally, positive-definite Gram duality constructs a single finite shared endpoint that realizes the Möbius-aligned correlations for all product-coupled profiles. This is a scoped obstruction to saving theorems based only on product rank or common endpoint data, not an arithmetic counterexample for $\Lambda(u+2)-b_x^{(z)}(u)$. The maximum claim is `PROVED_STRUCTURAL_L1 / STOP_SCOPED_PHYSICAL_COUPLING`; no arithmetic $L^2$ advance or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

=2em

# Question and claim ceiling

The preceding TPC-209 and TPC-210 stages isolate a precise interface in the prime-dynamics route. Whole-frame Poisson reindexing leaves one dual profile per divisor. If the profiles are treated as independently admissible, a finite Schwartz construction realizes exact Möbius alignment and defeats any universal profile-norm saving `\cite{WangTPC209,WangTPC210}`. That construction does not use the literal relation between the shifted-prime tensor and the hybrid tensor in the physical transition compiler. The next question is therefore:

> Does the product coupling of the actual local Euler factors force a useful cross-divisor rank or Gram cancellation?

This note gives the finite structural answer. There are two parts.

1.  The product family is rigid, but not low rank: all nonempty divisor defects are independent on a common CRT space.

2.  The physical logarithmic Möbius weight is also rigid: on a complete divisor packet it is an exact marked-prime derivative and annihilates the common endpoint.

The distinction between a complete packet and the actual transition window is the central firewall. The physical interval uses $Y_0<d\leq U$ and a reciprocal occupancy depending on $d$; it is not closed under taking divisors. We prove the complete-packet identity but do not replace the truncated object by it.

The claim ceiling is $$\boxed{\texttt{PROVED\_STRUCTURAL\_L1 / STOP\_SCOPED\_PHYSICAL\_COUPLING}.}$$ In particular, this paper contains no source-backed prime-distribution estimate, no Gate-B power saving, no fixed-atom credit, and no twin-prime theorem.

# The literal product-coupled profile family

Fix distinct odd primes $$\mathcal P=\{p_1,\ldots,p_s\},\qquad z< p_1,\qquad
 M=\prod_{p\in\mathcal P}p.
 \tag{2.1}$$ The cutoff condition is the finite version of the V46 regime in which the active primes exceed the hybrid cutoff. For $a\in\mathbb Z/p\mathbb Z$, define $$F_p(a)=\frac{p}{p-1}\mathbf 1_{a\not\equiv-2\pmod p},
 \tag{2.2}$$ and $$G_{p,z}(a)=
 \begin{cases}
 \dfrac{p}{p-1},&a\equiv0\pmod p,\\[2mm]
 \dfrac{p(p-2)}{(p-1)^2},&a\not\equiv0\pmod p.
 \end{cases}
 \tag{2.3}$$ These are exactly the two local factors used in the V46 proper-factor profile `\cite{WangV46}`. Both have normalized mean one, and their values agree at the zero residue: $$\frac1p\sum_{a\bmod p}F_p(a)=
 \frac1p\sum_{a\bmod p}G_{p,z}(a)=1,
 \qquad F_p(0)=G_{p,z}(0)=\frac{p}{p-1}.
 \tag{2.4}$$

For a nonempty subset $S\subseteq\mathcal P$, write $d_S=\prod_{p\in S}p$ and lift the divisor profile to $\mathbb Z/M\mathbb Z$ by $$P_S(a)=\prod_{p\in S}F_p(a),\qquad
 B_S(a)=\prod_{p\in S}G_{p,z}(a),\qquad
 \Delta_S(a)=P_S(a)-B_S(a).
 \tag{2.5}$$ Factors belonging to $\mathcal P\setminus S$ are understood as the constant function one. Thus all profiles in (2.5) live in the same finite Hilbert space $\mathcal H_M=\mathbb C^{\mathbb Z/M\mathbb Z}$ with counting inner product.

The lift is only a comparison device. The physical V46 residual is instead assembled one modulus at a time: $$\mathcal R_d(a)=
 \sum_{\substack{u\in I_x\\u\equiv a\pmod d}}
 \frac{w(u)-\Delta_d(a)}{\log u},
 \qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u).
 \tag{2.6}$$ The common CRT space allows us to ask which identities are forced by the literal profile family before the $d$-dependent reciprocal emitter is applied.

> **Proposition: zero axis and product cocycle** <span id="prop:cocycle" label="prop:cocycle">\[prop:cocycle\]</span> For every nonempty $S$, $$\Delta_S(0)=0,\qquad
>  \frac1M\sum_{a\bmod M}\Delta_S(a)=0.
>  \tag{2.7}$$ If $S,T$ are disjoint and nonempty, then pointwise $$\Delta_{S\cup T}
>  =P_S\Delta_T+B_T\Delta_S
>  =B_S\Delta_T+P_T\Delta_S.
>  \tag{2.8}$$

> **Proof** Equation (2.7) follows by multiplying the local equalities in (2.4) and using the product form of normalized CRT averages. For (2.8), expand $$P_SP_T-B_SB_T=P_S(P_T-B_T)+B_T(P_S-B_S),$$ and then interchange the roles of $S$ and $T$ for the second expression.

The cocycle is the first literal cross-divisor coupling relation. It is stronger than declaring one arbitrary profile per divisor, but it does not yet say that the resulting family occupies a small subspace. The next theorem answers that rank question exactly.

# Full divisor rank from Fourier support

For a function $f$ on $\mathbb Z/p\mathbb Z$, use the normalized transform $$\widehat f(k)=\frac1p\sum_{a\bmod p}f(a)e_p(-ka),
 \qquad e_p(v)=\mathrm e^{2\pi i v/p}.
 \tag{3.1}$$ The local transforms of (2.2)–(2.3) are $$\widehat F_p(0)=\widehat G_{p,z}(0)=1,
 \tag{3.2}$$ and, for $k\not\equiv0\pmod p$, $$\widehat F_p(k)=-\frac{e_p(2k)}{p-1},\qquad
 \widehat G_{p,z}(k)=\frac1{(p-1)^2}.
 \tag{3.3}$$ The formula for $F_p$ follows by subtracting its single forbidden residue from the complete additive sum. For $G_{p,z}$, the nonzero frequency is the difference between its value at zero and its common value on nonzero residues.

For a frequency vector $\boldsymbol k=(k_p)_{p\in\mathcal P}$ in the CRT Fourier group, let $$\operatorname{supp}(\boldsymbol k)=\{p:k_p\not\equiv0\pmod p\}.$$

> **Theorem: full rank of the literal defect family** <span id="thm:fullrank" label="thm:fullrank">\[thm:fullrank\]</span> The family $$\{\Delta_S:\varnothing\ne S\subseteq\mathcal P\}
>  \subseteq \mathcal H_M
>  \tag{3.4}$$ is linearly independent. Consequently its span has dimension $2^s-1$, exactly the number of nonempty squarefree divisors of $M$.

> **Proof** Let $T\ne\varnothing$ and choose a CRT frequency vector with support exactly $T$. By the tensor-product Fourier rule, the coefficient of $\Delta_S$ at this frequency is zero unless $T\subseteq S$. If $T\subseteq S$, the coordinates in $S\setminus T$ contribute their zero Fourier coefficient one, so the coefficient is independent of $S$ and equals $$C_T(\boldsymbol k)=
>  \prod_{p\in T}\widehat F_p(k_p)
>  -\prod_{p\in T}\widehat G_{p,z}(k_p).
>  \tag{3.5}$$ The two terms in (3.5) have different absolute values: $$\left|\prod_{p\in T}\widehat F_p(k_p)\right|
>  =\prod_{p\in T}\frac1{p-1},\qquad
>  \left|\prod_{p\in T}\widehat G_{p,z}(k_p)\right|
>  =\prod_{p\in T}\frac1{(p-1)^2}.
>  \tag{3.6}$$ Hence $C_T(\boldsymbol k)\ne0$.
>
> Suppose $\sum_{S\ne\varnothing}c_S\Delta_S=0$. Taking the Fourier coefficient at a frequency with support $T$ gives $$C_T(\boldsymbol k)\sum_{S\supseteq T}c_S=0,
>  \qquad\text{so}\qquad
>  \sum_{S\supseteq T}c_S=0.
>  \tag{3.7}$$ This holds for every nonempty $T$. Mobius inversion on the Boolean subset lattice now gives $c_S=0$ for all nonempty $S$.

> **Remark** The theorem is a physical-coupling result and a negative rank result at the same time. It proves that the literal product relation is present, but that the relation retains the full number of divisor degrees of freedom. A rank-only argument cannot provide the missing power saving.

# The logarithmic Möbius packet derivative

The full-rank theorem does not make the product structure useless. The transition coefficient on the $d\le U$ side of V43/V46 is $$\vartheta_x(d;u)=-\frac{\mu(d)\log d}{\log u}.
 \tag{4.1}$$ The logarithm is additive over prime factors, and this creates an exact derivative when the full divisor packet is present.

Write $\ell_p$ for an arbitrary scalar attached to $p$, set $\ell(S)=\sum_{p\in S}\ell_p$, and for any local values $X_p$ put $X_S=\prod_{p\in S}X_p$ with $X_\varnothing=1$.

> **Lemma: Boolean logarithmic derivative** <span id="lem:derivative" label="lem:derivative">\[lem:derivative\]</span> For every finite prime set $\mathcal P$, $$\sum_{S\subseteq\mathcal P}(-1)^{|S|}\ell(S)X_S
>  =-\sum_{p\in\mathcal P}\ell_pX_p
>      \prod_{r\in\mathcal P\setminus\{p\}}(1-X_r).
>  \tag{4.2}$$ Here $\ell(\varnothing)=0$.

> **Proof** Expand the right side. A fixed subset $S$ occurs once for every marked prime $p\in S$, with coefficient $(-1)^{|S|}\sum_{p\in S}\ell_p$.

> **Theorem: complete-packet product derivative** <span id="thm:packet" label="thm:packet">\[thm:packet\]</span> With $\ell_p=\log p$ and $\mu(d_S)=(-1)^{|S|}$, $$\sum_{\varnothing\ne S\subseteq\mathcal P}
>  \mu(d_S)\log(d_S)\Delta_S
>  =-\sum_{p\in\mathcal P}\log p\,\mathcal D_p,
>  \tag{4.3}$$ where $$\mathcal D_p(a)=
>  P_{\{p\}}(a)\prod_{r\ne p}(1-P_{\{r\}}(a))
>  -B_{\{p\}}(a)\prod_{r\ne p}(1-B_{\{r\}}(a)).
>  \tag{4.4}$$ If $|\mathcal P|\ge2$, then $$\sum_{\varnothing\ne S\subseteq\mathcal P}
>  \mu(d_S)\log(d_S)=0.
>  \tag{4.5}$$

> **Proof** Apply Lemma [\[lem:derivative\]](main.tex#L294){reference-type="ref" reference="lem:derivative"} pointwise with $X_p=F_p(a)$ and then with $X_p=G_{p,z}(a)$; subtract the two identities. This gives (4.3)–(4.4). For (4.5), apply the same lemma with $X_p=1$. Every product on the right contains a zero factor when there are at least two primes.

The packet identity has a direct physical interpretation. At a fixed endpoint $u$, let $$R_S(u)=w(u)-\Delta_S(u),
 \tag{4.6}$$ where the argument means the CRT residue of $u$. The complete product-frozen transition bracket is $$\sum_{S\ne\varnothing}
 \left(-\frac{\mu(d_S)\log(d_S)}{\log u}\right)R_S(u).
 \tag{4.7}$$ For at least two active primes, (4.5) removes the common $w(u)$ term and leaves exactly $$\frac1{\log u}
 \sum_{S\ne\varnothing}\mu(d_S)\log(d_S)\Delta_S(u),
 \tag{4.8}$$ which is the marked-prime expression (4.3) divided by $\log u$. This is an exact algebraic compression, not an estimate.

# Why the complete packet does not finish the physical gate

The V46 Poisson/compiler interface writes the transition residual as $$\mathfrak R_x^{\rm AP}
 =-H\sum_{Y_0<d\le U}\sum_{r\bmod d}
 A_d(r)\widehat{\mathcal R}_d(r),
 \tag{5.1}$$ where $$A_d(r)=\frac{\mu(d)\log d}{d}
 \sum_{q\in\mathcal Q}\sum_{0<|m|\le dq/H}
 \psi\!\left(\frac{Hm}{dq}\right)
 \mathbf 1_{r\equiv m\overline q\ (d)},
 \tag{5.2}$$ and $\mathcal R_d$ is the physical residue vector in (2.6). The complete packet theorem would apply to a fixed $t$ only if all squarefree divisors of $\operatorname{rad}(t)$ entered with the same endpoint and no divisor cut. The actual active set is $$\mathcal A_{Y,U}(t)=\{d:d\mid t,\ Y_0<d\le U,\ \mu^2(d)=1\}.
 \tag{5.3}$$ It is generally not the full Boolean lattice and is not downward closed.

For a squarefree $M$ and any subset $\mathcal A$ of its nonempty divisors, define the formal endpoint coefficient vector $$E_{\mathcal A,p}=
 \sum_{\substack{S:d_S\in\mathcal A\\p\in S}}
 \mu(d_S).
 \tag{5.4}$$ The full packet has $E_{\mathcal A,p}=0$ for every $p$ when $s\ge2$, but a truncated packet need not. For example, with active primes $5,7$, the set ${\mathcal A}=\{7,35\}$ has $$E_{\mathcal A,5}=1,\qquad E_{\mathcal A,7}=0,
 \tag{5.5}$$ so its common endpoint coefficient is not cancelled. The missing-subset boundary is therefore a real term, not a cosmetic change of notation.

The exact decomposition is $$\sum_{d\in\mathcal A_{Y,U}(t)}\mu(d)\log d\,R_d(u)
 =\sum_{d\mid\operatorname{rad}(t),\ d>1}
   \mu(d)\log d\,R_d(u)
 -\mathcal B_{Y,U}(t;u),
 \tag{5.6}$$ where $\mathcal B_{Y,U}$ is the sum over the missing divisors. The first term has the marked-prime derivative form, but (5.6) gives no bound for the boundary. Moreover, (5.2) varies with $d$ through both the reciprocal residue map and the cutoff $dq/H$. The current paper pays neither the boundary nor this emitter coupling.

> **Proposition: complete-packet cancellation is not a transition bound** <span id="prop:boundary" label="prop:boundary">\[prop:boundary\]</span> The identity (4.8) is a valid compiler for a complete product packet. It does not imply a bound for (5.1) unless one additionally proves a uniform estimate for the boundary (5.6) after pairing with (5.2).

> **Proof** The first statement is Theorem [\[thm:packet\]](main.tex#L312){reference-type="ref" reference="thm:packet"}. The second follows from the exact subtraction (5.6): the missing-divisor terms have nonzero endpoint coefficients in general, and their weights in (5.2) are not common across divisors. No cancellation from (4.3) applies to them without a new estimate.

# A shared-endpoint Gram obstruction

The full-rank result has a second consequence. Let $$G_{S,T}=\left\langle \Delta_S,\Delta_T\right\rangle_{\mathcal H_M}.
 \tag{6.1}$$ By Theorem [\[thm:fullrank\]](main.tex#L226){reference-type="ref" reference="thm:fullrank"}, $G$ is positive definite.

> **Theorem: finite shared-endpoint interpolation** <span id="thm:shared" label="thm:shared">\[thm:shared\]</span> For every target vector $(y_S)_{S\ne\varnothing}\in\mathbb C^{2^s-1}$ there is a single $w\in\operatorname{span}\{\Delta_S\}$ such that $$\left\langle w,\Delta_S\right\rangle_{\mathcal H_M}=y_S
>  \qquad(S\ne\varnothing).
>  \tag{6.2}$$ In particular, with $y_S=\mu(d_S)$, the weighted correlations $$Y_S=\mu(d_S)\left\langle w,\Delta_S\right\rangle
>  \tag{6.3}$$ are all equal to one. Therefore $$\frac{\left|\sum_{S\ne\varnothing}Y_S\right|^2}
>  {\sum_{S\ne\varnothing}|Y_S|^2}=2^s-1.
>  \tag{6.4}$$

> **Proof** Positive definiteness of $G$ gives a unique coefficient vector $\alpha$ with $G\alpha=y$. Taking $w=\sum_T\alpha_T\Delta_T$ gives (6.2), up to the choice of the harmless inner-product convention. For $y_S=\mu(d_S)$, equation (6.3) is one for every $S$, and (6.4) follows by direct summation.

This is a sharper scope result than the independent-profile construction in TPC-210: the profiles themselves are now the literal product-coupled V46 defects, and only the common finite endpoint is chosen by Gram duality. It is still not an arithmetic counterexample. The endpoint in Theorem [\[thm:shared\]](main.tex#L448){reference-type="ref" reference="thm:shared"} need not equal $\Lambda(u+2)-b_x^{(z)}(u)$, need not obey the interval support, and does not include the $d$-dependent emitter (5.2). The correct conclusion is therefore a design constraint:

> Any saving theorem must use arithmetic information beyond product coupling, finite rank, and a common endpoint. It must control the truncated boundary and the reciprocal physical emitter before taking the outer absolute value.

# Exact certificate and adversarial checks

The project certificate uses exact rational arithmetic at cutoff $z=3$ for three active-prime sets. The profile rank is computed by rational Gaussian elimination; the Gram determinant and the dual endpoint are also exact. The derivative identity is checked coefficientwise, without representing $\log p$ numerically. The independent checker reimplements all local factors, profiles, rank, Gram solve, cocycle, and derivative calculations rather than importing the producer.

<div id="tab:certificate">

| active primes |   $M$|  profiles|  rank|  alignment ratio| derivative |
|:--------------|-----:|---------:|-----:|----------------:|:-----------|
| $(5,7)$       |    35|         3|     3|                3| pass       |
| $(5,7,11)$    |   385|         7|     7|                7| pass       |
| $(5,7,11,13)$ |  5005|        15|    15|               15| pass       |

: TPC-211 finite structural certificate.

</div>

Across the three cases the certificate covers 25 profile rows, 77,875 CRT residue coordinates, 9 marked-prime derivative rows, three nonzero Gram determinants, and three shared-endpoint constructions. The producer, independent checker, optimized independent checker, and human-readable sanity script all pass. These finite results certify the algebraic statements and their implementation only; they are not asymptotic evidence.

# Route decision

The structural threshold advances because the actual V46 product coupling has now been analyzed rather than left as an unspecified physical constraint. The strongest positive result is the complete-packet marked-prime derivative (4.3), which is a candidate compiler for the next stage. The strongest obstruction is Theorem [\[thm:fullrank\]](main.tex#L226){reference-type="ref" reference="thm:fullrank"} together with Theorem [\[thm:shared\]](main.tex#L448){reference-type="ref" reference="thm:shared"}: product coupling retains full divisor rank and can still support finite Möbius-aligned correlations under a shared endpoint surrogate.

The next open theorem is narrower than the original TPC-210 question. It is to control the boundary between (5.3) and the full divisor lattice after the marked-prime derivative is extracted, with $A_d(r)$ retained as the literal reciprocal occupancy. Until that estimate is proved, the transition gate, arithmetic $L^2$, strict $1/400$ margin, and twin-prime endpoint remain open.

`TPC211_ROUTE_ADVANCE = YES`\
`TPC211_ARITHMETIC_ADVANCE = NO`\
`TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID`

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{WangTPC209,
  author = {Liang Wang},
  title = {Whole-Frame Poisson Reindexing and the Mobius-Dilation Obstruction},
  year = {2026},
  note = {TPC-209 internal research release, prime dynamics theory repository}
}

@misc{WangTPC210,
  author = {Liang Wang},
  title = {Poisson Profile Realizability and the Mobius Alignment Obstruction},
  year = {2026},
  note = {TPC-210 internal research release, prime dynamics theory repository}
}

@misc{WangV43,
  author = {Liang Wang},
  title = {Proper-Factor Poisson Transference and the Long-Mobius Frontier},
  year = {2026},
  note = {V43 internal route artifact, prime dynamics theory repository}
}

@misc{WangV46,
  author = {Liang Wang},
  title = {Transition-Native Euler Carrier and the AP--BDH Residual Gate},
  year = {2026},
  note = {V46 internal route artifact, prime dynamics theory repository}
}
```

<!-- SOURCE_BODY_END -->
