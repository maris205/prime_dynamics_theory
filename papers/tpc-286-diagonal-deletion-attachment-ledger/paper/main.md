# A Diagonal-Deletion Attachment Ledger for the Literal Prime-Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`
- Converter: `source-markdown-audit-v2`

## Abstract

The previous finite control atlas found sign changes in the literal source attachment under small schedule perturbations, while the preceding residue analysis found a tempting low-rank factorization that does not survive the physical diagonal convention. This paper isolates the missing term. For a finite prime shell we define a diagonal-including output, an explicit diagonal correction, and the physical deleted-diagonal output. A finite-sum argument proves the exact identities $g_{\mathrm{phys}}=g_{\mathrm{full}}-g_{\mathrm{diag}}$ and $C_{\mathrm{phys}}=C_{\mathrm{full}}-C_{\mathrm{diag}}$ for the declared four-block attachment. We then replay all 72 rows obtained from six baseline tuples, two kernel exponents, and six local controls. Every full, diagonal, and physical scalar interval is separated from zero. The full and physical signs differ in 15 rows; the diagonal correction opposes the physical term in 30 rows and has a strictly larger certified absolute magnitude in 21 rows. These are finite certificates, not asymptotic estimates. The result makes the obstruction explicit: any centered-residue proof of the literal arithmetic estimate must pay for the deleted diagonal before seeking signed cross-prime cancellation. No fixed-power credit, Gate-B passage, or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Motivation and contribution

The literal twin-prime route under study attaches a prime-shell operator to a finite source profile. TPC-284 showed that six natural schedule controls can change the sign of the resulting scalar attachment on a registered finite atlas `\cite{tpc284}`. TPC-285 then identified an exact algebraic structure: the centered residue block for one prime factors through its nonzero residue indicators and has rank at most $q-2$, but deleting the diagonal makes the active block full rank `\cite{tpc285}`. The two observations leave a precise question: how much of the finite sensitivity is carried by the diagonal term that the physical operator removes?

This paper answers that question at the level supported by the frozen finite model. Its contributions are:

1.  an exact decomposition of the diagonal-including and physical prime-shell outputs, including a closed formula for the deleted diagonal;

2.  an exact linearity proof for the scalar attachment used throughout the finite route;

3.  a 72-row, independently replayable ledger of the three components, their signs, sign flips, and interval-certified magnitude comparisons;

4.  a sharpened route obstruction: finite diagonal sensitivity is real, but it does not by itself settle growing-scale cancellation.

The main positive result is therefore structural rather than asymptotic. The main negative result is equally specific: a centered low-rank representation cannot be substituted for the literal physical block without tracking the diagonal correction.

# The frozen finite operator

Let $I$ be a finite interval of integer indices and let $q$ be an odd prime. Define the active mask and centered residue block by $$m_q(u)=\mathbf 1_{q\nmid u},\qquad
 B_q(u,t)=m_q(u)m_q(t)
 \left(\mathbf 1_{u\equiv t\pmod q}-\frac{1}{q-1}\right).
 \label{eq:block}$$ The physical convention removes the diagonal: $$D_q=B_q-\operatorname{diag}(B_q).
 \label{eq:deleted}$$ For height $H>0$ and exponent $s\in\{1,2\}$, the rational kernel is $$K_H(h)=\frac{H^{2s}}{(H^2+h^2)^s}.
 \label{eq:kernel}$$ For a finite shell $\mathcal S_Q=\{q:Q<q\leq2Q,\ q\text{ prime}\}$ and a source vector $\beta$, define the two outputs $$\begin{aligned}
 g_{\mathrm{full}}(u)
  &=\sum_{q\in\mathcal S_Q}\sum_{t\in I}
       qK_H(u-t)B_q(u,t)\beta(t),\label{eq:full}\\
 g_{\mathrm{phys}}(u)
  &=\sum_{q\in\mathcal S_Q}\sum_{t\in I}
       qK_H(u-t)D_q(u,t)\beta(t).\label{eq:physical}\end{aligned}$$ The first sum includes the $t=u$ terms; the second one does not.

The scalar used in the finite certificates is the four-block projected attachment. If $w$ is the interval-valued source weight and $g$ is an output, write $$C(w,g)=\sum_{u\in I}w(u)g(u)
 -\sum_{r=1}^{3}\frac{W_r(w)G_r(g)}{d_r},
 \label{eq:attachment}$$ where $W_r$ and $G_r$ are fixed linear block contrasts and $(d_1,d_2,d_3)$ are the corresponding fixed normalizers. The exact choices are the four equal blocks and contrasts inherited from TPC-268 `\cite{tpc268}`. Only linearity in the second argument is used in the theorem below.

# Exact diagonal split

