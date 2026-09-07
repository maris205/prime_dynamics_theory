# A Same-Clock Null-Channel Decomposition\ for the Literal V59 Signed Coupling

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST),; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-258 constructed a source-frozen transverse unit vector $z_{\mathrm{null}}$ for which the leading literal V59 adjoint diagonal cancels: $\langle z_{\mathrm{null}},A_x\beta\rangle=o(x^{7/6}/\log^3x)$. We now place that direction on the same clock as the physical hybrid residual $w(u)=\Lambda(u+2)-b_x^{(Z_x)}(u)$. A source-backed maximal-interval Type-I theorem controls each of the four consecutive Haar blocks and gives, for every fixed admissible $K$ and every fixed $M>0$, $$|\langle z_{\mathrm{null}},w\rangle|\ll_{M,K}\frac{x^{1/2}}{(\log x)^M}.$$ The exact Hilbert decomposition $$\langle w,A_x\beta\rangle
 =\overline{\langle z_{\mathrm{null}},w\rangle}\langle z_{\mathrm{null}},A_x\beta\rangle
   +\langle w_{\perp},A_x\beta\rangle$$ therefore makes the first rank-one channel $o(x^{5/3}/\log^{M+3}x)$. This is a source-backed advance for one literal signed-coupling channel, not for the full scalar. The orthogonal residual remains open, and an exact zero-diagonal finite witness shows that it can carry the entire scalar when the null channel vanishes. No fixed power saving, arithmetic $L^2$, full Gate B, strict global $1/400$ payment, or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Problem and claim boundary

