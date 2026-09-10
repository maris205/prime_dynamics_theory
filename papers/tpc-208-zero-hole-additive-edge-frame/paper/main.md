# **A Canonical Additive Edge Frame for Zero-Hole\ Reduced-Residue BDH Remainders**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We identify the exact additive-frequency geometry of the standard-zero-hole reduced-residue Barban–Davenport–Halberstam remainder. For a prime modulus $q$, the zero-hole variance is $q^{-1}y^*P_{q-1}y$, where $y$ contains the $q-1$ nonzero additive Fourier coefficients and $P_{q-1}$ projects off their constant direction. The complete-graph Laplacian turns this projection into a tight frame of $(q-1)(q-2)/2$ literal two-frequency differences. The same edge cells distribute the mandatory $(q-2)/(q-1)$ coefficient diagonal exactly, leaving a pure coefficient-off-diagonal remainder in every cell. Four-packet complex polarization is then edgewise, and contraction of the frame recovers the original physical residue kernel with no normalization change. We also prove a scoped uniqueness theorem: every scalar-weighted representation by literal vectors $e_k-e_l$ must use every edge with weight $1/(q-1)$, so no strict edge subset represents the projection. A residue-zero spike refutes separate absolute estimates of equal and unequal frequencies: the two pieces are nonzero, opposite, and sum to zero. An independent exact certificate checks 431 finite identities for $q=2,3,5,7,11$. The result is structural: it creates an additive pre-emitter, not a Kloosterman attachment or a prime-shell power saving.

<!-- SOURCE_BODY_BEGIN -->

=2em

# Introduction and claim firewall

The prime-dynamics Gate-B reduction studied in the preceding stages produces a signed, prime-modulus, kernel-localized reduced-residue variance. Complex polarization converts its two-sequence scalar into four one-sequence remainders, but the coefficient diagonal must be subtracted with the exact factor $q-2$ before the packet signs are reassembled `\cite{Wang2026V59}`. Translating a physical block changes the distinguished deleted residue; the moving-hole correction has already been isolated and paid at the critical $1/96$ clock `\cite{Wang2026TPC207}`. The remaining arithmetic object is therefore the standard-zero-hole remainder itself.

A first additive-Fourier attempt would split that remainder into equal- and unequal-frequency terms and estimate them separately. This order is invalid. For a row supported only at residue zero, the true zero-hole variance is zero, whereas the two proposed pieces have equal nonzero magnitude and opposite sign. Taking absolute values before their cancellation manufactures a large term from an exact zero.

The stable object is the complete-graph Laplacian on the nonzero additive frequencies. It retains the constant-direction cancellation internally and simultaneously distributes the mandatory coefficient diagonal. The paper’s contributions are the following.

1.  We prove that the zero-hole variance is $q^{-1}y^*P_{q-1}y$ and give its exact complete-graph tight-frame expansion. The frame has rank $q-2$, $(q-1)(q-2)/2$ edge vectors, and redundancy $(q-1)/2$ for $q>2$.

2.  We prove the edge-mass identity $\sum_e|\Delta_e(n)|^2=q(q-2)\mathbf 1_{q\nmid n}$. It places the $(q-2)/(q-1)$ coefficient diagonal inside the same edge cells, so every emitted cell is coefficient-off-diagonal before any estimate.

3.  We lift the four-packet polarization edge by edge, recover the frozen physical residue kernel exactly, and expose an oriented $(d,k)$ difference fiber with the unit-annihilating factor $1-\mathrm e_q(-dn)$.

4.  We prove that a scalar-weighted decomposition by literal two-frequency differences is unique. Every edge is forced, which rules out edge-subset sparsification and identifies the collective source theorem that is still missing.

All four items are finite-dimensional identities proved for every prime $q$ and every finitely supported complex sequence. They do not estimate the edge cells. In particular, the paper does not prove a prime-only Barban–Davenport–Halberstam asymptotic, attach the cells to a Kloosterman theorem, pay the full strict $1/400$ Gate-B margin, establish an arithmetic $L^2$ statement, earn fixed-atom credit, or prove a twin-prime theorem.

# The frozen zero-hole row