> **Theorem: diagonal output and physical split** For every finite $I$, finite prime shell $\mathcal S_Q$, source vector $\beta$, $H>0$, and integer $s\geq1$, define $g_{\mathrm{full}}$ and $g_{\mathrm{phys}}$ by [\[eq:full\]](main.tex#L108){reference-type="eqref" reference="eq:full"}–[\[eq:physical\]](main.tex#L111){reference-type="eqref" reference="eq:physical"}. Then $$g_{\mathrm{diag}}(u)=\sum_{q\in\mathcal S_Q}qK_H(0)
>        \frac{q-2}{q-1}m_q(u)\beta(u),
>  \label{eq:diag-output}$$ and $$g_{\mathrm{phys}}=g_{\mathrm{full}}-g_{\mathrm{diag}}.
>  \label{eq:output-split}$$ Moreover, every scalar functional linear in its output argument satisfies $$C(w,g_{\mathrm{phys}})=C(w,g_{\mathrm{full}})-C(w,g_{\mathrm{diag}}).
>  \label{eq:scalar-split}$$

> **Proof** If $q\mid u$, then the mask in [\[eq:block\]](main.tex#L91){reference-type="eqref" reference="eq:block"} is zero. Otherwise the congruence indicator on the diagonal is one. In both cases, $$B_q(u,u)=m_q(u)\left(1-\frac1{q-1}\right)
>  =m_q(u)\frac{q-2}{q-1}.
>  \label{eq:diagonal-entry}$$ The $t=u$ part of [\[eq:full\]](main.tex#L108){reference-type="eqref" reference="eq:full"} is therefore exactly [\[eq:diag-output\]](main.tex#L137){reference-type="eqref" reference="eq:diag-output"}. For $u\ne t$, $D_q(u,t)=B_q(u,t)$, while $D_q(u,u)=0$. Subtracting the diagonal summand from each finite full sum consequently gives $$g_{\mathrm{full}}(u)-g_{\mathrm{diag}}(u)
>  =\sum_{q\in\mathcal S_Q}\sum_{t\in I}
>  qK_H(u-t)D_q(u,t)\beta(t),$$ which is $g_{\mathrm{phys}}(u)$. Finally, linearity of $C$ gives $$C(w,g_{\mathrm{full}}-g_{\mathrm{diag}})
>  =C(w,g_{\mathrm{full}})-C(w,g_{\mathrm{diag}}).$$ All sums are finite, so no convergence or rearrangement theorem is required.

> **Remark** The theorem is stronger than a numerical coincidence but narrower than an asymptotic estimate. It identifies exactly what must be paid when the centered residue block of TPC-285 is replaced by the physical off-diagonal operator. It does not say that the diagonal correction dominates for every source scale or every shell.

# The registered 72-row ledger

The audit uses the six baseline tuples $$(64,15,4,4),\ (96,20,5,4),\ (128,24,5,4),\quad
 (192,32,6,5),\ (256,38,6,5),\ (384,50,7,5),
 \label{eq:baselines}$$ where a tuple records $(X,H,Q,z)$. Each baseline is evaluated at $s=1,2$ under the six controls $H-2$, $H+2$, $z-1$, $z+1$, $Q-1$, and $Q+1$. Thus the ledger contains $6\cdot2\cdot6=72$ rows. The source profile, cutoff convention, and interval arithmetic are inherited unchanged from the finite operator certificate `\cite{tpc268}`.

For each row we compute the exact rational vectors $g_{\mathrm{full}}$ and $g_{\mathrm{diag}}$, form $g_{\mathrm{phys}}=g_{\mathrm{full}}-g_{\mathrm{diag}}$, and apply [\[eq:attachment\]](main.tex#L121){reference-type="eqref" reference="eq:attachment"}. The stored intervals use the established decimal serialization; all sign and ratio tests are performed on the underlying rational interval endpoints. The principal census is shown in Table [1](main.tex#L208){reference-type="ref" reference="tab:census"}.

<div id="tab:census">

| Component                  |  Negative|  Positive|  Total|
|:---------------------------|---------:|---------:|------:|
| Full, diagonal included    |        49|        23|     72|
| Diagonal correction        |        34|        38|     72|
| Physical, diagonal deleted |        60|        12|     72|
| Component-separated rows   |          |        72|       |

: TPC-286 finite component census. Every component interval is sign-separated from zero.

</div>

The decomposition is computationally meaningful, not just notational. The full and physical signs differ in 15 rows. In 30 rows the diagonal correction has the opposite sign from the physical attachment, and in 21 rows its certified absolute lower bound is strictly larger than the physical absolute upper bound. The conservative ratio lower bound exceeds $2$ in 13 rows and $10$ in 4 rows. Exact interval subtraction confirms that the reconstructed interval $$\label{eq:reconstruction}$$ contains the independently computed physical interval in all 72 rows.

<div id="tab:controls">

| Control |  Rows|  Full/physical flips|  Diagonal opposite|
|:--------|-----:|--------------------:|------------------:|
| $H-2$   |    12|                    3|                  5|
| $H+2$   |    12|                    3|                  5|
| $z-1$   |    12|                    1|                  3|
| $z+1$   |    12|                    3|                  7|
| $Q-1$   |    12|                    0|                  2|
| $Q+1$   |    12|                    5|                  8|
| Total   |    72|                   15|                 30|

: Sensitivity summary for the six local controls.

</div>

Table [2](main.tex#L239){reference-type="ref" reference="tab:controls"} shows that the effect is not confined to one kind of perturbation. Height and shell-endpoint controls produce several flips, while the cutoff controls also alter the source weights that multiply the same operator. The table is descriptive of the registered finite family only.

# Interpretation and route consequence

The exact split supplies a clean interface between the two preceding papers. TPC-285’s centered factorization remains useful for isolating residue modes, but the physical operator is obtained only after subtracting $$\Delta_{\mathrm{diag}}(u)=\sum_{q\in\mathcal S_Q}qK_H(0)
 \frac{q-2}{q-1}m_q(u)\beta(u).
 \label{eq:delta}$$ The finite ledger shows why this term cannot be silently absorbed into a low-rank argument: it can change the scalar sign, oppose the physical term, and exceed its certified magnitude on a substantial subset of the registered controls.

There are two asymmetric lessons. First, the diagonal correction is a genuine analytic object with a closed formula, so future full-shell work can separate it before estimating any norm. Second, the finite evidence does not choose the eventual asymptotic sign. A diagonal correction that is large in a finite row may cancel across primes, and the 15 sign flips do not constitute a counterexample to a growing-scale theorem that has not been stated here.

The next mathematically meaningful target is therefore a signed full-shell estimate after the split. Such a result would need to control at least one of the following: cross-prime cancellation, source orthogonality, singular values of the full-rank physical blocks, or a uniform bound for the explicit diagonal sum. Separate absolute estimates for $g_{\mathrm{full}}$ and $g_{\mathrm{diag}}$ cannot by themselves supply the desired cancellation.

# Verification, limitations, and conclusion

The release contains four auditable layers. The producer locks the TPC-284 control result, the TPC-285 rank result, and the frozen TPC-268 engine by normalized-LF SHA-256 hashes. The independent checker rebuilds prime shells, all three output vectors, all 72 attachments, and the complete census without importing the producer. A hostile stress script rejects mutations to the theorem, component intervals, signs, flags, budget, provenance, and row census. Finally, the fail-closed Bridge-B checker runs the producer, independent checker, and stress audit in ordinary and optimized Python, requiring empty standard error and identical paired output.

The limitations are part of the result. The source profile is a declared finite modeling choice; the interval ledger has no moving-order theorem; the diagonal dominance counts have no asymptotic extrapolation; and no arithmetic $L^2$ estimate has been proved. The Session-level Route-A/Route-B evaluator files are not present in this checkout, so the local route evaluation is explicitly a fail-closed Route-B fallback.

In summary, the paper proves the exact identity needed to bridge centered and physical prime-shell operators and certifies its finite sensitivity on all 72 registered controls. The strongest reusable structure is $$\text{centered residue block}
 \longrightarrow \text{diagonal correction}
 \longrightarrow \text{physical attachment ledger}.$$ The next open theorem is signed full-shell cancellation after this split. Fixed-power credit remains zero, Gate B remains open, and no twin-prime conclusion follows.

# Reproducibility details

The shell parameters and control map are fixed by [\[eq:baselines\]](main.tex#L189){reference-type="eqref" reference="eq:baselines"}. The source interval is $I_X=(X/2,X]\cap\mathbb Z$ and the four blocks are equal consecutive subintervals. The three contrasts are $$(1,1,-1,-1),\qquad (1,-1,0,0),\qquad (0,0,1,-1),$$ with normalizers $4b,2b,2b$ when each block has size $b$. The producer uses exact rational arithmetic for $\beta$, the kernel, and the residue indicators; interval-valued source weights are rounded outward on the frozen grid. A stored component endpoint is checked after normalization against the frozen engine’s decimal serializer, while the reconstruction test uses the exact internal endpoints.

The certificate records the following finite facts:

| Fact                                               |   Count|
|:---------------------------------------------------|-------:|
| Rows with all three components separated from zero |      72|
| Rows with full/physical sign flip                  |      15|
| Rows with diagonal sign opposite to physical sign  |      30|
| Rows with strict diagonal-over-physical magnitude  |      21|
| Rows with ratio lower bound $>2$ / $>10$           |  13 / 4|
| Fixed-power credit                                 |       0|

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc284,
  author = {Liang Wang},
  title = {A Finite Control Atlas for Literal Twin-Prime Source Attachment},
  note = {TPC-284 in-repository research artifact, 2026}
}

@misc{tpc285,
  author = {Liang Wang},
  title = {Prime-Shell Residue Factorization and the Deleted-Diagonal Rank Obstruction},
  note = {TPC-285 in-repository research artifact, 2026}
}

@misc{tpc268,
  author = {Liang Wang},
  title = {Finite Cutoff Sensitivity Obstruction for the Literal Operator},
  note = {TPC-268 in-repository research artifact, 2026}
}
```

<!-- SOURCE_BODY_END -->
