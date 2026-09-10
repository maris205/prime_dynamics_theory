# **Whole-Frame Poisson Reindexing\ and the Möbius-Dilation Obstruction**

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

We test a proposed next transformation for the complete additive edge frame of the standard-zero-hole reduced-residue Barban–Davenport–Halberstam remainder. For a fixed unit dilation $D$ modulo a prime $q$, Poisson summation has an exact reindexing $n=qr+kD$: all edge vertices share one dual integer lattice. After the divisor sum is restored, however, the dual residue packet is acted on by the multiplicative permutation $U_D:b(k)\mapsto b(kD)$. We prove an exact vector-valued whole-frame covariance identity and diagonalize all such permutations by multiplicative Fourier analysis. The resulting shared-character profile formula contains a different dual profile for every divisor. For the physical additive Fourier vector, a Gauss-sum calculation returns exactly to the nonprincipal Dirichlet-character interface of the previous scalar compiler. Finally, an exact operator-norm calculation and a $q=5$ resonance fixture show that arbitrary profiles can align after the permutations. Thus the complete frame alone cannot collapse the divisor components into one scalar Kloosterman packet or create a power saving. This is a structural, scoped obstruction: the profile-aware prime-only theorem, the strict $1/400$ gate, and the twin-prime endpoint remain open.

<!-- SOURCE_BODY_BEGIN -->

=2em

# Introduction and claim ceiling

The current prime-dynamics route studies a fixed-gap prime-pair remainder through a standard-zero-hole, prime-modulus, $q$-weighted reduced-residue variance. The previous stage constructed an exact complete-graph tight frame on the nonzero additive frequencies and distributed the mandatory coefficient diagonal inside the same edge cells `\cite{Wang2026TPC208}`. That construction left a specific question: can one apply the Möbius and Poisson transforms to the complete oriented $(d,k)$ frame before paying an edge or fiber triangle, and thereby expose one shared dual variable for a source-valid Kloosterman estimate?

This paper answers the algebraic part of that question and records the first failure boundary. The answer is not a simple yes or no. A shared dual integer exists for each fixed divisor component. Across divisor components, the same dual packet is seen in different multiplicative coordinates. The correct whole-frame object is consequently vector-valued. Multiplicative Fourier analysis gives a clean normal form, but that normal form is a return to the nonprincipal-character representation already identified in the earlier polarized scalar compiler `\cite{Wang2026V59}`.

The maximum justified claim is therefore

The distinction matters. A finite exact frame identity is not an arithmetic estimate, and a post-emitter Kloosterman theorem cannot be applied until the divisor profiles, the exact $(q-2)$ diagonal subtraction, the prime shell, the four packet signs, and the physical block reassembly have all been compiled into its input type.

# The frozen additive frame

Let $q>2$ be prime and write $$G_q=\mathbb F_q^\times,\qquad N=q-1,qquad
 P_q=I_N-\frac1N\mathbf 1\mathbf 1^*.
 \tag{2.1}$$ For a finitely supported sequence $a$, a real $v$, and a scale $H>0$, define the nonzero additive-frequency vector $$Y_q[a](k;v)=\sum_{n\in\mathbb Z}a_n\mathrm e(vn/H)\mathrm e_q(-kn),
 \qquad k\in G_q.
 \tag{2.2}$$ If $e=\{k,l\}\subset G_q$, the literal edge transform is $$T_e[a](v)=Y_q[a](k;v)-Y_q[a](l;v).
 \tag{2.3}$$ The complete-graph incidence vectors satisfy $$\sum_{e} (e_k-e_l)(e_k-e_l)^*=NP_q.
 \tag{2.4}$$ Consequently the edge bilinear form is $$\mathcal E_q(Y,Z):=\frac1N\sum_e (Y(k)-Y(l))
 \overline{(Z(k)-Z(l))}
 =\langle P_qY,P_qZ\rangle.
 \tag{2.5}$$

For the TPC application, (2.5) is only the internal frame layer. The physical scalar retains the outer $q$, the kernel localization, the prime shell, the exact coefficient-off-diagonal subtraction, and the signed packet and block reassembly. We do not replace those layers by positivity.

# Poisson reindexing at one divisor

Let $D$ be an integer with $(D,q)=1$ and let $F_D$ be a Schwartz function. Use the Fourier convention $$\widehat F_D(\xi)=\int_{\mathbb R}F_D(x)\mathrm e(-x\xi)\,dx,
 \qquad \mathrm e_q(x)=\mathrm e(x/q).
 \tag{3.1}$$ The Poisson-ready component at additive vertex $k$ is $$Y_{q,D}(k)=\sum_{m\in\mathbb Z}F_D(m)\mathrm e_q(-kDm).
 \tag{3.2}$$

