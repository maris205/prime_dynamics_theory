# A Predeclared Long-Window Obstruction for a Fixed Prime-Shell Tilt

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 2026
- **Repository source commit:** `5bebbda8ae9cf0a92b28c03272f89c43e28cfbc5`

## Abstract

TPC-366 carried a fixed beta=2 prime-shell tilt through a finite higher-$Q$ ladder, but its origins were geometry-selected and its windows were short. We remove both conveniences in a scoped audit. Three origins are declared in advance as equally spaced points of the grid $620001+307j$, and counts $512$ and $1024$ are tested at $Q\in\{512,2048,8192\}$, with two kernel exponents, four fixed sign laws, and beta $0,2$. The complete replay has 288 rows. Beta=2 has no spectral-cap failure at count 512, but has exactly six spectral-cap failures at count 1024: all three origins fail at $Q=2048$ and $8192$ under the all-plus law. There are no beta=2 Schur-cap failures. The beta=0 control has 36 spectral and 36 Schur failures. This is a finite obstruction to one declared transfer statement, not an asymptotic theorem, an arithmetic estimate, or a twin-prime result.

# Question and scope

TPC-364/365 identified beta=2 as a useful finite shell tilt, and TPC-366 tested it on a geometry-selected panel through \(Q=8192\). The present paper asks a deliberately adversarial finite question: does the same cap survive when the origin choice is predeclared and the window is doubled from 512 to 1024? A failure is useful route reconnaissance; it is not evidence against the rule outside the declared panel.

The official Session-named Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B checker is therefore fail-closed repository evidence only. No source vector, signed response, adaptive law, or arithmetic reassembly enters this experiment.

# Finite operator and protocol

Let \(I=[a,a+N-1]\cap\mathbb Z\), \(Q<p\leq2Q\), and let \(s\in\{1,2\}\). The literal masked component is \[B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
\label{eq:block}\] For beta \(\in\{0,2\}\) and a fixed sign law \(\varepsilon\), put \[A_{\beta,\varepsilon}=\sum_{Q<p\leq2Q}\varepsilon_p
 \left(\frac pQ\right)^\beta B_p,\qquad
G_\beta(u)=\sum_{Q<p\leq2Q}\sum_{t\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,t)\right]^2.
\label{eq:weighted}\] When \(G_\beta(u)>0\), the finite normalized matrix is \[A_{\beta,\varepsilon}^{\#}(u,t)=
\frac{A_{\beta,\varepsilon}(u,t)}
 {\sqrt{G_\beta(u)G_\beta(t)}}.
\label{eq:norm}\] The geometry is a finite sum of rational squares. For any finite real symmetric matrix \(T\) we use only the elementary envelopes \[\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}\]

The candidate origin grid is \(a_j=620001+307j\), \(0\leq j<41\). The indices \((0,20,40)\), giving \((620001,626141,632281)\), are fixed before replay. This is a declaration, not a random-sampling model: no geometry score or response is consulted. The four laws are all-plus, alternating shell index, prime-modulo-four character, and half-shell split. The finite working caps are \(0.64\) for the true spectral radius and \(0.83\) for the Schur row sum.

# Complete finite audit

The Cartesian product has \(2\cdot3\cdot2\cdot3\cdot2\cdot4=288\) rows. Every law receives a true eigenvalue computation; Schur and Frobenius values are retained as separate envelopes.

<div id="tab:beta">

| beta | max spectrum | spectral failures |    max Schur | Schur failures |
| ---: | -----------: | ----------------: | -----------: | -------------: |
|    0 | 1.7829316949 |                36 | 1.8516811647 |             36 |
|    2 | 0.6741073807 |                 6 | 0.7000994578 |              0 |

Census over all 144 rows for each beta.

</div>

<div id="tab:phase">

| count | \(Q\) | max spectrum | failures |
| ----: | ----: | -----------: | -------: |
|   512 |   512 | 0.6162733029 |        0 |
|   512 |  2048 | 0.6195863919 |        0 |
|   512 |  8192 | 0.6208052938 |        0 |
|  1024 |   512 | 0.6218044852 |        0 |
|  1024 |  2048 | 0.6727799610 |        3 |
|  1024 |  8192 | 0.6741073807 |        3 |

Beta=2 phase localization by count and shell anchor.

</div>

The six failures are exactly the all-plus, exponent-one rows at the two larger anchors for the three predeclared origins. Exponent two remains below the spectral cap in this finite panel, which is a sensitivity observation, not a repair theorem. At count 512, beta=2 remains below the spectral cap at all three anchors. The beta=0 control fails at every count and anchor in the declared phase diagram. The beta=2 maximum exceeds the TPC-366 maximum \(0.62448287758976528\) by \(0.049624503118480101\); we make no monotonicity claim from this difference.

# Exact and independent verification

The exact anchor is the half-open interval \([620362,620375)\) at \(Q=4\), exponent one, whose shell is \(\{5,7\}\). Rational arithmetic checks symmetry and positive geometry for beta 0 and 2 and stores canonical matrix and geometry digests.

The forward producer accumulates each shell in increasing order. An independently written checker rebuilds its own sieve and evaluates every setting in descending shell order, then compares shells, weights, geometry extrema, raw and normalized envelopes, both eigenvalue endpoints, row indices, phase census, and the exact anchor. A 28-mutation stress checker rejects altered protocol flags, row data, audit counts, and claim fields. The local Bridge-B checker reruns the three checks in normal and optimized Python modes, requiring empty stderr and byte-identical stdout.

# Claim firewall and route decision

    TPC367_ORIGIN_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
    TPC367_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC367_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
    TPC367_LONG_WINDOW_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC367_UNSELECTED_ORIGIN_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC367_BETA2_LONG_WINDOW_TRANSFER = REFUTED_SCOPED
    TPC367_BETA2_EXPONENT_SENSITIVITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC367_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC367_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC367_GROWING_OPERATOR_BOUND = OPEN
    TPC367_SOURCE_UNIFORM_L2 = OPEN
    TPC367_ARITHMETIC_ADVANCE = NO
    TPC367_FIXED_POWER_CREDIT = 0
    TPC367_FULL_GATE_B = OPEN
    TPC367_TWIN_PRIME_RESULT = NONE

The strongest positive result is the complete count-512 beta=2 pass and the absence of Schur failures across all beta=2 rows. The strongest obstruction is the localized count-1024 spectral failure, reproduced at all three predeclared origins. The finite evidence does not close any official route gate, pay fixed-power credit, validate the source, or reassemble a prime correlation.

# Conclusion

The finite beta=2 signal is window-sensitive in the declared model: it holds through the tested higher-\(Q\) anchors at count 512 but not at count 1024 for the all-plus, exponent-one rows at \(Q=2048\) and \(8192\). The next natural experiment is a second predeclared origin family with the failing exponent and long-window scale frozen. Replication would broaden the obstruction; non-replication would motivate residue-phase localization. In either case, the arithmetic bridge, growing bounds, and twin-prime endpoint remain open.

`TPC367_ARITHMETIC_ADVANCE=NO`, `TPC367_FIXED_POWER_CREDIT=0`, `TPC367_FULL_GATE_B=OPEN`.
