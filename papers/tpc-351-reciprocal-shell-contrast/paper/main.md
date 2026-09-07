# A Reciprocal-Shell Zero-Sum Contrast: Finite Scale Repair for Prime-Incidence Defect Witnesses

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 3, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-350 found that a fixed balanced-step contrast of prime-divisibility incidences has a positive finite response but a low floor on large prime shells. We test one predeclared replacement on the identical literal masked operator and the identical 192-row panel. For shell primes $p_0<\cdots<p_{r-1}$, set $\gamma_j=p_j^{-1}-r^{-1}\sum_kp_k^{-1}$. This rational rule is independent of the interval, source law, and observed matrix, and has exact zero sum. Its prime-incidence Gram identity and induced-norm lower witness are exact. All 192 reciprocal witnesses have positive response; 180 improve the locked parent response, 111 reach half the defect norm, and 86 beat the coordinate baseline. The response-to-defect ratio ranges from $0.0917557319271$ to $0.901734353382$, with mean $0.539037202287$. At $Q=256$, four rows now reach one half, compared with none for the parent, but the minimum remains below one quarter. Thus the reciprocal rule gives a genuine finite scale repair, not a uniform floor, arithmetic $L^2$ estimate, or twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

The balanced-step witness in TPC-350 survived three fresh origins and four finite interval lengths, yet its $Q=256$ block had no row reaching one half of the defect norm and a minimum ratio $0.0657381187306$. The smallest natural continuation is to change only the shell coefficient rule while retaining the literal masked object and every panel key.

We impose a strict no-fit condition: coefficients may depend on the shell primes, but not on the origin, interval length, source signs, kernel exponent, matrix entries, singular vectors, or response. All comparisons below are finite. They do not imply a limit as $M$ or $Q$ grows, a source-uniform arithmetic estimate, a fixed power of $x$, or a statement about twin primes.

# Literal masked defect

Let $I=\{o,o+1,\ldots,o+M-1\}$ and let $R_I,E_I$ denote restriction and zero extension. For a shell prime $p$, put $(P_pf)(n)=\mathbf 1_{p\nmid n}f(n)$. The physical matrix, its unmasked ideal, and their defect are $$\begin{aligned}
 A_I&=\sum_p\varepsilon_pR_IP_pK_pP_pE_I,\\
 T_I&=R_I\left(\sum_p\varepsilon_pK_p\right)E_I,
 \qquad D_I=A_I-T_I.\end{aligned}$$ The source signs $\varepsilon_p$ are fixed independently of the test coefficients. The finite matrix entry is $$\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}\,p h_s(u-t)
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right),
 \qquad h_s(d)=\frac{H^{2s}}{(H^2+d^2)^s},\quad H=66.$$

# Reciprocal-shell incidence interface

For the primes in $(Q,2Q]$, define $$\gamma_j=\frac1{p_j}-\frac1r\sum_{k=0}^{r-1}\frac1{p_k}.
 \label{eq:gamma}$$ For $t\in I$, let $h_{p_j,I}(t)=\mathbf 1_{p_j\mid t}$ and set $$c_I=\sum_{j=0}^{r-1}\gamma_jh_{p_j,I}.$$ Multiply-divisible positions retain the algebraic sum of all incidences.

