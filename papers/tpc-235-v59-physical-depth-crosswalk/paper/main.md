# An Exact Physical-Depth Crosswalk and a Single-Clock Obstruction\ for V59 Gate-B Rows

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

We derive an exact crosswalk from the physical V59 Gate-B row to the growing-depth prime-shell clocks used in the preceding model analysis. For denominator $h$, the physical depth is $\lambda_h=hQ/H$: the multiplier cutoff is $\lfloor\lambda_hq/Q\rfloor$, the profile argument is $mQ/(\lambda_hq)$, and the modulus remains $h=(H/Q)\lambda_h$. Simultaneous agreement with the earlier single-clock row of modulus $4LQ$ occurs if and only if $h=4LQ$ and $H=4Q^2$. At the V59 scales $H=x^{21/32}$ and $Q=x^{1/3}$, the latter condition fails by the growing factor $4Q^2/H=4x^{1/96}$. We also prove that independently unit-normalizing the four packet outputs destroys the signed polarization identity: all four squared norms become one and their signed sum vanishes. Thus neither the one-clock geometry nor output-dependent normalization can be transferred automatically to the physical source. The result identifies the correct next object—a weighted many-clock $h$-fiber with explicit divisor weights and one common linear packet transform—but claims no arithmetic cancellation or Gate-B estimate.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Finite model clocks are useful only when their parameters can be traced back to the physical arithmetic source. The preceding prime-shell analysis used a clock of modulus $4LQ$, with multiplier depth approximately $L$. It produced exact support theorems and a depth-uniform Bessel estimate after row normalization. Those results are internally correct, but two transfer questions remained open: whether one modeled clock represents one physical denominator, and whether row normalization respects the four-packet source identity.

This note resolves both questions at the structural level. The physical row has two linked scales, not one: its depth is $\lambda_h=hQ/H$, while its modulus is the denominator $h$. The earlier clock imposes a different modulus–depth relation. Matching both relations is possible exactly at the exceptional scale $H=4Q^2$; V59 has $Q^2/H=x^{1/96}$ and therefore lies on the growing-mismatch side.

The normalization issue is independent. A Bessel theorem for normalized vectors is a legitimate frame-theoretic statement `\citep{christensen2016}`, but the physical source is recovered by a signed four-phase polarization formula. Normalizing each output separately is nonlinear and makes that formula identically zero. Any legal conditioning transform must instead be common and linear across packet labels, with all compensating weights retained explicitly.

The conclusions are deliberately scoped. We prove an exact parameter crosswalk and two incompatibility statements. We do not prove cancellation in the divisor weights, an $L^2$ saving, or the full Gate-B estimate.

# The exact physical-depth crosswalk

Freeze the V59 scales $$H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400},$$ and let $Q<q\le 2Q$ be prime. For a physical denominator $h$, the residue row is $$B_{h,q}(a)=
 \sum_{0<|m|\le\lfloor hq/H\rfloor}
 \psi\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod h}.                 \label{eq:physical-row}$$ The full source additionally contains $$C_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}
 \frac{\mu(d)\log d}{d},\qquad
 K_q(n)=\sum_{h,a}C_hB_{h,q}(a)\mathrm e(na/h).             \label{eq:full-source}$$ where $\mathrm e(t)=e^{2\pi it}$. In particular, deleting $C_h$ or collapsing the $h$-sum is not an innocent change of coordinates.

> **Theorem: Physical-depth reparametrization**<span id="thm:crosswalk" label="thm:crosswalk">\[thm:crosswalk\]</span> Define $$\lambda_h=\frac{hQ}{H}.$$ Then (1) is exactly $$B_{h,q}(a)=
>  \sum_{0<|m|\le\lfloor\lambda_hq/Q\rfloor}
>  \psi\!\left(\frac{mQ}{\lambda_hq}\right)
>  \mathbf 1_{m q^{-1}\equiv a\pmod h},                \label{eq:depth-row}$$ and its modulus satisfies $h=(H/Q)\lambda_h$.

> **Proof** The cutoff identity is $hq/H=(hQ/H)(q/Q)=\lambda_hq/Q$. Likewise $Hm/(hq)=mQ/(\lambda_hq)$. Neither substitution changes the residue condition or the modulus.

> **Corollary: Depth range and denominator grid**<span id="cor:range" label="cor:range">\[cor:range\]</span> If a row is active for some $q\le2Q$ and $h\le U$, then $$\frac12\le\lambda_h\le\frac{UQ}{H}=x^{23/2400}.$$ Consecutive integer denominators are separated by $Q/H$ in depth, so a unit depth interval contains $H/Q+O(1)=x^{31/96+o(1)}$ available denominator-grid points.

> **Proof** Activity implies $hq/H\ge1$, hence $h\ge H/(2Q)$. The upper bound follows from $h\le U$. Finally, $\lambda_{h+1}-\lambda_h=Q/H$.

The final count is a geometric grid count only. It does not assert that every corresponding coefficient $C_h$ in (2) is nonzero.

# The single-clock compatibility obstruction

The modeled clock used modulus $4LQ$, cutoff $\lfloor Lq/Q\rfloor$, and profile argument $mQ/(Lq)$. The next theorem characterizes exact transfer without an asymptotic approximation.

