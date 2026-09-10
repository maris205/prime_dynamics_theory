# **A Top-Prime Direct-Energy Floor\ for the Frozen Common Profile**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China; liang.wang@hust.edu.cn
- Source date: August 24, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We determine the exact asymptotic size of the top-prime, prime-shell-split direct residue-row energy in the frozen V59 common-profile model. For every fixed real profile $\psi\in C_c^\infty(\mathbb{R})$ with $0\leq\psi\leq1$, $\mathop{\mathrm{supp}}\psi\subseteq[-1,1]$, and $\int\psi=1$, let $\kappa_\psi=\int_{-1}^{1}\psi(t)^2\,dt$. At the scales $H=x^{21/32}$, $Q=x^{1/3}$, and $U=x^{133/400}$, we prove $$\mathcal{D}_{\mathrm{top}}^{\psi}=\left(\frac{1197\,\kappa_\psi\log2}{800}
       +o_\psi(1)\right)\frac{Q^2}{H}
       =x^{1/96+o_\psi(1)},
 \qquad \frac12\leq\kappa_\psi\leq1.$$ The proof compiles each fixed-prime signed integer row injectively into primitive residues, applies an endpoint-safe lattice Riemann estimate, and then evaluates two weighted prime sums. The aggregate row error is relatively $O_\psi(x^{-23/2400})$. Consequently this exact unsigned direct factor is not $o(Q^2/H)$ and admits no fixed-power saving. The statement is profilewise, not uniform over the full profile class. It concerns neither the prime-shell-collapsed collision energy nor the signed four-packet scalar; in particular, it does not establish the $x^{1/48}$ collision exponent or full Gate B.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The collision-compressed finite-window route reduces a substantial part of the current twin-prime correlation program to the size of a common-source coefficient vector. The best structural upper assembly presently carries the normalized power $x^{1/48}$, but that estimate is a composition of distinct upper bounds and does not prove that one physical object saturates all of them `\cite{WangTPC237}`. Before searching for another uniform saving, one must know the true scale of the direct factor that enters the composition.

Two earlier results isolate the ingredients. In the top divisor shell, the cluster coefficient contains a single divisor and equals $C_p=-\log(p)/p$ `\cite{WangTPC215}`. For one shell prime $q$, the signed integer emitter is injective modulo the divisor, so its squared row norm is an exact sum of squared atom weights `\cite{WangTPC216}`. Neither result evaluates the aggregate formed by the literal frozen profile, all top primes, and all prime-shell labels. The missing aggregate is the object studied here.

The main theorem gives a positive asymptotic constant. If $\kappa_\psi=\int\psi^2$, then $$\mathcal{D}_{\mathrm{top}}^{\psi}=\left(\frac{1197\,\kappa_\psi\log2}{800}
       +o_\psi(1)\right)\frac{Q^2}{H}.$$ The result has three concrete consequences.

1.  It identifies the exact leading constant for every fixed admissible profile, with $1/2\leq\kappa_\psi\leq1$.

2.  It proves an unavoidable $x^{1/96}$ floor for the q-split unsigned direct energy, thereby ruling out a fixed-power saving at that stage.

3.  It supplies a reusable proof chain: primitive fixed-$q$ injection, endpoint-safe lattice summation, and factorized weighted-prime averaging.

The conclusion is deliberately narrow. The energy keeps $q$ split before squaring, whereas the next collision question sums $q$ inside each residue. The coefficient occurs through $|C_p|^2$, so its sign is unavailable for cancellation. A finite-window consequence follows from nonnegativity and the lower frame of TPC-238 `\cite{WangTPC238}`, but it remains at power $1/96$. Thus this paper is an obstruction theorem for one exact structural factor, not an arithmetic Gate-B advance.

