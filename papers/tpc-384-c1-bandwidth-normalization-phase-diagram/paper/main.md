# TPC-384: A Finite Bandwidth–Normalization Phase Diagram

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang\\School of Mathematics and Statistics, HUST\\Wuhan, China
- **Source date:** September 4, 2026
- **Repository source commit:** `75e23fe44efae6c677b440ed8149eaacd31e2323`

## Abstract

We hold a centered prime-shell matrix and its square-energy geometry fixed, and cross four predeclared block-distance bandwidths with two explicit normalizations on a fresh response-blind origin panel. The resulting 288-row finite phase diagram has law-dependent origin stability. For the all-plus law, the pooled high-\(Q\) mean rises from \(0.36656315295619812\) at \(c=0\) to \(0.63888760360944985\) at \(c=3\), still below the fixed spectral cap \(0.64\). The pooled/local calibration shift changes sign at the narrowest bandwidth. These are finite model-relative observations; no bandwidth monotonicity, source-valid normalization, arithmetic cancellation, or twin-prime theorem is claimed.

# Question and frozen protocol

TPC-383 showed that a local-versus-pooled normalization comparison can preserve a finite all-plus origin shape while moving its absolute scale. The next question is whether that behavior is stable across bandwidth. We use a fresh affine grid \(a_j=1800001+401j\), freeze indices \(0,20,40\) before any response or metric read, and obtain origins \[(1800001,1808021,1816041).\]

Each window has \(N=512\) points in four contiguous blocks of length \(128\). The bandwidth menu is \(c\in\{0,1,2,3\}\), where entries in blocks \(b,b'\) are retained when \(\lvert b-b'\rvert\leq c\). We use \(Q\in\{512,2048,8192\}\), exponent one, beta two, height 66, and the four predeclared laws all-plus, alternating-index, mod-4 character, and half-split. The two normalizations are local diagonal whitening and a scalar pooled geometry. Thus the panel has \[3\times3\times4\times4\times2=288\] rows and \(4\times3\times4\times2=96\) origin-spread cells. The spread cap \(\Delta\leq0.01\), spectral cap \(0.64\), and Schur cap \(0.83\) are fixed in advance.

# Matrix construction

For \(I_o=\{o,\ldots,o+511\}\) and \(S_Q=\{p:Q<p\leq2Q,\ p\text{ prime}\}\), set \[B_p(u,t)=p(p/Q)^2\frac{66^2}{66^2+(u-t)^2}
\left(1_{p\mid(u-t)}-\frac1{p-1}\right)
1_{p\nmid u}1_{p\nmid t}1_{u\ne t}.\]

The law matrix is the signed sum of these components and the common geometry is \(g(u)=\sum_{t,p}B_p(u,t)^2\). For a law matrix \(M\), \[A^{\rm loc}_{u,t}=\frac{M_{u,t}}{\sqrt{g(u)g(t)}},\qquad
A^{\rm pool}_{u,t}=\frac{M_{u,t}}{G_Q},\] where \(G_Q\) is the mean of all geometry coordinates over the three fixed origins. We apply the block mask after normalization and record the largest absolute eigenvalue, Schur mass, and Frobenius norm. The exact anchor \([1800001,1800014)\) at \(Q=8\) has shell \([11,13]\); rational arithmetic checks geometry positivity and law-matrix symmetry.

# Results

The stable-cell counts (out of 12 law/\(Q\) cells for each pair) are:

|               |      |      |      |      |      |      |      |      |
| :-----------: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|               |      |      |      |      |      |      |      |      |
| normalization | loc  | pool | loc  | pool | loc  | pool | loc  | pool |
| stable cells  | 6/12 | 7/12 | 8/12 | 7/12 | 8/12 | 8/12 | 8/12 | 8/12 |

All 288 rows are below both fixed finite caps. This does not imply an operator theorem: the cap census is tied to this panel and this normalization menu. The alternating-index law is the persistent source of spread failures; its pooled high-\(Q\), \(c=3\) spread is \(0.039758700305072295\), while the all-plus high-\(Q\) cells are stable throughout the four bandwidths.

For all-plus at \(Q=8192\), the pooled/local relative shifts are

|                   \(c\)                    |              0 |            1 |            2 |            3 |
| :----------------------------------------: | -------------: | -----------: | -----------: | -----------: |
| \((G_{\rm pool}-G_{\rm loc})/G_{\rm loc}\) | \-0.0976844658 | 0.0364622707 | 0.0323564031 | 0.0291364393 |

The corresponding pooled all-plus means are \[0.36656315295619812,\quad 0.59976783258284894,\quad
0.63384010801912960,\quad 0.63888760360944985\] for \(c=0,1,2,3\), respectively. The upward sequence is a finite numerical observation, not a claim of monotonicity beyond the four declared points.

# Verification and claim boundary

The producer and a non-importing reverse-shell checker recompute the complete panel in normal and optimized Python modes. A 25-mutation adversarial suite rejects altered protocol, row, phase, and claim fields. The local Bridge-B locks the code, certificate, proof documents, PDF, and exact-anchor metadata, then repeats all checks in both modes. The Session-named Route-A and Route-B evaluator files are absent, so the local result is fail-closed repository evidence only.

| statement                                    | status                         |
| :------------------------------------------- | :----------------------------- |
| selection and coordinate separation          | PROVED / FINITE                |
| 288-row bandwidth phase diagram              | NUMERICALLY CERTIFIED / FINITE |
| origin-spread and calibration census         | NUMERICALLY CERTIFIED / FINITE |
| bandwidth monotonicity                       | OPEN                           |
| source-valid normalization and growing bound | OPEN                           |
| arithmetic \(L^2\), fixed power, Route-B     | NO CREDIT / OPEN               |
| twin-prime conclusion                        | NONE                           |

The next finite question is a response-blind origin holdout at the bandwidths that approach the cap. We record `ARITHMETIC_ADVANCE=NO` and `FIXED_POWER_CREDIT=0`.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
