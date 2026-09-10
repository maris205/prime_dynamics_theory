# A Source-Native Polarized Collision Compiler

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

We give an exact source-native compiler from four-phase packet energies to a prime-labelled collision form. If $U_q$ and $V_q$ are the common-profile row images of two source sequences and $W_q^{(j)}=U_q+\mathrm i^jV_q$, then the four-phase combination of AP energy minus its same-prime diagonal equals $\sum_{q\ne r}\langle U_q,V_r\rangle$. Thus packet phase remains on the source axis, the profile transform remains common, and diagonal deletion occurs before collision interpretation. On the first primitive $3$–$7$ resonance the compiler becomes an explicit four-term source block over two shared residues. Exact rational fixtures realize positive, negative, zero, directed and single-coordinate values. The result identifies the missing arithmetic correlation but does not estimate it; Route-B level 2 and any twin-prime conclusion remain open.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Four-phase polarization in the V59 compiler places the phases in the literal source sequences $\beta+\mathrm i^jw$ and uses one common Fourier–Poisson profile `\cite{tpc59}`. TPC-227 proved that a packet-dependent transform preserves this compiler for all sources only when its Gram equals the physical common Gram `\cite{tpc227}`. That theorem removes a typing ambiguity but leaves a constructive question: what exact collision scalar results when the source phase is kept in the right place?

We answer that question at the finite Hilbert level. Prime-labelled row transforms of $\beta$ and $w$ are denoted $U_q$ and $V_q$. The natural packet row is $U_q+\mathrm i^jV_q$. Instead of taking an unsigned envelope, we first subtract the same-prime quadratic diagonal and then polarize. The result is exactly the ordered off-diagonal source correlation $$\sum_{q\ne r}\langle U_q,V_r\rangle.$$

The first primitive collision classified in TPC-226 `\cite{tpc226}` then supplies a minimal four-term block. This does not determine an arithmetic sign, but it replaces the former free-profile sign question by a literal source-labelled target.

# Common-profile packet rows

Let $\mathcal Q$ be a finite set of prime labels and let $\mathcal H$ be a complex Hilbert space with inner product linear in the first argument. For each $q$, let $T_q$ denote a fixed row transform. The transform may depend on the prime row, but not on the packet label. Put $$U_q=T_q\beta,\qquad V_q=T_q w,$$ and define four packet rows $$W_q^{(j)}=U_q+\mathrm i^jV_q,\qquad 0\le j\le3.
 \label{eq:packet-row}$$ For each packet define $$E_{\rm AP}^{(j)}=\left\|\sum_qW_q^{(j)}\right\|^2,
 \qquad
 E_{\rm diag}^{(j)}=\sum_q\|W_q^{(j)}\|^2.
 \label{eq:energies}$$