> **Theorem: Compatibility if and only if**<span id="thm:compatibility" label="thm:compatibility">\[thm:compatibility\]</span> For a nonzero depth $L$, the physical row [\[eq:physical-row\]](sections/2_physical_crosswalk.tex#L12){reference-type="eqref" reference="eq:physical-row"} and the modeled row agree in modulus and in cutoff/profile scale for every multiplier and shell prime if and only if $$h=4LQ,\qquad H=4Q^2.                                  \label{eq:compatibility}$$

> **Proof** Equality of moduli gives $h=4LQ$. Equality of the profile arguments for a nonzero multiplier gives $H/h=Q/L$. Substitution yields $H=4Q^2$. Conversely, the two identities in [\[eq:compatibility\]](sections/3_single_clock.tex#L11){reference-type="eqref" reference="eq:compatibility"} make the modulus, cutoff, profile argument, and residue condition identical.

At the V59 scales, $$\frac{4Q^2}{H}=4x^{2/3-21/32}=4x^{1/96}\longrightarrow\infty. \label{eq:clock-gap}$$ Thus exact attachment to the single-clock family is refuted in this scope. Matching the physical depth makes the modeled modulus too large by [\[eq:clock-gap\]](sections/3_single_clock.tex#L24){reference-type="eqref" reference="eq:clock-gap"}; matching the modulus makes its multiplier depth too small by the same factor. This is not a constant-loss bookkeeping discrepancy: the mismatch grows on precisely the conductor-gap scale $Q^2/H$.

Theorem [\[thm:compatibility\]](sections/3_single_clock.tex#L7){reference-type="ref" reference="thm:compatibility"} does not invalidate the modeled clock as an abstract collision problem. It invalidates only the automatic identification of one such clock with one physical V59 row.

# Packet normalization and polarization

Let $T$ be the common linear transform used to assemble the source packets. With the project’s inner-product convention, the four-phase identity has the form $$\langle T\beta,Tw\rangle
 =\frac14\sum_{j=0}^3 i^j\|T(\beta+i^jw)\|^2.          \label{eq:polarization}$$ The key word is *common*: the same linear map acts on all four inputs.

> **Proposition: Output normalization erases polarization** Suppose all four vectors $T(\beta+i^jw)$ are nonzero. If each output in [\[eq:polarization\]](sections/4_polarization.tex#L7){reference-type="eqref" reference="eq:polarization"} is replaced by its own unit normalization, then the resulting right-hand side equals zero. It therefore cannot reproduce (6) in general.

> **Proof** Every normalized squared norm equals one, while $\sum_{j=0}^3i^j=0$. For a concrete counterexample take the one-dimensional map $T=1$, $\beta=1$, and $w=2$. The four raw squared norms are $9,5,1,5$ and [\[eq:polarization\]](sections/4_polarization.tex#L7){reference-type="eqref" reference="eq:polarization"} equals $2$, whereas their independently normalized replacements are $1,1,1,1$ and give zero.

Consequently, the normalized-row Bessel theorem from the model clock is not automatically source-valid. A fixed linear rescaling common to every packet may be legal, but its inverse or compensating weight must remain visible in the physical reassembly. Output-dependent unit normalization cannot be hidden inside [\[eq:full-source\]](sections/2_physical_crosswalk.tex#L18){reference-type="eqref" reference="eq:full-source"}.

# Exact reproduction and the next compiler

The finite certificate evaluates a rational fixture with $H=21$, $Q=5$, $h=14$, and $q=10$. It independently verifies $$\lambda_h=\frac{10}{3},\qquad
 \left\lfloor\frac{hq}{H}\right\rfloor
 =\left\lfloor\frac{\lambda_hq}{Q}\right\rfloor,$$ and checks every profile argument and residue bucket in the two parameterizations. The same fixture shows that matching the modeled modulus can produce cutoff zero where the physical row has cutoff five. The polarization fixture reproduces the transition $2\mapsto0$ exactly.

Three independent programs rebuild the record and reject mutated exponents, cutoffs, profile scales, and packet rules. Its exact finite-record digest is

`f2c12f8cfc21d0cfe6ce95c68462d04da646fd06ee61b5b661ecd39c3be4c4b4`.

The corrected physical object is now unambiguous. It is the weighted direct family $$\bigl\{C_hB_{h,q}: H/(2Q)\le h\le U,\ Q<q\le2Q\bigr\},$$ organized into bands of $\lambda_h=hQ/H$, while retaining one common transform for all four packet labels. Any future Bessel or large-sieve estimate must be proved for this family, not imported from the incompatible single-clock relation.

# Conclusion

The V59 row admits an exact physical depth, but it is a weighted many-clock object. Its modulus–depth relation differs from the earlier single clock by the growing factor $4x^{1/96}$. Independently normalizing packet outputs is also forbidden: it annihilates the signed polarization that recovers the bilinear source.

These are constructive obstructions. They specify the next admissible compiler: retain every physical $h$-fiber, the coefficient $C_h$, and a common linear packet transform, then analyze collisions at the true ratio $Q^2/H=x^{1/96}$. No arithmetic saving, $L^2$ estimate, fixed-atom credit, strict $1/400$ payment, full Gate B, or twin-prime theorem is claimed here.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{christensen2016,
  author    = {Ole Christensen},
  title     = {An Introduction to Frames and Riesz Bases},
  edition   = {Second},
  publisher = {Birkh{\"a}user},
  year      = {2016}
}
```

<!-- SOURCE_BODY_END -->
