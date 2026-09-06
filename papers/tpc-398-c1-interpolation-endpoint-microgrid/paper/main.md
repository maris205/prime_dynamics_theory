# TPC-398: Endpoint Microgrid on a Fresh Finite \(c=1\) Family

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `1374b4fc65fd288e3976bf9fdbf1653df17483d0`

## Abstract

TPC-397 left a finite transition panel unresolved between the interpolation coefficients \(\lambda=3/4\) and \(\lambda=1\). TPC-398 samples that segment at \(7/8\), \(15/16\), and \(31/32\), together with the endpoint, on a fresh coordinate-disjoint affine family. The response-blind panel contains 96 rows and 16 origin/law/normalization cells. All four normalizations pass the one-percent origin-spread rule at the three interior coefficients (12 of 16 cells), while the endpoint fails in all four normalizations, with spreads between 0.0734022 and 0.0756007. A frozen scalar interpolation of TPC-397’s two segment endpoints passes the three-percent cohort test at \(7/8\), \(15/16\), and \(1\), but fails at \(31/32\) by about 4.5 percent. Every within-family transfer passes, and no finite spectral or Schur row fails. These are certified finite proxy observations, not an arithmetic, asymptotic, Route-A/Route-B, or twin-prime theorem.

# Question and scope

The preceding TPC-397 audit replicated a finite endpoint transition: several interior probes were origin-stable while the alternating endpoint was not. The next minimal question is whether a finer, predeclared grid can localize the behavior and whether origin stability agrees with transfer to a frozen parent baseline.

All objects in this paper are finite proxy objects. A fractional coefficient in a matrix interpolation is not asserted to be an arithmetic character, a prime weight, or a new signed law. The claim firewall is \[\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.\] The official Session evaluator files are absent from this checkout, so the local proof and Bridge-B artifacts provide finite consistency evidence only.

# Finite construction

For a prime \(p\in(Q,2Q]\), with \(Q=8192\), \(H=66\), exponent one, and \(\beta=2\), define \[\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\qquad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}\] Let \(G(u)=\sum_{p,v}K_p(u,v)^2\). Ordering the shell increasingly gives the endpoint matrices \[M_{+}=\sum_pK_p,\qquad
 M_{\mathrm{alt}}=\sum_p(-1)^{\operatorname{index}(p)}K_p.\] TPC-398 forms the exact finite probes \[M_\lambda=(1-\lambda)M_{+}+\lambda M_{\mathrm{alt}},
 \qquad \lambda\in\{7/8,15/16,31/32,1\}.\] The identity is a linear-algebra construction. It does not identify a source law for the fractional probes.

The coordinate family is \[a_j=6800001+401j,\quad 0\leq j<41,\] with selected indices \((0,8,16,24,32,40)\). The first three origins, \(6800001,6803209,6806417\), are calibration; the last three, \(6809625,6812833,6816041\), are holdout. Each origin has \(N=1024\), eight blocks of length 128, and the fixed \(c=3\) band retains block pairs at distance at most three.

# Diagnostics and frozen parent interface

We use local diagonal, pooled-calibration, current-origin, and first- calibration frozen scalar normalizations. If \(S_\lambda(o)\) is the masked spectral diagnostic at origin \(o\), the declared origin spread is \[R_\lambda=\frac{\max_oS_\lambda(o)-\min_oS_\lambda(o)}
 {\operatorname{mean}_oS_\lambda(o)}.\] The origin cap is \(R_\lambda\leq0.01\). We also record the Schur row-sum diagnostic, with finite caps 0.64 and 0.83 for spectral and Schur values.

For cross-family comparison, TPC-397’s code and canonical certificate are hash-locked before current readout. Its all-origin means for the two segment endpoints ‘blend\_3\_4’ and ‘blend\_1’ define a response-blind scalar parent: \[t=\frac{\lambda-3/4}{1/4},\qquad
 B_\lambda=(1-t)B_{3/4}+tB_1.\] Calibration and holdout cohort means are divided by \(B_\lambda\) and reduced by one; the cap is 0.03. This is a frozen modeling baseline, not a theorem that the diagnostic is linear in \(\lambda\).

