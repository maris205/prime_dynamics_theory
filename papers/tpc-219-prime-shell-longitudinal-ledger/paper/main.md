# Prime-Shell Longitudinal Ledger and the Exact $P$ Collapse

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

TPC-218 retained the prime label in a Hilbert-valued finite-window estimate, but scalar recovery was recorded only as a factor $P=\#\mathcal Q_x$. This paper identifies the factor exactly. For the packet vector $Z_q(n)=(K_{j,q}(n))_j$, we decompose each prime-labelled family into its constant longitudinal mode and its mean-zero transverse remainder. The resulting identity is $$E_{\mathrm{shell}}=P(E_{\mathrm{diag}}-E_{\perp}),$$ where $E_{\perp}$ is the integrated transverse energy. Consequently, an improvement $E_{\mathrm{shell}}\leq\eta PE_{\mathrm{diag}}$ is equivalent to the lower bound $E_{\perp}\geq(1-\eta)E_{\mathrm{diag}}$. Exact rational fixtures attain both the aligned and balanced endpoints. The result is structural: it supplies no prime or Möbius cancellation and no twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / EXACT_LONGITUDINAL_TRANSVERSE_LEDGER`. The theorem is an exact Hilbert identity; the finite fixtures are controls, not asymptotic evidence.

# Why the $P$ factor must be opened

The previous finite-window stages control a common-source kernel after its rational frequencies have been grouped. TPC-218 kept $(q,j)$ as coordinates and proved a split bound at the scale $Q^2/H=x^{1/96}$, but the packet shell $K_j=\sum_{q\in\mathcal Q_x}K_{j,q}$ was recovered by pointwise Cauchy. That estimate is safe, but it hides the precise object on which a future signed argument must operate. The inherited finite-window estimate uses the standard additive large-sieve interface `\cite{montgomeryvaughan1973}`; the present paper audits what happens after its q labels are recombined.

The present paper asks a narrower question: for an arbitrary family of packet vectors, what is the exact difference between the q-diagonal energy and the scalar shell energy? This question is deliberately independent of any conjectural prime distribution. It is an algebraic audit of the interface that a prime-shell theorem would have to cross.

# The labelled packet object

Let $\mathcal Q_x$ be a nonempty finite set of primes and put $P=\#\mathcal Q_x$. Let $V=\mathbb C^J$ with its standard Hermitian norm. In the TPC-218 application, $$Z_q(n)=\bigl(K_{j,q}(n)\bigr)_{0\leq j<J}\in V,
 \qquad K_j(n)=\sum_{q\in\mathcal Q_x}K_{j,q}(n).$$ Nothing in the next theorem uses the formula for $K_{j,q}$; it only uses that all terms belong to one common Hilbert space and share the same interval.

For a finite interval $I$ define $$\overline Z(n)=\frac1P\sum_{q\in\mathcal Q_x}Z_q(n),\qquad
 R_q(n)=Z_q(n)-\overline Z(n),$$ and $$\begin{aligned}
 E_{\mathrm{shell}}&=\sum_{n\in I}\left\|\sum_{q\in\mathcal Q_x}Z_q(n)\right\|_2^2,\\
 E_{\mathrm{diag}}&=\sum_{n\in I}\sum_{q\in\mathcal Q_x}\|Z_q(n)\|_2^2,\\
 E_{\perp}&=\sum_{n\in I}\sum_{q\in\mathcal Q_x}\|R_q(n)\|_2^2.\end{aligned}$$

The names longitudinal and transverse refer only to the decomposition of the direct sum $V^P$ into the constant q-direction and its orthogonal complement. They do not assume that the primes behave randomly.

# Exact longitudinal/transverse theorem

> **Theorem: Exact $P$-collapse ledger** For every family $(Z_q(n))$ as above, $$E_{\mathrm{shell}}=P(E_{\mathrm{diag}}-E_{\perp}),\qquad
>  0\leq E_{\perp}\leq E_{\mathrm{diag}},$$ and hence $0\leq E_{\mathrm{shell}}\leq PE_{\mathrm{diag}}$. For $0\leq\eta\leq1$, $$E_{\mathrm{shell}}\leq\eta PE_{\mathrm{diag}}
>  \quad\Longleftrightarrow\quad
>  E_{\perp}\geq(1-\eta)E_{\mathrm{diag}}.$$

