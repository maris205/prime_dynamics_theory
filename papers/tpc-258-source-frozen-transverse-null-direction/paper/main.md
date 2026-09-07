# A Source-Frozen Transverse Null Direction\ for the Literal V59 Adjoint

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

TPC-257 found a same-order two-dimensional transverse floor for the literal V59 adjoint. We use only its limiting curvature constants $L_1=\log(3456/3125)$ and $L_2=\log(884736/823543)$ to form the unit direction $z_{\rm null}=(L_2z_1-L_1z_2)/(L_1^2+L_2^2)^{1/2}$. Exact Haar orthogonality makes this direction source-frozen. Since the two curvature constants are $\kappa_i=L_i/2$, the leading $B_Q$ diagonal cancels and $$\langle z_{\rm null},A_x\beta\rangle
 =o\!\left(x^{7/6}/\log^3x\right).$$ An explicit inherited rate gives only a conditional refinement. The unconditional theorem is not called a fixed-power saving: an $o(1)$ error may decay as slowly as $1/\sqrt{\log x}$. Full arithmetic $L^2$, Gate B, the strict global $1/400$ payment, and a twin-prime conclusion remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

The preceding paper isolated a genuine two-dimensional transverse floor `\cite{tpc257}`, but a floor does not determine the direction of its leading vector. The precise question here is whether the known diagonal can be cancelled without looking at the coefficient. We answer the smallest source-only version of that question using the two descendants of the left and right rank children.

The word “source-frozen” is intentional: the direction is fixed from ordered coordinates and limiting interval constants before inspecting any coefficient, sign, or finite sample. The word “null” refers only to the leading two-coordinate diagonal. No arithmetic $L^2$ upper bound is hidden in the result.

# Literal clock and four-block frame

Let $x\to\infty$ through real values and put $$a=\lfloor x/2\rfloor,\qquad b=\lfloor x\rfloor,
 \qquad I_x=\{a+1,\ldots,b\},\qquad N=b-a.
 \label{eq:clock}$$ The ordered rank split is inherited from the source-frozen compiler `\cite{tpc253}`: $$\ell=\lfloor N/2\rfloor,\quad r=N-\ell,\quad m=a+\ell,
 \quad L=\{a+1,\ldots,m\},\quad R=\{m+1,\ldots,b\}.
 \label{eq:rank}$$ Split the two children in their physical order: $$s_1=\lfloor\ell/2\rfloor,\quad s_2=\ell-s_1,
 \qquad s_3=\lfloor r/2\rfloor,\quad s_4=r-s_3.       \label{eq:blocksizes}$$ Let $B_1,B_2$ be the consecutive subintervals of $L$ of lengths $s_1,s_2$, and let $B_3,B_4$ be the analogous subintervals of $R$. For adjacent intervals $A,B$ of lengths $p,q$, define $$h(A,B)=\left(\frac{pq}{p+q}\right)^{1/2}
 \left(\frac{\mathbf 1_A}{p}-\frac{\mathbf 1_B}{q}\right).       \label{eq:contrast}$$ Our frame is $$z_0=h(B_1\cup B_2,B_3\cup B_4),\qquad
 z_1=h(B_1,B_2),\qquad z_2=h(B_3,B_4).              \label{eq:frame}$$ The vector $z_0$ is exactly the TPC-256 midpoint vector.

