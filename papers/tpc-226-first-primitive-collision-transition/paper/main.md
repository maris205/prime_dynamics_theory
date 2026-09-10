# First Primitive-Collision Transition in Dilated Shared Clocks

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology
- Source date: August 24, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We identify the first legitimate cross-prime support collision in an integer-dilated family of literal primitive rows used by the twin-prime bridge program. The difficulty is that increasing the cutoff alone creates nonprimitive overlaps that do not belong to the source row. For the clocks $H=4Q^2$ and $h_L=4LQ$, with $Q\ge8$ and $L\in\{1,2,3,4\}$, we prove that all distinct prime rows remain disjoint for $L\le3$. At $L=4$, every collision is, up to exchange and sign, the single resonance type $7p+3r=16Q$ with multipliers $3$ and $-7$. The first stable witness is $Q=25$, $(p,r)=(37,47)$. We then derive the exact signed Gram correction. On the full $Q=25$ prime shell, aligned profiles amplify the AP energy by the factor $15/13$, while a smooth balanced sign profile reduces it to $11/13$ and gives $E_{\rm pol}=E_{\rm all}=0$. An exact-rational certificate checks 505 consecutive scales and 30 profile records, with independent normal and optimized replay. The result is structural: collision geometry creates a cancellation interface, but the physical sign and the arithmetic transfer remain open.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

A prime-row collision is useful only when it belongs to the literal source support. This distinction becomes decisive immediately after the cutoff-one regime. The preceding audit proved that the clock $H=4Q^2$, $h=4Q$ has pairwise disjoint prime supports, so its AP energy equals its diagonal energy exactly `\cite{tpc225}`. A natural response is to enlarge the modulus and admit more multiplier layers. The first apparent overlap, however, uses a nonprimitive multiplier and disappears once the TPC row is restored.

The broader analytic motivation comes from the role of primes in arithmetic progressions and large-sieve estimates in sieve bounds related to twin primes `\cite{lichtman2023primes}`. The present paper does not import such an estimate. It asks a prior structural question: when does the exact finite row geometry first permit a cross-prime term, and what determines its sign? The answer separates collision existence from cancellation.

We study the integer-dilated family $$H=4Q^2,\qquad h_L=4LQ,\qquad L=1,2,3,4,$$ while retaining the primitive multiplier condition, the common normalization $C_h=1/h_L$, and the four-packet energy interface of TPC-220 and TPC-224 `\cite{tpc220,tpc224}`. The paper makes three falsifiable contributions.

1.  We prove pairwise disjointness for every $L\le3$ in the stable range $Q\ge8$. This rejects the tempting $L=3$, $m=4$ overlap as a nonprimitive artifact.

2.  We classify the first primitive transition. At $L=4$, all collisions have the form $7p+3r=16Q$ and use only the multiplier pair $(3,-7)$, together with its global negative.

3.  We prove that the first-transition Gram correction is sign-indefinite across profile families. Constant and inherited affine profiles amplify the AP energy, whereas balanced sign profiles produce strict AP saving and complete packet cancellation.

The strongest finite witness occurs at $Q=25$. The same full prime shell gives $E_{\mathrm{AP}}/E_{\mathrm{diag}}=15/13$ for aligned profiles and $11/13$ for balanced sign profiles. Thus overlap is necessary for the correction, but overlap alone does not pay an AP saving. The missing theorem must derive a negative sign from the physical packet source rather than select it as a finite profile.

# Literal primitive rows and claim boundary

