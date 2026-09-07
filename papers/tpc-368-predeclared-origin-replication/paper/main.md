# A Second Predeclared Origin-Family Replication of a Finite Prime-Shell Obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-367 found a finite long-window failure of a fixed beta=2 prime-shell tilt on three response-blind, predeclared origins. We test whether that pattern is specific to its origin family. A second grid, $810001+353j$, is declared in advance and the indices $0,20,40$ are frozen before any signed response or geometry score is evaluated. Counts $512$ and $1024$, shell anchors $Q\in\{512,2048,8192\}$, exponent one, four fixed sign laws, and beta $0,2$ produce 144 true-spectral rows. Beta=2 again has exactly six spectral-cap failures, all at count 1024, the two larger anchors, and the all-plus law; it has no Schur-cap failure. The beta=0 control has 18 spectral and 18 Schur failures. This is a finite replication and obstruction audit, not an asymptotic theorem, an arithmetic estimate, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The beta=2 point was selected as a useful finite shell tilt in the preceding TPC-364–366 experiments. TPC-367 then showed that a geometry-unselected long-window panel can break its working spectral cap. The present paper asks the smallest independent follow-up: does the same localized failure occur on a second, predeclared origin family?

The official Session-named Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B checker is consequently fail-closed repository evidence only. No source vector, adaptive selection, signed response, or arithmetic reassembly enters the experiment. All statements below are restricted to the explicitly declared finite panel.

# Finite operator and frozen protocol

Let $I=[a,a+N-1]\cap\mathbb Z$ and $S_Q=\{p\text{ prime}:Q<p\leq2Q\}$. With kernel exponent $s=1$, define $$B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\label{eq:block}$$ For beta $\in\{0,2\}$ and a fixed sign law $\varepsilon$, put $$A_{\beta,\varepsilon}=\sum_{p\in S_Q}\varepsilon_p
 \left(\frac pQ\right)^\beta B_p,\qquad
G_\beta(u)=\sum_{p\in S_Q}\sum_{t\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,t)\right]^2.
\label{eq:weighted}$$ Whenever $G_\beta(u)>0$, the normalized finite matrix is $$A_{\beta,\varepsilon}^{\#}(u,t)=
\frac{A_{\beta,\varepsilon}(u,t)}
 {\sqrt{G_\beta(u)G_\beta(t)}}.
\label{eq:norm}$$ The geometry is a finite sum of rational squares. For a finite real symmetric matrix $T$ we use only $$\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}$$

The candidate grid is $a_j=810001+353j$ for $0\leq j<41$. Indices $(0,20,40)$ give the origins $(810001,817061,824121)$ and are fixed before any matrix is evaluated. The laws are all-plus, alternating shell index, the prime-modulo-four character, and a half-shell split. The working caps are $0.64$ for the true spectral radius and $0.83$ for the Schur row sum. There are $2\cdot3\cdot1\cdot2\cdot4=48$ settings per beta and 144 law rows in total.

# Complete finite audit

Table [1](main.tex#L101){reference-type="ref" reference="tab:beta"} gives the census over all rows. Every law receives a true eigenvalue computation; Schur and Frobenius quantities are retained as separate envelopes.

<div id="tab:beta">

|  beta|  max spectrum|  spectral failures|     max Schur|  Schur failures|
|-----:|-------------:|------------------:|-------------:|---------------:|
|     0|  1.7829319996|                 18|  1.8516879707|              18|
|     2|  0.6741019059|                  6|  0.7000925111|               0|

: Census over the 72 rows for each beta.

</div>

<div id="tab:phase">

|  count|   $Q$|  max spectrum|  failures|
|------:|-----:|-------------:|---------:|
|    512|   512|  0.6163021933|         0|
|    512|  2048|  0.6196037018|         0|
|    512|  8192|  0.6208030776|         0|
|   1024|   512|  0.6218134237|         0|
|   1024|  2048|  0.6727835105|         3|
|   1024|  8192|  0.6741019059|         3|

: Beta=2 phase localization by count and shell anchor.

</div>

The six beta=2 failures are precisely $$(a,1024,2048,1,\mathrm{all\mathchar`-plus}),\quad
(a,1024,8192,1,\mathrm{all\mathchar`-plus})$$ for each $a\in\{810001,817061,824121\}$. Thus the finite failure key, not merely its aggregate maximum, is replicated. Count 512 stays below the spectral cap at all three anchors, and beta=2 stays below the Schur cap in all 72 rows. The beta=0 violations are all-plus rows across the declared settings and are retained as a literal control, not treated as a repair.

The replicated beta=2 maximum, $0.674101905927736$, is lower than the TPC-367 maximum $0.67410738070824539$ by $5.474780509384658\times10^{-6}$. This is a finite descriptive comparison; we infer neither monotonicity nor a limiting constant.

# Exact and independent verification

The exact anchor is the half-open interval $[810342,810355)$ at $Q=4$, whose shell is $\{5,7\}$. Rational arithmetic checks symmetry and positive geometry for beta 0 and 2, and stores canonical matrix and geometry digests.

The producer accumulates each shell in increasing order and evaluates all four laws from one component calculation per setting. An independently written checker rebuilds its own sieve, accumulates in descending shell order, and compares the shell, weights, geometry extrema, raw and normalized metrics, both eigenvalue endpoints, row indices, phase census, and exact anchor. Its output is

    TPC368_CERTIFICATE=PASS rows=144 beta2_rows=72
    TPC368_INDEPENDENT_CHECK=PASS rows=144 beta2_rows=72 beta2_violations=6

The adversarial checker rejects 29 mutations of protocol, data, audit, and claim fields. The local Bridge-B reruns producer, independent, and stress checks in normal and optimized Python modes, requiring empty stderr and byte-identical stdout.

# Claim firewall and route decision

    TPC368_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
    TPC368_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC368_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC368_SECOND_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC368_BETA2_LONG_WINDOW_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC368_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC368_ORIGIN_UNIFORMITY = OPEN
    TPC368_WINDOW_UNIFORMITY = OPEN
    TPC368_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC368_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC368_GROWING_OPERATOR_BOUND = OPEN
    TPC368_SOURCE_UNIFORM_L2 = OPEN
    TPC368_ARITHMETIC_ADVANCE = NO
    TPC368_FIXED_POWER_CREDIT = 0
    TPC368_FULL_GATE_B = OPEN
    TPC368_TWIN_PRIME_RESULT = NONE

The strongest positive result is a response-blind replication of the exact six-key finite pattern on a second origin family. The strongest obstruction is that the same pattern continues to block the declared count-1024 long-window cap transfer. This narrows the first-paper-origin explanation, but it does not establish origin uniformity, window uniformity, an asymptotic bound, source validity, arithmetic $L^2$, or any official route gate.

# Conclusion

Within the declared model, the beta=2 long-window obstruction survives a second predeclared origin family. The next minimal finite questions are a third response-blind origin family and a count-2048 window. A break in the pattern would motivate residue-phase localization; persistence would broaden the finite obstruction. In either case, no arithmetic credit is paid and the twin-prime endpoint remains untouched.

`TPC368_ARITHMETIC_ADVANCE=NO`, `TPC368_FIXED_POWER_CREDIT=0`, `TPC368_FULL_GATE_B=OPEN`.

<!-- SOURCE_BODY_END -->