> **Lemma: Exact orthonormality and variation**<span id="lem:frame" label="lem:frame">\[lem:frame\]</span> For all sufficiently large $x$, the three vectors in [\[eq:frame\]](main.tex#L99){reference-type="eqref" reference="eq:frame"} are source-only, exactly orthonormal, and, after zero extension outside $I_x$, satisfy $$\operatorname{TV}(z_i)=\frac{2}{\rho_i},
>  \qquad \rho_i^2=\frac{p_iq_i}{p_i+q_i},$$ where $(p_0,q_0)=(\ell,r)$, $(p_1,q_1)=(s_1,s_2)$, and $(p_2,q_2)=(s_3,s_4)$.

> **Proof** For a pair of sizes $p,q$, direct counting gives $$\|h(A,B)\|_2^2=\frac{pq}{p+q}\left(\frac1p+\frac1q\right)=1.$$ The sum of $z_1$ over $B_1\cup B_2$ is zero, whereas $z_0$ is constant there. Thus $\langle z_0,z_1\rangle=0$. The same argument on the right gives $\langle z_0,z_2\rangle=0$, and the last two vectors have disjoint support. This proves orthonormality, including all floor-rounding cases.
>
> For the zero extension of a contrast, the successive nonzero levels are $\rho_i/p_i$ and $-\rho_i/q_i$. The two outer jumps and the internal jump have total size $$\frac{\rho_i}{p_i}+\rho_i\left(\frac1{p_i}+\frac1{q_i}\right)
>        +\frac{\rho_i}{q_i}
>  =\frac{2}{\rho_i}.$$ The construction uses only ordered coordinates and the clock, so it is coefficient-independent by definition.

The scaled block limits are $$B_1=[1/2,5/8],\ B_2=[5/8,3/4],\quad
 B_3=[3/4,7/8],\ B_4=[7/8,1],$$ up to endpoint errors of size $O(1/x)$. In particular all three normalizations are comparable with $\sqrt{x}$.

# The literal coefficient and its three curvatures

Retain the V59 scales and literal coefficient $$H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400},
 \qquad \beta(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d\leq U}}\mu(d).             \label{eq:beta}$$ For an interval $J$ of length $s$, $$\#\{n\in J:d\mid n\}=s/d+\theta_{J,d},\qquad
 |\theta_{J,d}|\leq 1.$$ The leading $1/d$ term cancels for every divisor between the two children of each contrast. Consequently $$\left|\langle z_i,\sum_{d\mid\cdot,\ d\leq U}\mu(d)\rangle\right|
 \leq \frac{U}{\rho_i}=O(x^{-67/400}).                 \label{eq:divisor}$$ No Mertens cancellation is used.

