# A Prime-Shell Tilt Phase Diagram for a Finite Twin-Prime Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding TPC-362 shell ladder found that a finite normalized spectral cap, valid through $Q=80$, first fails at $Q=128$. TPC-363 showed that the failure survives two targeted five-percent principal restrictions. We now test a different finite modeling choice: multiply the literal block for $Q<p\leq 2Q$ by $(p/Q)^\beta$ and rebuild the diagonal normalizer from the corresponding weighted square energy. On the frozen high-origin panel $(313030,311166,321651)$, a complete replay of five integer tilts, four sign laws, two counts, four shell anchors, and two kernel exponents gives 960 law rows. The spectral-cap failure counts for $\beta=-2,-1,0,1,2$ are respectively $63,36,30,30,0$. Thus $\beta=2$ is a finite phase point with maximum normalized spectrum $0.61628753962786131$ and minimum effective shell fraction $0.66938300094026681$. This is a scoped finite phase diagram and a modeling observation, not an asymptotic operator bound, an arithmetic estimate, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

TPC-362 isolated a shell-scale obstruction: the inherited normalized cap $0.64$ held on the frozen panel for $Q\leq80$ but failed at larger shells. TPC-363 ruled out two simple localization explanations on the same panel. The next minimal question is whether a transparent relative shell weighting changes the finite geometry at all. We use the dimensionless family

$$w_{p,\beta}=\left(\frac pQ\right)^\beta,
        \qquad \beta\in\{-2,-1,0,1,2\},$$

and report the complete menu, rather than presenting the best member as an independent prediction. The panel is reused deliberately: this paper maps the finite phase diagram, while the next holdout must test any apparent repair. No source response, source profile, adaptive sign, or arithmetic reassembly is used. The official Session-named Route-A and Route-B evaluator files are absent from this checkout; local Bridge-B is fail-closed evidence only.

# Weighted finite operator

