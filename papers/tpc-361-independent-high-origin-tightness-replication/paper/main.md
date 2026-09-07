# Independent High-Origin Replication of a Finite Schur-Tightness Ledger

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We independently replicate a finite tightness audit for a normalized prime-shell operator on a new, geometry-selected high-origin panel. The selection scans 51 predeclared origins using only six unsigned mask-energy spreads at pilot count 256, then applies a deterministic separation rule. It selects $(313030,311166,321651)$. The post-selection replay contains 288 law rows: Schur and Frobenius envelopes are recorded everywhere, while true spectra are recorded for all four fixed sign laws at counts 256 and 512 and for all-plus at counts 1024 and 2048. The largest normalized Schur value is 0.80830232610282304, the largest recorded spectrum is 0.62690716242733457, and the largest spectral/Schur ratio is 0.77585950058997. The all-plus ladder has 12 increases, 36 decreases, and 6 flats over 54 adjacent transitions. These are finite, reproducible observations; they do not establish a growing operator estimate, an arithmetic $L^2$ theorem, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The preceding finite studies found a normalized cap and measurable slack in elementary Schur and Frobenius envelopes, but also found non-monotone count ladder behavior. The present question is whether that ledger survives an independently selected high-origin panel. The selection is fixed before any signed matrix or eigenvalue is evaluated. Thus the experiment tests finite transfer and implementation stability, not an asymptotic conjecture.

The Session-named official Route-A and Route-B evaluator files are not present in this checkout. We therefore report the local Bridge-B package as fail-closed finite evidence only. In particular, no source response is queried, no arithmetic reassembly is attempted, and no fixed-power credit is claimed.

# Finite operator

For an integer interval $I=[x,x+N-1]\cap\mathbb Z$, a shell parameter $Q$, and $s\in\{1,2\}$, define $$B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t},
 \label{eq:block}$$ where $Q<p\leq 2Q$ is prime. For a fixed law $\varepsilon$ on the shell, $A_\varepsilon=\sum_p\varepsilon_pB_p$. The unsigned geometry is $$G_u=\sum_{p}\sum_{t\in I}B_p(u,t)^2,
 \qquad A_\varepsilon^\#=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
 \quad D_G=\operatorname{diag}(G_u).
 \label{eq:normalization}$$ The four fixed laws are all-plus, alternating by shell index, the prime modulo-four character, and a half-shell split. The normalization uses no signed response or source vector.

For every finite real matrix $T$ we use the exact inequalities $$\lVert\,\cdot\,\rVert_2{T}\leq \max_u\sum_t|T(u,t)|,
 \qquad
 \lVert\,\cdot\,\rVert_2{T}\leq \left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
 \label{eq:envelopes}$$ Ratios to these envelopes are descriptive finite quantities, not proposed asymptotic constants.

# Frozen selection and replay

The candidate origins are $$x_j=310001+233j,\qquad 0\leq j\leq 50.$$ At $N=256$, each candidate is scored by the largest value of $\max(G)/\min(G)$ over $(Q,s)\in\{24,54,80\}\times\{1,2\}$. Candidates are sorted by decreasing score and then increasing origin. A candidate is kept only when it is at least 1536 away from every retained origin. The resulting ordered panel is $$(313030,\;311166,\;321651).$$ The top pilot score is 3.2949807763946679 at origin 313030; the next three scores in descending order are 3.0290850239243432, 3.006208135009345, and 2.9963861877986897. These numbers are included to make the selection audit replayable, but the signed replay never feeds back into the rule.

After selection, we use $N\in\{256,512,1024,2048\}$, $Q\in\{24,54,80\}$, $s\in\{1,2\}$, and the four laws. This yields $3\cdot4\cdot3\cdot2\cdot4=288$ rows. Spectra are calculated for all laws at the two short counts (144 rows) and for all-plus at the two long counts (36 rows), for 180 spectra in total. Every row records the literal shell, interval, geometry range, normalized Schur value, normalized Frobenius value, and a spectrum flag.

# Results

