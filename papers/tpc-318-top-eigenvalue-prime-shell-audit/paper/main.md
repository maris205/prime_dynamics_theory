# Finite Top-Eigenvalue Readout for a Literal Prime–Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 31 August 2026
- Source repository commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding TPC-317 study replaced a finite Frobenius envelope by the Schatten–4 quantity $\sqrt{\operatorname{tr}(G^2)}$ for a literal deleted-diagonal prime–shell Gram matrix $G=A^*A$, while leaving the actual top eigenvalue open. We compute that top eigenvalue directly on the same locked operator, using forward and reverse shell accumulation, a symmetric subset eigensolver, and an independent full-spectrum replay. For $X=640,1280,2560$, $Q\in\{24,36,54,80\}$, and $s\in\{1,2\}$, all 24 normalized top-eigenvalue rows are enclosed by finite numerical intervals and all 16 adjacent-scale comparisons are strictly decreasing. The corresponding finite log-base-two slopes lie between $-0.9972$ and $-0.4239$. This positive spectral readout has an equally important obstruction: ten of the 24 rows have relative top/second-eigenvalue gap below $0.01$, with minimum about $0.001704$. Thus a single leading eigenvector is not a stable arithmetic channel on these panels. The result is a finite numerical certificate, not an asymptotic estimate, arithmetic cancellation theorem, or proof of the twin-prime conjecture.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim ceiling

The TPC route studies whether a literal prime-shell source operator can be reassembled with a power saving. TPC-316 supplied the full finite operator but used its Hilbert–Schmidt mass as an intentionally loose interface; TPC-317 proved and measured the next trace-power envelope. The remaining local question is whether the actual spectral radius is smaller and has a coherent finite trend. This is a diagnostic question about one fixed dynamical-system family, not a replacement for the missing arithmetic theorem.

Our claim levels are deliberately separated:

-   the PSD and perturbation statements below are exact finite linear algebra;

-   the 24-row eigenvalue readout and its 16 strict comparisons are `NUMERICALLY_CERTIFIED_FINITE` under a declared error model;

-   the normalized trend, the finite slopes, and the gap census are `NUMERICAL_OBSERVATIONS`;

-   growing arithmetic cancellation, a fixed-power credit, Gate B, and a twin-prime conclusion remain open.

# The frozen operator

For an even scale $X$, put $$I_X=\{X/2+1,\ldots,X\},\qquad
 S_Q=\{p: p\text{ prime},\ Q<p\leq 2Q\},$$ and fix $H=66$. The literal entry is $$K_{p,u,t}^{(s)}={\bf 1}_{u\ne t}{\bf 1}_{p\nmid ut}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left({\bf 1}_{u\equiv t\pmod p}-\frac1{p-1}\right).
 \label{eq:entry}$$ The matrix $A_{Q,s,X}$ maps a source vector indexed by $I_X$ to coordinates indexed by $S_Q\times I_X$, and $G=A^*A$ acts on the source space. The operator, masks, source normalization, and shell rule are unchanged from the locked TPC-317 artifact `\cite{tpc317}`.

> **Proposition: finite PSD and trace-power facts** For every finite row, $G$ is positive semidefinite. If its eigenvalues are $\lambda_1\geq\cdots\geq\lambda_N\geq0$, then $$\lambda_1\leq\bigl(\operatorname{tr}(G^2)\bigr)^{1/2}\leq\operatorname{tr}(G).
>  \label{eq:chain}$$

> **Proof** The identity $G=A^*A$ gives positive semidefiniteness. The first inequality is $\lambda_1^2\leq\sum_i\lambda_i^2$, and the second follows from nonnegativity of the eigenvalues.

