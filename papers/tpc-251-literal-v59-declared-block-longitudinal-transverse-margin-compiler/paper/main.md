# A Declared-Block Longitudinal–Transverse Margin Compiler\ for the Literal V59 Scalar

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology, Wuhan, China; liang.wang@hust.edu.cn
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We give an exact longitudinal–transverse margin compiler for the literal V59 source scalar after an exhaustive nonempty coordinate partition has been declared. The literal block weights are one, so the probes contract inside each physical output lane before projection. Projection onto the flat unit of each declared block yields an exact scalar decomposition; the transverse remainder is bounded first by its true block norms and then by a projected coherence envelope inherited from TPC-250. Any independently certified external scalar therefore obeys a computable lower margin, and strict longitudinal dominance implies nonvanishing. An exact rational $8$-coordinate operator replay gives $C_{\rm long}=11/2$, $Q_{\rm trans}=-1$, $C_x=9/2$, and $R_{\rm trans}=R_{\rm coh}=1$; with $(F,E)=(4,1/2)$, the external bound and the lower margin $4$ are attained. Equality is insufficient for nonvanishing. The partition and flat direction are modeling choices, and no actual V59 coherence asymptotic or arithmetic advance is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Source lock and scope

Let $H=\mathbb{C}^I$, where $I$ is finite and nonempty, with inner product conjugate-linear in the first argument. Declare an exhaustive disjoint partition $$I=\bigsqcup_d J_d, \qquad J_d\ne\varnothing,$$ and let $P_d$ be its coordinate projections. The same complete partition indexes source blocks $b$ and output blocks $c$. From the literal TPC-247 source operator we import only `\cite{tpc247}` $$\beta_b=P_b\beta,\quad A_{cb}=P_cA_xP_b,\quad
 v_{cb}=A_{cb}\beta_b,\quad w_c=P_cw.$$ The actual scalar has $\lambda_{cb}=1$. Hence $$\label{eq:literal}
 g_c:=\sum_bv_{cb}=P_cA_x\beta,
 \qquad C_x=\langle w,A_x\beta\rangle=\sum_c\langle w_c,g_c\rangle.$$

The hard partition is a modeling choice. Once it is declared, define the block-flat unit $$u_c=|J_c|^{-1/2}{\bf 1}_{J_c}.$$ This unit is canonical only relative to $J_c$. It is not a V59-canonical direction, and it is not the TPC-219 longitudinal object `\cite{tpc219}`. These distinctions prevent the finite decomposition below from acquiring an unproved arithmetic interpretation.

# The declared-block compiler

Set $$a_c=\langle u_c,w_c\rangle,\quad b_c=\langle u_c,g_c\rangle,\quad
 w_c^\perp=w_c-a_cu_c,$$ and, probe by probe, $$m_{cb}=\langle u_c,v_{cb}\rangle,\qquad
 v_{cb}^\perp=v_{cb}-m_{cb}u_c,\qquad
 g_c^\perp=\sum_bv_{cb}^\perp.$$ Let $G_c(bb')=\langle v_{cb},v_{cb'}\rangle$. For $d_{cb}=\lVert v_{cb}^\perp\rVert$ define $$D_c=\sum_bd_{cb}^2,\qquad L_c=\sum_bd_{cb}.$$ If fewer than two $d_{cb}$ are nonzero, set $\mu_c=0$. Otherwise set $$\mu_c=\max_{\substack{b\ne b'\\d_{cb}d_{cb'}>0}}
 \frac{|\langle v_{cb}^\perp,v_{cb'}^\perp\rangle|}{d_{cb}d_{cb'}}.$$ This is exactly the total empty-pair convention needed to apply TPC-250 to the projected family `\cite{tpc250}`. Finally put $$\label{eq:upper}
 U_c=\sqrt{D_c+\mu_c(L_c^2-D_c)}\ge0.$$

