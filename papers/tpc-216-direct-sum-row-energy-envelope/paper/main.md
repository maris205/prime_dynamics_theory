# **Direct-Sum Row-Energy Envelope and the Cauchy Bottleneck**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The transition-native twin-prime program contains a complete-period direct-sum row energy which remains after TPC-215 controls reduced-frequency clustering. This paper gives a deterministic bound for that quantity on the literal V46 scales. Writing the emitter as a sum over primes, the condition $4Q<H$ makes the integer cutoff injective modulo each divisor for every fixed prime. The fixed-prime row norm is therefore exact, and one Cauchy inequality across the prime shell yields $$L^{-1}\mathcal E_{\mathrm{dir}}\ll_{\psi} (Q^3/H)(\log U)^3
 = x^{11/32+o(1)}.$$ No prime-number theorem and no Mobius cancellation are used. An exact rational fixture with all prime rows supported on the same two residues shows that the shell Cauchy factor cannot be replaced by free orthogonality. The result is a complete-period structural envelope only: the finite physical-window Gram, prime-shell reassembly, arithmetic $L^2$, and the twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / DIRECT_SUM_ROW_ENERGY_ENVELOPE`.\
The exponent $11/32$ is an unconditional source-locked envelope. The finite fixture is exact rational structural QA. No arithmetic saving is claimed.

# Introduction

The V46 transition scalar uses the literal coefficient $$c_d=\frac{\mu(d)\log d}{d}
 \label{eq:coefficient}$$ on a squarefree divisor band. Its reciprocal emitter is coupled across divisors through common rational frequencies. TPC-213 identified this common physical source, and TPC-214 reduced the complete-period Gram to reduced-denominator clusters `\cite{WangTPC214}`. TPC-215 then proved that the cluster Gram is at most an $O((\log x)^2)$ multiple of the divisor direct-sum energy `\cite{WangTPC215}`.

The next question is a narrower one: how large can that direct-sum row energy be before finite-window cross frequencies are restored? The answer here is a source-locked envelope, not a cancellation theorem. The fixed-prime integer cutoff has a useful exact feature. Since the shell is contained in $(Q,2Q]$ and $4Q<H$ for large $x$, distinct admissible integers cannot occupy the same residue modulo a fixed divisor. This removes cross terms within one prime row. Cauchy is used only once, across the prime shell, and the resulting divisor sum is elementary.

There is also a sharp warning. The prime rows need not be orthogonal to one another. A finite exact fixture with primes congruent to one modulo five makes all rows occupy the same two residues. Thus the shell Cauchy step is a genuine bottleneck of this structural proof.

# Literal source lock

We retain the V46 scales exactly as frozen in the transition compiler `\cite{WangV46}`: $$H=x^{21/32},\qquad Q=x^{1/3},\qquad
 Y_0=\frac{H}{4Q},\qquad U=x^{133/400}.
 \label{eq:scales}$$ Let $$\mathcal Q_x=\{q\text{ prime}:Q<q\le 2Q\},\qquad P=|\mathcal Q_x|,
 \label{eq:shell}$$ and $$\mathcal D_x=\{d\in\mathbb Z:Y_0<d\le U,\ \mu(d)^2=1\}.
 \label{eq:band}$$ For sufficiently large $x$, the source inequalities give $U<Q$, so every shell prime is invertible modulo every $d\in\mathcal D_x$. For a bounded profile $\psi$, set $$B_d(r)=\sum_{q\in\mathcal Q_x}\sum_{0<|m|\le\lfloor dq/H\rfloor}
 \psi\!\left(\frac{Hm}{dq}\right)
 \mathbf 1_{m\overline q\equiv r\pmod d}.
 \label{eq:emitter}$$ Write $M_\psi=\sup_t|\psi(t)|$ and let $\left\lVert v\right\rVert_{2,d}^2=\sum_{r\bmod d}|v(r)|^2$.

The exact exponent ledger is $$\frac{H}{4Q}=\frac14x^{31/96}\longrightarrow\infty,
 \qquad \frac{U}{Q}=x^{-1/1200}\longrightarrow0.
 \label{eq:source-inequalities}$$ Consequently, the proof below works in the asymptotic source range where $4Q<H$. The factor four is important: the shell extends to $2Q$, and fixed-prime injectivity requires $2q<H$, not merely $2Q<H$.

# Fixed-prime injectivity

For one prime define $$B_{d,q}(r)=\sum_{0<|m|\le n_{d,q}}
 \psi\!\left(\frac{Hm}{dq}\right)
 \mathbf 1_{m\overline q\equiv r\pmod d},
 \qquad n_{d,q}=\left\lfloor\frac{dq}{H}\right\rfloor.
 \label{eq:fixed-row}$$

> **Theorem: fixed-q no-collision** <span id="thm:no-collision" label="thm:no-collision">\[thm:no-collision\]</span> For $d\in\mathcal D_x$ and $q\in\mathcal Q_x$, distinct admissible integers $m$ in [\[eq:fixed-row\]](main.tex#L142){reference-type="eqref" reference="eq:fixed-row"} give distinct residues modulo $d$. Hence $$\left\lVert B_{d,q}\right\rVert_{2,d}^2
>  =\sum_{0<|m|\le n_{d,q}}
>  \left|\psi\!\left(\frac{Hm}{dq}\right)\right|^2
>  \le 2M_\psi^2\frac{dq}{H}.
>  \label{eq:fixed-energy}$$

> **Proof** Suppose $m_1\ne m_2$ collide. Since $q$ is a unit modulo $d$, $d\mid(m_1-m_2)$. On the other hand, $q\le2Q$ and [\[eq:source-inequalities\]](main.tex#L128){reference-type="eqref" reference="eq:source-inequalities"} give $$0<|m_1-m_2|\le2\left\lfloor\frac{dq}{H}\right\rfloor
>  \le\frac{2dq}{H}<d.$$ This is impossible. Thus the atom supports are distinct, so the squared norm is the sum of squared atom weights. There are at most $2\lfloor dq/H\rfloor\le2dq/H$ atoms, proving [\[eq:fixed-energy\]](main.tex#L154){reference-type="eqref" reference="eq:fixed-energy"}.

# The direct-sum envelope

> **Theorem: direct-sum row-energy envelope** <span id="thm:envelope" label="thm:envelope">\[thm:envelope\]</span> Let $$\mathcal E_{\mathrm{dir}}=L\sum_{d\in\mathcal D_x}|c_d|^2\left\lVert B_d\right\rVert_{2,d}^2,
>  \label{eq:direct-energy}$$ where $L$ is a complete common period. Then $$\frac{\mathcal E_{\mathrm{dir}}}{L}
>  \le 16M_\psi^2\frac{Q^3}{H}
>  \sum_{Y_0<d\le U}\frac{\mu(d)^2(\log d)^2}{d}
>  \ll_{\psi}\frac{Q^3}{H}(\log U)^3.
>  \label{eq:envelope}$$ In particular, $$\frac{\mathcal E_{\mathrm{dir}}}{L}\ll_{\psi}x^{11/32}(\log x)^3,
>  \label{eq:exponent}$$ The right-hand scale is $x^{11/32+o(1)}$, but no matching lower bound is claimed.

> **Proof** Since $B_d=\sum_{q\in\mathcal Q_x}B_{d,q}$, Cauchy in the $P$ shell coordinates and Theorem [\[thm:no-collision\]](main.tex#L146){reference-type="ref" reference="thm:no-collision"} give $$\begin{aligned}
>  \left\lVert B_d\right\rVert_{2,d}^2
>  &\le P\sum_{q\in\mathcal Q_x}\left\lVert B_{d,q}\right\rVert_{2,d}^2 \\
>  &\le \frac{2M_\psi^2Pd}{H}\sum_{q\in\mathcal Q_x}q
>  \le \frac{4M_\psi^2P^2dQ}{H}.
>  \label{eq:shell-cauchy}\end{aligned}$$ The interval $(Q,2Q]$ contains at most $2Q$ integers for $Q\ge1$, so $P\le2Q$. Therefore $$\left\lVert B_d\right\rVert_{2,d}^2\le16M_\psi^2\frac{dQ^3}{H}.$$ Using $|c_d|^2=\mu(d)^2(\log d)^2/d^2$ in [\[eq:direct-energy\]](main.tex#L178){reference-type="eqref" reference="eq:direct-energy"} proves the first inequality in [\[eq:envelope\]](main.tex#L186){reference-type="eqref" reference="eq:envelope"}. Finally, comparison with the integral of $(\log t)^2/t$ gives $$\sum_{1\le d\le U}\frac{(\log d)^2}{d}\ll(\log(2U))^3.$$ Since $Q^3/H=x^{1-21/32}=x^{11/32}$ and $\log(2U)=O(\log x)$, the result follows.

> **Remark: claim boundary** The proof uses absolute values in both the fixed-row bound and shell Cauchy. It does not use the signs of $\mu(d)$, any prime cancellation, or the four-packet signed reassembly. Also, $\mathcal E_{\mathrm{dir}}$ is a complete-period quantity. The finite physical interval has an off-frequency Gram that is not controlled by Theorem [\[thm:envelope\]](main.tex#L174){reference-type="ref" reference="thm:envelope"}.

# Exact aligned-shell adversary

The shell Cauchy step cannot be replaced by a direct orthogonal sum. Consider the finite rational fixture $$d=5,\qquad H=500,\qquad Q_{\mathrm{scale}}=100,
 \qquad \{q\} = \{101,131,151,181\},
 \qquad \psi(t)=\frac{1}{(1+t^2)^2}.
 \label{eq:adversary}$$ Each displayed $q$ is prime and congruent to one modulo five. Moreover, $\lfloor5q/500\rfloor=1$, so the only nonzero integers are $m=\pm1$. Since $q^{-1}=1\pmod5$, every fixed-q row has support exactly $\{1,4\}$. The exact rational certificate in the accompanying repository records the individual rows, the combined row, and all norms without floating point arithmetic.

For orientation, the exact values have decimal displays

| quantity                    |    decimal display|
|:----------------------------|------------------:|
| sum of individual row norms |  1.604830605122346|
| combined row norm           |  5.946998427183525|
| combined/direct ratio       |  3.705686075652919|

The decimal values are only presentations of exact rationals. The ratio is strictly larger than one, so positive cross terms occur. The fixture is a finite structural adversary, not a model for an asymptotic prime shell.

> **Proposition: aligned-shell obstruction** <span id="prop:adversary" label="prop:adversary">\[prop:adversary\]</span> No proof that uses only the individual fixed-q row norms may replace $\left\lVert \sum_qB_{d,q}\right\rVert_2^2$ by $\sum_q\left\lVert B_{d,q}\right\rVert_2^2$ for the literal row family. In particular, free shell orthogonality is refuted in this scoped structural sense.

> **Proof** The fixture [\[eq:adversary\]](main.tex#L238){reference-type="eqref" reference="eq:adversary"} has common support and an exact combined norm strictly larger than the individual norm sum. Therefore the proposed orthogonal replacement fails on an admissible finite reciprocal-emitter configuration. The statement is scoped to the replacement rule; it does not assert an asymptotic lower bound for the V46 object.

# Route evaluation and open gates

Theorem [\[thm:envelope\]](main.tex#L174){reference-type="ref" reference="thm:envelope"} is the next quantitative envelope after TPC-215: $$\text{complete-period direct row energy}
 \le x^{11/32+o(1)}.
 \label{eq:route-advance}$$ It removes the need to leave this direct-sum object completely unbounded, but it does not provide a saving relative to a required target scale. The exact remaining gates are:

1.  attach the normalized complete-period envelope to the literal finite physical window and its off-frequency Gram;

2.  preserve the Mobius signs, prime-only shell, block tails, and four-packet reassembly in one theorem;

3.  pay the arithmetic $L^2$, fixed-atom, and strict $1/400$ ledgers.

Route A is not applicable to this analytic twin-prime session. The current Route-B structural threshold passes, while arithmetic advance is `NO`, $L^2=\texttt{NONE}$, fixed-atom credit is zero, and full Gate B is open.

# Conclusion

The source inequality $4Q<H$ turns each fixed-prime reciprocal emitter row into an exact sum of distinct integer atoms. Shell Cauchy and the elementary Mobius-log divisor sum then give the complete-period envelope $L^{-1}\mathcal E_{\mathrm{dir}}\ll_\psi x^{11/32}(\log x)^3$. The aligned rational fixture shows why the shell Cauchy factor is a real bottleneck rather than a notation artifact. The next research step is a finite-window attachment that keeps this alignment issue and the literal signed reassembly visible.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{WangV46,
  author       = {Liang Wang},
  title        = {Bridge A / Gates A--B V46: Transition-Native Euler Carrier and the AP--BDH Residual Gate},
  year         = {2026},
  note         = {Internal research artifact, prime\_dynamics\_theory repository}
}

@misc{WangTPC215,
  author       = {Liang Wang},
  title        = {Short-Quotient Mobius Tails and a No-Power-Loss Majorant for the Physical Cluster Gram},
  year         = {2026},
  note         = {TPC-215 project, prime\_dynamics\_theory repository}
}

@misc{WangTPC214,
  author       = {Liang Wang},
  title        = {Mobius-Weighted Shared-Frequency Clusters in the Physical Cross-Divisor Gram},
  year         = {2026},
  note         = {TPC-214 project, prime\_dynamics\_theory repository}
}
```

<!-- SOURCE_BODY_END -->
