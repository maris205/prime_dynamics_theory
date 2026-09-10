# **Poisson Profile Realizability\ and the Möbius Alignment Obstruction**

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

The preceding TPC-209 stage identified a profile-aware nonprincipal-character problem after whole-frame Poisson reindexing. Its obstruction used arbitrary finite residue profiles, leaving open whether Schwartz regularity and the Poisson origin of those profiles might already force useful cross-divisor structure. We prove that they do not at finite modulus. For every prime $q>2$, every vector in $\mathbb C^{\mathbb F_q^\times}$ is exactly the residue profile of a compactly supported smooth Fourier packet. The construction uses separated dual nodes and a single compactly supported smooth bump. We then insert the literal Mobius weights and realize the aligned family $B_D=\mu(D)U_D^*z$, obtaining an exact coherent-to-diagonal energy ratio equal to the number of squarefree unit divisors. Finally, we write the complete profile-aware energy as a positive-semidefinite cross-divisor Gram quadratic form. The result is a genuine admissible-profile obstruction: individual profile norms and Mobius signs cannot supply a saving. It is deliberately scoped; the independently chosen packets are not asserted to be the fully coupled physical twin-prime coefficients, so the actual physical profile bound, the strict $1/400$ gate, and the twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

=2em

# Introduction and claim ceiling

The current prime-dynamics route studies a fixed-gap prime-pair remainder in a standard-zero-hole, prime-modulus, reduced-residue variance. TPC-208 built the complete additive edge frame, and TPC-209 applied Poisson before any edge triangle. For one divisor $D$, the dual index $$n=qr+kD$$ is shared by all additive vertices. Across divisors, however, the resulting residue packets are permuted by $U_D$. Multiplicative Fourier analysis gives a common character coordinate but leaves one profile per divisor `\cite{Wang2026TPC209}`.

The next natural question is narrower and more demanding:

> Does the fact that each profile comes from a Schwartz function through the Poisson map, together with the literal Mobius coefficient $\mu(D)$, already prevent the alignment obstruction?

This paper answers the interface-level question negatively. The word “interface” is essential. The construction below allows a separate smooth Fourier packet for each divisor. It therefore proves that no theorem stated only in terms of the individual Schwartz/Poisson admissibility conditions and the Mobius coefficient envelope can force cross-divisor cancellation. It does not prove that the literal, coupled TPC coefficient family realizes the same profiles.

The maximum justified claim is $$\boxed{\texttt{PROVED\_STRUCTURAL\_L1 / STOP\_SCOPED\_PROFILE\_CLASS}.}$$ More explicitly:

-   finite residue-profile interpolation is proved exactly;

-   a Mobius-weighted aligned family is proved exactly;

-   the missing arithmetic input is identified as a cross-divisor Gram bound on the literal physical packets;

-   no prime-only BDH estimate, Kloosterman attachment, arithmetic $L^2$ advance, fixed-atom credit, or twin-prime theorem is claimed.

# The profile interface

Let $q>2$ be prime and write $$G_q=\mathbb F_q^\times,\qquad N=q-1,qquad
 P_q=I_N-\frac1N\mathbf 1\mathbf 1^*.
 \tag{2.1}$$ For a Schwartz function $F_D$ on $\mathbb R$ and a unit divisor $D$ modulo $q$, define the Poisson residue profile $$B_{q,D}(s)=
 \sum_{\substack{n\in\mathbb Z\\ n\equiv s\pmod q}}
 \widehat F_D(n/q),
 \qquad s\in G_q.
 \tag{2.2}$$ This is the dual packet appearing after the exact TPC-209 reindexing. The corresponding additive vector is $U_DB_{q,D}$, where $$(U_D b)(k)=b(kD),\qquad k\in G_q.
 \tag{2.3}$$

The TPC frame removes the constant direction. Thus the relevant profile energy is $$\left\lVert P_qY\right\rVert^2,
 \qquad Y=\sum_{D\in\mathcal D}c_DU_DB_{q,D}.
 \tag{2.4}$$ The question is whether the range of (2.2) is sufficiently small to prevent coherent choices of the $B_{q,D}$.

# Exact finite profile interpolation

Choose, for each $s\in G_q$, the dual integer $$n_s=s+10qs=s(10q+1),
 \qquad \rho_q=\frac1{4q}.
 \tag{3.1}$$ The points $n_s/q$ are separated from one another by more than $10$, while two distinct points in the same residue class are separated by exactly one. Let $\eta\in C_c^\infty((-1,1))$ satisfy $\eta(0)=1$.

