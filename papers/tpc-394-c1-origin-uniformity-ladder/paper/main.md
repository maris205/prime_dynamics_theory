# TPC-394: A Same-Count Origin-Uniformity Ladder for a Finite $c=1$ Proxy

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 5, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-393 left a focused question: does its alternating-index origin-spread signal survive on another family after the normalization holdout? TPC-394 answers this with a response-blind eight-origin ladder at a common window length $N=1024$. All four declared normalizations are stable at the one-percent origin-spread level for the all-plus control, while all four fail for the alternating-index law, with relative spreads between $0.084824884787110394$ and $0.092863374514779065$. The calibration-to- holdout mean transfer remains within a predeclared three-percent cap in all eight cells. The finite $0.64$ spectral cap fails on all 32 all-plus rows and the Schur cap fails on no row. These are certified finite $c=1$ proxy facts; they do not establish source validity, a growing origin-uniform estimate, arithmetic $L^2$, Route-A/Route-B closure, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC-393 found that a high-$Q$ forecast anomaly from TPC-392 did not replicate, but that alternating-index origin spread remained above a one-percent diagnostic threshold. A direct same-count origin ladder is the smallest useful next test: it removes count-transfer from the primary statistic and asks whether the law-dependent signal survives a larger fresh family.

The status firewall is $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ The official Session evaluator files are absent from this checkout. The local proof package and Bridge-B artifact are therefore fail-closed evidence of finite consistency only; they cannot declare an official Route-A or Route-B pass.

# Finite proxy and frozen origin ladder

For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, set $$\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}$$ The row geometry and signed matrices are $$G(u)=\sum_p\sum_{v\in I}K_p(u,v)^2,
 \qquad M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v).$$ The fixed band retains block pairs at distance at most three. The candidate grid and selected origins are $$a_j=5000001+401j\quad(0\leq j<41),
 \qquad j\in\{0,5,10,15,20,25,30,35\}.$$ The first five origins are calibration and the last three are holdout. Every origin has $N=1024$, partitioned into eight blocks of length 128. We use $Q=8192$, the all-plus and alternating-index laws, and four fixed normalizations: local diagonal, pooled calibration scalar, current-origin scalar, and a first-calibration scalar frozen across origins.

For a cell, write $S(o)$ for the masked spectral diagnostic. The primary origin statistic is $$R_{\rm all}=\frac{\max_o S(o)-\min_o S(o)}{\operatorname{mean}_o S(o)},$$ with a one-percent pass cap. The secondary holdout transfer error is $$T=\frac{\operatorname{mean}_{o\in\mathrm{holdout}}S(o)}
 {\operatorname{mean}_{o\in\mathrm{calibration}}S(o)}-1,$$ with a three-percent cap. Both cohort roles and caps were fixed before the current responses were read.

# Certification protocol

The producer accumulates the prime shell in ascending order. An independent checker does not import the producer: it rebuilds the matrices in descending shell order and recomputes every row and aggregate. The canonical JSON certificate has 64 rows and 8 cells, exact TPC-393 parent hashes, and a rational 13-point anchor at $[5000001,5000014)$ with $Q=8$. The anchor checks positive geometry and exact symmetry for both laws. A 25-case mutation suite attacks hashes, roles, row census, summary fields, anchor data, and the claim firewall.

The producer and checker use float64 only for the finite matrix calculation; the opposite shell order is tolerated only at a small numerical replay tolerance. Ordinary and optimized runs are required to have identical outputs. The release Bridge-B checker locks all source, result, note, PDF, and compile-log artifacts.

# Finite results

<div id="tab:results">

| normalization            |  all-origin pass|    max spread|  transfer pass|  spectral failures|
|:-------------------------|----------------:|-------------:|--------------:|------------------:|
| local diagonal           |              1/2|  0.0848248848|            2/2|               8/16|
| pooled train scalar      |              1/2|  0.0928625707|            2/2|               8/16|
| origin scalar            |              1/2|  0.0928633745|            2/2|               8/16|
| frozen train-1024 scalar |              1/2|  0.0928625707|            2/2|               8/16|

: Origin-ladder summary. Each entry is a cell census over the two declared laws.

</div>

The complete panel has 64 rows and 8 cells. All four all-plus cells pass the one-percent origin rule. All four alternating-index cells fail it; their relative spreads, in local/pooled/origin/frozen order, are $$0.084824884787110394,\quad
0.092862570673886716,\quad
0.092863374514779065,\quad
0.092862570673886591.$$ For comparison, the all-plus spreads in the same order are $$\begin{gathered}
1.5006633030031748\times10^{-5},\quad
4.3100829567952307\times10^{-5},\\
2.2682851215503215\times10^{-5},\quad
4.3100829568062604\times10^{-5}.
\end{gathered}$$ Thus the finite split is strongly law-dependent and is not removed by any of the four normalization choices.

The holdout-transfer cap passes in all eight cells. Its largest absolute error is $0.027694160160074421$, so the observed obstruction is a same-count origin spread rather than a detected calibration-to-holdout level failure. The alternating/all-plus mean ratio is approximately $8.7\times10^{-4}$; this records finite cancellation in the selected proxy only.

The envelope diagnostics are asymmetric. The spectral cap fails in 32 of 64 rows, exactly the all-plus rows (8 per normalization), while no row fails the Schur cap. The Schur result is a finite diagnostic and not a growing Schur bound. Likewise, the spectral failure is a scoped obstruction to the chosen finite cap, not an asymptotic statement.

# Interpretation and next clue

The strongest positive result is a response-blind, independently replayed same-count control: all-plus origin magnitudes are stable at roughly $10^{-5}$–$10^{-4}$ across the eight-origin ladder under all four normalizations, and all holdout-transfer cells pass. The strongest obstruction is the normalization-invariant alternating-index spread of about nine percent. This supports a finite law-dependent obstruction hypothesis, not a source-uniform theorem.

The reusable structure is a same-count origin ladder with a law control, frozen normalization panel, explicit calibration/holdout roles, exact parent provenance, reverse-shell replay, and mutation testing. The next clue is $$\texttt{ROUND2\_CLUE=TEST\_C1\_ORIGIN\_CROSS\_FAMILY\_HOLDOUT}.$$ The next project should test whether this alternating origin obstruction transfers to another fresh affine family. Until a source-valid growing argument exists, no arithmetic power credit is assigned.

# Reproduction

All source, proof, certificate, notes, and Bridge-B files are stored in the TPC-394 project directory. The README lists ordinary and optimized producer, independent checker, stress, and Bridge-B commands. The release requires `paper/main.pdf` and `paper/paper.pdf` to be byte-identical.

<!-- SOURCE_BODY_END -->
