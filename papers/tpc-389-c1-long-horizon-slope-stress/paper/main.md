# TPC-389: Long-Horizon Stress Test for a Frozen Count Slope

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 5, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-388 reported a finite cross-family transfer of a logarithmic count slope. TPC-389 asks whether that interface survives one longer count interval. We freeze the TPC-388 slopes and, on a third coordinate-disjoint family, use three origins at counts $768$ and $1024$ for calibration and two later origins at count $1280$ for holdout. The panel has 256 rows and 32 cells. Anchored parent, same-family local, and recursive parent forecasts all pass a predeclared 3% finite ratio cap. The largest errors are $0.0176155841$, $0.0119975160$, and $0.0299499406$, respectively. This is a finite stress certificate: the inherited spectral diagnostic still fails on 64 of 256 rows, and no arithmetic or asymptotic conclusion follows.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC-388 showed that 32 slopes learned on an earlier finite count ladder survived transfer to a fresh origin family through $N=1024$. The next minimal question is horizon stress: does the same frozen interface remain predictive from $N=1024$ to $N=1280$? We choose a third, coordinate-disjoint affine family $$a_j=2800001+401j,\qquad 0\leq j<41,$$ and freeze indices $0,10,20,30,40$. The first three origins are calibration origins and the last two are holdout origins. All roles and the parent interface are fixed before current responses are read.

The claim firewall is $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ The Session’s official evaluator files are absent in this checkout; the local Bridge-B is fail-closed repository evidence only.

# Finite proxy

For $p\in(Q,2Q]$ and $H=66$, define $$\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left({\bf 1}_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot{\bf 1}_{u\ne v}{\bf 1}_{p\nmid u}{\bf 1}_{p\nmid v}.\end{aligned}$$ The row geometry is the finite square energy $G(u)=\sum_{p}\sum_{v\in I}K_p(u,v)^2$. For each of four sign laws $\ell$, the matrix is $M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v)$. We report local-diagonal normalization $M_\ell(u,v)/\sqrt{G(u)G(v)}$ and a pooled scalar normalization based only on calibration-origin geometry. The fixed band keeps block distance at most three; the full-relative band keeps all block pairs. We use $Q\in\{2048,8192\}$ and block length 128.

# Forecast interface

For a cell, let $S_N$ be the mean band spectral diagnostic over the relevant origins. The parent exponent $\alpha_{\rm P}$ is read from the hashed TPC-388 certificate and is not refit. The local exponent is fitted only from the two current calibration means: $$\alpha_{\rm L}=
 \frac{\log(S_{1024}/S_{768})}{\log(1024/768)}.$$ The anchored forecasts and the recursive forecast are $$\widehat S_{1280}^{\rm P}
   =S_{1024}(1280/1024)^{\alpha_{\rm P}},\qquad
 \widehat S_{1280}^{\rm L}
   =S_{1024}(1280/1024)^{\alpha_{\rm L}},$$ $$\widehat S_{1280}^{\rm rec}
   =S_{768}(1280/768)^{\alpha_{\rm P}}.$$ The holdout ratio is $S_{1280}/\widehat S_{1280}-1$; the finite pass cap is $|\text{ratio}|\leq0.03$. No ratio is interpreted outside this declared finite panel.

# Certification and results

The canonical certificate contains 256 rows and 32 cells. The producer accumulates prime shells in ascending order; an independent implementation rebuilds them in descending order and recomputes row values and all forecast cells. A rational 13-point $Q=8$ anchor at $[2800001,2800014)$ verifies positive geometry and symmetry for all four laws. A 25-mutation stress test rejects altered roles, hashes, summaries, and firewall values.

| quantity                           |               result|
|:-----------------------------------|--------------------:|
| parent anchored pass               |                32/32|
| local-control pass                 |                32/32|
| recursive parent pass              |                32/32|
| maximum parent error               |         0.0176155841|
| maximum local error                |         0.0119975160|
| maximum recursive error            |         0.0299499406|
| stable cells ($N=768,1024,1280$)   |  24/32, 27/32, 24/32|
| spectral failures / Schur failures |        64/256, 0/256|

: Finite forecast and stability census.

The strongest anchored deviation is the fixed-three-block, pooled, all-plus cell at $Q=8192$. The strongest recursive deviation is fixed-three-block, pooled, half-split at $Q=2048$. The latter is close to, but still inside, the finite cap. This proximity is a stress observation, not a margin for an asymptotic theorem. The 64 spectral failures occur while all Schur diagnostics remain below their cap, so the finite forecast success does not repair the operator-norm obstruction.

# Conclusion and next clue

TPC-389 supplies one independent finite progress point: a frozen slope remains predictive over a longer count horizon on a third coordinate family, under anchored, local, and recursive tests. The reusable structure is $$\text{hashed parent interface}\longrightarrow
 \text{fresh calibration/holdout ladder}\longrightarrow
 \text{three forecast audits}.$$ The strongest obstruction is the growing spectral-cap failure census, together with the recursive error being near the declared boundary. The open theorem is a source-valid, origin/count-uniform growing operator and slope control. The next clue is $$\texttt{ROUND2\_CLUE=TEST\_C1\_RECURSIVE\_SLOPE\_COMPOSITION}.$$ Arithmetic reassembly, Route-A/Route-B closure, and a twin-prime theorem remain open.

# Reproduction

All source, certificate, proof, experiment, and Bridge-B files are stored under the project directory:

[papers/tpc-389-c1-long-horizon-slope-stress/](..)

Run the ordinary and optimized producer, independent checker, mutation stress, and local Bridge-B commands listed in the project README. The release uses `paper/main.pdf` and `paper/paper.pdf` as byte-identical copies.

<!-- SOURCE_BODY_END -->
