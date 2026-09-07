# TPC-387: Calibration-Only Count-Ladder Renormalization

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 4, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-386 showed that a finite $0.64$ spectral diagnostic does not survive a direct count increase from $512$ to $1024$. We test whether the increase can be predicted by an intermediate count without using holdout data. Three fresh origins are evaluated at $N=512$ and $N=768$ for calibration, and two later origins at $N=1024$ are held out. For every declared law, bandwidth mode, normalization, and $Q$, a logarithmic count slope is fitted from the two calibration means and extrapolated once. All 32 endpoint cells fall within a predeclared 3% finite error envelope; the worst error is 2.6051%. This is a reproducible finite repair of the endpoint comparison, not a count-uniform operator theorem and not an arithmetic result.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

We remain in one finite $c=1$ dynamical-system family. The preceding count holdout identified a cap obstruction, so the next minimal question is whether the obstruction follows a smooth ladder that can be learned before the endpoint. We keep the count roles and origin roles separate: the $N=512$ and $N=768$ observations at three origins are calibration, while two new origins at $N=1024$ are holdout.

The following firewall is part of the result: $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ The official Session Route-A/Route-B evaluator files are absent from this checkout. The local Bridge-B checker is therefore repository evidence only, and is fail-closed.

# Proxy and protocol

For $p\in(Q,2Q]$ define the same finite kernel as in TPC-386, $$\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{66^2}{66^2+(u-v)^2}
 \left({\bf 1}_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot{\bf 1}_{u\ne v}{\bf 1}_{p\nmid u}{\bf 1}_{p\nmid v}.\end{aligned}$$ The square-energy geometry is $$G(u)=\sum_{p\in(Q,2Q]}\sum_{v\in I}K_p(u,v)^2.$$ We use local diagonal normalization or a pooled scalar. The pooled scalar at $N=512$ and $N=768$ is the mean of $G$ over the three calibration origins; the $N=1024$ scalar is a log-count extrapolation of those two geometry means. Blocks have length 128. The fixed band retains block distance at most three, and the full-relative band retains all block pairs at each count.

The candidate grid is $a_j=2400001+401j$, $0\leq j<41$; indices $0,10,20,30,40$ are frozen before readout. We use $Q=2048,8192$, exponent one, $\beta=2$, height 66, and the four laws all-plus, alternating-index, mod-$4$ character, and half-split.

For a fixed cell let $S_{512}$ and $S_{768}$ be the calibration-origin means of the spectral diagnostic. The only fitted quantity is $$\alpha=\frac{\log(S_{768}/S_{512})}{\log(768/512)},
 \qquad \widehat S_{1024}=S_{768}(1024/768)^\alpha .$$ The holdout ratio $S_{1024}/\widehat S_{1024}$ is read only after this rule has been fixed. The 3% threshold is a finite audit convention, not an asymptotic assertion.

# Exact and computational certification

The canonical JSON certificate has 256 rows and 32 cells. It locks the TPC-386 producer and certificate, records all count roles, and is replayed by an independent implementation that sums the prime shell in reverse order. The mutation firewall rejects 25 structural mutations. At the exact anchor $Q=8$, the interval $[2400001,2400014)$ has shell $\{11,13\}$; rational arithmetic verifies positive geometry and symmetry for all four laws.

# Results

The stability counts at $N=512$, $N=768$, and the $N=1024$ holdout level are respectively $24/32$, $24/32$, and $28/32$. There are 40 rows above the inherited $0.64$ spectral diagnostic and no Schur-cap failures. All 32 calibration-slope predictions pass the 3% endpoint cap.

| band          | normalization |  $\alpha$|    predicted|      holdout|     ratio|
|:--------------|:--------------|---------:|------------:|------------:|---------:|
| fixed $c=3$   | local         |  0.105214|  0.667768953|  0.661289031|  0.990296|
| fixed $c=3$   | pooled        |  0.107198|  0.688171962|  0.675238108|  0.981205|
| full relative | local         |  0.128235|  0.678510049|  0.674101715|  0.993503|
| full relative | pooled        |  0.124306|  0.696381184|  0.686312465|  0.985541|

: All-plus $Q=8192$ calibration slopes and endpoint holdouts.

The largest absolute deviation from one over all 32 law/mode/normalization/ $Q$ cells is $0.0260511620$, attained by the alternating-index law at $Q=2048$ with fixed-three-block and pooled normalization. Thus the panel-wide success is not obtained by fitting only the all-plus endpoint. For the four all-plus high-$Q$ cells, the absolute errors are between $0.006497$ and $0.018795$.

The finite repair should be interpreted alongside the cap obstruction. A calibration slope predicts the observed count increase reasonably well, but the raw endpoint can still exceed $0.64$, and the fitted slope has no reason to remain stable for a growing sequence of counts. The signed laws are controls: their scales and endpoint spreads differ, so no law-uniform claim is made.

# Conclusion and next clue

The strongest positive result is a response-blind, origin-disjoint, calibration-only endpoint extrapolation that passes its 3% finite census. The strongest obstruction is the absence of a theorem making that slope uniform in count, origin, law, or source normalization. The reusable object is the locked ladder protocol with an independent reverse-shell replay. The next clue is $$\texttt{ROUND2\_CLUE=TEST\_C1\_COUNT\_LADDER\_SECOND\_HOLDOUT}.$$ No arithmetic reassembly or twin-prime conclusion follows.

# Reproduction

The complete source, proof package, certificate, checkers, and local Bridge-B record are in the project directory [papers/tpc-387-c1-count-ladder-renormalization/](..). The release requires ordinary and optimized Python checks, 25-mutation stress, and byte-identical copies of `main.pdf` and `paper.pdf`.

<!-- SOURCE_BODY_END -->