> **Theorem: finite profile interpolation** <span id="thm:interpolation" label="thm:interpolation">\[thm:interpolation\]</span> For every target vector $b=(b(s))_{s\in G_q}\in\mathbb C^{G_q}$, define $$\widehat F_b(\xi)=
>  \sum_{s\in G_q} b(s)\,
>  \eta\!\left(\frac{\xi-n_s/q}{\rho_q}\right).
>  \tag{3.2}$$ Then $\widehat F_b\in C_c^\infty(\mathbb R)$, its inverse Fourier transform $F_b$ is Schwartz, and $$\sum_{\substack{n\in\mathbb Z\\ n\equiv t\pmod q}}
>  \widehat F_b(n/q)=b(t)
>  \qquad (t\in G_q).
>  \tag{3.3}$$ Consequently, the profile map $F\mapsto B_q$ in (2.2) is onto $\mathbb C^{G_q}$, and any finite family of target profiles is realized by choosing the functions independently.

> **Proof** The support of the $s$-th summand in (3.2) is contained in $(n_s/q-\rho_q,n_s/q+\rho_q)$. Since $2\rho_q<1$ and the points $n_s/q$ are separated by more than $10$, these intervals are disjoint and no interval contains any other point of the lattice $\{n/q:n\in\mathbb Z\}$. At the lattice point $n_t/q$, the $t$-th summand has value $b(t)$ and all other summands vanish. Every other point $n/q$ in the same residue class is outside the support of every summand. Therefore the residue sum in (3.3) has exactly one nonzero term, equal to $b(t)$. A compactly supported smooth function has a Schwartz inverse Fourier transform, completing the proof.

> **Remark** The theorem is finite and exact. It does not say that a single physical coefficient array can independently choose all divisor components. It says that smoothness and the Poisson residue map, by themselves, impose no such coupling.

# Mobius-weighted aligned profiles