> **Proof** For each $n$, the residuals satisfy $\sum_qR_q(n)=0$. Expanding the squared norms, the cross term with $\overline Z(n)$ therefore vanishes: $$\sum_q\|Z_q(n)\|_2^2
>  =P\|\overline Z(n)\|_2^2+\sum_q\|R_q(n)\|_2^2. \tag{1}$$ On the other hand, $\sum_qZ_q(n)=P\overline Z(n)$, so $$\left\|\sum_qZ_q(n)\right\|_2^2=P^2\|\overline Z(n)\|_2^2.$$ Eliminating the mean term with (1) gives the pointwise identity $$\left\|\sum_qZ_q(n)\right\|_2^2
>  =P\sum_q\|Z_q(n)\|_2^2-P\sum_q\|R_q(n)\|_2^2. \tag{2}$$ Summing (2) over $n\in I$ proves the first equality. Equation (1) and nonnegativity give $0\leq E_{\perp}\leq E_{\mathrm{diag}}$. Finally, rearranging the first equality proves the last equivalence; every operation divides only by the positive integer $P$.

> **Corollary: What a genuine shell saving must prove** If a future argument claims a factor $\eta<1$ relative to the TPC-218 Cauchy envelope, then it must prove a lower bound on the literal q-transverse energy of the form $E_{\perp}\geq(1-\eta)E_{\mathrm{diag}}$ on the same interval and with the same source object. An upper bound for $E_{\mathrm{diag}}$ alone cannot imply this claim.

# Sharp finite endpoints

The theorem has no slack at the level of abstract geometry. If $Z_q=v$ for every $q$, then $R_q=0$, so $E_{\perp}=0$ and $E_{\mathrm{shell}}=PE_{\mathrm{diag}}$. At the other endpoint, if $\sum_qZ_q=0$, then $\overline Z=0$, $E_{\perp}=E_{\mathrm{diag}}$, and $E_{\mathrm{shell}}=0$.

Table [1](main.tex#L159){reference-type="ref" reference="tab:firewall"} records the exact finite certificate. The vectors are rational, so no floating-point decision is used. The aligned row is the same structural pattern as the TPC-218 $d=5$ fixture, but the present theorem explains it as a zero-transverse endpoint rather than merely a large ratio.

<div id="tab:firewall">

| fixture    | $E_{\mathrm{diag}}$ / $E_{\perp}$ | $E_{\mathrm{shell}}$    |
|:-----------|:----------------------------------|:------------------------|
| aligned    | $20/0$                            | $80=PE_{\mathrm{diag}}$ |
| balanced   | $4/4$                             | $0$                     |
| orthogonal | $4/4$                             | $0$                     |
| mixed      | $10/8$                            | $8$                     |

: Exact rational endpoint and interior checks with $P=4$.

</div>

The aligned fixture refutes a geometry-only hope for a sub-$P$ estimate. The statement is scoped: it does not say that the literal growing prime shell is aligned. It says that such alignment cannot be excluded by the Hilbert envelope or by the label space alone.

# Route position and reproducibility

Route A is not applicable. Route B structural threshold A passes because the theorem acts on the exact labelled interface inherited from TPC-218. The maximum claim is `PROVED_STRUCTURAL_L1`. In particular, $$\texttt{ARITHMETIC\_ADVANCE}=\texttt{NO},\quad
 \texttt{FIXED\_ATOM\_CREDIT}=0,\quad
 \texttt{L2}=\texttt{NONE},$$ and the strict $1/400$ payment remains unpaid.

The producer, an independent checker, an optimized-mode replay, and a separate endpoint adversary are included in the project directory. The next natural edge is no longer ambiguous: rewrite $E_{\perp}$ using the congruence collisions of the literal prime rows. That is the TPC-220 question.

# Conclusion

TPC-219 converts the scalar $P$ collapse from an opaque Cauchy cost into an exact longitudinal/transverse ledger. Any successful signed prime-shell reassembly must create transverse energy in the literal q family; the aligned endpoint shows why this cannot be obtained from abstract packet geometry. The result is a structural bridge, not an arithmetic saving.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@article{montgomeryvaughan1973,
  author  = {Hugh L. Montgomery and Robert C. Vaughan},
  title   = {The large sieve},
  journal = {Mathematika},
  volume  = {20},
  year    = {1973},
  pages   = {119--134}
}
```

<!-- SOURCE_BODY_END -->
