# Control-Average and Centered Position Response in the Twin-Prime Signed-Gram Diagnostic

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding finite response-spectrum audit showed that three odd-affine coordinate bijections reverse the all-plus signed-Gram readout, while identity and reversal do not, despite preserving the source multiset and Euclidean norm. We now ask whether this response can be localized into a coherent control-average component and a centered position component. For five frozen permutations $P_j$, we prove the exact finite identity $$\frac1m\sum_j q(P_jv)=q(\bar v)+\frac1m\sum_j q(P_jv-\bar v)$$ for every quadratic form $q$, and apply it simultaneously to the energy, coordinate diagonal, and off-diagonal Gram forms. On the hash-locked two-origin, two-scale panel, this yields 128 guarded law-level decompositions. For the all-plus law, the control-average and centered off-diagonal terms are positive on all 32 rows, while the coherent mean term is positive on 31 rows and negative on one. The exact rational anchor verifies the three identities symbolically. This is a finite structural localization of the response; it does not supply a growing arithmetic $L^2$ estimate, a fixed-power credit, an official route pass, or a twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and contribution

The signed-Gram diagnostic in this session acts on a finite source vector with a literal centered prime-shell matrix. A coordinate permutation can preserve all source-only statistics while changing the physical quadratic response. TPC-330 measured that effect over five predeclared bijections. The next minimal question is not whether to add another permutation, but how to split the observed response:

> Does the positive affine response live in a coherent average source, in the centered position fluctuations, or in both?

The contribution of this paper is an exact control-orbit decomposition and a finite certificate for its three signed-Gram components. It provides a new analytic structure and a new numerical obstruction/localization, while keeping the arithmetic panel and system family unchanged.

# Finite object and source model

For an origin $o$ and even scale $N$, let $$I_{o,N}=\{o,o+1,\ldots,o+N/2-1\}.$$ We use $$o\in\{28001,36001\},\quad N\in\{4096,8192\},\quad
 Q\in\{24,36,54,80\},\quad s\in\{1,2\},\quad H=66.$$ For $p\in(Q,2Q]$, define the literal deleted-diagonal block $$\label{eq:block}
 B_{p,Q,s}(u,t)=
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right).$$ For one of four fixed shell sign laws $e$, set $$C_e=\sum_{p\in(Q,2Q]}e_pB_{p,Q,s}.$$ The laws are all-plus, alternating index, the sign of $p$ modulo $4$, and a half split in increasing prime order.

The finite declared source is inherited from the V59 model: $$\label{eq:source}
 \beta_o^{(2)}(t)=\Lambda(t+2)-b^{(2)}(t),\qquad
 b^{(2)}(t)=2C_2\mathbf 1_{2\nmid t}
 \prod_{\substack{p\mid t\\p>2}}\frac{p-1}{p-2}.$$ The Euler product is evaluated through $50000$ with the inherited positive tail enclosure. Logarithms use 100-digit midpoint intervals with a rational $10^{-70}$ guard; the final ratios use float64 and an outward guard $5\cdot10^{-8}$.

For a finite vector $x$ define $$\begin{aligned}
 E_e(x)&=\|C_ex\|_2^2,\\
 D_e(x)&=\sum_t x_t^2\sum_u C_e(u,t)^2,\\
 O_e(x)&=E_e(x)-D_e(x),\qquad R_e(x)=E_e(x)/D_e(x).\end{aligned}$$ The sign of $O_e$ is read from the guarded interval for $R_e$.

# The control-orbit decomposition

The five maps are $$\pi_0(i)=i,\quad \pi_{3,11}(i)=(3i+11)\bmod M,\quad
 \pi_{5,17}(i)=(5i+17)\bmod M,$$ $$\pi_{7,29}(i)=(7i+29)\bmod M,\qquad
 \pi_{\rm rev}(i)=M-1-i,qquad M=N/2.$$ The odd affine multipliers are units modulo the powers of two $M=2048,4096$. Consequently, each associated permutation matrix $P_j$ preserves the source multiset and Euclidean norm exactly. Put $$w_j=P_jv,\qquad \bar v=\frac15\sum_{j=1}^5w_j,
 \qquad z_j=w_j-\bar v.$$ Then $\sum_jz_j=0$.

#### Theorem (finite mean–centered identity).

For any real matrix $A$ and finite vectors $w_j$, with $q_A(x)=x^TA^TAx$, one has $$\label{eq:quadratic}
 \frac15\sum_{j=1}^5q_A(w_j)=q_A(\bar v)+
 \frac15\sum_{j=1}^5q_A(z_j).$$

#### Proof.

Expand $q_A(\bar v+z_j)$ and sum, as in the standard finite quadratic-form expansion `\cite{horn2013matrix}`. The cross term is $2\bar v^TA^TA(\sum_jz_j)/5=0$. This is finite bilinearity and uses no limit or number-theoretic estimate. $\square$

