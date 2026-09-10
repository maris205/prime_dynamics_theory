# **Prime-Shell Hilbert Lift and the Sharp Collapse Barrier**

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

The previous structural stage attached a literal common-source twin-prime kernel to a finite interval by a reduced rational-frequency large sieve, but it collapsed the prime shell before the finite-window estimate. We retain the prime label and the four-packet label as Hilbert coordinates. For $H=x^{21/32}$, $Q=x^{1/3}$, and $U=x^{133/400}$, fixed-$q$ cutoff injectivity and an elementary unsigned cluster bound give $$\frac{1}{N}\sum_{n\in I_x}\left\lVert \mathbf K(n)\right\rVert_2^2
 \ll J M^2 x^{1/96}(\log x)^5.$$ Here $\mathbf K$ has coordinates $(j,q)$, $J$ is the fixed packet count, and $M$ is a uniform profile bound. Recombining the prime labels costs exactly the elementary factor $P=\#\mathcal Q_x\leq 2Q$ and recovers the earlier scalar power $x^{11/32}$. A finite aligned fixture attains the full ratio $P=4$, while a parallel four-packet algebraic fixture has unit-projection ratio one. Thus the new theorem preserves the interfaces and isolates the precise prime-shell collapse barrier; it supplies no arithmetic cancellation, $L^2$ advance, fixed-atom credit, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / PRIME_LABEL_AND_PACKET_PRESERVING_LIFT`.\
The Hilbert lift, exponent ledger, and scalar recovery are proved under the declared common-source hypotheses. The finite fixtures are exact structural controls, not asymptotic arithmetic evidence.

# Introduction

A useful analytic route toward the twin-prime problem should expose every place where a collective estimate is required. The recent finite-window attachment did this for a common-source kernel by regrouping divisor rows according to their reduced rational frequencies and applying the additive large sieve. That argument was intentionally unsigned. In particular, it collapsed the prime shell before invoking the finite-window inequality.

The present paper asks a narrower follow-up question: can the outer prime label and the four-packet label be retained in the same finite-window object? This is important for bookkeeping. If the labels are removed too early, a later signed prime-shell or polarized reassembly can be accidentally replaced by a Cauchy estimate without recording its cost. If they are retained, one can measure exactly what the structural argument does and does not provide.

We work with the same V46 common-source scales $$H=x^{21/32},\qquad Q=x^{1/3},\qquad
 Y_0=\frac{H}{4Q},\qquad U=x^{133/400}.$$ The prime shell is $$\mathcal Q_x=\{q\ {\rm prime}: Q<q\leq 2Q\},
 \qquad P=\#\mathcal Q_x,$$ and the squarefree transition band is $$\mathcal D_x=\{d\in\mathbb Z:Y_0<d\leq U,\ \mu(d)^2=1\}.$$ The physical interval is $I_x=(x/2,x]\cap\mathbb Z$, with $N=|I_x|$.

Our main result is a tensorized version of the standard additive large sieve. It preserves $(q,j)$ as coordinates and gives a normalized split exponent $1/96$, since $$\frac{Q^2}{H}=x^{1/96}.$$ Only after this result do we form the scalar packet shell. Pointwise Cauchy over $q$ costs $P\leq 2Q$, changing $Q^2/H$ into $Q^3/H=x^{11/32}$. This identity is the central accounting statement of the paper.

The contributions are:

1.  an exact prime-label- and packet-label-preserving finite-window Hilbert lift;

2.  an explicit split-versus-scalar exponent ledger, with the $P$ cost isolated rather than hidden;

3.  a positive-semidefinite packet Gram formulation compatible with exact four-point complex polarization;

4.  two scoped adversarial controls: a $P$-saturating prime alignment and a geometry-only packet alignment.

#### Status boundary.

Nothing here proves a signed estimate for the literal prime shell. In the terminology of the route ledger, $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_ATOM\_CREDIT=0},\qquad
 \texttt{L2=NONE}.$$ The result is a structural bridge to the next open theorem.

# The split common-source object

