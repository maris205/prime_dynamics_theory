# Shared-Lane Gram Ellipsoids and Exact Joint Covariance Geometry

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

A source-index decomposition of the finite V59 twin-prime Gate-B scalar exposes, inside each fixed output block, several probe vectors paired with one shared physical output lane. Independent marginal disks therefore do not describe the source-valid joint family. We determine that family exactly. For the analysis operator $V^*W=(\langle v_i,W\rangle)_i$ and Gram matrix $G=V^*V$, the radius-$\rho$ ball maps onto $$\{y\in\operatorname{ran}G:y^*G^\dagger y\leq \rho^2\}.$$ We classify the exact-sphere image by the orthogonal slack $\operatorname{ker}V^*$, give the entrywise-conjugate physical covariance form, and distinguish independent group budgets from one global Hilbert budget. Repeated probes collapse two unit-disk marginals to a diagonal disk, while orthogonal probes give a Euclidean ball rather than a bidisk. These are exact structural results; they provide no arithmetic cancellation, strict $1/400$ payment, full Gate B, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# The source-native joint object

TPC-247 writes the physical scalar as a finite source covariance and, for a declared disjoint hard partition, obtains $$A_{cb}=P_cA_xP_b,\qquad \beta_b=P_b\beta,\qquad w_c=P_cw,
 \qquad
 C_x=\sum_{c,b}\langle w_c,A_{cb}\beta_b\rangle.$$ For fixed $c$, set $$v_{cb}:=A_{cb}\beta_b\in P_c\mathcal H_x.$$ The vectors $(v_{cb})_b$ are all observed by the same $w_c$; no independently variable lane $w_{cb}$ appears in the physical source. Tagged direct-sum copies reproduce the scalar but repeat $w_c$ once for every $b$, which is why their Cartesian geometry is not automatically source-valid `\cite{tpc247,tpc246}`.

We therefore solve the following finite-dimensional problem before applying any weighted reassembly. Throughout, complex Hilbert inner products are conjugate-linear in the first slot.

# Exact analysis-map ellipsoid

Let $v_1,\ldots,v_m$ be ordered vectors in a finite-dimensional complex Hilbert space $\mathcal H$. Define $$V:\mathbb C^m\longrightarrow\mathcal H,\qquad Va=\sum_{i=1}^m a_iv_i,
 \qquad G=V^*V,$$ so $G_{ij}=\langle v_i,v_j\rangle$. The Moore–Penrose inverse is denoted by $G^\dagger$.

> **Theorem: ball image and minimum preimage**<span id="thm:ball" label="thm:ball">\[thm:ball\]</span> For every $\rho\geq0$, $$V^*\{W\in\mathcal H:\|W\|\leq\rho\}
>  =\left\{y\in\operatorname{ran}G:y^*G^\dagger y\leq\rho^2\right\}.$$ For each $y\in\operatorname{ran}G$, the vector $$W_0=VG^\dagger y$$ is the unique minimum-norm preimage and $$\min_{V^*W=y}\|W\|^2=\|W_0\|^2=y^*G^\dagger y.$$

> **Proof** In finite dimension, $\operatorname{ran}V^*=\operatorname{ran}(V^*V)=\operatorname{ran}G$. If $y\in\operatorname{ran}G$, the Moore–Penrose identities give $$V^*W_0=GG^\dagger y=y.$$ Furthermore, $$\begin{aligned}
>  \|W_0\|^2
>  &=\langle VG^\dagger y,VG^\dagger y\rangle\\
>  &=(G^\dagger y)^*G(G^\dagger y)
>  =y^*G^\dagger y.\end{aligned}$$ Here we used that $G$ and $G^\dagger$ are Hermitian and that $GG^\dagger y=y$. Every other preimage is uniquely $W_0+k$ with $k\in\operatorname{ker}V^*$. Since $W_0\in\operatorname{ran}V=(\operatorname{ker}V^*)^\perp$, $$\|W_0+k\|^2=\|W_0\|^2+\|k\|^2.$$ The minimum formula and both inclusions in the ball identity follow. The same argument includes rank-zero $G$ and $\rho=0$.

The range condition is essential when the probes are linearly dependent: the quadratic inequality by itself must not be interpreted on all of $\mathbb C^m$.

# Exact spheres and physical orientation

> **Theorem: orthogonal-slack dichotomy**<span id="thm:sphere" label="thm:sphere">\[thm:sphere\]</span> Let $S_\rho=\{W:\|W\|=\rho\}$. If $\operatorname{ker}V^*\neq\{0\}$, then $$V^*S_\rho=\{y\in\operatorname{ran}G:y^*G^\dagger y\leq\rho^2\}.$$ If $\operatorname{ker}V^*=\{0\}$, then $$V^*S_\rho=\{y\in\operatorname{ran}G:y^*G^\dagger y=\rho^2\}.$$ Both formulas remain valid for $\rho=0$.

> **Proof** For a point of minimum energy $e=y^*G^\dagger y\leq\rho^2$, choose a unit $k\in\operatorname{ker}V^*$ and replace $W_0$ by $W_0+\sqrt{\rho^2-e}\,k$. This reaches the sphere without changing $y$. If the kernel is zero, $W_0$ is the only preimage, so sphere membership is equivalent to $e=\rho^2$.

