# Position-Aware Lower Witnesses\ for a Literal Prime-Shell Mask Defect

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `1de1964aa411aa631587da690524beadf1127d3c`
- Converter: `source-markdown-audit-v2`

## Abstract

We study the literal masked prime-shell matrix isolated in TPC-347. Writing the physical interval block as an unmasked convolution compression plus a divisibility-mask defect, we derive an exact coordinate formula for every defect column. If $J_I$ is the set of interval positions divisible by at least one active shell prime, then the induced Euclidean norm obeys the exact finite-dimensional lower bound $$\|D_I\|_{2\to2}\geq W_I(D):=
 \max_{t\in J_I}\|D_I e_t\|_2.$$ This witness uses only declared mask-hit positions and does not fit a leading eigenvector. On a locked grid of 192 rows, all rows have a positive witness; the best-hit witness is $0.453958762219$–$0.897148966365$ of the defect spectral norm and $0.0183057714619$–$0.336311065586$ of the unmasked ideal norm. These are finite observations, not growing lower bounds. The result therefore sharpens a scoped obstruction to deleting the masks while leaving the source-uniform arithmetic $L^2$ problem open.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The twin-prime route currently contains a literal finite prime-shell operator with two endpoint divisibility restrictions. The preceding TPC-347 release showed that replacing this physical object by its unmasked convolution can hide a sizeable finite defect. The present paper asks a narrower question: can that defect be witnessed by a deterministic position-aware vector, with no use of its leading eigenvector and no sign heuristic?

Our answer is yes in a precise finite sense. The main theorem is elementary operator-norm linear algebra, but its use here is structural: it identifies the positions at which the literal masks force a nonzero column and supplies a reproducible lower-witness audit. Nothing below is an asymptotic estimate, a source-uniform arithmetic theorem, or a proof of the twin-prime conjecture.

# The literal object

Let $I=\{o,o+1,\ldots,o+M-1\}$, let $R_I$ denote restriction, and let $E_I$ denote zero extension. For a shell prime $p$, define the diagonal projection $$(P_p f)(n)=\mathbf 1_{p\nmid n}f(n).$$ The translated residue kernel $K_p$ has the zero diagonal and the same height and exponent normalisation as TPC-347. With the declared sign $\varepsilon_p\in\{\pm1\}$, the physical and unmasked blocks are $$\begin{aligned}
 A_I&=\sum_{p}\varepsilon_p R_I P_pK_pP_pE_I,\\
 T_I&=R_I\left(\sum_p\varepsilon_pK_p\right)E_I,
 \qquad D_I=A_I-T_I.\end{aligned}$$ The distinction between $A_I$ and $T_I$ is essential: $T_I$ is an interval compression of a translation-invariant convolution, whereas $A_I$ retains the absolute-position masks.

For one prime, the projection algebra gives $$P_pK_pP_p-K_p=(P_p-I)K_pP_p+K_p(P_p-I).
 \label{eq:defect}$$ Thus $$D_I=\sum_p\varepsilon_pR_I\bigl((P_p-I)K_pP_p
                 +K_p(P_p-I)\bigr)E_I.
 \label{eq:global-defect}$$

# Exact position formula and lower witness

