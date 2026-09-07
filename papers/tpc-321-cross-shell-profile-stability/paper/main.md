# Cross-Shell Stability and Majorization of the\ Trace-Normalized Spectrum of a Literal Prime–Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 31 August 2026
- Source repository commit: `88c46824c79e9c202a698cf4db36fcaf98260537`
- Converter: `source-markdown-audit-v2`

## Abstract

We continue a finite structural audit of a deleted-diagonal, centered prime–shell operator used in a twin-prime research route. The preceding project removed source-count bookkeeping by normalizing the Gram spectrum by its trace. Here we ask whether the resulting ordered spectral profile is stable when the prime shell changes. For a positive-semidefinite Gram matrix $G$ with decreasing eigenvalues, let $p(G)=(\lambda_j/\operatorname{tr}(G))_j$. We compare adjacent shell anchors using the $\ell^1$ profile distance, a maximum partial-sum (Lorenz/Ky Fan) distance, and its integrated version. On 24 literal matrices and 18 adjacent-shell comparisons, outward numerical intervals certify $D_{\mathrm{TV}}>0.03$ and $D_{\mathrm{L}}>0.02$ in every case. The partial sums exhibit three forward majorization, two reverse majorization, and thirteen mixed patterns. Thus a single shell-monotone profile law is a finite-panel obstruction, not an asymptotic theorem. The exact positive-scalar invariance and the independent reverse-order replay make the result reproducible, while signed prime-shell reassembly, arithmetic cancellation, power saving, and a twin-prime theorem remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

This paper stays inside one dynamical-system family: the literal deleted-diagonal centered prime–shell operator used in TPC-318–320. TPC-320 showed that trace-normalized top-$k$ shares decrease along the tested source scales. That observation leaves a different question which cannot be answered by another top-$k$ slope:

> At a fixed source scale, does the complete trace-normalized ordered spectrum remain stable as the prime shell changes?

We make “complete” precise by comparing the whole vector of normalized eigenvalue masses in rank order. The result is deliberately finite. It is intended to locate a structural obstruction on the research map, not to turn 18 numerical comparisons into a uniform statement about the primes.

# Frozen operator and normalized profile

Let $I_X=(X/2,X]\cap\mathbb Z$, let $\mathcal S_Q=\{p:Q<p\leq2Q,\ p\text{ prime}\}$, and let $H=66$. For $s\in\{1,2\}$ define $$B_{p,s}(u,t)=\mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}
 \frac{pH^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{u\equiv t\pmod p}-\frac{1}{p-1}\right).
 \label{eq:block}$$ The matrix $A_{X,Q,s}$ has rows $(p,u)\in\mathcal S_Q\times I_X$ and columns $t\in I_X$. We use the Gram matrix $$G_{X,Q,s}=A_{X,Q,s}^{\mathsf T}A_{X,Q,s}.
 \label{eq:gram}$$ It is positive semidefinite by construction. Write $N=|I_X|$ and $$\lambda_1(G)\geq\cdots\geq\lambda_N(G)\geq0,\qquad
 T(G)=\operatorname{tr}(G),\qquad p_j(G)=\frac{\lambda_j(G)}{T(G)}.$$ The vector $p(G)$ is an ordered probability profile whenever $T(G)>0$.

> **Proposition: scale-invariant profile** For every $c>0$, $p_j(cG)=p_j(G)$. Hence every function of the profile, including the distances below and all Ky Fan cumulative masses, is invariant under $G\mapsto cG$.

> **Proof** The eigenvalues and trace of $cG$ are $c\lambda_j(G)$ and $cT(G)$, respectively. Cancelling $c$ gives the assertion term by term.

# Profile distances and the majorization firewall

For two same-dimensional profiles $p,q$, define the partial-sum difference $$d_r(p,q)=\sum_{j=1}^r(p_j-q_j),\qquad 1\leq r<N.$$ We use three finite diagnostics: $$D_{\mathrm{TV}}(p,q)=\frac12\sum_{j=1}^N|p_j-q_j|,\qquad
 D_{\mathrm{L}}(p,q)=\max_{r<N}|d_r(p,q)|,
 \label{eq:dist}$$ $$D_{\mathrm{int}}(p,q)=\frac1{N-1}\sum_{r<N}|d_r(p,q)|.
 \label{eq:integrated}$$ The first is the $\ell^1$ distance between the ordered rank-mass vectors. The second and third measure the discrepancy of their cumulative Ky Fan profiles. They are rank-profile diagnostics; we do not call them a Wasserstein distance between measures on the numerical eigenvalue axis.

We say $p$ majorizes $q$, written $p\succeq q$, when $d_r(p,q)\geq0$ for all $r<N$. A finite sign tolerance $\tau=10^{-8}$ is used only to classify computed signs. A pair is “mixed” when its cumulative differences have both signs beyond $\tau$.

