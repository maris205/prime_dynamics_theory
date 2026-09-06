# Bulk Persistence at the First Shell-Scale Failure

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 2026
- **Repository source commit:** `0fdbb7509057a196c20639a9b607311cdced464f`

## Abstract

TPC-362 found that a finite normalized spectral cap, valid on the inherited shell range through $Q=80$, first fails at $Q=128$. We test whether this failure is a small exceptional-row or localized-eigenvector effect. The same three high-origin intervals are frozen, and all four fixed sign laws are replayed at $Q\in\{80,128,256\}$, counts $256,512$, and kernel exponents $1,2$, giving 144 true spectra. For every row we delete five percent of the coordinates twice: once by normalized Schur row mass and once by squared mass of the principal eigenvector. All 18 cap-violating rows persist under both restrictions. The smallest retained restricted spectral norm is 1.1843597700033823 at $Q=128$ and 0.86120283374232454 over the full failure set. This is a finite, scoped bulk obstruction; it is not an asymptotic operator theorem, an arithmetic estimate, or a twin-prime result.

# Question and scope

The preceding shell-scale audit kept a normalized finite cap below \(0.64\) at \(Q\leq80\) and observed its first violation at \(Q=128\). A natural diagnostic question is whether the violation is caused by a tiny set of rows, or by a single coordinate carrying the principal eigenvector. If deleting a small set removes the violation, a localized repair might be plausible. If the violation survives targeted deletions, the finite evidence instead points to a collective obstruction.

We answer only this finite diagnostic question. The Session-named official Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B package is therefore used as a fail-closed reproducibility control; no official route pass is asserted. No source response, arithmetic reassembly, or fixed-power credit enters the experiment.

# Finite operator