> **Proposition: exact balance** The rational coefficient vector in [\[eq:gamma\]](main.tex#L84){reference-type="eqref" reference="eq:gamma"} satisfies $\sum_j\gamma_j=0$.

> **Proof** The first terms sum to $\sum_jp_j^{-1}$, while the repeated mean contributes $r\cdot r^{-1}\sum_kp_k^{-1}$.

> **Proposition: reciprocal incidence Gram identity** For every finite matrix $D_I$, $$\|D_Ic_I\|_2^2=\sum_{j,k}\gamma_j\gamma_k
>  \langle D_Ih_{p_j,I},D_Ih_{p_k,I}\rangle.
>  \label{eq:gram}$$

> **Proof** Apply linearity to the finite sum defining $c_I$ and expand the Euclidean inner product.

> **Theorem: normalized lower witness** If $c_I\ne0$, then $$\|D_I\|_{2\to2}\geq\frac{\|D_Ic_I\|_2}{\|c_I\|_2}.
>  \label{eq:lower}$$

> **Proof** The vector $c_I/\|c_I\|_2$ is a unit vector. Insert it into the definition of the induced Euclidean norm; see also `\cite{conway2000}`.

> **Remark** Equations [\[eq:gamma\]](main.tex#L84){reference-type="eqref" reference="eq:gamma"}–[\[eq:lower\]](main.tex#L118){reference-type="eqref" reference="eq:lower"} are exact finite algebra. They do not assert a sign for the cross-prime Gram terms or cancellation in the source variable.

# Frozen paired protocol

The TPC-350 producer and certificate are normalized-hash locked. We retain $$o\in\{60097,72097,84097\},\quad
 M\in\{256,512,1024,2048\},\quad
 Q\in\{36,80,128,256\},$$ the exponents $s\in\{1,2\}$ and source laws `all_plus` and `alternating_index`. Hence there are 192 paired rows and 48 fixed $(o,Q,s,\text{law})$ length series. Each reciprocal response is compared with the parent balanced-step response on exactly the same row key. The coordinate control is the largest defect column norm among mask-hit positions.

The producer accumulates shells forward. An independent checker accumulates them in reverse, recomputes all matrices, exact coefficients, norm ratios, parent comparisons, length series, and a rational anchor. No producer module is imported by the independent checker.

# Finite results

<div id="tab:summary">

| Quantity                                | Certified finite readout           |
|:----------------------------------------|:-----------------------------------|
| Rows / length series                    | $192$ / $48$                       |
| Positive reciprocal responses           | $192/192$                          |
| Rows improving TPC-350                  | $180/192$                          |
| Reciprocal incidence support            | $24$–$339$                         |
| $\|D_Ix_I\|/\|D_I\|$                    | $0.0917557319271$–$0.901734353382$ |
| Mean response-to-defect ratio           | $0.539037202287$                   |
| Coordinate baseline beaten              | $86/192$                           |
| At least half the defect norm           | $111/192$                          |
| Nondecreasing length series             | $25/48$                            |
| Arithmetic advance / fixed-power credit | no / zero                          |

: TPC-351 paired finite audit.

</div>

All reciprocal witnesses are nonzero with positive response. The parent comparison is broad but not universal: 180 rows improve and 12 do not. The half-defect census rises from 91 to 111, while the coordinate-baseline census rises from 70 to 86. Grouping by shell scale gives the sharper readout:

| $Q$ |   reciprocal min|  reciprocal mean|  reciprocal max|  half|  improved|
|:---:|----------------:|----------------:|---------------:|-----:|---------:|
|  36 |   0.688158407450|   0.804654885138|  0.901734353382|    48|        48|
|  80 |   0.364933284503|   0.632666956348|  0.834679518677|    41|        48|
| 128 |   0.178852728310|   0.448071439797|  0.783459763859|    18|        44|
| 256 |  0.0917557319271|   0.270755527864|  0.537734585425|     4|        40|

The $Q=256$ block is a real finite repair: its minimum increases from $0.0657381187306$ to $0.0917557319271$, and four rows reach one half instead of zero. It is not a universal repair, because eight high-shell rows lose to the parent and the block still contains sub-quarter values. Only 25 of 48 length series are nondecreasing, one more than the parent but far from a monotonicity theorem.

## Exact reciprocal anchor

For $I=[97,110]$, $Q=4$, $s=1$, and all-plus source signs, the shell is $(5,7)$ and $\gamma=(1/35,-1/35)$. The exact incidence vector is $$c_I=\frac1{35}(0,-1,0,1,0,0,0,0,0,0,0,0,0,1),
 \qquad \|c_I\|_2^2=\frac3{1225}.$$ Its exact squared response is $$\|D_Ic_I\|_2^2=
 \frac{14276593956453081571772409162371674557671952566687819648533844297}
 {154111273501081250130949964168272395131106235032884375403412500000}.$$ This anchor checks rational centering, multiply-divisible incidences, and the literal defect without floating point.

# Adversarial validation and claim boundary

Normal and optimized producer, independent, stress, and Bridge-B outputs must match byte for byte. Mutation tests reject a changed panel, deleted high shell, false positive census, false quarter-floor claim, inflated monotonicity, altered anchor, replaced parent, and inflated parent-improvement census. The local bridge locks source files, certificate, manuscript, compile log, and bridge text.

These checks establish finite package integrity only. No source-uniform arithmetic $L^2$ estimate, uniform masked-operator theorem, fixed-power saving, Route-B reassembly, or twin-prime conclusion is obtained. The Session-named official evaluator files are absent, so the local route evaluation remains fail closed.

# Conclusion and next question

Reciprocal centering is a simple, non-fitted scale-aware rule that improves most rows and partially repairs the $Q=256$ block. The strongest obstruction is equally clear: 12 losses, a sub-quarter floor, and 23 nonmonotone series remain. The next minimal step is an adversarial holdout on disjoint origins and shell scales. If the repair does not transfer, the finite incidence branch should be frozen and the main route returned to the source-native arithmetic $L^2$ gate.

# References

1 John B. Conway. *A Course in Functional Analysis*. Springer, 2nd edition, 2000.

<!-- SOURCE_BODY_END -->
