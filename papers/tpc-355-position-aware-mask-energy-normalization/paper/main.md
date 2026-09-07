# Position-Aware Mask-Energy Normalization for a Finite Masked Twin-Prime Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 3 September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding finite source/operator audit transferred positive operator polarization to higher origins but showed a downward movement of its all-plus minimum floor. We test a predeclared, response-independent position-aware normalization. For each unsigned prime component $B_p$ we form the diagonal mask-energy $G_u=\sum_{p,t}B_p(u,t)^2$ and apply the symmetric congruence $A^\sharp=D_G^{-1/2}AD_G^{-1/2}$. The construction uses no source vector, sign law, or observed response. On three frozen panels and 648 law-level rows, the normalized all-plus minimum drop from the low-origin parent to the higher-origin parent is $0.0262369882$, versus $0.0421511462$ without normalization, a finite reduction fraction of $0.3775498289$. The repair is not uniform: the all-plus mean drop becomes larger, and a fresh mod-4 row is still negatively aligned. We therefore record a finite partial repair and a sharp obstruction, not an asymptotic arithmetic estimate or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

TPC-353 attached the finite V59 residual $\beta(t)=\Lambda(t+2)-b^{(2)}(t)$ to a literal two-endpoint divisibility-masked shell operator. TPC-354 moved the same construction to disjoint higher origins. Its positive alignment census survived, while the all-plus minimum and mean decreased relative to the low-origin parent.

The present question is deliberately narrower: can a normalization based only on the position-dependent unsigned mask geometry account for that minimum-floor movement? The answer is tested on the locked TPC-353 panel, the locked TPC-354 panel, and a fresh origins-only panel. Every conclusion below is classified as either an exact finite identity, a declared finite model statement, or a numerically certified finite observation. No statement here supplies a growing bound in $X$.

# Finite operator and normalization

