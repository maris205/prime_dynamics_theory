# Literal Beta Rank-Midpoint Asymptotics and Diagonal-Dominant Adjoint Phase

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

For the literal V59 coefficient on $(x/2,x]\cap\mathbb Z$, we evaluate its coefficient-independent ordered-rank midpoint Haar moment. Exact layer-by-layer divisor-density cancellation removes the truncated Möbius lane with error $O(x^{-67/400})$, while the second-order curvature of $\operatorname{Li}$ gives $$\langle z_{\mathrm{mid}},\beta\rangle
 =\frac{\log(32/27)}{\sqrt2}\frac{\sqrt{x}}{\log^2x}
  +O\!\left(\frac{\sqrt{x}}{\log^3x}\right)>0.$$ Substitution into the exact TPC-255 adjoint decomposition shows that the returned diagonal dominates the input-unit, hard-window, and child-jump lanes. The two boundary terms have exponent $55/48$, strictly below the diagonal exponent $56/48$ by $1/48$. Consequently the generally complex scalar $\langle z_{\mathrm{mid}},A_x\beta\rangle$ has an explicit negative-real leading asymptotic, is eventually nonzero, and has normalized phase tending to $-1$. We do not claim that the scalar is real, that its unqualified principal argument tends to $+\pi$, or that one Haar projection closes full Gate B.

<!-- SOURCE_BODY_BEGIN -->

# Literal clock and ordered-rank geometry

Let $x$ tend to infinity through real values and put $$a=\lfloor x/2\rfloor,\quad b=\lfloor x\rfloor,
 \quad I_x=\{a+1,\ldots,b\},\quad N=b-a.             \label{eq:clock}$$ The primary split is by ordered rank `\cite{tpc253}`: $$\ell=\lfloor N/2\rfloor,\quad r=N-\ell,\quad m=a+\ell,
 \quad L=\{a+1,\ldots,m\},\quad R=\{m+1,\ldots,b\}, \label{eq:rank}$$ $$\rho^2=\frac{\ell r}{N},\qquad
 z_{\mathrm{mid}}=\rho\left(\frac{\mathbf 1_L}{\ell}-\frac{\mathbf 1_R}{r}\right). \label{eq:haar}$$ The counting inner product is conjugate-linear in its first slot: $\langle f,g\rangle=\sum_{n\in I_x}\overline{f(n)}g(n)$. Thus $\|z_{\mathrm{mid}}\|_2=1$ and $$\langle z_{\mathrm{mid}},f\rangle=\rho\left(\frac1\ell\sum_{n\in L}f(n)
                 -\frac1r\sum_{n\in R}f(n)\right)              \label{eq:contrast}$$ for every real-valued $f$.

> **Lemma: Real-clock endpoints**<span id="lem:endpoints" label="lem:endpoints">\[lem:endpoints\]</span> Uniformly for real $x$, $$N=\frac x2+O(1),\quad \ell,r=\frac x4+O(1),\quad
>  m=\frac{3x}{4}+O(1),\quad
>  \rho=\frac{\sqrt{x}}{2\sqrt2}+O(x^{-1/2}).$$ Moreover $$\rho\left(\frac1\ell+\frac1r\right)=\frac1\rho,
>  \qquad |z_{\mathrm{mid}}(n)|\leq\rho^{-1}.                     \label{eq:rhoidentities}$$