Write $e_t$ for the unit coordinate vector associated with $t\in I$. Applying [\[eq:defect\]](main.tex#L86){reference-type="eqref" reference="eq:defect"} gives two cases. If $p\mid t$, then $P_pe_t=0$ and the right-mask term is $-K_pe_t$. If $p\nmid t$, then $(P_p-I)e_t=0$ and the left-mask term retains only output coordinates divisible by $p$. Consequently $$D_Ie_t=-\sum_{p\mid t}\varepsilon_pR_IK_pe_t
       +\sum_{p\nmid t}\varepsilon_pR_I(P_p-I)K_pe_t.
 \label{eq:column-formula}$$ This identity retains both sides of the physical mask; it makes no assertion that the prime contributions have a common sign.

Define the mask-hit set and its coordinate envelope by $$J_I=\{t\in I:\text{there is an active shell prime }p\text{ with }p\mid t\},
 \qquad
 W_I(D)=\max_{t\in J_I}\|D_Ie_t\|_2.$$

> **Theorem: coordinate lower witness** For every finite matrix $D_I$ and every nonempty $J_I$, $$\|D_I\|_{2\to2}\geq W_I(D).
>  \label{eq:witness}$$ In particular, the bound applies to the defect in [\[eq:global-defect\]](main.tex#L92){reference-type="eqref" reference="eq:global-defect"} without any positivity, symmetry, or cancellation assumption.

> **Proof** Each $e_t$ is a unit vector. With the standard induced-norm convention `\cite{conway2000}`, $$\|D_I\|_{2\to2}=\sup_{\|x\|_2=1}\|D_Ix\|_2\geq\|D_Ie_t\|_2.$$ Taking the maximum over $t\in J_I$ proves [\[eq:witness\]](main.tex#L120){reference-type="eqref" reference="eq:witness"}.

> **Remark** The selector is not an eigenvector optimization: $J_I$ is fixed by the declared interval and shell, and the only optimization is the explicit maximum over its coordinate columns. We also record the first-hit coordinate as a non-adaptive control.

# Frozen audit protocol

The producer locks the TPC-347 code and canonical certificate. We retain its physical object and use $$o\in\{40097,48097\},\quad M\in\{256,512,1024\},\quad
 Q\in\{24,36,54,80\},\quad s\in\{1,2\},$$ with $H=66$. The four predeclared sign laws are `all_plus`, `alternating_index`, `mod4_character`, and `half_split`. This gives $2\cdot3\cdot4\cdot2\cdot4=192$ rows.

For each row we reconstruct $A_I$, $T_I$, and $D_I$, form $J_I$, and store the first-hit and best-hit column norms. The independent checker reverses the shell accumulation order and does not import the producer. It recomputes all 192 rows, the two-sided formula [\[eq:column-formula\]](main.tex#L104){reference-type="eqref" reference="eq:column-formula"}, and a rational six-point anchor. A separate stress suite mutates the selector, each side of the mask formula, the anchor, the census, and the claim firewall.

# Finite results

Table [1](main.tex#L174){reference-type="ref" reference="tab:summary"} gives the complete aggregate readout. The quantity $\|T_I\|$ is the norm of the unmasked ideal comparison, not the physical operator. The ratios are reported only to describe the finite panel.

<div id="tab:summary">

| Quantity                            | Certified finite readout           |
|:------------------------------------|:-----------------------------------|
| Rows                                | $192$                              |
| Rows with positive mask-hit witness | $192/192$                          |
| Mask-hit count per row              | $30$–$169$                         |
| Formula records                     | $192$                              |
| Maximum formula discrepancy         | $2.0872192863\times10^{-14}$       |
| $W_I(D)/\|D_I\|$                    | $0.453958762219$–$0.897148966365$  |
| $W_I(D)/\|T_I\|$                    | $0.0183057714619$–$0.336311065586$ |
| First-hit $\|D_Ie_t\|/\|D_I\|$      | $0.188855872493$–$0.533179477634$  |

: TPC-348 position-aware witness audit.

</div>

The first-hit interval is useful as a hostile control: it is chosen by the smallest mask-hit position rather than by the largest observed column. The best-hit envelope is nevertheless fully declared, and the same selector is recomputed independently. In particular, every row has a positive witness, but the minimum ratio to the ideal norm is modest; no fixed power of the main variable can be inferred.

## Exact rational anchor

For $I=\{1,\ldots,6\}$, $Q=4$, $s=1$, and all-plus signs, the shell is $\{5,7\}$ and $J_I=\{5\}$. The selected fifth defect column has exact squared norm $$\|D_Ie_5\|_2^2=
 \frac{1264004832717663389653333}
 {162252681195863096059456}.$$ The machine certificate stores the six rational column entries and a canonical digest; the independent replay reproduces both the selector and the digest.

# Adversarial checks and claim boundary

The normal and optimized producer outputs agree byte-for-byte. The reverse shell independent replay and both normal/optimized stress runs pass. The stress mutations reject a wrong coordinate, an omitted left mask, an omitted right mask, a changed exact anchor, a changed census, and a false Gate-B flag. These are integrity checks on the computational package, not replacements for the theorem.

The logically strongest statements in this release are:

-   the two-sided projection expansion and the position formula are exact finite identities;

-   the coordinate lower-witness inequality is exact induced-norm linear algebra;

-   the 192-row positive-witness and formula census is numerically certified for the declared panel;

-   mask deletion is refuted only as a uniformly negligible operation on that finite panel.

We do *not* claim a source-uniform arithmetic $L^2$ estimate, a uniform bound for the masked operator, a growing defect lower bound, a fixed-power payment, Route-B reassembly, or a twin-prime conclusion. The official Session-named Route-A/Route-B evaluator files are absent from this checkout; the local bridge is explicitly fail-closed.

# Conclusion and next question

TPC-348 turns the mask-defect observation into a reusable finite interface: literal block $\to$ two-sided projection defect $\to$ mask-hit set $\to$ coordinate lower witness. The result shows that a position-aware defect cannot be dismissed by an unstructured finite remainder argument on the declared grid. The next minimal question is whether a prime-balanced signed combination of hit coordinates produces additional structure that survives the same hostile controls. Until such a result exists, the source-native arithmetic $L^2$ gate remains open.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{conway2000,
  author    = {John B. Conway},
  title     = {A Course in Functional Analysis},
  edition   = {2},
  publisher = {Springer},
  year      = {2000}
}
```

<!-- SOURCE_BODY_END -->