Let $\mathcal D$ be a finite set of squarefree integers coprime to $q$, and put $$c_D=\mu(D),\qquad m=\lvert\mathcal D\rvert.
 \tag{4.1}$$ Take any centered vector $z\in\mathbf 1^\perp$ and define $$B_D=\mu(D)U_D^*z.
 \tag{4.2}$$ Theorem [\[thm:interpolation\]](main.tex#L154){reference-type="ref" reference="thm:interpolation"} realizes every $B_D$ by a valid Schwartz packet.

> **Proposition: exact Mobius alignment** <span id="prop:alignment" label="prop:alignment">\[prop:alignment\]</span> For the profiles (4.2), $$P_q\sum_{D\in\mathcal D}c_DU_DB_D=mz.
>  \tag{4.3}$$ Moreover, $$\sum_{D\in\mathcal D}|c_D|^2\left\lVert P_qU_DB_D\right\rVert^2
>    =m\left\lVert z\right\rVert^2,
>  \qquad
>  \left\lVert P_q\sum_{D\in\mathcal D}c_DU_DB_D\right\rVert^2
>    =m^2\left\lVert z\right\rVert^2.
>  \tag{4.4}$$ Thus the coherent-to-diagonal energy ratio is exactly $m$.

> **Proof** Since $U_DU_D^*=I$ and $\mu(D)^2=1$ on $\mathcal D$, $$c_DU_DB_D=\mu(D)U_D\bigl(\mu(D)U_D^*z\bigr)=z.$$ Summing gives (4.3), and $z$ is already in the range of $P_q$. Each individual output has squared norm $\left\lVert z\right\rVert^2$, which gives (4.4).

For the smallest nontrivial fixture, take $q=5$, $\mathcal D=\{2,3\}$, and $z=(1/2,-1/2,0,0)$. Both weights are $-1$, yet the two weighted outputs are identical. The ratio in (4.4) is $2$. This is the TPC-209 resonance with the additional fact that both profiles come from explicit compactly supported smooth Fourier packets.

# The exact missing object: a cross-divisor Gram theorem

For arbitrary profiles define the output vectors $$V_D=P_qU_DB_D,
 \qquad
 G_{D,E}=\left\langle V_D,V_E\right\rangle.
 \tag{5.1}$$

> **Proposition: Gram reduction** <span id="prop:gram" label="prop:gram">\[prop:gram\]</span> The matrix $G=(G_{D,E})_{D,E\in\mathcal D}$ is Hermitian positive semidefinite and the whole-frame energy is exactly $$\left\lVert P_q\sum_Dc_DU_DB_D\right\rVert^2
>  =\sum_{D,E}c_D\overline{c_E}\,G_{D,E}.
>  \tag{5.2}$$ Its diagonal is $$G_{D,D}=\left\lVert P_qB_D\right\rVert^2,
>  \tag{5.3}$$ because $U_D$ is unitary and commutes with $P_q$.

> **Proof** Equation (5.2) is the expansion of the squared norm. Any Gram matrix is Hermitian positive semidefinite. Finally, $U_D^*P_qU_D=P_q$, so (5.3) follows.

The diagonal data alone cannot imply cancellation. In the aligned family, $V_D=\mu(D)z$, so $$G_{D,E}=\mu(D)\mu(E)\left\lVert z\right\rVert^2.
 \tag{5.4}$$ The matrix is rank one on the divisor index set, and the Mobius quadratic form in (5.2) adds every cross term constructively. Therefore the next legitimate arithmetic target is not a profile-norm estimate. It is a theorem that uses the literal physical coupling of the $F_D$ to control the off-diagonal entries of $G$ after all TPC normalizations are restored.

The same point can be expressed in multiplicative Fourier coordinates. If $A_D(\chi)=(\mathcal MB_D)(\chi)$, then $$G_{D,E}=\sum_{\chi\ne\chi_0}
 \chi(D)\overline{\chi(E)}A_D(\chi)\overline{A_E(\chi)}.
 \tag{5.5}$$ Thus (5.5) is exactly the profile-aware nonprincipal-character interface identified in TPC-209, now with the admissible profile range made explicit.

# Finite certificate

The project certificate replays the interpolation geometry and the aligned family at $q=3,5,7,11,13$. It uses exact rational arithmetic. The producer and independent checker agree on the residue nodes, support radius, Mobius weights, Gram matrices, and energy ratios.

<div id="tab:certificate">

| quantity                         |          value| status      |
|:---------------------------------|--------------:|:------------|
| prime moduli                     |  $3,5,7,11,13$| exact       |
| realized divisor-profile rows    |           $20$| exact       |
| residue-coordinate rows          |          $178$| exact       |
| support-geometry rows            |           $34$| exact       |
| $q=5$ Mobius divisors            |          $2,3$| exact       |
| $q=5$ coherent-to-diagonal ratio |            $2$| exact       |
| continuous asymptotic estimate   |           none| not claimed |

: TPC-210 finite certificate.

</div>

The exact checks can be reproduced from the repository root with

    cd papers/tpc-210-poisson-profile-realizability
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/profile_interpolation_sanity.py

The certificate is a finite QA artifact. It verifies the exact construction; it is not numerical evidence for an asymptotic prime correlation estimate.

# Source boundary and route decision

TPC-209 left open a profile-aware prime-only estimate after the exact return to the V59 nonprincipal-character interface `\cite{Wang2026V59}`. TPC-210 proves that the basic Schwartz/Poisson profile class is too large for a universal saving: it contains an exact Mobius-aligned family. Consequently, any future positive theorem must use additional physical information, such as a coupling between the divisor components, a common underlying coefficient array, or a source-backed cross-divisor Gram estimate.

The conclusion is a scoped stop: $$\begin{gathered}
\texttt{PROFILE\_CLASS\_UNIVERSAL\_SAVING=REFUTED\_SCOPED},\\
\texttt{ACTUAL\_PHYSICAL\_PROFILE\_BOUND=OPEN},\\
\texttt{FULL\_GATE\_B=OPEN},\quad
\texttt{STRICT\_1/400=UNPAID},\\
\texttt{ARITHMETIC\_ADVANCE=NO},\quad
\texttt{L2=NONE}.
\end{gathered}$$

# Conclusion

The TPC-210 advance is a class-level separation theorem. Smooth Poisson packets can interpolate arbitrary finite residue profiles, and literal Mobius signs can be absorbed into adjoint dilations so that all whole-frame outputs align. The only route-compatible replacement is therefore a physical cross-divisor theorem controlling the Gram matrix (5.1), with the exact zero-hole diagonal and all downstream prime-shell and block data retained.

This does not settle the twin-prime problem and does not negate the possibility that the actual coupled TPC packet has additional structure. It does remove a specific shortcut: profile regularity and Mobius signs alone are not that structure.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{Wang2026TPC209,
  author       = {Liang Wang},
  title        = {Whole-Frame Poisson Reindexing and the Mobius-Dilation Obstruction},
  year         = {2026},
  note         = {TPC-209 session artifact, prime-dynamics theory repository}
}

@misc{Wang2026V59,
  author       = {Liang Wang},
  title        = {Polarized Local BDH Scalar Compiler},
  year         = {2026},
  note         = {V59 session artifact, prime-dynamics theory repository}
}

@misc{Wang2026TPC208,
  author       = {Liang Wang},
  title        = {Zero-Hole Additive Edge Frame},
  year         = {2026},
  note         = {TPC-208 session artifact, prime-dynamics theory repository}
}
```

<!-- SOURCE_BODY_END -->