Let $q$ be prime and put $$\mathrm e_q(t)=\exp(2\pi i t/q),\qquad \mathrm e(t)=\exp(2\pi i t).$$ Let $a=(a_n)$ be a finitely supported complex sequence, let $H>0$, and let $v\in\mathbb R$. Write $$\label{eq:residue-row}
 x_n(v)=a_n\mathrm e(vn/H),\qquad
 A_r(a;v)=\sum_{n\equiv r\; (\mathrm{mod}\ q)}x_n(v).$$ The mean over the $q-1$ retained residues and the standard-zero-hole variance are $$\label{eq:zero-hole-variance}
 \overline A^{\times}=\frac1{q-1}\sum_{r\ne0}A_r,
 \qquad
 V_0(a;v)=\sum_{r\ne0}|A_r-\overline A^{\times}|^2.$$ The mandatory coefficient diagonal and its remainder are $$\label{eq:diagonal-remainder}
 D_0(a)=\frac{q-2}{q-1}\sum_{q\nmid n}|a_n|^2,
 \qquad R_0(a;v)=V_0(a;v)-D_0(a).$$ The physical Gate-B row carries the outer factor $qR_0$, not merely $R_0$.

We use the additive transform $$\label{eq:dft}
 \widehat A(k)=\sum_{r\bmod q}A_r\mathrm e_q(-kr)
 =\sum_n a_n\mathrm e(vn/H)\mathrm e_q(-kn).$$ This convention is fixed throughout. No multiplicative character, inverse residue, or asymptotic estimate enters the frame construction.

# Zero-hole projection in additive frequency

Set $d=q-1$, enumerate the nonzero frequencies, and define $$\label{eq:projection}
 y=(\widehat A(k))_{k\in\mathbb F_q^\times}\in\mathbb C^d,
 \qquad P_d=I_d-\frac1d\mathbf 1\mathbf 1^*.$$

