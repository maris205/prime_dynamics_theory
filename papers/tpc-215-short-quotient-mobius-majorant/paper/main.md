# **Short-Quotient Möbius Tails and a No-Power-Loss\ Majorant for the Physical Cluster Gram**

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

The transition-native twin-prime program contains a squarefree divisor band and, after complete-period frequency clustering, the Möbius-log tails $C_h=\sum_{h\mid d}\mu(d)\log(d)/d.$ This paper estimates those tails on the literal V46 scales. The nonzero integer cutoff in the reciprocal emitter forces every active reduced denominator to satisfy $h\ge H/q_{\max}\ge H/(2Q)=2Y_0$. Thus $h$ itself lies in the full transition band. Writing $d=hk$ gives an exact quotient Möbius sum whose length is at most $2UQ/H=2x^{23/2400+o(1)}$. The $k=1$ term anchors the direct coefficient mass, while an elementary harmonic estimate bounds every cluster coefficient. Together with an exact reduced-denominator decomposition of the emitter row norm, this proves that the complete-period cluster Gram is at most $O((\log x)^2)=x^{o(1)}$ times the divisor direct-sum energy. Hence frequency clustering creates no fixed-power amplification. The comparison is not a saving theorem: every active denominator in $U/2<h\le U$ has cluster-to-direct coefficient ratio exactly one. The direct-sum arithmetic energy, finite-window off-frequency Gram, prime-shell reassembly, arithmetic $L^2$, and twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / SHORT_QUOTIENT_CLUSTER_MAJORANT`.\
The $O((\log x)^2)$ comparison is proved on the source-locked asymptotic scales. Finite decimal ratios are numerical observations only. No arithmetic saving or twin-prime conclusion is claimed.

# Introduction

The V46 transition scalar in the analytic twin-prime route contains one reciprocal emitter for each squarefree divisor $d$ in a short proper-factor range. Its literal coefficient is $$c_d=\frac{\mu(d)\log d}{d}.
 \label{eq:coefficient}$$ TPC-213 showed that these rows are pulled back from one common physical source, so different divisor blocks are not an orthogonal direct sum `\cite{WangTPC213}`. TPC-214 then identified the exact complete-period frequency clusters `\cite{WangTPC214}`. If $h\mid d$, the row at a frequency with reduced denominator $h$ equals the row at $h$ itself. Consequently all multiples of $h$ combine before the Hermitian square, with coefficient $$C_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}c_d.
 \label{eq:cluster-coefficient}$$

The remaining issue is quantitative. A completely arbitrary family of multiples could make the ratio between $|C_h|^2$ and $\sum_{h\mid d}|c_d|^2$ as large as the family size. The literal V46 emitter, however, has an integer activation threshold. A reduced row cannot appear until its denominator is large enough to admit a nonzero reciprocal frequency. That threshold places $h$ back inside the original divisor band and makes the quotient $k=d/h$ very short.

This observation leads to four exact steps:

1.  every active denominator satisfies $h\ge H/q_{\max}\ge2Y_0$;

2.  its cluster coefficient is a quotient Möbius sum with $k\le2x^{23/2400+o(1)}$;

3.  the $k=1$ coefficient anchors a harmonic comparison with the direct coefficient mass;

4.  reduced fractions partition every divisor row, converting the coefficient comparison into a complete-period energy comparison.

The resulting bound is subpower, and in fact $O((\log x)^2)$. This is a real structural advance over leaving the cluster tails unbounded, but it deliberately stops before arithmetic promotion. A top-shell identity also shows why the argument cannot by itself produce a fixed-power saving.

# Literal source lock and the emitter

We use the V46 parameters exactly as frozen in the transition-native Euler artifact `\cite{WangV46}`: $$H=x^{21/32},\qquad Q=x^{1/3},\qquad
 Y_0=\frac{H}{4Q}=x^{31/96+o(1)},\qquad
 U=x^{133/400}.
 \label{eq:scales}$$ Let $$\mathcal Q_x=\{q\text{ prime}:Q<q\le2Q\},
 \qquad q_{\max}=\max\mathcal Q_x,
 \label{eq:prime-shell}$$ and let the full squarefree transition band be $$\mathcal D_x=\{d\in\mathbb Z:Y_0<d\le U,\ \mu(d)^2=1\}.
 \label{eq:divisor-band}$$ For sufficiently large $x$, the source inequalities give $d<U<Q<q$. Thus every $q\in\mathcal Q_x$ is invertible modulo every $d\in\mathcal D_x$.

For an arbitrary profile $\psi$ on the arguments below, define the coefficient-free reciprocal row $$B_d(r)=\sum_{q\in\mathcal Q_x}
 \sum_{0<|m|\le dq/H}
 \psi\!\left(\frac{Hm}{dq}\right)
 \mathbf 1_{m\overline q\equiv r\pmod d},
 \qquad r\in\mathbb Z/d\mathbb Z.
 \label{eq:emitter}$$ The cutoff is interpreted in the integer sense: $|m|\le\lfloor dq/H\rfloor$.

TPC-214 proves the exact dilation covariance $$B_d\!\left(\frac dh a\right)=B_h(a),
 \qquad h\mid d,
 \label{eq:dilation}$$ and the complete-period cluster factorization. We use those two identities as the parent theorem; no continuous cutoff or independent-profile substitution is introduced here.

> **Remark: the full-band hypothesis** The family in [\[eq:divisor-band\]](main.tex#L135){reference-type="eqref" reference="eq:divisor-band"} contains every squarefree integer in the stated interval. This is essential below. For an arbitrary subfamily, an active reduced denominator can divide a selected $d$ without the diagonal member $d=h$ being selected.

# Activation and the short quotient

> **Lemma: activation floor** <span id="lem:activation" label="lem:activation">\[lem:activation\]</span> Suppose $h$ divides a member of $\mathcal D_x$ and $B_h$ is not the zero row. Then $$h\ge\frac{H}{q_{\max}}
>  \ge\frac{H}{2Q}=2Y_0.
>  \label{eq:activation}$$ In particular, $h\in\mathcal D_x$.

> **Proof** If $B_h$ is nonzero, then at least one contributing term in [\[eq:emitter\]](main.tex#L148){reference-type="eqref" reference="eq:emitter"} has a nonzero integer $m$. For the associated $q$, $$1\le |m|\le\frac{hq}{H}\le\frac{hq_{\max}}{H}.$$ This proves the first inequality in [\[eq:activation\]](main.tex#L178){reference-type="eqref" reference="eq:activation"}; the second follows from $q_{\max}\le2Q$ and the definition of $Y_0$. Since $h$ divides a squarefree $d\in\mathcal D_x$, it is squarefree and $h\le d\le U$. Equation [\[eq:activation\]](main.tex#L178){reference-type="eqref" reference="eq:activation"} gives $h>Y_0$, so $h$ belongs to the full band.

> **Lemma: short-quotient normal form** <span id="lem:normal-form" label="lem:normal-form">\[lem:normal-form\]</span> For every active reduced denominator $h$, $$C_h=\frac{\mu(h)}{h}
>  \sum_{\substack{Y_0/h<k\le U/h\\(k,h)=1}}
>  \frac{\mu(k)}{k}\bigl(\log h+\log k\bigr).
>  \label{eq:normal-form}$$ The term $k=1$ occurs, and every nonzero summand satisfies $$k\le\frac{Uq_{\max}}{H}
>  \le\frac{2UQ}{H}
>  =2x^{23/2400+o(1)}.
>  \label{eq:quotient-bound}$$

> **Proof** Write each multiple of $h$ as $d=hk$. Since $d$ is squarefree, $(h,k)=1$ and $\mu(hk)=\mu(h)\mu(k)$. Substitution into [\[eq:cluster-coefficient\]](main.tex#L89){reference-type="eqref" reference="eq:cluster-coefficient"} gives [\[eq:normal-form\]](main.tex#L202){reference-type="eqref" reference="eq:normal-form"}; allowing nonsquarefree $k$ is harmless because their Möbius coefficient is zero. Lemma [\[lem:activation\]](main.tex#L173){reference-type="ref" reference="lem:activation"} shows that $d=h$ belongs to $\mathcal D_x$, so $k=1$ is present. It also gives $$k\le\frac Uh\le\frac{Uq_{\max}}H\le\frac{2UQ}H.$$ Finally, $$\frac{133}{400}+\frac13-\frac{21}{32}
>  =\frac{798+800-1575}{2400}
>  =\frac{23}{2400},$$ which proves the last equality in [\[eq:quotient-bound\]](main.tex#L209){reference-type="eqref" reference="eq:quotient-bound"}.

> **Remark: scale of the reduction** The active divisor itself can be as large as $x^{133/400}$, but after fixing an emitter-visible reduced denominator, all cluster multiples are indexed by a quotient of length only $x^{23/2400+o(1)}$. This is a deterministic support reduction, not Möbius cancellation.

# A deterministic coefficient majorant

For every active $h$, define the direct coefficient mass $$D_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}|c_d|^2.
 \label{eq:direct-mass}$$ Let $\mathsf H_n=\sum_{k=1}^n1/k$ denote the $n$th harmonic number, with $\mathsf H_0=0$.

> **Lemma: anchored harmonic comparison** <span id="lem:harmonic" label="lem:harmonic">\[lem:harmonic\]</span> For every active $h$, $$|C_h|^2\le
>  \left(\frac{\log U}{\log h}\right)^2
>  \mathsf H_{\lfloor U/h\rfloor}^{,2}D_h.
>  \label{eq:row-majorant}$$

> **Proof** The $d=h$ term supplied by Lemma [\[lem:activation\]](main.tex#L173){reference-type="ref" reference="lem:activation"} gives $$D_h\ge |c_h|^2=\left(\frac{\log h}{h}\right)^2.
>  \label{eq:anchor}$$ On the other hand, the triangle inequality and $d=hk\le U$ give $$\begin{aligned}
>  |C_h|
>  &\le \sum_{\substack{k\le U/h\\(k,h)=1}}
>        \frac{|\mu(k)|\log(hk)}{hk} \\
>  &\le \frac{\log U}{h}
>        \sum_{k\le U/h}\frac1k
>  =\frac{\log U}{h}\mathsf H_{\lfloor U/h\rfloor}.
>  \label{eq:triangle}\end{aligned}$$ Squaring [\[eq:triangle\]](main.tex#L274){reference-type="eqref" reference="eq:triangle"} and using [\[eq:anchor\]](main.tex#L264){reference-type="eqref" reference="eq:anchor"} proves [\[eq:row-majorant\]](main.tex#L256){reference-type="eqref" reference="eq:row-majorant"}.

Define the source-locked uniform factor $$A_x=\left(\frac{\log U}{\log(H/q_{\max})}\right)^2
 \mathsf H_{\lfloor Uq_{\max}/H\rfloor}^{\,2}.
 \label{eq:Ax}$$

> **Corollary: subpower coefficient comparison** <span id="cor:subpower" label="cor:subpower">\[cor:subpower\]</span> Uniformly over all active reduced denominators, $$|C_h|^2\le A_xD_h,
>  \qquad A_x=O((\log x)^2)=x^{o(1)}.
>  \label{eq:subpower-coefficient}$$ More explicitly, $$A_x\le
>  \left(\frac{\log U}{\log(H/(2Q))}\right)^2
>  \mathsf H_{\lfloor2UQ/H\rfloor}^{,2}.
>  \label{eq:explicit-Ax}$$

> **Proof** Both factors on the right of [\[eq:row-majorant\]](main.tex#L256){reference-type="eqref" reference="eq:row-majorant"} are nonincreasing as $h$ increases. Apply Lemma [\[lem:activation\]](main.tex#L173){reference-type="ref" reference="lem:activation"} to obtain [\[eq:subpower-coefficient\]](main.tex#L293){reference-type="eqref" reference="eq:subpower-coefficient"}. Since $q_{\max}\le2Q$, enlarging the harmonic index and decreasing the logarithmic denominator gives [\[eq:explicit-Ax\]](main.tex#L300){reference-type="eqref" reference="eq:explicit-Ax"}. The logarithm ratio is bounded on the scales [\[eq:scales\]](main.tex#L124){reference-type="eqref" reference="eq:scales"}, while $$\mathsf H_n\le1+\log n,
>  \qquad n\le2x^{23/2400+o(1)}.$$ Thus $A_x=O((\log x)^2)$, which is $x^{o(1)}$.

# From rows to the complete-period Gram

For $h\ge2$, set $$N_h=\sum_{\substack{a\bmod h\\(a,h)=1}}|B_h(a)|^2.
 \label{eq:primitive-norm}$$ For completeness, let $N_1=|B_1(0)|^2$. In the source range $q<H$, so the additive zero axis vanishes and $N_1=0$ `\cite{WangTPC214}`.

> **Lemma: row-norm divisor decomposition** <span id="lem:row-decomposition" label="lem:row-decomposition">\[lem:row-decomposition\]</span> For every $d\in\mathcal D_x$, $$\sum_{r\bmod d}|B_d(r)|^2=\sum_{h\mid d}N_h.
>  \label{eq:row-decomposition}$$

> **Proof** Each residue $r\bmod d$ determines a unique reduced fraction $$\frac rd=\frac ah,
>  \qquad h\mid d,\quad (a,h)=1,$$ where the zero fraction is represented by $a=0,h=1$. Conversely, each pair on the right represents the residue $r=(d/h)a$. The classes indexed by $h$ therefore partition the complete residue row. Dilation covariance [\[eq:dilation\]](main.tex#L157){reference-type="eqref" reference="eq:dilation"} gives $B_d(r)=B_h(a)$ in each class, proving [\[eq:row-decomposition\]](main.tex#L333){reference-type="eqref" reference="eq:row-decomposition"}.

Let $$L=\operatorname{lcm}\{d:d\in\mathcal D_x\}
 \label{eq:period}$$ for a finite realization of the transition band, and define $$\begin{aligned}
 \mathcal E_{\mathrm{cl}}
 &=\sum_{u\bmod L}\left|
   \sum_{d\in\mathcal D_x}c_d\sum_{r\bmod d}
   B_d(r)\mathrm e^{2\pi iru/d}\right|^2,
 \label{eq:cluster-energy}\\
 \mathcal E_{\mathrm{dir}}
 &=L\sum_{d\in\mathcal D_x}|c_d|^2
   \sum_{r\bmod d}|B_d(r)|^2.
 \label{eq:direct-energy}\end{aligned}$$

> **Theorem: no-power-loss cluster majorant** <span id="thm:main" label="thm:main">\[thm:main\]</span> On the literal V46 squarefree transition band, $$\boxed{\mathcal E_{\mathrm{cl}}\le A_x\mathcal E_{\mathrm{dir}}},
>  \qquad A_x=O((\log x)^2)=x^{o(1)},
>  \label{eq:main}$$ where $A_x$ is given explicitly by [\[eq:Ax\]](main.tex#L284){reference-type="eqref" reference="eq:Ax"} and [\[eq:explicit-Ax\]](main.tex#L300){reference-type="eqref" reference="eq:explicit-Ax"}.

> **Proof** The TPC-214 complete-period factorization gives $$\frac{\mathcal E_{\mathrm{cl}}}{L}=\sum_hN_h|C_h|^2.
>  \label{eq:tpc214-factor}$$ Corollary [\[cor:subpower\]](main.tex#L288){reference-type="ref" reference="cor:subpower"} and a finite rearrangement of nonnegative terms give $$\begin{aligned}
>  \frac{\mathcal E_{\mathrm{cl}}}{L}
>  &\le A_x\sum_hN_hD_h \\
>  &=A_x\sum_{d\in\mathcal D_x}|c_d|^2\sum_{h\mid d}N_h \\
>  &=A_x\sum_{d\in\mathcal D_x}|c_d|^2
>        \sum_{r\bmod d}|B_d(r)|^2
>  =A_x\frac{\mathcal E_{\mathrm{dir}}}{L},\end{aligned}$$ where the penultimate equality is Lemma [\[lem:row-decomposition\]](main.tex#L329){reference-type="ref" reference="lem:row-decomposition"}. Multiplication by $L$ proves [\[eq:main\]](main.tex#L374){reference-type="eqref" reference="eq:main"}.

> **Remark: what the theorem does and does not remove** The theorem proves that the complete-period shared-frequency Gram has no additional fixed-power cost beyond the divisor direct sum. It does not bound $\mathcal E_{\mathrm{dir}}$ at the natural arithmetic scale. It also does not replace the finite physical interval by a complete period: off-frequency terms that vanish in [\[eq:tpc214-factor\]](main.tex#L384){reference-type="eqref" reference="eq:tpc214-factor"} must be revisited in the actual window.

# A sharp top-shell obstruction

> **Proposition: exact ratio one in the top shell** <span id="prop:top-shell" label="prop:top-shell">\[prop:top-shell\]</span> If an active reduced denominator satisfies $U/2<h\le U$, then $$C_h=c_h,\qquad D_h=|c_h|^2,
>  \qquad \frac{|C_h|^2}{D_h}=1.
>  \label{eq:top-shell}$$

> **Proof** Lemma [\[lem:activation\]](main.tex#L173){reference-type="ref" reference="lem:activation"} places $h$ itself in $\mathcal D_x$. Any distinct positive multiple of $h$ is at least $2h>U$, so no other member of the band is divisible by $h$. The definitions [\[eq:cluster-coefficient\]](main.tex#L89){reference-type="eqref" reference="eq:cluster-coefficient"} and [\[eq:direct-mass\]](main.tex#L244){reference-type="eqref" reference="eq:direct-mass"} reduce to the single term $d=h$.

Proposition [\[prop:top-shell\]](main.tex#L411){reference-type="ref" reference="prop:top-shell"} is a sharp scoped obstruction. It refutes a uniform rowwise estimate of the form $$|C_h|^2\le x^{-\delta}D_h
 \qquad(\delta>0)
 \label{eq:forbidden-saving}$$ based only on cluster coefficients. It does not refute a global saving that uses the size or distribution of $N_h$, finite-window oscillation, prime-shell averaging, or the signed four-packet scalar. Those inputs are absent from the coefficient identity [\[eq:top-shell\]](main.tex#L416){reference-type="eqref" reference="eq:top-shell"}.

# Finite exact certificate

The release fixture retains the TPC-214 rational profile but enlarges the divisor family to a full finite band: $$\mathcal Q=\{11,13,17\},\quad H=40,\quad Y_0=2,\quad U=35,
 \quad \psi(t)=\frac1{(1+t^2)^2}.
 \label{eq:fixture}$$ The finite band consists of all squarefree $2<d\le35$ coprime to the three fixture primes. This coprimality, rather than the asymptotic inequality $U<Q$, makes every finite inverse legal. All emitter entries and row-norm identities are exact rational numbers.

The activation floor is $\lceil40/17\rceil=3$, and the active denominators are $$3,5,6,7,10,14,15,19,21,23,29,30,31,35.
 \label{eq:active-fixture}$$ The largest realized quotient is $10$, below the uniform integer bound $\lfloor35\cdot17/40\rfloor=14$. Selected coefficient ratios are shown in Table [1](main.tex#L486){reference-type="ref" reference="tab:fixture"}. They use real logarithms and are therefore labeled `NUMERICAL_OBSERVATION`; the top-shell membership and ratio-one statements are exact.

<div id="tab:fixture">

|  $h$| band multiples  | quotients    |  $|C_h|^2/D_h$|  harmonic majorant|
|----:|:----------------|:-------------|--------------:|------------------:|
|    3| $3,6,15,21,30$  | $1,2,5,7,10$ |    $0.0721263$|          $95.5111$|
|    5| $5,10,15,30,35$ | $1,2,3,6,7$  |    $0.0279988$|          $32.8075$|
|    6| $6,30$          | $1,5$        |    $0.3363555$|          $20.5278$|
|    7| $7,14,21,35$    | $1,2,3,5$    |    $0.1711627$|          $17.4043$|
|   15| $15,30$         | $1,2$        |    $0.0992569$|           $3.8782$|
|   19| $19$            | $1$          |            $1$|           $1.4580$|
|   35| $35$            | $1$          |            $1$|                $1$|

: Finite coefficient diagnostics. The majorant is deliberately cancellation-free. Rows $h=19,21,23,29,30,31,35$ lie in the top shell and have exact ratio one.

</div>

Exact dilation covariance and the row decomposition are checked for every divisor and every reduced residue. With the exact rational row norms followed by real-logarithm evaluation, the whole finite cluster and direct energies are $$\mathcal E_{\mathrm{cl}}/L\approx5.5554404644,qquad
 \mathcal E_{\mathrm{dir}}/L\approx9.3063240426,qquad
 \mathcal E_{\mathrm{cl}}/\mathcal E_{\mathrm{dir}}\approx0.5969532588.
 \label{eq:finite-ratio}$$ Equation [\[eq:finite-ratio\]](main.tex#L496){reference-type="eqref" reference="eq:finite-ratio"} is a reproduction diagnostic, not evidence for asymptotic cancellation. An independent implementation reconstructs the rows, formal log polynomials, harmonic factors, and top-shell list without importing the producer. Normal and optimized interpreter modes are required to give byte-identical output. A separate adversarial checker covers 53 active rows across three finite configurations and verifies that deleting the $d=h$ member invalidates the diagonal-anchor hypothesis.

# Route evaluation and open arithmetic

The main theorem changes the structural state in one precise way: $$\text{complete-period cluster energy}
 \ \le\ x^{o(1)}\times
 \text{divisor direct-sum row energy}.
 \label{eq:route-change}$$ Thus a future proof no longer needs to budget a fixed power for coherent reduced-frequency collisions. The next arithmetic object is the right-hand side of [\[eq:route-change\]](main.tex#L513){reference-type="eqref" reference="eq:route-change"}, not the unestimated coefficient tail.

Three independent gaps remain:

1.  **Direct-sum arithmetic energy.** The current argument gives no natural-scale estimate for the physical residual rows weighted by $|c_d|^2$.

2.  **Finite physical interval.** Complete-period orthogonality removes unequal rational frequencies. The actual interval produces an off-frequency Gram that needs its own bound.

3.  **Prime-shell and four-packet reassembly.** The prime-only shell, block localization, exact diagonal subtraction, and signed polarization must be retained in one theorem with the strict $1/400$ loss ledger.

Accordingly, the formal Route-B status is $$\begin{array}{ll}
\texttt{STRUCTURAL\_THRESHOLD\_A} &= \texttt{PASS},\\
\texttt{CLUSTER\_TO\_DIRECT\_MAJORANT} &=
  \texttt{PROVED\_O\_LOG\_X\_SQUARED},\\
\texttt{UNIFORM\_ROWWISE\_POWER\_SAVING} &=
  \texttt{REFUTED\_SCOPED},\\
\texttt{ARITHMETIC\_ADVANCE} &= \texttt{NO},\\
\texttt{L2} &= \texttt{NONE},\\
\texttt{FULL\_GATE\_B\_STRICT\_1\_OVER\_400} &= \texttt{UNPAID}.
\end{array}$$ Route A is not applicable to this analytic twin-prime session. No fixed-atom credit or twin-prime conclusion follows from a complete-period comparison.

# Conclusion

The literal reciprocal cutoff turns every emitter-visible Möbius cluster into a short quotient sum. Because activation places the reduced denominator itself back in the full divisor band, the diagonal term anchors a deterministic harmonic comparison. Reduced-fraction row decomposition then upgrades this coefficient estimate to an $O((\log x)^2)$ complete-period Gram majorant.

This closes the fixed-power amplification question at the cluster stage. The top shell simultaneously proves that no uniform rowwise saving can come from cluster algebra alone. The next useful step is therefore to estimate the physical direct-sum row energy before reintroducing finite-window cross frequencies and the prime-shell four-packet assembly.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{WangV46,
  author       = {Liang Wang},
  title        = {Bridge A / Gates A--B V46: Transition-Native Euler Carrier and the AP--BDH Residual Gate},
  year         = {2026},
  note         = {Internal research artifact, prime\_dynamics\_theory repository}
}

@misc{WangTPC213,
  author       = {Liang Wang},
  title        = {Physical Profile Pullback and the Cross-Divisor Gram},
  year         = {2026},
  note         = {TPC-213 project, prime\_dynamics\_theory repository}
}

@misc{WangTPC214,
  author       = {Liang Wang},
  title        = {M{\"o}bius-Weighted Shared-Frequency Clusters in the Physical Cross-Divisor Gram},
  year         = {2026},
  note         = {TPC-214 project, prime\_dynamics\_theory repository}
}
```

<!-- SOURCE_BODY_END -->
