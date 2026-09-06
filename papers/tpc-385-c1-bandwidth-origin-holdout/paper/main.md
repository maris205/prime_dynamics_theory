# A Response-Blind Origin Holdout for a Finite Bandwidth--Normalization Phase

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- **Source date:** 4 September 2026
- **Repository source commit:** `a8e14036a6516d08a787b6e0af53141e3dc26b13`

## Abstract

We test whether the high-bandwidth phase observed in the preceding finite prime-shell dynamical audit transfers to new origins without using those origins to set the normalization. A fresh affine grid supplies five fixed origins: three calibration origins define a pooled geometry scalar and two later origins are held out. The complete response-blind panel has 160 rows, using bandwidths \(c=2,3\), shell anchors \(Q=2048,8192\), four declared sign laws, and local or calibration-pooled normalization. The four all-plus \(Q=8192\) holdout means differ from the locked parent forecasts by at most \(2.42\times 10^{-5}\) relatively, while the alternating control remains unstable at \(Q=2048\). This is a finite transfer certificate and a law-control obstruction; it supplies no arithmetic \(L^2\) estimate, power saving, or twin-prime conclusion.

# Question and finite object

The preceding TPC-384 phase diagram crossed four block-distance bandwidths and two normalization conventions on three origins. Its all-plus high-\(Q\) pooled values at \(c=2,3\) were \(0.63384010801912960\) and \(0.63888760360944985\). TPC-385 asks a narrower, response-blind question: do these two high-bandwidth values transfer to origins that are not used to define the pooled scalar?

For \(I_o=\{o,\ldots,o+511\}\) and primes \(Q<p\leq 2Q\), put \[B_p(u,t)=p(p/Q)^2\frac{66^2}{66^2+(u-t)^2}
\left({\bf1}_{p\mid u-t}-\frac{1}{p-1}\right)
{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}{\bf1}_{u\ne t}.\] The common row geometry is \[g_{o,Q}(u)=\sum_{t\in I_o}\sum_{Q<p\leq2Q}B_p(u,t)^2.\] Each declared law forms a signed shell matrix \(M_{o,Q,\ell}\). With block indices \(b(u)\), the reported matrices are \[{\bf1}_{|b(u)-b(t)|\leq c}\frac{M_{u,t}}{\sqrt{g(u)g(t)}}
 \quad\text{and}\quad
 {\bf1}_{|b(u)-b(t)|\leq c}\frac{M_{u,t}}{G_Q^{\rm train}},\] where \[G_Q^{\rm train}=\frac{1}{3\cdot512}
\sum_{o\in\mathcal C}\sum_{u\in I_o}g_{o,Q}(u),qquad
\mathcal C=(2000001,2004011,2008021).\] The holdout set is \(\mathcal H=(2012031,2016041)\).

# Frozen protocol and certification

All five origins are selected as indices \((0,10,20,30,40)\) in the affine grid \(a_j=2000001+401j\), with step \(401\). The role split, bandwidth menu, laws, and normalizations are frozen before any response, metric, or geometry score is read. The parent code and canonical parent certificate are SHA-256 locked. Thus the parent values are forecasts, not fitted parameters.

The producer constructs \[5\times2\times4\times2\times2=160\] rows and 32 cells. For every cell we record all-origin, calibration, and holdout spreads. The spectral and Schur caps are \(0.64\) and \(0.83\); the spread and forecast-error caps are both \(0.01\). A rational \(q=8\) anchor on \([2000001,2000014)\) has shell \(\{11,13\}\) and verifies positive geometry and exact symmetry for all four laws.

# Results

The calibration and holdout stability censuses are \(26/32\) and \(28/32\). All 160 rows are below both finite metric caps. The maximum holdout spread is \(0.033223638943350384\), attained by the alternating-index law at \((c,Q)=(3,2048)\) under local normalization. Hence the transfer is not law-uniform.

| cell                  |     parent forecast |        holdout mean |           relative error |
| :-------------------- | ------------------: | ------------------: | -----------------------: |
| \(c=2\), local        | 0.61397411407532332 | 0.61397983891736552 |  \(9.3242\times10^{-6}\) |
| \(c=2\), pooled train | 0.63384010801912960 | 0.63382483811179768 | \(-2.4091\times10^{-5}\) |
| \(c=3\), local        | 0.62079971051100025 | 0.62080564043709352 |  \(9.5521\times10^{-6}\) |
| \(c=3\), pooled train | 0.63888760360944985 | 0.63887214574940099 | \(-2.4195\times10^{-5}\) |

All-plus \(Q=8192\) holdout forecast audit.

All four forecast cells pass the predeclared one-percent error cap. This is a useful finite origin-holdout replication of the all-plus phase. It does not say that the cap persists with growing \(Q\), count, or origin, and it does not select the all-plus law as an arithmetic object.

# Claim boundary and route status

The paid finite statements are:

  - `PROVED`: the role split, coordinate disjointness, parent hash lock, and rational anchor;

  - `NUMERICALLY_CERTIFIED`: the 160-row certificate, 32-cell spread census, and four forecast comparisons;

  - `OPEN`: bandwidth monotonicity, law/origin/count uniformity, source-valid normalization, and a growing operator estimate;

  - `NO`: arithmetic advance, fixed-power credit, Route-B closure, and a twin-prime result.

The Session-named Route-A and Route-B evaluator files are absent from this checkout. The repository-local Bridge-B checker is therefore fail-closed evidence only. The next finite clue is `TEST_C1_HOLDOUT_COUNT_BANDWIDTH`: keep the high-bandwidth menu and test count transfer rather than retuning the origin normalization.

# Reproducibility

The repository contains the canonical JSON certificate, producer, independent reverse-shell checker, 25-mutation stress suite, proof and theorem ledgers, and a local Bridge-B checker. Reproduction uses Python with bytecode disabled and one BLAS/OpenMP thread; normal and optimized checker outputs are required to be byte-identical. The result is intentionally scoped to the declared finite dynamical proxy and carries no twin-prime claim.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