Section [2](sections/2_frozen_setup.tex#L2){reference-type="ref" reference="sec:setup"} freezes the object and quantifiers. Section [3](sections/3_exact_row_riemann.tex#L2){reference-type="ref" reference="sec:rows"} proves the row asymptotic, and Section [4](sections/4_weighted_pnt_aggregation.tex#L2){reference-type="ref" reference="sec:aggregation"} evaluates its prime averages. Sections [5](sections/5_certificate.tex#L2){reference-type="ref" reference="sec:certificate"} and [6](sections/6_route_boundary.tex#L2){reference-type="ref" reference="sec:boundary"} record the executable certificate and the route firewall.

# Frozen source and exact object

Retain the literal V59 scales $$H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400}.
 \label{eq:scales}$$ Write $$\mathcal{P}_{\mathrm{top}}=\{p\ \text{prime}:U/2<p\leq U\},\qquad
 \mathcal{Q}_x=\{q\ \text{prime}:Q<q\leq2Q\}.$$ The exponent ledger contains $$\begin{aligned}
 \frac{U}{Q}&=x^{-1/1200}, &
 \frac{H}{4Q}&=\frac14x^{31/96}, \label{eq:separation}\\
 \frac{UQ}{2H}&=\frac12x^{23/2400}, &
 \frac{H}{UQ}&=x^{-23/2400}.       \label{eq:depth}\end{aligned}$$ In particular, for all sufficiently large $x$, one has $U<Q$ and $4Q<H$.

