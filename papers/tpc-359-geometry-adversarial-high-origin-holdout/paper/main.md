# A Geometry-Adversarial High-Origin Holdout for a Masked Prime-Shell Operator

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 2026
- **Repository source commit:** `642a0314e9c2a8dd7eb8a83d0bbd3e22d903b18e`

## Abstract

We perform a hostile finite audit of a position-normalized literal divisibility-masked prime-shell operator. Before evaluating any signed matrix, source response, or eigenvalue, we scan 51 high-origin candidates $260001+211j$ using only the unsigned mask-energy spread and select three separated origins. The frozen replay has 288 law-level rows, four interval counts, three shell anchors, two kernel exponents, and four sign laws. Its normalized Schur maximum is $0.80834744529310265$ and its all-plus spectral maximum is $0.6271657593674812$, both within the preceding finite caps; the raw all-plus spectral maximum is $1542.7354827195263$. This is a new finite positive transfer under adversarial geometry selection. It does not establish an origin-uniform or growing bound: the normalized spectral ladder has 12 increases, 36 decreases, and 6 flats. No arithmetic or twin-prime conclusion is claimed.

# Question and claim boundary

The preceding fresh-origin audit transferred a finite normalized operator cap to three widely separated origins. A natural hostile question is whether the same cap survives origins selected for unusually uneven unsigned geometry. The present experiment answers only this finite question. It does not use the V59 source response, does not select a sign law from data, and does not perform the arithmetic reassembly required by the Route-B gate. The Session-named official evaluator files are absent from this checkout, so the accompanying local Bridge-B checker is reproducibility evidence rather than an official Route-A or Route-B pass.

# Literal operator and frozen selection

For \(I=[x,x+N-1]\cap\mathbb Z\), \(Q<p\leq2Q\), and \(s\in\{1,2\}\), we use \[B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
 \label{eq:block}\] For a fixed shell sign law \(\varepsilon\), let \(A_\varepsilon=\sum_p\varepsilon_pB_p\). The unsigned geometry and its position-aware congruence are \[G_u=\sum_{p,t}B_p(u,t)^2,\qquad
 A_\varepsilon^\#=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
 \quad D_G=\operatorname{diag}(G_u).
 \label{eq:norm}\]

The candidate list, pilot count, score, tie break, and minimum separation are fixed as follows: \[\mathcal C=\{260001+211j:0\leq j\leq50\},\quad N_0=256,
 \quad \operatorname{score}(x)=\max_{Q,s}\frac{\max_uG_u}{\min_uG_u},
 \quad \Delta=1536.\] Descending score with an origin tie break and greedy separation selects \[(x_0,x_1,x_2)=(267175,261267,269074).
 \label{eq:origins}\] This selection is response-blind by construction. The full replay uses \(N\in\{256,512,1024,2048\}\), \(Q\in\{24,54,80\}\), \(s\in\{1,2\}\), and the all-plus, alternating-index, mod-\(4\) character, and half-split laws.

# Finite inequalities

For every finite real symmetric matrix \(T\), \[\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|=:S(T),
 \qquad \lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}=:F(T).
 \label{eq:envelopes}\] These are exact finite inequalities. Positivity of every declared \(G_u\) makes the congruence in [\[eq:norm\]](#eq:norm) a well-defined finite real symmetric matrix. None of these facts supplies a bound uniform in \(x\) or \(N\).

# Results

| law         | form       | \(S_{\min}\) | \(S_{\max}\) | \(F_{\min}\) | \(F_{\max}\) |
| :---------- | :--------- | -----------: | -----------: | -----------: | -----------: |
| all-plus    | raw        |      836.380 |     4003.951 |     1163.724 |     9094.056 |
| all-plus    | normalized |     0.105895 |     0.808347 |     0.137913 |     2.214940 |
| alternating | raw        |      337.524 |     1774.141 |      528.188 |     7443.260 |
| alternating | normalized |     0.045981 |     0.208782 |     0.114219 |     0.730793 |
| mod-\(4\)   | raw        |      336.814 |     1918.819 |      528.069 |     7459.660 |
| mod-\(4\)   | normalized |     0.052398 |     0.212119 |     0.114815 |     0.731187 |
| half-split  | raw        |      353.449 |     1780.587 |      524.240 |     7443.891 |
| half-split  | normalized |     0.045793 |     0.214352 |     0.114235 |     0.725863 |

Extrema over the 72 rows of each sign law. Spectra are computed for all-plus only.

The headline extrema are \[\max S(A_\varepsilon^\#)=0.80834744529310265<0.83,
 \qquad
 \max\lVert\,\cdot\,\rVert_2{A_{+}^\#}=0.6271657593674812<0.64.
 \label{eq:headline}\] The preceding TPC-358 values were \(0.80850510742101689\) and \(0.62663944469203836\), respectively. Thus both finite caps transfer within the declared tolerance \(0.001\). The raw all-plus spectral maximum is \(1542.7354827195263\), showing that the normalized comparison is not a claim about the raw operator scale.

The 54 adjacent transitions of the normalized all-plus spectrum are \[(\text{increase},\text{decrease},\text{flat})=(12,36,6)\] under guard \(10^{-6}\). In particular, the finite cap is compatible with nonmonotone scale behavior. The selected pilot geometry spreads range from approximately \(1.54\) to \(3.38\) across the six settings and selected origins; this is a selection diagnostic, not an asymptotic statistic.

# Audits and proof package

The canonical JSON certificate records all 288 rows, the complete 51-record selection ledger, parent locks, finite inequalities, transition census, and a rational \(Q=4\) anchor on \([267205,267218]\). A separate reverse-shell checker rebuilds the sieve, literal masks, unsigned geometry, signed matrices, normalization, envelopes, and all-plus eigenvalues without importing the producer. A 14-mutation stress test rejects altered origins, selection, thresholds, row counts, response-blindness, firewall, anchor, and payload hash. The local Bridge-B checker reruns the three checks in normal and optimized Python modes and requires identical stdout.

The strongest positive statement is therefore a numerically certified finite high-origin adversarial holdout. The strongest obstruction is the persistent nonmonotone spectral ladder and the absence of any growing-origin quantifier.

# Conclusion and route status

TPC-359 strengthens finite evidence for the normalized operator cap under a deliberately hostile geometry-only selection. It does not pay an arithmetic loss, establish source-uniform \(L^2\), prove a growing masked-operator bound, or close Gate B. The next minimal question is whether the Schur envelope is tight or merely loose on the selected panel, followed by an independent high-origin replication if that audit remains inconclusive. The durable status is \(\texttt{ARITHMETIC\_ADVANCE=NO}\), \(\texttt{FIXED\_POWER\_CREDIT=0}\), and \(\texttt{FULL\_GATE\_B=OPEN}\); the twin-prime result remains none.