> **Theorem: shared dual integer at fixed dilation** <span id="thm:poisson" label="thm:poisson">\[thm:poisson\]</span> For every $k\in G_q$, $$\boxed{
>  Y_{q,D}(k)=\sum_{r\in\mathbb Z}\widehat F_D\!\left(r+\frac{kD}{q}\right)
>  =\sum_{\substack{n\in\mathbb Z\\n\equiv kD\;(q)}}\widehat F_D(n/q).}
>  \tag{3.3}$$ For fixed $D$, $(k,r)\mapsto n=qr+kD$ is a bijection from $G_q\times\mathbb Z$ to the integers not divisible by $q$. If $$B_{q,D}(s)=\sum_{n\equiv s\;(q)}\widehat F_D(n/q),
>  \qquad s\in G_q,
>  \tag{3.4}$$ and $(U_Db)(k)=b(kD)$, then $$\boxed{Y_{q,D}=U_DB_{q,D}.}
>  \tag{3.5}$$

> **Proof** Poisson summation applied to $F_D(x)\mathrm e(-kDx/q)$ gives the first equality in (3.3). Since $D$ is invertible modulo $q$, every $n\not\equiv0\pmod q$ has the unique representation $n=qr+kD$ with $k\in G_q$. The inverse is $$k\equiv nD^{-1}\pmod q,
>  \qquad r=(n-kD)/q.$$ Reindexing proves the second equality and (3.5).

Thus the fixed-divisor part of the proposed route succeeds exactly: no edge has been estimated separately, and the complete edge family uses one dual integer lattice. The price is the permutation $U_D$.

# The whole-frame vector compiler

Let $\mathcal D$ be a finite set of unit dilations and let $c_D,d_E\in\mathbb C$. Set $$Y=\sum_{D\in\mathcal D}c_DU_DB_D,
 \qquad
 Z=\sum_{E\in\mathcal D}d_EU_EC_E.
 \tag{4.1}$$

> **Proposition: whole-frame covariance** <span id="prop:covariance" label="prop:covariance">\[prop:covariance\]</span> The complete edge frame gives $$\boxed{
>  \mathcal E_q(Y,Z)=\sum_{D,E\in\mathcal D}c_D\overline{d_E}
>  \langle P_qU_DB_D,P_qU_EC_E\rangle.}
>  \tag{4.2}$$ Moreover $U_DP_q=P_qU_D$ and the cross term is governed by the relative dilation $D^{-1}E$: $$\langle P_qU_DB_D,P_qU_EC_E\rangle
>  =\langle P_qB_D,U_{D^{-1}E}P_qC_E\rangle.
>  \tag{4.3}$$

> **Proof** Insert (4.1) into (2.5). A multiplicative permutation preserves the constant vector and hence commutes with $P_q$. Also $U_D^*U_E=U_{D^{-1}E}$. This proves both identities.

Equation (4.2) is the exact whole-frame transform sought in the route. In particular, the $D\ne E$ terms are not errors. Dropping them, or replacing them by separate absolute values, would require a new estimate.

# Shared-character profile normal form

Let $\widehat{G_q}$ denote the multiplicative character group and define the unitary multiplicative Fourier transform $$(\mathcal Mb)(\chi)=N^{-1/2}\sum_{s\in G_q}b(s)\overline{\chi(s)}.
 \tag{5.1}$$ Direct substitution shows $$\mathcal M(U_Db)(\chi)=\chi(D)\mathcal Mb(\chi).
 \tag{5.2}$$ The principal character coordinate is the constant direction removed by $P_q$.

> **Theorem: shared-character profile normal form** <span id="thm:character" label="thm:character">\[thm:character\]</span> For $Y,Z$ in (4.1), $$\boxed{
>  \mathcal E_q(Y,Z)=\sum_{\chi\ne\chi_0}
>  \left(\sum_Dc_D\chi(D)(\mathcal MB_D)(\chi)\right)
>  \overline{\left(\sum_Ed_E\chi(E)(\mathcal MC_E)(\chi)\right)}.}
>  \tag{5.3}$$

> **Proof** Apply the unitary transform (5.1) to (4.2), use (5.2), and delete the principal coordinate. Parseval gives (5.3).

The exact shared coordinate is now a multiplicative character $\chi$, but the profiles $(\mathcal MB_D)(\chi)$ still depend on $D$. A scalar expression $\sum_Dc_D\chi(D)$ appears only after the extra assumption that the profiles are common.

# Gauss crosswalk to the previous interface

