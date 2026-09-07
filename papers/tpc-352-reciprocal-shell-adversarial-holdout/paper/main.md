# Adversarial Holdout for Reciprocal-Shell Contrasts:\ Partial Transfer and a High-Shell Obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 3, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-351 proposed the non-fitted reciprocal-shell contrast $\gamma_j=p_j^{-1}-r^{-1}\sum_k p_k^{-1}$ for the literal divisibility-mask defect in a prime-shell operator. We evaluate that same rule, without any refitting, on three disjoint origins and a new shell ladder. The exact zero-sum incidence identity and its induced-norm lower witness remain valid. On the frozen 144-row panel every reciprocal witness has positive response, but only $118/144$ rows improve the balanced-step parent. The reciprocal response/defect ratio is $0.0801262572786$–$0.829632172143$, compared with $0.099642909832$–$0.806767399067$ for the parent; the reciprocal witness beats the coordinate baseline on $47/144$ rows and reaches half the defect norm on $49/144$. At $Q=256$ its floor is lower than the parent. Thus the finite scale repair partially transfers but no uniform repair theorem is supported. No arithmetic $L^2$ estimate, fixed-power credit, or twin-prime result is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Question and literal defect

Let $I=\{o,o+1,\ldots,o+M-1\}$ and let $R_I,E_I$ denote restriction and zero extension. For a shell prime $p$, write $(P_pf)(n)=p\,\mathbf{1}_{p\mid n}f(n)$ and let $K_s$ have entries $$K_s(u,t)=\mathbf{1}_{u\ne t}\frac{H^{2s}}{(H^2+(u-t)^2)^s},\qquad H=66.$$ For fixed source signs $\varepsilon_p$, the physical and unmasked blocks are $$A_I=\sum_p\varepsilon_pR_IP_pK_sP_pE_I,
 \qquad T_I=R_I\Big(\sum_p\varepsilon_pK_s\Big)E_I,
 \qquad D_I=A_I-T_I.$$ The two projection factors in $A_I$ are retained literally. In particular, $D_I$ is not replaced by a convolution and no mask term is discarded.

TPC-350 found that a fixed balanced shell contrast had positive finite responses but a poor high-shell floor. The present question is narrower: does one fixed, scale-aware rule transfer to a panel chosen independently of those responses?

# Exact reciprocal-shell witness

For the ordered shell $p_0<\cdots<p_{r-1}$ define $$\gamma_j=\frac1{p_j}-\frac1r\sum_{k=0}^{r-1}\frac1{p_k},
 \qquad c_I(t)=\sum_{j=0}^{r-1}\gamma_j\mathbf{1}_{p_j\mid t}.
 \label{eq:gamma}$$ The coefficients are rational and satisfy $$\sum_j\gamma_j=\sum_jp_j^{-1}-r\,r^{-1}\sum_kp_k^{-1}=0
 \label{eq:balance}$$ exactly. The rule is fixed by the shell alone; it does not depend on $o$, $M$, $s$, the source law, an entry of $D_I$, or an observed response.

