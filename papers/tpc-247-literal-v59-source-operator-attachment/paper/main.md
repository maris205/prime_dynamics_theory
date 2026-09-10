# Literal V59 Source-Operator Two-Lane Block Attachment\ Exact covariance and the external-copy norm obstruction

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology, Wuhan, China
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The V59 twin-prime Gate-B scalar was known as a signed four-packet remainder, while the recent covariance route required a literal two-lane coefficient attachment. We construct such an attachment directly on the finite physical source-index space. The complete prime weight, unit masks, deleted diagonal, kernel orientation, and real physical coefficients are packaged in one operator $A_x$, giving the exact identity $\mathfrak C_x=\left\langle w,A_x\beta\right\rangle$. Any declared disjoint source partition then gives an exactly-once ordered block decomposition. Tagged external copies turn the block sum into one Hilbert covariance. This positive result comes with an exact obstruction: for $m$ input blocks the copied output lane has squared norm $m\|w\|^2$, and separating the input blocks can remove cancellation present in $A_x\beta$. Thus the physical-index attachment is exact but does not supply the norm-payable primitive-frequency attachment needed for the hard-window theorem. An exact-rational certificate independently replays every admissible triple and the two norm failures. No arithmetic $L^2$ estimate or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# The source-attachment problem

The frozen V59 record reduces the open analytic gate to the scalar $$\mathfrak C_x=\sum_{q\in\mathcal Q}q
 \sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
 \beta(t)w(u)K_H(u-t)u_1(u\overline t;q),                 \label{eq:v59}$$ where $I_x=(x/2,x]\cap\mathbb Z$, $q$ is prime, $u_1(a;q)=\mathbf 1_{a\equiv1\pmod q}-1/(q-1)$, and the physical $\beta,w$ are real `\cite{v59record}`. TPC-243 provides a strong bilinear transfer once two coefficient vectors have been identified in one separated-frequency synthesis space `\cite{tpc243record}`. TPC-246 then gives sharp aggregate disk geometry, but explicitly assumes the relevant joint feasible family `\cite{tpc246record}`. Neither theorem constructs the literal V59 coefficient lanes.