For a nonprincipal character $\chi$, define $$\tau_q(\overline\chi)=\sum_{x\in G_q}\overline\chi(x)\mathrm e_q(x).
 \tag{6.1}$$

> **Proposition: exact Gauss crosswalk** <span id="prop:gauss" label="prop:gauss">\[prop:gauss\]</span> For the physical vector (2.2), $$\boxed{
>  (\mathcal MY_q[a])(\chi)=
>  \frac{\overline{\chi(-1)}\tau_q(\overline\chi)}{\sqrt{q-1}}
>  \sum_{q\nmid n}a_n\mathrm e(vn/H)\chi(n).}
>  \tag{6.2}$$

> **Proof** Exchange the finite character sum and the sum over $n$. If $q\nmid n$, the substitution $x=-kn$ yields $$\sum_{k\in G_q}\overline\chi(k)\mathrm e_q(-kn)
>  =\overline{\chi(-1)}\chi(n)\tau_q(\overline\chi).$$ If $q\mid n$, the inner sum vanishes for nonprincipal $\chi$. Divide by $\sqrt{q-1}$.

The right side is precisely a nonprincipal Dirichlet-character transform of the original packet, up to the explicit Gauss factor and a harmless choice of whether $\chi$ or $\overline\chi$ names the coordinate. Hence the natural whole-frame Poisson route closes back to the V59 character representation `\cite{Wang2026V59}`. It has not emitted the fixed-modulus Kloosterman arrays accepted by the later local engine `\cite{BlomerPascadi2026}`.

# Sharp alignment obstruction

The profile dependence in (5.3) cannot be removed by the graph identity.

> **Theorem: sharp vector-valued alignment** <span id="thm:alignment" label="thm:alignment">\[thm:alignment\]</span> For $c=(c_D)_{D\in\mathcal D}$ define $$L_c:\bigoplus_{D\in\mathcal D}\mathbb C^{G_q}\to\mathbb C^{G_q},
>  \qquad L_c((B_D)_D)=P_q\sum_Dc_DU_DB_D.
>  \tag{7.1}$$ Then $$\boxed{\left\lVert L_c\right\rVert=\left(\sum_D|c_D|^2\right)^{1/2}.}
>  \tag{7.2}$$ Equality is attained on the centered subspace.

> **Proof** The adjoint is $$L_c^*z=(\overline{c_D}U_D^*P_qz)_D.$$ Therefore $$L_cL_c^*z=\sum_D|c_D|^2U_DP_qU_D^*P_qz
>  =\left(\sum_D|c_D|^2\right)P_qz.$$ This proves the upper bound. For a unit vector $z\in\mathbf 1^\perp$, choose $$B_D=\overline{c_D}U_D^*z/\left\lVert c\right\rVert_2.$$ The direct-sum input has unit norm and the output has norm $\left\lVert c\right\rVert_2$.

There is a simpler coherent fixture. For unit weights, take $B_D=U_D^*z$ for one nonzero centered vector $z$. All output vectors then align: the sum of the individual frame energies is $|\mathcal D|\left\lVert z\right\rVert^2$, while the whole-frame energy is $|\mathcal D|^2\left\lVert z\right\rVert^2$. Thus the ratio is exactly $|\mathcal D|$. This is an interface obstruction, not an asymptotic assertion about the actual Möbius coefficients.

# Common-profile resonance and finite validation

If one imposes the additional common-profile condition $B_D=B$, then $M_c=\sum_Dc_DU_D$ is diagonalized by multiplicative characters: $$M_c\chi=\left(\sum_Dc_D\chi(D)\right)\chi,
 \qquad
 \left\lVert P_qM_cP_q\right\rVert=\max_{\chi\ne\chi_0}
 \left|\sum_Dc_D\chi(D)\right|.
 \tag{8.1}$$ This special case still has exact resonance. For $q=5$, $D=2,3$, and $c_2=c_3=-1$, the quadratic character satisfies $\chi(2)=\chi(3)=-1$, so its multiplier is $2$, equal to the coefficient $\ell^1$ mass.

The project contains an independent exact certificate for $q=3,5,7,11,13$. It checks 1500 dual-index rows, 3016 permutation rows, all complete-graph Laplacians, and the alignment ratios. A separate Gaussian sanity script checks the continuous Poisson identity in three configurations; the maximum observed truncation error is below $10^{-12}$. These checks are finite QA artifacts and do not constitute asymptotic evidence.

<div id="tab:certificate">

