# TPC-397: Fine-Grid Replication of a Finite Interpolation Endpoint Transition

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `1374b4fc65fd288e3976bf9fdbf1653df17483d0`

## Abstract

TPC-396 sampled a finite origin-spread change coarsely at \(\lambda\in\{0,1/3,2/3,1\}\). We now fill the interior with \(\lambda\in\{3/4,5/6,11/12\}\) and repeat the endpoint on a fifth coordinate-disjoint family. The complete panel has 96 rows and 16 cells. All four normalizations pass the one-percent origin-spread rule at each of the three interior coefficients (12/16 cells), whereas all four fail at \(\lambda=1\), with spreads between \(0.0433995970\) and \(0.0485567529\). Every parent-relative calibration/holdout comparison and every within-family transfer passes the fixed three-percent cap; no spectral or Schur row fails. The rational anchor proves the interpolation identity exactly. These are finite proxy observations and a replication of endpoint localization, not a source-valid, asymptotic, arithmetic, Route-A/Route-B, or twin-prime theorem.

# Question and scope

The preceding TPC-396 audit found stable origin behavior through \(\lambda=2/3\) and an endpoint failure at \(\lambda=1\). The smallest next question is whether the failure appears at an interior coefficient on a fresh family. We use a response-blind finite panel to test that question.

The objects below are deliberately proxy objects. In particular, a fractional coefficient in a matrix interpolation is not asserted to be an arithmetic character, a prime weight, or a new signed law. The claim firewall remains \[\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.\] The official Session evaluator files are absent from this checkout; local proof and Bridge-B artifacts are fail-closed finite consistency evidence only.

# Finite construction

For \(p\in(Q,2Q]\), \(Q=8192\), put \(H=66\) and define \[\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\qquad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}\] Let \(G(u)=\sum_{p,v}K_p(u,v)^2\). If the primes are ordered increasingly, the two endpoint matrices are \[M_0=\sum_pK_p,\qquad
 M_1=\sum_p(-1)^{\operatorname{index}(p)}K_p.\] For the four declared probes we use the exact finite identity \[M_\lambda=(1-\lambda)M_0+\lambda M_1,
 \qquad \lambda\in\{3/4,5/6,11/12,1\}.\] The fixed \(c=3\) band retains pairs of the eight blocks whose block-index difference is at most three. We report the masked spectral diagnostic and, for an envelope check, the Schur diagnostic.

The current grid is \[a_j=6400001+401j\quad(0\leq j<41),
 \qquad j\in\{0,8,16,24,32,40\}.\] The calibration origins are \((6400001,6403209,6406417)\) and the holdouts are \((6409625,6412833,6416041)\). Every origin has \(N=1024\). We apply local diagonal, pooled-calibration, current-origin, and first-calibration frozen normalizations. All roles, coefficients, and caps were fixed before current readout.

# Statistics and certification

For a cell let \(S(o)\) denote its masked spectral value and define \[R=\frac{\max_oS(o)-\min_oS(o)}{\operatorname{mean}_oS(o)}.\] The origin cap is \(R\leq0.01\). Parent-relative calibration and holdout errors compare the corresponding cohort means with the same-coefficient linear interpolation of the two frozen TPC-396 endpoint means (‘`blend_0`‘ and ‘`blend_1`‘). Their cap is \(0.03\); the within-family holdout/calibration error has the same cap.

The producer sums the shell in ascending order. An independent checker sums in descending order and reconstructs all rows without importing producer functions. Parent code and certificate hashes are verified first. The certificate is canonical JSON with a row digest and payload digest. A rational 13-point anchor at \([6400001,6400014)\) with \(Q=8\) and shell \(\{11,13\}\) checks positive geometry, endpoint symmetry, and all four interpolation identities. The mutation suite contains 28 contract mutations.

# Results

Table [1](#tab:summary) reports the normalization-level aggregates. The entry “origin” counts the four interpolation coefficients; “cal” and “transfer” use the fixed three-percent caps.

<div id="tab:summary">

| normalization            | origin | cal | hold | transfer |    max \(R\) |
| :----------------------- | -----: | --: | ---: | -------: | -----------: |
| local diagonal           |    3/4 | 4/4 |  4/4 |      4/4 | 0.0485567529 |
| pooled train scalar      |    3/4 | 4/4 |  4/4 |      4/4 | 0.0433995970 |
| origin scalar            |    3/4 | 4/4 |  4/4 |      4/4 | 0.0434147460 |
| frozen train–1024 scalar |    3/4 | 4/4 |  4/4 |      4/4 | 0.0433995970 |

Finite TPC-397 panel: 96 rows and 16 cells.

</div>

At the law level, ‘blend\_3\_4’, ‘blend\_5\_6’, and ‘blend\_11\_12’ pass the origin cap for all four normalizations; ‘blend\_1’ passes none. Thus the origin-stable total is \(12/16\). The endpoint-1 origin spreads in local, pooled, origin, and frozen order are \[0.048556752880022216,\quad
0.043399597037557539,\quad
0.043414746028399794,\quad
0.043399597037557580.\] The largest parent-relative calibration error is \(0.017838648302480165\), and the largest parent-relative holdout error is \(0.024669590049843704\). The largest within-family transfer error is \(0.019666773775763424\). Thus all calibration, holdout, and transfer cells pass their fixed \(0.03\) caps. The finite spectral cap \(0.64\) fails on no row, and the Schur cap \(0.83\) also fails on no row.

The exact anchor reports positive geometry and exact symmetry for all four probes. Since the fractional matrices are constructed from the two endpoint matrices, the rational identity is proved at the anchor; this does not promote the float64 finite observations to an asymptotic assertion.

# Interpretation and next question

The strongest positive result is a replicated finite phase localization: all three interior samples \(\lambda=3/4,5/6,11/12\) preserve origin stability under every normalization, and all parent-relative and within-family transfer cells remain below the fixed cap. The strongest obstruction is the endpoint \(\lambda=1\), where every normalization loses origin stability. The justified statement is only that endpoint localization reappears on this fifth finite family; no universal threshold follows.

The reusable structure is a hash-locked endpoint interface, exact rational interpolation, a fresh same-count calibration/holdout family, independent reverse-order replay, and an explicit mutation firewall. The next natural experiment is a response-blind microgrid with coefficients closer to the endpoint, recorded as \[\texttt{ROUND2\_CLUE=TEST\_C1\_INTERPOLATION\_ENDPOINT\_MICROGRID}.\] Source-valid origin uniformity, growing operator control, arithmetic \(L^2\), Route closure, and the twin-prime endpoint remain open.

# Reproduction

The source, proof package, certificate, notes, and Bridge-B checker are stored under the TPC-397 project directory. The README gives ordinary and optimized commands for the producer, independent checker, stress test, and Bridge-B. The release requires ‘paper/main.pdf’ and ‘paper/paper.pdf’ to be byte-identical.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