For $I=[x,x+N-1]\cap\mathbb Z$, define the literal masked block $$B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
\left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
{\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
\label{eq:block}$$ For a fixed sign law $\varepsilon$, the tilted operator and its geometry are $$A_{\beta,\varepsilon}=\sum_{Q<p\leq2Q}\varepsilon_p w_{p,\beta}B_p,
\qquad
G_{\beta,u}=\sum_{Q<p\leq2Q}\sum_{t\in I}
                 (w_{p,\beta}B_p(u,t))^2.
\label{eq:weighted}$$ The normalized matrix is the symmetric congruence $$A_{\beta,\varepsilon}^{\#}=
D_{G_\beta}^{-1/2}A_{\beta,\varepsilon}D_{G_\beta}^{-1/2},
\qquad D_{G_\beta}=\operatorname{diag}(G_{\beta,u}).
\label{eq:norm}$$ All terms in $G_{\beta,u}$ are rational squares for the integer menu. The certificate checks positivity on every declared row. The exact finite envelopes used throughout are $$\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}$$

The four fixed laws are all-plus, alternating shell index, the prime modulo-four character, and a half-shell split. The protocol has $3\cdot2\cdot4\cdot2\cdot4\cdot5=960$ law rows. The value $0.64$ is only an inherited finite working cap; it is not asserted uniformly in $Q$.

# Phase diagram

Table [1](main.tex#L107){reference-type="ref" reference="tab:phase"} gives the full beta census. The effective shell count is $(\sum_pw_p^2)^2/\sum_pw_p^4$, divided by the literal shell cardinality; it is a diagnostic, not a new normalization theorem.

<div id="tab:phase">

|  $\beta$|  max spectrum|  cap failures|  max Schur|  min effective fraction|
|--------:|-------------:|-------------:|----------:|-----------------------:|
|     $-2$|     2.8500559|            63|  2.9846691|               0.5844197|
|     $-1$|     2.2811632|            36|  2.3887820|               0.8480857|
|      $0$|     1.6398895|            30|  1.7172665|               1.0000000|
|      $1$|     1.0539301|            30|  1.1036233|               0.8741246|
|      $2$|     0.6162875|             0|  0.6453140|               0.6693830|

: Complete finite phase diagram over 192 rows per tilt.

</div>

The beta=0 row reproduces the inherited literal normalization: 30 of its 192 rows exceed the cap, including the high-shell failures identified by TPC-362. The complete menu has exactly one zero-failure member, beta=2. Its largest normalized spectrum is at $Q=512$ and remains below $0.64$; its largest normalized Schur value is also below the inherited Schur working cap $0.83$. The effective fraction remains at least $0.6693830$, so the finite result is not described as retaining a single prime.

Table [2](main.tex#L137){reference-type="ref" reference="tab:q"} separates the inherited beta=0 normalization from the beta=2 phase point by shell. Each shell column aggregates all three origins, two counts, two exponents, and four laws, hence 48 rows.

<div id="tab:q">

|     |              |          |              |          |     |
|----:|-------------:|---------:|-------------:|---------:|----:|
|     |              |          |              |          |     |
|  $Q$|  max spectrum|  failures|  max spectrum|  failures|     |
|   80|     0.6269072|         0|     0.3254845|         0|     |
|  128|     1.3238826|         6|     0.5444779|         0|     |
|  256|     1.5433707|        12|     0.5820044|         0|     |
|  512|     1.6398895|        12|     0.6162875|         0|     |

: Shell-scale comparison for the baseline and the beta=2 phase point.

</div>

The other menu members do not repair the phase diagram: their total failure counts are 63, 36, and 30 for beta $-2,-1,1$, respectively. This direction dependence is itself useful evidence. It says that a finite cap can be strongly affected by the chosen shell geometry, but does not identify which normalization is legitimate for the arithmetic source problem.

# Exact and independent checks

The finite algebra is straightforward but important. Positive weights preserve symmetry of each masked block; the weighted geometry is a sum of nonnegative squares; and positivity makes the displayed diagonal congruence well-defined. Schur and Frobenius inequalities then apply to every finite matrix without an asymptotic assumption.

At $Q=4$, exponent one, the exact interval $[313060,313073]$ has shell $\{5,7\}$. Exact rational matrix and geometry digests are retained for all five beta values. The forward producer builds the 960 rows in increasing prime order. An independent checker rebuilds the sieve, masks, weights, four laws, geometry, envelopes, and all true spectra in reverse shell order. It compares the row keys, shell weights, effective counts, matrix metrics, phase census, and exact anchors. An 18-mutation stress test rejects altered protocols, row counts, phase counts, and claim-firewall values. Normal and optimized executions are required to emit empty stderr and byte-identical stdout by the local Bridge-B checker.

# Claim firewall and route decision

    TPC364_WEIGHTED_BLOCK_DEFINITION = PROVED_EXACT_FINITE
    TPC364_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC364_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_960_ROWS
    TPC364_PHASE_DIAGRAM = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC364_BETA2_PANEL_CAP_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC364_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC364_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC364_GROWING_OPERATOR_BOUND = OPEN
    TPC364_SOURCE_UNIFORM_L2 = OPEN
    TPC364_ARITHMETIC_ADVANCE = NO
    TPC364_FIXED_POWER_CREDIT = 0
    TPC364_FULL_GATE_B = OPEN
    TPC364_TWIN_PRIME_RESULT = NONE

The strongest positive result is a finite, all-law beta=2 cap repair on the reused panel. The strongest obstruction is selection dependence: the phase point was identified from a finite menu on the same panel, and the weighting has not been shown source-valid. Therefore no Route-A or Route-B gate is closed, no fixed power is credited, and no twin-prime conclusion follows. The next defensible experiment is a response-blind disjoint holdout for the predeclared beta=2 rule. A transfer failure must be recorded as an obstruction rather than used to refit beta.

# Conclusion

TPC-364 maps the next branch of the TPC route. A simple dimensionless prime-shell tilt changes the finite normalized operator substantially: the positive tilt beta=2 removes the observed cap failures through $Q=512$ on the frozen panel, while the rest of the symmetric integer menu does not. This is valuable as a candidate and as a boundary marker, but its scientific status is deliberately limited to the displayed finite certificate. The arithmetic source norm, a growing operator estimate, and the twin-prime endpoint remain open.

`TPC364_ARITHMETIC_ADVANCE=NO`, `TPC364_FIXED_POWER_CREDIT=0`, `TPC364_FULL_GATE_B=OPEN`.

<!-- SOURCE_BODY_END -->
