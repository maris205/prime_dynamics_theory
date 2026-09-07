# TPC-392: A Finite Normalization Phase Diagram for a $c=1$ Proxy

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 5, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-391 localized a finite forecast obstruction for a frozen interface. The next question is whether the finite phase depends on the normalization used to convert the source matrix into a spectral diagnostic. TPC-392 predeclares a fresh coordinate-disjoint family, two calibration counts, two terminal holdout origins, four sign laws, and four normalizations on a fixed three-block band. The resulting certificate has 256 rows and 32 phase cells. All three scalar normalizations pass the 3% calibration-to-holdout forecast cap in all eight law/$Q$ cells; local-diagonal normalization passes in seven of eight. Its only failure is the alternating-index, $Q=8192$ cell, with error $0.0341068507$. The scalar choices change the finite level by about 2.1%–3.7% relative to local diagonal scaling. These results are a scoped numerical phase diagram for a $c=1$ proxy, not an asymptotic, arithmetic, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC-391 found that a frozen count-slope interface can disagree with a fresh terminal response while a same-family local control remains inside the transfer cap. That experiment leaves a more basic ambiguity: the diagnostic itself may depend on how the row geometry is normalized. TPC-392 holds the near-block band and the response laws fixed and compares four normalization choices on a new family.

The affine candidate grid is $$a_j=3800001+401j,\qquad 0\leq j<41,$$ with retained indices $0,10,20,30,40$. The first three origins are measured at $N=1024,1280$ for calibration; the last two are measured only at the predeclared terminal holdout $N=1536$. No response is used to choose an origin, count, law, band, or normalization. The TPC-391 parent is hashed as a frozen historical interface reference, but its slope is not used in the current fit.

Our firewall is $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ The official Session evaluator files are absent from this checkout, so the local Route-B evidence below is fail-closed artifact evidence only.

# Finite proxy and normalization panel

For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, define $$\begin{aligned}
 K_p(u,v)={}&p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac{1}{p-1}\right)\\
 &\quad\cdot\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.\end{aligned}$$ The row geometry and signed matrix are $$G(u)=\sum_{p}\sum_{v\in I}K_p(u,v)^2,
 \qquad M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v).$$ The fixed band retains pairs of blocks whose indices differ by at most three. We use $Q\in\{2048,8192\}$ and the four laws all-plus, alternating-index, mod-$4$ character, and half-split.

The panel compares the following predeclared choices:

1.  local diagonal: $M_\ell(u,v)/\sqrt{G(u)G(v)}$;

2.  pooled train scalar: the calibration-origin mean geometry at each count, extrapolated to 1536 by the calibration log slope;

3.  origin scalar: the current-origin mean geometry at that count;

4.  frozen train-1024 scalar: the pooled calibration mean at 1024 for all three counts.

For each choice, let $S_N$ be the mean band spectral diagnostic over the origins available at count $N$. The finite calibration slope and terminal forecast are $$\alpha=\frac{\log(S_{1280}/S_{1024})}{\log(1280/1024)},
 \qquad \widehat S_{1536}=S_{1024}(1536/1024)^\alpha.$$ The phase cap is $|S_{1536}/\widehat S_{1536}-1|\leq0.03$.

# Certification protocol

The producer evaluates the prime shell in ascending order and writes a canonical JSON certificate only after all 256 rows are complete. An independent implementation evaluates the same finite source in descending shell order, reconstructs every row, and recomputes the phase cells and aggregates without importing the producer. A rational 13-point, $Q=8$ anchor at $[3800001,3800014)$ checks positive geometry and symmetry for all four laws. The mutation suite applies 25 altered-provenance, role, row, summary, and firewall payloads; each must be rejected.

The finite status labels are deliberately narrow: $$\begin{array}{ll}
\text{panel and definitions:}&\text{PROVED\_EXACT\_FINITE},\\
\text{phase and forecast counts:}&\text{NUMERICALLY\_CERTIFIED\_FINITE\_SCOPED},\\
\text{source-valid normalization and growing bounds:}&\text{OPEN},\\
\text{arithmetic advance and twin-prime result:}&\text{NO / NONE}.
\end{array}$$

# Finite results

Table [1](main.tex#L126){reference-type="ref" reference="tab:phase"} reports the sealed certificate. There are eight cells per normalization (four laws and two $Q$ values).

<div id="tab:phase">

| normalization            |  forecast pass|  max absolute error|  terminal mean|
|:-------------------------|--------------:|-------------------:|--------------:|
| local diagonal           |            7/8|        0.0341068507|   0.2252440026|
| pooled train scalar      |            8/8|        0.0275714874|   0.2299425502|
| origin scalar            |            8/8|        0.0289630000|   0.2302511268|
| frozen train-1024 scalar |            8/8|        0.0275714874|   0.2335560798|

: TPC-392 normalization phase diagram.

</div>

The only failing cell is local diagonal with the alternating-index law at $Q=8192$; its signed forecast error is $+0.034106850682897649$. The largest scalar error is $0.028962999969161629$, so all three scalar choices remain inside the declared cap. At the terminal holdout, the means are ordered $$\text{frozen train-1024} > \text{origin} > \text{pooled train} >
 \text{local diagonal}.$$ Relative to local diagonal, the three scalar terminal means have ratios about $1.0369$, $1.0222$, and $1.0209$, respectively. Thus normalization changes the finite level while preserving a largely common trajectory on this panel; the high-$Q$ alternating cell is the one visible forecast separation.

The within-one-percent origin-spread census is 25/32 at $N=1024$, 28/32 at $N=1280$, and 24/32 at the terminal holdout. Spectral-envelope failures are 16 per normalization (64/256 total), while Schur-envelope failures are 0/256. These counts are diagnostics of the declared finite envelope, not analytic operator bounds.

# Interpretation and next clue

The strongest positive result is the three-way scalar 8/8 forecast pass. The strongest obstruction is that local diagonal scaling alone misses the cap in one predeclared high-$Q$ alternating cell. This supports a finite normalization-phase distinction, but it does not establish that any scalar choice is valid for the source operator in a growing limit. In particular, origin uniformity, count uniformity, a growing operator bound, and the arithmetic $L^2$ reassembly gate remain open.

The reusable structure is a response-blind normalization panel coupled to a fixed holdout role and an independent reverse-shell replay. The next clue is $$\texttt{ROUND2\_CLUE=TEST\_C1\_NORMALIZATION\_ADVERSARIAL\_HOLDOUT}.$$ The natural next experiment is a fresh family chosen before responses are read, designed specifically to test whether the scalar advantage survives an adversarial holdout. No arithmetic power credit is assigned.

# Reproduction

All code, certificate, proof package, notes, and Bridge-B files are stored in the TPC-392 project directory. Run the ordinary and optimized producer, independent checker, mutation stress, and Bridge-B commands in the project README. The release requires `paper/main.pdf` and `paper/paper.pdf` to be byte-identical.

<!-- SOURCE_BODY_END -->