The subtraction in [\[eq:energies\]](sections/2_common_profile.tex#L20){reference-type="eqref" reference="eq:energies"} removes all $q=r$ terms before the outer four-phase sum. This order mirrors the diagonal-corrected V59 quadratic functional; moving the subtraction after an absolute-value estimate would lose the signed identity.

# Exact polarized collision identity

> **Theorem: Source-native collision compiler** <span id="thm:compiler" label="thm:compiler">\[thm:compiler\]</span> For the rows in [\[eq:packet-row\]](sections/2_common_profile.tex#L13){reference-type="eqref" reference="eq:packet-row"}, $$\boxed{
>  \frac14\sum_{j=0}^3\mathrm i^j
>  \bigl(E_{\rm AP}^{(j)}-E_{\rm diag}^{(j)}\bigr)
>  =\sum_{q\ne r}\langle U_q,V_r\rangle.}
>  \label{eq:compiler}$$

> **Proof** Expanding the two energies gives $$E_{\rm AP}^{(j)}-E_{\rm diag}^{(j)}
>  =\sum_{q\ne r}
>  \langle U_q+\mathrm i^jV_q,U_r+\mathrm i^jV_r\rangle.$$ For one ordered pair, multiplication by $\mathrm i^j$ makes the coefficient of $\langle U_q,V_r\rangle$ equal to one. The $U$–$U$ and $V$–$V$ coefficients sum to $\sum_j\mathrm i^j=0$, while the conjugate cross coefficient sums to $\sum_j\mathrm i^{2j}=0$. The desired coefficient sums to four. Interchanging the finite sums proves [\[eq:compiler\]](sections/3_compiler.tex#L11){reference-type="eqref" reference="eq:compiler"}.

> **Corollary** If distinct prime rows have disjoint output support, the polarized AP-minus-diagonal scalar vanishes exactly. Every nonzero contribution is supported on a cross-prime collision coordinate.

The theorem is indifferent to how the common row maps are represented. Its source content comes from the fixed identification of $U$ with the $\beta$ channel and $V$ with the $w$ channel, rather than from a chosen packet profile.

# The first 3–7 source block

TPC-226 gives the first primitive resonance at $$Q=25,\quad h=400,\quad (p,r)=(37,47),$$ with shared residues $119$ and $281$. The corresponding multipliers are $(3,-7)$ at the first coordinate and $(-3,7)$ at the second. Restricting Theorem [\[thm:compiler\]](sections/3_compiler.tex#L4){reference-type="ref" reference="thm:compiler"} to these two coordinates yields $$\frac1{400^2}\bigl(
 \beta_{37,3}w_{47,-7}+\beta_{47,-7}w_{37,3}
 +\beta_{37,-3}w_{47,7}+\beta_{47,7}w_{37,-3}
 \bigr).
 \label{eq:q25}$$

Formula [\[eq:q25\]](sections/4_q25_block.tex#L15){reference-type="eqref" reference="eq:q25"} has no free profile signs. Its sign is determined by the cross-prime source amplitudes. Setting all eight amplitudes to one gives $1/40000$; negating the four $w$ amplitudes gives $-1/40000$; taking opposite $w$ signs on the two prime rows gives zero. A directed $\beta_p$–$w_r$ source gives $1/80000$, and one active shared coordinate gives $1/160000$.

These controls prove that geometry alone still does not determine the sign. Their advance is that the sign freedom now belongs to named source channels rather than to arbitrary packet profiles.

# Certification and boundary

The certificate implements Gaussian-rational vectors and checks Theorem [\[thm:compiler\]](sections/3_compiler.tex#L4){reference-type="ref" reference="thm:compiler"} without floating point. Five Q25 fixtures cover both signs, zero, one orientation and one collision coordinate. A separate three-row graph checks that the identity is not special to one matching edge, and a disjoint-support control checks exact vanishing. An independent script rederives all Q25 values directly from $h^2=160000$; normal and optimized modes are byte-identical. Eight semantic mutations of the source/profile axes, theorem level and signed controls are rejected.

The actual map from the V59 coefficient index $n$ to primitive multiplier amplitudes in [\[eq:q25\]](sections/4_q25_block.tex#L15){reference-type="eqref" reference="eq:q25"} has not been constructed. Nor has any average of [\[eq:q25\]](sections/4_q25_block.tex#L15){reference-type="eqref" reference="eq:q25"} over growing scales been bounded. Consequently the certificate is structural evidence only: arithmetic cancellation, fixed-atom credit and the strict $1/400$ endpoint are absent.

# Conclusion

The common-profile four-packet interface now has an exact collision output. Polarizing after same-prime diagonal deletion produces the ordered source bilinear form and nothing else. On the first primitive resonance this becomes the explicit four-term block [\[eq:q25\]](sections/4_q25_block.tex#L15){reference-type="eqref" reference="eq:q25"}. The next minimal structural problem is to understand how these blocks assemble across the $3$–$7$ resonance graph—in particular, whether the graph has a sharp block decomposition that isolates the precise signed arithmetic input.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc59,author={Liang Wang},title={Polarized Local BDH Scalar Compiler},year={2026},note={V59 repository proof record}}
@misc{tpc226,author={Liang Wang},title={First Primitive-Collision Transition in Dilated Shared Clocks},year={2026},note={TPC-226 repository proof record}}
@misc{tpc227,author={Liang Wang},title={Packet/Profile Axis Separation for Source-Native Four-Phase Polarization},year={2026},note={TPC-227 repository proof record}}
```

<!-- SOURCE_BODY_END -->
