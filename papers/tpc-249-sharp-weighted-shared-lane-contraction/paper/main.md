# Sharp Weighted Contraction\ on Shared Gram Lanes

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology; Wuhan, China; liang.wang@hust.edu.cn
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The exact Gram ellipsoid for a shared output lane is multivariate, whereas the Gate-B reassembly ultimately requires a weighted scalar. We perform this contraction without splitting the lane into tagged copies. For probes $v_{cb}$, weights $\lambda_{cb}$, Gram matrix $G_c$, and independent lane balls $\|W_c\|\leq\rho_c$, the aggregate scalar has the exact disk image of radius $$R=\sum_c\rho_c\left\|\sum_b\lambda_{cb}v_{cb}\right\|
  =\sum_c\rho_c\sqrt{\lambda_c^*G_c\lambda_c}.$$ We give an explicit preimage for every disk point, derive the exact global direct-sum-budget radius, and sharply compare $R$ with the tagged marginal triangle radius. Equality occurs precisely under common-ray alignment on every active group. Repeated probes with opposite weights have zero exact radius but positive tagged radius, proving that contraction can recover cancellation erased by external copies. Affine translation is stated only for a declared modeling choice. No asymptotic Gram estimate, arithmetic $L^2$, Gate-B closure, or twin-prime result is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Literal weighted probes

TPC-247 supplies, for each hard output block $c$, the vectors $v_{cb}=A_{cb}\beta_b$ paired with one physical lane $w_c$. TPC-248 then classifies the complete shared-lane covariance vector by its Gram matrix `\cite{tpc247,tpc248}`. Let $\lambda_{cb}\in\mathbb C$ be fixed covariance weights and put $$g_c:=\sum_b\lambda_{cb}v_{cb},\qquad
 (G_c)_{bb'}=\langle v_{cb},v_{cb'}\rangle.$$ Our inner products are conjugate-linear in the first slot, hence linear in the second. Therefore the exact physical orientation is $$\sum_b\lambda_{cb}\langle W_c,v_{cb}\rangle
 =\langle W_c,g_c\rangle,
 \qquad
 \|g_c\|^2=\lambda_c^*G_c\lambda_c.$$ No conjugation of $\lambda_{cb}$ occurs in the definition of $g_c$.

# Exact independent-lane radius

> **Theorem: sharp weighted disk**<span id="thm:disk" label="thm:disk">\[thm:disk\]</span> Let $c$ range over a finite set, let $\rho_c\geq0$, and let $\|W_c\|\leq\rho_c$ independently. Then $$\left\{\sum_{c,b}\lambda_{cb}\langle W_c,v_{cb}\rangle\right\}
>  =R\overline{\mathbb D},
>  \qquad
>  R=\sum_c\rho_c\sqrt{\lambda_c^*G_c\lambda_c}.$$ Every point of the disk has an explicit preimage.

> **Proof** Write $r_c=\rho_c\|g_c\|$. Cauchy’s inequality gives $|\langle W_c,g_c\rangle|\leq r_c$. Conversely, if $g_c\neq0$, every $d_c$ with $|d_c|\leq r_c$ is realized by $$W_c=\frac{\overline{d_c}}{\|g_c\|^2}g_c,
>  \qquad \langle W_c,g_c\rangle=d_c.$$ If $g_c=0$, its image is the zero disk. Thus the aggregate image is the Minkowski sum of centered disks $r_c\overline\mathbb D$, namely $R\overline\mathbb D$. When $R>0$, a target $d$ is realized by assigning $d_c=(r_c/R)d$ and using the formula above. If $R=0$, every active functional vanishes and the image is $\{0\}$.

> **Corollary: declared affine model**<span id="cor:affine" label="cor:affine">\[cor:affine\]</span> Suppose one explicitly chooses the affine uncertainty domain $W_c=W_c^0+U_c$, $\|U_c\|\leq\rho_c$. Its exact scalar image is $$C+R\overline\mathbb D,
>  \qquad C=\sum_c\langle W_c^0,g_c\rangle.$$ Consequently zero is feasible iff $|C|\leq R$, and the minimum modulus is $\max\{|C|-R,0\}$.

> **Remark** The affine domain is a modeling choice, not a source-forced V59 uncertainty family. The centered support theorem remains unconditional finite geometry.