The V59 physical scalar uses the opposite orientation $$z_i=\langle W,v_i\rangle=\overline{\langle v_i,W\rangle}
 =\overline{y_i}.$$

> **Corollary: physical covariance ellipsoid**<span id="cor:physical" label="cor:physical">\[cor:physical\]</span> The physical ball image is $$\left\{z\in\operatorname{ran}\overline G:
>  z^*(\overline G)^\dagger z\leq\rho^2\right\}.$$ The sphere classification is Theorem [\[thm:sphere\]](main.tex#L144){reference-type="ref" reference="thm:sphere"} with $G$ replaced by $\overline G$.

> **Proof** Entrywise conjugation carries $\operatorname{ran}G$ onto $\operatorname{ran}\overline G$, commutes with the Moore–Penrose inverse, and conjugates the real nonnegative energy $y^*G^\dagger y$ to the displayed expression.

# Grouped budgets are not interchangeable

For output groups $c$, let $V_c^*W_c=y_c$ and $G_c=V_c^*V_c$.

> **Theorem: product and global budgets**<span id="thm:groups" label="thm:groups">\[thm:groups\]</span> For explicitly independent constraints $\|W_c\|\leq\rho_c$, the joint image is the Cartesian product $$\prod_c\{y_c\in\operatorname{ran}G_c:y_c^*G_c^\dagger y_c\leq\rho_c^2\}.$$ For one global direct-sum constraint $\sum_c\|W_c\|^2\leq\rho^2$, the exact image is instead $$\left\{(y_c)_c: y_c\in\operatorname{ran}G_c,\quad
>  \sum_c y_c^*G_c^\dagger y_c\leq\rho^2\right\}.$$

> **Proof** The first domain is a Cartesian product and the map acts coordinatewise. For the second domain, Theorem [\[thm:ball\]](main.tex#L99){reference-type="ref" reference="thm:ball"} supplies the minimum squared norm for each group; direct-sum orthogonality adds these minima. Independent minimum preimages realize every point satisfying the summed inequality.

Thus “local ellipsoid” does not by itself determine a cross-group feasible set. The budget domain is part of the theorem.

# Sharp adversarial fixtures

First take $v_1=v_2=e_1$ and $\rho=1$. Then $$G=\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
 G^\dagger=\frac14\begin{pmatrix}1&1\\1&1\end{pmatrix},$$ and the exact image is $$\{(t,t):|t|\leq1\}.$$ Each coordinate marginal is the unit disk, but $(1,0)$ is not jointly feasible. This refutes the bidisk promotion at rank one.

Second take $v_1=e_1,v_2=e_2$. The image is $\{(y_1,y_2):|y_1|^2+|y_2|^2\leq1\}$, again strictly smaller than the bidisk. If the ambient space contains an unused $e_3$, the exact unit sphere maps onto that whole solid ball; without $e_3$, it maps only onto its boundary.

Finally, two scalar groups with a global unit budget have local unit-disk marginals, but $(1,1)$ has minimum global energy $2$ and is forbidden. These examples isolate three different errors: ignoring Gram range, ignoring joint energy, and ignoring orthogonal sphere slack.

# Certificate and route boundary

The exact certificate freezes a rank-one Gram pair, two full-rank Gram pairs, the sphere dichotomy, a global-budget obstruction, a zero-radius boundary, and a Gaussian-rational orientation fixture. An independent implementation reconstructs the Moore–Penrose identities and rejects typed, semantic, and digest-rebound mutations. A separate stress program checks seven integer probe matrices and $87$ exact minimum-energy samples.

For TPC-247, Theorem [\[thm:ball\]](main.tex#L99){reference-type="ref" reference="thm:ball"} now classifies the vector $(\langle v_{cb},W_c\rangle)_b$ for each fixed $c$. It does not estimate the actual Gram matrices, attach primitive rational frequencies, or prove that a longitudinal center dominates any transverse radius. Consequently $$\texttt{ARITHMETIC\_L2=NONE},\qquad
 \texttt{FULL\_GATE\_B=OPEN},\qquad
 \texttt{STRICT\_1\_OVER\_400=UNPAID}.$$

The next exact contraction is now forced: combine weighted probes inside each shared output lane, compute the sharp group support radius from its Gram matrix, and only then sum across output blocks.

# Conclusion

The joint shared-lane geometry is an ellipsoid, not a product of marginal disks. Its range, energy, sphere filling, complex orientation, and grouped budget are all exact, including degenerate ranks and zero radius. This removes TPC-247’s first structural ambiguity while preserving its arithmetic firewall.

**Maximum claim.** `PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET`.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc247,
  author = {Liang Wang},
  title = {Literal V59 Source-Operator Two-Lane Block Attachment},
  year = {2026},
  note = {TPC-247 committed repository paper}
}

@misc{tpc246,
  author = {Liang Wang},
  title = {Weighted Covariance-Disk Reassembly and Hard-Window Margins},
  year = {2026},
  note = {TPC-246 committed repository paper}
}
```

# Non-content font-mapping input (preserved command)

Original TeX line 8: glyphtounicode.tex, SHA-256 395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851. This audited PDF glyph-to-Unicode map is not manuscript content. Its command is retained without executing TeX or expanding the mapping table.

``` {.latex}
\input{glyphtounicode}
```

<!-- SOURCE_BODY_END -->
