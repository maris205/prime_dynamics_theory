# Masked Signed-Gram Response and Output Interference\ A Fixed-Operator Test of Twin and Background Components

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `024fd8d535671c377bc5714346cb3c1b3136c9d5`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-335 separated the finite source residual into twin, non-twin prime-shift, prime-power, and zero-cross-support coordinates. This paper feeds those four vectors through one fixed all-plus signed-Gram operator, using the same two origins and three scales. The self-response gain ordering is identical on all six rows: $$\text{zero support} > \text{non-twin shift} > \text{twin} >
 \text{prime power}.$$ The corresponding gain ranges are approximately $3.94\times10^5$–$4.20\times10^5$, $1.17\times10^5$–$1.28\times10^5$, $3.74\times10^4$–$4.46\times10^4$, and $0$–$3.47\times10^4$. Moreover, the sum of self energies is 4.85–5.48 times the full response energy in every row, because output cross terms are strongly destructive. Thus source support proportions do not pass unchanged through the operator. This is a finite fixed-operator obstruction, not a uniform bound or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question

The previous two papers produced a source support ledger and an exact norm split. A source-level fraction, however, need not predict a response-level fraction: a matrix can rotate different coordinate pieces into aligned or anti-aligned output directions. The final question of this batch is:

> Does a fixed signed-Gram response preserve the source ordering, or do output interactions create a new obstruction?

We answer this for one predeclared operator and six finite windows. The limited operator choice isolates the interaction mechanism without claiming a shell-uniform theorem.

# Source masks and operator

Let $\beta_o^{(2)}(t)=\Lambda(t+2)-b_o^{(2)}(t)$ on $$I_{o,N}=\{o,\ldots,o+N/2-1\},\qquad
 o\in\{42001,44001\},\quad N\in\{2048,4096,8192\}.$$ Use the four TPC-334 classes $\mathcal C=\{T,B,P,Z\}$, where $T$ is the twin class, $B$ is the non-twin prime-shift class, $P$ is the higher prime-power class, and $Z$ is the zero-cross-support complement. Set $\beta_C=\beta\mathbf 1_C$. Then $$\label{eq:norm}
 \beta=\sum_{C\in\mathcal C}\beta_C,\qquad
 \|\beta\|_2^2=\sum_{C\in\mathcal C}\|\beta_C\|_2^2.$$

The operator is the literal all-plus deleted-diagonal prime-shell matrix $$C=\sum_{54<p\le108}B_{p,54,1},$$ with height $H=66$ and the same residue and divisibility masks as the parent model. For each class let $y_C=C\beta_C$ and define, when the denominator is nonzero, $$G_C=\frac{\|y_C\|_2^2}{\|\beta_C\|_2^2}.$$

# Finite output-Gram identity

Since $C\beta=\sum_Cy_C$, finite bilinearity gives $$\label{eq:response}
 \|C\beta\|_2^2=\sum_C\|y_C\|_2^2+
 2\sum_{C<D}\langle y_C,y_D\rangle.$$ The second term is essential. It can be negative even though every self energy is nonnegative. We record the full upper-triangular output Gram matrix, not only the four diagonal entries.

For each row the certificate also records $$D_C=\sum_t\beta_C(t)^2\sum_u C(u,t)^2,\qquad
 O_C=\|C\beta_C\|_2^2-D_C.$$ These values retain the signed-Gram diagnostic while the output-Gram matrix exposes interactions between support classes.

# Protocol and exact anchor

The producer rebuilds the parent-locked source and all four masks, constructs the fixed operator, and evaluates six rows. An independent implementation reverses shell accumulation and uses an independent trial-factorization source path. The response identity is checked with an explicit floating-point guard; it is not labeled exact in floating point. Five mutations of row geometry, a self metric, the response summary, the firewall, and the anchor are rejected by the stress suite.

For a rational anchor take $$A=\begin{pmatrix}2&1\\1&-1\end{pmatrix},\quad
 x_T=(1,0),\quad x_B=(0,2),\quad x=x_T+x_B=(1,2).$$ Then $\|Ax_T\|^2=5$, $\|Ax_B\|^2=8$, $\langle Ax_T,Ax_B\rangle=2$, and $$\|Ax\|^2=17=5+8+2(2).$$ This anchor certifies the finite output-Gram algebra only.

# Results

Table [1](main.tex#L122){reference-type="ref" reference="tab:gains"} gives the gain ranges over the six rows.

<div id="tab:gains">

| mask                 |      minimum|      maximum|
|:---------------------|------------:|------------:|
| twin prime           |   37443.5863|   44607.7734|
| non-twin prime shift |  117431.3630|  127558.5613|
| prime-power shift    |            0|   34676.0605|
| zero cross support   |  393547.7680|  419768.8445|

: Self-response gains for the four support masks.

</div>

The gain ordering $Z>B>T>P$ holds in all six rows. The self-response sum divided by the full response energy ranges from $$4.8538535937774503\quad\text{to}\quad5.4814134328177246.$$ Thus the pairwise interaction term in [\[eq:response\]](main.tex#L80){reference-type="eqref" reference="eq:response"} is negative in all six rows. In particular, the background–zero pair has output inner product between $-5.9051\times10^8$ and $-2.3895\times10^9$, while the twin–zero pair is also negative throughout the panel. The twin–background pair is positive, but it does not overcome the larger destructive interactions.

The result refines the source-level picture. Twin coordinates have a stable nonzero source component, yet their self response is below the non-twin and zero-support gains. More importantly, adding self responses would badly overestimate the full response. A future uniform argument must control the cross-class output Gram matrix, not merely each masked norm.

# Claim firewall and batch endpoint

The finite expansion [\[eq:response\]](main.tex#L80){reference-type="eqref" reference="eq:response"} is `PROVED_EXACT_FINITE` for the declared model. The six-row fixed operator replay, gain ordering, destructive interaction census, independent checker, and stress suite are `NUMERICALLY_CERTIFIED_FINITE`. The gain ranges are `NUMERICAL_OBSERVATION`; the statement that source ordering transfers to all operators is `REFUTED_SCOPED`. A uniform masked operator estimate, arithmetic power saving, strict $1/400$ payment, official route pass, and twin-prime conclusion remain `OPEN` or `NONE`. In particular, $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN}.$$

The Session-named evaluator files are absent from this checkout. The local Bridge-B result is consequently a fail-closed repository check only. The five-paper batch ends at a concrete obstruction: source support must be combined with a position-aware, cross-class operator estimate.

<!-- SOURCE_BODY_END -->
