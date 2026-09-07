# A Convolution Interface for the Literal Prime Shell and the Divisibility–Mask Defect

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `1de1964aa411aa631587da690524beadf1127d3c`
- Converter: `source-markdown-audit-v2`

## Abstract

We isolate the two mechanisms in the literal deleted–diagonal prime–shell matrix used in the current twin–prime route. The residue kernel is a translation–invariant convolution on $\mathbb Z$, whereas the two endpoint divisibility masks are coordinate projections. We prove an exact convolution–plus–defect factorisation, the Fourier multiplier formula for the unmasked convolution on $\ell^2(\mathbb Z)$, and a finite triangle envelope which retains the mask defect. A guarded audit on two disjoint origins, three source counts, four shells, two kernel exponents, and four sign laws contains 192 rows. The ideal matrix is translation invariant in all 96 parameter groups, but the defect-to-ideal spectral ratio reaches $0.467075645603$ and exceeds $1/4$ in 93 rows. The result is a precise interface and a finite obstruction to discarding the masks; it is not an arithmetic $L^2$ estimate, a power saving, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The recent finite route has repeatedly encountered a distinction between a signed source calculation and the physical output operator. Here we return to the unresolved source-uniform $L^2$ question at the operator level. The question is deliberately narrow: can the literal matrix be compared with a translation-invariant object without erasing the divisibility information?

Throughout, $Q<p\leq 2Q$ ranges over primes, $H=66$, and $s\in\{1,2\}$. For $d\in\mathbb Z$ define $$k_p(d)=\begin{cases}
 0,&d=0,\\[2mm]
 \displaystyle p\frac{H^{2s}}{(H^2+d^2)^s}
 \left(\mathbf 1_{p\mid d}-\frac1{p-1}\right),&d\ne0.
 \end{cases} \label{eq:kernel}$$ For a sign law $e=(e_p)$ let $K_e=\sum_{Q<p\leq2Q}e_pK_p$, where $(K_pf)(u)=\sum_d k_p(d)f(u-d)$. The physical finite matrix on an interval $I$ has entries $$A_I(u,t)=\sum_p e_p\,\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}
 \mathbf 1_{p\nmid t}\,p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right). \label{eq:physical}$$ No source vector is needed for this interface audit. In particular, the finite table below must not be read as evidence for a twin-prime density.

# Exact factorisation

Let $P_p$ be multiplication by $\mathbf 1_{p\nmid n}$ on sequences, and let $E_I$ extend a vector on $I$ by zero while $R_I$ restricts a sequence to $I$.

