# A Mask-Aware Frobenius Envelope\ A Sign-Free Response Bound for the Finite Twin-Prime Model

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-338 showed that signed output covariance changes when the control orbit is enlarged. We therefore test a sign-free alternative: for a vector supported on $S$, bound its response by the Frobenius norm of the corresponding column submatrix. The bound is an exact finite inequality and passes all 216 declared mask/control records on six windows. Its occupancy is below $0.2$ for every broad mask record (twin, non-twin, and zero-support), while prime-power singleton records can attain equality. The result supplies a valid envelope and a quantitative tightness obstruction, but no growing arithmetic estimate.

<!-- SOURCE_BODY_BEGIN -->

# Motivation and finite object

Let $A$ be the all-plus deleted-diagonal shell operator from the parent-locked TPC-338 model, with $Q=54$, exponent $1$, and $H=66$. On $$I_{o,N}=\{o,\ldots,o+N/2-1\},\qquad
 (o,N)\in\{42001,44001\}\times\{2048,4096,8192\},$$ write the source as four disjoint masked vectors $\beta_C$, indexed by twin, non-twin prime shift, prime-power shift, and zero-support. The nine controls are the TPC-338 affine/reversal orbit. For every control placement, the response is $A P_j\beta_C$.

The previous paper found a sign reversal in one covariance entry when five controls were replaced by nine. A bound based on that sign is consequently not a safe interface. This paper asks how far an elementary sign-free bound can go.

# Support-restricted bound

If $x$ is supported on $S$, let $A_S$ denote the columns of $A$ indexed by $S$. Then $$\label{eq:bound}
 \|Ax\|_2^2=\|A_Sx_S\|_2^2
 \leq \|A_S\|_2^2\|x_S\|_2^2
 \leq \|A_S\|_F^2\|x_S\|_2^2.$$ Define the support Frobenius gain $$F(S)^2=\|A_S\|_F^2=\sum_{t\in S}\sum_u|A(u,t)|^2.$$ For a nonzero $x$, the occupancy is $$\eta(A,x)=\frac{\|Ax\|_2^2/\|x\|_2^2}{F(\operatorname{supp}x)^2}\leq1.$$ This is deliberately independent of covariance signs and of the signs of the source entries. A small $\eta$ measures slack in the bound, not a payment of arithmetic cancellation.

# Audit protocol

The producer rebuilds six matrices, four masks, and nine controls, producing 216 records (198 nonempty). Each record stores the source norm, response energy and gain, support Frobenius gain, gap, and occupancy. The independent checker uses the TPC-338 reverse-shell engine under a hash lock and recomputes every record. Mutation stress changes both structural and semantic fields.

For an exact anchor take $$A=\begin{pmatrix}1&0\\2&1\end{pmatrix},\qquad x=(3,0).$$ Then $\|Ax\|^2=45$, $\|x\|^2=9$, and $F(\{0\})^2=5$, so equality holds in [\[eq:bound\]](main.tex#L52){reference-type="eqref" reference="eq:bound"}. The anchor proves the inequality’s algebraic interface only.

# Finite results

<div id="tab:occupancy">

| mask                 | nonempty records |          occupancy range          |
|:---------------------|:----------------:|:---------------------------------:|
| twin prime           |        54        |         0.028830–0.186855         |
| non-twin prime shift |        54        |         0.010649–0.055850         |
| prime-power shift    |        36        | 0.99999999999999–1.00000000000000 |
| zero support         |        54        |         0.007477–0.032068         |

: Occupancy of the support-restricted Frobenius envelope.

</div>

All 216 bounds pass. The global nonempty occupancy range is 0.0074766258–1.0000000000. The broad-mask maximum is 0.1868550366, below the declared factor-five tightness threshold. The prime-power records are singleton-like on this panel and therefore do not contradict the broad-mask slack.

The result is useful precisely because it separates validity from sharpness. The inequality controls every response without choosing a covariance sign, but its support-only nature discards the alignment of source amplitudes with the columns of $A$. A future estimate needs either a sharper masked Gram quantity or an independently justified structural projection.

# Claim firewall and next step

The support-restricted inequality is `PROVED_EXACT_FINITE_DECLARED_MODEL`; the 216-record replay and zero-violation census are `NUMERICALLY_CERTIFIED_FINITE`. The occupancy ranges are `NUMERICAL_OBSERVATION`. Uniform tightness of this elementary envelope is `REFUTED_SCOPED` at the finite factor-five diagnostic. There is no arithmetic advance or fixed-power credit: $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$ The official Session evaluator files are absent, so local Bridge-B is fail-closed and is not an official route pass.

The next project tests a hybrid of this support bound and a global Schur bound, with the explicit goal of reducing the zero-support slack without using signs.

<!-- SOURCE_BODY_END -->
