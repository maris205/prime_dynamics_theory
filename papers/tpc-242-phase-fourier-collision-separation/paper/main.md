# Phase-Fourier Separation of Unsigned Collision Energy\ from the Signed Four-Packet Channel

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China; liang.wang@hust.edu.cn
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

The literal four-packet projector in the V59 route is a nontrivial Fourier coefficient of four phase-labelled energies, whereas an unsigned collision energy naturally occupies the trivial phase character. We make this separation exact. In a complex Hilbert space with inner product conjugate-linear in the first slot, set $E_j=\left\lVert X+\mathrm{i}^jY\right\rVert^2$ and $F_k=\frac14\sum_{j=0}^3\mathrm{i}^{kj}E_j$. The complete spectrum is $F_0=\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2$, $F_1=\left\langle Y,X\right\rangle$, $F_2=0$, and $F_3=\left\langle X,Y\right\rangle$. Consequently every scalar added identically to all four energies contributes only to $F_0$ and exactly zero to the selected mode $F_1$. At fixed $S=F_0$, the exact feasible set of $F_1$ is the closed disk $\left\lvert z\right\rvert\leq S/2$, including $S=0$. Its boundary deficit splits as $$S^2-4\left\lvert F_1\right\rvert^2
 =\bigl(\left\lVert X\right\rVert^2-\left\lVert Y\right\rVert^2\bigr)^2
  +4\bigl(\left\lVert X\right\rVert^2\left\lVert Y\right\rVert^2-\left\lvert \left\langle Y,X\right\rangle\right\rvert^2\bigr).$$ Applied with source types preserved, these identities show that TPC-241’s standalone unsigned common-profile norm floor gives no direct quantitative information about the V59 signed coefficient. No physical top-prime annihilation, arithmetic cancellation, or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Squaring before retaining phase information can turn a signed target into an unsigned marginal. The distinction is decisive in the four-packet part of the V59 route: the physical scalar is selected by a nontrivial character of the cyclic phase group, while the most accessible collision lower bounds are phase-blind. Equal magnitudes in these two channels do not identify the underlying objects, and a strong estimate in one character need not transfer to another.

The starting polarization identity is already known. For complex scalars, the literal V59 convention reads $$\label{eq:known-polarization}
 x\overline y=\frac14\sum_{j=0}^3\mathrm{i}^j
 \left\lvert x+\mathrm{i}^j y\right\rvert^2.$$ It was source-locked in the V59 compiler and used in earlier TPC obstruction and source-native compiler papers `\cite{WangV59,WangTPC222,WangTPC228}`. We do not claim the four-point polarization formula itself as new. The contribution of this paper within the TPC route is to retain all four characters simultaneously, determine exactly what the trivial character can and cannot say about the selected character, and enforce the resulting source-type boundary against the unsigned TPC-241 estimate.

More precisely, the paper establishes four statements.

1.  We compute the complete $C_4$ spectrum of the four Hilbert energies in the literal $\mathrm{i}^j$ convention. This fixes the orientation $F_1=\left\langle Y,X\right\rangle$, proves $F_2=0$, and identifies $F_3$ as the conjugate mode.

2.  We prove that a genuinely phase-independent additive scalar is supported only at $F_0$. The conclusion is an exact character projection, not a heuristic assertion that an unrelated unsigned term is “common.”

3.  For every fixed total energy $S$, we identify the full feasible set of $F_1$ as the disk of radius $S/2$ and prove a defect formula separating norm imbalance from the two-vector Gram determinant.

4.  We apply these facts with source types intact. TPC-241 concerns a standalone common-profile kernel and explicitly does not project the four physical packets `\cite{WangTPC241}`; absent an attachment theorem, it earns zero direct quantitative credit for the V59 $F_1$ channel.

The disk theorem is sharp in both directions. Thus even exact knowledge of $F_0$ cannot force nonvanishing, sign, phase, or a positive lower bound for $F_1$. A lower bound on a separate unsigned object is weaker still. This does not imply that the physical top-prime contribution vanishes: survival, attenuation, cancellation, and annihilation remain logically possible until the literal contribution is decomposed phase by phase before squaring.