> **Proposition: mask factorisation** With $K_p$ defined by [\[eq:kernel\]](main.tex#L58){reference-type="eqref" reference="eq:kernel"}, the physical operator is $$A_I=\sum_p e_pR_IP_pK_pP_pE_I. \label{eq:factor}$$ If $T_I=R_IK_eE_I$ and $D_I=A_I-T_I$, then $$D_I=\sum_p e_pR_I\bigl((P_p-I)K_pP_p+K_p(P_p-I)\bigr)E_I. \label{eq:defect}$$

> **Proof** The two projections in [\[eq:factor\]](main.tex#L79){reference-type="eqref" reference="eq:factor"} remove exactly the entries whose endpoints are divisible by $p$, and $k_p(0)=0$ removes the diagonal. This gives [\[eq:physical\]](main.tex#L66){reference-type="eqref" reference="eq:physical"} entry by entry. For one prime, $(P-I)KP+K(P-I)=PKP-K$; summing and applying restriction and extension gives [\[eq:defect\]](main.tex#L83){reference-type="eqref" reference="eq:defect"}. All sums over the shell are finite.

The decomposition is more informative than a generic Frobenius envelope: $T_I$ is the part to which Fourier analysis applies, while $D_I$ records every position-sensitive mask contribution.

# The unmasked Fourier interface

Since $|k_p(d)|\ll_{p,H,s}|d|^{-2s}$ for $d\ne0$, $k_e\in\ell^1(\mathbb Z)$. Its Fourier series $$\widehat{k}_e(\theta)=\sum_{d\in\mathbb Z}k_e(d)e^{-id\theta},
 \qquad -\pi\leq\theta\leq\pi,
 \label{eq:symbol}$$ is continuous and periodic.

> **Theorem: Fourier and compression bounds** For the explicitly unmasked operator $K_e$, $$\left\lVert K_e\right\rVert_{\ell^2(\mathbb Z)\to\ell^2(\mathbb Z)}
>  =\operatorname*{ess\,sup}_{\theta\in[-\pi,\pi]}|\widehat{k}_e(\theta)|
>  \leq\sum_{d\in\mathbb Z}|k_e(d)|. \label{eq:fourierbound}$$ For every finite interval $I$, $$\left\lVert A_I\right\rVert\leq\left\lVert T_I\right\rVert+\left\lVert D_I\right\rVert
>  \leq\left\lVert K_e\right\rVert+\left\lVert D_I\right\rVert_F. \label{eq:triangle}$$

> **Proof** The Fourier transform on $\ell^2(\mathbb Z)$ is unitary and sends convolution by $k_e$ to multiplication by [\[eq:symbol\]](main.tex#L106){reference-type="eqref" reference="eq:symbol"}; the norm of a multiplication operator is the essential supremum. Young’s inequality gives the second inequality in [\[eq:fourierbound\]](main.tex#L115){reference-type="eqref" reference="eq:fourierbound"}. Since $R_I$ and $E_I$ have norm one, $\left\lVert T_I\right\rVert\leq\left\lVert K_e\right\rVert$. Apply the triangle inequality to $A_I=T_I+D_I$ and then $\left\lVert D_I\right\rVert\leq\left\lVert D_I\right\rVert_F$.

For $R\geq1$, the tail in the Young envelope has the explicit bound $$\sum_{|d|>R}|k_e(d)|
 \leq \frac{2H^{2s}\sum_{Q<p\leq2Q}p}{(2s-1)R^{2s-1}}. \label{eq:tail}$$ Indeed, the centered residue factor has absolute value at most one and $\sum_{d>R}d^{-2s}\leq R^{1-2s}/(2s-1)$. Equation [\[eq:tail\]](main.tex#L136){reference-type="eqref" reference="eq:tail"} is a sign-free baseline; it supplies no cancellation.

# Finite audit

The protocol uses origins $40097$ and $48097$, source counts $M\in\{256,512,1024\}$, $Q\in\{24,36,54,80\}$, $s\in\{1,2\}$, and the four sign laws ‘all-plus’, alternating shell index, the mod–4 character, and the half split. Thus $2\cdot3\cdot4\cdot2\cdot4=192$ physical/ideal/defect rows. The Young finite sum uses $R=65536$ and the analytic tail in [\[eq:tail\]](main.tex#L136){reference-type="eqref" reference="eq:tail"}.

For each row we compute the symmetric spectral norms of $A_I$, $T_I$, and $D_I$, and the Frobenius norm of $D_I$. The certificate also checks $$\left\lVert A_I\right\rVert\leq\left\lVert K_e\right\rVert+\left\lVert D_I\right\rVert_F. \label{eq:finitecertificate}$$ For each fixed $(M,Q,s,e)$, translating the interval changes neither the differences nor the ideal matrix. There are 96 such two-origin checks.

| quantity                                                                |       certified finite readout|
|:------------------------------------------------------------------------|------------------------------:|
| physical rows                                                           |                            192|
| ideal translation checks                                                |                          96/96|
| combined-envelope checks                                                |                        192/192|
| minimum $\left\lVert D_I\right\rVert/\left\lVert T_I\right\rVert$       |                0.0312337689685|
| maximum $\left\lVert D_I\right\rVert/\left\lVert T_I\right\rVert$       |                 0.467075645603|
| rows with $\left\lVert D_I\right\rVert/\left\lVert T_I\right\rVert>1/4$ |                         93/192|
| range of $\left\lVert A_I\right\rVert/\left\lVert T_I\right\rVert$      |   0.938011283061–1.13920880401|
| range of combined occupancy                                             |  0.121634514969–0.682234184555|

: Summary of the 192-row finite spectral audit.

The ideal translation identity is exact at the displayed operator level; the 96/96 label records its independent floating-point replay. The defect ratio is not a monotone function of shell size or interval count: it is a diagnostic of the masks and their placement, not a candidate exponent.

# Adversarial checks and claim boundary

The independent checker rebuilds the shells and matrices in reverse prime order, recomputes all spectral quantities, and verifies the canonical JSON payload. A rational six-point anchor with $Q=4$ and shell $\{5,7\}$ checks the identity $A_I=T_I+D_I$ and symmetry without floating point. The stress suite attacks a sign-flipped defect, a reintroduced diagonal, random projection contractions, and the analytic tail scale. Normal and optimized executions agree byte-for-byte at the reporting layer and produce empty standard error.

The result supports the following narrow ledger:

| statement                               | status                       |
|:----------------------------------------|:-----------------------------|
| mask factorisation and defect identity  | proved exact finite          |
| unmasked Fourier multiplier interface   | proved exact conditional     |
| Young envelope and interval compression | proved exact                 |
| 192-row spectral replay                 | numerically certified finite |
| discarding masks on this declared panel | refuted scoped               |
| source-uniform arithmetic $L^2$         | open                         |
| fixed-power credit / Route-B Gate B     | $0$ / open                   |
| twin-prime conclusion                   | none                         |

> **Remark** The finite obstruction does not say that every possible mask estimate fails, nor that the defect has a positive asymptotic lower bound. It says only that the current finite physical object is not faithfully represented by its unmasked convolution on the tested panel. Any future arithmetic $L^2$ argument must either control $D_I$ with its position dependence or prove cancellation for the masked sum directly.

# Conclusion and next question

The main route contribution is a typed interface: Fourier analysis is available for a precisely identified unmasked component, and the missing piece is an explicit operator defect rather than an implicit normalization error. The finite audit shows that this defect is sometimes substantial, with 93 of 192 rows above the quarter threshold. We therefore freeze the shortcut of dropping the masks and return to the position-aware arithmetic $L^2$ problem. No arithmetic advance is claimed in this release.

<!-- SOURCE_BODY_END -->
