# Block-local phase localization of a finite count-2048 prime-shell operator audit

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China
- **Source date:** September 3, 2026
- **Repository source commit:** `11cec020855d42e47f2e61a386f7a97665edb398`

## Abstract

We study the next finite question raised by a count-2048 prime-shell audit: whether its beta=2 high-shell spectral-cap failures are already visible in a short local phase. Three response-blind origins are inherited, each 2048-point window is partitioned into eight contiguous blocks of length 256, and the literal weighted congruence operator is recomputed on every block for three shell scales, four sign laws, and beta equal to 0 or 2. The resulting 576-row certificate has no beta=2 spectral or Schur-cap violation; its largest normalized spectral value is 0.5536333251967529. The beta=0 control has 72 violations of each kind. Thus, on this declared panel, the hypothesis that a parent beta=2 failure is already present in one independently normalized 256-point block is refuted. The normalization changes with the domain, so the result is a localization obstruction rather than a causal cross-block theorem. All claims are finite and scoped; no arithmetic or twin-prime consequence is asserted.

# Question and scope

The preceding TPC-370 audit used the three origins \(1010001,1018021,1026041\) and found six beta=2 spectral-cap failures in the full count-2048 object: the all-plus law at \(Q=2048\) and \(8192\), once at each origin. Its maximum normalized spectral value was 0.71099989528234753. This paper asks the smallest structural follow-up: does the same phenomenon occur inside one short contiguous phase of the window?

The question is deliberately finite. A positive answer would identify a local obstruction worth refining. A negative answer would eliminate the simplest local explanation, while leaving open interactions between blocks and the effect of changing the normalization domain. We do not infer an asymptotic statement from either outcome.

# Finite operator and frozen protocol

For a prime \(p\) with \(Q<p\leq 2Q\), define \[B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid u-t}-\frac{1}{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.\] For beta \(\beta\in\{0,2\}\) and a fixed sign law \(\varepsilon\), the block-local matrix and its row geometry are \[A(u,t)=\sum_{Q<p\leq2Q}\varepsilon_p\left(\frac pQ\right)^\beta B_p(u,t),
 \qquad
 G(u)=\sum_{Q<p\leq2Q}\sum_{s\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,s)\right]^2,\] \[T(u,t)=\frac{A(u,t)}{\sqrt{G(u)G(t)}}.\] Here \(I=\{a+256b,\ldots,a+256b+255\}\), where \(a\) is one of the three origins and \(b=0,\ldots,7\).

The protocol was fixed from the TPC-370 routing clue before the formal certificate replay. The origin grid is \(1010001+401j\), with indices \(0,20,40\); the shell anchors are \(512,2048,8192\), the kernel exponent is one, and the four laws are all-plus, alternating-index, mod-4 character, and half-split. Every Cartesian-product row is retained, giving \(3\cdot8\cdot3\cdot4\cdot2=576\) rows. No block is selected using a response, source vector, or geometry score.

The inherited exact anchor is the interval \([1010346,1010359)\), at \(Q=4\), exponent one, with shell \(\{5,7\}\). It is checked separately and does not select a main-panel row.

# Exact finite facts and certification

The block partition is an integer partition, and each entry of \(G\) is a finite sum of rational squares. Hence positivity can be checked exactly on the declared finite blocks. The resulting matrices are symmetric. For any finite real symmetric matrix, \[\left\lVert T\right\rVert_{2}\leq \max_u\sum_t|T(u,t)|,
 \qquad
 \left\lVert T\right\rVert_{2}\leq \left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.\] The certificate stores both envelopes and the true extremal eigenvalues.

The producer accumulates the shell in increasing order. An independent checker implements its own sieve and accumulates in descending shell order; it recomputes all geometry, raw metrics, normalized metrics, eigenvalue endpoints, and phase counts. A mutation suite tests the protocol, partition, row census, digests, inherited anchor, firewall, and routing clue. The local Bridge-B checker additionally runs normal and optimized Python modes, requires empty standard error, and compares their standard output byte-for-byte.

# Results

Table [1](#tab:census) gives the complete phase census. The beta=2 maximum is well below both working caps, while the unweighted beta=0 control retains a strong all-plus phase.

<div id="tab:census">

| \(\beta\) | rows | spectral violations | Schur violations |       max spectral |
| --------: | ---: | ------------------: | ---------------: | -----------------: |
|         0 |  288 |                  72 |               72 | 1.4642797645332997 |
|         2 |  288 |                   0 |                0 | 0.5536333251967529 |

Complete block-local finite census.

</div>

For beta=2, the maxima at \(Q=512,2048,8192\) are respectively 0.54979749502051356, 0.55258383785942589, and 0.5536333251967529. No one of the 24 declared origin/block locations crosses the spectral cap 0.64 or the Schur cap 0.83. By contrast, the parent full-window object has six beta=2 high-\(Q\) failures. The finite observation therefore rules out the narrow local hypothesis \[\text{``a parent failure must occur in one independently normalized
  256-point block.''}\] This is a scoped refutation, not a statement about every partition or every normalization.

# Interpretation and next step

The local and full-window matrices are normalized with different geometries. Consequently, the absence of a local failure does not prove that off-block entries cause the parent failure. It only says that the failure is not captured by this family of independently normalized local objects. The next predeclared audit should retain the full-window normalization and decompose the matrix into its fixed block-diagonal and off-block parts. That experiment can test whether the finite excess survives in a component with a common normalization.

# Claim firewall

    TPC371_BLOCK_LOCAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_576_ROWS
    TPC371_BETA2_LOCAL_FAILURE = REFUTED_SCOPED
    TPC371_CROSS_BLOCK_COHERENCE = OPEN
    TPC371_ARITHMETIC_ADVANCE = NO
    TPC371_FIXED_POWER_CREDIT = 0
    TPC371_FULL_GATE_B = OPEN
    TPC371_TWIN_PRIME_RESULT = NONE

The Session-named official Route-A/Route-B evaluator files are not present in this checkout. The local bridge is repository evidence only. In particular, this paper proves no source-uniform arithmetic \(L^2\) estimate, no growing operator bound, no prime-shell reassembly, and no twin-prime theorem.

#### Reproducibility.

The canonical certificate, source code, independent checker, stress suite, proof package, and PDF are stored in `papers/tpc-371-block-phase-localization/`. The project records the exact inherited anchor and all 576 row records in `results/tpc371_certificate.json`.