Let $h_{p_j,I}$ be the interval vector $\mathbf{1}_{p_j\mid t}$. Multiply-divisible positions are intentionally retained, so linearity gives $$c_I=\sum_j\gamma_jh_{p_j,I},\qquad
 \left\lVert D_Ic_I\right\rVert_2^2
 =\sum_{j,k}\gamma_j\gamma_k
 \langle D_Ih_{p_j,I},D_Ih_{p_k,I}\rangle.
 \label{eq:gram}$$ Consequently, whenever $c_I\ne0$, $$\left\lVert D_I\right\rVert_{2\to2}\geq
 \frac{\left\lVert D_Ic_I\right\rVert_2}{\left\lVert c_I\right\rVert_2}.
 \label{eq:witness}$$ Equations [\[eq:balance\]](main.tex#L73){reference-type="eqref" reference="eq:balance"}–[\[eq:witness\]](main.tex#L91){reference-type="eqref" reference="eq:witness"} are exact finite linear algebra. They do not assert cross-prime cancellation in the source variable.

# Adversarial holdout protocol

The holdout was fixed before its responses were read: $$\begin{gathered}
 o\in\{96097,120097,144097\},\quad
 M\in\{256,512,1024\},\quad
 Q\in\{64,128,256,512\},\\
 s\in\{1,2\},\quad
 \varepsilon\in\{\text{all-plus},\text{alternating-index}\}.
\end{gathered}$$ There are $3\cdot3\cdot4\cdot2\cdot2=144$ rows and $48$ fixed origin–scale–law length series. On each row we compute the reciprocal witness and, on the identical matrix, the TPC-350 balanced parent (the first $\lfloor r/2\rfloor$ shell coefficients are $+1$, the last are $-1$, and a middle coefficient is zero when $r$ is odd). We also record the largest defect norm among mask-hit coordinate columns. No coefficient is selected after seeing any of these quantities.

The producer accumulates shells in ascending order. An independent checker accumulates them in reverse order, reconstructs all matrices, recomputes the spectral norms, and checks the exact rational anchor at $I=[193,206]$, $Q=4$, $s=1$. A hostile checker applies eight protocol, certificate, anchor, census, claim, and parent-lock mutations.

# Finite results

Table [1](main.tex#L130){reference-type="ref" reference="tab:overall"} gives the aggregate readout. The maximum reciprocal Gram replay discrepancy is $1.15463194561\times10^{-14}$.

<div id="tab:overall">

| Quantity                         |       Reciprocal|  Balanced parent|
|:---------------------------------|----------------:|----------------:|
| Rows with positive response      |        $144/144$|        $144/144$|
| Response/defect ratio, minimum   |  0.0801262572786|   0.099642909832|
| Response/defect ratio, mean      |   0.397491684421|   0.361474079935|
| Response/defect ratio, maximum   |   0.829632172143|   0.806767399067|
| Rows reaching half defect        |         $49/144$|         $46/144$|
| Rows beating coordinate baseline |         $47/144$|         $30/144$|
| Nondecreasing length series      |          $22/48$|          $22/48$|

: TPC-352 paired finite holdout audit.

</div>

The reciprocal response is larger than the balanced response on $118/144$ rows. The gain range is $0.592696740468$–$1.47665316933$ with mean $1.09769598704$, so the comparison is plainly not uniform. The scale breakdown is:

<div id="tab:scale">

|     |         |         |         |         |         |         |     |     |
|:---:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:---:|:---:|
|     |         |         |         |         |         |         |     |     |
| $Q$ |   min   |   mean  |   max   |   min   |   mean  |   max   |  R  |  B  |
|  64 | .575197 | .695679 | .829632 | .472606 | .632789 | .806767 |  36 |  33 |
| 128 | .162468 | .419321 | .782947 | .110025 | .372357 | .698661 |  12 |  12 |
| 256 | .080126 | .225511 | .432048 | .099643 | .215682 | .366937 |  0  |  0  |
| 512 | .136136 | .249456 | .544274 | .134698 | .225069 | .508967 |  1  |  1  |

: Scale-resolved response/defect ratios and half-defect counts.

</div>

The $Q=256$ row is the decisive adversarial obstruction: reciprocal centering raises the mean slightly but lowers the minimum from the parent. At $Q=512$ the improvement is again only partial. The data therefore support a scale-specific finite observation, not a scale-uniform repair.

## Exact rational anchor

For $I=[193,206]$ and the shell $(5,7)$, equation [\[eq:gamma\]](main.tex#L68){reference-type="eqref" reference="eq:gamma"} gives $(\gamma_0,\gamma_1)=(1/35,-1/35)$. The exact incidence vector is $$c_I=\frac1{35}(0,0,1,-1,0,0,0,1,0,0,-1,0,1,0),
 \qquad \left\lVert c_I\right\rVert_2^2=\frac1{245}.$$ With the literal rational defect at exponent one, the squared response is $$\left\lVert D_Ic_I\right\rVert_2^2=
\frac{2094105299985077452542621112101565891110487723654736503672553}
{3198793259690951133635907806062856099910022277169847540500000}.$$ This anchor checks centering, multiply-divisible incidences, and the two-sided mask defect without relying on floating-point equality.

# Validation and claim boundary

The producer and reverse-shell checker both pass in normal and optimized Python modes with byte-identical stdout and empty stderr. The stress suite rejects eight mutations. The local Bridge-B checker additionally locks the producer, checker, stress script, certificate, PDF, compile log, and bridge text before rerunning the finite checks.

The Session-named Route-A and Route-B evaluator files are absent from this checkout. Accordingly, the local result is fail-closed and is not an official evaluator pass. The exact statements proved here are finite coefficient balance, incidence linearity, Gram expansion, and the induced-norm test-vector inequality. The holdout census is numerical evidence only. In particular, this paper does not prove a source-uniform arithmetic $L^2$ estimate, a uniform masked-operator bound, a growing lower bound, a fixed-power saving, Route-B reassembly, or a twin-prime theorem.

# Conclusion

The reciprocal-shell rule transfers as a useful but non-uniform finite witness: it improves most rows and both global half-defect and coordinate-baseline counts, yet its high-shell floor can be worse than the balanced parent. This is a genuine adversarial obstruction to promoting the TPC-351 repair into a uniform shell-scale principle. We therefore freeze this finite incidence branch and return the main route to the literal source-native masked arithmetic $L^2$ gate.

# References

1 J. B. Conway, *A Course in Functional Analysis*, 2nd ed., Springer, 2000.

<!-- SOURCE_BODY_END -->