# One global budget

Independent radii and a global energy budget must not be interchanged.

> **Theorem: global direct-sum support**<span id="thm:global" label="thm:global">\[thm:global\]</span> Under $$\sum_c\|U_c\|^2\leq\rho^2,$$ the exact centered scalar image is a disk of radius $$R_{\rm glob}=\rho\left(\sum_c\lambda_c^*G_c\lambda_c\right)^{1/2}.$$

> **Proof** In the direct-sum Hilbert space set $g_\oplus=\bigoplus_cg_c$ and $U_\oplus=\bigoplus_cU_c$. The scalar is $\langle U_\oplus,g_\oplus\rangle$. The one-functional ball image is the disk of radius $\rho\|g_\oplus\|$; its reverse realization is $U_\oplus=(\overline{d}/\|g_\oplus\|^2)g_\oplus$ when $g_\oplus\neq0$.

# Exact comparison with tagged marginals

The external-copy or marginal triangle estimate gives $$R_{\rm tag}:=\sum_c\rho_c\sum_b|\lambda_{cb}|\,\|v_{cb}\|.$$

> **Theorem: dominance and equality**<span id="thm:equality" label="thm:equality">\[thm:equality\]</span> One always has $R\leq R_{\rm tag}$. Equality holds exactly when, for every group with $\rho_c>0$, all nonzero vectors $\lambda_{cb}v_{cb}$ lie on one common nonnegative real ray. Groups with $\rho_c=0$ impose no condition.

> **Proof** For each $c$, apply the triangle inequality to $g_c=\sum_b\lambda_{cb}v_{cb}$ and multiply by $\rho_c$. The equality condition for a finite sum in a complex Hilbert space is precisely that all nonzero summands are nonnegative real multiples of one vector. Since every group deficit is nonnegative, equality after summing occurs exactly when each positive-$\rho_c$ group has equality.

Three endpoints are instructive. Orthogonal unit probes with equal weights give exact radius $\sqrt2\rho$ versus tagged radius $2\rho$. Positively aligned probes attain equality. Repeated probes $v_1=v_2=v\neq0$ with weights $(1,-1)$ give $$g=0,\qquad r=0,\qquad r_{\rm tag}=2\rho\|v\|.$$ Thus fixed marginal norms do not determine even the order of magnitude of the true shared-lane support radius.

# Exact certificate

The finite certificate contains orthogonal, aligned, and exact-cancellation groups. Their independent exact radius is $4$, while the tagged radius is $54/5$. It also freezes a target reverse realization, affine zero and positive-margin cases, a global radius squared of $20$, and a Gaussian-rational orientation check. The independent checker imports no producer and rejects nine typed, semantic, and digest-rebound attacks. A separate stress test verifies $100$ weighted families, including $52$ equality and eight exact-cancellation cases.

# Route boundary and conclusion

TPC-249 removes the tagged-copy triangle loss at the exact structural level. The remaining question is no longer which joint set or weighted scalar is correct: it is how large the literal quadratic forms $\lambda_c^*G_c\lambda_c$ are on the V59 source. No theorem here bounds those forms asymptotically. Therefore $$\texttt{ARITHMETIC\_L2=NONE},\qquad
 \texttt{FULL\_GATE\_B=OPEN},\qquad
 \texttt{STRICT\_1\_OVER\_400=UNPAID}.$$

The next robust step is to bound the exact Gram quadratic from computable diagonal and coherence data, and to test the sharpness of every such bound before returning to the literal longitudinal/transverse source decomposition.

**Maximum claim.** `PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION`.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc248,
  author = {Liang Wang},
  title = {Shared-Lane Gram Ellipsoids and Exact Joint Covariance Geometry},
  year = {2026},
  note = {TPC-248 committed repository paper}
}

@misc{tpc247,
  author = {Liang Wang},
  title = {Literal V59 Source-Operator Two-Lane Block Attachment},
  year = {2026},
  note = {TPC-247 committed repository paper}
}
```

# Non-content font-mapping input (preserved command)

Original TeX line 7: glyphtounicode.tex, SHA-256 395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851. This audited PDF glyph-to-Unicode map is not manuscript content. Its command is retained without executing TeX or expanding the mapping table.

``` {.latex}
\input{glyphtounicode}
```

<!-- SOURCE_BODY_END -->
