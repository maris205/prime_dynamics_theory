# TPC-383: Local and Pooled Normalization in a Finite \(c=1\) Panel

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang\\School of Mathematics and Statistics, HUST\\Wuhan, China
- **Source date:** September 4, 2026
- **Repository source commit:** `75e23fe44efae6c677b440ed8149eaacd31e2323`

## Abstract

We test whether the finite origin stability observed in a normalized prime-shell operator is caused by row-wise diagonal whitening. A fresh, response-blind panel with \(N=512\), three origins, three shell anchors, and four fixed laws is evaluated using both local diagonal normalization and a common pooled scalar geometry. The all-plus high-\(Q\) origin spread remains below one percent under both choices, while its pooled mean shifts upward by \(3.6457251256851203\%\). The alternating-index control remains unstable, with pooled high-\(Q\) spread \(10.104585338571119\%\). This is a finite normalization audit and does not identify an arithmetic source law or prove a twin-prime statement.

# Question

TPC-382 found a small all-plus magnitude spread across two protocol-matched origin families, but used row-wise normalization. We therefore ask whether the origin-stability shape survives a common scalar normalization, while tracking any absolute calibration shift. The experiment is deliberately finite and response-blind; all four laws are retained as controls.

# Protocol

The candidate grid is \(a_j=1600001+401j\), with indices \(0,20,40\) fixed before any response or metric is read. Thus the origins are \((1600001,1608021,1616041)\). Each window has 512 points in four contiguous 128-point blocks. We use the inherited block-distance-one mask, exponent one, beta two, height 66, and \(Q\in\{512,2048,8192\}\). The laws are all-plus, alternating-index, mod-4 character, and half-split.

Let \(M_{o,Q,\ell}\) be the raw law matrix and \(g_{o,Q}(i)\) its common square-energy geometry. The two matrices are \[A^{\rm loc}_{ij}=M_{ij}/\sqrt{g(i)g(j)},\qquad
 A^{\rm pool}_{ij}=M_{ij}/G_Q,\] where \(G_Q\) is the mean of all coordinate geometries over the three fixed origins. The same band mask is applied in both cases. For each law, \(Q\), and normalization, the reported origin spread is \[\Delta=(\max_o s_o-\min_o s_o)/(\tfrac13\sum_o s_o),\] with the cap \(\Delta\leq0.01\) fixed in advance.

All current endpoints avoid the prior coordinate panels. The exact q=8 anchor \([1600001,1600014)\) has shell \([11,13]\); rational arithmetic verifies positive geometry and symmetry for every law.

# Results

The local and pooled all-plus high-\(Q\) spreads are respectively \(1.1394111498671383\times10^{-5}\) and \(4.6321361430822112\times10^{-5}\), both far below the one-percent cap. The pooled scalar is therefore not merely a relabelling: the all-plus high-\(Q\) mean changes by \[\frac{m_{\rm pool}-m_{\rm loc}}{m_{\rm loc}}
 =0.036457251256851203.\] The complete stability census is:

| law               | local stable cells | pooled stable cells |
| :---------------- | :----------------: | :-----------------: |
| all-plus          |        3/3         |         3/3         |
| alternating-index |        0/3         |         0/3         |
| mod-4 character   |        3/3         |         3/3         |
| half-split        |        3/3         |         3/3         |

Thus both normalizations give 9/12 stable cells, but this agreement is law-dependent. At high \(Q\), the pooled alternating-index spread is \(0.10104585338571119\), the largest in the panel. The result supports a limited shape-versus-calibration separation: all-plus origin stability transfers, while absolute magnitude depends on normalization.

# Verification and boundary

The producer and a direct reverse-shell independent checker recompute all 72 rows in normal and optimized Python modes. A 25-field adversarial suite rejects altered protocol, row, phase, firewall, and clue fields. The local Bridge-B checks canonical certificate identity, exact anchor data, and byte-identical normal/optimized outputs. The official Session evaluator files are absent, so this is not an official Route-A or Route-B verdict.

| claim                                             | status                         |
| :------------------------------------------------ | :----------------------------- |
| predeclared panel, mask, and normalization family | PROVED FINITE                  |
| 72-row local/pooled replay                        | NUMERICALLY CERTIFIED / FINITE |
| all-plus high-\(Q\) transfer                      | NUMERICALLY CERTIFIED / FINITE |
| normalization magnitude shift                     | NUMERICALLY CERTIFIED / FINITE |
| source validity and growing uniformity            | OPEN                           |
| Route-A / Route-B gates                           | OPEN                           |
| twin-prime conclusion                             | NONE                           |

We record `ARITHMETIC_ADVANCE`=`NO` and `FIXED_POWER_CREDIT`=0. The next finite question is the bandwidth–normalization phase diagram, which varies the block band while keeping the two normalization rules explicit.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
