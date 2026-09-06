# TPC-386: A Count Holdout for the Finite $c=1$ Bandwidth Proxy

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 4, 2026
- **Repository source commit:** `a8e14036a6516d08a787b6e0af53141e3dc26b13`

## Abstract

The preceding TPC-385 experiment transferred a finite high-bandwidth phase between fresh origins while keeping the window count fixed. We now freeze that reference and change the count. Three coordinate-disjoint windows of length \(512\) define a calibration-only pooled geometry, and two windows of length \(1024\) are evaluated as a response-blind holdout. Both a fixed three-block band and the full relative band are recorded. In the all-plus law at \(Q=8192\), the holdout-to-calibration spectral ratios range from \(1.0652\) to \(1.1295\), while the inherited finite spectral diagnostic \(0.64\) fails on all sixteen all-plus holdout rows. The failure already appears in the fixed band, so it is not caused solely by remote block pairs. The result is a finite count-transfer observation and a scoped obstruction to promoting the old cap to a count-uniform statement. It proves no growing operator bound and makes no arithmetic claim about twin primes.

# Question and claim boundary

We work in one fixed finite dynamical-system family. The question is whether the origin transfer observed in TPC-385 survives a predeclared change from \(N=512\) to \(N=1024\), and whether its diagnostic spectral cap can be reused. The distinction matters: a finite origin holdout and a bound uniform in the window count are different claims. Throughout this paper, \[\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.\] The official Session evaluator files are not present in this checkout; the local Bridge-B checker is therefore treated as fail-closed repository evidence rather than an official route verdict.

# Finite proxy and frozen protocol

For \(p\in(Q,2Q]\) and \(u,v\) in a consecutive integer interval \(I\), set \[\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{66^2}{66^2+(u-v)^2}
 \left({\bf 1}_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot{\bf 1}_{u\ne v}{\bf 1}_{p\nmid u}{\bf 1}_{p\nmid v}.\end{aligned}\] For each of the four declared sign laws \(\sigma\), let \(K_\sigma=\sum_{p\in(Q,2Q]}\sigma(p)K_p\) and define the diagonal geometry \[G(u)=\sum_{p\in(Q,2Q]}\sum_{v\in I}K_p(u,v)^2.\] The local matrix divides \(K_\sigma(u,v)\) by \(\sqrt{G(u)G(v)}\). The pooled matrix divides by the mean of \(G\) over the three calibration windows only. Blocks have length \(128\).

The candidate origins are \(a_j=2200001+401j\) for \(0\leq j<41\); indices \(0,10,20,30,40\) are selected before readout. Indices \(0,10,20\) have \(N=512\) and are calibration, while indices \(30,40\) have \(N=1024\) and are holdout. The fixed band retains block pairs at distance at most three. The full-relative band retains all block pairs at the relevant count. We use \(Q=2048,8192\), exponent one, \(\beta=2\), and the laws `all_plus`, `alternating_index`, `mod4_character`, and `half_split`.

For a masked symmetric matrix \(B\) we record \(\|B\|_2\), its maximum absolute row mass (Schur diagnostic), its Frobenius norm, and its symmetry error. The count ratio is the \(N=1024\) holdout mean divided by the \(N=512\) calibration mean within one fixed cell. A \(20\%\) ratio envelope is an explicitly declared finite audit threshold, not a theorem.

# Certificate and exact anchor

The producer writes a canonical JSON certificate with 160 rows and 32 cells. The certificate locks the TPC-385 producer and certificate hashes, records the response-blind selection protocol, and includes an independent replay which sums the prime shell in reverse order. A second script applies 25 structural mutations; all are rejected by the certificate validator.

At \(Q=8\), the exact interval \([2200001,2200014)\) has shell \(\{11,13\}\). Rational arithmetic verifies positive diagonal geometry and symmetry of all four signed matrices on this anchor. This exact check validates the finite construction, not its large-\(N\) behavior.

# Results

The complete panel has no Schur-cap failure. There are 16 spectral-cap failures, exactly the all-plus rows at \(N=1024\) for the two modes, two normalizations, and two values of \(Q\). The calibration and holdout one-percent stability counts are respectively \(20/32\) and \(28/32\).

| band          | normalization | calibration |     holdout |    ratio | \(\log_2\) ratio |
| :------------ | :------------ | ----------: | ----------: | -------: | ---------------: |
| fixed \(c=3\) | local         | 0.620802645 | 0.661288692 | 1.065216 |         0.091146 |
| fixed \(c=3\) | pooled        | 0.638885619 | 0.709942760 | 1.111220 |         0.152145 |
| full relative | local         | 0.620802645 | 0.674100952 | 1.085854 |         0.118830 |
| full relative | pooled        | 0.638885619 | 0.721585871 | 1.129445 |         0.175613 |

All-plus \(Q=8192\) count transfer. The parent reference is the locked TPC-385 \(N=512\) value; “ratio” compares holdout with calibration.

All four ratios lie inside the declared \(20\%\) finite audit envelope, but that observation does not establish count uniformity. Relative to the locked parent values \(0.6207997105\) (local) and \(0.6388876036\) (pooled), the four holdout forecast errors are \(6.5221\%\), \(11.1217\%\), \(8.5859\%\), and \(12.9441\%\), in the table order. The fixed-band local holdout value already exceeds \(0.64\), and the full band is only modestly larger. Thus the old cap cannot be transferred to this count change even in a band that excludes the most remote block pairs.

The signed laws remain controls rather than a uniformity certificate. For example, in the full-relative, \(Q=8192\) cell their holdout means are \(0.000581599\), \(0.004598884\), and \(0.218454930\) for the alternating, mod-\(4\), and half-split laws, respectively. Their different scales and spreads reinforce the need to keep the all-plus transfer claim scoped.

# Interpretation and next step

The strongest positive result is a reproducible, origin-disjoint count transfer inside a broad finite envelope. The strongest obstruction is the failure of the inherited \(0.64\) spectral diagnostic on every all-plus \(N=1024\) row, including the fixed-band mode. The reusable structure is a locked parent forecast, calibration-only pooled normalization, explicit count roles, and reverse-order plus mutation checks.

The next minimal question is whether the observed increase is a smooth count ladder effect or an artifact of the endpoint normalization. The project therefore emits \[\texttt{ROUND2\_CLUE=TEST\_C1\_COUNT\_LADDER\_RENORMALIZATION}.\] Any resulting statement must remain finite until a genuine growing-\(N\) argument is supplied.

# Reproduction

The source, certificate, proof package, and checkers are in `papers/tpc-386-c1-count-holdout-bandwidth/`. The release runs the producer and independent checker in ordinary and optimized Python modes, the 25-mutation stress test, and the local Bridge-B checker. The generated files `paper/main.pdf` and `paper/paper.pdf` are byte-identical.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