The producer accumulates primes in ascending order. An independent checker accumulates them in descending order and reconstructs all rows without importing producer functions. A rational 13-point anchor on \([6800001,6800014)\), with \(Q=8\) and shell \(\{11,13\}\), checks positive geometry, symmetry, and exact interpolation identities. The certificate is canonical JSON with row and payload hashes; a 28-case mutation suite tests its contract.

# Results

<div id="tab:summary">

| normalization            | origin | parent-cal | parent-hold | transfer |    max \(R\) |
| :----------------------- | -----: | ---------: | ----------: | -------: | -----------: |
| local diagonal           |    3/4 |        3/4 |         3/4 |      4/4 | 0.0734022263 |
| pooled train scalar      |    3/4 |        3/4 |         3/4 |      4/4 | 0.0755780570 |
| origin scalar            |    3/4 |        3/4 |         3/4 |      4/4 | 0.0756006542 |
| frozen train–1024 scalar |    3/4 |        3/4 |         3/4 |      4/4 | 0.0755780570 |

TPC-398 finite panel. Counts use the four laws; parent and transfer caps are three percent.

</div>

At the law level, ‘blend\_7\_8’, ‘blend\_15\_16’, and ‘blend\_31\_32’ pass the origin cap under all four normalizations; ‘blend\_1’ passes none. Thus 12 of 16 cells are origin-stable. The endpoint-1 spreads in local, pooled, origin, and frozen order are \[0.073402226295029099,\quad
0.075578056988127071,\quad
0.075600654173434007,\quad
0.075578056988126863.\]

The parent-relative pass counts are 3 of 4 for calibration and 3 of 4 for holdout under every normalization. In each case ‘blend\_31\_32’ is the failing law: its largest absolute calibration discrepancy is 0.0446288 and its largest holdout discrepancy is 0.0449715. The endpoint ‘blend\_1’ is within the parent cohort cap, with calibration discrepancies below 0.0280 and holdout discrepancies below 0.0031, but it has the large origin spread shown above. All 16 within-family transfers pass; their largest absolute error is 0.0256693. There are zero spectral failures and zero Schur failures among the 96 rows.

The exact anchor has positive geometry, symmetric endpoint matrices, and true interpolation identities for all four rational coefficients. This exact finite check does not turn the float64 panel into an asymptotic statement.

# Interpretation and route ledger

The strongest positive result is a finer finite localization of the origin diagnostic: stability persists through \(31/32\) on the new family. The strongest obstruction is a diagnostic split. At \(31/32\), origin stability survives but the parent-relative cohort comparison misses by roughly 4.5 percent; at \(1\), the parent endpoint comparison is close but origin stability fails by 7.3–7.6 percent. These observations do not select a universal transition coefficient.

The reusable structure is a hash-locked segment endpoint interface, exact finite matrix interpolation, a predeclared calibration/holdout family, reverse-order replay, and separate gates for origin spread and parent transfer. The next response-blind test is a second fresh-family replication of this endpoint microgrid: \[\texttt{ROUND2\_CLUE=TEST\_C1\_ENDPOINT\_MICROGRID\_CROSS\_FAMILY\_REPLICATION}.\]

The theorem ledger remains conservative: \[\begin{array}{ll}
\mathrm{PROVED\_EXACT\_FINITE:}&\text{selection, disjointness, hashes, anchor identity;}\\
\mathrm{NUMERICALLY\_CERTIFIED:}&\text{96 finite rows and stated aggregate flags;}\\
\mathrm{OPEN:}&\text{source-valid uniformity, growing bounds, arithmetic }L^2;\\
\mathrm{NONE:}&\text{arithmetic advance, fixed-power credit, twin-prime result.}
\end{array}\] Route-A is not officially evaluated because its Session evaluator is absent; Route-B remains open.

# Reproduction

All source, notes, proof/checker files, certificate, and the release PDF are under the TPC-398 project directory. The README lists ordinary and optimized commands for the producer, independent checker, mutation stress, and Bridge-B. The release requires ‘paper/main.pdf’ and ‘paper/paper.pdf’ to be byte-identical.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
