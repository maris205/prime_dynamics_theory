# Fresh-Origin Transfer of a Finite Operator-Norm Certificate

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 2026
- **Repository source commit:** `642a0314e9c2a8dd7eb8a83d0bbd3e22d903b18e`

## Abstract

We test whether a finite operator certificate for the position-aware normalization of a literal divisibility-masked prime-shell operator transfers to fresh, widely separated origins. The three new origins are fixed in advance as $52001+100000j$ for $j=0,1,2$, and the preceding count, shell, kernel, and sign-law protocol is replayed without using a source response. Across 288 law-level rows, every raw and normalized matrix receives Schur row-sum and Frobenius envelopes; the all-plus law also receives 144 extreme eigenvalue readouts. The fresh normalized Schur maximum is 0.80850510742101689 and the fresh all-plus spectral maximum is 0.62663944469203836, both inside the frozen parent thresholds $0.83$ and $0.64$. The origin span is 168000. This finite transfer is accompanied by the same obstruction as before: normalized spectral values have 13 upward, 34 downward, and 7 flat adjacent count transitions. No origin-uniform operator estimate, arithmetic advance, or twin-prime conclusion follows.

# Question and scope

TPC-357 established a finite Schur/spectral scale audit on three origins selected by a geometry-only adversarial rule. A finite cap can be informative only if it survives a new origin panel chosen independently of the measured spectral values. We therefore ask whether the two numerical thresholds from TPC-357 transfer to a disjoint, widely spaced panel.

The experiment is intentionally operator-only. It does not evaluate the V59 source response, select a sign law from data, or reassemble an arithmetic estimate. The Session-named official Route-A and Route-B evaluator files are absent from this checkout; the accompanying local Bridge-B checker is fail-closed reproducibility evidence rather than an official evaluator pass.

# Model and frozen holdout

Let \(I=[x,x+N-1]\cap\mathbb Z\), let \(S_Q=\{p\text{ prime}:Q<p\leq2Q\}\), and set \(H=66\). The inherited literal component is \[B_p(u,t)=p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
 \label{eq:block}\] For a shell sign vector \(\varepsilon\), write \(A_\varepsilon=\sum_{p\in S_Q}\varepsilon_pB_p\) and define the unsigned geometry \[G_u=\sum_{p\in S_Q}\sum_{t\in I}B_p(u,t)^2,
 \qquad A_\varepsilon^\#=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
 \quad D_G=\operatorname{diag}(G_u).
 \label{eq:norm}\] The four fixed laws are all-plus, alternating shell index, the prime mod-\(4\) character, and a half-shell split.

The fresh origins are \[(x_0,x_1,x_2)=(52001,120001,220001),\] chosen by the arithmetic rule \(x_j=52001+100000j\) before any matrix is constructed. The four count values are \(N\in\{256,512,1024,2048\}\); the shell anchors are \(Q\in\{24,54,80\}\); and the exponents are \(s\in\{1,2\}\). The Cartesian product with four laws has \(3\cdot4\cdot3\cdot2\cdot4=288\) rows. Schur and Frobenius values are recorded everywhere; all-plus extreme eigenvalues are recorded on 72 raw and 72 normalized rows.

# Finite inequalities and transfer criterion

For any finite real symmetric matrix \(T\), the induced-norm inequality gives \[\lVert\,\cdot\,\rVert_2{T}\leq\sqrt{\lVert T\rVert_1\lVert T\rVert_\infty}
 =\max_u\sum_t|T(u,t)|=:S(T),
 \label{eq:schur}\] and the singular-value decomposition gives \[\lVert\,\cdot\,\rVert_2{T}\leq\lVert T\rVert_F.
 \label{eq:frob}\] The inequalities are exact finite statements. They do not imply that their right sides are uniform in \(x\) or \(N\).

