# A Count-2048 Audit of a Persistent Finite Prime-Shell Failure Signature

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We perform the next predeclared finite-window audit after a third-origin replication of a beta=2 prime-shell obstruction. The origin grid $1010001+401j$ and indices $0,20,40$ are inherited without reading any response, giving $(1010001,1018021,1026041)$. We fix count $2048$, shell anchors $Q\in\{512,2048,8192\}$, exponent one, four sign laws, and beta $0,2$, for 72 true-spectral rows. Beta=2 has exactly six spectral-cap failures: the all-plus law at $Q=2048$ and $8192$ at all three origins; it has no Schur-cap failure. The beta=0 control has nine spectral and nine Schur failures. The six-key origin/$Q$/law support agrees with the parent count-1024 signature after removing the count coordinate, while the maximum increases from $0.67410489800609708$ to $0.71099989528234753$. This is a finite numerical certificate and obstruction analysis, not an asymptotic theorem, an arithmetic estimate, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

The preceding TPC-369 audit reproduced a six-key beta=2 failure support on a third response-blind origin family at count 1024. The present question is minimal and outcome-neutral: does that support persist when only the window count is changed to 2048, and does its normalized magnitude remain comparable?

The official Session-named Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B checker is therefore fail-closed repository evidence only. We make no claim about an official route pass. In particular, all statements below are restricted to the declared finite panel; no source vector, adaptive origin ranking, or arithmetic reassembly is used.

# Finite operator and frozen protocol

Let $I=[a,a+N-1]\cap\mathbb Z$ and $S_Q=\{p\text{ prime}:Q<p\le 2Q\}$. With height 66 and kernel exponent one, $$B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\label{eq:block}$$ For beta $\in\{0,2\}$ and a fixed sign law $\varepsilon$, define $$A_{\beta,\varepsilon}=\sum_{p\in S_Q}\varepsilon_p
 \left(\frac pQ\right)^\beta B_p,
\qquad
G_\beta(u)=\sum_{p\in S_Q}\sum_{t\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,t)\right]^2.
\label{eq:weighted}$$ When $G_\beta(u)>0$, the normalized finite matrix is $$A_{\beta,\varepsilon}^{\#}(u,t)=
\frac{A_{\beta,\varepsilon}(u,t)}
 {\sqrt{G_\beta(u)G_\beta(t)}}.
\label{eq:norm}$$ Every summand of $G_\beta$ is a rational square. For a finite real symmetric matrix $T$, we use only the elementary envelopes $$\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}$$

The candidate grid is $a_j=1010001+401j$ for $0\le j<41$; indices $(0,20,40)$ give the three origins above. Count $N=2048$, shell anchors $512,2048,8192$, beta values $0,2$, exponent one, the spectral cap $0.64$, and the Schur cap $0.83$ are fixed before signed replay. The four laws are all-plus, alternating shell index, the prime-modulo-four character, and a half-shell split. The Cartesian product has 72 rows.

# Inherited exact anchor

The exact proof anchor is inherited from TPC-369 rather than reselected: the half-open interval $[1010346,1010359)$ at $Q=4$, exponent one, and shell $\{5,7\}$. The producer recomputes its exact rational matrix and geometry for both beta values and checks symmetry and positivity. This inheritance is hash-locked to the parent code and certificate and is independent of all count-2048 responses. It is a finite witness for well-defined normalization, not evidence for a growing operator.

# Complete count-2048 audit

Table [1](main.tex#L110){reference-type="ref" reference="tab:phase"} gives the complete phase census. Every row receives a true eigenvalue endpoint computation; Schur and Frobenius values remain separate finite envelopes.

<div id="tab:phase">

|  beta|  count|            $Q$|  spectral failures|  Schur failures|
|-----:|------:|--------------:|------------------:|---------------:|
|     0|   2048|  512,2048,8192|                  9|               9|
|     2|   2048|            512|                  0|               0|
|     2|   2048|           2048|                  3|               0|
|     2|   2048|           8192|                  3|               0|

: Count-2048 census over the 36 rows for each beta.

</div>

The six beta=2 failure keys are $$(a,2048,2048,1,\mathrm{all\mathchar`-plus}),\qquad
(a,2048,8192,1,\mathrm{all\mathchar`-plus})$$ for each $a\in\{1010001,1018021,1026041\}$. Thus the origin/$Q$/law support agrees with the TPC-369 parent support after quotienting out the changed count coordinate. This comparison is deliberately weaker than an assertion that the matrices or their maxima agree.

The beta=2 maxima in this panel are $$\max\lVert\,\cdot\,\rVert_2{A^{\#}_{2,\varepsilon}}=0.71099989528234753,
\qquad
\max\operatorname{Schur}(A^{\#}_{2,\varepsilon})=0.72908109638522522.$$ The latter is below the Schur cap. The parent beta=2 maximum was $0.67410489800609708$, so the finite difference is $0.036894997276250452$. The count change therefore preserves failure support but does not support a constant-level extrapolation. The beta=0 control has maximum spectral value $1.8805246187378462$ and maximum Schur value $1.9283610051844953$.

# Independent and hostile verification

The producer accumulates each shell in increasing order. An independent checker uses a separate prime sieve and descending shell accumulation. It recomputes all 72 rows, the inherited exact anchor, the parent certificate signature, phase counts, row indices, raw and normalized metrics, and eigenvalue endpoints. The certificate is canonical JSON with explicit payload and row digests. The hostile checker rejects 32 mutations spanning protocol, count, row, phase, parent-signature, anchor-inheritance, firewall, and clue fields.

The local Bridge-B checker runs the producer, independent replay, and hostile stress suite in normal and optimized Python modes; it requires empty stderr and byte-identical stdout. Because the named official evaluator files are not present, this is repository-level finite evidence only.

# Claim firewall and route decision

    TPC370_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
    TPC370_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC370_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
    TPC370_COUNT_2048_WINDOW = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC370_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC370_BETA2_PARENT_SIGNATURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC370_ORIGIN_UNIFORMITY = OPEN
    TPC370_WINDOW_UNIFORMITY = OPEN
    TPC370_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC370_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC370_GROWING_OPERATOR_BOUND = OPEN
    TPC370_SOURCE_UNIFORM_L2 = OPEN
    TPC370_ARITHMETIC_ADVANCE = NO
    TPC370_FIXED_POWER_CREDIT = 0
    TPC370_FULL_GATE_B = OPEN
    TPC370_TWIN_PRIME_RESULT = NONE

The strongest positive result is finite support replication of the six-key pattern under a predeclared count change. The strongest obstruction is the simultaneous magnitude change: support persistence alone does not yield a stable normalized operator scale. The reusable structure is to compare support after removing the deliberately changed coordinate while retaining the magnitude as an independent diagnostic.

No growing operator bound, source-valid normalization, source-uniform arithmetic $L^2$, prime-shell reassembly, fixed-power saving, official route gate closure, asymptotic repair, or twin-prime statement is proved.

# Conclusion

At count 2048, the same high-$Q$, all-plus beta=2 support appears at all three inherited origins, but its maximum is materially larger than at count 1024. The next minimal question is phase localization: identify which predeclared origin/residue/high-$Q$ subphase carries the persistent support without using the observed response to select a cell. Arithmetic advance remains `NO`, fixed-power credit remains zero, and full Gate B remains open.

`ROUND2_CLUE = TEST_COUNT_2048_PHASE_LOCALIZATION`.

<!-- SOURCE_BODY_END -->
