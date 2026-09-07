# Exact Adjoint Diagonal Return and Hard-Boundary Decomposition\ for the Literal V59 Haar Lane

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Electronic Information and Communications, Huazhong University of Science and Technology (HUST),; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`
- Converter: `source-markdown-audit-v2`

## Abstract

We push a coefficient-independent ordered-rank Haar vector through the adjoint of the literal V59 prime-shell operator. A complete-lattice unit-centered row vanishes exactly by the previously frozen band-limited Poisson theorem once $H>2Q$. This does not annihilate the physical row: deleting its diagonal returns a $B_Q$-weighted midpoint moment of the literal coefficient $\beta$, while truncation to $(x/2,x]\cap\mathbb Z$ and the jump between the two rank children create two explicit boundary lanes. We retain the input and output unit masks and show that the output correction is jointly centered only. The result is an exact normal form for $\langle z_{\rm mid},A_x\beta\rangle$, not an estimate. In particular, no sign, nonzero value, power saving, $L^2$ theorem, or twin-prime conclusion is asserted. Exact Gaussian-rational fixtures and 192 stress families reproduce the finite algebra but are not asymptotic evidence.

<!-- SOURCE_BODY_BEGIN -->

# Frozen operator and ordered-rank test

Retain the literal V59 scales and coefficient $$I_x=(x/2,x]\cap\mathbb Z,\quad H=x^{21/32},\quad Q=x^{1/3},\quad
 \mathcal Q_x=\{q\text{ prime}:Q<q\leq2Q\},                    \label{eq:scales}$$ $$K_H(h)=\widehat\psi_+(h/H),\qquad
 \beta(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d),       \label{eq:beta}$$ where $\operatorname{supp}\psi_+\subset[-1,1]$ and $K_H(0)=\int\psi_+=1$. For $u,t\in I_x$, the source-frozen operator is $$A_x(u,t)=\mathbf 1_{u\ne t}\sum_{q\in\mathcal Q_x}q\mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}
 K_H(u-t)\left(\mathbf 1_{u\equiv t\,(q)}-\frac1{q-1}\right).        \label{eq:operator}$$ This orientation and the associated scalar are fixed in TPC-247 `\cite{tpc247}`; the physical V59 source is `\cite{v59}`.

Write $I_x=\{n_1<\cdots<n_N\}$, assume $N\geq2$, and put $$\ell=\lfloor N/2\rfloor,\quad r=N-\ell,
 \quad L=\{n_1,\ldots,n_\ell\},\quad R=I_x\setminus L,           \label{eq:rank}$$ $$\rho^2=\frac{\ell r}{N},\qquad
 z_{\rm mid}=\rho\left(\frac{\mathbf 1_L}{\ell}-\frac{\mathbf 1_R}{r}\right).  \label{eq:haar}$$ The split is by ordered rank for every real $x$. The integer-only $\lfloor3x/4\rfloor$ crosswalk is not used at nonintegral clocks `\cite{tpc253}`.

# Complete row and exact adjoint decomposition

For $q\in\mathcal Q_x$ and $q\nmid t$, define the complete periodic unit row $$v_{q,t}(u)=\mathbf 1_{q\nmid u}
 \left(\mathbf 1_{u\equiv t\,(q)}-\frac1{q-1}\right),\qquad u\in\mathbb Z. \label{eq:v}$$ Its mean over a period is zero. Introduce the adjoint-oriented quantities $$\begin{aligned}
 P^*_{q,t}&=\sum_{u\in\mathbb Z}\overline{K_H(u-t)}v_{q,t}(u),          \label{eq:p}\\
 E^*_{q,t}&=\sum_{u\notin I_x}\overline{K_H(u-t)}v_{q,t}(u),    \label{eq:e}\\
 J^*_{q,t}&=\sum_{u\in I_x}\overline{K_H(u-t)}v_{q,t}(u)
                   (z_{\rm mid}(u)-z_{\rm mid}(t)).                             \label{eq:j}\end{aligned}$$ Absolute convergence follows from the Schwartz decay of $K_H$.

> **Theorem: Adjoint diagonal–boundary compiler**<span id="thm:compiler" label="thm:compiler">\[thm:compiler\]</span> For every real $x$ with $N\geq2$, $$\begin{aligned}
>  (A_x^*z_{\rm mid})(t)=\sum_{q\in\mathcal Q_x}q\mathbf 1_{q\nmid t}
>  \bigg[&z_{\rm mid}(t)P^*_{q,t}-z_{\rm mid}(t)E^*_{q,t}+J^*_{q,t} \notag\\
>  &-\frac{q-2}{q-1}\overline{K_H(0)}z_{\rm mid}(t)\bigg].               \label{eq:full}\end{aligned}$$ If $H>2Q$, the source-backed complete-lattice theorem gives $P^*_{q,t}=0$, and hence $$(A_x^*z_{\rm mid})(t)=\sum_{q\in\mathcal Q_x}q\mathbf 1_{q\nmid t}
>  \left[-z_{\rm mid}(t)E^*_{q,t}+J^*_{q,t}-\frac{q-2}{q-1}z_{\rm mid}(t)\right].\label{eq:reduced}$$ Moreover, $$J^*_{q,t}=\begin{cases}
>  -\rho^{-1}\displaystyle\sum_{u\in R}\overline{K_H(u-t)}v_{q,t}(u),&t\in L,\\[2mm]
>  +\rho^{-1}\displaystyle\sum_{u\in L}\overline{K_H(u-t)}v_{q,t}(u),&t\in R.
>  \end{cases}                                                     \label{eq:jump}$$

> **Proof** Fix $q\nmid t$ and abbreviate $F(u)=\overline{K_H(u-t)}v_{q,t}(u)$. Adding and subtracting $z_{\rm mid}(t)$ gives $$z_{\rm mid}(t)P^*_{q,t}-z_{\rm mid}(t)E^*_{q,t}+J^*_{q,t}
>  =\sum_{u\in I_x}F(u)z_{\rm mid}(u).$$ The operator deletes $u=t$, where $v_{q,t}(t)=(q-2)/(q-1)$. Multiplication by the outer $q$ and summation prove [\[eq:full\]](main.tex#L99){reference-type="eqref" reference="eq:full"}.
>
> For the Poisson attachment, use the reflected-conjugate profile $\phi(v)=\overline{\psi_+(-v)}$. Reflection and conjugation preserve support in $[-1,1]$, and its physical kernel is $\overline{K_H(-h)}$. Thus the V43 complete-lattice theorem `\cite{v43}` applies in the adjoint direction without assuming that $K_H$ is even or real. When $q\leq2Q<H$, every nonzero dual frequency lies outside the profile support, so $P^*_{q,t}=0$. Finally, $$z_{\rm mid}|_L-z_{\rm mid}|_R=\rho\left(\frac1\ell+\frac1r\right)=\rho^{-1},$$ and only the opposite child survives in [\[eq:j\]](main.tex#L90){reference-type="eqref" reference="eq:j"}, proving [\[eq:jump\]](main.tex#L112){reference-type="eqref" reference="eq:jump"}.

# The literal beta pairing and the returned shell coefficient

The counting inner product is conjugate-linear in its first slot. Since $\beta$ and $z_{\rm mid}$ are real, $$\langle z_{\rm mid},A_x\beta\rangle=\langle A_x^*z_{\rm mid},\beta\rangle.                       \label{eq:adjoint}$$ Let $E_{q,t}$ and $J_{q,t}$ denote the conjugates of the starred quantities in [\[eq:e\]](main.tex#L88){reference-type="eqref" reference="eq:e"}–[\[eq:j\]](main.tex#L90){reference-type="eqref" reference="eq:j"}. Under $H>2Q$, Theorem [\[thm:compiler\]](main.tex#L94){reference-type="ref" reference="thm:compiler"} yields $$\begin{aligned}
 \langle z_{\rm mid},A_x\beta\rangle={}&D_{\beta,z_{\rm mid}}
 -\sum_{q\in\mathcal Q_x}q\sum_{\substack{t\in I_x\\q\nmid t}}
       \beta(t)z_{\rm mid}(t)E_{q,t} \notag\\
 &+\sum_{q\in\mathcal Q_x}q\sum_{\substack{t\in I_x\\q\nmid t}}
       \beta(t)J_{q,t},                                         \label{eq:scalar}\end{aligned}$$ where $$D_{\beta,z_{\rm mid}}=-\sum_{q\in\mathcal Q_x}\frac{q(q-2)}{q-1}
 \sum_{\substack{t\in I_x\\q\nmid t}}z_{\rm mid}(t)\beta(t).         \label{eq:d}$$ Put $$B_Q=\sum_{q\in\mathcal Q_x}\frac{q(q-2)}{q-1}.$$ Restoring the omitted input multiples gives the exact identity $$D_{\beta,z_{\rm mid}}=-B_Q\langle z_{\rm mid},\beta\rangle
 +\sum_{q\in\mathcal Q_x}\frac{q(q-2)}{q-1}
   \sum_{\substack{t\in I_x\\q\mid t}}z_{\rm mid}(t)\beta(t).         \label{eq:bq}$$ The coefficient is the same deleted-diagonal shell coefficient isolated in V43. Equations [\[eq:scalar\]](main.tex#L154){reference-type="eqref" reference="eq:scalar"}–[\[eq:bq\]](main.tex#L169){reference-type="eqref" reference="eq:bq"} are an exact arithmetic normal form, not an estimate.

# Unit-mask and normalization firewalls

For $q\nmid t$, write $$c_{q,t}(u)=\mathbf 1_{u\equiv t\,(q)}-\frac1{q-1},\qquad
 d_q(u)=\frac{\mathbf 1_{q\mid u}}{q-1}.                              \label{eq:cd}$$ Then $v_{q,t}=c_{q,t}+d_q$, but over one period $$\sum_{u\bmod q}c_{q,t}(u)=-\frac1{q-1},\qquad
 \sum_{u\bmod q}d_q(u)=+\frac1{q-1}.                            \label{eq:modes}$$ Only their sum is centered. Their complete-lattice zero-frequency terms are $-H\psi_+(0)/(q(q-1))$ and $+H\psi_+(0)/(q(q-1))$; applying centered Poisson after discarding either term is invalid. This residue-class normalization is distinct from the deleted-diagonal value $K_H(0)=\widehat\psi_+(0)=\int\psi_+=1$. If $q\mid t$, the input mask in [\[eq:operator\]](main.tex#L60){reference-type="eqref" reference="eq:operator"} makes the entire $q$ summand zero, and no centered row is constructed.

# Finite validation and adversarial controls

The executable certificate is deliberately finite and exact. Its primary fixture uses the literal clock $x=64$, so $I_x=\{33,\ldots,64\}$, $\ell=r=16$, $\rho^2=8$, and $\mathcal Q_x=\{5,7\}$. To avoid introducing an irrational representation of $\rho$, the executable checks the rational step $h=z_{\rm mid}/\rho$; linearity then gives the identical formula for $z_{\rm mid}$. It uses the literal $\beta$, together with a nonreal, noneven Gaussian-rational kernel supported on the nineteen differences $-9,\ldots,9$ and normalized by $K(0)=1$. The producer computes $A_x^*h$ directly and reassembles all 32 coordinates from the four terms in [\[eq:full\]](main.tex#L99){reference-type="eqref" reference="eq:full"}. It also checks $$\langle h,A_x\beta\rangle=\langle A_x^*h,\beta\rangle$$ and the two equivalent forms of the deleted-diagonal lane. Thus a missing conjugate, outer $q$, mask, diagonal sign, or $q-2$ coefficient is visible in exact arithmetic.

The independent checker imports no producer code. It reconstructs the certificate independently, verifies eight frozen source hashes and strict integer types at nested fields, and rejects 100 adversarial mutations in 14 named classes. The separate stress program checks 192 deterministic exact families, split evenly between integer and noninteger clocks. Its coverage ledger contains 8448 coordinate decompositions, 9690 left-child and 9944 right-child jump checks, 5710 input-mask rows, and 206110 output-mask terms; all 192 kernels are nonreal and noneven. Normal and optimized Python executions have byte-identical output and empty standard error.

These computations do not approximate $\psi_+$, take a large-$x$ limit, or test prime cancellation. The complete-row zero in Theorem [\[thm:compiler\]](main.tex#L94){reference-type="ref" reference="thm:compiler"} is supported by the frozen Poisson theorem, not inferred from the finite fixture. Conversely, the fixture retains a generally nonzero $P^*_{q,t}$ in [\[eq:full\]](main.tex#L99){reference-type="eqref" reference="eq:full"}, so the algebraic decomposition is tested before the source-backed zero is substituted. A separate complete-period row checks [\[eq:modes\]](main.tex#L185){reference-type="eqref" reference="eq:modes"} and rejects dropping the output-unit correction.

# Route status

TPC-255 proves exact literal structure. It supplies no estimate for $\langle z_{\rm mid},\beta\rangle$, the input-unit correction, or the two boundary lanes. Triangulating these pieces prime by prime would remove precisely the signed reassembly one must eventually exploit. Accordingly $$\texttt{ROUTE\_ADVANCE=YES\_EXACT\_LITERAL\_STRUCTURE},$$ $$\texttt{LITERAL\_ARITHMETIC\_STRUCTURE\_ADVANCE=YES},\qquad
 \texttt{ARITHMETIC\_ADVANCE=NO}.$$ The strict $1/400$ budget is unpaid and no twin-prime statement follows. The next admissible theorem must estimate the same signed object in [\[eq:scalar\]](main.tex#L154){reference-type="eqref" reference="eq:scalar"}–[\[eq:bq\]](main.tex#L169){reference-type="eqref" reference="eq:bq"}, with both masks and all three surviving lanes retained.

#### Strongest result and obstruction.

The complete-lattice centered alias has been removed from the literal adjoint Haar form without an evenness or self-adjointness assumption. What remains is an exact three-lane object: the $B_Q$-weighted local return, the outer hard-window leakage, and the internal child-jump leakage, together with the input-unit correction already contained in the first lane. This is the strongest positive conclusion. The matching obstruction is equally exact: Poisson cancellation acts before diagonal deletion and therefore cannot pay the returned $B_Q$ term. No frozen theorem controls that term collectively with both boundary lanes on the V59 clock.

#### Reusable compiler and open theorem.

The reusable sequence is $$\text{literal adjoint test}
 \longrightarrow \text{unit-centered complete lattice}
 \longrightarrow \text{Poisson zero}
 \longrightarrow \text{diagonal and boundary return}.$$ The open theorem is a signed estimate for [\[eq:scalar\]](main.tex#L154){reference-type="eqref" reference="eq:scalar"} after the substitution [\[eq:bq\]](main.tex#L169){reference-type="eqref" reference="eq:bq"}, preserving the whole prime shell, both unit masks, and both physical boundaries. Separate absolute estimates for the displayed pieces would not establish that theorem. Thus TPC-255 identifies the next arithmetic target exactly while leaving $L^2$, fixed-atom credit, full Gate B, and the twin-prime problem open.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{v59,
  author       = {Wang, Liang},
  title        = {Polarized Local {BDH} Scalar Compiler},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V59}
}
@misc{v43,
  author       = {Wang, Liang},
  title        = {Proper-Factor Poisson Transference},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, Bridge B V43}
}

@misc{tpc247,
  author       = {Wang, Liang},
  title        = {Literal {V59} Source-Operator Attachment},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, TPC-247}
}

@misc{tpc253,
  author       = {Wang, Liang},
  title        = {Source-Frozen Rank-Midpoint Contrasts for the Literal {V59} Scalar},
  year         = {2026},
  howpublished = {Prime Dynamics Theory, TPC-253}
}
```

<!-- SOURCE_BODY_END -->