Section [2](sections/2_v59_source_lock.tex#L1){reference-type="ref" reference="sec:source-lock"} fixes the V59 convention and source types. Sections [3](sections/3_phase_fourier_theorem.tex#L1){reference-type="ref" reference="sec:spectrum"} and [4](sections/4_feasible_disk.tex#L1){reference-type="ref" reference="sec:disk"} prove the complete spectrum, sharp disk, and defect identity. Section [5](sections/5_tpc241_no_transfer.tex#L1){reference-type="ref" reference="sec:no-transfer"} states the typed consequence for TPC-241. The certificate and claim boundary are recorded in Sections [6](sections/6_certificate.tex#L1){reference-type="ref" reference="sec:certificate"} and [7](sections/7_route_boundary.tex#L1){reference-type="ref" reference="sec:boundary"}.

# Literal V59 convention and source lock

Let $\mathcal{H}$ be a complex Hilbert space. Throughout, $\left\langle \cdot,\cdot\right\rangle$ is conjugate-linear in its first slot and linear in its second. Hence $$\left\langle \alpha u,v\right\rangle=\overline\alpha\left\langle u,v\right\rangle,
 \qquad
 \left\langle u,\alpha v\right\rangle=\alpha\left\langle u,v\right\rangle.$$ This convention must be declared because changing it changes which oriented cross coefficient is selected by a fixed Fourier sign.

The V59 source freezes four literal packets of the form $$a^{(j)}=\beta+\mathrm{i}^j w,\qquad 0\leq j\leq3,$$ and uses the multiplier $\frac14\sum_j\mathrm{i}^j$ on the corresponding off-diagonal energy remainders `\cite{WangV59}`. In the present convention the scalar identity [\[eq:known-polarization\]](sections/1_introduction.tex#L13){reference-type="eqref" reference="eq:known-polarization"} has orientation $$x\overline y=\left\langle y,x\right\rangle.$$ Thus the source target is the $k=1$ mode defined below. Replacing the phase multiplier by $(-\mathrm{i})^j$, or silently switching to a linear-first inner product, would select the conjugate orientation instead.

Earlier papers establish two relevant boundaries. TPC-222 records exact four-point polarization and shows that diagonal or trace information alone does not identify signed reassembly `\cite{WangTPC222}`. TPC-228 performs the source-native off-prime polarization after deleting the same-label diagonal, but leaves the literal physical packet-to-primitive-atom crosswalk open `\cite{WangTPC228}`. TPC-241 then proves a sharp unsigned lower bound for a fixed common-profile top-prime collision kernel; its scope statement says explicitly that no four-packet projection is taken `\cite{WangTPC241}`.

These sources determine a strict type boundary:

| Object         | Source type                                                |
|:---------------|:-----------------------------------------------------------|
| V59 target     | $k=1$ coefficient of four literal packet energies          |
| TPC-241 output | unsigned norm floor for a standalone common-profile kernel |
| Missing map    | phase-by-phase physical attachment to the V59 remainder    |

The structural theorem below applies whenever one common pair $(X,Y)$ really generates the four energies. It does not manufacture the missing map.

# The complete phase-Fourier theorem

For $X,Y\in\mathcal{H}$, define $$\label{eq:def-energy-dft}
 E_{j}=\left\lVert X+\mathrm{i}^jY\right\rVert^2,
 \qquad
 F_{k}=\frac14\sum_{j=0}^3\mathrm{i}^{kj}E_{j},
 \qquad 0\leq k\leq3.$$

> **Theorem: Complete $C_4$ spectrum**<span id="thm:spectrum" label="thm:spectrum">\[thm:spectrum\]</span> With the conjugate-linear-first convention, $$\label{eq:complete-spectrum}
>  F_{0}=\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2,
>  \qquad F_{1}=\left\langle Y,X\right\rangle,
>  \qquad F_{2}=0,
>  \qquad F_{3}=\left\langle X,Y\right\rangle.$$

> **Proof** Put $S=\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2$ and $c=\left\langle Y,X\right\rangle$. Conjugate-linearity in the first variable gives $$\begin{aligned}
>  E_{j}
>  &=\left\langle X+\mathrm{i}^jY,X+\mathrm{i}^jY\right\rangle\\
>  &=S+\mathrm{i}^j\left\langle X,Y\right\rangle+\mathrm{i}^{-j}\left\langle Y,X\right\rangle
>   =S+\mathrm{i}^j\overline c+\mathrm{i}^{-j}c.\end{aligned}$$ For every integer $m$, fourth-root orthogonality says $$\label{eq:root-filter}
>  \frac14\sum_{j=0}^3\mathrm{i}^{mj}
>  =\begin{cases}1,&4\mid m,\\0,&4\nmid m.\end{cases}$$ Substitution into [\[eq:def-energy-dft\]](sections/3_phase_fourier_theorem.tex#L4){reference-type="eqref" reference="eq:def-energy-dft"} yields $$F_{k}=S\mathbf1_{k=0}+c\mathbf1_{k=1}
>               +\overline c\mathbf1_{k=3}
>  \quad (0\leq k\leq3),$$ which is [\[eq:complete-spectrum\]](sections/3_phase_fourier_theorem.tex#L13){reference-type="eqref" reference="eq:complete-spectrum"}.

The theorem contains the familiar polarization identity as its $k=1$ coordinate, but it also displays the trivial mode, the identically zero second mode, and the conjugate third mode. Since every $E_j$ is real, $F_3=\overline{F_1}$ is also the expected Fourier reality symmetry.

> **Corollary: Common-offset projection**<span id="cor:offset" label="cor:offset">\[cor:offset\]</span> Suppose a scalar $A$ is added independently of phase, so that $E'_j=E_j+A$ for all four $j$. Then $$F'_0-F_0=A,
>  \qquad
>  F'_1-F_1=F'_2-F_2=F'_3-F_3=0.$$ In particular, every phase-independent additive scalar contributes exactly zero to the V59-selected mode $F_1$.

> **Proof** The increment is $\frac A4\sum_j\mathrm{i}^{kj}$, and equation [\[eq:root-filter\]](sections/3_phase_fourier_theorem.tex#L31){reference-type="eqref" reference="eq:root-filter"} applies.

> **Remark: Type of the hypothesis** Corollary [\[cor:offset\]](sections/3_phase_fourier_theorem.tex#L49){reference-type="ref" reference="cor:offset"} assumes the same scalar is proved to occur inside each of the four labelled energies. It does not license the replacement of an unsigned estimate on a separate kernel by such a common term. Establishing that equality is part of the physical attachment problem.

# The sharp feasible disk and phase defect

The trivial mode controls the selected mode only through a sharp disk.

> **Theorem: Exact fixed-energy feasible set**<span id="thm:disk" label="thm:disk">\[thm:disk\]</span> Let $\mathcal{H}$ be nonzero and fix $S\geq0$. Over all pairs $X,Y\in\mathcal{H}$ satisfying $\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2=S$, the set of possible values of $F_1=\left\langle Y,X\right\rangle$ is exactly $$\label{eq:disk}
>  \left\{z\in\mathbb{C}:\left\lvert z\right\rvert\leq\frac S2\right\}.$$ For $S=0$, this disk is the singleton $\{0\}$.

> **Proof** Cauchy–Schwarz followed by the arithmetic–geometric mean inequality gives $$\left\lvert \left\langle Y,X\right\rangle\right\rvert\leq\left\lVert X\right\rVert\left\lVert Y\right\rVert
>  \leq\frac{\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2}{2}=\frac S2.$$ This proves one inclusion.
>
> For the converse, suppose first that $S>0$ and choose any $z$ with $\rho:=\left\lvert z\right\rvert\leq S/2$. Put $$D=\sqrt{S^2-4\rho^2},\qquad
>  a=\frac{S+D}{2},\qquad b=\frac{S-D}{2}.$$ Then $a>0$, $a+b=S$, and $ab=\rho^2$. Choose a unit vector $e\in\mathcal{H}$ and define $$\label{eq:disk-witness}
>  X=\sqrt a\,e,\qquad
>  Y=\frac{\overline z}{\sqrt a}\,e.$$ Consequently, $$\left\lVert X\right\rVert^2=a,\qquad
>  \left\lVert Y\right\rVert^2=\frac{\left\lvert z\right\rvert^2}{a}=b,
>  \qquad
>  \left\langle Y,X\right\rangle=z.$$ Thus every point in [\[eq:disk\]](sections/4_feasible_disk.tex#L9){reference-type="eqref" reference="eq:disk"} is attained. If $S=0$, both nonnegative squared norms vanish, so $X=Y=0$ and $F_1=0$.

The construction realizes the center, every interior point, and every boundary phase. Consequently even an exact value of $F_0$ gives no positive lower bound for $\left\lvert F_1\right\rvert$ and no preferred argument of $F_1$. For instance, at $S=2$, orthogonal unit vectors give $F_1=0$, whereas $X=(1,0)$ and $Y=(-\mathrm{i},0)$ give $F_1=\mathrm{i}$ on the boundary.

The distance from the boundary has a canonical two-part decomposition.

> **Theorem: Exact phase-defect identity**<span id="thm:defect" label="thm:defect">\[thm:defect\]</span> Let $S=\left\lVert X\right\rVert^2+\left\lVert Y\right\rVert^2$ and $F_1=\left\langle Y,X\right\rangle$. Then $$\label{eq:defect}
>  S^2-4\left\lvert F_1\right\rvert^2
>  =\bigl(\left\lVert X\right\rVert^2-\left\lVert Y\right\rVert^2\bigr)^2
>   +4\left(\left\lVert X\right\rVert^2\left\lVert Y\right\rVert^2-\left\lvert \left\langle Y,X\right\rangle\right\rvert^2\right).$$ Both terms on the right are nonnegative.

> **Proof** Set $a=\left\lVert X\right\rVert^2$ and $b=\left\lVert Y\right\rVert^2$. Expanding and inserting $4ab$ gives $$(a+b)^2-4\left\lvert \left\langle Y,X\right\rangle\right\rvert^2
>  =(a-b)^2+4\left(ab-\left\lvert \left\langle Y,X\right\rangle\right\rvert^2\right).$$ The final parenthesis is the determinant of the Gram matrix of $X$ and $Y$, so Cauchy–Schwarz makes it nonnegative.

Equality $\left\lvert F_1\right\rvert=S/2$ holds precisely when the norms agree and the Gram determinant vanishes. Away from the boundary, equation [\[eq:defect\]](sections/4_feasible_disk.tex#L56){reference-type="eqref" reference="eq:defect"} distinguishes two mechanisms: imbalance between packet energies and angular decorrelation between the packet vectors. Any future strict signed saving must create a quantitative defect of one of these forms on the attached physical object.

# Typed no-transfer from TPC-241

TPC-241 proves a lower bound for an unsigned top-prime collision energy $E_{\mathrm{top}}^\psi$ and, after a full-vector lower-frame step, for the finite-window norm of a standalone common-profile synthesis $K_\psi$ `\cite{WangTPC241}`. The profile is fixed independently of the asymptotic parameter. The result is sharp at its unsigned fixed-power scale, but its scope statement records that it does not use the sign after absolute squaring and does not project through the four literal packets.

By contrast, Theorem [\[thm:spectrum\]](sections/3_phase_fourier_theorem.tex#L11){reference-type="ref" reference="thm:spectrum"} begins with four energies generated by one proved common pair $(X,Y)$ and their phase labels. To substitute the TPC-241 result into this theorem, one would need a source-backed equality of at least one of the following forms: $$\label{eq:missing-maps}
 K_\psi=T\beta,\qquad K_\psi=Tw,\qquad
 E_{\mathrm{top}}^\psi=F_0,\qquad
 E_{\mathrm{top}}^\psi=A\ \text{inside every }E_j.$$ No locked source proves any equality in [\[eq:missing-maps\]](sections/5_tpc241_no_transfer.tex#L15){reference-type="eqref" reference="eq:missing-maps"}. Similar notation, a shared profile, or an unsigned norm scale cannot replace an identification theorem.

> **Corollary: Source-typed TPC-241 boundary**<span id="cor:no-transfer" label="cor:no-transfer">\[cor:no-transfer\]</span> TPC-241’s standalone unsigned common-profile norm floor supplies zero direct quantitative implication for the literal V59 coefficient $F_1$. In particular, it directly proves none of a lower bound, upper bound, nonvanishing statement, phase restriction, sign statement, or power saving for that coefficient.

> **Proof** The hypotheses needed to identify the TPC-241 object with either a V59 marginal or a common additive term are absent. Therefore neither Theorem [\[thm:disk\]](sections/4_feasible_disk.tex#L5){reference-type="ref" reference="thm:disk"} nor Corollary [\[cor:offset\]](sections/3_phase_fourier_theorem.tex#L49){reference-type="ref" reference="cor:offset"} can be instantiated with the TPC-241 floor. This is a failure of a required source-type conversion, not a numerical loss that can be absorbed into an estimate.

Corollary [\[cor:no-transfer\]](sections/5_tpc241_no_transfer.tex#L24){reference-type="ref" reference="cor:no-transfer"} is deliberately scoped. It does not say that the actual top-prime contribution has zero $k=1$ coefficient. The physical mode may survive, attenuate, cancel, or vanish after phase projection. Those possibilities remain open until the top-prime contribution is expressed in each literal packet before squaring and its actual Fourier coefficient is computed. The phrase “zero direct implication” refers to logical credit from TPC-241, not to the value of the unknown physical mode.

# Exact executable certificate

The accompanying executable artifact checks the convention-sensitive finite algebra using Gaussian numbers represented as pairs of `fractions.Fraction` values. It evaluates the four energies, performs the $C_4$ transform, recomputes both sides of the defect identity, and checks exact witnesses at the center, interior, and boundary of the feasible disk. No floating-point comparison appears in a theorem-facing check.

The producer has a required mutually exclusive interface: `–write` creates the canonical certificate, while `–check` is read-only. The JSON representation uses sorted keys, compact separators, ASCII encoding, one terminal newline, reduced fractions with positive denominators, and a SHA-256 digest over the payload. A separately implemented checker parses the document with duplicate-key and nonfinite-constant rejection and recomputes the exact fixtures without importing the producer.

Both programs exercise semantic mutation firewalls. They reject an inner-product orientation reversal, replacement of $\mathrm{i}^j$ by $(-\mathrm{i})^j$, a nonzero $F_2$, leakage of a common offset into $F_1$, a fabricated physical attachment, a status promotion, and Python’s boolean-as-integer ambiguity. The digest is recomputed on semantic mutations before validation, so mutation rejection cannot be credited merely to stale checksums. Parser mutations also test duplicate keys and nonfinite constants.

Finally, an independent stress program exhausts all ordered pairs of two-dimensional vectors whose component real and imaginary parts lie in $\{-1,0,1\}$. This is $81^2=6561$ vector pairs and $26244$ phase-energy evaluations. Every calculation is exact, but the census is labelled

`NUMERICAL_FINITE_ILLUSTRATION_ONLY`.

The executable artifacts test transcription, representation, and finite interfaces. The symbolic proofs in Sections [3](sections/3_phase_fourier_theorem.tex#L1){reference-type="ref" reference="sec:spectrum"} and [4](sections/4_feasible_disk.tex#L1){reference-type="ref" reference="sec:disk"}, rather than the finite census, establish the theorem.

# Route boundary and remaining loss ledger

The result advances the route by isolating a structural obstruction. It does not advance the arithmetic endpoint. Table [1](sections/7_route_boundary.tex#L29){reference-type="ref" reference="tab:ledger"} records the claim boundary.

<div id="tab:ledger">

| Item                                             | Status          |
|:-------------------------------------------------|:----------------|
| Complete literal-convention $C_4$ spectrum       | Proved exactly  |
| Sharp fixed-$F_0$ cross disk and defect identity | Proved exactly  |
| Phase-blind common-offset projection             | Proved exactly  |
| Direct TPC-241 quantitative credit for V59 $F_1$ | Zero            |
| TPC-241-to-V59 physical identification           | Open            |
| Physical top-prime annihilation                  | Not claimed     |
| Signed $C_h$ cancellation theorem                | None            |
| Arithmetic $L2$                                  | None            |
| Fixed-atom credit                                | $0$             |
| Strict $1/400$ loss                              | Unpaid globally |
| Full Gate B                                      | Open            |
| Twin-prime conclusion                            | None            |

: The normalization and claim ledger. Structural identities do not pay arithmetic losses.

</div>

The strongest obstruction can be stated without asymptotics: exact knowledge of the unsigned total energy admits all selected coefficients in a closed disk. Therefore a route that estimates only the trivial character cannot by itself establish a distinguished nontrivial coefficient. This conclusion is stronger than observing that one particular lower-bound proof loses signs; it identifies the full set of cross terms consistent with the total energy.

The narrowest valid next step is also clear. One must express the literal top-prime contribution separately in each physical packet $\beta+\mathrm{i}^j w$ before absolute squaring, prove that this decomposition belongs to the V59 remainder, and compute its actual $k=1$ coefficient. Only then can one test whether imbalance, Gram decorrelation, or arithmetic sign cancellation creates a useful phase defect. Until that source-backed attachment is available, no promotion beyond structural L1 is justified.

Accordingly the maximum status of this paper is

`PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER`.

# Conclusion

The four phase energies split exactly into a trivial total-energy mode, one oriented cross mode, an identically zero second mode, and the conjugate cross mode. This complete spectrum fixes the V59 orientation and proves exact annihilation of genuinely phase-independent additive terms in the selected channel. The selected coefficient at fixed total energy fills a sharp closed disk, while its boundary defect separates norm imbalance from the Gram determinant.

These facts close a logical loophole but not the arithmetic gate. TPC-241’s unsigned common-profile floor has no proved physical crosswalk to the four V59 packets and therefore provides zero direct information about their signed $k=1$ coefficient. That statement must not be read as physical vanishing. The next theorem must retain the literal phase labels through the top-prime decomposition and compute the attached cross mode before squaring. Signed cancellation, arithmetic $L2$, the strict $1/400$ endpoint, full Gate B, and the twin-prime objective all remain open.

# Source and status ledger

For reproducibility, the source lock uses the following repository anchors at baseline

`845256279ca1126c592e210801ce3dbb3d743eab`.

-   V59 polarization compiler, lines 143–205;

-   TPC-222 proof package, lines 8–24;

-   TPC-228 proof package, lines 3–65;

-   TPC-241 proof package, lines 19–40 and 141–146.

The accompanying source-lock note records full paths and SHA-256 digests.

The machine-readable status cell is reproduced below with breakable monospaced lines.\
\

\

The result is an exact abstract Hilbert-space theorem plus a source-typed non-transfer corollary. It contains no $x$-asymptotic arithmetic estimate and does not identify any physical top-prime V59 marginal.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@unpublished{WangV59,
  author = {Liang Wang},
  title  = {Polarized Local BDH Scalar Compiler},
  note   = {Bridge B V59 repository technical report},
  year   = {2026}
}

@unpublished{WangTPC222,
  author = {Liang Wang},
  title  = {Four-Packet Polarization and the PSD Cross-Term Obstruction},
  note   = {TPC-222 repository manuscript and proof package},
  year   = {2026}
}

@unpublished{WangTPC228,
  author = {Liang Wang},
  title  = {A Source-Native Polarized Collision Compiler},
  note   = {TPC-228 repository manuscript and proof package},
  year   = {2026}
}

@unpublished{WangTPC241,
  author = {Liang Wang},
  title  = {A Top-Prime Collision Lower Bound at the One-over-Forty-Eight Barrier},
  note   = {TPC-241 repository manuscript and proof package},
  year   = {2026}
}
```

<!-- SOURCE_BODY_END -->
