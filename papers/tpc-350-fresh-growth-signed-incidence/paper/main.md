# Fresh-Growth Replication and Shell-Scale Stress for Prime-Balanced Incidence Witnesses

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We test the finite prime-balanced incidence witness introduced in TPC-349 on fresh locations and a wider shell-scale ladder. The literal object is kept unchanged: a masked prime-shell matrix is compared with its unmasked ideal, and a zero-sum signed sum of all divisibility incidences is used as a test vector. The incidence Gram identity and the induced-norm lower bound remain exact. A predeclared panel with three fresh origins, four interval lengths, four shell scales, two source laws, and two kernel exponents contains 192 rows. Every signed vector has positive response. The response-to-defect ratio ranges from $0.0657381187306$ to $0.8797933448$, with mean $0.492863038063$; the high-shell scale $Q=256$ has no row reaching one half of the defect norm. Only 24 of 48 length series are nondecreasing, and the signed witness beats the coordinate baseline on 70 rows. Thus fresh replication is positive finite evidence, while a universal quarter-floor and monotonic growth law are refuted on the declared panel. No arithmetic $L^2$ estimate, fixed-power saving, or twin-prime conclusion follows.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

TPC-349 converted a coordinate mask-defect witness into a deterministic zero-sum contrast of prime divisibility incidences. Its finite panel showed substantial response but did not establish a growing statement. The minimal next question is whether the same vector rule survives when both the interval length and the location are changed, and whether a larger shell scale changes the finite floor.

We answer this question only on a locked finite panel. The term “growth” below means the four lengths $M=256,512,1024,2048$; it does not mean a limit as $M\to\infty$. Likewise, the shell ladder $Q=36,80,128,256$ is a finite stress test. None of the numerical ratios is promoted to an asymptotic claim, a source-uniform arithmetic estimate, or a theorem about twin primes.

# The literal masked matrix

Let $I=\{o,o+1,\ldots,o+M-1\}$ and let $R_I,E_I$ denote restriction and zero extension. For a shell prime $p$, put $(P_pf)(n)=\mathbf 1_{p\nmid n}f(n)$. With the same height-normalized kernel as the parent releases, the physical and ideal finite matrices are $$\begin{aligned}
 A_I&=\sum_p\varepsilon_p R_IP_pK_pP_pE_I,\\
 T_I&=R_I\left(\sum_p\varepsilon_pK_p\right)E_I,
 \qquad D_I=A_I-T_I.\end{aligned}$$ Here the source signs $\varepsilon_p$ are fixed by the declared source law. They are distinct from the test coefficients introduced next. The finite entry used in the computation is $$\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}\,p h_s(u-t)
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right),
 \qquad
 h_s(d)=\frac{H^{2s}}{(H^2+d^2)^s},\quad H=66.$$

# Exact incidence interface

Order the primes in $(Q,2Q]$ as $p_0<\cdots<p_{r-1}$, put $m=\lfloor r/2\rfloor$, and define $$\beta_j=\begin{cases}
  +1,&j<m,\\
  0,&m\le j<r-m,\\
  -1,&j\ge r-m.
 \end{cases}$$ For $t\in I$, let $h_{p_j,I}(t)=\mathbf 1_{p_j\mid t}$ and set $$b_I=\sum_{j=0}^{r-1}\beta_jh_{p_j,I}.$$ The definition intentionally adds every incidence at a multiply divisible position; it is not an owner-class partition. If $b_I\ne0$, write $x_I=b_I/\|b_I\|_2$.

> **Proposition: balance** The coefficient sum is zero, with equally many positive and negative entries and at most one neutral entry.

> **Proof** The positive and negative index blocks each have $m$ elements and the middle block has size $r-2m\in\{0,1\}$.

> **Proposition: prime-incidence Gram identity** For every finite matrix $D_I$, $$\|D_Ib_I\|_2^2=\sum_{j,k}\beta_j\beta_k
>  \langle D_Ih_{p_j,I},D_Ih_{p_k,I}\rangle.
>  \label{eq:gram}$$

> **Proof** Substitute the finite sum defining $b_I$, apply linearity, and expand the Euclidean inner product.

> **Theorem: normalized lower witness** If $b_I\ne0$, then $$\|D_I\|_{2\to2}\geq
>  \frac{\|D_Ib_I\|_2}{\|b_I\|_2}.
>  \label{eq:lower}$$

