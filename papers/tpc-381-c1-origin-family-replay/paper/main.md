# An Origin-Family Replay of a Finite $c=1$ Prime-Shell Law Control

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: See preserved source title block
- Source date: See preserved source title block
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-380 found that a finite high-$Q$ spectral signature of the all-plus prime-shell law disappeared under three diagnostic signed controls. This paper tests the next origin-family question: does the separation survive on a second predeclared coordinate-disjoint family at the fixed count $N=2048$? On that fresh affine panel, the complete $3\times3\times4=36$ row experiment gives the all-plus profile $(0,3,3)$ and the three signed-control profiles $(0,0,0)$. There are six spectral-cap failures and no Schur-cap failures. The result is finite origin-family persistence with a law-dependence obstruction; it is neither an origin/scale-uniform theorem nor a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

**An Origin-Family Replay of a Finite $c=1$ Prime-Shell Law Control**\
Liang Wang\
School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China\
September 4, 2026

# Question and claim boundary

The finite operator family is designed to expose where a proposed near-block Route-B bridge needs uniformity. TPC-380 held the count at $2048$ on its first fresh family and found an all-plus high-$Q$ profile that did not occur for three fixed signed laws. Here only the coordinate-disjoint origin family changes. The same $c=1$ mask, normalization, shell ladder, and law family are retained.

All assertions below are scoped to one explicit finite computation. The signed laws are diagnostic controls; they are not asserted to be source-valid arithmetic weights. In particular, finite sub-cap values do not pay an arithmetic loss or close either route gate.

# Finite operator

For $I=[a,a+N-1]\cap\mathbb Z$, $Q<p\leq2Q$, and $u,t\in I$, set $$K_p(u,t)=p\left(\frac pQ\right)^2
 \frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid(u-t)}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.$$ For a declared law $\ell$ with signs $s_p(\ell)\in\{-1,1\}$, define $$A_\ell(u,t)=\sum_{Q<p\leq2Q}s_p(\ell)K_p(u,t),\quad
 G(u)=\sum_{t\in I}\sum_{Q<p\leq2Q}K_p(u,t)^2,
 \quad T_\ell(u,t)=\frac{A_\ell(u,t)}{\sqrt{G(u)G(t)}}.$$ The four laws are all-plus, alternating shell index, the sign of $p\bmod4$, and a first-half/second-half shell split. With $b(u)=\lfloor(u-a)/256\rfloor$, the common band and tail are $$B_\ell(u,t)=T_\ell(u,t){\bf1}_{|b(u)-b(t)|\leq1},\qquad
 R_\ell=T_\ell-B_\ell.$$ For every unit eigenvector $v$ of $T_\ell$ with eigenvalue $\lambda$, $$v^{\mathsf T}B_\ell v+v^{\mathsf T}R_\ell v=\lambda$$ is an exact finite identity.

# Predeclared origin-family protocol

Before any response or metric is read, fix $$a_j=1400001+401j,\quad 0\leq j<41,$$ and select indices $(0,20,40)$, giving origins $(1400001,1408021,1416041)$. Use $N=2048$, eight contiguous blocks of length $256$, beta $2$, exponent one, height $66$, and $Q=512,2048,8192$. The spectral and Schur caps are $0.64$ and $0.83$. All four laws are evaluated at every origin and every $Q$ before the profile is summarized.

The current intervals are disjoint from the declared TPC-376–380 intervals by exact integer endpoint comparisons. The first 13-point subinterval $[1400001,1400014)$ is the $q=8$ anchor. Its shell is $\{11,13\}$, and exact rational arithmetic checks positive common geometry and symmetry for all four laws. This anchor is an audit object, not a row-selection signal.

# Results

Table [1](main.tex#L99){reference-type="ref" reference="tab:count"} gives band spectral-cap failures among the three origins at each shell scale.

<div id="tab:count">

| law                | $Q=512$ | $Q=2048$ | $Q=8192$ |  max band spectral|
|:-------------------|:-------:|:--------:|:--------:|------------------:|
| all\_plus          |  $0/3$  |   $3/3$  |   $3/3$  |        0.666944276|
| alternating\_index |  $0/3$  |   $0/3$  |   $0/3$  |        0.007761004|
| mod4\_character    |  $0/3$  |   $0/3$  |   $0/3$  |        0.012055505|
| half\_split        |  $0/3$  |   $0/3$  |   $0/3$  |        0.216139340|

: TPC-381 finite count-2048 origin-family law-control panel.

</div>

Thus the all-plus profile is $(0,3,3)$ and each signed control has profile $(0,0,0)$. The total spectral census is $6/36$ and the Schur census is $0/36$. The corresponding maximum band spectral values in the displayed law order are approximately $$0.66694427563296521,\quad 0.0077610039910285299,\quad
0.012055505105884349,\quad 0.21613933977437655.$$ The certificate records all full/band metrics, selected-mode Rayleigh terms, and finite numerical residuals.

# Independent audit

The producer locks the TPC-380 source and canonical certificate, and writes a canonical JSON certificate. A separate checker uses a direct sieve through $20000$, reverse shell accumulation, independent sign construction, common geometry, and independent full and band eigensystems without importing the TPC-381 producer. A 25-mutation stress suite changes protocol, count, laws, rows, census, clue, and firewall fields; every mutation must be rejected. Normal and optimized runs require empty standard error and byte-identical summaries. The local Bridge-B repeats these finite checks and locks the stable project artifacts.

# Route status and conclusion

The Session-named Route-A and Route-B evaluator files are absent from this checkout, so the local route note and Bridge-B are fail-closed repository evidence rather than an official evaluator verdict. The exact finite protocol, endpoint separation, common geometry, four laws, and Rayleigh split are proved finite statements. The replay and failure census are numerically certified finite statements.

The strongest positive result is persistence of the TPC-380 all-plus high-$Q$ profile on a second origin family at the same count. The strongest obstruction is that the persistence remains law-dependent, so it cannot be promoted to a law-invariant mask theorem. Law/origin/scale uniformity, source-valid normalization, cross-block causality, a growing operator bound, source-uniform arithmetic $L^2$, signed prime-shell reassembly, and a twin-prime conclusion remain open. The certificate records $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
\texttt{FIXED\_POWER\_CREDIT=0},\qquad
\texttt{FULL\_GATE\_B=OPEN}.$$ The next minimal finite question is `TEST_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT`.

<!-- SOURCE_BODY_END -->