Let $I$ be a finite integer interval and let $S_Q=\{p: p\text{ prime},\ Q<p\leq 2Q\}$. For exponent $s$ and height $H$, define the unsigned component $$B_p(u,t)=1_{u\ne t}1_{p\nmid u}1_{p\nmid t}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(1_{u\equiv t\pmod p}-\frac1{p-1}\right).
 \label{eq:block}$$ For a predeclared sign law $e=(e_p)_{p\in S_Q}$, the literal operator is $$A_e=\sum_{p\in S_Q}e_pB_p.
 \label{eq:operator}$$ The endpoint masks in [\[eq:block\]](main.tex#L64){reference-type="eqref" reference="eq:block"} are part of the definition.

The position-aware geometry energy is $$G_u=\sum_{p\in S_Q}\sum_{t\in I}B_p(u,t)^2,
 \qquad D_G=\operatorname{diag}(G_u),
 \qquad A_e^\sharp=D_G^{-1/2}A_eD_G^{-1/2}.
 \label{eq:normalization}$$ The square is taken before signs are inserted. Consequently $G_u$ is independent of $e$, and it also does not use $\Lambda$, $b$, $\beta$, or an output vector. On every audited row $G_u>0$, so the congruence is well defined. It is a finite preconditioner, not a claimed uniformly bounded operator family.

# Exact finite identities

For either $T=A_e$ or $T=A_e^\sharp$ and $\beta=L-b$, finite bilinearity gives $$\lVert T\beta\rVert_2^2=\lVert TL\rVert_2^2+\lVert Tb\rVert_2^2-2\langle TL,Tb\rangle.
 \label{eq:polar}$$ Writing $E_L=\lVert TL\rVert_2^2$, $E_b=\lVert Tb\rVert_2^2$ and $$\kappa_T=\frac{2\langle TL,Tb\rangle}{E_L+E_b},
 \qquad R_T=\frac{\lVert T\beta\rVert_2^2}{E_L+E_b},
 \label{eq:kappa}$$ we have the exact finite relation $R_T=1-\kappa_T$. Cauchy–Schwarz gives $$\frac{(\sqrt{E_L}-\sqrt{E_b})^2}{E_L+E_b}
 \leq R_T\leq
 \frac{(\sqrt{E_L}+\sqrt{E_b})^2}{E_L+E_b}.
 \label{eq:cauchy}$$ The diagonal congruence changes the finite geometry on which these identities are evaluated; it does not change their logical status.

# Frozen protocol and audit

The three panels are shown in Table [1](main.tex#L119){reference-type="ref" reference="tab:protocol"}. Counts, shells, exponents, height, source cutoff, source convention, and four sign laws are identical across panels. The fresh panel was fixed before its responses were computed.

<div id="tab:protocol">

| panel                   | origins                                        |
|:------------------------|:-----------------------------------------------|
| low parent (TPC-353)    | $6001,8001,10001$                              |
| higher parent (TPC-354) | $21001,23001,25001$                            |
| fresh holdout           | $29001,33001,37001$                            |
| source counts           | $256,512,1024$                                 |
| shell anchors           | $Q=24,54,80$                                   |
| kernel exponents        | $s=1,2$                                        |
| height / source cutoff  | $H=66$ / $50000$                               |
| sign laws               | all-plus, alternating-index, mod-4, half-split |

: Frozen three-panel protocol.

</div>

The Cartesian product has $3\cdot3\cdot3\cdot2\cdot4=216$ rows per panel, 648 rows in total. The producer uses the finite V59 midpoint convention and accumulates shells in increasing order. A separate checker reconstructs the source and accumulates shells in reverse order; it does not import the producer. Both raw and normalized metrics are compared. An exact rational fourteen-point anchor on $[29001,29014]$ with shell $\{5,7\}$ verifies the unscaled polarization identity, while positivity of the rational geometry diagonal is checked independently. Ten in-memory mutations are required to be rejected by the certificate stress suite.

# Results

Table [2](main.tex#L156){reference-type="ref" reference="tab:floor"} records the all-plus minima and means. The normalization reduces the low-to-higher minimum drop, but does not reduce the corresponding mean drop.

<div id="tab:floor">

|        |         |         |         |         |         |         |
|:-------|--------:|--------:|--------:|--------:|--------:|--------:|
|        |         |         |         |         |         |         |
| panel  |      min|     mean|      max|      min|     mean|      max|
| low    |  .692912|  .895612|  .996268|  .690971|  .899454|  .996303|
| higher |  .650760|  .874362|  .991350|  .664734|  .874614|  .989806|
| fresh  |  .654458|  .880122|  .994391|  .664140|  .886090|  .993322|

: All-plus output coefficient $\kappa_T$ by panel.

</div>

The raw higher-panel minimum drop is $$0.69291151430780062-0.65076036812307647
  =0.042151146184724153.$$ The normalized drop is $$0.69097110464200440-0.66473411648923819
  =0.026236988152766205,$$ so the descriptive drop-reduction fraction is $$1-\frac{0.026236988152766205}{0.042151146184724153}
  =0.37754982894688971.$$ On the fresh panel, the normalized minimum is $0.6641398063$, only $-0.0005943102$ below the higher-panel normalized minimum. This is evidence for a finite partial stabilization of the minimum, not a uniform lower-floor statement.

The mean gives the opposing signal. The raw low-to-higher mean drop is $0.021249745559872912$, whereas the normalized mean drop is $0.024839744603963321$. For the four laws, the fresh panel retains one negative mod-4 row in each metric family: the raw negative row is $(33001,256,Q=24,s=1)$ and the normalized negative row is $(33001,512,Q=24,s=1)$. The higher-panel half-split minimum also decreases under normalization, from $0.0393482615$ to $0.0353891510$.

<div id="tab:census">

| metric                  |  positive|  negative|  unresolved|
|:------------------------|---------:|---------:|-----------:|
| raw $A_e$               |       647|         1|           0|
| normalized $A_e^\sharp$ |       647|         1|           0|

: Alignment census over all 648 rows.

</div>

Thus the normalization improves a selected all-plus minimum statistic while leaving a law-level sign obstruction and a mean-transfer obstruction intact.

# Interpretation and route status

The reusable structure is a source-independent geometry layer that can be inserted between a literal masked operator and the finite polarization interface. It makes the location of the finite obstruction more explicit: normalizing unsigned endpoint/mask energy can alter floor behavior without selecting a canonical sign law.

The strongest licensed claims are:

-   the geometry diagonal and diagonal congruence are exact finite declared constructions;

-   polarization and its Cauchy envelope hold exactly for both finite operators;

-   the raw/normalized three-panel replay is numerically certified on 648 rows, with independent reverse-shell and mutation controls;

-   the all-plus minimum-floor reduction is a finite partial repair, while mean repair and law-uniform alignment are scoped refuted.

No source-uniform arithmetic $L^2$ estimate, growing geometry bound, canonical sign law, fixed-power credit, Route-B reassembly, or twin-prime conclusion follows. The Session-named official Route-A/Route-B evaluator files are absent from this checkout; the local Bridge-B result is therefore fail-closed fallback evidence only.

# Reproducibility

The project directory contains the source, independent checker, stress suite, canonical JSON certificate, proof and theorem ledgers, and this manuscript. The top-level README gives the exact normal and optimized commands. The certificate status is

`NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT`.

The arithmetic advance is ‘NO’, fixed-power credit is zero, and the next natural experiment is an adversarial position/origin holdout.

# References

9 G. H. Hardy and J. E. Littlewood, Some problems of “Partitio Numerorum” III: On the expression of a number as a sum of primes, *Acta Math.* 44 (1923), 1–70. G. Greaves, *Sieves in Number Theory*, Springer, 2001.

<!-- SOURCE_BODY_END -->