Let $\psi_j:\mathbb R\to\mathbb C$ be bounded profiles for $0\leq j<J$, and put $$M=\max_{0\leq j<J}\left\lVert \psi_j\right\rVert_\infty.$$ For $q\in\mathcal Q_x$, $h\leq U$, and $a\pmod h$, define $$B_{h,q}^{(j)}(a)
 =
 \sum_{0<|m|\leq \lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m\overline q\equiv a\pmod h}.
 \label{eq:row}$$ The row is defined on all residues; only primitive residues will be used as reduced-frequency numerators. Set $$c_d=\frac{\mu(d)\log d}{d},\qquad
 C_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}c_d.
 \label{eq:coeff}$$ The split coordinates are $$K_{j,q}(n)=
 \sum_{h\leq U}\ \sum_{\substack{a\bmod h\\(a,h)=1}}
 C_h B_{h,q}^{(j)}(a)\mathrm e(na/h),
 \qquad
 \mathbf K(n)=\bigl(K_{j,q}(n)\bigr)_{\substack{0\leq j<J\\q\in\mathcal Q_x}}.
 \label{eq:split}$$ The scalar packet shell is $$K_j(n)=\sum_{q\in\mathcal Q_x}K_{j,q}(n).
 \label{eq:scalar}$$

The exponent relations needed below are $$\frac{Q^2}{H}=x^{1/96},\quad
 \frac{Q^3}{H}=x^{11/32},\quad
 \frac{U^2}{x}=x^{-67/200},\quad
 \frac{UQ}{H}=x^{23/2400}.
 \label{eq:exponents}$$ For sufficiently large $x$, $4Q<H$ and $U<Q$. In particular every shell prime is a unit modulo every divisor in $\mathcal D_x$.

## The inherited reduced-frequency identity

The divisor-dilation identity from the preceding finite-window stage is $$B_{d,q}^{(j)}(ka)=B_{h,q}^{(j)}(a)
 \qquad (d=kh,\ h\mid d),
 \label{eq:dilation}$$ because the congruence forces $m=kn$ and the cutoff and profile argument scale exactly. Thus the literal common-source kernel can be partitioned by the reduced frequency $a/h$ while retaining $(q,j)$. This is an identity, not an orthogonality assertion.

# The Hilbert-valued finite-window theorem

> **Lemma: fixed-$q$ cutoff injectivity** <span id="lem:inject" label="lem:inject">\[lem:inject\]</span> For sufficiently large $x$, $$\sum_{\substack{a\bmod h\\(a,h)=1}}
>    \left|B_{h,q}^{(j)}(a)\right|^2
>  \leq 2M^2\frac{hq}{H}.$$

