# Weighted Covariance-Disk Reassembly\ and Hard-Window Margins

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

We determine the exact aggregate geometry of finitely many local complex covariances. Arbitrary jointly feasible local values contained in disks give a weighted aggregate contained in one explicit disk. If the joint feasible set is the full Cartesian product of those disks, the containment is an equality: its center is the weighted sum of the local centers and its radius is the sum of the absolute-weighted local radii. An explicit inverse construction realizes every aggregate point and covers all degenerate cases. Exact cancellation, minimum-modulus, and phase-sector criteria follow. Applied to the common-multiplier direct-sum geometry of TPC-244 and the local covariance disks of TPC-245, the theorem gives a sharp coefficient-space obstruction. The TPC-243 hard-window error enlarges the radius once and yields a conditional strict nonvanishing margin. Full product realizability, the physical two-lane attachment, and every arithmetic estimate remain open; no twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

TPC-245 identifies a local covariance with fixed longitudinal moments and transverse energies as a closed disk when the complex transverse dimension is at least two. TPC-244 shows that a common block multiplier contributes the nonnegative weight $|\gamma_h|^2$ to the coefficient covariance. The next question is therefore global: what set is generated when all local disks are reassembled?

There are two logically distinct answers. Marginal disk containments always give a containing aggregate disk. Equality requires the stronger statement that all local choices can be realized jointly, i.e. that the joint feasible set is a Cartesian product. This distinction is essential for an arithmetic source, where different blocks may be coupled even when every marginal projection is large.

The main theorem proves the exact product result for arbitrary complex scalar weights. It then specializes to the source-compatible weights $|\gamma_h|^2$ and pays the hard-window transfer error. The result is a sharp dichotomy: the aggregate center dominates both transverse freedom and window leakage, or the available local data do not certify nonvanishing.

# Joint feasible sets and unconditional containment

Let $A$ be finite. For $h\in A$, fix $c_h,\lambda_h\in\mathbb{C}$ and $r_h\ge0$. Let $\mathcal J$ be a nonempty set of jointly feasible tuples $z=(z_h)_{h\in A}$ satisfying $$z_h\in c_h+r_h\overline{\mathbb{D}}.$$ Define $$\mathfrak{C}=\sum_{h\in A}\lambda_hc_h,
 \qquad
 \mathfrak{R}=\sum_{h\in A}|\lambda_h|r_h,$$ and $$\mathcal A_\lambda(\mathcal J)
 =\left\{\sum_{h\in A}\lambda_hz_h:z\in\mathcal J\right\}.$$

> **Proposition: Coupled-family enclosure**<span id="prop:containment" label="prop:containment">\[prop:containment\]</span> For every such joint family, $$\mathcal A_\lambda(\mathcal J)
>  \subseteq \mathfrak{C}+\mathfrak{R}\overline{\mathbb{D}}.$$ No product-realizability assumption is needed.

> **Proof** For $z\in\mathcal J$, write $z_h=c_h+e_h$ with $|e_h|\le r_h$. Then $$\left|\sum_h\lambda_hz_h-\mathfrak{C}\right|
>  \le \sum_h|\lambda_h|\,|e_h|
>  \le \mathfrak{R}.$$

The nonemptiness premise matters: an unrealizable local TPC-245 branch makes the full joint family empty, even when its scalar weight happens to vanish.

# Exact weighted-disk reassembly

> **Theorem: Weighted Minkowski disk identity**<span id="thm:disk" label="thm:disk">\[thm:disk\]</span> Assume blockwise product realizability, $$\mathcal J=\prod_{h\in A}(c_h+r_h\overline{\mathbb{D}}).$$ Then $$\mathcal A_\lambda(\mathcal J)=\mathfrak{C}+\mathfrak{R}\overline{\mathbb{D}}.$$ The identity includes an empty index set, zero weights, and zero radii.