Fix an integer $Q\ge8$ and let $\mathcal Q_Q$ be the primes in $(Q,2Q)$. For $L\in\{1,2,3,4\}$ define $$x=Q^3,\qquad H=4Q^2,\qquad h_L=4LQ,$$ and $$\mathcal M_L(q)=\left\{m\in\mathbb Z:
 0<|m|\le \left\lfloor\frac{Lq}{Q}\right\rfloor,
 (m,h_L)=1\right\}.$$ Every $q\in\mathcal Q_Q$ is a unit modulo $h_L$. The literal row is $$W_{q,j}^{(L)}(a)=\frac1{h_L}
 \sum_{m\in\mathcal M_L(q)}
 \psi_j\!\left(\frac{mQ}{Lq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod{h_L}}.
 \label{eq:literal-row}$$ The primitive restriction in $\mathcal M_L(q)$ is inherited from the exact prime-AP crosswalk `\cite{tpc220}`; it is not an optional simplification.

All four energies use the same rows: $$\begin{aligned}
 E_{\mathrm{diag}}&=\sum_{q,j}\|W_{q,j}^{(L)}\|_2^2,\nonumber\\
 E_{\mathrm{AP}}&=\sum_j\left\|\sum_qW_{q,j}^{(L)}\right\|_2^2,
 &
 E_{\mathrm{pol}}&=\sum_q\left\|\sum_jW_{q,j}^{(L)}\right\|_2^2,\nonumber\\
 E_{\mathrm{all}}&=\left\|\sum_{q,j}W_{q,j}^{(L)}\right\|_2^2.
 \label{eq:energies}\end{aligned}$$ The preceding compatibility theorem controls $E_{\mathrm{all}}$ through the two marginals $E_{\mathrm{AP}}$ and $E_{\mathrm{pol}}$ `\cite{tpc224}`. Here we determine the first clock at which the AP marginal contains any off-diagonal prime term.

The dilation parameter $L$ is a finite modeling choice. Equation [\[eq:literal-row\]](sections/2_setup.tex#L20){reference-type="eqref" reference="eq:literal-row"} preserves the source row, but no theorem identifies $h_L$ with the physical V46 clock. Consequently all conclusions below are structural level-one statements. No arithmetic $L^2$ estimate, fixed-atom credit, or twin-prime conclusion is asserted.

# The first primitive-collision transition

Write $$S_{q,L}=\{m q^{-1}\bmod h_L:m\in\mathcal M_L(q)\}.$$ Since $L\le4$, the cutoff lies between $L$ and $2L-1$, so every allowed multiplier has magnitude at most seven. The stable assumption $Q\ge8$ therefore gives $|m|<q$ for every active prime.

> **Theorem: Primitive transition** <span id="thm:transition" label="thm:transition">\[thm:transition\]</span> For distinct primes $q_1,q_2\in\mathcal Q_Q$, the supports $S_{q_1,L}$ and $S_{q_2,L}$ are disjoint for $L=1,2,3$. For $L=4$, every collision is, up to exchanging the primes and changing both signs, $$7p+3r=16Q,\qquad m_p=3,\qquad m_r=-7.
>  \label{eq:resonance}$$ Conversely, a prime pair satisfying [\[eq:resonance\]](sections/3_collision_transition.tex#L18){reference-type="eqref" reference="eq:resonance"}, the literal cutoff conditions, and $(21,16Q)=1$ produces exactly two shared coordinates.

> **Proof** A shared coordinate is equivalent to $$m_1q_2-m_2q_1\equiv0\pmod{4LQ}.$$ Equal signs give a difference of magnitude less than $(4L-3)Q<4LQ$. Zero difference would force one active prime to divide a nonzero multiplier of magnitude at most seven. Thus the signs are opposite, and a collision reduces to $$a q_2+b q_1=4LQ,
>  \qquad a,b>0.
>  \label{eq:positive-collision}$$ Primitivity makes $a$ and $b$ odd, while the prime-shell inequalities imply $2L<a+b<4L$.
>
> For $L=1$ no pair remains. At $L=2$, only $(3,3)$ remains, but both cutoff conditions force $q_i\ge3Q/2$, making the left side of [\[eq:positive-collision\]](sections/3_collision_transition.tex#L35){reference-type="eqref" reference="eq:positive-collision"} at least $9Q>8Q$. At $L=3$, multiplier $3$ is nonprimitive modulo $12Q$; the only remaining pair is $(5,5)$, whose cutoffs force at least $50Q/3>12Q$.
>
> At $L=4$, the possible positive primitive multipliers are $1,3,5,7$. The size and cutoff constraints reduce the table to $(3,7)$, $(5,5)$, $(5,7)$, and $(7,7)$. The last two exceed $16Q$ after their own cutoff bounds are imposed. The pair $(5,5)$ would imply $5(q_1+q_2)=16Q$, but using multiplier five primitively requires $5\nmid Q$. Only $(3,7)$ and its exchange survive. The two global sign choices give the two coordinates, which cannot coincide because $16Q\nmid6$.

<div id="tab:transition">

| $L$ | primitive collision? | first obstruction or surviving type         |
|:---:|:--------------------:|:--------------------------------------------|
|  1  |          no          | cutoff-one block orthogonality              |
|  2  |          no          | $(3,3)$ violates its cutoff lower bound     |
|  3  |          no          | $m=4$ is nonprimitive; $(5,5)$ is too large |
|  4  |          yes         | only $7p+3r=16Q$ with $(3,-7)$              |

: The first nontrivial cutoff is not the first primitive collision. The integer-dilation transition occurs at $L=4$.

</div>

At $Q=25$, the active pair $(p,r)=(37,47)$ satisfies $7\cdot37+3\cdot47=400$. The inverses are $37^{-1}=173$ and $47^{-1}=383$ modulo $400$, so the shared coordinates are $$3\cdot173\equiv-7\cdot383\equiv119,
 \qquad
 -3\cdot173\equiv7\cdot383\equiv281\pmod{400}.$$ This is the first stable collision found by the exact boundary census, and the theorem shows that its type is the only possible one.

# Signed energy on the resonance graph

The transition theorem determines where cross terms occur. Their sign still depends on the profiles. For a resonance $(p,r)$ define $$u_p=\frac{3Q}{4p},\qquad v_r=\frac{7Q}{4r}.$$ The two shared coordinates contribute exactly $$\frac{2}{h^2}\Re\sum_j\left[
 \psi_j(u_p)\overline{\psi_j(-v_r)}+
 \psi_j(-u_p)\overline{\psi_j(v_r)}
 \right]
 \label{eq:signed-correction}$$ to $E_{\mathrm{AP}}-E_{\mathrm{diag}}$. Summing [\[eq:signed-correction\]](sections/4_signed_energy.tex#L14){reference-type="eqref" reference="eq:signed-correction"} over all prime resonance pairs gives the complete off-diagonal correction.

> **Proposition: Profile sign trichotomy** <span id="prop:trichotomy" label="prop:trichotomy">\[prop:trichotomy\]</span> Suppose the $L=4$ resonance set is nonempty.
>
> 1.  For aligned profiles $\psi_j(t)=1$, one has $E_{\mathrm{AP}}>E_{\mathrm{diag}}$.
>
> 2.  For the inherited affine profiles $\psi_j(t)=1+s_jt$, with $s=(0,1,-1,2)/10$, one has $E_{\mathrm{AP}}>E_{\mathrm{diag}}$.
>
> 3.  Let $\chi$ be a smooth compactly supported odd function equal to $\operatorname{sgn}(t)$ for $1/8\le|t|\le1$, and set $\psi_j(t)=\alpha_j\chi(t)$ with $\alpha=(1,-1,1,-1)$. Then $E_{\mathrm{AP}}<E_{\mathrm{diag}}$ and $E_{\mathrm{pol}}=E_{\mathrm{all}}=0$.

> **Proof** For aligned profiles, every resonance contributes $4J/h^2>0$. For affine profiles, the contribution is $$\frac4{h^2}\left(J-S_2u_pv_r\right),
>  \qquad S_2=\sum_js_j^2=\frac3{50},$$ which is positive because $0<u_p,v_r\le1$. Every sampled nonzero argument for the $L=4$ row lies in $1/8<|t|\le1$. The balanced sign profile therefore assigns opposite values to the two colliding multipliers, and each resonance contributes $-4(\sum_j\alpha_j^2)/h^2<0$. Finally $\sum_j\alpha_j=0$, so each prime-polarized row vanishes pointwise.

<div id="tab:profiles">

| profile on the full $Q=25$ shell | sign of $E_{\mathrm{AP}}-E_{\mathrm{diag}}$ | $E_{\mathrm{AP}}/E_{\mathrm{diag}}$ |
|:---------------------------------|:-------------------------------------------:|:-----------------------------------:|
| aligned                          |                   positive                  |               $15/13$               |
| inherited affine                 |                   positive                  |                 $>1$                |
| balanced sign                    |                   negative                  |               $11/13$               |

: One collision geometry supports amplification or cancellation. For the affine row, the exact positive correction is $221017/2225920000$. The certificate retains the full exact rational ratio.

</div>

Proposition [\[prop:trichotomy\]](sections/4_signed_energy.tex#L20){reference-type="ref" reference="prop:trichotomy"} is the main route decision. The collision graph is no longer empty, but a profile-independent saving is false on the same clock. The next theorem must control the signed correlation attached to the literal packet source.

# Exact certification and adversarial controls

The executable package uses rational arithmetic throughout. The producer checks every $Q=8,\ldots,512$ and every $L=1,\ldots,4$. Across these 505 scales, the first three dilations have no primitive collision. The fourth dilation has 182 collision-bearing scales and 235 resonance pairs; the first occurs at $Q=25$. These counts certify the finite census only. They are not a density theorem for the linear prime relation $7p+3r=16Q$.

Thirty additional records evaluate aligned, affine, and balanced sign profiles at ten collision-bearing scales through $Q=1000$. Each record rebuilds the literal rows, their supports, all four energies, and the signed correction independently of any floating-point tolerance. The independent checker does not import the producer and runs identically under normal and optimized Python modes.

The adversarial test targets the most likely source error. If primitivity is removed at $L=3$, $Q=8$, then the primes $11$ and $13$ appear to collide through multipliers $4$ and $-4$ at two coordinates. Both multipliers have nontrivial gcd with $h=96$, so the literal primitive row contains neither point. Restoring $(m,h)=1$ removes the entire false transition. The same adversary then checks the valid $Q=25$ residues and the three energy signs from Table [2](sections/4_signed_energy.tex#L62){reference-type="ref" reference="tab:profiles"}.

The certificate and checker are trust boundaries, not theorem evidence. The theorem is the integer classification in Section 3; the computation tests implementation, boundary, schema, and exact-energy consistency.

# Conclusion

Primitive support delays the first stable collision beyond the first two nontrivial cutoff enlargements. In the integer-dilated family studied here, $L\le3$ remains block-orthogonal, while $L=4$ admits exactly the $3$–$7$ resonance $7p+3r=16Q$. That resonance supplies a genuine off-diagonal interface, but its sign is not geometric: the inherited affine profiles amplify the AP energy, whereas a balanced sign profile yields strict AP saving and complete packet cancellation.

The result closes the support-geometry subproblem at the first collision transition. It does not source the negative sign required by the arithmetic bridge, identify the dilated clock with V46, or pay any fixed-atom or strict $1/400$ gate. The next useful step is therefore narrow: derive or refute a negative signed correlation for the actual $3$–$7$ packet resonance before attempting a uniform AP saving.

# Coefficient case table

For completeness, equation $a q_2+b q_1=4LQ$ and the inequalities $2L<a+b<4L$ leave only a short finite table. At $L=2$, the pair $(3,3)$ is incompatible with its two cutoff lower bounds. At $L=3$, primitivity removes $3$ and the remaining pair $(5,5)$ is too large. At $L=4$, the candidates with sum between eight and sixteen are $(3,7)$, $(5,5)$, $(5,7)$, and $(7,7)$. Cutoff lower bounds remove the last two; primitive divisibility removes $(5,5)$. Hence $(3,7)$ and its exchange exhaust the primitive collision table.

The balanced sign profile can be chosen smoothly. Start with any smooth odd function that equals $-1$ on $[-1,-1/8]$, equals $1$ on $[1/8,1]$, and interpolate smoothly inside $[-1/8,1/8]$. Multiplication by an even compactly supported cutoff equal to one on $[-1,1]$ preserves every sampled row value and makes the profile compactly supported.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc220,
  author       = {Liang Wang},
  title        = {Prime-AP Collision Crosswalk for the Literal Shell},
  year         = {2026},
  note         = {TPC-220 repository proof record}
}

@misc{tpc224,
  author       = {Liang Wang},
  title        = {Literal Two-Channel Compatibility Audit},
  year         = {2026},
  note         = {TPC-224 repository proof record}
}

@misc{tpc225,
  author       = {Liang Wang},
  title        = {Cutoff-One Shared-Clock Obstruction},
  year         = {2026},
  note         = {TPC-225 repository proof record}
}

@misc{lichtman2023primes,
  author       = {Jared Duker Lichtman},
  title        = {Primes in Arithmetic Progressions to Large Moduli, and Goldbach Beyond the Square-Root Barrier},
  year         = {2023},
  eprint       = {2309.08522},
  archiveprefix = {arXiv},
  primaryclass = {math.NT}
}
```

<!-- SOURCE_BODY_END -->