Our narrower question is algebraic: can [\[eq:v59\]](main.tex#L46){reference-type="eqref" reference="eq:v59"} itself be written as a two-lane covariance without changing its physical coefficients? The answer is yes on the source-index space. The resulting representation also shows why existence is weaker than a usable hard-window attachment.

#### Conventions.

All complex Hilbert inner products are conjugate-linear in the first slot. The physical sequence $w$ is real. If it were replaced by a genuinely complex coefficient while the unconjugated factor $w(u)$ in [\[eq:v59\]](main.tex#L46){reference-type="eqref" reference="eq:v59"} were retained, the first Hilbert lane would be $\overline w$.

# Literal source operator

Let $\mathcal H_x=\mathbb C^{I_x}$. Define the finite matrix $$A_x(u,t)=\mathbf1_{u\ne t}\sum_{q\in\mathcal Q}
 q\,\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}K_H(u-t)
 \left(\mathbf1_{u\equiv t\pmod q}-\frac{1}{q-1}\right). \label{eq:A}$$ The two unit masks make $t^{-1}$ well defined modulo $q$, and $u t^{-1}\equiv1$ exactly when $u\equiv t$. Consequently [\[eq:A\]](main.tex#L74){reference-type="eqref" reference="eq:A"} is a repackaging of the full kernel in [\[eq:v59\]](main.tex#L46){reference-type="eqref" reference="eq:v59"}; it does not alter the outer $q$, diagonal deletion, or kernel orientation.

> **Proposition: Literal two-lane source operator**<span id="prop:operator" label="prop:operator">\[prop:operator\]</span> For the real physical V59 lanes, $$\mathfrak C_x=\left\langle w,A_x\beta\right\rangle_{\mathcal H_x}.$$ No Hermiticity or positivity of $A_x$ is required.

> **Proof** Expand the right side. Conjugate-linearity in the first slot gives $\sum_u\overline{w(u)}\sum_tA_x(u,t)\beta(t)$. Since $w$ is real, this is exactly [\[eq:v59\]](main.tex#L46){reference-type="eqref" reference="eq:v59"} after the unit-residue equivalence above.

The proposition is source-native in a precise sense: both vector coordinates are the literal physical integers in $I_x$. It is not yet an identification with primitive rational frequencies, and $A_x$ is not asserted to be a Gram matrix $T^*T$.

# Exactly-once hard blocks

Fix a finite disjoint partition $I_x=\bigsqcup_{b\in\mathcal B}I_b$ and let $P_b$ multiply by $\mathbf1_{I_b}$. Put $$\beta_b=P_b\beta,\qquad w_c=P_cw,\qquad A_{cb}=P_cA_xP_b.$$

> **Theorem: Exactly-once source blocks**<span id="thm:block" label="thm:block">\[thm:block\]</span> One has $$A_x=\sum_{b,c}A_{cb},\qquad
>  \mathfrak C_x=\sum_{b,c}\left\langle w_c,A_{cb}\beta_b\right\rangle.              \label{eq:block}$$ Every admissible triple $(q,t,u)$ in [\[eq:v59\]](main.tex#L46){reference-type="eqref" reference="eq:v59"} occurs in exactly one summand of [\[eq:block\]](main.tex#L112){reference-type="eqref" reference="eq:block"}.

> **Proof** The projections are self-adjoint, pairwise orthogonal, and sum to the identity. Hence $$\sum_{b,c}A_{cb}=\left(\sum_cP_c\right)A_x
>                     \left(\sum_bP_b\right)=A_x.$$ Because $A_{cb}\beta_b\in P_c\mathcal H_x$, orthogonality of the output supports gives the scalar identity. Finally every $t$ has one input label $b(t)$ and every $u$ has one output label $c(u)$. The complete summand for an admissible $(q,t,u)$ therefore lies in $(c(u),b(t))$ and nowhere else.

The disjoint hypothesis is essential for the literal “exactly once” wording. V59 also uses a smooth bounded-overlap partition of unity. That is an exact weighted pair partition, but one physical pair can occur in several weighted block pairs. We do not identify the two constructions.

# Tagged covariance and its exact toll

For each ordered pair $(b,c)$ introduce a tagged copy $\mathcal H_c^{(b,c)}\cong P_c\mathcal H_x$ and set $$\mathcal H_{\rm ext}=\bigoplus_{b,c}\mathcal H_c^{(b,c)},\quad
 \mathbf B=\bigoplus_{b,c}A_{cb}\beta_b,\quad
 \mathbf W=\bigoplus_{b,c}w_c.$$

> **Theorem: External-copy covariance and norm ledger**<span id="thm:norm" label="thm:norm">\[thm:norm\]</span> If $m=|\mathcal B|$, then $$\begin{aligned}
>  \left\langle \mathbf W,\mathbf B\right\rangle_{\mathcal H_{\rm ext}}&=\mathfrak C_x,\label{eq:cov}\\
>  \|\mathbf W\|^2&=m\|w\|^2,\label{eq:wnorm}\\
>  \|\mathbf B\|^2&=\sum_{b,c}\|A_{cb}\beta_b\|^2.\label{eq:bnorm}\end{aligned}$$ There is no general equality between [\[eq:bnorm\]](main.tex#L151){reference-type="eqref" reference="eq:bnorm"} and $\|A_x\beta\|^2$.

> **Proof** Orthogonality of the tags turns each direct-sum inner product and norm into the sum of its coordinate values. Equation [\[eq:cov\]](main.tex#L149){reference-type="eqref" reference="eq:cov"} is then Theorem [\[thm:block\]](main.tex#L108){reference-type="ref" reference="thm:block"}. Every $w_c$ appears once for each of the $m$ input blocks, proving [\[eq:wnorm\]](main.tex#L150){reference-type="eqref" reference="eq:wnorm"}; [\[eq:bnorm\]](main.tex#L151){reference-type="eqref" reference="eq:bnorm"} is immediate.
>
> For the final assertion, use singleton blocks on three coordinates and $$A=\begin{pmatrix}0&1&-1\\0&0&0\\0&0&0\end{pmatrix},
>  \qquad \beta=(0,1,1)^T.$$ Then $A\beta=0$, but the two nonzero tagged block outputs are $+1$ and $-1$. Their squared direct-sum norm is $2$. This is an exact counterexample.

The obstruction has two parts. The $w$ lane pays a compulsory factor $\sqrt m$ if every ordered block pair is retained. The $B$ lane moves cross-input-block cancellation out of the norm. Applying a near-isometry error to these lanes without paying both effects would therefore be invalid.

# Certificate, route boundary, and conclusion

The certificate uses six physical indices, primes $5$ and $7$, three hard blocks, nonconstant real $\beta,w$, and the rational kernel $K(h)=1/(1+|h|)$. It reconstructs every matrix entry, compares the direct and block scalars, and counts each admissible $(q,t,u)$ exactly once. The independent checker imports no producer code and rejects type, digest, coverage, norm, and arithmetic-promotion mutations. A separate stress test checks five partitions, the complex-$w$ orientation, and the block-norm cancellation example.

The exact maximum claim is $$\texttt{PROVED\_STRUCTURAL\_L1\_LITERAL\_V59\_SOURCE\_OPERATOR\_}
\texttt{ATTACHMENT\_WITH\_NORM\_OBSTRUCTION}.$$ The primitive-frequency attachment, the TPC-243 synthesis map, a TPC-244 common multiplier, source product realizability, arithmetic $L^2$, fixed-atom credit, strict $1/400$, full Gate B, and the twin-prime conclusion remain open. The next minimal problem is no longer whether a physical two-lane pairing exists. It is to characterize the joint covariance family generated when the same output lane $w_c$ is shared by all input-block probes.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{v59record,
  author = {Prime Dynamics Theory Project},
  title = {V59 Polarized Local BDH Scalar Compiler},
  year = {2026},
  note = {Committed repository research record}
}

@misc{tpc243record,
  author = {Wang, Liang},
  title = {Hard-Window Near-Isometry and Signed Bilinear Transfer},
  year = {2026},
  note = {TPC-243 committed repository paper}
}

@misc{tpc246record,
  author = {Wang, Liang},
  title = {Weighted Covariance-Disk Reassembly and Hard-Window Margins},
  year = {2026},
  note = {TPC-246 committed repository paper}
}
```

<!-- SOURCE_BODY_END -->