> **Proof** Proposition [\[prop:containment\]](sections/2_joint_geometry.tex#L21){reference-type="ref" reference="prop:containment"} gives one inclusion. If $\mathfrak{R}=0$, every nonnegative summand $|\lambda_h|r_h$ vanishes, so every weighted deviation is zero and the aggregate is the singleton $\{\mathfrak{C}\}$.
>
> Suppose $\mathfrak{R}>0$ and fix $d\in\mathbb{C}$ with $|d|\le\mathfrak{R}$. Define $$e_h=
>  \begin{cases}
>  \displaystyle
>  \frac{\overline{\lambda_h}}{|\lambda_h|}
>  \frac{r_h}{\mathfrak{R}}\,d,&\lambda_h\ne0,\\[7pt]
>  0,&\lambda_h=0.
>  \end{cases}$$ Then $|e_h|=r_h|d|/\mathfrak{R}\le r_h$ whenever $\lambda_h\ne0$, while $$\sum_h\lambda_he_h
>  =\frac d{\mathfrak{R}}\sum_h|\lambda_h|r_h=d.$$ Thus $z_h=c_h+e_h$ is a jointly feasible product choice whose aggregate is $\mathfrak{C}+d$. This proves the reverse inclusion. For $A=\varnothing$, the empty product has one empty tuple and the empty sum gives $\{0\}$, agreeing with the formula.

The formula uses arbitrary complex weights only as abstract covariance scalars. A common multiplier in both Hilbert-space lanes gives the narrower weight $|\gamma_h|^2$. Different lane multipliers $a_h,d_h$ would instead give $\overline{a_h}d_h$ and require separate norm budgets.

# Sharp cancellation and insufficiency

> **Corollary: Distance and phase**<span id="cor:geometry" label="cor:geometry">\[cor:geometry\]</span> Under Theorem [\[thm:disk\]](sections/3_exact_reassembly.tex#L3){reference-type="ref" reference="thm:disk"}, $$0\in\mathcal A_\lambda(\mathcal J)\iff |\mathfrak{C}|\le\mathfrak{R},
>  \qquad
>  \min_Q|Q|=\max\{|\mathfrak{C}|-\mathfrak{R},0\}.$$ If $\mathfrak{R}<|\mathfrak{C}|$, all aggregate values lie in the sharp sector about $\mathfrak{C}$ of half-angle $\arcsin(\mathfrak{R}/|\mathfrak{C}|)$.

> **Proof** The first two statements are the distance from the origin to the exact disk. When the disk misses the origin, its two tangent rays make a right triangle with hypotenuse $|\mathfrak{C}|$ and opposite side $\mathfrak{R}$. Tangency also proves sharpness.

Consequently, if $|\mathfrak{C}|\le\mathfrak{R}$, fixed local centers and radii alone cannot prove a positive aggregate lower bound in the product model: the explicit construction in Theorem [\[thm:disk\]](sections/3_exact_reassembly.tex#L3){reference-type="ref" reference="thm:disk"} realizes exact zero. This is an insufficiency theorem about those data, not evidence that an unknown coupled arithmetic subfamily actually attains zero.

The full-disk premise cannot be weakened silently. A positive-radius one-dimensional TPC-245 branch is a circle. For example, the sum of two centered circles of radii $2$ and $1$ is the annulus $\{z:1\le|z|\le3\}$, not the radius-$3$ disk. Nor do exact marginal disks imply a product: if $\mathcal J=\{(z,-z):|z|\le1\}$ and both weights are one, the aggregate is always zero although each marginal is the unit disk.

# Common multipliers and hard-window inflation

For each block, let TPC-245 supply a full local disk $$\left\langle w_h,b_h\right\rangle\in c_h+r_h\overline{\mathbb{D}},
 \qquad
 c_h=\overline{w_h^{\parallel}}b_h^{\parallel},
 \quad r_h=\sqrt{E_{B,h}E_{W,h}},$$ where every positive-radius active transverse space has complex dimension at least two. If these choices have blockwise product realizability, then the TPC-244 common multipliers $\gamma_h$ give the exact coefficient disk with $$\mathfrak{C}=\sum_h|\gamma_h|^2c_h,
 \qquad
 \mathfrak{R}=\sum_h|\gamma_h|^2r_h.$$

Assume additionally that both coefficient lanes lie in one finite $\delta$-separated frequency space and are synthesized by the common TPC-243 map $T$ on $N$ consecutive integers. Write $$\epsilon=\frac{\delta^{-1}H_{\lfloor1/(2\delta)\rfloor}}{N},
 \qquad
 Q_I=N^{-1}\left\langle TW,TB\right\rangle.$$ With fixed local moments and energies, the common-multiplier direct sum has fixed norm budgets $$L_B^2=\sum_h|\gamma_h|^2
       (|b_h^{\parallel}|^2+E_{B,h}),\qquad
 L_W^2=\sum_h|\gamma_h|^2
       (|w_h^{\parallel}|^2+E_{W,h}).$$

> **Theorem: Window-inflated margin**<span id="thm:window" label="thm:window">\[thm:window\]</span> Under the stated attachment, with $E_{\mathrm{win}}=\epsilon L_WL_B$, $$Q_I\in\mathfrak{C}+(\mathfrak{R}+E_{\mathrm{win}})\overline{\mathbb{D}}$$ and $$|Q_I|\ge\max\{|\mathfrak{C}|-\mathfrak{R}-E_{\mathrm{win}},0\}.$$ In particular, $|\mathfrak{C}|>\mathfrak{R}+E_{\mathrm{win}}$ implies uniform nonvanishing.

> **Proof** TPC-243 gives the correctly oriented one-transfer estimate $$|Q_I-\left\langle W,B\right\rangle|\le\epsilon\left\lVert W\right\rVert\left\lVert B\right\rVert=E_{\mathrm{win}}.$$ The coefficient covariance lies in $\mathfrak{C}+\mathfrak{R}\overline{\mathbb{D}}$. The triangle and reverse-triangle inequalities prove the claims.

If the norms vary over admissible realizations, $L_WL_B$ must be replaced by a uniform supremum. The displayed physical set is only contained in the inflated disk: the transfer theorem does not realize every error phase. The strict margin is sufficient, not necessary, and only one factor of $\epsilon$ is paid for this single coefficient-to-window comparison.

# Exact finite certificate

The machine-readable certificate uses three Gaussian-rational local disks and complex weights of moduli $1,1,2$. It recomputes $$\mathfrak{C}=\frac{61}{65}-\frac{97}{65}i,\qquad \mathfrak{R}=2,$$ and uses the proof’s reverse formula to realize aggregate zero and a boundary point exactly. A second fixture has coefficient center $7$, radius $3/4$, and window leakage $1/4$, giving the strict lower margin $6$.

The independent checker redoes the Gaussian-rational algebra without importing the producer and rejects sixteen digest-rebound semantic mutations. The stress suite checks 175 forward product points, 27 reverse targets (including a zero-radius system), and a circle-annulus control. These are finite reproduction checks only; the theorem is symbolic and no asymptotic claim is inferred from the fixtures.

# Source lock and route boundary

The structural chain is $$\begin{aligned}
 \text{TPC-245 local disk}
 &\longrightarrow \text{TPC-244 weight }|\gamma_h|^2
 \longrightarrow \text{exact aggregate disk}\\
 &\longrightarrow \text{TPC-243 window enclosure}.
\end{aligned}$$ Only the first three arrows are exact in the stated abstract product model; the final arrow is a conditional containing estimate.

The committed source does not construct literal V59 coefficient lanes in one common separated synthesis space, a source-native one-dimensional direction in each block, or blockwise product realizability. It also does not pay the local moments, transverse energies, or coefficient norms needed to make $$|\mathfrak{C}|-\mathfrak{R}-\epsilon L_WL_B$$ positive on an arithmetic scale. The similarly named TPC-219 object is a constant-prime-label subspace and remains projection lineage only.

Accordingly, the maximum claim is $$\texttt{PROVED\_STRUCTURAL\_L1\_WEIGHTED\_COVARIANCE\_DISK\_REASSEMBLY}.$$ There is no arithmetic L2 estimate, fixed-atom credit, payment of strict $1/400$, full Gate B, or twin-prime theorem.

# Conclusion

Local covariance disks now have an exact global calculus. Their weighted product image is one disk, and its center–radius gap is the complete coefficient-space nonvanishing margin. Hard-window synthesis spends an additional explicit radius. This isolates the next useful target sharply: construct the source-native two-lane block object and prove a longitudinal margin that dominates both transverse freedom and window leakage. Until that interface is supplied, the result remains a structural obstruction and conditional bridge rather than an arithmetic advance.

# Status ledger

| Field                                       | Status                                             |
|:--------------------------------------------|:---------------------------------------------------|
| Maximum claim                               | `PROVED_STRUCTURAL_L1_` `WEIGHTED_DISK_REASSEMBLY` |
| Coupled-family aggregate disk               | proved containment                                 |
| Full product aggregate disk                 | proved exact with explicit inverse                 |
| Zero criterion / minimum modulus            | proved exact                                       |
| Phase sector                                | proved sharp for $\mathfrak{R}<|\mathfrak{C}|$     |
| Common-multiplier specialization            | structural; weights $|\gamma_h|^2$                 |
| Hard-window disk                            | conditional containment, not exact image           |
| Blockwise product realizability             | open for the arithmetic source                     |
| Literal V59 two-lane attachment             | open                                               |
| Canonical block directions / payable margin | open / open                                        |
| Arithmetic L2 / fixed atom                  | none / zero                                        |
| Strict $1/400$ / full Gate B                | unpaid / open                                      |
| Twin-prime result                           | none                                               |

# Non-content font-mapping input (preserved command)

Original paper/main.tex line 8: glyphtounicode.tex, SHA-256 395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851. This audited PDF glyph-to-Unicode map is not manuscript content. Its command is retained without executing TeX or expanding the mapping table.

``` {.latex}
\input{glyphtounicode}
```

<!-- SOURCE_BODY_END -->
