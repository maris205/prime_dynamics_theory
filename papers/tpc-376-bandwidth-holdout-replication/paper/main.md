# A Bandwidth Holdout Replication for the Count-2048 Prime-Shell Operator

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 3, 2026
- **Repository source commit:** `ddfb775a88bced9a1bcafff5c65b13e6df441e55`

## Abstrac

TPC-375 found that the first member of a finite block-band menu matching its high-$Q$ spectral failure support was the block-distance cutoff $c=1$. This paper tests that rule on a response-blind grid-index holdout. We use the three reserved indices $(5,15,30)$ of the previously declared grid $a_j=1010001+401j$, with count $2048$, eight blocks of length $256$, $Q\in\{512,2048,8192\}$, beta $2$, exponent one, and the all-plus law. On the complete nine-row panel, the $c=1$ band has spectral failure profile $(0,3,3)$ by increasing $Q$, exactly the parent profile, and has no Schur-cap failure. The selected full-mode band Rayleigh retention is between $0.93760019185559207$ and $0.976941204869197$. The result is a finite grid-index replication only: the two lower-index holdout windows overlap nearby training windows, and no origin-uniform, growing, arithmetic, or twin-prime conclusion is claimed.

**A Response-Blind Holdout**

for the Finite \(c=1\) Bandwidth Rule

Liang Wang

School of Mathematics and Statistics, Huazhong University of Science

and Technology (HUST), Wuhan, China

September 4, 2026

# Question and claim boundary

The recent finite TPC audits locate a recurring high-\(Q\) spectral signal in a normalized prime-shell matrix. TPC-374 showed that a predeclared near-block band with block distance at most three reproduced six parent failure keys. TPC-375 then compared the nested cutoffs \(c=0,1,2,3\) on the same complete beta-\(2\) panel. Its first parent-support match was \(c=1\). The natural next question is transfer to origins that were reserved by the earlier origin-grid protocol rather than used in that panel.

The present result is deliberately finite. The term *holdout* means a set of grid indices fixed independently of the signed response; it does not mean that all coordinate intervals are disjoint. In particular, the first two holdout intervals overlap a neighboring training interval by a small number of coordinates. We therefore do not interpret this experiment as an independent physical source sample.

# Finite normalized objec

For a frozen interval \(I=[a,a+2047]\cap\mathbb Z\), \(Q\in\{512,2048,8192\}\), and a prime \(p\in(Q,2Q]\), put \[K_p(u,t)=p\left(\frac pQ\right)^2
 \frac{66^2}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid(u-t)}-\frac{1}{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.\] The all-plus numerator and its row geometry are \[A(u,t)=\sum_{Q<p\leq 2Q}K_p(u,t),\qquad
 G(u)=\sum_{t\in I}\sum_{Q<p\leq2Q}K_p(u,t)^2.\] The full normalized matrix is \[\mathsf T(u,t)=\frac{A(u,t)}{\sqrt{G(u)G(t)}}.\] Write \(b(u)=\lfloor(u-a)/256\rfloor\). The frozen \(c=1\) band and tail are \[\mathsf B(u,t)=\mathsf T(u,t)\mathbf 1_{\lvert b(u)-b(t)\rvert\leq1},
 \qquad \mathsf R=\mathsf T-\mathsf B.\]

The geometry is a finite sum of rational squares. At the exact anchor \(I=[1012006,1012019)\) and \(Q=4\), direct rational arithmetic verifies symmetry and strict positivity. Also, entrywise \(\mathsf T=\mathsf B+\mathsf R\). Thus, if \(\mathsf Tv=\lambda v\) and \(\|v\|_2=1\), then \[v^\mathsf{T}\mathsf B\,v+v^\mathsf{T}\mathsf R\,v
 =v^\mathsf{T}\mathsf Tv=\lambda .\] These are finite identities and carry no assertion about a growing family.

# Response-blind holdout protocol

The earlier candidate grid is \[a_j=1010001+401j,\qquad 0\leq j<41.\] TPC-375 used the training indices \((0,20,40)\). Before reading any holdout metric, this audit reserved \((5,15,30)\), giving \[(a_5,a_{15},a_{30})=(1012006,1016016,1022031).\] The complete Cartesian product of these origins and the three \(Q\) anchors is evaluated. No origin, row, cutoff, eigenmode, or sign is selected after a response is observed. The full mode is the eigenvalue of largest absolute value, with the minimum eigenvalue winning an exact tie.

