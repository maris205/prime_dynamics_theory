# A Shell-Scale Obstruction to a Finite Normalized Prime-Shell Cap

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 2026
- **Repository source commit:** `0fdbb7509057a196c20639a9b607311cdced464f`

## Abstract

We test the missing shell-scale quantifier in a finite normalized prime-shell operator. The three high-origin intervals selected by the preceding geometry-only holdout are held fixed, while the shell ladder is widened from $Q\leq80$ to $Q\in\{12,24,36,54,80,128,256,512\}$. At counts 256 and 512, two kernel exponents, and four fixed sign laws, the replay contains 384 rows with true spectra. The inherited working caps, 0.83 for the normalized Schur envelope and 0.64 for the normalized spectrum, hold through $Q=80$ and fail first at $Q=128$. The global maxima are 1.7172665118910415 and 1.6398895499394266; 33 Schur rows and 30 spectral rows violate the corresponding caps. This is a finite, scoped shell-scale obstruction, not an asymptotic theorem or an arithmetic advance.

# Question and scope

TPC-361 independently reproduced a finite normalized cap on a new high-origin panel at the shell anchors used by the earlier studies. That result leaves a different quantifier untested: uniformity as the prime shell itself grows. The present paper keeps the origins fixed and varies \(Q\) across a wider ladder. A failure is scientifically useful because it identifies where a finite cap stops transferring; it is not evidence for a twin-prime theorem.

The Session-named official Route-A and Route-B evaluator files are absent from this checkout. We therefore use a fail-closed local Bridge-B package only. No source response, arithmetic reassembly, or fixed-power credit is used.

# Finite operator and envelopes

For \(I=[x,x+N-1]\cap\mathbb Z\), define, for prime \(Q<p\leq2Q\), \[B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t},
 \label{eq:block}\] where \(s\in\{1,2\}\). For a fixed sign law \(\varepsilon\) on the shell, let \(A_\varepsilon=\sum_p\varepsilon_pB_p\). The unsigned geometry and normalized operator are \[G_u=\sum_p\sum_{t\in I}B_p(u,t)^2,
 \qquad A_\varepsilon^\#=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
 \quad D_G=\operatorname{diag}(G_u).
 \label{eq:norm}\] The laws are all-plus, alternating shell index, the prime modulo-four character, and a half-shell split. For each finite real matrix \(T\), \[\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
 \qquad
 \lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
 \label{eq:envelope}\] These inequalities are exact finite facts. The numerical caps below are working finite benchmarks inherited from the previous anchor range.

# Protocol

The origins are frozen as \[(313030,\;311166,\;321651),\] with counts \(N\in\{256,512\}\). The shell ladder is \[Q\in\{12,24,36,54,80,128,256,512\},
 \qquad s\in\{1,2\}.\] All four laws are evaluated at every setting, giving \(3\cdot2\cdot8\cdot2\cdot4=384\) rows. Every row records the literal shell, geometry range, normalized Schur row-sum, normalized Frobenius norm, and true spectral norm. The first five shell values form the low-\(Q\) comparison set; the last three form the high-\(Q\) stress set. We classify all 336 adjacent \(Q\) transitions using a \(10^{-8}\) guard.

# Results

Table [1](#tab:q) reports the extrema at each shell value. Each row of the table aggregates 48 law-level records.

<div id="tab:q">

| \(Q\) | rows | max Schur | max spectrum | Schur violations | spectral violations |
| ----: | ---: | --------: | -----------: | ---------------: | ------------------: |
|    12 |   48 |  0.193367 |     0.055968 |                0 |                   0 |
|    24 |   48 |  0.155771 |     0.060848 |                0 |                   0 |
|    36 |   48 |  0.192496 |     0.095375 |                0 |                   0 |
|    54 |   48 |  0.378084 |     0.242326 |                0 |                   0 |
|    80 |   48 |  0.808302 |     0.626907 |                0 |                   0 |
|   128 |   48 |  1.501455 |     1.323883 |                9 |                   6 |
|   256 |   48 |  1.596727 |     1.543371 |               12 |                  12 |
|   512 |   48 |  1.717267 |     1.639890 |               12 |                  12 |

Normalized extrema by shell anchor.

</div>

Over all 384 rows, the normalized Schur maximum is \[1.7172665118910415,\] and the normalized spectral maximum is \[1.6398895499394266.\] The low-\(Q\) maxima are ‘0.80830232610282304‘ and ‘0.62690716242733457‘, so both inherited caps hold through \(Q=80\). The first Schur and spectral cap failures are both at \(Q=128\). There are 33 Schur violations and 30 spectral violations over the full ladder. The normalized Frobenius maximum is 2.9085219065076484; it is recorded as an envelope, not used to rescue the failed Schur or spectral cap.

At the 96 fixed settings, the largest-law census is all-plus 78, alternating-index 4, mod-\(4\) 14, and half-split 0. Thus all-plus is usually, but not universally, the largest finite law. Across the 336 adjacent \(Q\) transitions, 200 increase and 136 decrease, with no flat transition under the guard. The high-\(Q\) obstruction is consequently visible in multiple laws and does not reduce to a choice of one exceptional count ladder.

# Audits and exact anchor

The forward producer locks the TPC-355 base implementation and the TPC-361 certificate, then computes the full 384-row certificate. The independent checker rebuilds the prime sieve, traverses every shell in reverse order, reconstructs all masks and sign laws, and recomputes every metric without importing either producer. A 15-mutation stress test rejects altered shell sets, row counts, cap census, transition census, and claim-firewall values. Normal and optimized executions have identical checker output.

At \(Q=4\), \(s=1\), the exact interval ‘\[313060,313073\]‘ has shell \(\{5,7\}\). Rational evaluation gives a symmetric matrix and positive unsigned geometry; the certificate stores rational matrix and geometry digests. This anchor is an exact finite sanity check and does not affect the high-\(Q\) conclusion.

# Claim firewall and route decision

The envelope inequalities in [\[eq:envelope\]](#eq:envelope) are proved for finite matrices. The following statuses deliberately separate the finite positive low-\(Q\) result from the scoped negative extension:

    TPC362_SHELL_SCALE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
    TPC362_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC362_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC362_LOW_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC362_HIGH_Q_CAP_EXTENSION = REFUTED_SCOPED_ON_DECLARED_Q_LADDER
    TPC362_LAW_WINNER_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC362_GROWING_OPERATOR_BOUND = OPEN
    TPC362_SOURCE_UNIFORM_L2 = OPEN
    TPC362_ARITHMETIC_ADVANCE = NO
    TPC362_FIXED_POWER_CREDIT = 0
    TPC362_FULL_GATE_B = OPEN
    TPC362_TWIN_PRIME_RESULT = NONE

The high-\(Q\) observation is scoped to the declared finite operator and does not rule out a future renormalization or a different theorem. It does rule out silently carrying the current ‘Q\<=80‘ cap to ‘Q\>=128‘ in this model.

# Conclusion

The shell ladder locates a sharp finite route obstruction: the normalized cap that survives the independent high-origin replication is not shell-uniform. The next defensible task is to localize the first \(Q=128\) failure by law and row geometry, then test any proposed repair under an equally explicit finite holdout. A growing masked-operator bound, source-uniform arithmetic \(L^2\), Route-B reassembly, fixed-power credit, and the twin-prime endpoint remain open.

`TPC362_ARITHMETIC_ADVANCE=NO`, `TPC362_FIXED_POWER_CREDIT=0`, `TPC362_FULL_GATE_B=OPEN`.
