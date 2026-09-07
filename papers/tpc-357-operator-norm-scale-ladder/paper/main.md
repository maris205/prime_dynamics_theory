# A Finite Operator-Norm Scale Ladder\ for Position-Aware Twin-Prime Operators

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We perform a finite operator-level audit of the position-aware congruence introduced in the preceding <span class="smallcaps">TPC</span> releases. The three origins selected by a response-blind geometry rule in TPC-356 are frozen, and the interval count is extended from 256 through 2048. For every one of four sign laws, three shell anchors, two kernel exponents, three origins, and four counts, we record the exact finite Schur row-sum and Frobenius envelopes, giving 288 law-level rows. For the all-plus law we additionally compute both extreme eigenvalues on every row. The normalized Schur maximum is 0.8077815961017315, while the normalized all-plus spectral maximum is 0.62665294142584216; the corresponding raw all-plus spectral maximum is 1542.7455490253569. These are finite scoped certificates, not uniform estimates. In fact, the normalized all-plus spectral ladder has 15 upward transitions, 35 downward transitions, and 4 guarded flats. Thus a natural monotone-decay hypothesis is rejected on the declared ladder, while a growing operator bound and every arithmetic Route-B gate remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The twin-prime program under study uses literal divisibility-masked shell operators. TPC-355 introduced a response-independent diagonal congruence based on unsigned mask energy, and TPC-356 selected deliberately uneven origins using geometry alone. The present question is narrower: what can be said about operator size along a longer finite count ladder once those origins are frozen?

There are two reasons to separate this question from the source calculation. First, an operator estimate should not depend on a fitted source response or on a preferred sign law. Second, a finite spectral readout and an exact norm inequality have different logical status. We therefore report Schur and Frobenius envelopes for every sign law, but reserve true spectral computation for the all-plus subfamily. Nothing below asserts an estimate uniform in the origin, interval length, shell, or source.

The official Session-named Route-A and Route-B evaluator files are not present in this checkout. The local Bridge-B checker is consequently used as fail-closed reproducibility evidence and is not called an official evaluator pass.

# Finite operator model

