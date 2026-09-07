# Cross-Origin Replication of a Finite Source–Scale Prime–Shell Spectral Ladder

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST)
- Source date: September 1, 2026
- Source repository commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`
- Converter: `source-markdown-audit-v2`

## Abstract

Finite source–scale experiments can be misleading if their profile is tied to one residue environment. We therefore repeat the complete TPC–325 four-rung ladder at a second, disjoint origin. The literal deleted-diagonal centered prime-shell blocks, shell anchors, height, exponents, and four sign laws are unchanged; only the source origin is moved from $12001$ to $16001$. The new panel has $32$ rows over source counts $160,320,640,1280$. The all-plus coherent normalized spectral profile strictly majorizes the direct profile on all $32$ rows. The four-law profile census agrees exactly with the parent panel, and the new all-plus total-variation and energy envelopes agree with the parent within predeclared finite thresholds. Independent reverse reconstruction, residue-perturbation stress, exact rational anchoring, and normal/optimized replay all pass. This is a finite cross-origin replication certificate only: it supplies no uniform-in-source theorem, arithmetic $L^2$ cancellation, power saving, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC–325 found a four-rung profile pattern at the fixed origin $12001$. The minimal adversarial question is whether the pattern survives a genuinely different residue environment. We use $$I_N=[16001,16000+N/2]\cap\mathbb Z,\qquad
 N\in\{320,640,1280,2560\}.$$ The four source counts are consequently $160,320,640,1280$. For a prime $p\in(Q,2Q]$, let $$B_{p,N}^{(s)}(u,t)=p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
\left({\bf 1}_{p\mid u-t}-\frac1{p-1}\right)
{\bf 1}_{u\ne t}{\bf 1}_{p\nmid u}{\bf 1}_{p\nmid t},
\qquad H=66.$$ The direct and signed Gram matrices are $$G_0(N)=\sum_p B_p^*B_p,\qquad
 G_e(N)=\left(\sum_p e_pB_p\right)^*
                 \left(\sum_p e_pB_p\right).$$ Thus $G_e=(\sum_p e_pB_p)^*(\sum_p e_pB_p)$ throughout. The sign menu is all-plus, index-alternating, the mod-$4$ character, and half-split signs.

For a positive-trace Gram matrix $G$, define $$\pi(G)=\left(\frac{\lambda_1(G)}{\operatorname{tr}G},\ldots,
 \frac{\lambda_d(G)}{\operatorname{tr}G}\right),
 \qquad \lambda_1\geq\cdots\geq\lambda_d.$$ The release claim is deliberately finite:

> **NUMERICALLY CERTIFIED FINITE:** the new origin reproduces the parent profile census on $32$ rows and the all-plus ladder passes the declared envelope and positivity tests.

# Frozen operator and cross-origin test

Every displayed Gram matrix is a finite Gram matrix, hence positive semidefinite. Its trace-normalized decreasing spectrum is therefore a probability vector whenever the trace is positive. This exact finite typing is separate from the numerical comparison of profiles; see, for example, `\cite{horn2013matrix}` for the underlying finite-dimensional spectral facts.

The source origin is the only intervention relative to TPC–325. The intervals are strictly nested: $$[16001,16160]\subset[16001,16320]\subset[16001,16640]
\subset[16001,17280].$$ They are disjoint from the earlier source panels, including the parent origin $12001$ ladder. The stress suite also compares every active residue mask with its one-step shifted version; this prevents the replication from being presented as a formal translation identity.

For each rung, the all-plus TV lower envelope is the minimum of the eight row values, and the all-plus energy upper envelope is the maximum of the signed/direct trace ratios. We compare these finite diagnostics with the parent using thresholds $0.001$ and $0.005$, respectively. These thresholds are controls for this experiment, not asymptotic error terms.

# Certified results

Table [1](main.tex#L107){reference-type="ref" reference="tab:ladder"} reports the new-origin all-plus ladder. Every row has a positive recorded lower endpoint for the interior prefix tests; all $32$ rows pass strict majorization.

<div id="tab:ladder">

|   $N$|  $|I_N|$|  minimum prefix lower|  TV lower envelope|  energy upper envelope|
|-----:|--------:|---------------------:|------------------:|----------------------:|
|   320|      160|    $1.24826\,10^{-5}$|           0.285054|               8.904796|
|   640|      320|    $3.25191\,10^{-4}$|           0.211087|               6.864730|
|  1280|      640|    $6.92074\,10^{-5}$|           0.190246|               6.249096|
|  2560|     1280|    $1.64549\,10^{-5}$|           0.170044|               5.998423|

: All-plus finite ladder at the second origin.

</div>

The profile-majorization census is shown below. The new counts exactly match the parent counts:

| sign law          |  signed majorizes|  mixed|  direct majorizes|
|:------------------|-----------------:|------:|-----------------:|
| all-plus          |                32|      0|                 0|
| alternating index |                21|     11|                 0|
| mod-$4$ character |                26|      6|                 0|
| half-split        |                23|      9|                 0|

The corresponding energy-side census is also unchanged: all-plus is below one on $4/32$ rows and above one on $28/32$ rows (with the same side-counts for the other laws as recorded in the canonical certificate). Thus the second origin reproduces both the shape classification and the amplitude-side census, while not selecting an arithmetic sign law.

At the exact rational anchor $[16001,16016]$, $Q=4$, $s=1$, the direct and index-alternating energies have SHA–256 digests `e9855d70...ff97fe2d0` and `d97b7e1b...97afae136`. Their decimal values are approximately $1318.7472759963152$ and $1380.0905068064244$, with signed/direct ratio $1.0465162900630558$. The canonical JSON retains the complete rational numerator/denominator identities.

# What the replication establishes

The strongest conclusion is a finite adversarial one: the TPC–325 readout is not falsified by moving the source origin to this second disjoint panel. The exact census match and the small envelope discrepancies are useful control evidence for the finite operator experiment. They do not establish source universality. In particular, four rungs at two origins do not imply a growing-scale limit, and the threshold comparison does not quantify an analytic error term.

The operator still has no Möbius or von Mangoldt weighting and no source-native signed arithmetic estimate. Consequently, $$\texttt{ARITHMETIC\_ADVANCE = NO},\qquad
\texttt{FIXED\_POWER\_CREDIT = 0},\qquad
\texttt{FULL\_GATE\_B = OPEN}.$$ The Session-named official Route-A and Route-B evaluator files are absent from this checkout. The local Bridge-B checker is fail-closed and is not an official evaluator pass.

# Reproducibility

The project contains the locked parent provenance, canonical certificate, independent reverse/einsum checker, cross-origin stress audit, derivation and proof packages, and this manuscript. From the repository root:

    cd papers/tpc-326-cross-origin-scale-replication
    python -B code/tpc326_cross_origin_scale_replication.py --check
    python -B experiments/tpc326_independent_checker.py --check
    python -B experiments/tpc326_cross_origin_stress.py --check

The optimized counterparts and local Bridge-B normal/optimized equality check are part of the release contract. The machine-readable result is `results/tpc326_certificate.json`; the final manuscript is `paper/paper.pdf`.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{horn2013matrix,
  author    = {Roger A. Horn and Charles R. Johnson},
  title     = {Matrix Analysis},
  edition   = {2},
  publisher = {Cambridge University Press},
  year      = {2013}
}
```

<!-- SOURCE_BODY_END -->
