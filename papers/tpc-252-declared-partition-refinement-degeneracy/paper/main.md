# Binary Refinement Calculus and Singleton Degeneracy\ for Declared-Block V59 Margins

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

We determine the exact effect of refining a declared coordinate partition in the longitudinal–transverse compiler for the finite V59 source scalar. A binary split enlarges the block-averaging range by one normalized contrast, so the projection has a rank-one update. The associated contrast covariance is added to the longitudinal term and subtracted from the transverse term, with the conjugation fixed by the first-slot convention. The exact transverse radius cannot increase. Repeated refinement reaches the singleton partition, where all projected probes, projected Gram data, coherence quantities, and transverse radii vanish, while the longitudinal term equals the original scalar. It follows that, for every fixed external error $E\geq0$, maximizing the TPC-251 lower margin over all legal declared partitions gives exactly $[|C_x|-E]_+$; adaptive partition search produces no stronger certificate than the direct external bound. A two-coordinate synthetic replay proves that the resulting coarse/fine decomposition metrics can differ while $A,\beta,w$ remain fixed and unchanged; a second fixed source refutes universal instability. No monotonicity of the intermediate coherence radius or literal V59 arithmetic gain is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Source lock and declared projections

Let $H=\mathbb{C}^I$, where $I$ is finite and nonempty, and take the inner product to be conjugate-linear in its first argument. We freeze the finite source object from TPC-247 `\cite{tpc247}`, $$\label{eq:source}
 g=A_x\beta,\qquad C_x=\langle w,g\rangle.$$ No property of the entries of $A_x$ is used below. The literal source weight remains $\lambda_{cb}=1$.

Let $\mathcal P$ be an exhaustive partition of $I$ into nonempty coordinate blocks. For $J\in\mathcal P$, embed $$u_J=|J|^{-1/2}{\bf1}_J\in H$$ and define the block-averaging orthogonal projection $$\label{eq:projection}
 M_{\mathcal P}=\sum_{J\in\mathcal P}u_J\otimes u_J,
 \qquad (u\otimes u)h=u\langle u,h\rangle.$$ The global form of the TPC-251 split `\cite{tpc251}` is $$\begin{aligned}
 C_{\rm long}(\mathcal P)&=\langle M_{\mathcal P}w,M_{\mathcal P}g\rangle,\label{eq:long}\\
 Q_{\rm trans}(\mathcal P)&=\langle (I-M_{\mathcal P})w,(I-M_{\mathcal P})g\rangle.
 \label{eq:qtrans}\end{aligned}$$ Since the two ranges are orthogonal, $$\label{eq:split}
 C_x=C_{\rm long}(\mathcal P)+Q_{\rm trans}(\mathcal P).$$

For later use, write $w_J^\perp$ and $g_J^\perp$ for the restrictions of the two transverse vectors to $J$, and set $$\label{eq:rtrans}
 R_{\rm trans}(\mathcal P)
 =\sum_{J\in\mathcal P}\lVert w_J^\perp\rVert\lVert g_J^\perp\rVert.$$ TPC-251 further bounds this by a projected-coherence radius $R_{\rm coh}(\mathcal P)$, using the total TPC-250 convention that coherence is zero when fewer than two projected probes are active `\cite{tpc250}`: $$\label{eq:tpc251}
 |C_x-C_{\rm long}(\mathcal P)|
 \leq R_{\rm trans}(\mathcal P)\leq R_{\rm coh}(\mathcal P).$$ The partition is declared data, not a V59-canonical object.

# Exact binary refinement calculus

Suppose $\mathcal P'$ replaces one block $J$ by disjoint nonempty blocks $J_1,J_2$. Put $n_i=|J_i|$, $n=n_1+n_2$, and define the normalized contrast $$\label{eq:z}
 z=\sqrt{\frac{n_2}{n_1n}}\,{\bf1}_{J_1}
   -\sqrt{\frac{n_1}{n_2n}}\,{\bf1}_{J_2}.$$