The Route-B scalar needed downstream is not merely a product of two unrelated norms. On the literal V59 clock it has the signed form $$C_x=\langle w,A_x\beta\rangle.                                      \label{eq:fullscalar}$$ The preceding papers separately supplied a strong hybrid mean for $w$ and a source-frozen adjoint null direction `\cite{tpc254,tpc258}`. The smallest honest question is whether these facts suppress a precisely identified piece of [\[eq:fullscalar\]](main.tex#L64){reference-type="eqref" reference="eq:fullscalar"} on one and the same clock.

The answer is yes for one rank-one channel and no as a formal inference for the full scalar. We keep the residual in every identity. In particular, the phrase “null channel” below refers to the projection onto one fixed Haar direction; it never means that $C_x$ itself is zero or small.

Throughout, $$\langle f,g\rangle=\sum_u\overline{f(u)}g(u)$$ is conjugate-linear in the first slot. The literal $w$ and the Haar directions are real, while $A_x\beta$ may be complex.

# One clock, four blocks, and the frozen null direction

Let $x\to\infty$ through real values and put $$a=\lfloor x/2\rfloor,\qquad b=\lfloor x\rfloor,
 \qquad I_x=\{a+1,\ldots,b\},\qquad N=b-a.              \label{eq:clock}$$ Write $\ell=\lfloor N/2\rfloor$, $r=N-\ell$, and split the two ordered children into four consecutive blocks $B_1,\ldots,B_4$, of sizes $$s_1=\lfloor\ell/2\rfloor,\quad s_2=\ell-s_1,
 \qquad s_3=\lfloor r/2\rfloor,\quad s_4=r-s_3.          \label{eq:sizes}$$ Thus the blocks cover $I_x$ exactly for every admissible real clock, and $s_j=x/8+O(1)$.

For adjacent blocks of sizes $p,q$, define the normalized contrast $$h(A,B)=\left(\frac{pq}{p+q}\right)^{1/2}
 \left(\frac{\mathbf 1_A}{p}-\frac{\mathbf 1_B}{q}\right).$$ The two transverse descendants are $$z_1=h(B_1,B_2),\qquad z_2=h(B_3,B_4),                  \label{eq:descendants}$$ with normalizations $\rho_1^2=s_1s_2/(s_1+s_2)$ and $\rho_2^2=s_3s_4/(s_3+s_4)$.

Set $$L_1=\log(3456/3125),\qquad L_2=\log(884736/823543),
 \qquad L_T=(L_1^2+L_2^2)^{1/2},                       \label{eq:logs}$$ and freeze $$z_{\mathrm{null}}=\frac{L_2z_1-L_1z_2}{L_T}.                    \label{eq:null}$$

> **Lemma: Exact source geometry**<span id="lem:geometry" label="lem:geometry">\[lem:geometry\]</span> For every sufficiently large real $x$, the vectors $z_1,z_2$ are exactly orthonormal. Hence $z_{\mathrm{null}}$ is an exact unit vector. It depends only on the ordered source coordinates and the two fixed interval constants; it is independent of $w$, $\beta$, and the observed output.

> **Proof** For a contrast on blocks of sizes $p,q$, direct counting gives $$\|h(A,B)\|_2^2=\frac{pq}{p+q}\left(\frac1p+\frac1q\right)=1.$$ The supports of $z_1$ and $z_2$ are disjoint, so their inner product is zero. Equation [\[eq:null\]](main.tex#L119){reference-type="eqref" reference="eq:null"} then has squared norm $(L_2^2+L_1^2)/L_T^2=1$. Every quantity in its definition is fixed before either literal coefficient is inspected.

TPC-258 proved, with $$S_x=\frac{x^{7/6}}{\log^3x},                           \label{eq:scale}$$ the source-backed cancellation $$\langle z_{\mathrm{null}},A_x\beta\rangle=o(S_x).                         \label{eq:tpc258}$$ It arises because the two leading curvatures are $L_1/2,L_2/2$, so their cross combination cancels exactly. Equation [\[eq:tpc258\]](main.tex#L146){reference-type="eqref" reference="eq:tpc258"} is an $o(1)$ statement and is not promoted here to a fixed-power estimate.

# Four-block control of the literal hybrid residual

Fix a finite admissible $K$ and write $$Z_x=(\log x)^K,\qquad
 w(u)=\Lambda(u+2)-b_x^{(Z_x)}(u).                     \label{eq:w}$$ The source-locked hybrid maximal Type-I theorem, through its nonnegative $m=1$ row, gives for every fixed $M>0$ $$\max_{\substack{J\subset I_x\\J\ \mathrm{consecutive}}}
 \left|\sum_{u\in J}w(u)\right|
 \ll_{M,K}\frac{x}{(\log x)^M}.                       \label{eq:maximal}$$ We record the consequence for the frozen transverse direction.

> **Theorem: Source-backed null moment**<span id="thm:w-null" label="thm:w-null">\[thm:w-null\]</span> For every fixed admissible $K$ and every fixed $M>0$, $$\boxed{\displaystyle
>  |\langle z_{\mathrm{null}},w\rangle|\ll_{M,K}\frac{x^{1/2}}{(\log x)^M}.} \label{eq:w-null}$$ The implied constant is not uniform in $M$ or $K$.

> **Proof** Let $W_j=\sum_{u\in B_j}w(u)$. Each $B_j$ is one of the consecutive intervals admitted in [\[eq:maximal\]](main.tex#L164){reference-type="eqref" reference="eq:maximal"}, so $$|W_j|\ll_{M,K}\frac{x}{(\log x)^M},\qquad 1\le j\le4. \label{eq:blocksum}$$ The exact Haar formulas are $$\langle z_1,w\rangle=\rho_1\left(\frac{W_1}{s_1}-\frac{W_2}{s_2}\right),
>  \qquad
>  \langle z_2,w\rangle=\rho_2\left(\frac{W_3}{s_3}-\frac{W_4}{s_4}\right).$$ Here $s_j=x/8+O(1)$, while $\rho_i\le\sqrt{s_{2i-1}+s_{2i}}/2\ll\sqrt{x}$. Dividing [\[eq:blocksum\]](main.tex#L181){reference-type="eqref" reference="eq:blocksum"} by the block sizes therefore gives $$|\langle z_1,w\rangle|+|\langle z_2,w\rangle|
>  \ll_{M,K}\frac{x^{1/2}}{(\log x)^M}.$$ Finally, [\[eq:null\]](main.tex#L119){reference-type="eqref" reference="eq:null"} is a fixed linear combination whose coefficient $\ell^1$-norm is less than two. This proves [\[eq:w-null\]](main.tex#L172){reference-type="eqref" reference="eq:w-null"}.

> **Remark: Quantifiers** The theorem means: first freeze finite $K$, then choose fixed $M$, then take $x\ge x_0(M,K)$. Arbitrary fixed logarithmic saving does not imply $x^{1/2-\delta}$ for any fixed $\delta>0$.

# Exact signed-coupling split

Put $$c_x=\langle z_{\mathrm{null}},w\rangle,\qquad
 w_{\parallel}=c_xz_{\mathrm{null}},\qquad
 w_{\perp}=w-c_xz_{\mathrm{null}}.                                  \label{eq:projection}$$ Since $z_{\mathrm{null}}$ is unit, $\langle z_{\mathrm{null}},w_{\perp}\rangle=0$. The next identity is purely finite-dimensional and requires no symmetry of $A_x$.

> **Proposition: Rank-one/residual identity**<span id="prop:split" label="prop:split">\[prop:split\]</span> For every finite clock, $$\boxed{\displaystyle
>  \langle w,A_x\beta\rangle
>  =\overline{c_x}\langle z_{\mathrm{null}},A_x\beta\rangle
>   +\langle w_{\perp},A_x\beta\rangle.}                            \label{eq:split}$$

> **Proof** Equation [\[eq:projection\]](main.tex#L212){reference-type="eqref" reference="eq:projection"} gives $w=c_xz_{\mathrm{null}}+w_{\perp}$. By conjugate-linearity in the first slot, $$\langle c_xz_{\mathrm{null}},A_x\beta\rangle
>  =\overline{c_x}\langle z_{\mathrm{null}},A_x\beta\rangle.$$ Adding the residual term proves [\[eq:split\]](main.tex#L223){reference-type="eqref" reference="eq:split"}.

> **Theorem: Same-clock null-channel suppression**<span id="thm:channel" label="thm:channel">\[thm:channel\]</span> For every fixed admissible $K$ and every fixed $M>0$, the first term in [\[eq:split\]](main.tex#L223){reference-type="eqref" reference="eq:split"} satisfies $$\boxed{\displaystyle
>  \overline{\langle z_{\mathrm{null}},w\rangle}\langle z_{\mathrm{null}},A_x\beta\rangle
>  =o\!\left(\frac{x^{5/3}}{\log^{M+3}x}\right).}       \label{eq:main}$$

> **Proof** Write $\langle z_{\mathrm{null}},A_x\beta\rangle=S_xe(x)$, where $e(x)\to0$ by [\[eq:tpc258\]](main.tex#L146){reference-type="eqref" reference="eq:tpc258"}. Theorem [\[thm:w-null\]](main.tex#L168){reference-type="ref" reference="thm:w-null"} gives $$\left|\overline{c_x}\langle z_{\mathrm{null}},A_x\beta\rangle\right|
>  \ll_{M,K}\frac{x^{1/2}}{\log^Mx}\,
>               \frac{x^{7/6}}{\log^3x}|e(x)|.$$ Since $1/2+7/6=5/3$, this is exactly [\[eq:main\]](main.tex#L243){reference-type="eqref" reference="eq:main"}.

The theorem controls one explicitly identified piece of the literal scalar [\[eq:fullscalar\]](main.tex#L64){reference-type="eqref" reference="eq:fullscalar"}. It says nothing yet about $$R_x=\langle w_{\perp},A_x\beta\rangle.                            \label{eq:residual}$$ This term is not discarded, bounded by wishful orthogonality, or absorbed into the little-oh notation.

# Conditional rate and the residual obstruction

TPC-258 isolated the following stronger rate as conditional: if its two scalar remainders satisfy $$\langle z_{\mathrm{null}},A_x\beta\rangle
 \ll_{\psi,\varepsilon}\frac{S_x}{\log x}+x^{55/48+\varepsilon},$$ then Theorem [\[thm:w-null\]](main.tex#L168){reference-type="ref" reference="thm:w-null"} gives $$|\overline{c_x}\langle z_{\mathrm{null}},A_x\beta\rangle|
 \ll_{M,K,\psi,\varepsilon}
 \frac{x^{5/3}}{\log^{M+4}x}
 +\frac{x^{79/48+\varepsilon}}{\log^Mx}.                       \label{eq:conditional}$$ Indeed, $1/2+55/48=79/48$, while $5/3=80/48$; the boundary exponent has a $1/48$ gap before $\varepsilon$. Equation [\[eq:conditional\]](main.tex#L279){reference-type="eqref" reference="eq:conditional"} is a `CONDITIONAL_THEOREM`, not an unconditional fixed-power claim.

The open residual cannot be controlled by projection algebra alone.

> **Proposition: Exact synthetic non-promotion witness**<span id="prop:witness" label="prop:witness">\[prop:witness\]</span> There exist a real unit vector $z$, real vectors $w,\beta$, and a real zero-diagonal matrix $A$ such that $$\langle z,w\rangle=0,\qquad
>  \overline{\langle z,w\rangle}\langle z,A\beta\rangle=0,\qquad
>  \langle w,A\beta\rangle\ne0.$$

> **Proof** In $\mathbb R^2$, choose $$z=(1,0),\qquad w=(0,1),\qquad \beta=(1,0),\qquad
>  A=\begin{pmatrix}0&0\\ \lambda&0\end{pmatrix}$$ with $\lambda\ne0$. Then $A\beta=(0,\lambda)$, so $\langle z,w\rangle=\langle z,A\beta\rangle=0$, while $\langle w,A\beta\rangle=\lambda$. Here $w_\perp=w$, and the residual carries the entire scalar.

This witness is structural. It is not claimed to arise from the literal prime shell, and it does not refute any arithmetic estimate. It refutes only the attempted implication from null-channel suppression to full-scalar suppression without an additional theorem.

# Route evaluation

The strongest positive result is the source-backed estimate [\[eq:main\]](main.tex#L243){reference-type="eqref" reference="eq:main"} for one same-clock signed channel. The strongest obstruction is exact: the perpendicular residual [\[eq:residual\]](main.tex#L261){reference-type="eqref" reference="eq:residual"} may carry all of a general zero-diagonal scalar. The next open theorem is therefore to estimate $R_x$ for the literal V59 operator, or to reassemble all four signed packets while retaining that residual explicitly.

The reusable chain is $$\text{same clock}\to\text{four-block Haar null}
 \to\text{maximal-interval }w\text{ moment}
 \to\text{exact rank-one split}
 \to\text{residual firewall}.$$ No step supplies arithmetic $L^2$, a full Gate-B upper estimate, the strict global $1/400$ endpoint, a fixed atom, or a twin-prime theorem.

# Reproducibility and epistemic labels

The companion certificate reconstructs the exact real-clock block geometry, the source-frozen null weights, the projection identity, the exponent ledger, and the zero-diagonal witness. A separate implementation rejects mutations that replace the residual status `OPEN` by a theorem, and a stress family varies integral and nonintegral clocks and both signs of $\lambda$. Finite checks receive no prime-asymptotic proof credit. The maximum status is $$\texttt{PROVED\_SOURCE\_BACKED\_SAME\_CLOCK\_NULL\_CHANNEL\_SUPPRESSION\_}$$ $$\texttt{FOR\_LITERAL\_V59\_SIGNED\_COUPLING}.$$

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc254,
  author = {Liang Wang},
  title = {Source-Backed Rank-Midpoint Hybrid-Mean Closure},
  year = {2026},
  howpublished = {Prime Dynamics Theory, TPC-254 project and Bridge B V107}
}

@misc{tpc258,
  author = {Liang Wang},
  title = {A Source-Frozen Transverse Null Direction for the Literal {V59} Adjoint},
  year = {2026},
  howpublished = {Prime Dynamics Theory, TPC-258 project}
}
```

<!-- SOURCE_BODY_END -->