Let $I=[x,x+N-1]\cap\mathbb Z$, let $S_Q=\{p\text{ prime}:Q<p\leq 2Q\}$, and put $H=66$. For $s\in\{1,2\}$ define $$B_p(u,t)=p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac{1}{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
 \label{eq:block}$$ For a fixed sign vector $\varepsilon$ on the shell, write $$A_\varepsilon=\sum_{p\in S_Q}\varepsilon_p B_p,
 \qquad
 G_u=\sum_{p\in S_Q}\sum_{t\in I}B_p(u,t)^2.
 \label{eq:raw}$$ The TPC-355 normalization is the symmetric congruence $$A_\varepsilon^{\#}=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
 \qquad D_G=\operatorname{diag}(G_u).
 \label{eq:norm}$$ The finite replay checks $G_u>0$ on every row. The four declared laws are all-plus, alternating by shell index, the mod-$4$ character of the prime, and a half-shell split.

# Exact envelopes and numerical protocol

For a finite real symmetric matrix $T$, symmetry gives $\lVert T\rVert_1=\lVert T\rVert_\infty$. The induced-norm inequality therefore yields $$\lVert\,\cdot\,\rVert_2{T}\leq \sqrt{\lVert T\rVert_1\lVert T\rVert_\infty}
 =\max_u\sum_t|T(u,t)|=:S(T).
 \label{eq:schur}$$ Independently, the singular-value decomposition gives $$\lVert\,\cdot\,\rVert_2{T}\leq \lVert T\rVert_F.
 \label{eq:frob}$$ These are exact finite inequalities. They do not say that $S(T)$ or $\lVert T\rVert_F$ stays bounded when the finite model changes.

The three origins are inherited without re-selection from TPC-356 `\cite{tpc356}`: $$(38423,\,42010,\,45597).$$ We use $N\in\{256,512,1024,2048\}$, $Q\in\{24,54,80\}$, $s\in\{1,2\}$, and the four laws, for $3\cdot4\cdot3\cdot2\cdot4=288$ rows. Each row records $S(T)$ and $\lVert T\rVert_F$ for both $A_\varepsilon$ and $A_\varepsilon^\#$. For all-plus, both extreme eigenvalues are computed with a symmetric dense eigensolver, so there are 72 raw and 72 normalized spectral values.

For each fixed $(x,Q,s)$, we compare the four counts. A transition is an increase or decrease only when its absolute difference exceeds $10^{-6}$; otherwise it is called flat. The producer accumulates shell components in forward order. A separate checker rebuilds every matrix in reverse shell order, which changes floating-point summation order while preserving the mathematical protocol.

# Results

Table [1](main.tex#L139){reference-type="ref" reference="tab:envelopes"} summarizes the extrema of the principal envelopes. The all-plus raw operator has a much larger finite scale than its normalized counterpart. The other sign laws have no spectral claim in this paper, but their Schur and Frobenius values are still part of the common audit.

<div id="tab:envelopes">

| Law         | operator   |  $S_{\min}$|  $S_{\max}$|  $F_{\min}$|  $F_{\max}$|
|:------------|:-----------|-----------:|-----------:|-----------:|-----------:|
| all-plus    | raw        |     836.619|    4004.288|    1164.473|    9094.443|
| all-plus    | normalized |    0.106203|    0.807782|    0.137940|    2.215056|
| alternating | raw        |     347.970|    1801.600|     528.168|    7443.041|
| alternating | normalized |    0.046478|    0.213798|    0.114206|    0.730698|
| mod-4       | raw        |     324.105|    1923.928|     528.630|    7459.411|
| mod-4       | normalized |    0.052538|    0.218149|    0.114806|    0.730972|
| half-split  | raw        |     313.851|    1799.567|     523.919|    7443.576|
| half-split  | normalized |    0.046551|    0.203572|    0.114214|    0.725633|

: Extrema over the 72 rows of each sign law. Spectral columns are reported only for all-plus.

</div>

The normalized all-plus spectral maximum is $$\max\lVert\,\cdot\,\rVert_2{A_\varepsilon^\#}=0.62665294142584216<0.64,
 \label{eq:cap}$$ whereas the raw maximum is $1542.7455490253569>1500$. Across all 288 rows, the computed spectral values obey both finite envelopes whenever a spectral value is recorded; there are no envelope violations. The exact rational anchor uses $I=[38431,38444]$, $Q=4$, and shell $\{5,7\}$, and independently verifies matrix symmetry and positive geometry before any floating-point cap is quoted.

The scale transition census is more informative than a single maximum. For raw all-plus spectral values, all 54 transitions increase. For normalized all-plus spectral values, the counts are $$(\text{increase},\text{decrease},\text{flat})=(15,35,4).$$ At $(x,Q,s)=(42010,80,2)$ the four normalized spectral values are $$0.6263543507,\quad 0.6032097319,\quad
 0.6033370730,\quad 0.6036446871,$$ which contains a sharp initial decrease followed by two increases. At $(38423,24,1)$ all three transitions increase, from $0.0300699460$ to $0.0303127446$. The observed cap and the observed nonmonotonicity are compatible: boundedness on four finite counts is not a decay theorem.

# Independent controls

The release certificate is canonical JSON with a content hash. It locks the TPC-355 producer and the TPC-356 producer and certificate, and contains the full row payload and transition audit. The independent reverse-shell checker does not import the TPC-357 producer. It reconstructs the prime sieve, divisibility masks, geometry diagonal, four signed matrices, normalized congruences, envelopes, eigenvalue rows, and exact anchor. Its tolerance is $3\times10^{-5}$ relative to the larger of one and the compared values.

The mutation stress test applies twelve in-memory mutations, including schema, row count, parent provenance, threshold values, response-blindness, transition census, exact-anchor status, firewall, and payload hash. Every mutation is rejected and the unmodified baseline digest is preserved. The local Bridge-B checker reruns producer, independent, and stress checks in normal and optimized Python modes and requires byte-identical stdout.

# Claim firewall and conclusion

The exact contribution is the finite norm envelope [\[eq:schur\]](main.tex#L100){reference-type="eqref" reference="eq:schur"}– [\[eq:frob\]](main.tex#L105){reference-type="eqref" reference="eq:frob"}, together with a reproducible 288-row operator audit. On the declared panel, the normalized Schur maximum is below $0.83$ and the all-plus spectral maximum is below $0.64$. These values provide a useful finite diagnostic for the TPC-355 preconditioner.

The obstruction is decisive for route planning. The normalized spectral ladder is not monotone even after the geometry normalization, and neither the finite cap nor the Schur envelope controls a growing origin or interval. We therefore assign zero fixed-power credit. A source-uniform masked $L^2$ estimate, arithmetic reassembly, full Gate B, and any twin-prime conclusion remain open. The next experiment should attack the finite spectral cap on a fresh pre-registered origin-scale holdout before any arithmetic claim is attempted.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc355,
  author       = {Liang Wang},
  title        = {Position-aware mask-energy normalization},
  year         = {2026},
  note         = {TPC-355 finite research release in the accompanying repository}
}

@misc{tpc356,
  author       = {Liang Wang},
  title        = {Geometry-adversarial normalization holdout},
  year         = {2026},
  note         = {TPC-356 finite research release in the accompanying repository}
}
```

<!-- SOURCE_BODY_END -->
