# Prime-Balanced Signed Incidence Witnesses\ for a Literal Prime-Shell Mask Defect

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2, 2026
- Source repository commit: `1de1964aa411aa631587da690524beadf1127d3c`
- Converter: `source-markdown-audit-v2`

## Abstract

We continue the literal masked prime-shell analysis of TPC-348. Rather than testing one mask-hit coordinate at a time, we assign equal total positive and negative mass to the ordered shell primes and sum all divisibility incidences. The resulting deterministic vector has an exact cross-prime Gram expansion. For a nonzero incidence vector $b_I$ and the defect block $D_I$, the induced Euclidean norm obeys $$\|D_I\|_{2\to2}\geq \frac{\|D_Ib_I\|_2}{\|b_I\|_2}.$$ On the locked two-origin, three-count, four-anchor, two-exponent, four-law panel, all 192 signed vectors are nonzero and have positive response. The signed response is $0.39083565842$–$0.954375010719$ of the defect spectral norm, exceeds the best mask-hit coordinate baseline on 136 rows, and reaches one half of that norm on 175 rows. The comparison is not uniform: the signed vector loses to the coordinate baseline on 56 rows. These are finite observations, not a growing arithmetic estimate; the source-uniform masked $L^2$ problem and the twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

TPC-348 localized the divisibility-mask defect with an exact coordinate lower witness. The next minimal question is whether the shell itself supplies a natural signed combination of hit coordinates that exposes cross-prime structure. We study one rule fixed before the finite audit: an equal positive and negative split of the ordered shell, with a neutral middle prime when the shell length is odd.

The exact algebra below is finite-dimensional. The numerical table is a declared panel audit only. In particular, no statement here supplies a source-native arithmetic vector, a uniform-in-$x$ estimate, a fixed power of $x$, a Route-B reassembly, or a proof of the twin-prime conjecture.

# The literal masked object

Let $I=\{o,o+1,\ldots,o+M-1\}$, let $R_I$ be restriction, and let $E_I$ be zero extension. For an active shell prime $p$, write $$(P_pf)(n)=\mathbf 1_{p\nmid n}f(n)$$ for the divisibility projection. With the same kernel normalization as the parent releases, the physical and unmasked blocks are $$\begin{aligned}
 A_I&=\sum_p\varepsilon_pR_IP_pK_pP_pE_I,\\
 T_I&=R_I\left(\sum_p\varepsilon_pK_p\right)E_I,
 \qquad D_I=A_I-T_I.\end{aligned}$$ The source signs $\varepsilon_p$ belong to the frozen four-law protocol. The new test vector below has its own declared coefficients $\beta_j$; conflating these two sign systems would change the object.

# Prime balance and the exact Gram interface

Order the shell as $p_0<p_1<\cdots<p_{r-1}$ and put $m=\lfloor r/2\rfloor$. Define $$\beta_j=\begin{cases}
  +1,&0\leq j<m,\\
  0,&m\leq j<r-m,\\
  -1,&r-m\leq j<r.
 \end{cases}$$ Thus there are equally many positive and negative coefficients, and at most one neutral coefficient. For $t\in I$, let $$h_{p_j,I}(t)=\mathbf 1_{p_j\mid t},\qquad
 b_I=\sum_{j=0}^{r-1}\beta_jh_{p_j,I}.$$ At a multiply-divisible position, all active incidences are added; this is an incidence contrast rather than an exclusive owner-class assignment. Whenever $b_I\ne0$, set $x_I=b_I/\|b_I\|_2$.

> **Proposition: prime balance** The coefficient vector satisfies $\sum_j\beta_j=0$ and has equal positive and negative support.

> **Proof** The first and last blocks each have $m$ indices and are disjoint. The middle block has size $r-2m\in\{0,1\}$. Summing the coefficients proves the claim.

> **Proposition: prime-incidence Gram identity** For every finite matrix $D_I$, $$\|D_Ib_I\|_2^2
>  =\sum_{j,k}\beta_j\beta_k
>    \langle D_Ih_{p_j,I},D_Ih_{p_k,I}\rangle.
>  \label{eq:gram}$$

> **Proof** By definition $b_I=\sum_j\beta_jh_{p_j,I}$. Apply linearity of $D_I$ and expand the Euclidean inner product. The sum is finite, so no convergence assumption is involved.

> **Theorem: signed-incidence lower witness** If $b_I\ne0$, then $$\|D_I\|_{2\to2}\geq
>  \frac{\|D_Ib_I\|_2}{\|b_I\|_2}.
>  \label{eq:lower}$$

