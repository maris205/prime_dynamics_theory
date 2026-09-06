# TPC-400: Third-Family Replication of a Finite C1 Endpoint Microgrid

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `9a2bab8588f5a81316ac3c6b6435e691e84ae8b7`

## Abstract

TPC-399 found a finite separation between same-law mean transfer and origin uniformity: the probes through \(\lambda=31/32\) were origin-stable, while the endpoint \(\lambda=1\) was not. TPC-400 tests the next response-blind question on a third coordinate-disjoint affine family. Its 96-row panel compares each current same-law cohort mean with a hash-locked all-origin mean from TPC-399. Every one of the 16 law/normalization cells passes both the three-percent calibration and holdout transfer caps, and all 16 within-family transfers pass. At the same time, \(\lambda=1\) fails the one-percent origin-spread rule in all four normalizations, with maximum spreads between \(0.0536045\) and \(0.0538907\). The endpoint calibration discrepancy approaches the declared cross-family boundary but remains below it. This is finite replication and obstruction evidence, not an arithmetic, asymptotic, Route-A/Route-B, or twin-prime theorem.

# Question and claim boundary

TPC-399 supplied a frozen same-law interface from a second fresh family and showed that close cohort means can coexist with endpoint origin instability. The present paper asks whether that split survives on a third family, with all roles and probes fixed before the new response is read.

Every object below is finite. In particular, a fractional coefficient in a matrix interpolation is not asserted to be an arithmetic character, a prime sign law, or a source weight. The claim firewall is \[\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.\] The official Session evaluator files are absent from this checkout, so the local proof, independent checker, and Bridge-B artifacts provide finite consistency evidence only.

# Finite construction

For a prime \(p\in(Q,2Q]\), set \(Q=8192\), \(H=66\), exponent one, and \(\beta=2\). The component used in the certificate is \[\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\qquad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}\] Let \[G(u)=\sum_{p\in(Q,2Q]}\sum_v K_p(u,v)^2.\] If the shell is indexed increasingly, define \[M_+=\sum_p K_p,\qquad
 M_{\rm alt}=\sum_p(-1)^{\operatorname{index}(p)}K_p.\] The four probes are the exact finite combinations \[M_\lambda=(1-\lambda)M_+ + \lambda M_{\rm alt},\qquad
 \lambda\in\left\{\frac78,\frac{15}{16},\frac{31}{32},1\right\}.\] This is a finite linear-algebra identity, not an arithmetic interpolation theorem.

The response-blind third-family grid is \[a_j=7600001+401j,\quad 0\leq j<41,\] with selected indices \((0,8,16,24,32,40)\) and origins \[7600001,\ 7603209,\ 7606417,\ 7609625,\ 7612833,\ 7616041.\] The first three are calibration origins and the last three are holdout origins. Every window has \(N=1024\) points, split into eight blocks of length 128; the fixed \(c=3\) band retains block pairs at distance at most three.

# Diagnostics and frozen parent interface

Four normalizations are recorded: local diagonal, pooled calibration scalar, current-origin scalar, and first-calibration frozen scalar. If \(S_\lambda(o)\) denotes the masked spectral diagnostic, its origin spread is \[R_\lambda=\frac{\max_o S_\lambda(o)-\min_o S_\lambda(o)}
 {\operatorname{mean}_o S_\lambda(o)}.\] The origin cap is \(R_\lambda\leq0.01\). Finite spectral and Schur caps are 0.64 and 0.83.

TPC-399 is imported only through its hash-locked code and canonical certificate. For each law and normalization, let \(B^{(399)}_\lambda\) be its recorded all-origin mean. The current cohort errors are \[E_{\rm cal}=\frac{\operatorname{mean}_{o\in\mathcal C}S_\lambda(o)}
 {B^{(399)}_\lambda}-1,\qquad
 E_{\rm hold}=\frac{\operatorname{mean}_{o\in\mathcal H}S_\lambda(o)}
 {B^{(399)}_\lambda}-1.\] Both use cap 0.03. The within-family error is \[E_{\rm within}=\frac{\operatorname{mean}_{o\in\mathcal H}S_\lambda(o)}
 {\operatorname{mean}_{o\in\mathcal C}S_\lambda(o)}-1,\] also tested at cap 0.03. No segment or threshold fit is performed.

