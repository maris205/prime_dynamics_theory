# A Coordinate-Disjoint Cross-Holdout for the $c=1$ Prime-Shell Band

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 4, 2026
- **Repository source commit:** `ddfb775a88bced9a1bcafff5c65b13e6df441e55`

## Abstrac

TPC-377 found that a finite $c=1$ prime-shell band retained its high-$Q$ failure support across a nested count ladder. This paper tests whether the support transfers to a fresh, coordinate-disjoint origin family. We freeze an affine grid, select three indices before reading any response, and evaluate the endpoint counts $N=1024,2048$ at $Q=512,2048,8192$, giving 18 rows. The complete band profile is $(0,3,3)$ at both counts: 12 of 18 rows exceed the spectral cap and none exceed the Schur cap. Selected full-mode absolute Rayleigh retention ranges from $0.93759972206138864$ to $0.98046528117382914$. This is finite response-blind support-transfer evidence only; it does not prove origin or scale uniformity, an asymptotic operator bound, an arithmetic estimate, or a twin-prime theorem.

<span>**A Coordinate-Disjoint Cross-Holdout for the \(c=1\) Prime-Shell Band**</span>
Liang Wang
School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
September 4, 2026

# Question and claim boundary

The recent TPC line has isolated a recurring finite signature: after full-window square-energy normalization, the \(c=1\) near-block band exceeds a working spectral cap at the two high-\(Q\) anchors while the \(Q=512\) row remains below it. TPC-377 tested this signature on nested prefixes of established origins. The present question is deliberately narrower and more hostile: does the same cap-support pattern occur on new origins whose coordinates are disjoint from the earlier windows?

All statements in this paper concern the declared finite panel. In particular, a coordinate-disjoint sample is not an origin-uniform theorem, and a shared left endpoint between two finite counts is not a growing operator construction. The normalization is recomputed at each scale.

# Finite object and exact identities

For \(I=[a,a+N-1]\cap\mathbb Z\), \(p\in(Q,2Q]\), and \(u,t\in I\), define \[K_p(u,t)=p\left(\frac pQ\right)^2
 \frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid(u-t)}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.\] The all-plus matrix and its full-window square-energy geometry are \[A(u,t)=\sum_{Q<p\le2Q}K_p(u,t),\qquad
 G(u)=\sum_{t\in I}\sum_{Q<p\le2Q}K_p(u,t)^2,
 \qquad T(u,t)=\frac{A(u,t)}{\sqrt{G(u)G(t)}}.\] With \(b(u)=\lfloor(u-a)/256\rfloor\), the inherited \(c=1\) band is \[B_1(u,t)=T(u,t){\bf1}_{|b(u)-b(t)|\le1},
 \qquad R_1=T-B_1.\] The geometry is a finite sum of nonnegative rational squares. The exact 13-point anchor at \((a,Q)=(1100001,4)\) checks positive geometry and symmetry by rational arithmetic. The mask gives \(T=B_1+R_1\) entrywise; hence, if \(Tv=\lambda v\) and \(\|v\|_2=1\), \[v^\mathsf{T}B_1v+v^\mathsf{T}R_1v
 =v^\mathsf{T}Tv=\lambda.\] These are exact finite identities, not uniform estimates.

# Predeclared cross-holdout protocol

Before reading any response, we fix the affine candidate grid \[a_j=1100001+401j,\qquad 0\le j<41,\] and select indices \((0,20,40)\), giving \((1100001,1108021,1116041)\). The largest current endpoint interval is \([a,a+2047]\). Exact integer endpoint comparisons show that all six current intervals are disjoint from the largest declared TPC-376 and TPC-377 intervals. At each new origin, the \(N=1024\) interval is a prefix of the \(N=2048\) interval.

We freeze contiguous blocks of length 256, the \(c=1\) mask, exponent one, height 66, beta 2, the all-plus law, and \(Q=(512,2048,8192)\). The spectral and Schur caps are respectively \(0.64\) and \(0.83\). The complete Cartesian panel has \(3\times2\times3=18\) rows, and no row or count is selected using a response, signed metric, or geometry score. The extremal full mode is the largest-absolute-eigenvalue mode, with the minimum mode resolving an exact tie.

# Results

Table [1](#tab:profile) reports the range over the three fresh origins and the number of spectral-cap failures. The two rows in each entry are not independent random samples; they are the fixed finite protocol above.

<div id="tab:profile">

| \(N\) | blocks  |      \(Q=512\)      |     \(Q=2048\)      |     \(Q=8192\)      |
| :---: | :-----: | :-----------------: | :-----------------: | :-----------------: |
| 1024  |    4    | .60988488–.60989272 | .65205068–.65205804 | .65334113–.65334662 |
| 2048  |    8    | .50283355–.50284232 | .66562664–.66564016 | .66694192–.66694513 |
|       | \(0/3\) |       \(3/3\)       |       \(3/3\)       |                     |

Band spectral ranges and failure profile.

</div>

Thus the count-by-\(Q\) profile is \[(0,3,3)\quad\text{at }N=1024,\qquad
 (0,3,3)\quad\text{at }N=2048.\] There are 12 spectral-cap violations and zero Schur-cap violations. The profile agrees with TPC-377 on this new coordinate-disjoint panel. The agreement is a support statement: the displayed spectral ranges change between counts, so no magnitude-stability law is inferred.

For the selected full eigenmode, the absolute band-Rayleigh retention over all 18 rows satisfies \[0.93759972206138864\le
 \frac{|v^\mathsf{T}B_1v|}{|\lambda|}
 \le0.98046528117382914,\] and the largest corresponding absolute tail fraction is \(0.062400277938610291\). Eigen residual, norm, symmetry, Frobenius, and Schur-envelope checks are recorded row by row in the canonical certificate.

# Independent audi

The producer locks the TPC-377 source and certificate and writes a canonical JSON certificate. A separate checker does not import the TPC-378 producer: it sieves primes through 20000, accumulates the shell in reverse order, reconstructs the full and masked matrices, and recomputes all 18 eigensystems. It also recomputes the exact rational anchor. A 24-mutation stress suite changes protocol, row, census, and firewall fields and requires every mutation to be rejected.

Normal and optimized Python runs are required to return zero with empty standard error and byte-identical summary lines. The repository Bridge-B then locks the package source, certificate, paper, PDF, log, and route notes before repeating these checks. The official Session-named Route-A and Route-B evaluator files are absent, so Bridge-B is local fail-closed evidence and not an official evaluator verdict.

# Limitations and route decision

The finite transfer does not prove origin uniformity, window-scale uniformity, spectral-magnitude stability, cross-block causality, source validity of the normalization, a growing masked-operator bound, or a source-uniform arithmetic \(L^2\) estimate. It pays no fixed-power credit: `ARITHMETIC_ADVANCE = NO`, `FIXED_POWER_CREDIT = 0`, and `FULL_GATE_B = OPEN`. There is no Route-B reassembly and no twin-prime conclusion.

The strongest positive result is a response-blind profile transfer to three fresh coordinate-disjoint origins at two endpoint scales. The strongest obstruction is that this transfer remains a threshold census with scale-specific normalization and moving magnitudes. The reusable structure is the affine-grid selector together with exact interval separation and the common band/tail Rayleigh audit. The next finite question is `TEST_C1_CROSSHOLDOUT_LAW_CONTROL`.

# Conclusion

TPC-378 closes the finite origin/scale cross-holdout proposed by TPC-377: the parent \((0,3,3)\) support pattern survives on the declared fresh panel. It strengthens the empirical map of the finite model while leaving every arithmetic and growing-operator gate open.
