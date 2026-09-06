# TPC-393: An Adversarial Holdout Audit of Scalar Normalization

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `95c85091ce74cf431bccd00631bae57dd1ca3833`

## Abstract

TPC-392 found one finite calibration-to-holdout forecast failure in a high-\(Q\) alternating-index/local-diagonal cell of a larger normalization panel. TPC-393 performs the smallest useful adversarial follow-up: a fresh coordinate-disjoint affine family, the same fixed band and four declared normalizations, and only the \(Q=8192\) all-plus control and alternating-index target. The 64-row certificate shows that the forecast failure does not recur: all four normalizations pass the \(3\%\) forecast cap for both laws. However, all four alternating-index cells fail the one-percent origin-spread diagnostic, all 32 rows fail the declared \(0.64\) spectral cap, and no row fails the Schur cap. These are finite \(c=1\) proxy observations with explicit claim firewalls, not an arithmetic, asymptotic, or twin-prime theorem.

# Question and claim boundary

TPC-392 exposed a scoped separation between a local-diagonal normalization and three scalar normalizations. Before interpreting that separation as a phase, one must ask whether it survives a fresh family chosen independently of the observed responses. TPC-393 answers this narrower replication question and also records the remaining origin-spread signal.

The status firewall is \[\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.\] The official Session evaluator files are absent from this checkout. The local proof package and Bridge-B artifact are therefore fail-closed evidence of finite consistency only; they cannot declare an official Route-A or Route-B pass.

# Finite proxy and predeclared panel

For \(p\in(Q,2Q]\), \(H=66\), and \(u,v\) in a finite interval, define \[\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}\] The row geometry and signed matrix are \[G(u)=\sum_p\sum_{v\in I}K_p(u,v)^2,
 \qquad M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v).\] The fixed band retains pairs of blocks whose indices differ by at most three.

The candidate grid is \[a_j=4200001+401j,\qquad 0\leq j<41,\] and the retained indices are \(0,10,20,30,40\). The first three origins \((4200001,4204011,4208021)\) are calibration origins at \(N=1024,1280\). The last two \((4212031,4216041)\) are used only at the terminal holdout \(N=1536\). The only prime-shell anchor is \(Q=8192\); the laws are all-plus and alternating-index. The four normalizations are

1.  local diagonal, \(M_\ell(u,v)/\sqrt{G(u)G(v)}\);

2.  pooled calibration scalar, with log extrapolation at \(1536\);

3.  current-origin scalar;

4.  frozen pooled calibration scalar at \(N=1024\).

All choices and roles were fixed before current responses were read. The TPC-392 code and certificate are a hashed parent reference only, and no parent response or slope is used in the current fit.

For a cell, let \(S_N\) be the mean fixed-band spectral diagnostic over the origins available at count \(N\). The finite forecast is \[\alpha=\frac{\log(S_{1280}/S_{1024})}{\log(1280/1024)},
 \qquad \widehat S_{1536}=S_{1024}(1536/1024)^\alpha,\] with a pass defined by \(|S_{1536}/\widehat S_{1536}-1|\leq0.03\). The separate origin-spread flag requires \[(\max S_N-\min S_N)/\operatorname{mean}(S_N)\leq0.01.\]

# Certification protocol

The producer sums the prime shell in ascending order. An independent checker does not import the producer: it rebuilds the same matrices in descending shell order and recomputes rows, normalization cells, and aggregates. The certificate is canonical JSON with a payload hash, exact parent provenance, and 64 rows in 8 cells. A rational 13-point anchor at \([4200001,4200014)\) and \(Q=8\) checks positive geometry and exact symmetry for both laws. A 25-case mutation suite attacks hashes, roles, row census, summary fields, the exact anchor, and the claim firewall.

The ordinary and optimized producer outputs agree exactly. The ordinary and optimized independent-checker outputs also agree exactly, as do both stress outputs. The release Bridge-B checker repeats these checks and locks every source, certificate, note, PDF, and compile log.

# Finite results

<div id="tab:results">

| normalization            | forecast pass |    max error | terminal mean |
| :----------------------- | ------------: | -----------: | ------------: |
| local diagonal           |           2/2 | 0.0101030096 |  0.3371554518 |
| pooled train scalar      |           2/2 | 0.0097142554 |  0.3442034715 |
| origin scalar            |           2/2 | 0.0110393577 |  0.3446551871 |
| frozen train-1024 scalar |           2/2 | 0.0097142554 |  0.3496082547 |

TPC-393 results on the predeclared 8-cell panel.

</div>

The forecast pass count is \(2/2\) for each normalization because the panel contains exactly the all-plus control and the alternating-index target. The largest error is \(0.011039357664235361\), well inside the declared cap. Thus the TPC-392 forecast anomaly is not reproduced on this fresh family. The terminal ordering is \[\text{frozen} > \text{origin} > \text{pooled} > \text{local diagonal},\] and the three scalar terminal means are respectively about \(1.03693\), \(1.02224\), and \(1.02090\) times the local-diagonal mean. The normalization level effect remains measurable even though the forecast separation does not.

The origin-spread result is law-specific. At each of \(N=1024,1280,1536\), exactly 4 of 8 cells pass the one-percent flag: all four all-plus cells pass, and all four alternating-index cells fail. This is a finite observation on five selected origins, not a source-uniform origin theorem.

The envelope diagnostics are asymmetric. Spectral-cap failures occur in all 32 rows (8 per normalization, all in the all-plus rows); Schur-cap failures occur in 0 of 32 rows. The latter is only a finite Schur diagnostic, not a growing-family Schur bound. Conversely, the universal spectral failure is a scoped obstruction to the particular \(0.64\) finite envelope, not a claimed asymptotic theorem.

# Interpretation and next clue

The strongest positive result is a response-blind, independently replayed forecast replication: no declared normalization exceeds the \(3\%\) terminal forecast cap in either law. The strongest negative result is that the alternating-index origin-spread instability survives while the forecast anomaly does not, together with the universal failure of the declared finite spectral cap. This separates two diagnostics that had been conflated in the earlier phase diagram.

The reusable structure is a minimal adversarial holdout: fresh affine coordinates, a fixed all-plus control, a targeted alternating law, frozen normalization definitions, exact parent hashes, reverse-order replay, and mutation rejection. The next clue is \[\texttt{ROUND2\_CLUE=TEST\_C1\_ORIGIN\_UNIFORMITY\_AFTER\_REPLICATION}.\] The next project should test that origin signal directly on another fresh, response-blind family while retaining the control and preserving the spectral obstruction in the ledger.

# Reproduction

All source, proof, certificate, notes, and Bridge-B files are stored in the TPC-393 project directory. The README lists ordinary and optimized producer, independent checker, stress, and Bridge-B commands. The release requires `paper/main.pdf` and `paper/paper.pdf` to be byte-identical.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