> **Theorem: zero-hole frequency projection**<span id="thm:projection" label="thm:projection">\[thm:projection\]</span> For every prime $q$, every finitely supported complex sequence $a$, and every real $v$, $$\label{eq:projection-identity}
>  \boxed{V_0(a;v)=\frac1q\,y^*P_dy.}$$ Moreover, $P_d$ is an orthogonal projection of rank $q-2$. For $q=2$ both sides of [\[eq:projection-identity\]](main.tex#L158){reference-type="eqref" reference="eq:projection-identity"} vanish.

> **Proof** For a general row $z=(z_r)_{r\bmod q}$, let $\mu=q^{-1}\sum_rz_r$ and let $V_{\rm all}=\sum_r|z_r-\mu|^2$. Deleting coordinate zero and recentering the retained coordinates gives the elementary leave-one-out identity $$\label{eq:leave-one-out}
>  \sum_{r\ne0}\left|z_r-\frac1{q-1}\sum_{s\ne0}z_s\right|^2
>  =V_{\rm all}-\frac q{q-1}|z_0-\mu|^2.$$ Indeed, the retained mean equals $\mu-(z_0-\mu)/(q-1)$; expanding around $\mu$ proves [\[eq:leave-one-out\]](main.tex#L170){reference-type="eqref" reference="eq:leave-one-out"}.
>
> Apply this identity to $z_r=A_r$. Parseval and Fourier inversion yield $$\label{eq:parseval-inversion}
>  V_{\rm all}=\frac1q\sum_{k\ne0}|\widehat A(k)|^2,
>  \qquad
>  A_0-\mu=\frac1q\sum_{k\ne0}\widehat A(k).$$ Substitution gives $$\label{eq:projection-expanded}
>  V_0=\frac1q\sum_{k\ne0}|\widehat A(k)|^2
>  -\frac1{q(q-1)}\left|\sum_{k\ne0}\widehat A(k)\right|^2,$$ which is [\[eq:projection-identity\]](main.tex#L158){reference-type="eqref" reference="eq:projection-identity"}. The matrix $P_d$ projects onto $\mathbf 1^\perp$, so its rank is $d-1=q-2$. When $q=2$, $d=1$ and $P_d=0$.

The null direction in Theorem [\[thm:projection\]](main.tex#L155){reference-type="ref" reference="thm:projection"} is essential. A vector whose nonzero Fourier coordinates are all equal contributes no zero-hole variance, even if its Euclidean norm is large.

# The complete-graph tight frame

Let $K_d$ be the complete graph on the nonzero-frequency vertices. For an unordered edge $e=\{k,l\}$ define $$\label{eq:edge-vector}
 g_e=e_k-e_l,
 \qquad
 \Delta_{k,l}(n)=\mathrm e_q(-kn)-\mathrm e_q(-ln).$$ The graph Laplacian is $$\label{eq:laplacian}
 \sum_{e\in E(K_d)}g_eg_e^*=dI_d-\mathbf 1\mathbf 1^*=dP_d.$$

> **Theorem: canonical additive edge frame**<span id="thm:edge-frame" label="thm:edge-frame">\[thm:edge-frame\]</span> For every object in Theorem [\[thm:projection\]](main.tex#L155){reference-type="ref" reference="thm:projection"}, $$\label{eq:edge-frame}
>  \boxed{
>  V_0(a;v)=\frac1{q(q-1)}
>  \sum_{\{k,l\}\in E(K_{q-1})}
>  \left|\sum_n a_n\mathrm e(vn/H)\Delta_{k,l}(n)\right|^2.}$$ The edge family contains $(q-1)(q-2)/2$ vectors and spans a space of dimension $q-2$. For $q>2$ its frame redundancy is $(q-1)/2$.

> **Proof** The edge transform is $$\label{eq:edge-transform}
>  T_e[a](v)=\langle g_e,y\rangle
>  =\widehat A(k)-\widehat A(l)
>  =\sum_na_n\mathrm e(vn/H)\Delta_{k,l}(n).$$ Contracting [\[eq:laplacian\]](main.tex#L207){reference-type="eqref" reference="eq:laplacian"} with $y$ gives $\sum_e|T_e[a](v)|^2=d\,y^*P_dy$. Theorem [\[thm:projection\]](main.tex#L155){reference-type="ref" reference="thm:projection"} and $d=q-1$ prove [\[eq:edge-frame\]](main.tex#L213){reference-type="eqref" reference="eq:edge-frame"}. The count and redundancy follow from the complete graph and the rank of $P_d$. For $q=2$ the edge set is empty.

The redundancy in Theorem [\[thm:edge-frame\]](main.tex#L211){reference-type="ref" reference="thm:edge-frame"} is exact bookkeeping. It is not a power saving and does not permit a triangle inequality over the edge set. Section [7](main.tex#L406){reference-type="ref" reference="sec:uniqueness"} will show that every literal edge is forced in a scalar-weighted representation of this projection.

# Exact edgewise diagonal deletion

Each edge difference annihilates the excluded residue: $$\label{eq:zero-residue-annihilation}
 q\mid n\quad\Longrightarrow\quad \Delta_{k,l}(n)=0.$$ The total edge mass on a unit residue is also exact.

> **Lemma: edge mass**<span id="lem:edge-mass" label="lem:edge-mass">\[lem:edge-mass\]</span> For every integer $n$, $$\label{eq:edge-mass}
>  \boxed{
>  \sum_{e\in E(K_{q-1})}|\Delta_e(n)|^2
>  =q(q-2)\mathbf 1_{q\nmid n}.}$$

> **Proof** If $q\mid n$, [\[eq:zero-residue-annihilation\]](main.tex#L244){reference-type="eqref" reference="eq:zero-residue-annihilation"} proves the claim. Suppose $q\nmid n$ and put $u(n)=(\mathrm e_q(-kn))_{k\ne0}$. Then $\|u(n)\|_2^2=q-1$ and $\langle\mathbf 1,u(n)\rangle=\sum_{k\ne0}\mathrm e_q(-kn)=-1$. Therefore $$\begin{aligned}
>  \sum_e|\langle g_e,u(n)\rangle|^2
>  &=u(n)^*\bigl((q-1)I-\mathbf 1\mathbf 1^*\bigr)u(n)\\
>  &=(q-1)^2-1=q(q-2).\end{aligned}$$

Define the edge diagonal and edge remainder by $$\label{eq:edge-diagonal}
 D_e[a]=\sum_n|a_n|^2|\Delta_e(n)|^2,
 \qquad
 \mathcal E_e^\circ[a](v)=|T_e[a](v)|^2-D_e[a].$$ Expanding the square removes the coefficient diagonal inside each cell: $$\label{eq:pure-off-diagonal}
 \boxed{
 \mathcal E_e^\circ[a](v)=
 \sum_{t\ne u}a_t\overline{a_u}\mathrm e(v(t-u)/H)
 \Delta_e(t)\overline{\Delta_e(u)}.}$$

> **Corollary: zero-hole off-diagonal edge compiler** <span id="cor:edge-compiler" label="cor:edge-compiler">\[cor:edge-compiler\]</span> The diagonal in [\[eq:diagonal-remainder\]](main.tex#L133){reference-type="eqref" reference="eq:diagonal-remainder"} distributes over the edge frame without an error: $$\label{eq:diagonal-distribution}
>  \frac1{q(q-1)}\sum_eD_e[a]
>  =\frac{q-2}{q-1}\sum_{q\nmid n}|a_n|^2=D_0(a).$$ Consequently, $$\label{eq:edge-remainder}
>  \boxed{
>  R_0(a;v)=\frac1{q(q-1)}\sum_e\mathcal E_e^\circ[a](v),
>  \qquad
>  qR_0(a;v)=\frac1{q-1}\sum_e\mathcal E_e^\circ[a](v).}$$

> **Proof** Sum [\[eq:edge-diagonal\]](main.tex#L272){reference-type="eqref" reference="eq:edge-diagonal"} over edges and apply Lemma [\[lem:edge-mass\]](main.tex#L249){reference-type="ref" reference="lem:edge-mass"}. Subtract the result from Theorem [\[thm:edge-frame\]](main.tex#L211){reference-type="ref" reference="thm:edge-frame"}. The second identity retains the mandatory physical outer factor $q$.

Corollary [\[cor:edge-compiler\]](main.tex#L286){reference-type="ref" reference="cor:edge-compiler"} is the main local improvement over a bare Fourier decomposition. The frame geometry and coefficient-diagonal cancellation now occupy the same cell; neither has to be recovered after an absolute estimate.

# Polarization and the physical kernel

For two finitely supported sequences $\beta,w$, define the bilinear edge cell $$\label{eq:bilinear-edge-cell}
 \mathcal E_e^\circ(\beta,w;v)
 =T_e[\beta](v)\overline{T_e[w](v)}
 -\sum_n\beta(n)\overline{w(n)}|\Delta_e(n)|^2.$$ It has the pure off-diagonal expansion $$\label{eq:bilinear-off-diagonal}
 \mathcal E_e^\circ(\beta,w;v)
 =\sum_{t\ne u}\beta(t)\overline{w(u)}\mathrm e(v(t-u)/H)
 \Delta_e(t)\overline{\Delta_e(u)}.$$

> **Proposition: edgewise four-packet polarization** <span id="prop:polarization" label="prop:polarization">\[prop:polarization\]</span> Let $a^{(j)}=\beta+i^jw$ for $j=0,1,2,3$. Then, for every edge, $$\label{eq:edge-polarization}
>  \boxed{
>  \frac14\sum_{j=0}^3i^j\mathcal E_e^\circ[a^{(j)}](v)
>  =\mathcal E_e^\circ(\beta,w;v).}$$

> **Proof** For complex $x,y$, $x\overline y=\frac14\sum_{j=0}^3i^j|x+i^jy|^2$. Apply this identity first to $T_e[\beta],T_e[w]$ and then pointwise to $\beta(n),w(n)$. Subtracting the two polarized identities gives [\[eq:edge-polarization\]](main.tex#L332){reference-type="eqref" reference="eq:edge-polarization"}.

Let $\psi_+$, the prime shell $\mathcal Q$, and the literal sequences $\beta,w$ be the frozen V59 objects. Corollary [\[cor:edge-compiler\]](main.tex#L286){reference-type="ref" reference="cor:edge-compiler"}, summed before any outer absolute value, gives the exact physical normal form $$\label{eq:physical-scalar}
 \boxed{
 \mathfrak C_x=
 \int_{\mathbb R}\psi_+(v)
 \sum_{q\in\mathcal Q}\frac1{q-1}
 \sum_{e\in E(K_{q-1})}\mathcal E_e^\circ(\beta,w;v)\,dv.}$$ The ordered block decomposition also commutes with [\[eq:physical-scalar\]](main.tex#L350){reference-type="eqref" reference="eq:physical-scalar"}: replace $\beta,w$ by each ordered pair $\beta_b,w_c$ and sum over $(b,c)$ before applying an absolute value. If the $v$-integral is evaluated first, its kernel $K_H$ produces the additive pre-emitter $$\label{eq:pre-emitter}
 \sum_{t\ne u}\beta_b(t)\overline{w_c(u)}K_H(u-t)
 \Delta_e(t)\overline{\Delta_e(u)}.$$ Equation [\[eq:pre-emitter\]](main.tex#L362){reference-type="eqref" reference="eq:pre-emitter"} is not yet a Kloosterman cell.

The following contraction verifies every residue coefficient in [\[eq:physical-scalar\]](main.tex#L350){reference-type="eqref" reference="eq:physical-scalar"}. For $r,s\bmod q$, put $$\label{eq:physical-kernel-definition}
 \mathcal K_q(r,s)=\sum_e
 (\mathrm e_q(-kr)-\mathrm e_q(-lr))(\mathrm e_q(ks)-\mathrm e_q(ls)).$$

> **Proposition: physical-kernel crosswalk**<span id="prop:physical-kernel" label="prop:physical-kernel">\[prop:physical-kernel\]</span> The edge contraction is $$\label{eq:physical-kernel}
>  \boxed{
>  \mathcal K_q(r,s)=
>  \begin{cases}
>  0,&rs\equiv0\pmod q,\\
>  q(q-2),&r=s\ne0,\\
>  -q,&r,s\ne0,\ r\ne s.
>  \end{cases}}$$ Hence, on unit residues, $$\label{eq:literal-crosswalk}
>  \frac{\mathcal K_q(r,s)}{q-1}
>  =q\left(\mathbf1_{r=s}-\frac1{q-1}\right),$$ which is the original V59 coefficient.

> **Proof** If either residue is zero, every edge difference on that coordinate vanishes. For nonzero $r,s$, use [\[eq:laplacian\]](main.tex#L207){reference-type="eqref" reference="eq:laplacian"} with $u(r)=(\mathrm e_q(-kr))_{k\ne0}$. The diagonal case is $(q-1)^2-1=q(q-2)$ as in Lemma [\[lem:edge-mass\]](main.tex#L249){reference-type="ref" reference="lem:edge-mass"}. If $r\ne s$, additive orthogonality gives $\langle u(s),u(r)\rangle=-1$, while both coordinate sums equal $-1$; contraction with $(q-1)I-\mathbf 1\mathbf 1^*$ therefore gives $(q-1)(-1)-1=-q$. Dividing by $q-1$ proves [\[eq:literal-crosswalk\]](main.tex#L387){reference-type="eqref" reference="eq:literal-crosswalk"}.

# Oriented difference fibers and uniqueness

Write $l=k+d$ in $\mathbb F_q$. Counting each unordered edge in both orientations gives $$\label{eq:oriented-sum}
 \sum_{e\in E(K_{q-1})}\mathcal E_e^\circ
 =\frac12\sum_{d\in\mathbb F_q^\times}
 \sum_{\substack{k\in\mathbb F_q^\times\\k\ne-d}}
 \mathcal E_{k,k+d}^\circ.$$ The edge factor separates as $$\label{eq:difference-fiber}
 \boxed{
 \Delta_{k,k+d}(n)=\mathrm e_q(-kn)\bigl(1-\mathrm e_q(-dn)\bigr).}$$ Thus [\[eq:physical-scalar\]](main.tex#L350){reference-type="eqref" reference="eq:physical-scalar"} is equivalently $$\label{eq:oriented-physical-scalar}
 \mathfrak C_x=
 \int\psi_+(v)\sum_{q\in\mathcal Q}\frac1{2(q-1)}
 \sum_{d\ne0}\sum_{k\ne0,-d}
 \mathcal E_{k,k+d}^\circ(\beta,w;v)\,dv.$$ The base twist $k$ and the unit-annihilating difference factor in [\[eq:difference-fiber\]](main.tex#L417){reference-type="eqref" reference="eq:difference-fiber"} are the preferred interface for a future Poisson/Kloosterman compiler. The factor $1/2$ and the exclusion $k=-d$ are mandatory.

The complete edge family cannot be reduced within its literal class.

> **Theorem: literal-edge no-sparsification**<span id="thm:no-sparsification" label="thm:no-sparsification">\[thm:no-sparsification\]</span> Let $d\ge1$. Suppose scalar weights $w_{k,l}\in\mathbb C$ satisfy $$\label{eq:weighted-edge-decomposition}
>  P_d=\sum_{1\le k<l\le d}
>  w_{k,l}(e_k-e_l)(e_k-e_l)^*.$$ Then $$\label{eq:forced-edge-weight}
>  \boxed{w_{k,l}=\frac1d=\frac1{q-1}}$$ for every edge. In particular, no strict subset of literal two-frequency differences represents $P_d$ with scalar edge weights.

> **Proof** For $k\ne l$, the $(k,l)$ entry of $P_d$ is $-1/d$. On the right side of [\[eq:weighted-edge-decomposition\]](main.tex#L437){reference-type="eqref" reference="eq:weighted-edge-decomposition"}, only the outer product belonging to $\{k,l\}$ has a nonzero $(k,l)$ entry, and that entry is $-w_{k,l}$. Hence $w_{k,l}=1/d$ for every pair. With these weights the diagonal entries agree automatically by the complete-graph identity.

The scope in Theorem [\[thm:no-sparsification\]](main.tex#L435){reference-type="ref" reference="thm:no-sparsification"} matters. It excludes neither a dense orthonormal basis of $\mathbf 1^\perp$, a signed higher-rank cell system, nor an arithmetic theorem that estimates the full redundant frame jointly. It says that deleting literal edges and repairing their weights cannot be the next compiler.

# Sharp falsifiers and mutation boundaries

## Equal/off-equal estimation is unstable

Take $A_0=L$ and $A_r=0$ for every $r\ne0$. The retained row is zero, so $V_0=0$. On the other hand, $\widehat A(k)=L$ for every $k\ne0$, and the two terms in [\[eq:projection-expanded\]](main.tex#L185){reference-type="eqref" reference="eq:projection-expanded"} are $$\label{eq:spike-equal}
 \frac1q\sum_{k\ne0}|\widehat A(k)|^2
 =\frac{q-1}{q}|L|^2,$$ $$\label{eq:spike-off-equal}
 -\frac1{q(q-1)}\left|\sum_{k\ne0}\widehat A(k)\right|^2
 =-\frac{q-1}{q}|L|^2.$$ Separate absolute estimates lose their exact cancellation. Every edge difference in Theorem [\[thm:edge-frame\]](main.tex#L211){reference-type="ref" reference="thm:edge-frame"} instead vanishes before an estimate is taken. This fixture refutes the proposed estimate order, not the valid algebraic split in [\[eq:projection-expanded\]](main.tex#L185){reference-type="eqref" reference="eq:projection-expanded"}.

## One coefficient cancels cellwise

If $a$ has one nonzero coefficient at a unit residue, then $|T_e[a]|^2=D_e[a]$ for every edge. Thus $\mathcal E_e^\circ[a]=0$ edge by edge. A global diagonal subtraction that leaves nonzero individual cells would fail this local test.

## Mandatory factors

Several nearby formulas describe different objects.

-   Summing oriented edges without the factor $1/2$ doubles the scalar.

-   Including frequency zero replaces $K_{q-1}$ by $K_q$ and produces an all-residue projection rather than the zero-hole row.

-   Replacing $q-1$ by $q$ changes every off-diagonal projection entry and violates Theorem [\[thm:no-sparsification\]](main.tex#L435){reference-type="ref" reference="thm:no-sparsification"}.

-   Omitting $D_e[a]$ returns a positive variance, not the signed coefficient-off-diagonal remainder.

-   Dropping one literal edge changes exactly one pair of off-diagonal matrix entries and cannot be repaired by reweighting other edges.

These mutations are included in the exact checker. Their rejection protects the physical signs and normalization; it does not supply arithmetic evidence.

# Source boundary and related analytic engines

The additive edge frame is an upstream representation theorem. Three nearby analytic sources clarify what remains to be proved.

#### General-sequence BDH architecture.

Harper proves simple Barban–Davenport–Halberstam type asymptotics for broad classes of general sequences under explicit Progressions, Non-concentration, and further structural hypotheses `\cite{Harper2024}`. For prime moduli, grouping reduced residues naturally leads to a zero-hole variance. The source does not state [\[eq:physical-scalar\]](main.tex#L350){reference-type="eqref" reference="eq:physical-scalar"}, verify its hypotheses uniformly for the four literal prime-dynamics packets, select the prime subset after the signed diagonal subtraction, or perform the ordered block reassembly. The present paper neither invokes nor disproves Harper’s theorem; it gives an exact local normal form for testing a future attachment.

#### Post-emitter Kloosterman bounds.

Blomer and Pascadi obtain strong bounds for bilinear forms with Kloosterman sums, including the critical fixed-modulus saving used in the route ledger `\cite{BlomerPascadi2026}`. Their theorem accepts an already emitted form with source-valid coefficient arrays. The additive expression [\[eq:pre-emitter\]](main.tex#L362){reference-type="eqref" reference="eq:pre-emitter"} has not been transformed into those arrays. In particular, the complete $(d,k)$ frame, four packet signs, prime shell, block norms, and one final reassembly cannot be supplied by renaming [\[eq:pre-emitter\]](main.tex#L362){reference-type="eqref" reference="eq:pre-emitter"} a Kloosterman cell.

#### Exceptional-spectrum and sparse-Fourier machinery.

Pascadi’s large-sieve framework for exceptional Maass forms supplies powerful sparse-Fourier and incomplete-Kloosterman tools after the relevant transform and norm hypotheses have been established `\cite{Pascadi2026LargeSieve}`. Here those hypotheses are precisely part of the open compiler. The source is a plausible downstream engine, not evidence that the edge pre-emitter already meets its input contract.

#### Bounded novelty claim.

The complete-graph Laplacian identity is standard finite-dimensional linear algebra. A bounded arXiv metadata search on 17 August 2026 found no direct match for the combinations “reduced residue and graph Laplacian,” “BDH and additive Fourier,” or “leave-one-out variance and Fourier.” Such a query does not prove literature-wide novelty. The claim made here is narrower: the exact attachment to the frozen zero-hole remainder, edgewise distribution of its mandatory diagonal, physical-kernel crosswalk, and scoped uniqueness of its literal two-frequency representation.

# Exact computational certificate

The accompanying producer works with Gaussian rationals and prime cyclotomic coefficient vectors. For $q=2,3,5,7,11$, it checks the complete-graph Laplacian entrywise, reduces every physical-kernel entry exactly, compares direct and emitted variances on deterministic complex rows, verifies complex polarization, and exercises the spike and edge-weight falsifiers. The independent checker imports neither the producer nor its mathematical module; it reconstructs the projection and closed physical kernel from separate formulas.

The canonical certificate contains 431 exact mathematical rows:

| Check family                              |  Exact rows|
|:------------------------------------------|-----------:|
| Laplacian entries, edge counts, and ranks |         167|
| Physical residue kernel                   |         208|
| Row variance and diagonal normalization   |          20|
| Complex polarization                      |           2|
| Falsifiers and literal-edge uniqueness    |          20|
| Explicit mutation checks                  |          14|
| Total                                     |         431|

Both programs use explicit failures rather than optimization-sensitive assertions, reject duplicate JSON keys and nonfinite values at their trust boundaries, and reproduce byte-identical output in normal and optimized Python modes. These computations detect transcription and normalization mutations. The proofs in Sections 3–7, not the finite table, establish the general identities.

# Route consequence and open theorem

Table [1](main.tex#L596){reference-type="ref" reference="tab:status"} separates the completed structural layer from the unpaid arithmetic layer.

<div id="tab:status">

| Statement                                        | Status           |
|:-------------------------------------------------|:-----------------|
| Zero-hole projection and complete-graph frame    | `PROVED`         |
| Edgewise $(q-2)$ diagonal deletion               | `PROVED`         |
| Physical-kernel and four-packet crosswalk        | `PROVED`         |
| No strict literal-edge subset representation     | `PROVED`, scoped |
| Separate absolute equal/off-equal estimates      | `REFUTED`        |
| Whole-frame Poisson/Kloosterman emission         | `OPEN`           |
| Prime-shell fixed saving greater than $1/400$    | `OPEN / UNPAID`  |
| Arithmetic advance, fixed atom, or $L^2$ theorem | `NONE`           |

: Claim status for the zero-hole additive edge route.

</div>

The smallest next theorem is now explicit.

> **Open collective compiler.** Apply Möbius and Poisson or Voronoi transformations to the complete oriented $(d,k)$ frame in [\[eq:oriented-physical-scalar\]](main.tex#L422){reference-type="eqref" reference="eq:oriented-physical-scalar"} before any edge or fiber triangle inequality. Produce source-valid Kloosterman cells and retain a fixed saving after the ordered blocks, four packet signs, and prime moduli are reassembled once.

The most concrete heuristic is to look for a dual variable shared across the entire tight frame. A shared variable could preserve the complete-graph orthogonality through the transform. If each edge or each $d$-fiber acquires an independent absolute loss instead, Theorem [\[thm:no-sparsification\]](main.tex#L435){reference-type="ref" reference="thm:no-sparsification"} predicts a prohibitive multiplicity and the proposed compiler should be recorded as obstructed rather than promoted conditionally.

# Conclusion

The standard-zero-hole remainder has a canonical additive representation: the complete-graph Laplacian on nonzero frequencies, with the coefficient diagonal deleted inside each edge cell. This representation preserves the outer $q$ normalization, the four-packet signs, and the original physical residue kernel. It also explains why the earlier equal/off-equal estimate order fails and why literal edge-subset sparsification cannot repair it.

The resulting object is a precise pre-emitter. The arithmetic burden has not shrunk into a local bound: it has become a joint whole-frame transformation and reassembly theorem. Future progress requires that theorem, or a rigorous obstruction showing that the complete frame cannot share enough dual structure under the available Poisson/Kloosterman engines.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{Harper2024,
  author        = {Adam J. Harper},
  title         = {Simple {Barban--Davenport--Halberstam} Type Asymptotics for General Sequences},
  year          = {2024},
  eprint        = {2412.19644},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT},
  note          = {Version 1}
}

@misc{BlomerPascadi2026,
  author        = {Valentin Blomer and Alexandru Pascadi},
  title         = {Bilinear Forms with {Kloosterman} Sums via Quadratic Characters},
  year          = {2026},
  eprint        = {2607.24311},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT},
  note          = {Version 1}
}

@article{Pascadi2026LargeSieve,
  author        = {Pascadi, Alexandru},
  title         = {Large Sieve Inequalities for Exceptional {Maass} Forms and the Greatest Prime Factor of {$n^2+1$}},
  journal       = {Forum of Mathematics, Pi},
  volume        = {14},
  eid           = {e8},
  pages         = {1--54},
  year          = {2026},
  doi           = {10.1017/fmp.2026.10025},
  eprint        = {2404.04239},
  archivePrefix = {arXiv},
  primaryClass  = {math.NT},
  url           = {https://doi.org/10.1017/fmp.2026.10025}
}

@misc{Wang2026V59,
  author       = {Liang Wang},
  title        = {Polarized Local {BDH} Scalar Compiler},
  year         = {2026},
  howpublished = {Internal prime-dynamics-theory repository artifact},
  note         = {V59, research/tpc-big-road}
}

@misc{Wang2026TPC207,
  author       = {Liang Wang},
  title        = {Moving-Hole Defects in Translated Reduced-Residue {BDH} Variances},
  year         = {2026},
  howpublished = {TPC-207, internal prime-dynamics-theory paper},
  note         = {Structural L1 release}
}
```

<!-- SOURCE_BODY_END -->