> **Proof** $x_I$ is a unit vector. Inserting it into the definition of the induced Euclidean norm gives $\|D_I\|_{2\to2}\geq\|D_Ix_I\|_2$, which is ([\[eq:lower\]](main.tex#L128){reference-type="ref" reference="eq:lower"}); see also `\cite{conway2000}`.

> **Remark** Equation ([\[eq:gram\]](main.tex#L115){reference-type="ref" reference="eq:gram"}) is exact but makes no sign assertion about its cross-prime terms. The theorem is a finite linear-algebra statement and does not supply cancellation in the source variable.

# Frozen fresh-growth protocol

The parent TPC-349 producer and certificate are hash locked. We use the three previously unused origins $$o\in\{60097,72097,84097\},
 \quad M\in\{256,512,1024,2048\},
 \quad Q\in\{36,80,128,256\},$$ the two exponents $s\in\{1,2\}$, and source laws `all_plus` and `alternating_index`. Thus there are $3\cdot4\cdot4\cdot2\cdot2=192$ rows and 48 fixed-$(o,Q,s,\text{law})$ length series. The baseline is the largest defect column norm among all positions hit by at least one shell prime.

The producer accumulates shells forward. An independent checker reverses the shell order and recomputes the matrices, the incidence vector, every norm ratio, each growth series, and a rational anchor at $I=[97,110]$, $Q=4$. The anchor is outside the large audit panel and tests the exact multi-hit incidence arithmetic without floating point.

# Finite results

<div id="tab:summary">

| Quantity                      | Certified finite readout              |
|:------------------------------|:--------------------------------------|
| Fresh origins                 | $60097,72097,84097$                   |
| Lengths / shell scales        | $256,512,1024,2048$ / $36,80,128,256$ |
| Rows / length series          | $192$ / $48$                          |
| Positive signed responses     | $192/192$                             |
| Signed support per row        | $24$–$294$                            |
| Incidence Gram records        | $192$                                 |
| Maximum Gram discrepancy      | $1.06581410364\times10^{-14}$         |
| $\|D_Ix_I\|/\|D_I\|$          | $0.0657381187306$–$0.8797933448$      |
| Mean response-to-defect ratio | $0.492863038063$                      |
| $\|D_Ix_I\|/C_I$              | $0.329452329144$–$1.93522876157$      |
| Coordinate baseline beaten    | $70/192$                              |
| At least half the defect norm | $91/192$                              |
| Nondecreasing length series   | $24/48$                               |

: TPC-350 finite fresh-growth and shell-scale audit.

</div>

All 192 fresh rows have positive response, so the exact lower-witness interface is not an artifact of the two parent origins. The finite floor is nevertheless strongly scale dependent. Grouping by shell scale gives:

| $Q$ |  rows|    minimum ratio|   maximum ratio|  rows at least one half|
|:---:|-----:|----------------:|---------------:|-----------------------:|
|  36 |    48|   0.645570841526|    0.8797933448|                      48|
|  80 |    48|   0.283951823484|  0.780369733529|                      25|
| 128 |    48|   0.127216174002|  0.733093535707|                      18|
| 256 |    48|  0.0657381187306|  0.456967381039|                       0|

The $Q=256$ block therefore supplies a scoped obstruction to a universal quarter-floor: its minimum is below $1/4$, and no row reaches one half. This does not say that every larger shell fails, nor does it prove decay. Along the length ladder, only 24 of 48 series are nondecreasing. The series statistic is descriptive and is not a monotonicity theorem.

## Exact fresh anchor

For $I=[97,110]$, $Q=4$, $s=1$, and all-plus source signs, the shell is $(5,7)$ and $\beta=(1,-1)$. The exact incidence vector is $$b_I=(0,-1,0,1,0,0,0,0,0,0,0,0,0,1),
 \qquad \|b_I\|_2^2=3.$$ The exact squared response is $$\|D_Ib_I\|_2^2=
 \frac{14276593956453081571772409162371674557671952566687819648533844297}
 {125805121225372449086489766667977465413147946965619898288500000}.$$ The certificate stores the exact image-vector digest as well. This anchor contains a multiply divisible position and hence checks the incidence sum, not an exclusive owner assignment.

# Adversarial validation and claim boundary

The normal and optimized producer outputs are required to be byte identical. The independent reverse-shell checker recomputes all 192 rows and all 48 series. Its stress suite rejects changed origins, a shortened shell ladder, altered census, false quarter-floor status, inflated monotonicity, a mutated anchor, and a replaced parent certificate. A local Bridge-B wrapper locks the producer, replay, stress script, certificate, PDF, log, and bridge text.

These checks establish finite package integrity. They do not establish a source-uniform arithmetic $L^2$ estimate, a uniformly bounded physical masked operator, a fixed power of $x$, or any twin-prime conclusion. The official Session-named Route-A/Route-B evaluator files are absent from this checkout, so the local route assessment is fail closed.

# Conclusion and next question

TPC-350 gives a clear two-sided map location. The TPC-349 incidence witness survives all three fresh origins and all four finite lengths with positive response, but the response floor drops from the low-shell block to the $Q=256$ block and length monotonicity is not universal. Thus the reusable structure is a fresh finite lower-witness interface, while the obstruction is scale sensitivity of a fixed balanced contrast.

The next minimal question is whether a predeclared scale-adaptive zero-sum contrast can repair this high-shell loss without fitting coefficients to each row. If not, the incidence branch should be frozen and the main route should return to the source-native arithmetic $L^2$ gate.

# References

1 John B. Conway. *A Course in Functional Analysis*. Springer, 2nd edition, 2000.

<!-- SOURCE_BODY_END -->
