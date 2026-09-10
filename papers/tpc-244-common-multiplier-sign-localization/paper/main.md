# Common-Multiplier Sign Localization\ in Primitive Denominator Blocks

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology; Wuhan, China; liang.wang@hust.edu.cn
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We determine exactly where the outer sign of a common clustered multiplier can survive in a polarized two-lane covariance. In an orthogonal block direct sum, simultaneous multiplication of both lanes by $C_h$ produces the local factor $|C_h|^2$; hence every common blockwise unit phase is invisible to covariance and both lane norms. For nonorthogonal reassembly and real sign flips, we derive an exact graph-cut polynomial and prove that invariance under all sign patterns is equivalent to the vanishing of every symmetrized cross-block edge. Combining the direct-sum identity with the TPC-243 hard-window bilinear estimate bounds the difference between any two common sign patterns by $2\varepsilon\left\lVert W\right\rVert\left\lVert B\right\rVert$. The literal V59 interpretation remains conditional on the missing phasewise primitive two-lane coefficient attachment. Thus the result is a structural localization theorem and obstruction: the aggregate outer sign of $C_h$ cannot control the same-block main covariance, while internal Möbius cancellation in $|C_h|$ remains untouched.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The preceding hard-window theorem transports an already defined coefficient covariance to the physical interval with a relative Gram error. The next question is therefore not another unsigned energy estimate: it is whether the literal Möbius–log cluster coefficient can supply a signed principal term in the two polarized coefficient lanes.

The answer depends on where the multiplier is placed. If the same scalar $C_h$ multiplies both lanes in one orthogonal denominator block, conjugate linearity forces the product $\overline{C_h}C_h=|C_h|^2$. The aggregate outer sign or phase disappears exactly. This does not make the arithmetic tail unsigned: the Möbius signs inside the sum defining $C_h$ can still alter its magnitude. It only rules out a second, external sign mechanism.

We prove three statements. First, common blockwise phases preserve the exact coefficient covariance and both norms. Second, for arbitrary linear embeddings into a common ambient Hilbert space, the complete dependence on real sign flips is a finite Walsh polynomial indexed by the edges of the block graph. Third, when the direct-sum coefficients enter the hard-window synthesis of TPC-243, all residual dependence on a common sign pattern is bounded by two copies of the Gram error.

The contribution is deliberately typed as structural. Current sources retain one literal $C_h$ in each packet and canonical primitive frequency coordinates, but they do not yet identify the literal V59 source sequences with two such coefficient lanes in one common synthesis map. No arithmetic cancellation, coefficient norm bound, or twin-prime conclusion is claimed.

# Source lock and conventions

All Hilbert-space inner products are conjugate-linear in the first slot. The literal clustered coefficient inherited from the V59 source chain is $$C_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}
       \frac{\mu(d)\log d}{d},
\qquad
H=x^{21/32},\quad Q=x^{1/3},\quad U=x^{133/400}.$$ It is real. Reduced rational-frequency clustering produces one coefficient per primitive denominator block, and primitive representatives give canonical exactly-once coefficient coordinates. The frozen packet kernels retain the same outer $C_h$ for every phase label.

Those facts do not by themselves produce two source-native lanes. In particular, the current source compiler leaves open a literal map from the V59 $\beta,w$ sequences to primitive vectors $b_h,w_h$ in a common synthesis space. We therefore separate the unconditional finite-dimensional theorems from their conditional V59 interpretation.

For a finite index set $\mathcal A$, write $$\mathcal H=\bigoplus_{h\in\mathcal A}\mathcal H_h.$$ The direct sum is orthogonal. Later, $J_h:\mathcal H_h\to\mathcal K$ denotes an arbitrary linear embedding into one ambient Hilbert space; it is not assumed isometric.

An “outer phase change” means $C_h\mapsto\eta_hC_h$ with $|\eta_h|=1$ after $C_h$ has been formed. It is not a change of any individual Möbius summand inside $C_h$.