TPC-357 froze the numerical thresholds \(S(A_\varepsilon^\#)<0.83\) on its all-law panel and \(\lVert\,\cdot\,\rVert_2{A_{+}^\#}<0.64\) on its all-plus panel . We call the fresh test a parent-cap transfer when both fresh maxima remain below these thresholds and within \(0.001\) of the corresponding parent maxima. This is a finite comparison rule, not a statistical confidence statement or an asymptotic assertion.

# Results

Table [1](#tab:extrema) reports the envelope extrema over the 72 rows of each law. The normalized scales are close to the preceding panel despite the large origin separation, while the raw scales remain much larger.

<div id="tab:extrema">

| Law         | operator   | \(S_{\min}\) | \(S_{\max}\) | \(F_{\min}\) | \(F_{\max}\) |
| :---------- | :--------- | -----------: | -----------: | -----------: | -----------: |
| all-plus    | raw        |      836.380 |     4003.951 |     1163.724 |     9094.056 |
| all-plus    | normalized |     0.105781 |     0.808505 |     0.137913 |     2.214940 |
| alternating | raw        |      337.524 |     1774.141 |      528.188 |     7443.260 |
| alternating | normalized |     0.046774 |     0.212987 |     0.114219 |     0.730793 |
| mod-4       | raw        |      336.814 |     1918.819 |      528.069 |     7459.660 |
| mod-4       | normalized |     0.052819 |     0.211316 |     0.114815 |     0.731187 |
| half-split  | raw        |      353.449 |     1780.587 |      524.240 |     7443.891 |
| half-split  | normalized |     0.046866 |     0.208925 |     0.114235 |     0.725863 |

Fresh-panel envelope extrema. Spectral columns are computed only for all-plus.

</div>

The two headline fresh values are \[\max S(A_\varepsilon^\#)=0.80850510742101689<0.83,
 \qquad
 \max\lVert\,\cdot\,\rVert_2{A_{+}^\#}=0.62663944469203836<0.64.
 \label{eq:headline}\] The raw all-plus spectral maximum is \(1542.7492651981368\), above the declared raw scale marker 1500. Relative to TPC-357, the normalized Schur maximum changes by less than \(0.001\), and the normalized spectral maximum changes by less than \(0.001\) in absolute value.

The transfer does not restore monotone scale behavior. Of the 54 adjacent count transitions for normalized all-plus spectral values, the census is \[(\text{increase},\text{decrease},\text{flat})=(13,34,7),\] where the guard is \(10^{-6}\). For example, at \((x,Q,s)=(52001,80,2)\) the sequence is \[0.6266387277,\quad 0.6033229425,\quad
 0.6033050929,\quad 0.6034590753.\] The cap therefore transfers as a finite envelope while decay does not.

# Controls and claim firewall

The certificate is canonical JSON and locks the TPC-355 base implementation and the TPC-357 producer and certificate. A forward producer computes the fresh rows. A separate reverse-shell checker rebuilds the sieve, literal divisibility masks, unsigned geometry, signed matrices, normalized matrices, envelopes, eigenvalue rows, and a rational \(Q=4\) anchor on \([52031,52044]\). The checker does not import the producer and tolerates only the declared floating-point replay difference.

A fourteen-mutation stress test rejects altered schema, rows, provenance, thresholds, origin rule, response-blindness, transition census, firewall, and exact-anchor fields. The local Bridge-B checker subsequently reruns producer, independent checker, and stress test in normal and optimized Python modes and requires byte-identical stdout. These controls certify the finite artifact; they do not supply an origin-uniform theorem.

# Conclusion

The fresh origin-scale holdout supports a useful but narrow statement: on the declared 168000-span panel, the TPC-357 normalized Schur and all-plus spectral caps transfer within the frozen finite thresholds. This is a new independent finite positive result. The same experiment also preserves the key obstruction: normalized spectral values rise on 13 adjacent transitions, and finite cap transfer alone gives no growing operator estimate.

Accordingly, the source-uniform masked arithmetic \(L^2\) problem, a growing masked-operator bound, fixed-power credit, full Gate B, Route-B reassembly, and the twin-prime endpoint remain open. The next admissible test is a hostile geometry selection on a still-fresh origin panel or a Schur-tightness audit; neither should be presented as arithmetic progress until its own gates close.