The parent locks are

code: 6b65f30fd6aa3f54e58596635a1248c892c01eb71d4156a37578bb71a1079d2b
certificate: 6f632add733947838c4268969748068633b2b85fadbd8fba7c21a146d98b7896

The producer accumulates the shell in ascending order. An independent checker accumulates it in descending order and recomputes all aggregates. At the exact anchor \([7600001,7600014)\) with \(Q=8\) and shell \(\{11,13\}\), exact ‘Fraction’ arithmetic verifies positive geometry, symmetry, and all four interpolation identities.

# Results

<div id="tab:summary">

| normalization            | origin | cross-cal | cross-hold | within |    max \(R\) |
| :----------------------- | -----: | --------: | ---------: | -----: | -----------: |
| local diagonal           |    3/4 |       4/4 |        4/4 |    4/4 | 0.0536044969 |
| pooled train scalar      |    3/4 |       4/4 |        4/4 |    4/4 | 0.0538721097 |
| origin scalar            |    3/4 |       4/4 |        4/4 |    4/4 | 0.0538906727 |
| frozen train–1024 scalar |    3/4 |       4/4 |        4/4 |    4/4 | 0.0538721097 |

TPC-400 finite panel. Counts are across the four laws.

</div>

The interior laws \(7/8\), \(15/16\), and \(31/32\) pass the one-percent origin-spread cap under all four normalizations. The endpoint law \(1\) passes none, giving 12 of 16 origin-stable cells. The maximum absolute cross-family calibration errors, in local, pooled, origin, and frozen order, are \[0.0242418805,\quad 0.0277738760,\quad
0.0277699591,\quad 0.0277815666,\] and the corresponding holdout maxima are \[0.0001317872,\quad 0.0024016863,\quad
0.0023850574,\quad 0.0024091870.\] All 16 cells pass both cross-family tests. The maximum absolute within-family transfer errors in the same order are \(0.0236215933\), \(0.0246865486\), \(0.0246990112\), and \(0.0246865486\); all 16 pass. No spectral or Schur row fails among the 96 rows. The spectral and Schur values are reproducible float64 observations; no interval eigenvalue enclosure or propagated rounding certificate is claimed.

# Interpretation and route ledger

The strongest positive result is a response-blind third-family replication: the frozen TPC-399 same-law means transfer to the current family in every law, normalization, and cohort role at the declared three-percent scale. The strongest obstruction is that the endpoint remains origin-unstable, with a 5.36–5.39 percent spread. The endpoint calibration error is close to the cross-family cap, so the finite panel does not justify a stronger uniformity claim.

The reusable structure is a direct hash-locked same-law interface, exact finite matrix interpolation, coordinate-disjoint calibration/holdout families with explicit prior-interval checks, reverse-order replay, and separate origin and transfer gates. The next response-blind clue is \[\texttt{ROUND2\_CLUE=TEST\_C1\_ENDPOINT\_MICROGRID\_FOURTH\_FAMILY\_REPLICATION}.\]

The theorem ledger is intentionally conservative:

| status                 | finite scope                                                |
| :--------------------- | :---------------------------------------------------------- |
| PROVED\_EXACT\_FINITE  | selection, disjointness, hashes, anchor identities          |
| NUMERICAL\_OBSERVATION | 96 float64 rows and stated aggregate observations           |
| OPEN                   | source-valid uniformity, growing bounds, arithmetic \(L^2\) |
| NONE                   | arithmetic advance, fixed-power credit, twin-prime result   |

Route-A is not officially evaluated because its Session evaluator is absent; Route-B remains open. The certificate makes no claim about a source-uniform estimate, an arithmetic \(L^2\) bound, a growing operator, or the twin-prime conjecture.

# Reproduction

The project contains the required README, code, experiments, results, notes, proof package, and Bridge-B artifacts. The canonical certificate is `results/tpc400_certificate.json`; the release contains byte-identical `paper/main.pdf` and `paper/paper.pdf`. The README lists normal and optimized commands for all checks.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