| quantity                   | value                            |
| :------------------------- | :------------------------------- |
| holdout indices            | \((5,15,30)\)                    |
| holdout origins            | \((1012006,1016016,1022031)\)    |
| window and blocks          | \(2048\) points; \(8\times256\)  |
| shell anchors              | \(Q=512,2048,8192\)              |
| beta, exponent, law        | \(2,1,\mathrm{all\text{-}plus}\) |
| band                       | block distance \(\leq1\)         |
| spectral failures by \(Q\) | \(0/3,\ 3/3,\ 3/3\)              |
| Schur failures             | \(0/9\)                          |

Frozen protocol and finite census.

# Results

The \(c=1\) band spectral values range from \(0.50281931\) to \(0.50283444\) at \(Q=512\), from \(0.66562826\) to \(0.66563868\) at \(Q=2048\), and from \(0.66694246\) to \(0.66694503\) at \(Q=8192\); the certificate records the full precision. Relative to the cap \(0.64\), this gives six failures, with the same \((0,3,3)\) Q-profile as the TPC-375 panel. The Schur cap \(0.83\) is not crossed in any row.

|  origin | \(Q\) |       band spectrum |          band Schur |      abs. retention |
| ------: | ----: | ------------------: | ------------------: | ------------------: |
| 1012006 |   512 | 0.50283444162621627 | 0.53128395220859004 |   0.976941204869197 |
| 1012006 |  2048 | 0.66562917307210956 | 0.67846748108299049 | 0.93760084447589365 |
| 1012006 |  8192 | 0.66694245634594918 | 0.67972169418368655 | 0.93760019185559207 |
| 1016016 |   512 | 0.50282578731047578 | 0.53133693522854253 | 0.97693928706874245 |
| 1016016 |  2048 | 0.66563867656808429 | 0.67852090333711979 | 0.93760180369522450 |
| 1016016 |  8192 | 0.66694481889731727 | 0.67971862044077846 | 0.93760051104122999 |
| 1022031 |   512 | 0.50281930544856424 | 0.53129871974955478 | 0.97693949932444424 |
| 1022031 |  2048 | 0.66562825618491772 | 0.67848910457776990 | 0.93760054654011304 |
| 1022031 |  8192 | 0.66694502781223552 | 0.67973329833486718 | 0.93760019630794067 |

Row-level band values and selected-mode tail summary.

The selected full-mode band absolute-Rayleigh retention is \[0.93760019185559207\leq
  \frac{|v^\mathsf{T}\mathsf B\,v|}{|\lambda|}
  \leq0.976941204869197,\] and the maximum corresponding absolute tail fraction is \(0.062399808144408715\). The producer checks eigenvector residuals, norm, symmetry, and the finite Schur/Frobenius envelopes. A separate checker reconstructs the prime shell in descending order and obtains the same failure profile and principal metrics within its declared numerical tolerance.

# Audit and reproducibility

The repository package contains a producer, a reverse-shell independent checker, a mutation stress test, an exact-anchor record, and a local fail-closed Bridge-B. The producer locks the TPC-375 engine and certificate by LF-normalized SHA-256; the independent checker does not import the producer. Normal and optimized Python runs are required to have empty standard error and byte-identical output.

The exact finite statements are the fixed grid protocol, the finite nonnegative-square geometry, the common normalization, the band/tail identity, and the Rayleigh decomposition. The numerical statements are scoped to the nine declared rows. The official Route-A and Route-B evaluator files named by the Session are absent, so no official evaluator pass is asserted.

# Conclusion and next question

The c=1 bandwidth rule survives this predeclared grid-index holdout at the level of its Q-profile: six high-Q spectral failures and no Schur failures. This is a concrete finite transfer edge from TPC-375, while the overlap between some coordinate intervals is an explicit obstruction to stronger sample-independence language. Origin/window uniformity, cross-block causality, a growing operator estimate, source-uniform arithmetic \(L^2\), fixed-power credit, and the twin-prime endpoint remain open.

The next minimal experiment is a predeclared window-scale/count holdout for the same c=1 rule, recorded in the route ledger as `TEST_C1_WINDOW_SCALE_HOLDOUT`.