# Common-multiplier phase blindness

> **Theorem: orthogonal common-multiplier identity** For $b_h,w_h\in\mathcal H_h$ and $C_h\in\mathbb C$, put $$B=\bigoplus_{h\in\mathcal A}C_hb_h,
> \qquad
> W=\bigoplus_{h\in\mathcal A}C_hw_h.$$ Then $$\begin{aligned}
> \left\langle W,B\right\rangle&=\sum_{h\in\mathcal A}|C_h|^2\left\langle w_h,b_h\right\rangle,\label{eq:cov}\\
> \left\lVert B\right\rVert^2&=\sum_{h\in\mathcal A}|C_h|^2\left\lVert b_h\right\rVert^2,\qquad
> \left\lVert W\right\rVert^2=\sum_{h\in\mathcal A}|C_h|^2\left\lVert w_h\right\rVert^2.\label{eq:norms}\end{aligned}$$ Consequently, replacing $C_h$ by $\eta_hC_h$ simultaneously in both lanes, with $|\eta_h|=1$, changes none of these quantities.

> **Proof** Distinct direct-sum blocks are orthogonal. On one block, $$\left\langle C_hw_h,C_hb_h\right\rangle
> =\overline{C_h}C_h\left\langle w_h,b_h\right\rangle
> =|C_h|^2\left\langle w_h,b_h\right\rangle.$$ Summing proves [\[eq:cov\]](sections/3_direct_sum.tex#L12){reference-type="eqref" reference="eq:cov"}; taking equal lane vectors proves [\[eq:norms\]](sections/3_direct_sum.tex#L14){reference-type="eqref" reference="eq:norms"}. A common unit phase has unit modulus and therefore leaves every factor $|C_h|^2$ unchanged.

The empty family and one-block family are included. Zero multipliers simply remove blocks. The conclusion fails in general if the lanes carry different multipliers: if $A_h$ multiplies $w_h$ and $D_h$ multiplies $b_h$, the local factor is $\overline{A_h}D_h$ and its phase is visible.

For the literal real $C_h$, a simultaneous external sign flip is therefore invisible. By contrast, changing a Möbius sign inside the defining sum can change $|C_h|$, so the theorem does not erase or estimate internal arithmetic cancellation.

# Nonorthogonal reassembly as a sign cut

The direct-sum identity identifies the principal block term. To locate every possible failure of phase blindness, let $J_h:\mathcal H_h\to\mathcal K$ be linear maps and, for real $C_h$ and $s_h\in\{-1,1\}$, define $$W(s)=\sum_hs_hC_hJ_hw_h,
\qquad
B(s)=\sum_hs_hC_hJ_hb_h,
\qquad Q(s)=\left\langle W(s),B(s)\right\rangle.$$ Put $$M_{hk}=\left\langle J_hw_h,J_kb_k\right\rangle,\qquad
D=\sum_hC_h^2M_{hh},\qquad
S_{hk}=C_hC_k(M_{hk}+M_{kh})\quad(h<k).$$

> **Theorem: exact sign-cut localization** For every sign pattern $s$, $$\begin{aligned}
> Q(s)&=D+\sum_{h<k}s_hs_kS_{hk},\label{eq:walsh}\\
> Q(s)-Q(\mathbf 1)&=-2\sum_{\substack{h<k\\s_h\ne s_k}}S_{hk}.\label{eq:cut}\end{aligned}$$ Moreover, $Q$ is constant on the complete sign cube if and only if $S_{hk}=0$ for every unordered pair.

> **Proof** Expand $Q(s)$ over ordered pairs. The diagonal has $s_h^2=1$. Pairing the two directed terms for $h<k$ yields [\[eq:walsh\]](sections/4_sign_cut.tex#L22){reference-type="eqref" reference="eq:walsh"}. Relative to the all-positive pattern, precisely the edges joining opposite signs reverse, so [\[eq:cut\]](sections/4_sign_cut.tex#L23){reference-type="eqref" reference="eq:cut"} follows.
>
> If all $S_{hk}$ vanish, [\[eq:walsh\]](sections/4_sign_cut.tex#L22){reference-type="eqref" reference="eq:walsh"} is constant. Conversely, fix $a<b$, multiply [\[eq:walsh\]](sections/4_sign_cut.tex#L22){reference-type="eqref" reference="eq:walsh"} by the Walsh character $s_as_b$, and average over all $2^{|\mathcal A|}$ patterns. Orthogonality of distinct sign characters gives $$2^{-|\mathcal A|}\sum_sQ(s)s_as_b=S_{ab}.$$ The left side is zero when $Q$ is constant. Hence every $S_{ab}$ vanishes.

The edge coefficients may be complex; the theorem locates sensitivity and does not assign a real saving sign. Vanishing of $S_{hk}$ only requires the two directed terms to cancel in their sum. For complex baseline multipliers, the correct paired edge is $$\overline{C_h}C_kM_{hk}+\overline{C_k}C_hM_{kh},$$ not $C_hC_k(M_{hk}+M_{kh})$.

# Hard-window leakage bound

Let $T$ be the common synthesis map on a finite $\delta$-separated frequency set and $N$ consecutive integers. TPC-243 proves $$\left|N^{-1}\left\langle Tu,Tv\right\rangle-\left\langle u,v\right\rangle\right|
\leq\varepsilon\left\lVert u\right\rVert\left\lVert v\right\rVert,
\qquad
\varepsilon=\frac{\delta^{-1}H_{\lfloor1/(2\delta)\rfloor}}{N}.$$

For a common unit-phase pattern $\eta=(\eta_h)_h$, let $B(\eta),W(\eta)$ denote the direct-sum vectors obtained by replacing $C_h$ with $\eta_hC_h$, and define $$Q_I(\eta)=N^{-1}\left\langle TW(\eta),TB(\eta)\right\rangle.$$

> **Corollary: pairwise physical sign localization** For any two common unit-phase patterns $\eta,\xi$, $$|Q_I(\eta)-Q_I(\xi)|
> \leq2\varepsilon\left\lVert W\right\rVert\left\lVert B\right\rVert.$$ The norms on the right are coefficient-space norms.

> **Proof** The orthogonal common-multiplier theorem makes the coefficient covariance and both coefficient norms independent of the phase pattern. If their common covariance is $q_0$, the hard-window estimate gives $$|Q_I(\eta)-q_0|\leq\varepsilon\left\lVert W\right\rVert\left\lVert B\right\rVert,
> \qquad
> |Q_I(\xi)-q_0|\leq\varepsilon\left\lVert W\right\rVert\left\lVert B\right\rVert.$$ The triangle inequality proves the claim.

The orientation matches the selected TPC-242 mode: for $X=N^{-1/2}TB$ and $Y=N^{-1/2}TW$, one has $F_1=\left\langle Y,X\right\rangle=Q_I$. For primitive rational frequencies of height at most $U=x^{133/400}$ on the V59 interval, $$\varepsilon=\left(\frac{133}{100}+o(1)\right)
x^{-67/200}\log x=x^{-67/200+o(1)}.$$ This decay is not yet an arithmetic saving: literal two-lane attachment and a payable estimate for $\left\lVert W\right\rVert\left\lVert B\right\rVert$ remain open.

# Exact finite certification

The executable package contains three independent exact-rational controls. First, three two-dimensional orthogonal blocks with multipliers $2,-3,5$ are tested under all eight common sign patterns; covariance and both norms are identical in every case. Second, three blocks are embedded nonorthogonally into a two-dimensional ambient space. The resulting edge coefficients are $$D=-12,\qquad S_{5,7}=-12,\qquad S_{5,35}=20,\qquad S_{7,35}=-15.$$ All eight patterns satisfy the cut identity, and more than one covariance value occurs. This is an exact sign-sensitive control.

Third, four quarter frequencies on the hard interval $\{-3,-2,\ldots,13\}$ are grouped into three sign blocks. Here $N=17$, $R=6$, and $\varepsilon=6/17$. Every sign pattern satisfies the individual TPC-243 transfer inequality, and all $64$ ordered pairs satisfy the squared factor-two bound.

The independent checker reimplements Gaussian arithmetic, the hard-window synthesis, strict JSON parsing, source hashing, all nested schema checks, and hostile digest-rebound mutations without importing the producer. A separate stress census verifies $104{,}976$ common-sign direct-sum covariances and $216$ sign-cut identities. These records are finite illustrations only; the proofs above establish the theorem.

# Route evaluation and source boundary

The strongest positive result is an exact localization: a common aggregate phase is absent from the same-block principal covariance, while every nonorthogonal sign effect lies on a symmetrized cross-block edge. TPC-243 then confines physical hard-window variation to two Gram-error terms.

The strongest obstruction is equally explicit. The local principal term is $$|C_h|^2\left\langle w_h,b_h\right\rangle,$$ so the outer sign of $C_h$ cannot drive its cancellation. A successful signed mechanism must instead use at least one of the following: cancellation inside $|C_h|$, a nontrivial local covariance, cross-block leakage, or asymmetric multipliers on the two lanes.

The first physical blocker is the absent literal V59 map $$(\beta,w)\longmapsto\{b_{h,a},w_{h,a}\}_{(a,h)=1}$$ with the same coefficient placement and one synthesis operator. The current result is therefore conditional at that interface. It supplies no arithmetic $L^2$, fixed-atom credit, strict endpoint payment, full Gate B, or twin-prime conclusion.

The next minimal invariant is the within-block covariance. Given a canonical unit vector in a block, its longitudinal moments and transverse energies determine a sharp center-radius disk for $\left\langle w_h,b_h\right\rangle$. This avoids chasing an outer sign that the present theorem proves invisible.

# Conclusion

We proved that a common clustered multiplier enters an orthogonal two-lane covariance through its squared modulus, not its outer sign. A complete nonorthogonal expansion turns every possible real-sign effect into a graph-cut edge, and hard-window synthesis limits common-sign variation by $2\varepsilon\left\lVert W\right\rVert\left\lVert B\right\rVert$. The result closes one tempting route: outer $C_h$ signs cannot control the same-bucket main term. The open road is now the local lane covariance and its literal V59 attachment, beginning with a sharp longitudinal–transverse decomposition.

# Status ledger

| Item                            | Status                                                                   |
|:--------------------------------|:-------------------------------------------------------------------------|
| Common-multiplier covariance    | Proved exact                                                             |
| Common unit-phase invariance    | Proved exact                                                             |
| Internal Möbius cancellation    | Preserved; not estimated                                                 |
| Nonorthogonal sign-cut identity | Proved exact                                                             |
| All-sign invariance criterion   | Proved if and only if                                                    |
| Hard-window pair variation      | At most $2\varepsilon\left\lVert W\right\rVert\left\lVert B\right\rVert$ |
| Literal V59 two-lane attachment | Open                                                                     |
| Coefficient norm payment        | Open                                                                     |
| Arithmetic advance / $L^2$      | No / none                                                                |
| Fixed-atom credit               | Zero                                                                     |
| Strict $1/400$ / full Gate B    | Unpaid / open                                                            |
| Twin-prime result               | None                                                                     |

Maximum claim: structural L1 common-multiplier sign localization. The V59 specialization remains conditional on a literal phasewise primitive two-lane attachment.

# Non-content font-mapping input (preserved command)

Original paper/main.tex line 8: glyphtounicode.tex, SHA-256 395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851. This audited PDF glyph-to-Unicode map is not manuscript content. Its command is retained without executing TeX or expanding the mapping table.

``` {.latex}
\input{glyphtounicode}
```

<!-- SOURCE_BODY_END -->