Apply [\[eq:quadratic\]](main.tex#L132){reference-type="eqref" reference="eq:quadratic"} to $A=C_e$, and to the diagonal quadratic form $D_e(x)=x^T\Delta_ex$ where $\Delta_e=\operatorname{diag}(\sum_uC_e(u,t)^2)_t$. Subtracting gives $$\begin{aligned}
 \overline E_e&=E_e(\bar v)+E_e^{\rm cen},\\
 \overline D_e&=D_e(\bar v)+D_e^{\rm cen},\\
 \overline O_e&=O_e(\bar v)+O_e^{\rm cen},
 \label{eq:three}\end{aligned}$$ where an overline means the average over the five placements and “cen” means the average over $z_j$. Importantly, [\[eq:three\]](main.tex#L150){reference-type="eqref" reference="eq:three"} is an identity for quadratic values, not an average of the ratios $R_e$.

# Certificate protocol

The TPC-330 producer and certificate are parent-locked by normalized SHA-256. TPC-331 recomputes the same 32 rows, with four laws and the five maps, and stores for every law the three triples $(E,D,O)$, their guarded ratios, the coherent/centered energy fractions, and the three floating-point identity residuals. The exact anchor is the interval $[36001,36016]$ with $Q=4$, shell $\{5,7\}$, $s=1$, and $$v_t=\mathbf 1_{t+2\ \mathrm{prime}}-\mathbf 1_{t\ \mathrm{odd}}.$$ All entries of this anchor are computed as reduced rational numbers.

The independent checker uses separate trial factorization and reverse shell accumulation, then recomputes the mean and centered vectors directly. The stress checker performs exact small-matrix algebra and rejects representative mutations of a component, census, digest, protocol, and claim firewall. The local Bridge-B wrapper is fail-closed; the Session-named evaluator files are not present in this checkout.

# Finite decomposition results

Table [1](main.tex#L184){reference-type="ref" reference="tab:decomp"} gives negative/positive counts over the 32 rows. No component observation is unresolved.

<div id="tab:decomp">

| law               |  control average|  coherent mean|  centered position|
|:------------------|----------------:|--------------:|------------------:|
| all-plus          |             0/32|           1/31|               0/32|
| alternating index |             23/9|           23/9|               23/9|
| mod-$4$ character |             32/0|           32/0|               32/0|
| half split        |             32/0|           32/0|               32/0|

: Three-component off-diagonal census.

</div>

For all-plus, the ratio ranges are $$\begin{array}{c|c}
\text{component}&\text{range of }E/D\\ \hline
\text{control average}&[1.0291358503710915,\;2.6078747190560239]\\
\text{coherent mean}&[0.99496392236342945,\;4.7216117506002702]\\
\text{centered position}&[1.0059897276060032,\;2.7607585737280149].
\end{array}$$ Thus the averaged and centered terms have a positive margin on every row, whereas the coherent term has exactly one scoped negative row. The coherent energy fraction lies in $$[0.14793771984595222,\;0.39709863476862445],$$ so the centered fraction is between $0.6029013652313755$ and $0.85206228015404784$. These fractions are finite diagnostics, not probabilities or asymptotic densities.

The all-plus component signatures are $$(+,-,+)\quad\text{on one row},\qquad
 (+,+,+)\quad\text{on 31 rows},$$ where the order is average, coherent, centered. For the alternating law the six observed signatures are finite mixed types; mod-$4$ and half split are $( -,-,-)$ on all 32 rows.

The largest recorded float64 decomposition residuals are $$4.76837158203125\cdot10^{-6}\quad(E),\qquad
2.6226043701171875\cdot10^{-6}\quad(D),\qquad
5.9604644775390625\cdot10^{-6}\quad(O).$$ They are retained in the certificate and are far below the scale-relative replay tolerance. The exact anchor, rather than these residuals, carries the symbolic identity evidence.

# Exact rational anchor

For the anchor, the identity placement gives $$E=306.7544239093389,\quad D=332.4445614235858,\quad
 O=-25.69013751424689.$$ The five-control average and its two components give $$\begin{array}{c|rrr}
 &E&D&O\\ \hline
\text{average}&363.6332602358012&317.6172879064013&46.01597232939993\\
\text{coherent}&133.3854380709001&137.9827494868488&-4.597311415948666\\
\text{centered}&230.2478221649011&179.6345384195525&50.6132837453486.
\end{array}$$ Exact fraction arithmetic verifies, in all three columns, $$(\text{average})=(\text{coherent})+(\text{centered}).$$ The reduced numerator/denominator digests are stored in the machine-readable certificate and independently replayed. Decimal values above are only a readable projection of those fractions.

# Interpretation and claim boundary

The strongest finite positive result is a localization: the all-plus positive response survives control averaging and is entirely positive in the centered position component on the frozen panel. The coherent mean is almost as strong, but has one negative row, so the data do not support replacing the position-aware problem by a purely source-aligned one.

The strongest obstruction is equally important. The decomposition does not make the centered term small: it carries roughly 60–85 percent of the finite all-plus energy. Therefore a future theorem must control this position-aware component rather than infer cancellation from source norm, coordinate multiset, or control averaging.

The release labels are:

-   `PROVED_EXACT_FINITE`: the mean–centered identities, finite Gram split, and rational anchor;

-   `NUMERICALLY_CERTIFIED_FINITE`: 32 rows, four laws, three components, independent replay, and mutation stress;

-   `NUMERICAL_OBSERVATION`: ratio ranges and energy fractions;

-   `OPEN`: uniform position-response bounds, growing source-native $L^2$, canonical sign, strict $1/400$ payment, full Gate B, and the twin-prime endpoint.

Hence $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
 \texttt{FIXED\_POWER\_CREDIT=0},\qquad
 \texttt{FULL\_GATE\_B=OPEN},\qquad
 \texttt{TWIN\_PRIME\_RESULT=NONE}.$$

# Reproducibility

The project directory contains the derivation and proof packages, canonical certificate, producer, independent replay, stress audit, and local Bridge-B checker. The compiled manuscript is `paper/paper.pdf`. All claims are scoped to the declared finite model; no official Route-A or Route-B pass is claimed.

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
