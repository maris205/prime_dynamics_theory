# A Higher-$Q$ Scale Audit of a Fixed Prime-Shell Tilt

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 2026
- **Repository source commit:** `5bebbda8ae9cf0a92b28c03272f89c43e28cfbc5`

## Abstract

TPC-365 found that a beta=2 prime-shell tilt survived a response-blind finite holdout through $Q=512$. We now freeze beta=2 and attack scale on a new geometry-selected panel, using the five-anchor ladder $Q\in\{512,1024,2048,4096,8192\}$. Forty-one candidate origins are scored only by unsigned weighted square geometry on 256-point pilots; the declared greedy rule selects $(623071,631360,629211)$. The complete replay has 480 rows, with two betas, two counts, two kernel exponents, four fixed sign laws, and all five shell anchors. Beta=2 has zero spectral-cap and zero Schur-cap violations in all 240 rows, with maximum normalized spectrum $0.62448287758976528$ and maximum normalized Schur value $0.65368278287004711$. The beta=0 control has 60 violations of each cap. This is a finite higher-$Q$ observation, not a shell-uniform operator theorem, a source-valid arithmetic normalization, a Route-A/Route-B pass, or a twin-prime result.

# Question and scope

TPC-362 located a finite cap failure beginning at \(Q=128\) for the inherited normalization. TPC-364 introduced the explicit shell weight \[w_{p,\beta}=\left(\frac pQ\right)^\beta,\] and TPC-365 showed that the fixed choice beta=2 transferred to a new finite panel through \(Q=512\). The present question is narrower: after beta=2 is frozen, how far does the finite cap observation extend in \(Q\)?

The panel is still geometry-selected. It is therefore useful for mapping a route and locating scale obstructions, but it is not a random independent sample or a uniform-in-origin claim. No source vector, adaptive sign, or arithmetic reassembly is used. The official Session-named Route-A and Route-B evaluator files are absent from this checkout; local Bridge-B is fail-closed evidence only.

# Finite operator and frozen selection

For \(I=[x,x+N-1]\cap\mathbb Z\) and \(Q<p\leq2Q\), define \[B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
\left(\mathbf{1}_{p\mid u-t}-\frac1{p-1}\right)
\mathbf{1}_{u\ne t}\mathbf{1}_{p\nmid u}\mathbf{1}_{p\nmid t}.
\label{eq:block}\] For integer beta, let \[A_{\beta,\varepsilon}=\sum_{Q<p\leq2Q}\varepsilon_p
\left(\frac pQ\right)^\beta B_p,\qquad
G_{\beta,u}=\sum_{Q<p\leq2Q}\sum_{t\in I}
\left(\left(\frac pQ\right)^\beta B_p(u,t)\right)^2 .
\label{eq:weighted}\] The normalized matrix is the finite symmetric congruence \[A_{\beta,\varepsilon}^{\#}
=D_{G_\beta}^{-1/2}A_{\beta,\varepsilon}D_{G_\beta}^{-1/2},
\qquad D_{G_\beta}=\operatorname{diag}(G_{\beta,u}).
\label{eq:norm}\] The geometry is a sum of rational squares. Once it is positive, the only operator bounds used are the elementary finite envelopes \[\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}\]

Candidate origins are \(a_j=620001+307j\), \(0\leq j<41\). On \([a_j,a_j+255]\), calculate beta=2 geometry at every declared \((Q,s)\) and score \[S(a_j)=\max_{Q,s}\frac{\max_uG_{2,u}}{\min_uG_{2,u}},
\qquad Q\in\{512,1024,2048,4096,8192\},\quad s\in\{1,2\}.
\label{eq:score}\] Sort by decreasing score and increasing origin, then greedily retain origins separated by at least 2048. The ordered output is \((623071,631360,629211)\). The top score is \(2.0552882031131818\) at origin 623071, attained at \((Q,s)=(512,2)\). The signed matrices are evaluated only after this rule is frozen.

# Higher-\(Q\) audit

The protocol uses counts \(256,512\), exponents \(1,2\), four fixed laws (all-plus, alternating shell index, prime modulo-four character, and half-shell split), and beta \(0,2\). Thus it contains \(2\cdot3\cdot2\cdot5\cdot2\cdot4=480\) rows, with a true spectrum for every law. The spectral value \(0.64\) and Schur value \(0.83\) are inherited finite working caps only.

