# A Third Predeclared Origin-Family Audit of a\ Finite Prime-Shell Obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We test a third response-blind origin family against the finite beta=2 prime-shell obstruction found in TPC-367 and replicated in TPC-368. The candidate grid $1010001+401j$ is declared in advance, and indices $0,20,40$ are frozen before any signed response or geometry score is evaluated. Counts $512$ and $1024$, shell anchors $Q\in\{512,2048,8192\}$, exponent one, four fixed sign laws, and beta $0,2$ give 144 true-spectral rows. Beta=2 again has exactly six spectral-cap failures: count 1024, the two larger shell anchors, the all-plus law, and all three origins. It has no Schur-cap failure. The beta=0 control has 18 spectral and 18 Schur failures. An initially proposed small exact anchor has zero geometry and is explicitly refuted; a deterministic unsigned first-positive rule repairs only that proof anchor before spectral replay. The result is a finite third-family replication and obstruction audit, not an asymptotic theorem, an arithmetic estimate, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC-367 located a count-1024 failure of a fixed beta=2 shell tilt on a predeclared long-window panel. TPC-368 reproduced the exact six failure keys on a second origin family. The present paper asks the next minimal question: does the same finite pattern survive a third family with a different start and step, again selected without reading the response?

The official Session-named Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B checker is therefore fail-closed repository evidence only. No source vector, adaptive origin ranking, or arithmetic reassembly enters the experiment. Every statement below is restricted to the declared finite panel.

# Finite operator and frozen protocol

Let $I=[a,a+N-1]\cap\mathbb Z$ and $S_Q=\{p\text{ prime}:Q<p\leq2Q\}$. With height 66 and kernel exponent one, define $$B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\label{eq:block}$$ For beta $\in\{0,2\}$ and a fixed sign law $\varepsilon$, put $$A_{\beta,\varepsilon}=\sum_{p\in S_Q}\varepsilon_p
 \left(\frac pQ\right)^\beta B_p,
\qquad
G_\beta(u)=\sum_{p\in S_Q}\sum_{t\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,t)\right]^2.
\label{eq:weighted}$$ When $G_\beta(u)>0$, the normalized finite matrix is $$A_{\beta,\varepsilon}^{\#}(u,t)=
\frac{A_{\beta,\varepsilon}(u,t)}
 {\sqrt{G_\beta(u)G_\beta(t)}}.
\label{eq:norm}$$ The geometry is a finite sum of rational squares. For a finite real symmetric matrix $T$, the only analytic envelopes used here are $$\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}$$

The frozen candidate grid is $a_j=1010001+401j$ for $0\leq j<41$. Indices $(0,20,40)$ give $$(a_0,a_{20},a_{40})=(1010001,1018021,1026041).$$ These indices, counts $512,1024$, shell anchors $512,2048,8192$, beta values $0,2$, exponent one, the spectral cap $0.64$, and the Schur cap $0.83$ are fixed before signed replay. The four laws are all-plus, alternating shell index, the prime-modulo-four character, and a half-shell split. The Cartesian product contains 72 rows per beta and 144 rows total.

# Exact-anchor obstruction and repair

The first proposed proof anchor was the half-open interval $[1010342,1010355)$ at $Q=4$, whose shell is $\{5,7\}$. Exact rational evaluation found a zero geometry row for both beta values. This refutes the initial finite positivity assertion before any main-panel spectrum or signed response is evaluated.

We retain every main-panel parameter and replace only the proof-anchor rule. Starting at 1010342, scan consecutive 13-point intervals to the right and select the first interval having positive exact geometry for both beta 0 and 2. This unsigned, response-blind rule selects $[1010346,1010359)$, at offset four. Exact rational arithmetic verifies positive geometry and symmetry for both beta values. The certificate stores the failed anchor, the selection rule, the offset, and canonical matrix and geometry digests. This repair certifies a small finite witness only; it does not alter or validate the large numerical panel.

# Complete finite audit