> **Proof** The endpoint assertions follow directly from the floor errors in [\[eq:clock\]](main.tex#L59){reference-type="eqref" reference="eq:clock"} and the rank rounding in [\[eq:rank\]](main.tex#L64){reference-type="eqref" reference="eq:rank"}. Expanding $\rho^2=\ell r/N=x/8+O(1)$ proves the displayed asymptotic. Finally, $\rho(1/\ell+1/r)=\rho N/(\ell r)=1/\rho$. On $L$, for example, $(\rho/\ell)/(1/\rho)=r/N\leq1$; the $R$ case is symmetric.

Retain the literal V59 scales and coefficient `\cite{v35,v51}`: $$H=x^{21/32},\quad Q=x^{1/3},\quad U=x^{133/400},
 \quad \mathcal Q_x=\{q\text{ prime}:Q<q\leq2Q\},             \label{eq:scales}$$ $$\beta(t)=\frac{\Lambda(t)}{\log t}
       -\sum_{\substack{d\mid t\\d\leq U}}\mu(d),
 \qquad t\in I_x.                                   \label{eq:beta}$$

# The literal beta Haar asymptotic

Write $P(t)=\Lambda(t)/\log t$ and $D_U(t)=\sum_{d\mid t,\,d\leq U}\mu(d)$, so that $\beta=P-D_U$. The divisor lane requires no cancellation estimate for $\mu$.

> **Lemma: Exact layerwise density cancellation**<span id="lem:divisor" label="lem:divisor">\[lem:divisor\]</span> One has $$\left|\langle z_{\mathrm{mid}},D_U\rangle\right|
>  \leq \rho U\left(\frac1\ell+\frac1r\right)
>  =\frac{U}{\rho}=O(x^{-67/400}).                    \label{eq:divisorbound}$$

> **Proof** If $J$ is any interval of $s$ consecutive integers, then $\#\{n\in J:d\mid n\}=s/d+\theta_{J,d}$ with $|\theta_{J,d}|\leq1$. Inserting this separately on $L$ and $R$ into [\[eq:contrast\]](main.tex#L74){reference-type="eqref" reference="eq:contrast"}, the two $1/d$ densities cancel for every individual $d$ before any triangle inequality. Hence $$|\langle z_{\mathrm{mid}},D_U\rangle|
>  \leq\rho\sum_{d\leq U}|\mu(d)|
>        \left(\frac1\ell+\frac1r\right)
>  \leq \rho U\left(\frac1\ell+\frac1r\right).$$ Lemma [\[lem:endpoints\]](main.tex#L78){reference-type="ref" reference="lem:endpoints"} and $133/400-1/2=-67/400$ finish the proof.

For the prime-power lane define $$F(y)=\sum_{2\leq n\leq y}\frac{\Lambda(n)}{\log n}.$$ The classical de la Vallée Poussin prime number theorem `\cite{davenport,montgomery-vaughan,ik}`, source-locked for this program in `\cite{tpc233}`, states $$\pi(y)=\operatorname{Li}(y)+O\!\left(y e^{-c\sqrt{\log y}}\right).          \label{eq:pnt}$$ Since $$F(y)=\pi(y)+\sum_{k\geq2}\frac1k\pi(y^{1/k})
      =\pi(y)+O(\sqrt y\log y),$$ the prime-power tail is absorbed by a possibly smaller constant in [\[eq:pnt\]](main.tex#L149){reference-type="eqref" reference="eq:pnt"}: $$F(y)=\operatorname{Li}(y)+O\!\left(y e^{-c_1\sqrt{\log y}}\right).          \label{eq:F}$$

> **Lemma: Second-order $\operatorname{Li}$ curvature**<span id="lem:li" label="lem:li">\[lem:li\]</span> The ordered children satisfy $$\frac{F(m)-F(a)}{\ell}-\frac{F(b)-F(m)}r
>  =\frac{2\log(32/27)}{\log^2x}+O\!\left(\frac1{\log^3x}\right). \label{eq:curvature}$$

> **Proof** The error in [\[eq:F\]](main.tex#L159){reference-type="eqref" reference="eq:F"}, divided by a child length comparable to $x$, is $O(e^{-c_2\sqrt{\log x}})$. Replacing the integer endpoints by $x/2,3x/4,x$ changes each normalized $\operatorname{Li}$ difference by $O(1/(x\log x))$. Uniformly for $y\in[1/2,1]$, $$\frac1{\log(xy)}=\frac1{\log x}-\frac{\log y}{\log^2x}
>                   +O\!\left(\frac1{\log^3x}\right).$$ Both children have scaled length $1/4$, so their $1/\log x$ terms cancel. The coefficient of $1/\log^2x$ in the lower-minus-upper difference is $$\begin{aligned}
>  4\left(\int_{3/4}^{1}\log y\,dy
>        -\int_{1/2}^{3/4}\log y\,dy\right)
>  &=2\log\frac{32}{27}.\end{aligned}$$ The endpoint, normalization, and PNT errors are all absorbed in the stated remainder.

> **Theorem: Literal beta rank-midpoint asymptotic**<span id="thm:beta" label="thm:beta">\[thm:beta\]</span> For all sufficiently large real $x$, $$\boxed{\displaystyle
>  \langle z_{\mathrm{mid}},\beta\rangle
>  =\frac{\log(32/27)}{\sqrt2}\frac{\sqrt{x}}{\log^2x}
>   +O\!\left(\frac{\sqrt{x}}{\log^3x}\right)>0.}      \label{eq:betamain}$$

> **Proof** Multiply [\[eq:curvature\]](main.tex#L166){reference-type="eqref" reference="eq:curvature"} by $\rho=\sqrt{x}/(2\sqrt2)+O(x^{-1/2})$ and subtract the divisor contribution from Lemma [\[lem:divisor\]](main.tex#L117){reference-type="ref" reference="lem:divisor"}. Since $x^{-67/400}=o(\sqrt{x}/\log^3x)$, this gives [\[eq:betamain\]](main.tex#L196){reference-type="eqref" reference="eq:betamain"}. Its main constant is positive.

# Exact adjoint lanes and their estimates

Fix a smooth profile $\psi_+$ supported in $[-1,1]$, normalized by $\int\psi_+=1$, and set $K_H(h)=\widehat\psi_+(h/H)$. No reality or evenness is assumed. The literal operator is `\cite{v59,tpc255}` $$A_x(u,t)=\mathbf 1_{u\ne t}\sum_{q\in\mathcal Q_x}q\mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 K_H(u-t)\left(\mathbf 1_{u\equiv t\,(q)}-\frac1{q-1}\right).      \label{eq:operator}$$ For $q\nmid t$ define the complete combined unit row $$v_{q,t}(u)=\mathbf 1_{q\nmid u}
 \left(\mathbf 1_{u\equiv t\,(q)}-\frac1{q-1}\right).             \label{eq:unitrow}$$ It is centered over a complete period. The TPC-255 adjoint compiler, using the band-limited complete-lattice Poisson zero from V43 `\cite{v43,tpc255}`, gives for all sufficiently large $x$ (hence $H>2Q$) $$S_x:=\langle z_{\mathrm{mid}},A_x\beta\rangle
 =-B_Q\langle z_{\mathrm{mid}},\beta\rangle+R_{\rm unit}+R_{\rm hard}+R_{\rm jump}, \label{eq:decomp}$$ where $$\begin{aligned}
 B_Q&=\sum_{q\in\mathcal Q_x}\frac{q(q-2)}{q-1},                       \label{eq:BQ}\\
 R_{\rm unit}&=\sum_{q\in\mathcal Q_x}\frac{q(q-2)}{q-1}
       \sum_{\substack{t\in I_x\\q\mid t}}z_{\mathrm{mid}}(t)\beta(t), \label{eq:Runit}\\
 R_{\rm hard}&=-\sum_{q\in\mathcal Q_x}q
       \sum_{\substack{t\in I_x\\q\nmid t}}\beta(t)z_{\mathrm{mid}}(t)
       \sum_{u\notin I_x}K_H(u-t)v_{q,t}(u),                  \label{eq:Rhard}\\
 R_{\rm jump}&=\sum_{q\in\mathcal Q_x}q
       \sum_{\substack{t\in I_x\\q\nmid t}}\beta(t)
       \sum_{u\in I_x}K_H(u-t)v_{q,t}(u)(z_{\mathrm{mid}}(u)-z_{\mathrm{mid}}(t)).     \label{eq:Rjump}\end{aligned}$$ The adjoint identity behind [\[eq:decomp\]](main.tex#L227){reference-type="eqref" reference="eq:decomp"} is $\langle z_{\mathrm{mid}},A_x\beta\rangle=\langle A_x^*z_{\mathrm{mid}},\beta\rangle$ because the first slot is conjugate-linear. Conjugating $A_x^*z_{\mathrm{mid}}$ restores $K_H$ in [\[eq:Rhard\]](main.tex#L236){reference-type="eqref" reference="eq:Rhard"}–[\[eq:Rjump\]](main.tex#L239){reference-type="eqref" reference="eq:Rjump"}; no self-adjointness is used.

> **Lemma: Weighted diagonal coefficient**<span id="lem:BQ" label="lem:BQ">\[lem:BQ\]</span> $$B_Q=\left(\frac92+o(1)\right)\frac{x^{2/3}}{\log x}.          \label{eq:BQasymp}$$

> **Proof** The exact identity $q(q-2)/(q-1)=q-1-1/(q-1)$ and weighted PNT give $$B_Q=\sum_{Q<q\leq2Q}q+o(Q^2/\log Q)
>     =\left(\frac32+o(1)\right)\frac{Q^2}{\log Q}.$$ This frozen weighted-prime input is also recorded in `\cite{vtop}`. Since $Q=x^{1/3}$, [\[eq:BQasymp\]](main.tex#L248){reference-type="eqref" reference="eq:BQasymp"} follows.

> **Lemma: Combined unit-mask first moment**<span id="lem:firstmoment" label="lem:firstmoment">\[lem:firstmoment\]</span> For $q\in\mathcal Q_x$, $q\nmid t$, and $h\in\mathbb Z$, $$|v_{q,t}(t+h)|\leq\mathbf 1_{q\mid h}+\frac2q.                    \label{eq:maskbound}$$ Moreover, uniformly for $q\leq2Q<H$, $$\sum_{h\in\mathbb Z}|hK_H(h)|\left(\mathbf 1_{q\mid h}+\frac2q\right)
>  \ll_{\psi}\frac{H^2}{q}.                                  \label{eq:firstmoment}$$

> **Proof** If $q\mid(t+h)$, the left side of [\[eq:maskbound\]](main.tex#L265){reference-type="eqref" reference="eq:maskbound"} is zero. Otherwise, if $q\mid h$ it is $(q-2)/(q-1)\leq1$, and if $q\nmid h$ it is $1/(q-1)\leq2/q$. This proves the pointwise bound while retaining the full output-unit mask.
>
> For any fixed $A>3$, Schwartz decay gives $|K_H(h)|\ll_{A,\psi}(1+|h|/H)^{-A}$. Therefore $$\sum_{q\mid h}|hK_H(h)|
>  =q\sum_{k\in\mathbb Z}|kK_H(qk)|\ll_\psi H^2/q,$$ because $H/q>1$; also $q^{-1}\sum_h|hK_H(h)|\ll_\psi H^2/q$. Combining the two estimates proves [\[eq:firstmoment\]](main.tex#L270){reference-type="eqref" reference="eq:firstmoment"}. This is the same source-backed centered first-moment mechanism as in `\cite{v43}`.

> **Proposition: Boundary power separation**<span id="prop:remainders" label="prop:remainders">\[prop:remainders\]</span> For every fixed $\varepsilon>0$, $$\begin{aligned}
>  R_{\rm unit}&=O_\varepsilon(x^{5/6+\varepsilon}),                              \label{eq:unitbound}\\
>  R_{\rm hard},R_{\rm jump}&=O_{\psi,\varepsilon}(x^{55/48+\varepsilon}).      \label{eq:boundarybound}\end{aligned}$$

> **Proof** The divisor bound gives $|\beta(t)|\leq1+\tau(t)\ll_\varepsilon x^\varepsilon$ on $I_x$. Using $|z_{\mathrm{mid}}(t)|\leq\rho^{-1}$ and at most $x/q+1$ multiples of $q$, $$|R_{\rm unit}|\ll\frac{x^\varepsilon}{\rho}
>    \sum_{q\in\mathcal Q_x}q\left(\frac{x}{q}+1\right)
>  \ll \frac{x^{1+\varepsilon}Q}{\rho}=O(x^{5/6+\varepsilon}).$$
>
> For each fixed displacement $h$, at most $|h|$ values of $t\in I_x$ have $t+h\notin I_x$. Apply [\[eq:maskbound\]](main.tex#L265){reference-type="eqref" reference="eq:maskbound"} and [\[eq:firstmoment\]](main.tex#L270){reference-type="eqref" reference="eq:firstmoment"} directly to the combined row, without splitting its zero modes. This gives $$|R_{\rm hard}|\ll_{\psi,\varepsilon}
>  \frac{x^\varepsilon}{\rho}\sum_{q\in\mathcal Q_x}q\frac{H^2}{q}
>  \ll_{\psi,\varepsilon}\frac{QH^2}{\rho}x^\varepsilon.$$ For $R_{\rm jump}$, the difference $z_{\mathrm{mid}}(u)-z_{\mathrm{mid}}(t)$ vanishes inside either child and has absolute value $1/\rho$ across the midpoint by [\[eq:rhoidentities\]](main.tex#L88){reference-type="eqref" reference="eq:rhoidentities"}. At a fixed $h$, the number of pairs crossing that single boundary is again at most $|h|$. The identical first-moment estimate therefore applies. Finally $$\frac{QH^2}{\rho}
>  =x^{,1/3+2(21/32)-1/2+o(1)}=x^{55/48+o(1)},$$ which proves [\[eq:boundarybound\]](main.tex#L296){reference-type="eqref" reference="eq:boundarybound"} after absorbing the harmless divisor envelope into $x^\varepsilon$.

The combined row in [\[eq:unitrow\]](main.tex#L220){reference-type="eqref" reference="eq:unitrow"} is essential. If it is written as $$c_{q,t}(u)=\mathbf 1_{u\equiv t\,(q)}-\frac1{q-1},\qquad
 d_q(u)=\frac{\mathbf 1_{q\mid u}}{q-1},$$ then $v_{q,t}=c_{q,t}+d_q$, but their period sums are respectively $-1/(q-1)$ and $+1/(q-1)$. Only the sum is centered. Thus applying Poisson to either piece separately is refuted; Proposition [\[prop:remainders\]](main.tex#L292){reference-type="ref" reference="prop:remainders"} uses the combined mask throughout.

> **Theorem: Diagonal-dominant adjoint phase**<span id="thm:adjoint" label="thm:adjoint">\[thm:adjoint\]</span> As real $x\to\infty$, $$\boxed{\displaystyle
>  \langle z_{\mathrm{mid}},A_x\beta\rangle
>  =-\left(\frac{9\log(32/27)}{2\sqrt2}+o(1)\right)
>        \frac{x^{7/6}}{\log^3x}}\qquad\text{in }\mathbb C.     \label{eq:adjointmain}$$ Consequently, for all sufficiently large $x$, $$\Re\langle z_{\mathrm{mid}},A_x\beta\rangle<0,\qquad \langle z_{\mathrm{mid}},A_x\beta\rangle\ne0,
>  \qquad
>  \frac{\langle z_{\mathrm{mid}},A_x\beta\rangle}{|\langle z_{\mathrm{mid}},A_x\beta\rangle|}\longrightarrow-1. \label{eq:phase}$$

> **Proof** Combine Theorem [\[thm:beta\]](main.tex#L190){reference-type="ref" reference="thm:beta"}, Lemma [\[lem:BQ\]](main.tex#L246){reference-type="ref" reference="lem:BQ"}, and the exact identity [\[eq:decomp\]](main.tex#L227){reference-type="eqref" reference="eq:decomp"}. The diagonal has exponent $2/3+1/2=7/6=56/48$. Choose any fixed $0<\varepsilon<1/48$ in Proposition [\[prop:remainders\]](main.tex#L292){reference-type="ref" reference="prop:remainders"}; the boundary exponent is $55/48+\varepsilon$, so the gap is $$\frac{56}{48}-\frac{55}{48}=\frac1{48},$$ and even the factor $\log^3x$ is absorbed by this fixed power. The input-unit term is smaller still. This proves [\[eq:adjointmain\]](main.tex#L347){reference-type="eqref" reference="eq:adjointmain"} as a complex asymptotic. Division by its positive real scale gives a strictly negative real limit, which implies all three statements in [\[eq:phase\]](main.tex#L353){reference-type="eqref" reference="eq:phase"}.

> **Remark: Phase firewall** The remainder in [\[eq:adjointmain\]](main.tex#L347){reference-type="eqref" reference="eq:adjointmain"} may be nonreal because $K_H$ need not be real or even. The theorem does not say that the scalar itself is real. It also does not force the unqualified principal argument to approach $+\pi$: approach from opposite half-planes may select opposite endpoints of the principal branch. The invariant statement is the normalized phase in [\[eq:phase\]](main.tex#L353){reference-type="eqref" reference="eq:phase"}, equivalently convergence to $\pi$ modulo $2\pi$.

# Validation, status, and remaining gate

The executable artifact verifies source hashes at the frozen TPC-255 release, 64 exact rank clocks, 1,536 divisor layers, 8,814 full unit-mask terms, and both boundary-counting rules. An independent implementation imports no producer code and rejects 112 deterministic semantic mutations in 14 classes. A separate suite checks 192 exact families, evenly split between integer and noninteger clocks. The finite values $$0.126722052900396\quad(x=10^5),\qquad
 0.119396549784227\quad(x=10^6)$$ are scaled beta-Haar *numerical observations*; they receive no proof credit. The proved target constant is $\log(32/27)/\sqrt2=0.120136761035088\ldots$.

The exact route classification is a scoped arithmetic advance:

| Marker | Value |
|:-------|:------|
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |
|        |       |

#### Strongest result and obstruction.

The literal $\beta$ midpoint moment has an explicit positive asymptotic, and the deleted-diagonal $B_Q$ return forces an explicit negative-real leading asymptotic for the literal adjoint Haar scalar. The corresponding obstruction is structural: the Poisson zero does not make this lane small; diagonal deletion returns the asymptotically dominant term. Moreover, the two output-unit pieces cannot be separated before exact recentering.

#### Open theorem and reusable structure.

One ordered-rank Haar projection does not control the transverse/full-output component of $A_x\beta$, couple it to the physical $w$ lane, prove an $L^2$ estimate, or pay full Gate B. The reusable chain is $$\begin{aligned}
 &\text{layerwise divisor density cancellation}
 \longrightarrow \text{second-order PNT curvature}\\
 &\qquad\longrightarrow \text{literal beta Haar main term}
 \longrightarrow B_Q\text{ amplification}\\
 &\qquad\longrightarrow \text{first-moment boundary separation}.\end{aligned}$$ The retained next clue is

.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{davenport,
  author    = {Davenport, Harold},
  title     = {Multiplicative Number Theory},
  edition   = {Third},
  publisher = {Springer},
  year      = {2000}
}

@book{montgomery-vaughan,
  author    = {Montgomery, Hugh L. and Vaughan, Robert C.},
  title     = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  year      = {2007}
}

@book{ik,
  author    = {Iwaniec, Henryk and Kowalski, Emmanuel},
  title     = {Analytic Number Theory},
  publisher = {American Mathematical Society},
  year      = {2004}
}

@misc{v35,
  author       = {Wang, Liang},
  title        = {Proper Factors and the Coprime Fixed-Shift Ratio Core},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V35}
}

@misc{v43,
  author       = {Wang, Liang},
  title        = {Proper-Factor Poisson Transference},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V43}
}

@misc{v51,
  author       = {Wang, Liang},
  title        = {Compensated Pair Dilation and Angular Dispersion},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V51}
}

@misc{v59,
  author       = {Wang, Liang},
  title        = {Polarized Local {BDH} Scalar Compiler},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V59}
}

@misc{vtop,
  author       = {Wang, Liang},
  title        = {Top-Prime Direct Energy Floor},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B internal report}
}

@misc{tpc233,
  author       = {Wang, Liang},
  title        = {Critical-Depth Row-Mass Obstruction},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, TPC-233 source lock}
}

@misc{tpc253,
  author       = {Wang, Liang},
  title        = {Source-Frozen Rank-Midpoint Contrasts for the Literal {V59} Scalar},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, TPC-253}
}

@misc{tpc255,
  author       = {Wang, Liang},
  title        = {Exact Adjoint Diagonal Return and Hard-Boundary Decomposition for the Literal {V59} Haar Lane},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, TPC-255}
}
```

<!-- SOURCE_BODY_END -->
