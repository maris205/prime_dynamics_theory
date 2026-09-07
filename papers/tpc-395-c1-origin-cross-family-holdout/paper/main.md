# TPC-395: Cross-Family Holdout of a Finite $c=1$ Origin Obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 5, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-394 found a law-dependent origin-spread split on an eight-origin finite $c=1$ proxy family. TPC-395 freezes its cell means as a response-blind baseline and tests a third, coordinate-disjoint affine family with three calibration and three holdout origins, all at $N=1024$. All-plus remains origin-stable under four declared normalizations, while alternating-index fails the one-percent spread rule in every normalization, with spreads from $0.067101222970965949$ to $0.068267525703845117$. The new-family holdout means stay within $2.33\%$ of the frozen TPC-394 means, and all within-family holdout-transfer cells pass a $3\%$ cap. The finite spectral cap fails on all 24 all-plus rows and the Schur cap fails on no row. These are certified finite proxy observations, not a source-valid, asymptotic, arithmetic, Route, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC-394 directly reproduced the alternating-index origin-spread signal after TPC-393’s normalization holdout. The next minimal question is whether that signal is tied to one family. We therefore freeze TPC-394’s normalized cell means and perform a third-family cross-family holdout. The baseline is read only after exact parent hashes are checked and is not refit to current rows.

The status firewall is $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ The official Session evaluator files are absent from this checkout. Local proof and Bridge-B artifacts are fail-closed finite evidence only and cannot declare an official Route-A or Route-B pass.

# Finite proxy and cross-family protocol

For $p\in(Q,2Q]$, $H=66$, define $$\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}$$ Set $G(u)=\sum_{p,v}K_p(u,v)^2$ and $M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v)$. The fixed band retains block pairs whose eight block indices differ by at most three. We use $Q=8192$, the all-plus and alternating-index laws, and local diagonal, pooled calibration, current-origin, and first-calibration frozen normalizations.

The current candidate grid is $$a_j=5600001+401j\quad(0\leq j<41),
 \qquad j\in\{0,8,16,24,32,40\}.$$ The first three origins $(5600001,5603209,5606417)$ are calibration and the last three $(5609625,5612833,5616041)$ are holdout. Every origin has $N=1024$. For a cell, $S(o)$ is the masked spectral diagnostic and $$R=\frac{\max_o S(o)-\min_o S(o)}{\operatorname{mean}_o S(o)}$$ is the within-family origin spread. If $P$ is the matching TPC-394 all-origin mean, the cross-family error is cohort mean divided by $P$ minus one; the within-family transfer error is holdout mean divided by calibration mean minus one. The fixed caps are one percent, three percent, and three percent, respectively.

# Certification protocol

The producer sums the shell in ascending order. An independent checker does not import it and sums in descending order, reconstructing all 48 rows and eight cells. Parent code and certificate hashes are checked before the baseline is read. The canonical JSON certificate includes a rational 13-point anchor at $[5600001,5600014)$ with $Q=8$, where positivity and exact symmetry are checked for both laws. A 25-case mutation suite attacks hashes, roles, rows, summaries, anchor data, and claim fields. Normal and optimized runs are compared byte-for-byte at the output layer, and Bridge-B locks every release artifact.

# Finite results

| normalization            |  origin pass|    max spread|  cross holdout|  spectral fail|
|:-------------------------|------------:|-------------:|--------------:|--------------:|
| local diagonal           |          1/2|  0.0682675257|            2/2|           6/12|
| pooled train scalar      |          1/2|  0.0671052446|            2/2|           6/12|
| origin scalar            |          1/2|  0.0671012230|            2/2|           6/12|
| frozen train-1024 scalar |          1/2|  0.0671052446|            2/2|           6/12|

: TPC-395 cross-family holdout summary; each row aggregates the two declared laws.

The panel has 48 rows and 8 cells. All four all-plus cells pass the one- percent origin rule; all four alternating-index cells fail. The alternating spreads in local/pooled/origin/frozen order are $$0.068267525703845117,\quad
0.067105244599520317,\quad
0.067101222970965949,\quad
0.067105244599520331.$$ All-plus spreads are at most $5.2094472553133891\times10^{-5}$. Thus the law-dependent split transfers to a third family and persists under all four normalizations.

The cross-family calibration and holdout comparisons pass in all eight cells. The maximum absolute holdout error is $0.023289195722825839$, below the predeclared three-percent cap. New-family holdout-versus-calibration transfer also passes in all eight cells, with maximum absolute error $0.021220574691123151$. The finite spectral cap fails in 24 of 48 rows, exactly the all-plus rows; no row fails the Schur cap. These envelope statements are scoped to this finite proxy and do not imply a growing operator bound.

# Interpretation and next clue

The strongest positive result is cross-family level transfer: the new calibration and holdout means remain close to the frozen TPC-394 baseline in both laws and all four normalizations. The strongest obstruction is the alternating-index origin spread, which remains about seven percent on the new family while all-plus remains stable. This rules out a simple single-family or single-normalization explanation, but it does not identify a source-valid analytic mechanism.

The reusable structure is a hashed parent-mean interface, a fresh same-count family, explicit calibration/holdout roles, a law control, reverse-shell replay, and mutation testing. The next clue is $$\texttt{ROUND2\_CLUE=TEST\_C1\_SIGNED\_LAW\_INTERPOLATION}.$$ The next project should vary the signed law through a predeclared interpolation or sign-density panel to locate the mechanism behind the alternating spread. No arithmetic power credit is assigned.

# Reproduction

All source, proof, certificate, notes, and Bridge-B files are stored in the TPC-395 project directory. The README lists ordinary and optimized producer, independent checker, stress, and Bridge-B commands. The release requires `paper/main.pdf` and `paper/paper.pdf` to be byte-identical.

<!-- SOURCE_BODY_END -->