> **Proof** If two nonzero atoms $m_1,m_2$ in [\[eq:row\]](main.tex#L142){reference-type="eqref" reference="eq:row"} occupy the same residue, then $h\mid(m_1-m_2)$. Since $q\leq 2Q$ and $4Q<H$, $$|m_1-m_2|
>  \leq 2\left\lfloor\frac{hq}{H}\right\rfloor<h.$$ Thus the atoms are distinct modulo $h$. Summing their squared magnitudes over all residues, and then restricting to primitive residues, gives at most $2\lfloor hq/H\rfloor M^2\leq 2M^2hq/H$.

> **Lemma: active-cluster harmonic bound** <span id="lem:cluster" label="lem:cluster">\[lem:cluster\]</span> The literal coefficients satisfy $$\sum_{h\leq U}h|C_h|^2\ll(\log x)^5.
>  \label{eq:cluster}$$

> **Proof** If the row indexed by $h$ is nonzero for at least one shell prime, then $\lfloor hq/H\rfloor\geq1$, hence $h\geq H/(2Q)$. Writing $d=hk$ in [\[eq:coeff\]](main.tex#L149){reference-type="eqref" reference="eq:coeff"}, we have $k\leq U/h\leq 2UQ/H$. Therefore $$|C_h|
>  \leq \frac{\log U}{h}\sum_{k\leq U/h}\frac1k
>  \ll \frac{(\log x)^2}{h}.$$ The active $h$ form a subinterval of $[H/(2Q),U]$, so $$\sum_hh|C_h|^2
>  \ll(\log x)^4\sum_{H/(2Q)\leq h\leq U}\frac1h
>  \ll(\log x)^5.$$ No cancellation in $\mu$ is used.

> **Lemma: Hilbert-valued additive large sieve** <span id="lem:hilbert" label="lem:hilbert">\[lem:hilbert\]</span> Let $I$ be a consecutive interval of $N$ integers. Then $$\sum_{n\in I}\left\lVert \mathbf K(n)\right\rVert_2^2
>  \leq (N+U^2)
>  \sum_{\substack{h\leq U\\(a,h)=1}}
>  \sum_{q\in\mathcal Q_x}\sum_{0\leq j<J}
>  |C_hB_{h,q}^{(j)}(a)|^2.
>  \label{eq:hilbert}$$

> **Proof** Distinct reduced fractions with denominators at most $U$ have circular spacing at least $U^{-2}$. Apply the standard additive large-sieve inequality `\cite{MontgomeryVaughan1973}` to the scalar expansion of each coordinate $K_{j,q}(n)$, with coefficient $C_hB_{h,q}^{(j)}(a)$, and sum the resulting inequalities over $(q,j)$. This is precisely the coordinate realization of the tensor lift from scalar coefficients to $\ell^2(\mathcal Q_x\times\{0,\ldots,J-1\})$.

> **Theorem: prime-label- and packet-preserving lift** <span id="thm:split" label="thm:split">\[thm:split\]</span> For fixed $J$ and bounded packet profiles, $$\sum_{n\in I_x}\left\lVert \mathbf K(n)\right\rVert_2^2
>  \ll J M^2(N+U^2)\frac{Q^2}{H}(\log x)^5.
>  \label{eq:split-bound}$$ Consequently, $$\frac1N\sum_{n\in I_x}\left\lVert \mathbf K(n)\right\rVert_2^2
>  \ll J M^2x^{1/96}(\log x)^5,
>  \label{eq:split-normalized}$$ and the unnormalized exponent is $97/96+o(1)$.

> **Proof** By Lemma [\[lem:inject\]](main.tex#L193){reference-type="ref" reference="lem:inject"}, $$\begin{aligned}
>  &\sum_{h,a,q,j}|C_hB_{h,q}^{(j)}(a)|^2\\
>  &\quad\leq
>  \frac{2M^2J}{H}\left(\sum_{q\in\mathcal Q_x}q\right)
>  \sum_hh|C_h|^2\\
>  &\quad\ll J M^2\frac{P Q}{H}(\log x)^5
>  \ll J M^2\frac{Q^2}{H}(\log x)^5,
> \end{aligned}$$ where $P\leq2Q$. Insert this into Lemma [\[lem:hilbert\]](main.tex#L242){reference-type="ref" reference="lem:hilbert"}. Since $U^2/N=x^{-67/200+o(1)}$, division by $N$ gives the normalized estimate.

## Scalar recovery and the packet Gram

> **Corollary: exact scalar collapse ledger** <span id="cor:scalar" label="cor:scalar">\[cor:scalar\]</span> For the packet shell [\[eq:scalar\]](main.tex#L163){reference-type="eqref" reference="eq:scalar"}, $$\frac1N\sum_{n\in I_x}\sum_{j<J}|K_j(n)|^2
>  \ll J M^2x^{11/32}(\log x)^5.
>  \label{eq:scalar-bound}$$

> **Proof** For each $j,n$, Cauchy gives $|\sum_qK_{j,q}(n)|^2\leq P\sum_q|K_{j,q}(n)|^2$. Sum over $j,n$ and apply Theorem [\[thm:split\]](main.tex#L265){reference-type="ref" reference="thm:split"}; then use $P\leq2Q$ and $Q^3/H=x^{11/32}$.

For a finite interval define the packet Gram matrix $$G_I[j,\ell]=\sum_{n\in I}K_j(n)\overline{K_\ell(n)}.
\label{eq:gram-definition}$$ It is positive semidefinite, and Corollary [\[cor:scalar\]](main.tex#L300){reference-type="ref" reference="cor:scalar"} is a trace bound. For every unit packet vector $\omega$, $$\sum_{n\in I}\left|\sum_j\overline{\omega_j}K_j(n)\right|^2
 =\omega^*G_I\omega\leq\operatorname{tr}(G_I).
 \label{eq:gram}$$ The exact four-packet polarization interface remains available through $$x\overline y=\frac14\sum_{r=0}^{3}i^r|x+i^ry|^2.
 \label{eq:polarization}$$ The trace inequality is unsigned and therefore does not supply the signed four-packet estimate needed by the terminal route.

# Adversarial controls

## A P-saturating prime-label fixture

Take $$d=5,\qquad H=500,\qquad
 \{q\}=\{101,131,151,181\},\qquad \psi(t)\equiv1.$$ All four primes are $1\pmod5$, and $\lfloor dq/H\rfloor=1$. Hence every fixed-$q$ row is $e_1+e_4$. The coherent row and diagonal energies are $$\left\|\sum_qB_{5,q}\right\|_2^2=32,\qquad
 \sum_q\|B_{5,q}\|_2^2=8,$$ so their ratio is $4=P$. This is an exact rational finite structural adversary. It refutes only the scoped shortcut that fixed-$q$ row geometry would imply a free or sub-$P$ shell collapse.

## A packet-projection alignment

Let $v\neq0$ and let $\omega$ be a unit four-vector. Set $Z^{(j)}=\omega_jv$. Then $$\sum_j\left\lVert Z^{(j)}\right\rVert^2=\left\lVert v\right\rVert^2,\qquad
 \left\|\sum_j\overline{\omega_j}Z^{(j)}\right\|^2=\left\lVert v\right\rVert^2.$$ For $\omega=(1,i,-1,-i)/2$, the projection-to-total ratio is one. This is an algebraic Hilbert-space obstruction: packet geometry alone cannot create cancellation. It is not a claim that every literal TPC profile realizes this parallel family.

|                                   |                                       |
|:----------------------------------|:--------------------------------------|
| Structural lift                   | `PROVED_STANDARD_TENSOR_LIFT`         |
| Split exponent                    | `PROVED_1_OVER_96_LOG_FIVE`           |
| Scalar recovery                   | `PROVED_P_FACTOR_RECOVERS_11_OVER_32` |
| Prime-label orthogonality         | `REFUTED_SCOPED`                      |
| Packet cancellation               | `NONE`                                |
| Arithmetic advance                | `NO`                                  |
| Prime shell / four packets        | `OPEN`                                |
| Full Gate B / strict one-over-400 | `OPEN / UNPAID`                       |

: TPC-218 claim firewall.

# Route position and reproducibility

The result belongs to Route B’s structural threshold-A layer. Route A is not applicable. The strongest positive result is the label-preserving split envelope with exponent $1/96$, together with the exact identification of the single $P$ factor needed for scalar recovery. The strongest obstruction is the finite $P$-saturating row alignment. The open theorem is a signed prime-shell reassembly that beats this cost while retaining the literal four-packet, zero/nonunit, fixed-atom, and normalization interfaces.

The repository release contains a producer, an independent checker, normal and optimized-mode checks, and a separate adversarial script. The finite dilation fixture uses the exact rational surrogate $\mu(d)/d$ solely to check the index map; the asymptotic theorem above uses the literal $\mu(d)\log(d)/d$. No numerical fixture is used as asymptotic evidence.

# Conclusion

TPC-218 turns the instruction “keep the shell” into a precise Hilbert-valued theorem. The split object is controlled at the $Q^2/H=x^{1/96}$ scale, while scalar shell recovery necessarily records a $P\leq2Q$ payment and returns the TPC-217 exponent $11/32$. The finite aligned row and the parallel packet construction show why geometry alone cannot pay the missing arithmetic saving. The next research target is therefore unambiguous: $$\text{prove a signed prime-shell reassembly beyond the exact \(P\) collapse.}$$ This paper makes no claim that the target has been achieved.

#### Acknowledgement of scope.

The claims are limited to the displayed common-source object and its declared finite-window normalization. In particular, `TPC218_ARITHMETIC_ADVANCE=NO`, `TPC218_FIXED_ATOM_CREDIT=0`, and `TPC218_FULL_GATE_B=OPEN`.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{MontgomeryVaughan1973,
  author    = {Hugh L. Montgomery and Robert C. Vaughan},
  title     = {The large sieve},
  publisher = {Mathematika},
  volume    = {20},
  year      = {1973},
  pages     = {119--134}
}

@misc{WangTPC215,
  author       = {Liang Wang},
  title        = {Short-Quotient Mobius Majorant},
  year         = {2026},
  note         = {TPC-215 repository release}
}

@misc{WangTPC216,
  author       = {Liang Wang},
  title        = {Direct-Sum Row-Energy Envelope},
  year         = {2026},
  note         = {TPC-216 repository release}
}

@misc{WangTPC217,
  author       = {Liang Wang},
  title        = {Finite-Window Attachment by Reduced Rational-Frequency Large Sieve},
  year         = {2026},
  note         = {TPC-217 repository release}
}
```

<!-- SOURCE_BODY_END -->