<div id="tab:beta">

| beta | max spectrum | spectral failures |    max Schur | Schur failures |
| ---: | -----------: | ----------------: | -----------: | -------------: |
|    0 | 1.6419614116 |                60 | 1.7182186230 |             60 |
|    2 | 0.6244828776 |                 0 | 0.6536827829 |              0 |

Complete beta census on the higher-\(Q\) panel (240 rows per beta).

</div>

<div id="tab:q">

|       |              |          |              |          |
| ----: | -----------: | -------: | -----------: | -------: |
|       |              |          |              |          |
| \(Q\) | max spectrum | failures | max spectrum | failures |
|   512 | 1.6398880045 |       12 | 0.6163019781 |        0 |
|  1024 | 1.6409838731 |       12 | 0.6244828776 |        0 |
|  2048 | 1.6415483555 |       12 | 0.6196009007 |        0 |
|  4096 | 1.6418250155 |       12 | 0.6229914076 |        0 |
|  8192 | 1.6419614116 |       12 | 0.6208083916 |        0 |

Maximum normalized spectrum at each shell anchor.

</div>

The beta=0 failures occur at every shell anchor in this declared panel. The beta=2 maximum remains below both finite caps, but it is not monotone: it rises from the TPC-365 value \(0.61633188509480319\) to \(0.62448287758976528\), a difference of \(0.0081509924949620949\). We record this increase rather than assigning a decay or transfer theorem. The minimum effective shell fraction is \(0.66944805377549699\), so the finite observation is not described as a one-prime truncation.

# Exact and independent verification

At \(Q=4\), exponent one, the half-open interval \([623372,623385)\) has shell \(\{5,7\}\). Exact rational matrix and geometry digests are retained for beta=0 and beta=2; symmetry and positivity are checked by exact arithmetic.

The forward producer evaluates 480 rows in increasing shell order. An independently written checker rebuilds the sieve, response-blind selection, masks, weights, four laws, geometry, finite envelopes, and all true spectra in reverse shell order. It compares every row’s shell, weights, geometry extrema, raw and normalized metrics, row index, phase census, and exact anchor. A separate adversarial checker rejects 23 mutations of protocol, selection, scale limits, phase counts, and claim-firewall fields. Local Bridge-B requires empty stderr and byte-identical stdout in normal and optimized modes.

# Claim firewall and route decision

    TPC366_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
    TPC366_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC366_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_480_ROWS
    TPC366_HIGHER_Q_LADDER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC366_BETA2_HIGHER_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC366_BETA2_SCALE_UNIFORMITY = OPEN
    TPC366_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC366_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC366_GROWING_OPERATOR_BOUND = OPEN
    TPC366_SOURCE_UNIFORM_L2 = OPEN
    TPC366_ARITHMETIC_ADVANCE = NO
    TPC366_FIXED_POWER_CREDIT = 0
    TPC366_FULL_GATE_B = OPEN
    TPC366_TWIN_PRIME_RESULT = NONE

The strongest positive result is a fixed beta=2 cap observation through \(Q=8192\) on the declared finite panel. The strongest obstruction is the nonmonotone finite scale profile together with geometry-based origin selection and the absence of source validity. No Route-A or Route-B gate is closed, no fixed power is credited, and no twin-prime conclusion follows. The next minimal attack is to keep beta=2 fixed while using longer windows and predeclared or unselected origins.

# Conclusion

TPC-366 extends the finite beta=2 signal by four additional shell scales, through \(Q=8192\), while the beta=0 control continues to fail at every anchor. This is useful route reconnaissance: the immediate obstruction is no longer the tested shell size, but the lack of a uniform statement across windows, origins, and the arithmetic source. The result remains a finite modeling audit. A growing operator bound, source-uniform \(L^2\), source-valid normalization, reassembly, and the twin-prime endpoint remain open.

`TPC366_ARITHMETIC_ADVANCE=NO`, `TPC366_FIXED_POWER_CREDIT=0`, `TPC366_FULL_GATE_B=OPEN`.
