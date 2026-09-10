# **Truncated Divisor Bands and the Reciprocal-Emitter Boundary Operator**

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

The preceding TPC-211 analysis gives an exact logarithmic Möbius derivative for a complete squarefree divisor packet of the literal product-coupled Euler profiles. The physical transition, however, uses the non-Boolean band $Y_0<d\leq U$ and a divisor-dependent reciprocal emitter. This paper isolates that boundary interface. For any selected divisor family we prove that its common-endpoint leakage is the signed incidence vector of the selected Boolean faces, with coefficients in the independent basis $(\log p)_{p\in\mathcal P}$. The selected packet is exactly the complete packet minus the missing-subset boundary. We then define a finite reciprocal occupancy operator and prove its exact collision Gram identity. In the natural direct sum over divisor residue spaces the emitter Gram is block diagonal and full rank; normalized residuals attain coherent-to-diagonal ratios equal to the number of divisor blocks. Thus a divisor cut and reciprocal occupancy, without a theorem coupling the literal residual profiles across divisors, do not force a saving. The finite checks use exact rational arithmetic and a unit-weight reciprocal fixture ($\psi=1$); they are structural certificates, not asymptotic prime-distribution evidence. The physical smooth emitter, prime shell, cross-divisor profile theorem, Gate B, and the twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / STOP_SCOPED`\
`BOUNDARY_EMITTER`. No arithmetic $L^2$ credit or fixed-atom credit is claimed.

# Introduction

The working twin-prime route in this repository studies a fixed gap through a literal transition carrier. Its central difficulty is not a missing formal Fourier identity but the simultaneous preservation of the divisor signs, the physical zero axis, the prime shell, and the cross-divisor Gram structure. The local V46 compiler writes the transition residual in the form $$\mathfrak R^{\mathrm{AP}}_x
 =-H\sum_{Y_0<d\leq U}\sum_{r\bmod d}
 A_d(r)\widehat{\mathcal R}_d(r),
 \label{eq:physical-residual}$$ where, schematically, as in the V46 transition artifact `\cite{WangV46}`, $$A_d(r)=\frac{\mu(d)\log d}{d}
 \sum_{q\in\mathcal Q}\sum_{0<|m|\leq dq/H}
 \psi\!\left(\frac{Hm}{dq}\right)
 \mathbf 1_{r\equiv m\overline q\pmod d}.
 \label{eq:emitter}$$ The residue vector $\mathcal R_d$ is the literal physical profile at divisor $d$.

TPC-209 showed that a whole-frame Poisson transform leaves divisor-dependent multiplicative permutations. TPC-210 showed that independent admissible Poisson profiles can realize a Möbius-aligned Gram obstruction `\cite{WangTPC210}`. TPC-211 then moved to the literal product-coupled Euler profiles. It proved a product cocycle, full divisor rank, and the exact complete-packet identity `\cite{WangTPC211}`. $$\sum_{\varnothing\ne S\subseteq\mathcal P}
 \mu(d_S)\log(d_S)\Delta_S
 =-\sum_{p\in\mathcal P}\log p\,\mathcal D_p,
 \label{eq:tpc211-derivative}$$ where $d_S=\prod_{p\in S}p$ and $\Delta_S$ is the product-profile defect. The common endpoint cancels on the complete packet when $|\mathcal P|\geq 2$.

The identity in [\[eq:tpc211-derivative\]](main.tex#L100){reference-type="eqref" reference="eq:tpc211-derivative"} does not apply directly to [\[eq:physical-residual\]](main.tex#L79){reference-type="eqref" reference="eq:physical-residual"}. The active divisor set is a band in the divisor lattice, not a complete packet, and $A_d$ changes with $d$. The precise question of this paper is therefore:

> Does the actual divisor cut together with the reciprocal map force a cross-divisor cancellation before one proves a new theorem for the literal physical profiles?

We answer the algebraic question negatively, but in a controlled way. The answer has two parts. First, the cut produces an exact endpoint leakage vector. Second, the reciprocal map has an exact collision Gram, but its natural direct-sum geometry has no cross-divisor entries. This does not disprove a future estimate on the coupled physical family. It identifies the missing input: a coupling theorem must relate $\mathcal R_d$ across divisors after the boundary and emitter are retained.

Our contributions are:

1.  an exact signed-incidence formula for any divisor selector and an exact complete-minus-missing decomposition;

2.  an exact reciprocal occupancy collision identity and a block-diagonal direct-sum Gram theorem;

3.  a sharp finite alignment construction showing that emitter geometry alone cannot supply a universal cross-divisor saving;

4.  exact finite certificates covering four cuts, 5,810 profile coordinates, and nine emitter divisor rows.

#### Scope firewall.

The proof is finite and algebraic. We do not estimate the shifted-prime sequence, the hybrid profile, the smooth weight $\psi$, the prime shell, the four-packet reassembly, or any asymptotic twin-prime count. The unit-weight emitter used in the certificate is explicitly a modeling fixture.

# The divisor band as a signed Boolean boundary

## Notation

Let $$\mathcal P=\{p_1,\ldots,p_s\},\qquad p_i>2,$$ be a finite set of distinct active primes. For a nonempty subset $S\subseteq\mathcal P$, put $$d_S=\prod_{p\in S}p,\qquad \varepsilon_S=(-1)^{|S|}.$$ The squarefree divisors of $t=\prod_{p\in\mathcal P}p$ are indexed by the nonempty faces of the Boolean cube. A divisor band is represented by a selector $$\mathcal A\subseteq 2^{\mathcal P}\setminus\{\varnothing\}.$$ For the physical interval, the selector is $$\mathcal A_{Y,U}(t)=\{S:Y_0<d_S\leq U\}.
 \label{eq:band-selector}$$ The complement within the nonempty Boolean lattice is denoted by $$\mathcal M=(2^{\mathcal P}\setminus\{\varnothing\})\setminus\mathcal A.$$

For every active prime define the signed incidence $$\eta_p(\mathcal A)=\sum_{\substack{S\in\mathcal A\\p\in S}}\varepsilon_S.
 \label{eq:incidence}$$ The corresponding logarithmic endpoint coefficient is $$L(\mathcal A)=\sum_{S\in\mathcal A}\varepsilon_S\log d_S
       =\sum_{p\in\mathcal P}\eta_p(\mathcal A)\log p.
 \label{eq:log-leakage}$$

> **Lemma: complete-packet incidence cancellation** <span id="lem:full-incidence" label="lem:full-incidence">\[lem:full-incidence\]</span> If $s\geq 2$, then $$\eta_p(2^{\mathcal P}\setminus\{\varnothing\})=0
>  \qquad(p\in\mathcal P).$$ Consequently, the complete packet has $L=0$.

> **Proof** Fix $p$. Pair each subset $S$ containing $p$ with the subset obtained by adding or removing one fixed prime $r\ne p$. The two signs are opposite. Equivalently, $$\eta_p=(-1)\sum_{T\subseteq\mathcal P\setminus\{p\}}(-1)^{|T|}
>        =-(1-1)^{s-1}=0.$$ The logarithmic statement follows from [\[eq:log-leakage\]](main.tex#L178){reference-type="eqref" reference="eq:log-leakage"}.

> **Theorem: exact endpoint leakage** <span id="thm:leakage" label="thm:leakage">\[thm:leakage\]</span> For every selector $\mathcal A$, the common endpoint contribution of the weighted packet is exactly $L(\mathcal A)$ times that endpoint. If $\mathcal A$ is not complete and $\eta_p(\mathcal A)\ne0$ for some $p$, then the endpoint contribution cannot vanish uniformly over endpoint values. More precisely, for a scalar endpoint $w$, $$\sum_{S\in\mathcal A}\varepsilon_S\log(d_S)w=L(\mathcal A)w.
>  \label{eq:endpoint-term}$$ Moreover, $L(\mathcal A)=0$ if and only if $\eta_p(\mathcal A)=0$ for every $p$.

> **Proof** The first identity is linearity and [\[eq:log-leakage\]](main.tex#L178){reference-type="eqref" reference="eq:log-leakage"}. Suppose $L(\mathcal A)=0$. Then $$\prod_{p\in\mathcal P}p^{\eta_p(\mathcal A)}=1$$ after exponentiating the logarithmic relation. The exponents are integers, so unique factorization gives $\eta_p(\mathcal A)=0$ for all $p$. The converse is immediate from [\[eq:log-leakage\]](main.tex#L178){reference-type="eqref" reference="eq:log-leakage"}. If some incidence is nonzero then the logarithmic coefficient is nonzero, and choosing $w\ne0$ gives nonzero leakage.

<span id="ex:35-band" label="ex:35-band">\[ex:35-band\]</span> Take $t=5\cdot7=35$ and $Y_0=5$, $U=35$. Then $$\mathcal A_{5,35}(35)=\{\{7\},\{5,7\}\}.$$ The signs are $-1,+1$, so $$\eta_5=1,\qquad \eta_7=0,
 \qquad L(\mathcal A)= -\log7+\log35=\log5.
 \label{eq:35-leak}$$ Thus the first proper divisor cut already restores a common endpoint term. This is an exact witness, not a numerical approximation to a logarithm.

## Complete minus missing is an operator identity

Let $\Delta_S$ be any family of vectors in a common real or complex vector space and let $w$ be a common endpoint vector. Write $$R_S=w-\Delta_S,
 \qquad
 \mathcal T_\mathcal A=\sum_{S\in\mathcal A}\varepsilon_S\log(d_S)R_S.
 \label{eq:packet-functional}$$ The next statement does not assume the product formula for $\Delta_S$.

> **Proposition: boundary decomposition** <span id="prop:boundary-decomp" label="prop:boundary-decomp">\[prop:boundary-decomp\]</span> With $\mathcal M$ the missing subset family, $$\mathcal T_\mathcal A=\mathcal T_{\mathrm{full}}-\mathcal T_\mathcal M.
>  \label{eq:boundary-decomp}$$ If the complete packet is a TPC-211 product packet with at least two active primes, then its endpoint-free part is the marked-prime derivative, while the missing packet contributes the exact boundary $$\mathcal T_\mathcal M
>  =L(\mathcal M)w-\sum_{S\in\mathcal M}\varepsilon_S\log(d_S)\Delta_S.
>  \label{eq:missing-boundary}$$ The endpoint coefficient of the selected packet is $L(\mathcal A)=-L(\mathcal M)$.

> **Proof** The first identity is the partition of the complete nonempty subset family into $\mathcal A$ and $\mathcal M$. Expanding $R_S=w-\Delta_S$ gives $$\mathcal T_\mathcal M=L(\mathcal M)w-
>  \sum_{S\in\mathcal M}\varepsilon_S\log(d_S)\Delta_S.$$ Lemma [\[lem:full-incidence\]](main.tex#L182){reference-type="ref" reference="lem:full-incidence"} gives $L(\mathcal A)+L(\mathcal M)=0$ when the full packet has at least two active primes. No estimate or limiting argument is used.

> **Remark** The boundary in [\[eq:missing-boundary\]](main.tex#L268){reference-type="eqref" reference="eq:missing-boundary"} has two distinct pieces: endpoint leakage and missing profile mass. Treating the first complete-packet identity as if it bounded both pieces silently changes the divisor set. The physical emitter adds a third issue because its row also changes with $d$.

# The reciprocal occupancy operator

## Finite emitter model

Fix a positive integer $H$, a divisor $d\geq2$, and a finite set $\mathcal Q$ of integers coprime to $d$. Define the finite index set $$I_d=\left\{(q,m):q\in\mathcal Q,
 0<|m|\leq\left\lfloor\frac{dq}{H}\right\rfloor\right\}.$$ For unit weights, define the occupancy operator $$E_d:\mathbb C^{I_d}\longrightarrow\mathbb C^{\mathbb Z/d\mathbb Z},
 \qquad
 (E_d a)(r)=\sum_{(q,m)\in I_d}
 a(q,m)\mathbf 1_{r\equiv m\overline q\pmod d}.
 \label{eq:occupancy-operator}$$ The physical emitter is the same pushforward with $$a(q,m)=\psi\!\left(\frac{Hm}{dq}\right),$$ followed by the nonzero scalar $\mu(d)\log(d)/d$. We first isolate the pushforward algebra.

> **Lemma: reciprocal collision identity** <span id="lem:collision" label="lem:collision">\[lem:collision\]</span> Let $a\equiv1$ on $I_d$ and write $N_d=E_d a$. Then $$\left\lVert N_d\right\rVert_2^2
>  =\sum_{(q_1,m_1),(q_2,m_2)\in I_d}
>  \mathbf 1_{d\mid m_1q_2-m_2q_1}.
>  \label{eq:collision}$$ More generally, for arbitrary weights $a$, $$\left\lVert E_da\right\rVert_2^2
>  =\sum_{I_d\times I_d}a(q_1,m_1)\overline{a(q_2,m_2)}
>  \mathbf 1_{d\mid m_1q_2-m_2q_1}.
>  \label{eq:weighted-collision}$$

> **Proof** Expand the squared norm and use $$m_1\overline q_1\equiv m_2\overline q_2\pmod d.$$ Multiplication by $q_1q_2$, which is invertible modulo $d$, converts this condition exactly into $m_1q_2\equiv m_2q_1\pmod d$. The unit-weight case is the specialization $a=1$.

> **Proposition: direct-sum emitter Gram** <span id="prop:direct-sum" label="prop:direct-sum">\[prop:direct-sum\]</span> Let $\mathcal B$ be a finite divisor family and set $$\mathcal H_\mathcal B=\bigoplus_{d\in\mathcal B}\mathbb C^{\mathbb Z/d\mathbb Z}.$$ Let $v_d$ be the unit-weight occupancy vector in the $d$-block, embedded in this direct sum. Then $$\left\langle v_d,v_e\right\rangle=0\quad(d\ne e),
>  \qquad
>  \left\langle v_d,v_d\right\rangle=\left\lVert v_d\right\rVert_2^2.
>  \label{eq:block-gram}$$ If every $v_d$ is nonzero, the Gram matrix of the family has rank $|\mathcal B|$. For any signs $\sigma_d\in\{\pm1\}$ the residuals $$r_d=\sigma_d\frac{v_d}{\left\lVert v_d\right\rVert_2^2}
>  \label{eq:aligned-residual}$$ satisfy $$\sigma_d\left\langle v_d,r_d\right\rangle=1.
>  \label{eq:aligned-contribution}$$ Consequently the coherent-to-diagonal ratio of these unit contributions is $|\mathcal B|$.

> **Proof** Different direct-sum blocks are orthogonal, proving [\[eq:block-gram\]](main.tex#L356){reference-type="eqref" reference="eq:block-gram"}. Nonzero diagonal entries give full rank. Equation [\[eq:aligned-residual\]](main.tex#L362){reference-type="eqref" reference="eq:aligned-residual"} gives $\left\langle v_d,r_d\right\rangle=\sigma_d$, hence [\[eq:aligned-contribution\]](main.tex#L367){reference-type="eqref" reference="eq:aligned-contribution"}. The coherent energy is $|\mathcal B|^2$ and the diagonal energy is $|\mathcal B|$.

> **Remark** Proposition [\[prop:direct-sum\]](main.tex#L345){reference-type="ref" reference="prop:direct-sum"} is deliberately a negative interface result. It does not say that the literal residual family can choose the aligned residuals independently. It says that the reciprocal pushforward itself has not supplied the missing coupling. A saving theorem must use extra structure of $\mathcal R_d$, not only the congruence defining $E_d$.

# Exact finite certificates

## Protocol

The certificate in the project directory is generated by exact rational code. The boundary test uses deterministic rational profiles on the common CRT coordinate set of size $\prod p$. This makes the equality in [\[eq:boundary-decomp\]](main.tex#L260){reference-type="eqref" reference="eq:boundary-decomp"} a coefficientwise finite identity rather than a floating-point regression. The emitter test uses the finite unit-weight fixture $\psi=1$. For each divisor the code records the occupancy vector, its squared norm, and the independent ordered collision count in [\[eq:collision\]](main.tex#L323){reference-type="eqref" reference="eq:collision"}.

The independent checker reimplements the Boolean and reciprocal arithmetic; it does not import the producer module. The optimized Python run is included as a second execution mode, not as an independent mathematical proof.

<div id="tab:boundary-cases">

|  $\mathcal P$ | $Y_0$ | $U$ |  active divisors | $\eta(\mathcal A)$ | coordinates |
|:-------------:|:-----:|:---:|:----------------:|:------------------:|:-----------:|
|    $(5,7)$    |   5   |  35 |      $7,35$      |       $(1,0)$      |      35     |
|   $(5,7,11)$  |   5   |  35 |     $7,35,11$    |     $(1,0,-1)$     |     385     |
|   $(5,7,11)$  |   10  |  77 |   $35,11,55,77$  |      $(2,2,1)$     |     385     |
| $(5,7,11,13)$ |   30  | 100 | $35,55,77,65,91$ |     $(3,3,2,2)$    |     5005    |

: Boundary-band certificate cases. Incidence is ordered by the active prime list.

</div>

The first row is the exact witness in Example [\[ex:35-band\]](main.tex#L228){reference-type="ref" reference="ex:35-band"}. The other rows show that a divisor band can leave several nonzero incidence coordinates; the effect is not peculiar to a two-prime packet. In all four rows the full incidence vector is zero and the selected plus missing incidence vectors add to it exactly.

<div id="tab:emitter-cases">

|    divisors    | $\mathcal Q$ | $H$ | $\left\lVert v_d\right\rVert_2^2$ | rank | ratio |
|:--------------:|:------------:|:---:|:---------------------------------:|:----:|:-----:|
|    $(7,35)$    |  $(2,3,13)$  |  10 |             $(86,470)$            |   2  |   2   |
| $(7,11,35,55)$ |  $(2,3,13)$  |  10 |         $(86,158,470,710)$        |   4  |   4   |
|  $(35,55,77)$  |  $(2,3,13)$  |  10 |          $(470,710,1014)$         |   3  |   3   |

: Unit-weight reciprocal-emitter fixtures. The displayed Gram rank is the rank in the natural direct sum over the listed divisor blocks.

</div>

The collision counts equal the squared norms entry by entry. The residuals in [\[eq:aligned-residual\]](main.tex#L362){reference-type="eqref" reference="eq:aligned-residual"}, with the literal Möbius signs of the displayed divisors, make all weighted contributions equal to one. This is a sharp finite alignment statement for the emitter interface.

## Certificate status

The exact certificate covers four boundary cases, 5,810 profile coordinates, three emitter cases, and nine divisor rows. The producer, independent checker, and optimized independent checker all pass. The following status is part of the release contract:

    TPC212_ROUTE_ADVANCE = YES
    TPC212_STRUCTURAL_THRESHOLD_A = PASS
    TPC212_CUT_ENDPOINT_LEAKAGE = PROVED_EXACT
    TPC212_BOUNDARY_DECOMPOSITION = PROVED_EXACT
    TPC212_RECIPROCAL_COLLISION = PROVED_EXACT_FINITE
    TPC212_EMITTER_GRAM = PROVED_EXACT_BLOCK_DIAGONAL
    TPC212_EMITTER_ONLY_UNIVERSAL_SAVING = REFUTED_SCOPED
    TPC212_LITERAL_PHYSICAL_BOUNDARY_BOUND = OPEN
    TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
    TPC212_ARITHMETIC_ADVANCE = NO
    TPC212_FIXED_ATOM_CREDIT = 0
    TPC212_L2 = NONE
    TPC212_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID

# What the obstruction does and does not say

## The missing physical coupling

The direct sum in Proposition [\[prop:direct-sum\]](main.tex#L345){reference-type="ref" reference="prop:direct-sum"} is the correct ambient space for an arbitrary family of residue vectors $(\mathcal R_d)_{d\in\mathcal
B}$. It is also exactly the space in which a separate Cauchy estimate sees one emitter row per divisor. The proposition shows why that estimate cannot be upgraded by rhetoric about “the same reciprocal variable”: after the residue pushforward, different divisor blocks are still independent unless a new map identifies them.

For the literal TPC object, such an identifying map might come from the product-coupled Euler factors, the common endpoint, or the common underlying integer $u$. TPC-211 proved that product rank and a shared endpoint do not provide it automatically. TPC-212 adds that the cut and reciprocal occupancy do not provide it either. The remaining theorem must therefore be of the form $$\left|\sum_{d\in\mathcal A_{Y,U}(t)}
 \frac{\mu(d)\log d}{d}
 \left\langle E_d\psi_d,\widehat{\mathcal R}_d\right\rangle\right|
 \leq \text{a saving bound for the coupled family},
 \label{eq:needed-physical-theorem}$$ where the right side must use a relation between the different $\widehat{\mathcal R}_d$. Applying Cauchy in the direct sum, replacing $\widehat{\mathcal R}_d$ by arbitrary unit vectors, or replacing the smooth $\psi_d$ by independent unit weights cannot prove such a relation.

## Why the finite fixture is not an arithmetic result

The finite emitter certificate sets $\psi=1$ on a finite set of $(q,m)$ pairs. It is useful because the congruence collision is then an integer identity and because every nonzero block can be aligned explicitly. It is not the physical smooth emitter, does not include the prime shell, and does not control the relative phases of the literal residuals. Therefore the correct label is `NUMERICALLY_CERTIFIED` for the finite rows and `MODELING_CHOICE` for the unit-weight fixture, not an arithmetic theorem.

The endpoint incidence theorem is stronger in a different direction: it uses the exact logarithmic basis and unique factorization, so it is a general finite identity for every cut selector. Still, it only identifies the term that a future physical estimate must pay; it does not bound that term in the asymptotic transition range.

# Conclusion and next route

TPC-212 converts the open phrase “truncated boundary plus reciprocal emitter” into two explicit operators. The divisor cut has a signed Boolean incidence vector, and the reciprocal map has a collision Gram. The complete packet annihilates the first vector, while a proper band generally does not. The natural emitter Gram is block diagonal and admits sharp finite alignment.

The strongest positive result is the exact boundary/operator decomposition. The strongest obstruction is the scoped failure of emitter-only universal saving. The next theorem is now sharply specified: construct and bound the coupling map that takes the literal V46 profile family into these divisor blocks, retaining the smooth weights and the prime shell before any outer absolute value. Until that theorem is proved, Gate B remains open and no twin-prime conclusion follows.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{WangTPC210,
  author = {Liang Wang},
  title = {Poisson Profile Realizability and the Mobius Alignment Obstruction},
  year = {2026},
  note = {TPC-210 project release in the prime dynamics theory repository}
}

@misc{WangTPC211,
  author = {Liang Wang},
  title = {Product-Coupled Euler Profiles and the Mobius-Logarithmic Gram Constraint},
  year = {2026},
  note = {TPC-211 project release in the prime dynamics theory repository}
}

@misc{WangV46,
  author = {Liang Wang},
  title = {Transition-Native Euler-BDH Compiler},
  year = {2026},
  note = {V46 Bridge-A research artifact in the prime dynamics theory repository}
}
```

<!-- SOURCE_BODY_END -->