> **Theorem: Literal declared-block margin compiler**<span id="thm:compiler" label="thm:compiler">\[thm:compiler\]</span> Define $$\begin{aligned}
>  C_{\rm long}&=\sum_c\overline{a_c}b_c,&
>  Q_{\rm trans}&=\sum_c\langle w_c^\perp,g_c^\perp\rangle,\\
>  R_{\rm trans}&=\sum_c\lVert w_c^\perp\rVert\lVert g_c^\perp\rVert,&
>  R_{\rm coh}&=\sum_c\lVert w_c^\perp\rVert U_c.\end{aligned}$$ Then $$\label{eq:chain}
>  C_x=C_{\rm long}+Q_{\rm trans},\qquad
>  |C_x-C_{\rm long}|\le R_{\rm trans}\le R_{\rm coh}.$$ Moreover, the projected Gram matrix is exactly $$\label{eq:gram}
>  G_c^\perp(bb')=G_c(bb')-\overline{m_{cb}}m_{cb'}.$$

> **Proof** Exhaustiveness gives $\sum_bP_b=\sum_cP_c=I$, so [\[eq:literal\]](main.tex#L62){reference-type="eqref" reference="eq:literal"} follows without tagged copies. Both $w_c^\perp$ and every $v_{cb}^\perp$ are orthogonal to $u_c$. Therefore $$\langle w_c,g_c\rangle=\overline{a_c}b_c+\langle w_c^\perp,g_c^\perp\rangle,$$ where the conjugation of $a_c$ is forced by the first-slot convention. Summation proves the identity in [\[eq:chain\]](main.tex#L115){reference-type="eqref" reference="eq:chain"}.
>
> Expanding the two orthogonal projections and using $\langle v_{cb},u_c\rangle=\overline{m_{cb}}$ gives [\[eq:gram\]](main.tex#L120){reference-type="eqref" reference="eq:gram"}. Applying the TPC-250 upper Gram bound to the projected probes with all weights one gives $\lVert g_c^\perp\rVert^2\le U_c^2$. Equation [\[eq:upper\]](main.tex#L102){reference-type="eqref" reference="eq:upper"} chooses the nonnegative root, hence $\lVert g_c^\perp\rVert\le U_c$. Cauchy–Schwarz followed by the triangle inequality now proves both inequalities in [\[eq:chain\]](main.tex#L115){reference-type="eqref" reference="eq:chain"}.

The theorem is a pointwise enclosure for fixed source data. It does not claim that varying an undeclared source parameter fills a disk, much less an exact disk image.

# External margins and the strict endpoint

> **Corollary: Conditional external compiler**<span id="cor:external" label="cor:external">\[cor:external\]</span> Let $F$ be any independently certified scalar, and let $E\ge0$ satisfy $|F-C_x|\le E$. Then $$\label{eq:external}
>  |F-C_{\rm long}|\le R_{\rm coh}+E,\qquad
>  |F|\ge\left(|C_{\rm long}|-R_{\rm coh}-E\right)_{+}.$$ Consequently, $|C_{\rm long}|>R_{\rm coh}+E$ implies $F\ne0$.

> **Proof** The first estimate follows from $F-C_{\rm long}=(F-C_x)+(C_x-C_{\rm long})$ and Theorem [\[thm:compiler\]](main.tex#L106){reference-type="ref" reference="thm:compiler"}. Reverse triangle gives the second estimate after intersection with zero. A strict positive lower endpoint proves the final claim.

The hypothesis $|F-C_x|\le E$ is an independent input. In particular, this paper does not obtain it automatically from the conditional synthesis interface of TPC-243 `\cite{tpc243}`.

> **Proposition: Equality obstruction**<span id="prop:equality" label="prop:equality">\[prop:equality\]</span> In $\mathbb R^4$, let $$u=\tfrac12(1,1,1,1),\qquad
>  t=\tfrac12(1,-1,1,-1),\qquad w=u+t,\quad g=u-t.$$ Then $u,t$ are orthonormal and $$C_{\rm long}=1,\qquad Q_{\rm trans}=-1,\qquad
>  R_{\rm trans}=1,\qquad \langle w,g\rangle=0.$$ Thus equality $|C_{\rm long}|=R_{\rm trans}$ cannot imply nonvanishing.

> **Proof** The two longitudinal coefficients equal one, while the transverse vectors are $t$ and $-t$. Their covariance is $-1$ and their norm product is one, so the two scalar contributions cancel exactly.

# Exact finite operator replay

The release certificate realizes a rational $8\times8$ operator. There are two blocks of size four; $\beta$ is supported at the first coordinate of each block. In each block use $$u=\tfrac12(1,1,1,1),\quad
 t_1=\tfrac12(1,-1,1,-1),\quad
 t_2=\tfrac12(1,1,-1,-1).$$ The two selected columns of $A$ are assembled from $$\begin{aligned}
 v_{00}&=\tfrac12(1,1,1,1)+\tfrac35t_1,&
 v_{01}&=\tfrac14(1,1,1,1)+\tfrac45t_2,\\
 v_{10}&=\tfrac13(1,1,1,1)+t_1,&
 v_{11}&=\tfrac23(1,1,1,1)-t_1.\end{aligned}$$ Take $$w_0=\tfrac12(1,1,1,1)-\tfrac35t_1-\tfrac45t_2,\qquad
 w_1=(1,1,1,1).$$

<div id="tab:fixture">

| $c$ | $D_c$ | $L_c$ | $\mu_c$ | $U_c$ | $\lVert g_c^\perp\rVert$ | $\lVert w_c^\perp\rVert$ |
|:---:|:-----:|:-----:|:-------:|:-----:|:------------------------:|:------------------------:|
| $0$ |  $1$  | $7/5$ |   $0$   |  $1$  |            $1$           |            $1$           |
| $1$ |  $2$  |  $2$  |   $1$   |  $2$  |            $0$           |            $0$           |

: Exact projected data for the synthetic finite operator replay. The second block has the largest coherence upper but contributes no transverse radius because both physical transverse vectors vanish after contraction or lane projection.

</div>

Direct rational calculation gives $$C_{\rm long}=\frac{11}{2},\quad Q_{\rm trans}=-1,\quad
 C_x=\frac92,\quad R_{\rm trans}=R_{\rm coh}=1.$$ For $F=4$ and $E=1/2$, both sides of the first estimate in [\[eq:external\]](main.tex#L153){reference-type="eqref" reference="eq:external"} equal $3/2$, and the strict lower margin is $4$. The replay is explicitly labeled *synthetic exact finite operator replay, not a literal V59 arithmetic instance*. It verifies the compiler and supplies no asymptotic evidence.

The real replay cannot detect a missing complex conjugation. The certificate therefore adds a Gaussian-rational two-coordinate fixture. It independently checks that $\overline{a} b=1-i$ rather than $ab=-1+i$, and that one off-diagonal projected Gram entry is $i$ only when $G_{12}-\overline{m_1}m_2$ is used. Singleton and one-active-probe fixtures also verify $U=0$ and the $\mu=0$ empty-pair convention.

# Computational trust boundary and limitations

The JSON producer uses exact rational arithmetic. The checker imports no producer code: it reparses canonical rationals, rejects duplicate keys, audits exact integer types and exhaustive blocks, recomputes the full operator replay, and rejects fifteen typed, semantic, stale-digest, duplicate-key, and digest-rebound mutations. A deterministic stress program checks $160$ exact-rational declared partitions and probe families in normal and optimized Python modes. None of these finite checks proves an asymptotic statement.

The remaining mathematical gap is source-specific. The theorem neither controls the actual V59 projected coherences nor proves that the declared longitudinal term dominates every transverse and external loss. In particular, full Gate B and its global strict $1/400$ endpoint remain unpaid.

**Claim firewall.** The hard partition is an exhaustive-nonempty modeling choice, and the flat direction is relative only to its declared block. The TPC-243 external error is conditional, not automatic. Actual projected V59 coherence and payable longitudinal dominance are open. Arithmetic advance is no; fixed-atom credit is zero; L2 and the twin-prime result are none. Full Gate B is open, and its global strict $1/400$ endpoint is unpaid.

**Maximum supported claim.**

`PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER`

# Conclusion

The literal V59 source scalar admits an exact longitudinal–transverse split relative to every declared exhaustive nonempty coordinate partition. The projected Gram subtraction and TPC-250 coherence bound turn that split into a total, computable conditional margin, while the equality fixture identifies the necessary strict endpoint. The result is structural L1 progress only: the block-flat direction remains a modeling choice, the external error remains conditional, and the actual arithmetic margin remains open. There is no Route A claim, arithmetic advance, fixed-atom credit, L2 result, Gate-B closure, or twin-prime conclusion.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc219,
  author = {Liang Wang},
  title = {Prime-Shell Longitudinal Ledger and the Exact P Collapse},
  year = {2026},
  note = {TPC-219 project-local repository paper}
}

@misc{tpc243,
  author = {Liang Wang},
  title = {Hard-Window Near-Isometry and Signed Bilinear Transfer},
  year = {2026},
  note = {TPC-243 project-local repository paper}
}

@misc{tpc247,
  author = {Liang Wang},
  title = {Literal V59 Source-Operator Two-Lane Block Attachment},
  year = {2026},
  note = {TPC-247 project-local repository paper}
}

@misc{tpc250,
  author = {Liang Wang},
  title = {Coherence-Controlled Gram Quadratic Bounds and Sharpness},
  year = {2026},
  note = {TPC-250 project-local repository paper, August 25, 2026}
}
```

<!-- SOURCE_BODY_END -->