For \(I=[x,x+N-1]\cap\mathbb Z\), prime \(Q<p\leq2Q\), and \(s\in\{1,2\}\), use the literal block \[B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
\left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
{\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
\label{eq:block}\] For a fixed sign law \(\varepsilon\), let \(A_\varepsilon=\sum_p\varepsilon_pB_p\). The unsigned mask-energy diagonal and normalized matrix are \[G_u=\sum_p\sum_{t\in I}B_p(u,t)^2,
\qquad
A_\varepsilon^\#=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
\quad D_G=\operatorname{diag}(G_u).
\label{eq:norm}\] The four laws are all-plus, alternating shell index, the prime modulo-four character, and a half-shell split. For every finite real matrix \(T\) we use the exact envelopes \[\lVert\,\cdot\,\rVert_2{T}\leq\max_u\sum_t|T(u,t)|,
\qquad
\lVert\,\cdot\,\rVert_2{T}\leq\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
\label{eq:envelopes}\]

# Localization audit

Let \(\lambda_*\) be the eigenvalue of \(A_\varepsilon^\#\) with largest absolute value and let \(v_*\) be a unit eigenvector. Define the row score \(r_u=\sum_t|A_\varepsilon^\#(u,t)|\) and coordinate score \(z_u=|v_*(u)|^2\). With \[k=\lfloor N/20\rfloor,\] we form two principal restrictions. The first deletes the \(k\) largest \(r_u\); the second deletes the \(k\) largest \(z_u\). Ties are resolved by a stable descending sort and the original index. If \(J\) is either deleted set, the reported restricted value is the directly recomputed quantity \[\lVert\,\cdot\,\rVert_2{A_\varepsilon^\#[J^c,J^c]}.\] This is a descriptive finite test, not a claim that a data-selected restriction is an independent random holdout.

The protocol freezes origins \((313030,311166,321651)\) from TPC-361, counts \(N\in\{256,512\}\), shell anchors \(Q\in\{80,128,256\}\), both exponents, and all four laws. Thus there are \(3\cdot2\cdot3\cdot2\cdot4=144\) law rows. The inherited working cap is \(0.64\); it is not promoted to an asymptotic bound.

# Results

Table [1](#tab:q) separates the control shell from the first-failure and stress shells. “Trim max” is the largest value over both deletion rules and all 48 law rows at that \(Q\).

<div id="tab:q">

| \(Q\) | rows | max spectrum | cap failures | trim max | trim cap failures |
| ----: | ---: | -----------: | -----------: | -------: | ----------------: |
|    80 |   48 |     0.626907 |            0 | 0.603135 |                 0 |
|   128 |   48 |     1.323883 |            6 | 1.239083 |                12 |
|   256 |   48 |     1.543371 |           12 | 1.470909 |                24 |

Finite spectral and deletion audit by shell anchor.

</div>

There are six cap failures at \(Q=128\) and twelve at \(Q=256\). Every one is an all-plus row; alternating-index, mod-\(4\), and half-split laws contribute zero failures in this finite panel. The smallest restricted value among the six \(Q=128\) failures is \[1.1843597700033823,\] and the smallest restricted value over all 18 failures is \[0.86120283374232454.\] Both numbers are above the inherited cap. In contrast, the largest restricted value in the 48-row \(Q=80\) control is 0.60313535281541197, below the cap.

<div id="tab:bulk">

| quantity                       | \(Q=128\) | \(Q=256\) | all failures |
| :----------------------------- | --------: | --------: | -----------: |
| original cap failures          |         6 |        12 |           18 |
| persist after Schur trim       |         6 |        12 |           18 |
| persist after eigenvector trim |         6 |        12 |           18 |
| minimum retained spectrum      |  1.184360 |  0.861203 |     0.861203 |

Failure persistence and eigenvector mass diagnostics.

</div>

The largest squared coordinate mass of a principal eigenvector among failing rows is only \(0.0065671250441509798\) in this normalization, and the minimum effective-support fraction \([\sum_u|v_*(u)|^4]^{-1}/N\) is 0.55114876369112986. These are finite descriptive indicators of a spread eigenvector, not a theorem of asymptotic delocalization.

# Checks and exact anchor

The producer locks the TPC-355 base implementation and the TPC-362 certificate, then constructs the 144-row certificate. An independent checker rebuilds the prime sieve, traverses each shell in reverse order, reconstructs the masks and four sign laws, recomputes the eigenvectors and both principal restrictions, and compares every recorded metric. A 16-mutation stress test rejects altered protocols, row counts, failure counts, bulk-persistence counts, and claim-firewall values. Normal and optimized executions have identical checker output.

At \(Q=4\), \(s=1\), the exact interval \([313060,313073]\) has shell \(\{5,7\}\). Rational evaluation confirms symmetry of the unsigned matrix and positivity of the geometry diagonal; rational matrix and geometry digests are retained in the certificate. This exact sanity anchor does not enlarge the high-\(Q\) claim.

# Claim firewall and route decision

    TPC363_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC363_FINITE_ENVELOPE_INEQUALITIES = PROVED_EXACT_FINITE
    TPC363_FIRST_Q128_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC363_SINGLE_ROW_SPIKE_EXPLANATION = REFUTED_SCOPED_ON_DECLARED_TRIMS
    TPC363_EIGENVECTOR_DELOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC363_RENORMALIZED_REPAIR = OPEN
    TPC363_GROWING_OPERATOR_BOUND = OPEN
    TPC363_SOURCE_UNIFORM_L2 = OPEN
    TPC363_ARITHMETIC_ADVANCE = NO
    TPC363_FIXED_POWER_CREDIT = 0
    TPC363_FULL_GATE_B = OPEN
    TPC363_TWIN_PRIME_RESULT = NONE

The strongest finite conclusion is that two natural five-percent leverage trims do not remove the observed high-\(Q\) violation. The strongest obstruction is also the limit of the evidence: the trim sets are selected from the same matrix, the panel is finite, and no universal renormalization statement follows. A repair must therefore be tested on an explicit holdout, while the growing operator bound, source-uniform arithmetic \(L^2\), Route-B reassembly, and the twin-prime endpoint remain open.

# Conclusion

TPC-363 converts the first shell-scale cap failure into a more precise finite obstruction. It is not a one-row spike under either declared deletion rule; the failure survives at least a five-percent targeted principal restriction. The next defensible experiment is an explicitly frozen re-normalization or shell reweighting tested on a holdout, with the same fail-closed proof package.

`TPC363_ARITHMETIC_ADVANCE=NO`, `TPC363_FIXED_POWER_CREDIT=0`, `TPC363_FULL_GATE_B=OPEN`.