Table [1](main.tex#L122){reference-type="ref" reference="tab:summary"} gives the law-wise spectral summary. The missing long-count spectra for the three non-all-plus laws are intentional protocol choices, not imputed values.

<div id="tab:summary">

| law         |  rows|  spectral rows|  min spectrum|  max spectrum|  max $\rho_S$|
|:------------|-----:|--------------:|-------------:|-------------:|-------------:|
| all-plus    |    72|             72|      0.029889|      0.626907|      0.775860|
| alternating |    72|             36|      0.017456|      0.047343|      0.495175|
| mod-$4$     |    72|             36|      0.028453|      0.072081|      0.586181|
| half-split  |    72|             36|      0.021482|      0.065843|      0.499608|

: Recorded normalized spectra and envelope ratios.

</div>

Across all 288 rows, the normalized Schur maximum is $$0.80830232610282304,$$ and the normalized Frobenius maximum is 2.2149803188558002. Across the 180 recorded spectra, the maximum is 0.62690716242733457. The largest ratios to the Schur and Frobenius envelopes are, respectively, $$\max\rho_S=0.77585950058997,
 \qquad
 \max\rho_F=0.62120835204021907.$$ Thus the most saturated recorded row still has at least 0.22414049941003 relative Schur slack and 0.37879164795978093 relative Frobenius slack. The slack statement is restricted to the declared finite matrices.

At each of the 36 short-count settings, all-plus is the largest spectrum 30 times and the mod-$4$ law is largest 6 times; alternating and half-split do not win. This is evidence that all-plus is a useful finite stress law, while the six mod-$4$ wins prevent treating it as a universal proxy without an additional theorem.

The all-plus count ladder was also classified with a $10^{-6}$ guard. Of its 54 adjacent transitions, 12 increase, 36 decrease, and 6 are flat. Hence a monotone-decay claim is refuted on this declared ladder. This observation also blocks the tempting inference from a finite cap to a growing-origin operator bound.

# Independent audit and exact anchor

The producer writes a canonical JSON certificate. The independent checker rebuilds primes up to 50000, traverses every shell in reverse order, rebuilds the divisibility masks and all four signed matrices, and recomputes the 288 rows and 180 spectra without importing the producer or the locked base implementation. It also reruns the 51-candidate geometry scan and the separated selection. The producer, independent checker, and 15-mutation certificate stress test all pass in normal and optimized Python modes.

As a small exact anchor, at $Q=4$, $s=1$, the interval $[313060,313073]$ has prime shell $\{5,7\}$. Direct rational evaluation gives a symmetric matrix and strictly positive geometry at every coordinate. The certificate stores SHA-256 digests of the rational matrix and geometry lists, so this local check is reproducible without floating point.

# Claim firewall and route decision

The finite envelope inequalities in [\[eq:envelopes\]](main.tex#L81){reference-type="eqref" reference="eq:envelopes"} are proved exactly for finite matrices. The finite selection and its response independence are also exact consequences of the declared algorithm. The numerical caps, tightness ratios, law census, and transition census are certified only for this finite protocol.

    TPC361_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
    TPC361_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
    TPC361_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC361_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC361_TIGHTNESS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC361_LAW_UNIFORM_SHORT_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC361_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
    TPC361_GROWING_OPERATOR_BOUND = OPEN
    TPC361_SOURCE_UNIFORM_L2 = OPEN
    TPC361_ARITHMETIC_ADVANCE = NO
    TPC361_FIXED_POWER_CREDIT = 0
    TPC361_FULL_GATE_B = OPEN
    TPC361_TWIN_PRIME_RESULT = NONE

The official Session evaluator files are absent, so neither official Route A nor official Route B is declared passed. The local result is a useful finite obstruction/replication checkpoint, not progress through the missing arithmetic gate.

# Conclusion

The independent high-origin panel reproduces the finite normalized cap and its nontrivial envelope slack. It also reproduces the two limitations that matter for route planning: sign-law variation remains finite but nonzero, and the all-plus scale ladder is not monotone. The next defensible step is a new scale-or-shell stress that explicitly tests these interactions. A source-uniform arithmetic $L^2$ statement, a growing masked-operator bound, Route-B reassembly, and the twin-prime endpoint remain open.

`TPC361_ARITHMETIC_ADVANCE=NO`, `TPC361_FIXED_POWER_CREDIT=0`, `TPC361_FULL_GATE_B=OPEN`.

<!-- SOURCE_BODY_END -->