Fix a function $\psi$ independently of $x$ such that $$\psi\in C_c^\infty(\mathbb{R}),\qquad 0\leq\psi\leq1,\qquad
 \mathop{\mathrm{supp}}\psi\subseteq[-1,1],\qquad
 \int_{-1}^{1}\psi(t)\,dt=1.
 \label{eq:profile}$$ Set $$\kappa_\psi=\int_{-1}^{1}\psi(t)^2\,dt.
 \label{eq:kappa}$$ For $p\in\mathcal{P}_{\mathrm{top}}$, $q\in\mathcal{Q}_x$, and $a\pmod p$, define $$B_{p,q}^{\psi}(a)=
 \sum_{0<|m|\leq\lfloor pq/H\rfloor}
 \psi\!\left(\frac{Hm}{pq}\right)
 \mathbf{1}_{m q^{-1}\equiv a\pmod p},
 \qquad C_p=-\frac{\log p}{p}.
 \label{eq:row}$$ The inverse is legal because $p<q$. Our main object is $$\mathcal{D}_{\mathrm{top}}^{\psi}=
 \sum_{p\in\mathcal{P}_{\mathrm{top}}}|C_p|^2
 \sum_{q\in\mathcal{Q}_x}
 \sum_{\substack{a\bmod p\\(a,p)=1}}
 |B_{p,q}^{\psi}(a)|^2.
 \label{eq:direct-energy}$$ It is unsigned and q-split. There is no complete-period multiplier and no finite-window normalization in [\[eq:direct-energy\]](sections/2_frozen_setup.tex#L51){reference-type="eqref" reference="eq:direct-energy"}.

> **Theorem: top-prime direct-energy asymptotic** <span id="thm:main" label="thm:main">\[thm:main\]</span> For every fixed profile satisfying [\[eq:profile\]](sections/2_frozen_setup.tex#L28){reference-type="eqref" reference="eq:profile"}, $$\frac12\leq\kappa_\psi\leq1
>  \label{eq:kappa-range}$$ and $$\mathcal{D}_{\mathrm{top}}^{\psi}=
>  \left(\frac{1197\,\kappa_\psi\log2}{800}+o_\psi(1)\right)
>  \frac{Q^2}{H}
>  =x^{1/96+o_\psi(1)}.
>  \label{eq:main-asymptotic}$$ The quantifier is profilewise: for every fixed admissible $\psi$ and every $\varepsilon>0$, there exists $x_0(\psi,\varepsilon)$ such that the asymptotic estimate holds for all $x\geq x_0(\psi,\varepsilon)$. No threshold uniform over the whole profile class is asserted.

Theorem [\[thm:main\]](sections/2_frozen_setup.tex#L57){reference-type="ref" reference="thm:main"} will follow from the row calculation in Section [3](sections/3_exact_row_riemann.tex#L2){reference-type="ref" reference="sec:rows"} and the prime averages in Section [4](sections/4_weighted_pnt_aggregation.tex#L2){reference-type="ref" reference="sec:aggregation"}.

# Primitive row identity and lattice asymptotic

The norm interval for the profile is immediate but will make the final constant strictly positive.

> **Lemma: profile norm interval** <span id="lem:kappa" label="lem:kappa">\[lem:kappa\]</span> Under [\[eq:profile\]](sections/2_frozen_setup.tex#L28){reference-type="eqref" reference="eq:profile"}, one has $1/2\leq\kappa_\psi\leq1$.

> **Proof** Cauchy–Schwarz on an interval of length two gives $$1=\left(\int_{-1}^{1}\psi(t)\,dt\right)^2
>  \leq2\int_{-1}^{1}\psi(t)^2\,dt=2\kappa_\psi.$$ The pointwise bounds $0\leq\psi\leq1$ also give $\psi^2\leq\psi$. Integration proves the upper bound.

> **Lemma: exact primitive fixed-$q$ row** <span id="lem:row" label="lem:row">\[lem:row\]</span> For all sufficiently large $x$, every $p\in\mathcal{P}_{\mathrm{top}}$ and $q\in\mathcal{Q}_x$ satisfy $$\sum_{\substack{a\bmod p\\(a,p)=1}}|B_{p,q}^{\psi}(a)|^2
>  =\sum_{0<|m|\leq\lfloor pq/H\rfloor}
>  \left|\psi\!\left(\frac{Hm}{pq}\right)\right|^2.
>  \label{eq:row-identity}$$

> **Proof** Put $M=\lfloor pq/H\rfloor$. Equations [\[eq:separation\]](sections/2_frozen_setup.tex#L17){reference-type="eqref" reference="eq:separation"} imply that $p<q$, hence $q$ is invertible modulo the prime $p$. They also give $$2M\leq\frac{2pq}{H}\leq\frac{4pQ}{H}<p.$$ If two distinct admissible integers $m_1,m_2$ produce the same residue in [\[eq:row\]](sections/2_frozen_setup.tex#L42){reference-type="eqref" reference="eq:row"}, then $p\mid(m_1-m_2)$, while $0<|m_1-m_2|\leq2M<p$, which is impossible. Each occupied residue is nonzero because $0<|m|\leq M<p$. Thus the signed integer atoms map injectively into the primitive residues, and the squared norm has no cross terms. This proves [\[eq:row-identity\]](sections/3_exact_row_riemann.tex#L30){reference-type="eqref" reference="eq:row-identity"}.

The preceding identity is inherited from the fixed-row mechanism of TPC-216. The new step is its asymptotic evaluation for the literal common profile, uniformly across the two prime shells.

> **Lemma: endpoint-safe lattice Riemann estimate** <span id="lem:riemann" label="lem:riemann">\[lem:riemann\]</span> For every fixed admissible $\psi$, uniformly for $p\in\mathcal{P}_{\mathrm{top}}$ and $q\in\mathcal{Q}_x$, $$\sum_{\substack{a\bmod p\\(a,p)=1}}|B_{p,q}^{\psi}(a)|^2
>  =\kappa_\psi\frac{pq}{H}+O_\psi(1).
>  \label{eq:row-asymptotic}$$

> **Proof** Let $f=\psi^2$ and $T=pq/H$. For each integer $m$, the fundamental theorem of calculus gives $$\begin{aligned}
>  \left|f(m/T)-T\int_{m/T}^{(m+1)/T}f(t)\,dt\right|
>  &\leq T\int_{m/T}^{(m+1)/T}|f(m/T)-f(t)|\,dt\\
>  &\leq\int_{m/T}^{(m+1)/T}|f'(s)|\,ds.\end{aligned}$$ Summing in $m$ yields $$\sum_{m\in\mathbb{Z}}f(m/T)=T\int_{\mathbb{R}}f(t)\,dt+O(\|f'\|_1).
>  \label{eq:riemann}$$ Because $f$ is compactly supported in $[-1,1]$ and vanishes at the endpoints, the support restriction in [\[eq:riemann\]](sections/3_exact_row_riemann.tex#L74){reference-type="eqref" reference="eq:riemann"} is exactly $|m|\leq\lfloor T\rfloor$. Omitting $m=0$ subtracts $f(0)$, which is absorbed by $O_\psi(1)$. Lemma [\[lem:row\]](sections/3_exact_row_riemann.tex#L23){reference-type="ref" reference="lem:row"} now proves [\[eq:row-asymptotic\]](sections/3_exact_row_riemann.tex#L59){reference-type="eqref" reference="eq:row-asymptotic"}.
>
> Finally, [\[eq:depth\]](sections/2_frozen_setup.tex#L19){reference-type="eqref" reference="eq:depth"} gives $T\geq UQ/(2H)=\tfrac12x^{23/2400}\to\infty$. The same fixed-profile error therefore applies uniformly over both shells. Its dependence on $\|f'\|_1$ and $f(0)$ explains why the result is not uniform over all profiles.

# Weighted-prime aggregation

Substitute Lemma [\[lem:riemann\]](sections/3_exact_row_riemann.tex#L53){reference-type="ref" reference="lem:riemann"} into [\[eq:direct-energy\]](sections/2_frozen_setup.tex#L51){reference-type="eqref" reference="eq:direct-energy"}. Since $|C_p|^2=(\log p)^2/p^2$, define $$A_U=\sum_{p\in\mathcal{P}_{\mathrm{top}}}\frac{(\log p)^2}{p},\qquad
 E_U=\sum_{p\in\mathcal{P}_{\mathrm{top}}}\frac{(\log p)^2}{p^2},\qquad
 S_Q=\sum_{q\in\mathcal{Q}_x}q,$$ and write $P=|\mathcal{Q}_x|$. Then $$\mathcal{D}_{\mathrm{top}}^{\psi}=\frac{\kappa_\psi}{H}A_US_Q+O_\psi(PE_U).
 \label{eq:aggregate}$$

The accumulated row error is genuinely lower order. On the top shell, $p>U/2$, so $E_U\leq2A_U/U$. Every $q\in\mathcal{Q}_x$ exceeds $Q$, hence $P\leq S_Q/Q$. Relative to the positive main product in [\[eq:aggregate\]](sections/4_weighted_pnt_aggregation.tex#L14){reference-type="eqref" reference="eq:aggregate"}, these inequalities give $$\frac{HPE_U}{A_US_Q}
 \leq\frac{2H}{UQ}
 =O\!\left(x^{-23/2400}\right).
 \label{eq:relative-error}$$ The fixed factor $\kappa_\psi^{-1}\leq2$ can be absorbed into the implied constant.

We next evaluate the two positive weighted sums. Partial summation from the prime number theorem gives `\cite{MontgomeryVaughan2007}` $$\begin{aligned}
 S_Q&=\left(\frac32+o(1)\right)\frac{Q^2}{\log Q},
 \label{eq:q-pnt}\\
 A_U&=(\log2+o(1))\log U.
 \label{eq:p-pnt}\end{aligned}$$ For completeness, the main integral in [\[eq:q-pnt\]](sections/4_weighted_pnt_aggregation.tex#L34){reference-type="eqref" reference="eq:q-pnt"} is $$\int_Q^{2Q}\frac{t}{\log t}\,dt
 =\left(\frac32+o(1)\right)\frac{Q^2}{\log Q}.$$ The main integral in [\[eq:p-pnt\]](sections/4_weighted_pnt_aggregation.tex#L36){reference-type="eqref" reference="eq:p-pnt"} is $$\int_{U/2}^{U}\frac{\log t}{t}\,dt
 =\log2\,\log U-\frac{(\log2)^2}{2}.$$

> **Proof: Proof of Theorem [\[thm:main\]](sections/2_frozen_setup.tex#L57){reference-type="ref" reference="thm:main"}** Lemma [\[lem:kappa\]](sections/3_exact_row_riemann.tex#L8){reference-type="ref" reference="lem:kappa"} proves [\[eq:kappa-range\]](sections/2_frozen_setup.tex#L61){reference-type="eqref" reference="eq:kappa-range"}. Combining [\[eq:aggregate\]](sections/4_weighted_pnt_aggregation.tex#L14){reference-type="eqref" reference="eq:aggregate"}–[\[eq:p-pnt\]](sections/4_weighted_pnt_aggregation.tex#L36){reference-type="eqref" reference="eq:p-pnt"} with [\[eq:relative-error\]](sections/4_weighted_pnt_aggregation.tex#L25){reference-type="eqref" reference="eq:relative-error"} gives $$\mathcal{D}_{\mathrm{top}}^{\psi}=\left(
>  \frac32\,\kappa_\psi\log2\,
>  \frac{\log U}{\log Q}+o_\psi(1)\right)\frac{Q^2}{H}.$$ The frozen scales satisfy $$\frac{\log U}{\log Q}=\frac{133/400}{1/3}=\frac{399}{400}.$$ Thus the rational multiplier is $(3/2)(399/400)=1197/800$. Finally, $$\frac{Q^2}{H}=x^{2/3-21/32}=x^{1/96}.$$ This proves [\[eq:main-asymptotic\]](sections/2_frozen_setup.tex#L69){reference-type="eqref" reference="eq:main-asymptotic"}, with the fixed-profile quantifier stated in Theorem [\[thm:main\]](sections/2_frozen_setup.tex#L57){reference-type="ref" reference="thm:main"}.

Because the leading constant is positive, Theorem [\[thm:main\]](sections/2_frozen_setup.tex#L57){reference-type="ref" reference="thm:main"} immediately rules out $\mathcal{D}_{\mathrm{top}}^{\psi}=o(Q^2/H)$. More strongly, for this exact object no estimate of the form $\mathcal{D}_{\mathrm{top}}^{\psi}\ll_\psi x^{-\delta}Q^2/H$ can hold with fixed $\delta>0$.

# Deterministic certificate and finite stress tests

The release package separates theorem proof from executable reproduction. The producer records the source object, exact rational exponent ledger, theorem status, route firewall, and a finite algebraic row fixture in canonical JSON. The leading rational $1197/800$, the powers $1/96$ and $\pm23/2400$, and the interval $[1/2,1]$ are represented by exact rational pairs before serialization. A SHA-256 digest binds the canonical payload.

The independent checker does not import the producer. It reconstructs the entire certificate and rejects nine mutation classes: status promotion, Boolean/integer confusion, the wrong rational constant, the wrong exponent, a coefficient-sign change, a profile-class change, expansion of the top-prime domain, substitution of a q-collapsed object, and substitution of an inadmissible plateau.

A separate stress program uses two functions of the form $$\psi(t)=\frac{\exp(-1/(1-t^2))w(t)}
 {\int_{-1}^{1}\exp(-1/(1-s^2))w(s)\,ds}
 \mathbf{1}_{|t|<1},$$ with $w(t)=1$ and $w(t)=1+t^2/4$. These are fixed, nonnegative smooth profiles satisfying the literal support condition; numerical quadrature checks their normalization and bound. Across three increasing prime fixtures, the program checks residue injectivity, equality of atom and residue-row energies, and decreasing error in the approximation of $\kappa_\psi$.

All finite values in this section are classified `NUMERICAL_FINITE_ILLUSTRATION_ONLY`. They test implementation and schema integrity but do not support the asymptotic theorem. The proof of Theorem [\[thm:main\]](sections/2_frozen_setup.tex#L57){reference-type="ref" reference="thm:main"} rests on Lemmas [\[lem:row\]](sections/3_exact_row_riemann.tex#L23){reference-type="ref" reference="lem:row"} and [\[lem:riemann\]](sections/3_exact_row_riemann.tex#L53){reference-type="ref" reference="lem:riemann"} and the classical weighted prime number theorem.

# Finite-window consequence and route boundary

The fixed profile is nonnegative. Define the q-collapsed residue row $$B_p^\psi(a)=\sum_{q\in\mathcal{Q}_x}B_{p,q}^\psi(a).$$ Every summand is nonnegative, so pointwise expansion of the square gives $$\sum_{\substack{a\bmod p\\(a,p)=1}}|B_p^\psi(a)|^2
 \geq
 \sum_{q\in\mathcal{Q}_x}
 \sum_{\substack{a\bmod p\\(a,p)=1}}|B_{p,q}^\psi(a)|^2.
 \label{eq:nonnegative-collapse}$$ This inequality sees the direct floor but does not quantify the positive cross-$q$ collision terms.

Let $I$ be an interval of $N$ consecutive integers and put $$z_{p,a}=C_pB_p^\psi(a),\qquad
 K_\psi(n)=\sum_{p\in\mathcal{P}_{\mathrm{top}}}
 \sum_{\substack{a\bmod p\\(a,p)=1}}z_{p,a}\mathrm{e}^{2\pi ina/p}.$$ The primitive fractions $a/p$ are distinct and have height at most $U$. The TPC-238 normalized lower frame `\cite{WangTPC238}`, followed by [\[eq:nonnegative-collapse\]](sections/6_route_boundary.tex#L14){reference-type="eqref" reference="eq:nonnegative-collapse"}, therefore gives

> **Corollary: firewalled finite-window lower bound** <span id="cor:window" label="cor:window">\[cor:window\]</span> For every such interval, $$\frac1N\sum_{n\in I}|K_\psi(n)|^2
>  \geq
>  \left[\frac 12-\frac{\pi^2U^4}{6N^2}\right]_{+}\mathcal{D}_{\mathrm{top}}^{\psi}.
>  \label{eq:window-lower}$$ If $N\asymp x$, the bracket is $1/2-o(1)$ because $U^4/N^2=x^{-67/100+o(1)}$.

Corollary [\[cor:window\]](sections/6_route_boundary.tex#L29){reference-type="ref" reference="cor:window"} remains at scale $x^{1/96+o(1)}$. It neither proves that the q-collision excess contributes another $x^{1/96}$ nor shows that the $x^{1/48}$ upper exponent from the collision-compressed assembly is sharp. That is the next theorem to test.

The claim firewall is otherwise strict. Although $C_p$ is negative before squaring, only $|C_p|^2$ appears here, so no Möbius sign cancellation is available. The paper supplies no signed four-packet projection, no arithmetic $L2$ estimate, no fixed-atom credit, and no strict $1/400$ payment. Full Gate B and the twin-prime endpoint remain open.

# Conclusion

The frozen common profile forces a positive top-prime q-split direct-energy floor. Fixed-$q$ injectivity turns the residue norm into a lattice sum, the literal profile contributes $\kappa_\psi$, and two weighted prime averages produce the exact multiplier $1197\log2/800$. The resulting scale $x^{1/96}$ is unavoidable for every fixed admissible profile.

This closes one proposed source of savings: the direct factor itself cannot be made smaller by a fixed power. The useful next question is correspondingly more specific. One must measure the top-prime q-collapsed collision excess, while retaining the actual profile and original outer q-weight, before claiming sharpness of the $x^{1/48}$ structural upper exponent. Signed $C_h$ cancellation and the four-packet projection remain later gates.

# Status ledger and declarations

| Item                             | Status             | Scope                                          |
|:---------------------------------|:-------------------|:-----------------------------------------------|
| Profile interval                 | `PROVED`           | $1/2\leq\kappa_\psi\leq1$                      |
| Fixed-$q$ row identity           | `PROVED_INHERITED` | Primitive top-prime row                        |
| Row Riemann asymptotic           | `PROVED`           | Fixed profile; $O_\psi(1)$ error               |
| Direct-energy constant           | `PROVED`           | $1197\kappa_\psi\log2/800$                     |
| Direct-energy power              | `PROVED`           | $x^{1/96+o_\psi(1)}$                           |
| Finite calculations              | `NUMERICAL`        | Finite illustration only; not theorem evidence |
| q-collision $x^{1/48}$ sharpness | `OPEN`             | Not inferred from the floor                    |
| Signed $C_h$ cancellation        | `NONE`             | Sign erased by absolute square                 |
| Signed four-packet scalar        | `OPEN`             | No projection in this paper                    |
| Arithmetic $L2$                  | `NONE`             | No arithmetic advance                          |
| Strict $1/400$                   | `UNPAID_GLOBAL`    | Full gate remains open                         |
| Twin-prime conclusion            | `NONE`             | Not claimed                                    |

#### Data and code availability.

The complete deterministic certificate, independent checker, finite stress program, and generated JSON result are included with the project.

#### Ethics, conflicts, and funding.

The work uses no human participants, animals, or personal data. The author declares no conflict of interest and no external funding for this project.

#### Author contributions.

Liang Wang performed the conceptualization, formal analysis, software, validation, and manuscript preparation.

#### Tool-use disclosure.

AI-assisted drafting and deterministic computational tools supported document preparation and executable checks. All mathematical claims were separately source-locked and proof-audited; no numerical output is treated as theorem evidence.

#### Route extraction.

The reusable chain is fixed-$q$ signed-interval injectivity, endpoint-safe lattice Riemann summation, and factorized weighted-prime averaging. The next clue is to test the top-prime q-collapsed collision excess over the exact direct floor before claiming $x^{1/48}$ sharpness.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@unpublished{WangTPC215,
  author = {Liang Wang},
  title = {Short-Quotient {M{\"o}bius} Tails and a No-Power-Loss Majorant for the Physical Cluster Gram},
  note = {TPC-215 project release},
  year = {2026}
}

@unpublished{WangTPC216,
  author = {Liang Wang},
  title = {Direct-Sum Row-Energy Envelope and the Cauchy Bottleneck},
  note = {TPC-216 project release},
  year = {2026}
}

@unpublished{WangTPC237,
  author = {Liang Wang},
  title = {Collision-Compressed Prime-Shell Reassembly on Finite Windows},
  note = {TPC-237 project release},
  year = {2026}
}

@unpublished{WangTPC238,
  author = {Liang Wang},
  title = {A Finite-Window Lower Frame Obstruction for Primitive Rational Frequencies},
  note = {TPC-238 project release},
  year = {2026}
}

@book{MontgomeryVaughan2007,
  author = {Hugh L. Montgomery and Robert C. Vaughan},
  title = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  address = {Cambridge},
  year = {2007}
}
```

<!-- SOURCE_BODY_END -->