Let $F(y)=\sum_{2\leq n\leq y}\Lambda(n)/\log n$. Prime-power decomposition and the source-locked de la Vallée Poussin theorem `\cite{davenport,montgomery-vaughan,ik,tpc233}` give $$F(y)=\operatorname{Li}(y)+O\left(y\exp(-c\sqrt{\log y})\right).     \label{eq:pnt}$$ For equal-width limiting intervals $A,B$, of width $d$, expanding $1/\log(xy)$ gives $$\operatorname{mean}_A(P)-\operatorname{mean}_B(P)
 =\frac{1}{d\log^2x}
   \left(\int_B\log y\,dy-\int_A\log y\,dy\right)
   +O(\log^{-3}x),                                    \label{eq:curvature}$$ where $P=\Lambda/\log$. The endpoint and PNT errors are absorbed in the remainder. The three elementary integrals are summarized in Table [1](main.tex#L186){reference-type="ref" reference="tab:curv"}.

<div id="tab:curv">

| vector |     limiting pair     |     mean curvature     | $\rho_i/\sqrt{x}$ |        $\kappa_i$       |
|:------:|:---------------------:|:----------------------:|:-----------------:|:-----------------------:|
|  $z_0$ |  $[1/2,3/4],[3/4,1]$  |     $2\log(32/27)$     |   $1/(2\sqrt2)$   |   $\log(32/27)/\sqrt2$  |
|  $z_1$ | $[1/2,5/8],[5/8,3/4]$ |   $2\log(3456/3125)$   |       $1/4$       |   $\log(3456/3125)/2$   |
|  $z_2$ |  $[3/4,7/8],[7/8,1]$  | $2\log(884736/823543)$ |       $1/4$       | $\log(884736/823543)/2$ |

: Second-order curvature constants.

</div>

All three logarithm arguments exceed one. Combining the table with [\[eq:divisor\]](main.tex#L162){reference-type="eqref" reference="eq:divisor"} proves $$\langle z_i,\beta\rangle=(\kappa_i+O(1/\log x))\frac{\sqrt{x}}{\log^2x}>0
 \quad (i=0,1,2)                                  \label{eq:betacontrasts}$$ for all sufficiently large real $x$.

# Adjoint normal form for bounded variation

Let $\mathcal Q_x=\{q\text{ prime}:Q<q\leq2Q\}$, and let $K_H(h)=\widehat{\psi_+}(h/H)$, with the fixed smooth compactly supported profile normalized by $\int\psi_+=1$. The literal operator is $$A_x(u,t)=\mathbf 1_{u\ne t}\sum_{q\in\mathcal Q_x}q\mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 K_H(u-t)\left(\mathbf 1_{u\equiv t\ (q)}-\frac1{q-1}\right). \label{eq:operator}$$ For $q\nmid t$, retain the combined row from the exact adjoint compiler `\cite{tpc255}`: $$v_{q,t}(u)=\mathbf 1_{q\nmid u}\left(\mathbf 1_{u\equiv t\ (q)}-\frac1{q-1}\right).$$ Its complete period is zero only after the two displayed pieces are recombined. The exact TPC-255 Poisson calculation, based on the V43 transference `\cite{v43}`, applies to every zero-extended piecewise-constant test function and yields $$\langle z,A_x\beta\rangle=-B_Q\langle z,\beta\rangle+R_{\rm unit}(z)+R_{\rm bdry}(z),
 \qquad B_Q=\sum_{q\in\mathcal Q_x}\frac{q(q-2)}{q-1}.             \label{eq:normalform}$$ The term $R_{\rm bdry}$ includes every outer endpoint and every internal jump of the zero extension. This is an exact algebraic extension of the one-jump identity; it does not discard a boundary.

The combined row obeys $$|v_{q,t}(t+h)|\leq\mathbf 1_{q\mid h}+\frac2q,\qquad
 \sum_h|hK_H(h)|\left(\mathbf 1_{q\mid h}+\frac2q\right)
 \ll_{\psi_+}\frac{H^2}{q}.                           \label{eq:firstmoment}$$ For a fixed displacement $h$, at most $|h|$ source points cross any one jump. Thus, for a fixed $\varepsilon>0$, $$|R_{\rm bdry}(z)|\ll_{\psi_+,\varepsilon}QH^2\operatorname{TV}(z)x^\varepsilon,
 \qquad |R_{\rm unit}(z)|\ll_\varepsilon x^{5/6+\varepsilon}             \label{eq:remainders}$$ for each of the three normalized contrasts. Since $\operatorname{TV}(z_i)=O(x^{-1/2})$, the first quantity is $O_{\psi_+,\varepsilon}(x^{55/48+\varepsilon})$.

> **Lemma: Diagonal scale**<span id="lem:bq" label="lem:bq">\[lem:bq\]</span> The weighted prime-shell input gives $$B_Q=\left(\frac92+o(1)\right)\frac{x^{2/3}}{\log x}.$$

> **Proof** Use $q(q-2)/(q-1)=q-1-1/(q-1)$ and the weighted prime number theorem recorded in the top-shell ledger `\cite{v59}`: $$\sum_{Q<q\leq2Q}q=\left(\frac32+o(1)\right)\frac{Q^2}{\log Q}.$$ The lower-order terms are absorbed, and $Q=x^{1/3}$ gives the claim.

# Inherited TPC-257 floor

> **Theorem: Three-mode adjoint asymptotics**<span id="thm:main" label="thm:main">\[thm:main\]</span> For each $i=0,1,2$, $$\boxed{\displaystyle
>  \langle z_i,A_x\beta\rangle
>  =-\left(\frac92\kappa_i+o(1)\right)
>    \frac{x^{7/6}}{\log^3x}}\qquad\text{in }\mathbb C.              \label{eq:scalar}$$

> **Proof** Insert [\[eq:betacontrasts\]](main.tex#L202){reference-type="eqref" reference="eq:betacontrasts"} and Lemma [\[lem:bq\]](main.tex#L247){reference-type="ref" reference="lem:bq"} into [\[eq:normalform\]](main.tex#L226){reference-type="eqref" reference="eq:normalform"}. The diagonal exponent is $2/3+1/2=7/6=56/48$. The boundary exponent from [\[eq:remainders\]](main.tex#L242){reference-type="eqref" reference="eq:remainders"} is $$1/3+2(21/32)-1/2=55/48,$$ and the input-unit exponent is $5/6$. Choose a fixed $0<\varepsilon<1/48$. All remainders are then lower order than the diagonal, and the asserted complex asymptotic follows. The proof uses only absolute remainder bounds after the exact combined-row cancellation; it assumes no reality or evenness of the kernel.

> **Corollary: Transverse and three-mode floors**<span id="cor:floors" label="cor:floors">\[cor:floors\]</span> Let $Z=\operatorname{span}\{z_0,z_1,z_2\}$ and $T=\operatorname{span}\{z_1,z_2\}$. Then $$\begin{aligned}
>  \|P_ZA_x\beta\|_2
>  &=\left(\frac92\sqrt{\kappa_0^2+\kappa_1^2+\kappa_2^2}+o(1)\right)
>    \frac{x^{7/6}}{\log^3x},                              \label{eq:zfloor}\\
>  \|P_TA_x\beta\|_2
>  &=\left(\frac92\sqrt{\kappa_1^2+\kappa_2^2}+o(1)\right)
>    \frac{x^{7/6}}{\log^3x}.                              \label{eq:tfloor}\end{aligned}$$ In particular, $T\subset z_0^\perp$, so the second line is a lower floor for $\|(I-z_0\otimes z_0)A_x\beta\|_2$.

> **Proof** Lemma [\[lem:frame\]](main.tex#L103){reference-type="ref" reference="lem:frame"} gives an orthonormal family. Therefore finite dimensional Parseval gives $$\|P_Zg\|_2^2=\sum_{i=0}^2|\langle z_i,g\rangle|^2,
>  \qquad \|P_Tg\|_2^2=\sum_{i=1}^2|\langle z_i,g\rangle|^2.$$ Apply this with $g=A_x\beta$ and use Theorem [\[thm:main\]](main.tex#L265){reference-type="ref" reference="thm:main"}. The constants are positive, so taking square roots is stable. The inclusion of $T$ in $z_0^\perp$ was proved exactly in Lemma [\[lem:frame\]](main.tex#L103){reference-type="ref" reference="lem:frame"}.

The factors before $9/2$ are approximately $$0.135096662713318\quad\text{and}\quad0.061792126717520,$$ respectively. These decimals are orientation data only; the logarithmic forms in the theorem are the actual constants.

# TPC-258 source-frozen null cancellation

Write $S_x=x^{7/6}/\log^3x$, and set $$L_1=\log(3456/3125),\qquad L_2=\log(884736/823543),\qquad
 L_T=(L_1^2+L_2^2)^{1/2},\qquad
 z_{\rm null}=(L_2z_1-L_1z_2)/L_T.$$ This direction is chosen before inspecting any coefficient or sample. The two inherited scalar formulas are $$\langle z_i,A_x\beta\rangle/S_x=-(9/2)\kappa_i+o(1),\qquad
 \kappa_1=L_1/2,\quad \kappa_2=L_2/2.$$ Consequently, $$\langle z_{\rm null},A_x\beta\rangle
 =\frac{L_2\langle z_1,A_x\beta\rangle-L_1\langle z_2,A_x\beta\rangle}{L_T},\qquad
 L_2\left(-\frac92\frac{L_1}{2}\right)
 -L_1\left(-\frac92\frac{L_2}{2}\right)=0.$$

> **Theorem: Source-frozen transverse diagonal cancellation**<span id="thm:null" label="thm:null">\[thm:null\]</span> For the unit vector $z_{\rm null}$, $$\boxed{\langle z_{\rm null},A_x\beta\rangle=o(S_x)}.$$ The statement is in $\mathbb C$ and retains the TPC-255 unit, diagonal, hard-window, and child-jump lanes.

> **Proof** The exact orthonormality of the TPC-257 frame makes $z_{\rm null}$ unit and orthogonal to $z_0$. Substitute the two scalar asymptotics into the displayed linear combination and use the exact cancellation. The fixed linear coefficients preserve the $o(S_x)$ remainder. The inherited boundary ratio is $$x^{55/48+\varepsilon}/S_x=x^{-1/48+\varepsilon}\log^3x\longrightarrow0
>  \quad(\varepsilon<1/48),$$ so no boundary term is silently removed.

> **Proposition: Conditional rate refinement**<span id="prop:nullrate" label="prop:nullrate">\[prop:nullrate\]</span> If the two scalar formulas have remainder $O_{\psi,\varepsilon}(S_x/\log x+x^{55/48+\varepsilon})$, then $$|\langle z_{\rm null},A_x\beta\rangle|
>  \ll_{\psi,\varepsilon}S_x/\log x+x^{55/48+\varepsilon}.$$ This is a <span class="upright">CONDITIONAL\_THEOREM</span>; it is not a fixed-power claim.

An error of size $1/\sqrt{\log x}$ is still $o(1)$, but it is larger than every fixed power $x^{-\delta}$. Thus the unconditional theorem does not pay the strict global $1/400$ endpoint. It also supplies no upper bound for the unprojected output, no signed $w$ coupling, and no arithmetic $L^2$ theorem.

# Reproducibility and epistemic labels

The companion certificate checks the finite rational identities, source hashes, curvature logarithm vectors, and exponent ledger. Its finite beta samples are marked `NUMERICAL_OBSERVATION`; they are not evidence for the PNT asymptotic. The status of this paper is $$\texttt{PROVED\_SOURCE\_BACKED\_TRANSVERSE\_DIAGONAL\_NULL\_CANCELLATION\_FOR\_LITERAL\_V59\_ADJOINT}.$$

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc253,
  author = {Liang Wang},
  title = {Source-Frozen Rank-Midpoint Contrast Compiler},
  note = {TPC-253 project in the accompanying repository}
}

@misc{tpc255,
  author = {Liang Wang},
  title = {Exact Adjoint Diagonal and Hard-Boundary Compiler},
  note = {TPC-255 project in the accompanying repository}
}

@misc{tpc256,
  author = {Liang Wang},
  title = {Literal Beta Haar and Diagonal-Dominant Adjoint Asymptotic},
  note = {TPC-256 project in the accompanying repository}
}

@misc{tpc257,
  author = {Liang Wang},
  title = {Four-Block Haar Lifts and a Transverse Norm Floor},
  note = {TPC-257 project in the accompanying repository}
}

@book{ik,
  author = {Henryk Iwaniec and Emmanuel Kowalski},
  title = {Analytic Number Theory},
  publisher = {American Mathematical Society},
  year = {2004}
}

@misc{v43,
  author = {Liang Wang},
  title = {Proper-Factor Poisson Transference},
  year = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V43}
}

@misc{v59,
  author = {Liang Wang},
  title = {Polarized Local {BDH} Scalar Compiler},
  year = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V59}
}

@misc{tpc233,
  author = {Liang Wang},
  title = {Critical-Depth Row-Mass Obstruction},
  year = {2026},
  howpublished = {Prime Dynamics Theory, TPC-233 source lock}
}

@book{davenport,
  author = {Harold Davenport},
  title = {Multiplicative Number Theory},
  edition = {3},
  publisher = {Springer},
  year = {2000}
}

@book{montgomery-vaughan,
  author = {Hugh L. Montgomery and Robert C. Vaughan},
  title = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  year = {2007}
}
```

<!-- SOURCE_BODY_END -->
