# Extremal-eigenmode separation by block distance in a finite count-2048 prime-shell operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 3, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We resolve the extremal eigenmode of a finite count-2048 prime-shell operator into eight fixed block-distance Rayleigh layers. The complete panel contains three response-blind origins, three shell scales, the all-plus law, and beta equal to 0 or 2. All 18 matrices select their minimum-eigenvalue mode, and the same-block layer is the largest individual contribution. On all six beta=2 high-scale failure rows, the eight layer terms have the same negative sign; distances zero through three carry at least 99.157 percent of absolute Rayleigh mass, while distances four through seven carry at most 0.843 percent. This is a finite near-block signed-coherence certificate, not a causal attribution, a uniform decay theorem, or a twin-prime consequence.

<!-- SOURCE_BODY_BEGIN -->

# Question and frozen panel

The preceding common-normalization audit wrote the full operator as a fixed block-diagonal part plus its off-block remainder. Neither component alone crossed the working spectral cap on the beta=2 failure rows, although their sum did. We now ask the next smaller question: along the full matrix’s extremal eigenvector, which fixed block separations contribute to the Rayleigh quotient?

The origins are (1010001,1018021,1026041). Each window has 2048 points, split into eight contiguous blocks of length 256. We evaluate all $Q\in\{512,2048,8192\}$, exponent one, the all-plus law, and $\beta\in\{0,2\}$, for 18 rows. Every row and every block-distance mask is declared before the response is read. The extremal-mode rule selects the eigenvalue of greatest absolute value, with the minimum eigenvalue winning an exact tie.

# Operator and exact layer identity

For $Q<p\leq2Q$, let $$B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid u-t}-\frac{1}{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.$$ On the full interval $I$, define $$A(u,t)=\sum_{Q<p\leq2Q}\left(\frac pQ\right)^\beta B_p(u,t),
 \quad
 G(u)=\sum_{Q<p\leq2Q}\sum_{s\in I}
 \left[\left(\frac pQ\right)^\beta B_p(u,s)\right]^2,$$ and $T(u,t)=A(u,t)/\sqrt{G(u)G(t)}$. The same full-window geometry is used throughout.

If $b(i)=\lfloor i/256\rfloor$, set $$L_d(i,j)=\mathbf 1_{|b(i)-b(j)|=d}T(i,j),\qquad 0\leq d\leq7.$$ The masks are disjoint and exhaustive, so $T=\sum_{d=0}^7L_d$ entrywise. For the selected unit eigenvector $v$, with $Tv=\lambda v$, define $c_d=v^{\mathsf T}L_dv$. Linearity gives the exact finite identity $$\sum_{d=0}^7c_d=v^{\mathsf T}Tv=\lambda.$$ We report both signed fractions $c_d/\lambda$ and absolute fractions $|c_d|/\sum_e|c_e|$. The latter is descriptive and is not a norm decomposition.

# Certification

The producer computes all rows using ascending prime-shell order. An independent checker has its own sieve, uses descending shell order, rebuilds every normalized matrix and eigensystem, and compares all layer terms and residuals. An adversarial suite mutates protocol, parent provenance, mode selection, layer census, numerical errors, and claim fields. Local Bridge-B repeats each check in normal and optimized Python modes with empty standard error and byte-identical output required. The separate rational anchor $[1010346,1010359)$, at $Q=4$ and shell $\{5,7\}$, does not select a panel row.

The maximum layer reconstruction error is zero in the stored arrays, the maximum Rayleigh-sum error is $2.665\times10^{-15}$, and the largest infinity-norm eigen-residual is $8.084\times10^{-16}$.

# Finite results

Table [1](main.tex#L107){reference-type="ref" reference="tab:census"} gives the complete mode census. The working spectral and Schur caps are 0.64 and 0.83.

<div id="tab:census">

| $\beta$ |  rows|  min. mode|  distance-0 dominant|  spectral failures|  Schur failures|
|:--------|-----:|----------:|--------------------:|------------------:|---------------:|
| 0       |     9|          9|                    9|                  9|               9|
| 2       |     9|          9|                    9|                  6|               0|

: Finite full-panel census.

</div>

For beta=2, cross-block distances carry between (0.3204176539) and (0.3441539224) of the absolute Rayleigh mass. The total share at distances four through seven never exceeds (0.0084288236). The six parent failures occur at all three origins and $Q=2048,8192$. On these six rows every $c_d$ is negative, so there is no layer-level sign cancellation in the selected negative mode. Their absolute mass ranges are summarized in Table [2](main.tex#L129){reference-type="ref" reference="tab:layers"}.

<div id="tab:layers">

| block-distance group |    observed range|
|:---------------------|-----------------:|
| $d=0$                |  65.5846–65.5853%|
| $d=1$                |  28.1747–28.1753%|
| $d=2$                |  4.05997–4.06004%|
| $d=3$                |  1.33717–1.33723%|
| $4\leq d\leq7$       |  0.84264–0.84288%|

: Absolute Rayleigh-mass ranges over the six beta=2 failure rows.

</div>

Thus the parent failure mode is neither purely block diagonal nor diffusely spread across all block separations. It has a stable finite near-block profile: the same-block term is largest, the nearest off-block layer is substantial, and distances zero through three account for at least 99.157 percent of absolute mass.

# Interpretation and limits

The same-sign layer census removes one possible explanation for the six failure rows: at this partition scale, their selected extremal quotient is not created by cancellation among block-distance terms. It does not show that the near-block entries cause the spectral excess. A Rayleigh profile of one data-dependent eigenvector is not an operator-norm bound for a truncated band, and the panel supplies no origin-, window-, or shell-uniform decay law. The next finite test is therefore a predeclared near-block band truncation, not an asymptotic promotion.

    TPC373_RAYLEIGH_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC373_CROSS_BLOCK_DECAY = OPEN
    TPC373_CROSS_BLOCK_CAUSALITY = OPEN
    TPC373_ARITHMETIC_ADVANCE = NO
    TPC373_FIXED_POWER_CREDIT = 0
    TPC373_FULL_GATE_B = OPEN
    TPC373_TWIN_PRIME_RESULT = NONE

No source-uniform arithmetic $L^2$ estimate, growing operator bound, prime-shell reassembly, official Route-A/Route-B closure, or twin-prime theorem is claimed. The official evaluator files are absent; local Bridge-B is repository evidence only.

<!-- SOURCE_BODY_END -->