| quantity                    |                value| status           |
|:----------------------------|--------------------:|:-----------------|
| prime moduli                |        $3,5,7,11,13$| exact            |
| dual reindex rows           |               $1500$| exact            |
| permutation-matrix rows     |               $3016$| exact            |
| $q=5$ coherent energy ratio |                  $2$| exact            |
| Gaussian Poisson cases      |                  $3$| numerical sanity |
| maximum Gaussian error      |  $4.5\times10^{-16}$| numerical sanity |

: Finite certificate summary.

</div>

The exact checks can be reproduced from the repository root with

    cd papers/tpc-209-whole-frame-poisson-mobius-obstruction
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/gaussian_poisson_sanity.py

# Source boundary and route decision

The complete edge frame from TPC-208 is an exact finite-dimensional identity. The Poisson step in Theorem [\[thm:poisson\]](main.tex#L157){reference-type="ref" reference="thm:poisson"}, the covariance in Proposition [\[prop:covariance\]](main.tex#L207){reference-type="ref" reference="prop:covariance"}, the spectral form in Theorem [\[thm:character\]](main.tex#L251){reference-type="ref" reference="thm:character"}, and the Gauss crosswalk in Proposition [\[prop:gauss\]](main.tex#L281){reference-type="ref" reference="prop:gauss"} are proved directly here. No external theorem is used to promote them to an asymptotic estimate.

The current source lock contains a general-sequence BDH architecture and post-emitter Kloosterman estimates `\cite{Harper2024,BlomerPascadi2026}`. The latter accept fixed-modulus bilinear arrays after a valid emitter and norm ledger have been supplied. Equations (5.3) and (6.2) are upstream of that input: they retain divisor-dependent profiles, the exact character family, and the physical diagonal boundary. No locked source proves the required prime-only, signed, block-reassembled profile bound.

The first fatal for this particular route is therefore $$\begin{split}
\texttt{NO\_FRAME\_ONLY\_SCALAR\_EMITTER:}
&\quad\text{Poisson gives one shared dual lattice per dilation, but}\\
&\quad\text{dilation permutations survive; character diagonalization}\\
&\quad\text{returns to V59, and arbitrary profiles align sharply.}
\end{split}$$

This is a scoped stop, not a global nonexistence theorem. The smallest repaired target is a profile-aware estimate for (5.3) on the actual Möbius/hybrid packets, preserving the $(q-2)$ subtraction, prime shell, kernel localization, packet signs, and physical normalization. That target remains open and is the natural next route question.

# Conclusion

The complete TPC-208 edge frame does support a legitimate whole-frame Poisson reindexing, but only in a vector-valued sense. The exact shared integer $n=qr+kD$ survives all edges for one divisor. Across divisors, the residual permutations are not cosmetic: they are the representation-theoretic content of the frame. Multiplicative Fourier exposes a shared character coordinate and simultaneously shows the exact return to the earlier V59 character packets. The sharp alignment theorem rules out obtaining a scalar emitter or a power saving from frame algebra alone.

The result advances the route by replacing a vague “look for a shared dual variable” instruction with a precise profile-aware interface and a precise obstruction. It leaves the arithmetic Gate B status unchanged: $$\texttt{FULL\_GATE\_B=OPEN},\qquad
 \texttt{STRICT\_1/400=UNPAID},\qquad
 \texttt{ARITHMETIC\_ADVANCE=NO}.$$

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{Harper2024,
  author        = {Adam J. Harper},
  title         = {Simple {Barban--Davenport--Halberstam} Type Asymptotics for General Sequences},
  year          = {2024},
  eprint        = {2412.19644},
  archivePrefix  = {arXiv},
  primaryClass  = {math.NT},
  note          = {Version 1}
}

@misc{BlomerPascadi2026,
  author        = {Valentin Blomer and Alexandru Pascadi},
  title         = {Bilinear Forms with {Kloosterman} Sums via Quadratic Characters},
  year          = {2026},
  eprint        = {2607.24311},
  archivePrefix  = {arXiv},
  primaryClass  = {math.NT},
  note          = {Version 1}
}

@misc{Wang2026V59,
  author       = {Liang Wang},
  title        = {Polarized Local {BDH} Scalar Compiler},
  year         = {2026},
  howpublished = {Internal prime-dynamics-theory repository artifact},
  note         = {V59, research/tpc-big-road}
}

@misc{Wang2026TPC208,
  author       = {Liang Wang},
  title        = {A Canonical Additive Edge Frame for Zero-Hole Reduced-Residue {BDH} Remainders},
  year         = {2026},
  howpublished = {TPC-208, internal prime-dynamics-theory paper},
  note         = {Structural L1 release}
}
```

<!-- SOURCE_BODY_END -->
