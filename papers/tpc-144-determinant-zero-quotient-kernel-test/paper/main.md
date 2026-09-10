# **Determinant and Zero-Mode Quotients**\ **on a Frontier Lift: Kernel Equivalence**\ **and the Missing Canonical-Parent Bridge**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-144-determinant-zero-quotient-kernel-test.pdf](../tpc-144-determinant-zero-quotient-kernel-test.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The determinant fibers used by the TPC energy gate and the ordered outer fibers used by the signed zero-mode gate are two different quotients of a literal occurrence archive. We give an exact simultaneous-lift criterion. For finite surjective maps $Q_D,Q_Z$ with a common domain, an isomorphism $J$ satisfying $JQ_D=Q_Z$ exists precisely when $\ker Q_D=\ker Q_Z$. If $J$ must be a literal relabeling, equality of kernels is supplemented by equality of occurrence partitions and exact map multipliers. Equality on one coefficient vector, or of one final scalar sum, does not imply this criterion. Applying the test to the source-locked cut archive exposes the exact missing fields. The determinant quotient needs the canonical parent, targets, content, normalized determinant and inverse aggregation; the zero quotient needs the outer affine key, canonical order, arithmetic sign, reconstruction weight and content allocation. Neither field family is connected to the cut paths by the absent occurrence lift. Thus the abstract quotient test is proved at $\mathrm{L0}$, whereas both literal totality statements and their intertwining remain <span class="smallcaps">not-testable</span>. No determinant-energy, zero-mode or fixed-shift arithmetic exponent is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Two quotients, one literal domain

Let $\mathcal O_X$ be a fully typed row-separated occurrence space on all nonsoft cut paths. This includes both eligible-tail-open and frontier-unmapped records. TPC-143 identifies the still missing conservative lift from the cut archive to $\mathcal O_X$ `\citep{WangTPC136,WangTPC143}`.

The determinant construction of TPC-95 and TPC-110 first inverse-aggregates computational children to canonical mathematical parents $t=(\alpha,\gamma,j)$. A parent has ordered slopes $m_\alpha,m_\gamma$, targets $$x_t=m_\alpha j+h_0,\qquad y_t=m_\gamma j+h_0,$$ content $c_t=(x_t,y_t)$, and the literal determinant label $$\nu_D(t)=\frac{m_\alpha-m_\gamma}{c_t}\in\mathbb Z\setminus\{0\}.
 \label{eq:detlabel}$$ We write $\nu_D$ rather than $\nu$ to prevent collision with the physical normalization identifier $\nu_{\rm phys}$.

The zero-mode construction of TPC-111 and TPC-122 instead uses outer affine keys $\theta$, canonically ordered coordinates $$r_{\theta,1}<\cdots<r_{\theta,m_\theta},$$ literal signs $\sigma_{\theta,i}$, outer weights $w_{\theta,i}$, and an exact retained/content allocation `\citep{WangTPC111,WangTPC122}`. The order is part of the object: permuting a fiber can preserve its final scalar while changing every signed-prefix maximum.

> **Definition: Literal quotient maps** Let $H_X=\mathbb C^{\mathcal O_X}$. A literal determinant quotient $$Q_D:H_X\longrightarrow K_D$$ is the exact inverse-aggregation and determinant-binning map on the canonical parents. A literal zero-mode quotient $$Q_Z:H_X\longrightarrow K_Z$$ is the exact outer-record aggregation with its canonical order and factor allocation retained in the output records.

The linear maps contain exact multipliers; a target label without its edge multiplier is not a quotient implementation. A zero literal coefficient is not permission to omit its formal occurrence unless an exact aggregation theorem supplies that zero.

# The quotient-kernel criterion

> **Theorem: Simultaneous quotient lift** <span id="thm:kernel" label="thm:kernel">\[thm:kernel\]</span> Let $H,K_D,K_Z$ be finite-dimensional vector spaces and let $$Q_D:H\to K_D,\qquad Q_Z:H\to K_Z$$ be surjective. There exists a unique isomorphism $J:K_D\to K_Z$ satisfying $$JQ_D=Q_Z
>  \label{eq:intertwine}$$ if and only if $$\boxed{\ker Q_D=\ker Q_Z.}
>  \label{eq:kernels}$$

