# Twin-Isolated Source Norms in a Finite Prime-Shift Model

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-334 found that the source polarization cross term is dominated by odd composite predecessors of a prime shift rather than by twin-prime pairs. We now apply the same support masks to the full residual vector $\beta=\Lambda-b$. Because the masks are disjoint, the residual Euclidean norm splits exactly into twin, non-twin prime-shift, higher prime-power, and zero-cross-support parts. On two disjoint origins and three nested scales, twin coordinates carry $9.5561721\%$–$12.2415982\%$ of residual energy, the non-twin background carries $67.0497016\%$–$69.6569087\%$, and higher prime powers carry at most $0.1873706\%$. Twin residual energy is amplified relative to twin cross-term mass by a factor between $1.7065$ and $1.7706$. This is a finite source-level separation and a precise input for the next operator test; it is not a density estimate, power saving, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Motivation

The source vector in the session’s twin-prime dynamical bridge is $$\beta_o^{(2)}(t)=\Lambda(t+2)-b_o^{(2)}(t).$$ TPC-333 measured the polarization cross term and TPC-334 showed that its mass is mostly supported on $t+2$ prime with $t$ composite. That conclusion concerns one term in $\|\beta\|_2^2$, however. A natural follow-up is to ask whether the same background dominates the residual norm itself, and whether the twin coordinates are suppressed or amplified by subtraction.

We answer this on the exact finite panel inherited from those papers. The word “twin-isolated” means a coordinate mask, not a new asymptotic source.

# Finite source and masks

For $o\in\{42001,44001\}$ and $N\in\{2048,4096,8192\}$, let $$I_{o,N}=\{o,o+1,\ldots,o+N/2-1\}.$$ The declared source is $$\label{eq:source}
 \beta_o^{(2)}(t)=\Lambda(t+2)-2C_2\mathbf 1_{2\nmid t}
 \prod_{\substack{p\mid t\\p>2}}\frac{p-1}{p-2},$$ with the inherited finite Euler-tail cutoff $50000$ and midpoint guard. Define four coordinate classes: $$\begin{aligned}
 \mathsf T&=\{t:t,t+2\text{ prime}\},\\
 \mathsf B&=\{t:t+2\text{ prime},\ t\text{ not prime}\},\\
 \mathsf P&=\{t:t+2=p^k,\ k\ge2\},\\
 \mathsf Z&=I_{o,N}\setminus(\mathsf T\cup\mathsf B\cup\mathsf P).\end{aligned}$$ The last class is exactly the zero-cross-support complement; its residual entries need not be zero. Let $$\beta_C(t)=\beta(t)\mathbf 1_{t\in C},\qquad C\in\{\mathsf T,\mathsf B,\mathsf P,\mathsf Z\}.$$

# Exact masked norm identity

The classes are disjoint and exhaustive. Consequently, $$\label{eq:normsplit}
 \|\beta\|_2^2=\sum_{C\in\{\mathsf T,\mathsf B,\mathsf P,\mathsf Z\}}
 \|\beta_C\|_2^2.$$ This is simply a regrouping of a finite sum, but it is useful because it separates support from magnitude before any signed-Gram operator is applied. For comparison with TPC-334, define the twin amplification diagnostic $$A_{\mathsf T}=
 \frac{\|\beta_{\mathsf T}\|_2^2/\|\beta\|_2^2}
 {X_{\mathsf T}/\langle\Lambda,b\rangle},$$ where $X_{\mathsf T}$ is the twin cross-term mass. This ratio is a finite descriptive statistic, not a universal invariant.

# Certificate protocol

The producer is parent-locked to TPC-334 and rebuilds all six arrays. For each coordinate it independently tests primality of $t$, prime-power status of $t+2$, and then accumulates both residual squared norm and cross mass by class. It records partition residuals and all four class counts. A rational anchor uses $\beta=(2,-3,6,-1)$ with one coordinate in each class; the four squared norms are $4,9,36,1$ and sum to $50$ exactly.

The independent checker uses a separate trial sieve, reverse factorization, and reverse tail-product order. A mutation stress suite changes a row, masked value, summary census, firewall label, and anchor flag; all five mutations are rejected. The local Bridge-B wrapper is fail-closed and checks normal/optimized equality.

# Finite results

Table [1](main.tex#L115){reference-type="ref" reference="tab:shares"} gives the extrema over the six windows.

<div id="tab:shares">

| quantity                       |    minimum   |    maximum   |
|:-------------------------------|:------------:|:------------:|
| twin norm share                | 0.0955617209 | 0.1224159818 |
| non-twin background norm share | 0.6704970165 | 0.6965690875 |
| prime-power norm share         |       0      | 0.0018737060 |
| twin norm / twin cross share   | 1.7065194951 | 1.7705815591 |

: Residual norm shares and twin amplification.

</div>

All six twin norm shares lie in $(0.09,0.13)$, and all six background shares lie in $(0.65,0.72)$. The zero-cross-support class accounts for the remaining approximately $18.9\%$–$21.3\%$. The twin share of residual norm is larger than its $5.43\%$–$7.17\%$ share of the raw cross term by the amplification factor shown in the table, but it remains far below the non-twin background.

This observation refines the previous obstruction. Removing or modeling the background is necessary if one wants a twin-specific source, but doing so cannot be justified by saying that twin coordinates have no residual energy. They have a stable, non-dominant component on this panel.

# Claim firewall

The finite mask identity [\[eq:normsplit\]](main.tex#L79){reference-type="eqref" reference="eq:normsplit"} is `PROVED_EXACT_FINITE` for the declared arrays. The six-row norm ledger, independent replay, and mutation stress are `NUMERICALLY_CERTIFIED_FINITE`. The share and amplification ranges are `NUMERICAL_OBSERVATION`. A source-uniform $L^2$ theorem, a twin-prime density conclusion, strict $1/400$ payment, and full Gate B are `OPEN`; `ARITHMETIC_ADVANCE=NO` and `FIXED_POWER_CREDIT=0`. The official Session evaluator files are absent, so the local Bridge-B check is not an official route pass.

# Next question

The source-level twin component is neither dominant nor negligible. The next minimal experiment is to apply one fixed signed-Gram shell operator to the full, twin-isolated, and background residual vectors and record whether the operator preserves this ordering or creates a new placement obstruction.

<!-- SOURCE_BODY_END -->