The point of this paper is not to reprove [\[eq:chain\]](main.tex#L88){reference-type="eqref" reference="eq:chain"}, but to measure $\lambda_1$ itself and to test whether its leading eigenspace is isolated.

# Finite error model

All entries in [\[eq:entry\]](main.tex#L76){reference-type="eqref" reference="eq:entry"} are rational. Large panels are nevertheless evaluated in binary64. The code accumulates $G$ once in increasing prime order and once in decreasing order, symmetrizes each result, and obtains the top two eigenvalues with a symmetric subset driver. A full NumPy $\operatorname{eigvalsh}$ calculation supplies a second scalar readout for each accumulation path.

The literal entry bound used in the guard is $$|K_{p,u,t}^{(s)}|\leq160.
 \label{eq:entrybound}$$ Indeed, every declared shell has $p\leq157$, the kernel factor is at most one, and the centered factor has modulus at most one. If $\widehat G$ is a computed matrix and $\|G-\widehat G\|_2\leq\varepsilon$, Weyl’s inequality gives $$|\lambda_1(G)-\lambda_1(\widehat G)|\leq\varepsilon.
 \label{eq:weyl}$$ We use the elementary conversion $\|E\|_2\leq\|E\|_F\leq N\max_{i,j}|E_{ij}|$, with a generous accumulation multiplier, and add the observed dual-path spread and eigensolver residual. The resulting interval is a finite numerical enclosure under this model. It is not a formal theorem about every floating-point implementation; that is why the large-panel claim remains numerical. Weyl’s inequality itself is standard finite matrix theory `\cite{weyl,hj}`.

# Certificate and independent replay

The canonical certificate contains 24 rows, each identified by $(X,Q,s)$. The reported spectral quantity is $$\Lambda_{Q,s}(X)=\frac{\lambda_1(G_{Q,s,X})}{N},
 \qquad N=|I_X|=X/2.
 \label{eq:normalized}$$ For each row the interval contains the four top estimates (two eigensolver families and two shell orders), the largest returned residual, the propagated matrix guard, and an outward decimal pad. The independent checker does not import the producer: it reconstructs the same literal matrix with a reverse shell einsum accumulation and checks that its full-spectrum top eigenvalue lies inside the stored interval.

As a small exact anchor, the checker constructs the rational one-prime panel $I=\{17,\ldots,32\}$, $p=5$, $s=1$. It records exact digests for $\operatorname{tr}(G)$, $\operatorname{tr}(G^2)$, and a positive coordinate Rayleigh witness. This anchor checks the rational matrix convention without pretending that the 24 large rows are exact algebraic eigenvalue computations.

# Results

Table [\[tab:top\]](main.tex#L159){reference-type="ref" reference="tab:top"} gives the normalized top readout. The intervals are wider than the displayed centers; every adjacent comparison was made using interval separation rather than rounded centers.

For all eight $(Q,s)$ rows, both transitions are decreasing. The 16 interval ratios range from approximately $0.50096$ to $0.80618$, equivalently the finite base-two slopes range from $-0.9972377$ to $-0.4238528$. Thus the top-eigenvalue readout is materially sharper than the TPC-317 Schatten–4 upper envelope on these finite panels.

The gap in the last column is $1-\lambda_2/\lambda_1$. Ten of the 24 individual rows have gap below $0.01$; the global minimum is $0.0017043531$. This is not a numerical failure: it is the main structural warning supplied by the new calculation.

# What the result does and does not buy

There are two different notions of scale in the certificate. The normalized quantity [\[eq:normalized\]](main.tex#L135){reference-type="eqref" reference="eq:normalized"} decreases, but the unnormalized top eigenvalue is $N\Lambda_{Q,s}(X)$. Adding the source-count exponent shifts each finite log-base-two slope by $+1$; the corresponding unnormalized slopes therefore range approximately from $0.0027623$ to $0.5761472$. The finite data do not pay a uniform source-to-output power saving under either convention.

Moreover, a small top/second gap makes a single top eigenvector sensitive to perturbations and to the choice of shell scale. A future arithmetic argument would need a clustered spectral projector, a stable subspace comparison, or a direct signed reassembly estimate. The present calculation supplies none of these. In particular, the 16 finite decreases cannot be used as a fixed-power credit, and no prime cancellation has been evaluated.

# Conclusion and next question

The direct finite spectral readout closes the local question left by TPC-317: the normalized top eigenvalue decreases on all 16 declared adjacent comparisons and is substantially sharper than the trace-power envelope. It simultaneously opens the next, more relevant question: how much of this readout belongs to a stable leading spectral subspace, and how much is a near-degenerate cluster? The current claim firewall is $$\begin{array}{ll}
\texttt{PROVED\_EXACT\_FINITE}:&\text{PSD spectrum facts and Weyl inequality},\\
\texttt{NUMERICALLY\_CERTIFIED\_FINITE}:&24\text{ rows; }16\text{ strict decreases; dual replay},\\
\texttt{OPEN}:&\text{cluster theorem, growing law, arithmetic cancellation, Gate B, TPC}.
\end{array}$$ The natural continuation is a spectral-cluster and normalization audit on the same prime-shell family.

# References

9 H. Weyl, Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen, *Math. Ann.* 71 (1912), 441–479.

R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013.

Liang Wang, *Schatten–4 Compression of a Literal Prime–Shell Operator*, TPC-317 project artifact, 2026, local release package.

<!-- SOURCE_BODY_END -->