> **Proposition: finite metric facts** The three quantities in [\[eq:dist\]](main.tex#L108){reference-type="eqref" reference="eq:dist"}–[\[eq:integrated\]](main.tex#L112){reference-type="eqref" reference="eq:integrated"} are symmetric, nonnegative, and at most one. The $\ell^1$ profile distance obeys the triangle inequality. If $p\succeq q$, then $D_{\mathrm{L}}(p,q)=\max_{r<N}d_r(p,q)$.

> **Proof** These statements follow from the corresponding elementary facts for the absolute value and the finite $\ell^1$ norm. Since $p$ and $q$ are probability vectors, their $\ell^1$ distance is at most two. The partial sums lie in $[0,1]$, giving the bounds for the other two quantities. Under majorization all partial differences are nonnegative, so the absolute values may be removed in the maximum.

The ordering matters. A global positive rescaling disappears from $p$, but changing the shell changes the operator itself. The present experiment tests whether that remaining dependence is negligible or systematic.

# Protocol and finite enclosure

The panel is $$X\in\{640,1280,2560\},\qquad
 Q\in\{24,36,54,80\},\qquad s\in\{1,2\}.$$ There are 24 rows. At each fixed $(X,s)$ we compare the three adjacent shell transitions $24\to36$, $36\to54$, and $54\to80$, for 18 comparisons total.

For every row the producer accumulates the literal blocks in both forward and reverse prime order. NumPy and SciPy full symmetric eigensolvers provide three retained profiles: NumPy-forward, NumPy-reverse, and SciPy-forward. For each shell transition we evaluate all nine cross-path pairs. If their scalar values are $v_i$, the stored interval is $$[\max(0,\min_i v_i-10^{-12}),
   \min(1,\max_i v_i+10^{-12})].$$ This is an outward finite numerical guard, not an interval theorem for unlisted matrices. A separate checker reverses the shell loop, uses an `einsum` Gram accumulation, and recomputes the full spectrum without importing the producer. A deterministic stress suite tests scalar invariance, metric geometry, majorization labels, near-tie handling, and the separation thresholds.

# Results

Table [1](main.tex#L180){reference-type="ref" reference="tab:distances"} gives point-estimate ranges over the three source scales for each shell transition. The certificate uses the outward intervals; the table is a compact view of the same data. In the last column, P, R, and M mean forward majorization, reverse majorization, and mixed signs.

<div id="tab:distances">

| $s$ | $Q\to Q'$ | $D_{\mathrm{TV}}$ range | $D_{\mathrm{L}}$ range | $D_{\mathrm{int}}$ range | P/R/M |
|:---:|:---------:|:-----------------------:|:----------------------:|:------------------------:|:-----:|
|  1  | $24\to36$ |       .0832–.1079       |       .0831–.1079      |        .0503–.0587       | 3/0/0 |
|  1  | $36\to54$ |       .0386–.0498       |       .0280–.0484      |        .0196–.0290       | 0/0/3 |
|  1  | $54\to80$ |       .0321–.0584       |       .0234–.0361      |        .0045–.0137       | 0/0/3 |
|  2  | $24\to36$ |       .0417–.0507       |       .0234–.0376      |        .0132–.0217       | 0/0/3 |
|  2  | $36\to54$ |       .0950–.1100       |       .0946–.1092      |        .0286–.0388       | 0/0/3 |
|  2  | $54\to80$ |       .2233–.2597       |       .2232–.2597      |        .0916–.1006       | 0/2/1 |

: Cross-shell profile distances. Every interval lower endpoint in the certificate is above $0.03$ for $D_{\mathrm{TV}}$ and above $0.02$ for $D_{\mathrm{L}}$.

</div>

All 18 comparisons are strictly separated in both primary metrics. The smallest outward lower endpoints are $$\min D_{\mathrm{TV}}^- =0.03212981290619634,\qquad
 \min D_{\mathrm{L}}^- =0.02339722207455566.$$ The integrated discrepancy ranges from $0.0044941484$ to $0.1006381999$. The complete majorization census is 3 P, 2 R, and 13 M. In particular, the finite panel refutes both a universal forward direction and a universal reverse direction; it also rules out equality of neighboring ordered profiles at the declared resolution.

> **Remark: what the result is not** The statement “profile stability is refuted” is shorthand for the finite-panel status $$\texttt{REFUTED\_FINITE\_PANEL}.$$ It is not a theorem that all larger shells are separated, nor does it identify a limiting spectral law. The mixed majorization labels are an obstruction to a particularly simple monotone model, not a replacement theorem.

# Route status and conclusion

The strongest positive result is a scale-invariant, full-rank readout: after the trace removes global amplitude, adjacent prime shells still produce nontrivial profile changes on every tested transition. The strongest obstruction is structural heterogeneity: forward, reverse, and mixed partial sum patterns coexist, so one shell-monotone majorization principle cannot organize this panel.

The arithmetic gates remain open. The Gram construction squares an unsigned block and never reassembles the centered prime-shell signs into a signed bilinear estimate. Consequently this paper supplies no arithmetic cancellation, fixed-power credit, asymptotic theorem, or twin-prime result. The Session-named Route-A and Route-B evaluator files are absent from the checkout; the local Bridge-B checker is a fail-closed record of the finite certificate and must not be described as an official evaluator pass.

The next mathematically meaningful branch is either a theorem controlling the cross-shell profile distances under explicit hypotheses, or a signed projector reassembly that can explain why the observed profile sensitivity does (or does not) survive the arithmetic step. Neither should be inferred from this finite audit alone.

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. A. W. Marshall, I. Olkin, and B. C. Arnold, *Inequalities: Theory of Majorization and Its Applications*, 2nd ed., Springer, 2011. R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013. L. Wang, *Scale-Invariant Spectral Concentration and Participation Growth for a Literal Prime–Shell Operator*, TPC-320 project release, 2026.

<!-- SOURCE_BODY_END -->
