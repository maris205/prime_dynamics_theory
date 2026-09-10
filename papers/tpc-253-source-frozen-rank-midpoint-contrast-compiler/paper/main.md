# Source-Frozen Rank-Midpoint Contrasts for the Literal V59 Scalar

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Electronic Information and Communications, Huazhong University of Science and Technology (HUST),; Wuhan, China
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We freeze a nontrivial two-block direction from the ordered physical interval of the literal V59 scalar before inspecting any coefficient, margin, or sign. The first $\lfloor N/2\rfloor$ coordinates and the remaining coordinates define a normalized Haar contrast $z$. Its rank-one projector admits the exact rational representation $\rho^2h_i h_j$, even when $\rho$ is irrational. We derive exact partial-sum formulas for both coarse and midpoint longitudinal terms. Their difference is $\overline{\langle z,w\rangle}\langle z,A_x\beta\rangle$, with the first-slot conjugation explicit, and the transverse covariance changes by its negative; the remainder is the sum of the two within-child covariances. For integral $x$, the rank split is exactly the threshold $\lfloor3x/4\rfloor$. Substitution of the literal TPC-247 kernel retains its prime weight, two unit masks, deleted diagonal, orientation, physical kernel, centered residue bracket, and $\beta$. The valid transfer is $\langle z,A_x\beta\rangle=\langle A_x^*z,\beta\rangle$; self-adjointness is not used. A canonical exact certificate, 59 rejected mutations, and 192 exact-rational stress families reproduce these identities. Constant and signed controls show that the compiler alone proves no sign, nonzero value, or arithmetic scale.

<!-- SOURCE_BODY_BEGIN -->

# Frozen source choice and scope

Keep the finite literal TPC-247 source object $$g=A_x\beta,\qquad C_x=\langle w,g\rangle,                         \label{eq:source}$$ on $I_x=(x/2,x]\cap\mathbb Z$, with the inner product conjugate-linear in its first slot `\cite{tpc247}`. TPC-252 shows that a declared binary refinement adds one orthogonal contrast direction and transfers its covariance from the transverse to the longitudinal term `\cite{tpc252}`. Unrestricted partition optimization ends at the degenerate singleton partition. The narrow next question is therefore different: can the physical coordinates themselves freeze one nontrivial split before any coefficient is observed?

Let $$I_x=\{n_1<\cdots<n_N\},\quad N\geq2,\qquad
 \ell=\lfloor N/2\rfloor,\quad r=N-\ell,               \label{eq:ranks}$$ and set $L=\{n_1,\ldots,n_\ell\}$ and $R=\{n_{\ell+1},\ldots,n_N\}$. This choice uses only $x$ and the ordered coordinate set. It is declared before $\beta,w,A_x\beta$, any margin, or any sign. It is a source-frozen modeling choice, not a unique V59-canonical partition and not V59’s smooth bounded-overlap mesoscopic partition.

The exact release status is

`PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER`.

# Rank-midpoint geometry

Put $$h=\frac{\mathbf 1_L}{\ell}-\frac{\mathbf 1_R}{r},\qquad
 \rho^2=\frac{\ell r}{N},\qquad z=\rho h.              \label{eq:contrast}$$

> **Proposition: Normalization and projector**<span id="prop:projector" label="prop:projector">\[prop:projector\]</span> The vector $z$ is the unique unit child-flat zero-sum contrast whose sign is positive on $L$. If $u_J=|J|^{-1/2}\mathbf 1_J$, then $$M_{\mathrm c}=u_{I_x}\otimes u_{I_x},\qquad
>  M_{\mathrm m}=u_L\otimes u_L+u_R\otimes u_R
>       =M_{\mathrm c}+z\otimes z.                                 \label{eq:projector}$$ Every entry of the added projector is the rational number $(z\otimes z)_{ij}=\rho^2h_i h_j$.