Table [1](main.tex#L126){reference-type="ref" reference="tab:beta"} gives the complete census. Every row receives a true eigenvalue computation, while Schur and Frobenius values remain distinct upper envelopes.

<div id="tab:beta">

|  beta|  max spectrum|  spectral failures|     max Schur|  Schur failures|
|-----:|-------------:|------------------:|-------------:|---------------:|
|     0|  1.7829323182|                 18|  1.8516731225|              18|
|     2|  0.6741048980|                  6|  0.7000873871|               0|

: Census over the 72 rows for each beta.

</div>

The six beta=2 failures are exactly $$(a,1024,2048,1,\mathrm{all\mathchar`-plus}),\qquad
(a,1024,8192,1,\mathrm{all\mathchar`-plus})$$ for every $a\in\{1010001,1018021,1026041\}$. Hence the full finite failure key, not only an aggregate maximum, agrees with the TPC-368 template. Count 512 has no beta=2 spectral failure at any declared anchor; count 1024 has no beta=2 failure at $Q=512$; and no beta=2 row exceeds the Schur cap. The beta=0 control has 18 spectral and 18 Schur failures and is retained literally.

The third-family beta=2 maximum is $0.67410489800609708$, versus $0.674101905927736$ in TPC-368, a difference of $2.9920783610748458\times10^{-6}$. This close agreement is a finite descriptive fact. It proves neither origin uniformity nor convergence to a limiting constant.

# Independent and hostile verification

The producer accumulates each shell in increasing order. An independently written checker rebuilds the prime sieve and accumulates in descending shell order. It compares all 144 shell, weight, geometry, raw-matrix, normalized, eigenvalue, row-index, phase-census, failure-key, parent-comparison, and exact anchor fields. The audited outputs are

    TPC369_CERTIFICATE=PASS rows=144 beta2_rows=72
    TPC369_INDEPENDENT_CHECK=PASS rows=144 beta2_rows=72 beta2_violations=6
     baseline_beta0_violations=18

The adversarial checker rejects 30 mutations, including changes to the anchor-repair record. The local Bridge-B reruns producer, independent, and stress checks in normal and optimized Python modes, requires empty stderr, and requires byte-identical stdout.

# Claim firewall and route decision

    TPC369_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
    TPC369_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC369_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC369_THIRD_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC369_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC369_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC369_INITIAL_ANCHOR_POSITIVITY = REFUTED_SCOPED
    TPC369_REPAIRED_ANCHOR_RULE = PROVED_EXACT_FINITE
    TPC369_ORIGIN_UNIFORMITY = OPEN
    TPC369_WINDOW_UNIFORMITY = OPEN
    TPC369_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC369_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC369_GROWING_OPERATOR_BOUND = OPEN
    TPC369_SOURCE_UNIFORM_L2 = OPEN
    TPC369_ARITHMETIC_ADVANCE = NO
    TPC369_FIXED_POWER_CREDIT = 0
    TPC369_FULL_GATE_B = OPEN
    TPC369_TWIN_PRIME_RESULT = NONE

The strongest positive result is exact finite replication of the six-key pattern on a third predeclared family. The strongest obstruction is its persistence at count 1024 after another origin-phase change. The initial proof-anchor failure is a second, sharply scoped obstruction with a fully declared finite repair. None of these results proves a growing operator bound, source-valid normalization, source-uniform arithmetic $L^2$, prime- shell reassembly, fixed-power saving, an official route gate, or a twin-prime statement.

# Conclusion

Three response-blind finite origin families now exhibit the same beta=2 failure keys. The next minimal attack is to increase the window count to 2048 under a predeclared protocol; if the pattern changes, residue-phase localization is the natural fallback. Arithmetic advance remains `NO`, fixed-power credit remains zero, and full Gate B remains open.

`ROUND2_CLUE = TEST_COUNT_2048_ORIGIN_PHASE_OR_RESIDUE_PHASE`.

<!-- SOURCE_BODY_END -->