> **Proof** If [\[eq:intertwine\]](../main.tex#L140){reference-type="eqref" reference="eq:intertwine"} holds with $J$ injective, then $$Q_Dv=0\iff JQ_Dv=0\iff Q_Zv=0.$$ Conversely, under [\[eq:kernels\]](../main.tex#L145){reference-type="eqref" reference="eq:kernels"} define $$J(Q_Dv)=Q_Zv.$$ If $Q_Dv=Q_Dw$, then $v-w\in\ker Q_D=\ker Q_Z$, so the definition is well posed. It is linear and onto because $Q_Z$ is onto. Its kernel is zero by the same kernel equality, hence it is an isomorphism. Surjectivity of $Q_D$ makes $J$ unique.

> **Corollary: Row-space execution** <span id="cor:rowspace" label="cor:rowspace">\[cor:rowspace\]</span> After bases are fixed, [\[eq:kernels\]](../main.tex#L145){reference-type="eqref" reference="eq:kernels"} is equivalent to equality of the row spaces of $Q_D$ and $Q_Z$. It is therefore decidable by exact row reduction.

> **Proof** For a finite matrix $A$, the row space is the annihilator of $\ker A$. Equal kernels have equal annihilators, and conversely.

> **Remark: Literal relabeling is stronger** The isomorphism in [\[thm:kernel\]](../main.tex#L131){reference-type="ref" reference="thm:kernel"} is an abstract linear map. If the proposed $J$ is a relabeling of literal fibers, the occurrence equivalence relations, canonical orders where applicable, and exact map multipliers must also match. Equal kernels do not authorize an unrecorded change of physical meaning.

> **Proposition: Literal relabeling test** <span id="prop:literal-relabel" label="prop:literal-relabel">\[prop:literal-relabel\]</span> Fix occurrence-column orderings and typed bases of $K_D,K_Z$. For an allowed metadata-preserving bijection $\varphi$ between the two output-record sets, let $\Pi_\varphi$ be its permutation matrix. Then $\varphi$ intertwines the literal quotients if and only if $$Q_Z=\Pi_\varphi Q_D.$$ Equivalently, after the allowed relabeling, the complete weighted rows —not merely their supports or final scalar sums—agree exactly. Kernel equality alone does not imply this condition.

> **Proof** The displayed equality is precisely the coefficientwise statement $\Pi_\varphi Q_Dv=Q_Zv$ for every occurrence vector $v$. For strictness, take $$Q_D=I_2,\qquad
>  Q_Z=\begin{pmatrix}1&1\\0&1\end{pmatrix}.$$ Both kernels are zero, but the rows of $Q_Z$ are not a permutation of the rows of $Q_D$.

# Why scalar equality is insufficient

> **Proposition: A conservative scalar can hide distinct kernels** <span id="prop:scalar" label="prop:scalar">\[prop:scalar\]</span> There are surjective incidence quotients $Q_D,Q_Z$ such that $$\mathbf 1^TQ_Dc=\mathbf 1^TQ_Zc
> \quad\hbox{for every }c,$$ but $\ker Q_D\ne\ker Q_Z$.

> **Proof** Take $$Q_D=\begin{pmatrix}1&1&0\\0&0&1\end{pmatrix},
>  \qquad
>  Q_Z=\begin{pmatrix}1&0&1\\0&1&0\end{pmatrix}.$$ Both matrices have column sums one, so their final scalar sums agree on every vector. But $$(1,-1,0)\in\ker Q_D,\qquad
>  Q_Z(1,-1,0)^T=(1,-1)^T\ne0.$$

TPC-124 already requires the coefficientwise matrix identity $(JQ_D-Q_Z)M=0$, not agreement on one literal coefficient vector `\citep{WangTPC124}`. The kernel criterion explains the quotient geometry behind that firewall. Even equality for every final scalar does not determine which occurrences were identified. If $M$ is not surjective onto $H_X$, however, the TPC-124 identity constrains only $\operatorname{Ran}M$. Then the full-space kernel equality in [\[thm:kernel\]](../main.tex#L131){reference-type="ref" reference="thm:kernel"} is sufficient but need not be necessary; the exact restricted criterion compares $$\ker(Q_D|_{\operatorname{Ran}M})
 \quad\hbox{and}\quad
 \ker(Q_Z|_{\operatorname{Ran}M})$$ with codomains replaced by their respective images. A full-space necessity claim therefore requires a proved surjectivity statement for $M$. This restricted kernel test concerns existence of an abstract image isomorphism; a prescribed or literal $J$ must still pass the coefficientwise identity on $\operatorname{Ran}M$.

# Exact field requirements

Before either quotient is compared, both matrices must provide the same ordered occurrence-column registry. Each must also certify surjectivity onto its declared codomain or explicitly replace that codomain by the image used in the restricted criterion.

For $Q_D$, every completed occurrence lineage must provide:

1.  the canonical parent and exact child-to-parent aggregation;

2.  row identifiers, integer slopes, $j$, targets and content;

3.  an exact verification of [\[eq:detlabel\]](../main.tex#L93){reference-type="eqref" reference="eq:detlabel"};

4.  physical and computational multiplicities in distinct fields;

5.  the literal parent coefficient $u_t$; and

6.  the determinant-bin target and exact map multiplier.

For $Q_Z$, it must provide:

1.  the outer affine key and ordered coordinate;

2.  the canonical rank within the outer interval;

3.  the literal arithmetic sign and outer reconstruction weight;

4.  the fixed factor-allocation identifier;

5.  retained/content status and content-remainder destination; and

6.  the zero-mode output record and exact map multiplier.

These lists are data contracts, not determinant or prefix estimates. In particular, recording $u_t$ does not prove phase coherence, and recording $\sigma_{\theta,i}$ does not prove a signed-prefix saving `\citep{WangTPC121,WangTPC122}`.

> **Proposition: The common parent bridge is absent** <span id="prop:missing" label="prop:missing">\[prop:missing\]</span> The committed TPC-136 and TPC-143 artifacts contain no exact map from a nonsoft cut path to the canonical parent or outer occurrence records above. Consequently neither literal quotient matrix can be formed from the current artifacts.

> **Proof** TPC-143 performs an exact field census on every nonsoft cut record. The cut records contain the native tuple $(\ell,k,d)$, dyadic block, cut type, $h_0$ and normalization. They contain none of the canonical-parent, inverse-aggregation, outer-key, ordered-coordinate or quotient-edge fields listed above. A statement defining those objects in an earlier paper is not a path-ID crosswalk. Thus the matrix rows and columns required for $Q_D,Q_Z$ have no current literal source.

# Executable theorem and actual verdict

The companion program `experiments/tpc144_quotient_kernel_audit.py` uses exact rational row reduction. Synthetic matrices verify \[[thm:kernel](../main.tex#L131),[prop:literal-relabel](../main.tex#L185),[prop:scalar](../main.tex#L213)\], including the surjectivity precondition; they are explicitly marked `SYNTHETIC_L0_ONLY`. A separate actual manifest imports the TPC-143 occurrence-lift status and contains no fabricated map edge. Default mode writes deterministic JSON and `–check` compares it byte for byte without writing.

\@P0.36P0.24Y@ Statement & Status & Scope\
Surjective quotient kernel criterion & $\textnormal{\textsc{proved}}_{\mathrm{L0}}$ & Exact finite-dimensional theorem.\
Literal $Q_D$ totality & $\textnormal{\textsc{not-testable}}$ & Missing occurrence and canonical-parent lift.\
Literal $Q_Z$ totality & $\textnormal{\textsc{not-testable}}$ & Missing outer records, order and allocation.\
$Q_D/Q_Z$ intertwining & $\textnormal{\textsc{not-testable}}$ & Neither actual kernel is available.\
Schema/scalar-only derivation & $\textnormal{\textsc{stop-declared-route}}$ & Scoped stop; augmented lift remains open.\

The audit rejects a frontier-only domain, a fabricated quotient edge, a proved status without a source, deletion of a required D6/Z6 field, promotion of either actual kernel or literal relabeling, and a scalar-to-coefficientwise promotion. Its required domain remains $$\mathcal C_X^{\mathsf{ETO}}\sqcup
 \mathcal C_X^{\mathsf{FUM}},$$ even though the current finite sample has no eligible-tail row.

# Claim boundary

> **Theorem: Current quotient verdict** For the current source-locked occurrence obligations, $$\boxed{
> \begin{aligned}
> \mathsf{H1.frontier\_QD\_totality}&=\textnormal{\textsc{not-testable}},\\
> \mathsf{H1.frontier\_QZ\_totality}&=\textnormal{\textsc{not-testable}},\\
> \mathsf{H1.frontier\_QD\_QZ\_intertwining}&=\textnormal{\textsc{not-testable}}.
> \end{aligned}}$$ The direct schema-or-scalar derivation is stopped, while a theorem-backed occurrence-augmented route is not stopped.

No assertion here bounds the complete frontier scalar, proves that a formal coefficient is nonzero, lower-bounds determinant energy, controls the distinguished zero mode, gives a positive fixed-$h_0$ $\mathrm{L2}$ saving, pays the $1/400$ endpoint, or proves a prime-pair or twin-prime statement. The next input remains the literal occurrence lift identified by TPC-143.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC95,
  author = {Wang, Liang},
  title  = {Shared-Target Rigidity, Dominance Energy, and the Exact Native Census},
  year   = {2026},
  note   = {TPC-95 manuscript}
}

@misc{WangTPC110,
  author = {Wang, Liang},
  title  = {Post-Bin Determinant Energy on the Literal Carrier},
  year   = {2026},
  note   = {TPC-110 manuscript}
}

@misc{WangTPC111,
  author = {Wang, Liang},
  title  = {The Distinguished Zero Mode and Ordered Outer Reassembly},
  year   = {2026},
  note   = {TPC-111 manuscript}
}

@misc{WangTPC121,
  author = {Wang, Liang},
  title  = {A Fiber-Phase Coherence Certificate},
  year   = {2026},
  note   = {TPC-121 manuscript}
}

@misc{WangTPC122,
  author = {Wang, Liang},
  title  = {Signed-Prefix Transfer to the Distinguished Zero Mode},
  year   = {2026},
  note   = {TPC-122 manuscript}
}

@misc{WangTPC124,
  author = {Wang, Liang},
  title  = {Provenance-Faithful Physical Reassembly},
  year   = {2026},
  note   = {TPC-124 manuscript}
}

@misc{WangTPC136,
  author = {Wang, Liang},
  title  = {A Complete Cut Archive at the First Unsupported Carrier},
  year   = {2026},
  note   = {TPC-136 manuscript}
}

@misc{WangTPC143,
  author = {Wang, Liang},
  title  = {The Frontier Occurrence-Lift Contract},
  year   = {2026},
  note   = {TPC-143 manuscript}
}
```

<!-- SOURCE_BODY_END -->