> **Proof** The cardinalities give $$\sum_{n\in I_x}h(n)=1-1=0,
>  \qquad
>  \|z\|^2=\frac{\ell r}{N}\left(\frac1\ell+\frac1r\right)=1.$$ If a child-flat zero-sum unit vector equals $a>0$ on $L$ and $b<0$ on $R$, then $b=-\ell a/r$ and unit norm forces $a=\sqrt{r/(\ell N)}=\rho/\ell$; hence $b=-\rho/r$. Thus the sign convention fixes $z$ uniquely. The orthonormal pair $u_{I_x},z$ spans the same child-flat plane as $u_L,u_R$, proving [\[eq:projector\]](main.tex#L98){reference-type="eqref" reference="eq:projector"}. Finally $z_i\overline{z_j}=\rho^2h_i h_j$ because $h$ is real.

The rational projector representation is the executable normalization: no floating approximation to $\rho$ is needed when $N$ is odd.

> **Proposition: Integer crosswalk**<span id="prop:crosswalk" label="prop:crosswalk">\[prop:crosswalk\]</span> For integral $x=k\geq3$, the last coordinate of $L$ is $\lfloor3k/4\rfloor$. Equivalently, $$L=(k/2,\lfloor3k/4\rfloor]\cap\mathbb Z,\qquad
>  R=(\lfloor3k/4\rfloor,k]\cap\mathbb Z.$$

> **Proof** Here $I_k=\{\lfloor k/2\rfloor+1,\ldots,k\}$ and $N=k-\lfloor k/2\rfloor$. Write $k=4m+s$. The four exact cases are
>
> | $s$ | $\lfloor k/2\rfloor$ |   $N$  | $\ell$ | left endpoint |
> |:---:|:--------------------:|:------:|:------:|:-------------:|
> | $0$ |         $2m$         |  $2m$  |   $m$  |      $3m$     |
> | $1$ |         $2m$         | $2m+1$ |   $m$  |      $3m$     |
> | $2$ |        $2m+1$        | $2m+1$ |   $m$  |     $3m+1$    |
> | $3$ |        $2m+1$        | $2m+2$ |  $m+1$ |     $3m+2$    |
>
> The last column is $\lfloor3k/4\rfloor$ in each row.

Proposition [\[prop:crosswalk\]](main.tex#L123){reference-type="ref" reference="prop:crosswalk"} is only an integer crosswalk. Definition [\[eq:ranks\]](main.tex#L71){reference-type="eqref" reference="eq:ranks"}, rather than a threshold formula, remains primary for arbitrary real $x$.

# Partial-sum covariance compiler

For $J\subset I_x$, write $S_f(J)=\sum_{n\in J}f(n)$ and $\mu_f(J)=S_f(J)/|J|$. Put $W_J=S_w(J)$ and $G_J=S_g(J)$.

> **Theorem: Exact midpoint compiler**<span id="thm:compiler" label="thm:compiler">\[thm:compiler\]</span> The contrast moment, two longitudinal terms, covariance transfer, and transverse terms satisfy $$\begin{aligned}
>  \langle z,f\rangle
>  &=\rho\left(\frac{S_f(L)}\ell-\frac{S_f(R)}r\right),                 \label{eq:moment}\\
>  C_{\mathrm{long}}(\mathrm m)
>  &=\frac{\overline{W_L}G_L}{\ell}+\frac{\overline{W_R}G_R}{r},               \label{eq:midlong}\\
>  C_{\mathrm{long}}(\mathrm c)
>  &=\frac{\overline{W_L+W_R}(G_L+G_R)}N,                                  \label{eq:coarselong}\\
>  C_{\mathrm{long}}(\mathrm m)-C_{\mathrm{long}}(\mathrm c)
>  &=\overline{\langle z,w\rangle}\langle z,g\rangle                                               \notag\\
>  &=\frac{\ell r}{N}
>  \overline{\left(\frac{W_L}{\ell}-\frac{W_R}{r}\right)}
>  \left(\frac{G_L}{\ell}-\frac{G_R}{r}\right),                      \label{eq:transfer}\\
>  Q_{\mathrm{trans}}(\mathrm m)-Q_{\mathrm{trans}}(\mathrm c)
>  &=-\overline{\langle z,w\rangle}\langle z,g\rangle.                                             \label{eq:qchange}\end{aligned}$$ Moreover, $$Q_{\mathrm{trans}}(\mathrm m)=\sum_{J\in\{L,R\}}\sum_{n\in J}
>  \overline{w(n)-\mu_w(J)}\,[g(n)-\mu_g(J)],                              \label{eq:within}$$ and $$C_x=C_{\mathrm{long}}(\mathrm m)+Q_{\mathrm{trans}}(\mathrm m),\qquad
>  Q_{\mathrm{trans}}(\mathrm c)=\overline{\langle z,w\rangle}\langle z,g\rangle+Q_{\mathrm{trans}}(\mathrm m).                                    \label{eq:decomp}$$

> **Proof** Equation [\[eq:moment\]](main.tex#L164){reference-type="eqref" reference="eq:moment"} follows by summing the two constant values of $z$. Orthogonal block averaging gives [\[eq:midlong\]](main.tex#L166){reference-type="eqref" reference="eq:midlong"} and [\[eq:coarselong\]](main.tex#L168){reference-type="eqref" reference="eq:coarselong"}. Proposition [\[prop:projector\]](main.tex#L92){reference-type="ref" reference="prop:projector"} and orthogonality of the coarse range with $z$ give $$\langle M_{\mathrm m}w,M_{\mathrm m}g\rangle=\langle M_{\mathrm c}w,M_{\mathrm c}g\rangle
>  +\overline{\langle z,w\rangle}\langle z,g\rangle,$$ where the conjugation is forced by the first-slot convention. Substituting [\[eq:moment\]](main.tex#L164){reference-type="eqref" reference="eq:moment"} gives [\[eq:transfer\]](main.tex#L173){reference-type="eqref" reference="eq:transfer"}. The fixed scalar $C_x$ has the orthogonal decompositions $C_{\mathrm{long}}(\mathrm c)+Q_{\mathrm{trans}}(\mathrm c)$ and $C_{\mathrm{long}}(\mathrm m)+Q_{\mathrm{trans}}(\mathrm m)$, so subtraction gives [\[eq:qchange\]](main.tex#L175){reference-type="eqref" reference="eq:qchange"}. Finally $(I-M_{\mathrm m})w$ and $(I-M_{\mathrm m})g$ are the childwise centered vectors, yielding [\[eq:within\]](main.tex#L180){reference-type="eqref" reference="eq:within"} and [\[eq:decomp\]](main.tex#L185){reference-type="eqref" reference="eq:decomp"}.

The theorem is a complex covariance identity. Neither longitudinal term nor their difference acquires a sign or monotonicity property.

# Literal kernel expansion and safe adjoint

Retain the TPC-247 data $$\begin{gathered}
 H=x^{21/32},\quad Q=x^{1/3},\quad
 \mathcal Q_x=\{q\ \text{prime}:Q<q\leq2Q\},\quad
 K_H(h)=\widehat{\psi_+}(h/H),                                       \label{eq:scales}\\
 \beta(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u).                                    \label{eq:weights}\end{gathered}$$ The inherited superscript in $b_x^{(z)}$ is source notation and does not identify the rank contrast. The literal operator is $$A_x(u,t)=\mathbf 1_{u\ne t}\sum_{q\in\mathcal Q_x}q
 \mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}K_H(u-t)
 \left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right).                 \label{eq:operator}$$

> **Proposition: Literal expansion and adjoint**<span id="prop:literal" label="prop:literal">\[prop:literal\]</span> The midpoint $g$-moment is $$\begin{aligned}
>  \langle z,A_x\beta\rangle
>  ={}&\rho\sum_{q\in\mathcal Q_x}q\sum_{u,t\in I_x}
>  \left(\frac{\mathbf 1_L(u)}\ell-\frac{\mathbf 1_R(u)}r\right)
>  \mathbf 1_{u\ne t}\mathbf 1_{q\nmid u}\mathbf 1_{q\nmid t}                    \notag\\[-2pt]
>  &\qquad\times\beta(t)K_H(u-t)
>  \left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right).               \label{eq:literal}\end{aligned}$$ Also, $$\langle z,A_x\beta\rangle=\langle A_x^*z,\beta\rangle,\qquad
>  (A_x^*z)(t)=\sum_{u\in I_x}\overline{A_x(u,t)}z(u).                    \label{eq:adjoint}$$

> **Proof** Insert [\[eq:operator\]](main.tex#L224){reference-type="eqref" reference="eq:operator"} into [\[eq:moment\]](main.tex#L164){reference-type="eqref" reference="eq:moment"} to obtain [\[eq:literal\]](main.tex#L235){reference-type="eqref" reference="eq:literal"}. No factor is rearranged or dropped. For [\[eq:adjoint\]](main.tex#L240){reference-type="eqref" reference="eq:adjoint"}, expand the finite sums: $$\langle A_x^*z,\beta\rangle
>  =\sum_t\overline{\sum_u\overline{A_x(u,t)}z(u)}\,\beta(t)
>  =\sum_{u,t}\overline{z(u)}A_x(u,t)\beta(t).$$ This is $\langle z,A_x\beta\rangle$. The argument uses only the adjoint definition.

In particular, output $u$, input $t$, the outer weight $q$, both unit masks, the deleted diagonal, $K_H(u-t)$, the centered residue bracket, and literal $\beta(t)$ all remain visible. No symmetry of $K_H$, equality $A_x^*=A_x$, or self-adjointness is source-locked.

# Sharp controls, exact audit, and limitations

> **Proposition: Nonliteral sharp controls**<span id="prop:controls" label="prop:controls">\[prop:controls\]</span> If $w$ is constant or $g$ is constant, the transfer in [\[eq:transfer\]](main.tex#L173){reference-type="eqref" reference="eq:transfer"} is zero. The synthetic choices $(w,g)=(z,z)$ and $(z,-z)$ give transfer $+1$ and $-1$, respectively.

> **Proof** A constant factor has zero $z$-moment because $\sum z=0$. For the signed controls, $\langle z,z\rangle=1$, so the two products are $1$ and $-1$.

These are exact finite Hilbert-space controls, not literal numerical V59 instances. They show that source-free geometry cannot decide sign, nonvanishing, or scale.

#### Executable audit.

The certificate stores rational and Gaussian-rational data as canonical strings and uses only $\rho^2h_i h_j$ for projector products. An odd-rank, nonintegral-clock fixture checks all formulas. A separately labeled nonliteral exact-kernel sample substitution checks every factor in [\[eq:operator\]](main.tex#L224){reference-type="eqref" reference="eq:operator"}; its deliberately non-self-adjoint matrix verifies that [\[eq:adjoint\]](main.tex#L240){reference-type="eqref" reference="eq:adjoint"}, rather than an $A_x^*=A_x$ shortcut, is used. The independent checker imports no producer, enforces exact integer types, and rejects 59 typed, semantic, digest, duplicate-key, nonfinite, and noncanonical mutations. The stress program verifies 192 deterministic families: 96 integer clocks, including 24 in each class modulo four, and 96 nonintegral rational clocks. Optimized and normal Python modes produce identical output. These computations reproduce finite algebra only.

#### Claim firewall.

The rank midpoint is not V59-canonical and is not identified with a smooth V59 partition. The exact-sample kernel fixture is not an actual V59 numerical replay. We claim no $A_x$ self-adjointness, contrast sign, nonzero value, asymptotic scale, arithmetic saving, L2 theorem, fixed-atom credit, Gate-B closure, strict $1/400$, or twin-prime result. The open theorem is a source-backed joint estimate for $\langle z,w\rangle$ and $\langle z,A_x\beta\rangle$ on one common growing V59 clock.

# Conclusion

The ordered physical interval now supplies one reproducible nontrivial contrast before the source coefficients are observed. Its projector, partial sums, covariance transfer, within-child remainder, literal kernel expansion, and adjoint orientation are exact. The compiler isolates the two literal imbalances that a future arithmetic theorem must estimate; it does not estimate them itself.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc247,
  author = {Liang Wang},
  title = {Literal V59 Source-Operator Two-Lane Block Attachment},
  year = {2026},
  note = {TPC-247 project-local repository paper, August 25, 2026}
}

@misc{tpc252,
  author = {Liang Wang},
  title = {Binary Refinement Calculus and Singleton Degeneracy for Declared-Block V59 Margins},
  year = {2026},
  note = {TPC-252 project-local repository paper, August 25, 2026}
}
```

<!-- SOURCE_BODY_END -->
