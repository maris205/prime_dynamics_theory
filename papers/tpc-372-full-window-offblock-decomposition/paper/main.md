# A common-normalization block/off-block decomposition of a finite count-2048 prime-shell operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 3, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We decompose the finite full-window operator from a count-2048 prime-shell audit into a fixed block-diagonal component and an off-block component, using one common normalization. The panel contains three response-blind origins, three shell scales, the all-plus law, and beta equal to 0 or 2. For beta=2, the full matrix has six spectral-cap failures at high shell scale, but neither component alone crosses the cap. On every failing row the reverse triangle inequality gives a positive lower bound for the off-block norm. This records a finite sum/coherence obstruction and removes the normalization ambiguity of an independently normalized short-block audit. It does not prove causal cross-block attribution, an asymptotic theorem, or any twin-prime consequence.

<!-- SOURCE_BODY_BEGIN -->

# Motivation and frozen panel

The preceding block-local audit found no beta=2 cap failure in any of 24 independently normalized 256-point blocks, although the full count-2048 object had six high-$Q$, all-plus failures. A local matrix and a principal submatrix of a globally normalized matrix are different objects. We therefore retain the full-window normalization and split the resulting matrix directly.

The three origins are $1010001,1018021,1026041$, inherited from the fixed grid $1010001+401j$ at indices $0,20,40$. The window has 2048 points and is partitioned into eight fixed contiguous blocks of length 256. We evaluate all $Q\in\{512,2048,8192\}$, exponent one, the all-plus law, and $\beta\in\{0,2\}$, giving 18 rows. The protocol is fixed before component metrics are read; no response or geometry ranking selects a row.

# Operator and decomposition

For $Q<p\leq2Q$, let $$B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid u-t}-\frac{1}{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.$$ On the full interval $I$, define $$A(u,t)=\sum_{Q<p\leq2Q}\left(\frac pQ\right)^\beta B_p(u,t),
 \qquad
 G(u)=\sum_{Q<p\leq2Q}\sum_{s\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,s)\right]^2,$$ and $T(u,t)=A(u,t)/\sqrt{G(u)G(t)}$. Let $P$ be the fixed mask that keeps entries in the same 256-point block. The two components are $$D=P\odot T,\qquad R=(1-P)\odot T,qquad T=D+R.$$ All three matrices use the same $G$. The inherited exact anchor is $[1010346,1010359)$ at $Q=4$, exponent one, shell $\{5,7\}$; it is checked separately and does not select a panel row.

# Finite certification

The decomposition identity is an exact finite entrywise identity. For finite real symmetric matrices, the reverse triangle inequality gives $$\left\lVert R\right\rVert_2\geq \left\lVert T\right\rVert_2-\left\lVert D\right\rVert_2,
 \qquad
 \left\lVert T\right\rVert_2\leq\left\lVert D\right\rVert_2+\left\lVert R\right\rVert_2.$$ The geometry is a finite sum of rational squares, and the Schur and Frobenius quantities are independent finite envelopes for the spectral norm.

The producer accumulates prime shells in increasing order. An independent checker uses its own sieve and descending-shell accumulation, reconstructs the full matrix, applies the fixed mask, and compares all component metrics, eigenvalue endpoints, lower bounds, and phase counts. An adversarial suite mutates protocol, parent lock, row data, decomposition data, anchor, and claim fields. The local Bridge-B reruns every check in normal and optimized Python modes and requires empty standard error and byte-identical output.

# Results

Table [1](main.tex#L101){reference-type="ref" reference="tab:components"} summarizes the complete beta census. The working spectral and Schur caps are 0.64 and 0.83, respectively.

<div id="tab:components">

| $\beta$ |  full spectral|  diagonal spectral|  off-block spectral|  full Schur|
|:--------|--------------:|------------------:|-------------------:|-----------:|
| 0       |              9|                  9|                   6|           9|
| 2       |              6|                  0|                   0|           0|

: Finite component census.

</div>

For beta=2, the largest normalized spectral values over the 9 rows are $$\max\left\lVert T\right\rVert_2=0.71099989528234753,\quad
 \max\left\lVert D\right\rVert_2=0.51702415681590108,\quad
 \max\left\lVert R\right\rVert_2=0.26329369743038339.$$ The six full failures are exactly the three origins at $Q=2048,8192$. On each such row, $\left\lVert D\right\rVert_2<0.64<\left\lVert T\right\rVert_2$, so the recorded lower bound $\left\lVert T\right\rVert_2-\left\lVert D\right\rVert_2$ is positive (approximately 0.1936–0.1940). At the same time $\left\lVert R\right\rVert_2<0.64$. Thus neither component alone crosses the cap, while their common-normalization sum does.

The beta=0 control has nine full spectral and nine full Schur failures; its block-diagonal component also retains a strong all-plus phase. This control does not alter the beta=2 interpretation.

# Interpretation and limits

The result proves a finite necessity statement: on the six beta=2 failure rows, an off-block contribution of at least the reverse-triangle lower bound is required to bridge the diagonal norm to the full norm. It does not prove that the off-block entries cause the failure, because a norm of a sum can reflect signed coherence and cancellation in ways not captured by component norms. It also says nothing about other partitions, origins, windows, or limits.

    TPC372_DECOMPOSITION_IDENTITY = NUMERICALLY_CERTIFIED_FINITE
    TPC372_OFF_BLOCK_NECESSITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC372_CROSS_BLOCK_CAUSALITY = OPEN
    TPC372_ARITHMETIC_ADVANCE = NO
    TPC372_FIXED_POWER_CREDIT = 0
    TPC372_FULL_GATE_B = OPEN
    TPC372_TWIN_PRIME_RESULT = NONE

No source-uniform arithmetic $L^2$ estimate, growing operator bound, prime-shell reassembly, Route-A/Route-B closure, or twin-prime theorem is claimed. The official Session evaluator files are absent; local Bridge-B is repository evidence only.

#### Reproducibility.

The complete certificate and proof package are stored in the TPC-372 project; the canonical row records are in `tpc372_certificate.json` and the compiled manuscript is `paper.pdf`.

<!-- SOURCE_BODY_END -->
