# TPC-382: A Finite \(c=1\) Origin-Family Magnitude Audit

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang\\School of Mathematics and Statistics, HUST\\Wuhan, China
- **Source date:** September 4, 2026
- **Repository source commit:** `75e23fe44efae6c677b440ed8149eaacd31e2323`

## Abstract

We audit the magnitude, rather than only the threshold profile, of a finite prime-shell operator family used in the twin-prime exploratory line. Two sealed, protocol-matched \(N=2048\) panels (TPC-380 and TPC-381) provide six origins, three \(Q\)-anchors, and four predeclared laws. With the rule \(\Delta=(\max-\min)/\operatorname{mean}\leq 0.01\) fixed before reading the parent rows, all-plus is stable at all three \(Q\)’s; the full law census has 8 of 12 cells within the cap. A separately labelled TPC-379 \(N=1024\) scale control refutes one-percent matched-count invariance for all-plus at high \(Q\), with a relative contrast of \(0.020813995160269608\). These are finite certificate results. They do not establish source validity, an asymptotic uniformity theorem, arithmetic power saving, or a twin-prime result.

# Question and scope

The preceding origin-family replay preserved the finite band failure profile but left magnitude stability as an explicit open diagnostic. We ask two finite questions:

1.  Is the normalized band spectral magnitude stable across the two protocol-matched \(N=2048\) origin families?

2.  Is that stability common to all four declared laws, and does it persist when the count is changed to the earlier \(N=1024\) panel?

The first question is answered using already sealed certificates. The second is split into a law census and a clearly non-matched scale control; no claim is made about an unobserved source law.

# Locked protocol

For a parent panel \(P\), law \(\ell\), anchor \(Q\), and origin \(o\), let \(s(P,\ell,Q,o)\) denote the recorded spectral value of the normalized \(c=1\) band. For a locked set of values define \[\Delta=\frac{\max s-\min s}{|O|^{-1}\sum_{o\in O}s(P,\ell,Q,o)}.\] The one-percent cap is fixed at \(0.01\). TPC-380 and TPC-381 have the same count, block rule, shell anchors, kernel, weights, and four laws; their three origins are combined, giving \(6\times3\times4=72\) values in 12 cells. TPC-379 is retained only as a count-\(1024\) scale control with 36 values.

Before aggregation, the producer locks the source and certificate hashes: TPC-379, TPC-380, and TPC-381 are respectively identified by their canonical certificate hashes `a41800cb`, `c80dbfab`, and `c217a475` (prefixes shown only for readability). The independent checker repeats the parent loading, row-key census, and arithmetic without importing the producer.

# Results

The all-plus same-count cells have relative spreads \[1.9035250282068572\!\times\!10^{-5},\quad
 2.380537285421679\!\times\!10^{-5},\quad
 8.0645464844910632\!\times\!10^{-6}\] at \(Q=512,2048,8192\), respectively. The high-\(Q\) mean is \(0.66694363456350925\). The complete same-count census is shown below; “yes” means that the cell’s six-origin spread is at most one percent.

| law               | \(Q=512\) | \(Q=2048\) | \(Q=8192\) |
| :---------------- | :-------: | :--------: | :--------: |
| all-plus          |    yes    |    yes     |    yes     |
| alternating-index |    no     |     no     |     no     |
| mod-4 character   |    no     |    yes     |    yes     |
| half-split        |    yes    |    yes     |    yes     |

Thus 8/12 cells pass the fixed cap. The four failures are exactly the three alternating-index cells and the mod-4 cell at \(Q=512\). This is a law- dependent magnitude census, not evidence that a law may be selected from the data.

For the scale control, compare the mean of the six \(N=2048\) values with the mean of the three TPC-379 \(N=1024\) values at matched law and \(Q\). At all-plus and \(Q=8192\), \[\frac{m_{2048}-m_{1024}}{m_{1024}}
 =0.020813995160269608,\] which exceeds the predeclared one-percent scale-invariance cap. Because the two counts use different normalizations and different origin families, this is a finite refutation of that narrowly stated hypothesis, not a theorem of scale non-uniformity.

# Verification and claim firewall

The canonical producer replay, independent aggregation replay, and 25-field adversarial mutation suite each pass in normal and optimized Python modes. The finite proof package therefore certifies the arithmetic transformation of the locked parent rows and the stated finite comparisons. The official Session evaluator files are not present in this checkout; the repository’s Bridge-B is a local fail-closed check.

| item                                                          | status                               |
| :------------------------------------------------------------ | :----------------------------------- |
| parent locks and row census                                   | PROVED\_EXACT\_FINITE                |
| all-plus high-\(Q\) one-percent stability                     | NUMERICALLY CERTIFIED, FINITE SCOPED |
| law-dependent spread census                                   | NUMERICALLY CERTIFIED, FINITE SCOPED |
| matched-count one-percent scale hypothesis                    | REFUTED, FINITE SCOPED               |
| source-valid normalization, growing bound, arithmetic \(L^2\) | OPEN                                 |
| Route-A / Route-B gates                                       | OPEN                                 |
| twin-prime conclusion                                         | NONE                                 |

In particular, `ARITHMETIC_ADVANCE`=`NO` and `FIXED_POWER_CREDIT`=0. The next finite test is the predeclared pooled cross-origin normalization audit: determine whether the observed magnitude persistence survives a common normalization.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