> **Proof** The vector $x_I=b_I/\|b_I\|_2$ is a unit vector. Substitution into the definition of the induced Euclidean norm `\cite{conway2000}` gives $$\|D_I\|_{2\to2}=\sup_{\|x\|_2=1}\|D_Ix\|_2
>  \geq \|D_Ix_I\|_2,$$ which is ([\[eq:lower\]](main.tex#L133){reference-type="ref" reference="eq:lower"}).

> **Remark** The theorem is exact finite linear algebra. It does not say that the Gram cross terms in ([\[eq:gram\]](main.tex#L118){reference-type="ref" reference="eq:gram"}) have a common sign or that the balanced vector is close to a leading eigenvector.

# Frozen audit protocol

The producer locks the TPC-348 code and certificate. We retain $$o\in\{40097,48097\},\quad M\in\{256,512,1024\},\quad
 Q\in\{24,36,54,80\},\quad s\in\{1,2\},$$ with height $H=66$ and the four source sign laws `all_plus`, `alternating_index`, `mod4_character`, and `half_split`. There are $2\cdot3\cdot4\cdot2\cdot4=192$ rows.

For each row we form $D_I$, the incidence vector $b_I$, its normalized response, and the TPC-348 coordinate baseline $$C_I=\max_{t\in J_I}\|D_Ie_t\|_2,
 \qquad J_I=\{t\in I:\exists p\mid t\}.$$ The baseline is used only for a finite comparison. The independent checker reverses the shell accumulation order, recomputes all row metrics, and checks the exact multi-hit anchor. The stress suite mutates the coefficient rule, incidence support, census, range, anchor, and firewall.

# Finite results

Table [1](main.tex#L186){reference-type="ref" reference="tab:summary"} reports the canonical certificate. The denominator $\|T_I\|$ is the unmasked ideal comparison, while $\|D_I\|$ is the defect spectral norm.

<div id="tab:summary">

| Quantity                        | Certified finite readout           |
|:--------------------------------|:-----------------------------------|
| Rows                            | $192$                              |
| Nonzero signed vectors          | $192/192$                          |
| Positive signed responses       | $192/192$                          |
| Signed support per row          | $28$–$150$                         |
| Incidence Gram records          | $192$                              |
| Maximum Gram replay discrepancy | $1.06581410364\times10^{-14}$      |
| $\|D_Ix_I\|/\|D_I\|$            | $0.39083565842$–$0.954375010719$   |
| $\|D_Ix_I\|/\|T_I\|$            | $0.0125941959067$–$0.430061305156$ |
| $\|D_Ix_I\|/C_I$                | $0.542800508699$–$2.04702542827$   |
| Baseline beaten                 | $136/192$                          |
| At least half the defect norm   | $175/192$                          |

: TPC-349 prime-balanced signed-incidence audit.

</div>

The signed vector is often stronger than the best single coordinate, but the comparison is not uniform: 56 rows do not beat $C_I$. This is why the claim ledger marks a universal balanced-gain statement as `REFUTED_SCOPED`. The response/defect ratio itself is a valid finite lower-witness ratio because of Theorem [\[eq:lower\]](main.tex#L133){reference-type="ref" reference="eq:lower"}; its persistence on growing panels is a separate open question.

## Exact multi-hit anchor

Take $I=\{1,\ldots,14\}$, $Q=4$, exponent one, and all-plus source signs. The shell is $(5,7)$ and $\beta=(1,-1)$. The exact incidence vector is $$b_I=(0,0,0,0,1,0,-1,0,0,1,0,0,0,-1),
 \qquad \|b_I\|_2^2=4.$$ The exact squared norm of its defect image is $$\|D_Ib_I\|_2^2=
 \frac{1580136191762341638715051100269721298390649257672312877072677225319}
 {4277374121662663268940652066711233824047030196831076541809000000}.$$ The canonical certificate also stores the exact image-vector digest. This anchor includes positions divisible by both shell primes in the interval and therefore tests the incidence sum rather than a one-hit shortcut.

# Adversarial checks and claim boundary

The normal and optimized producer outputs agree byte-for-byte. The reverse shell replay agrees with every stored metric within its declared floating tolerance, and the stress mutations reject a wrong beta split, an owner-only incidence vector, a changed census, a false universal-gain flag, a changed range, and a changed parent lock. These checks establish package integrity; they are not additional arithmetic theorems.

The strongest exact statements are the zero-sum coefficient identity, the incidence Gram expansion, and the normalized induced-norm lower witness. The strongest finite observation is the 136/192 baseline improvement. The main obstruction is that this improvement is not universal even on the declared panel. We claim neither a source-uniform masked operator bound nor an arithmetic $L^2$ cancellation estimate. The Session-named Route-A/Route-B evaluator files are absent from this checkout; the local bridge is explicitly fail-closed.

# Conclusion and next question

TPC-349 supplies a reusable interface $$\text{ordered shell}\;\longrightarrow\;\text{zero-sum beta}
 \longrightarrow\text{incidence contrast}\longrightarrow\text{prime Gram}
 \longrightarrow\text{finite norm witness}.$$ It demonstrates substantial finite response while exposing the limit of a single balanced rule: no uniform gain follows. The next minimal question is whether the signed incidence Gram persists under fresh growing panels and whether its cross-prime terms can be bounded without discarding the literal masks.

# References

1 John B. Conway. *A Course in Functional Analysis*. Springer, 2nd edition, 2000.

<!-- SOURCE_BODY_END -->