> **Theorem: Binary refinement**<span id="thm:binary" label="thm:binary">\[thm:binary\]</span> For fixed $w,g$, the averaging projections and covariances obey $$\begin{aligned}
>  M_{\mathcal P'}&=M_{\mathcal P}+z\otimes z,\label{eq:mupdate}\\
>  C_{\rm long}(\mathcal P')
>  &=C_{\rm long}(\mathcal P)+\overline{\langle z,w\rangle}\langle z,g\rangle,\label{eq:cupdate}\\
>  Q_{\rm trans}(\mathcal P')
>  &=Q_{\rm trans}(\mathcal P)-\overline{\langle z,w\rangle}\langle z,g\rangle.
>  \label{eq:qupdate}\end{aligned}$$ Moreover, $$\label{eq:rmono}
>  R_{\rm trans}(\mathcal P')\leq R_{\rm trans}(\mathcal P).$$

> **Proof** The support sizes in [\[eq:z\]](main.tex#L102){reference-type="eqref" reference="eq:z"} give $\lVert z\rVert=1$, while direct summation gives $\langle u_J,z\rangle=0$. The old flat unit and the contrast form an orthonormal basis of the two-dimensional child-flat space: $$\operatorname{span}\{u_{J_1},u_{J_2}\}
>  =\operatorname{span}\{u_J\}\mathbin{\perp}
>   \operatorname{span}\{z\}.$$ All other flat directions are unchanged, proving [\[eq:mupdate\]](main.tex#L110){reference-type="eqref" reference="eq:mupdate"}.
>
> Let $Z=z\otimes z$. The ranges of $M_{\mathcal P}$ and $Z$ are orthogonal, so $$\langle M_{\mathcal P'}w,M_{\mathcal P'}g\rangle=\langle M_{\mathcal P}w,M_{\mathcal P}g\rangle+\langle Zw,Zg\rangle.$$ Because $Zw=z\langle z,w\rangle$ and the first slot is conjugate-linear, $\langle Zw,Zg\rangle=\overline{\langle z,w\rangle}\langle z,g\rangle$. This proves [\[eq:cupdate\]](main.tex#L112){reference-type="eqref" reference="eq:cupdate"}. The old transverse range is the orthogonal direct sum of $\operatorname{span}
> \{z\}$ and the new transverse range; subtracting the same pairing proves [\[eq:qupdate\]](main.tex#L115){reference-type="eqref" reference="eq:qupdate"}.
>
> For the radius, decompose the old parent residuals orthogonally as $$w_J^\perp=z\langle z,w\rangle+w_1^\perp+w_2^\perp,\qquad
>  g_J^\perp=z\langle z,g\rangle+g_1^\perp+g_2^\perp.$$ Set $x_0=|\langle z,w\rangle|$, $x_i=\lVert w_i^\perp\rVert$ and similarly $y_0=|\langle z,g\rangle|$, $y_i=\lVert g_i^\perp\rVert$. The refined contribution satisfies $$\begin{aligned}
>  x_1y_1+x_2y_2
>  &\leq \sqrt{x_1^2+x_2^2}\sqrt{y_1^2+y_2^2}\\
>  &\leq \sqrt{x_0^2+x_1^2+x_2^2}
>           \sqrt{y_0^2+y_1^2+y_2^2},\end{aligned}$$ which is the old parent contribution. The remaining blocks are unchanged.

The theorem transfers one covariance from the transverse term to the longitudinal term; it does not give either term a monotone absolute value. Equation [\[eq:rmono\]](main.tex#L118){reference-type="eqref" reference="eq:rmono"} concerns the exact radius only. No monotonicity of $R_{\rm coh}$ is asserted because the projected probes and their coherence data change under common repartition.

# Fixed probes, singleton collapse, and optimal margins

There is one useful rank-one consequence whose indexing must be frozen.

> **Proposition: Fixed-family Gram subtraction**<span id="prop:gram" label="prop:gram">\[prop:gram\]</span> Let $v_1,\ldots,v_m$ be a fixed family independent of the partition, and set $$G_{\mathcal P}^{\perp}(i,j)
>  =\langle (I-M_{\mathcal P})v_i,(I-M_{\mathcal P})v_j\rangle.$$ Under the split in Theorem [\[thm:binary\]](main.tex#L107){reference-type="ref" reference="thm:binary"}, $$\label{eq:gramupdate}
>  G_{\mathcal P'}^{\perp}(i,j)
>  =G_{\mathcal P}^{\perp}(i,j)
>   -\overline{\langle z,v_i\rangle}\langle z,v_j\rangle.$$

> **Proof** Use $I-M_{\mathcal P'}=(I-M_{\mathcal P})-z\otimes z$. Since $z$ lies in the old transverse range, expansion of the two residuals removes exactly their $z$-Gram pairing.

The qualification “fixed family” is essential. Native TPC-251 probes have $v_{cb}=P_cA_xP_b\beta$. A common input/output repartition changes both indices, the number of probes, and the vectors, so [\[eq:gramupdate\]](main.tex#L177){reference-type="eqref" reference="eq:gramupdate"} is not an indexed before/after update for those native arrays.

Let $\mathcal S$ denote the singleton partition of $I$.

> **Corollary: Singleton degeneracy**<span id="cor:singleton" label="cor:singleton">\[cor:singleton\]</span> For every finite source in [\[eq:source\]](main.tex#L56){reference-type="eqref" reference="eq:source"}, $M_{\mathcal S}=I$. Every native projected probe and its projected Gram matrix vanish. On every output singleton, $$D=L=\mu=U=0,$$ and globally $$\label{eq:singleton}
>  Q_{\rm trans}(\mathcal S)=R_{\rm trans}(\mathcal S)
>  =R_{\rm coh}(\mathcal S)=0,\qquad
>  C_{\rm long}(\mathcal S)=C_x.$$ The normalized parameter $\kappa=L^2/D$ is undefined at this $D=0$ endpoint.

> **Proof** Block averaging on one coordinate is the identity. Thus every transverse projection is zero, and all probe, Gram, norm, coherence, and scalar conclusions follow. The value $\mu=0$ uses the fewer-than-two-active-probes convention; $\kappa$ is not formed.

The singleton endpoint solves the unrestricted partition optimization exactly.

> **Theorem: Margin optimality**<span id="thm:margin" label="thm:margin">\[thm:margin\]</span> For every fixed independently certified $E\geq0$, $$\label{eq:margin}
>  \max_{\mathcal P}
>  \left[|C_{\rm long}(\mathcal P)|-R_{\rm coh}(\mathcal P)-E\right]_{+}
>  =\left[|C_x|-E\right]_{+},$$ where the maximum ranges over all exhaustive nonempty coordinate partitions.

> **Proof** Equation [\[eq:tpc251\]](main.tex#L92){reference-type="eqref" reference="eq:tpc251"} implies $|C_{\rm long}(\mathcal P)|\leq |C_x|+R_{\rm coh}(\mathcal P)$. Subtracting $R_{\rm coh}(\mathcal P)+E$ and applying the monotone positive-part map gives the upper bound in [\[eq:margin\]](main.tex#L225){reference-type="eqref" reference="eq:margin"}. Corollary [\[cor:singleton\]](main.tex#L197){reference-type="ref" reference="cor:singleton"} shows that $\mathcal S$ attains it. The maximum exists because a finite set has only finitely many partitions.

If an external scalar $F$ satisfies $|F-C_x|\leq E$, the right side of [\[eq:margin\]](main.tex#L225){reference-type="eqref" reference="eq:margin"} is precisely the direct reverse-triangle lower bound for $|F|$. Adaptive declared-partition optimization therefore adds no strength.

# Same-source non-invariance and exact verification

Partition dependence can nevertheless occur for fixed source data.

> **Proposition: Existential two-coordinate witness**<span id="prop:witness" label="prop:witness">\[prop:witness\]</span> On $\mathbb{C}^2$, take $$A=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
>  \beta=\begin{pmatrix}-1\\1\end{pmatrix},\qquad
>  w=\begin{pmatrix}1\\-1\end{pmatrix}.$$ Then $g=A\beta=w$ and $C_x=2$. The one-block and singleton partitions give the exact values in Table [1](main.tex#L275){reference-type="ref" reference="tab:witness"}.

<div id="tab:witness">

| Partition  | $C_{\rm long}$ | $Q_{\rm trans}$ | $R_{\rm trans}$ | $R_{\rm coh}$ | margin at $E=1/2$ |
|:-----------|:--------------:|:---------------:|:---------------:|:-------------:|:-----------------:|
| One block  |       $0$      |       $2$       |       $2$       |      $2$      |        $0$        |
| Singletons |       $2$      |       $0$       |       $0$       |      $0$      |       $3/2$       |

: Decomposition metrics for the same unchanged synthetic $A,\beta,w$ under the two legal partitions of a two-coordinate set.

</div>

> **Proof** Both $w$ and $g$ have coarse mean zero, so the full pairing is transverse. There is one active coarse projected probe: $D=2$, $L=\sqrt2$, $\mu=0$, $U=\sqrt2$, and $\lVert w^\perp\rVert=\sqrt2$, giving $R_{\rm coh}=2$. Corollary [\[cor:singleton\]](main.tex#L197){reference-type="ref" reference="cor:singleton"} gives the second row.

This witness is explicitly classified as a *synthetic exact finite source-operator replay, not a literal V59 arithmetic instance*. It proves existence only. With the same swap matrix, $\beta=(1,1)$ and $w=(2,2)$ instead give $C_{\rm long}=C_x=4$ and zero transverse terms for both partitions. Hence every-source instability is false.

The exact release certificate also uses a Gaussian-rational four-coordinate split. In an orthonormal block basis $(u,z,t)$, it takes $$w=2u+(1+i)z+t,\qquad g=3u+(2+2i)z+2t.$$ The contrast increment is $\overline{(1+i)}(2+2i)=4$, whereas omission of conjugation would give $4i$. The replay checks $$(C_{\rm long},Q_{\rm trans},R_{\rm trans}):
 (6,6,6)\longmapsto(10,2,2),\qquad C_x=12.$$ An independently implemented checker rejects $28$ typed, semantic, digest, duplicate-key, nonfinite-token, and canonical-byte mutations. A deterministic stress suite verifies $192$ exact Gaussian-rational refinement families, including the fixed-family Gram update and singleton collapse, in normal and optimized Python modes. These finite computations reproduce structural identities; they are not arithmetic or asymptotic evidence.

# Limitations and conclusion

The result identifies a degeneracy in the unrestricted declared-partition compiler. It neither chooses a non-singleton partition canonically nor proves that a literal V59 source has nonzero covariance in any coarse contrast. Intermediate $R_{\rm coh}$ monotonicity is not established, and the fixed-probe Gram formula cannot be attached to changing native probe arrays without a new indexing argument. The external $E$ remains independently certified.

The narrow consequence is definitive: binary refinement has an exact rank-one covariance calculus, the true transverse radius is monotone, and the singleton endpoint makes all-partition margin optimization equal to the direct external bound. The maximum supported claim is structural L1 only. There is no canonical partition, actual V59 asymptotic, arithmetic advance, L2, Route A, fixed-atom credit, Gate-B closure, global strict $1/400$, or twin-prime conclusion. The next source-specific question is the direct one: can $|C_x|>E$ be certified on a literal V59 clock?

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc247,
  author = {Liang Wang},
  title = {Literal V59 Source-Operator Two-Lane Block Attachment},
  year = {2026},
  note = {TPC-247 project-local repository paper, August 25, 2026}
}

@misc{tpc250,
  author = {Liang Wang},
  title = {Coherence-Controlled Gram Quadratic Bounds and Sharpness},
  year = {2026},
  note = {TPC-250 project-local repository paper, August 25, 2026}
}

@misc{tpc251,
  author = {Liang Wang},
  title = {A Declared-Block Longitudinal--Transverse Margin Compiler for the Literal V59 Scalar},
  year = {2026},
  note = {TPC-251 project-local repository paper, August 25, 2026}
}
```

<!-- SOURCE_BODY_END -->
