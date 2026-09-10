# Packet/Profile Axis Separation for Source-Native\ Four-Phase Polarization

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

Four-phase polarization converts a bilinear source correlation into four quadratic packet energies. A previous finite collision model obtained a negative cross term by placing signs in row-dependent packet profiles, while the source identity places the four phases in the coefficient sequences and uses one common Poisson profile. We prove an exact axis-separation theorem. Given a physical transform $T$ and packet-dependent transforms $T_j$, the four-phase formula recovers $\langle Tx,Ty\rangle$ for every source pair if and only if $T_j^*T_j=T^*T$ for all four packets. Thus global packet phases are invisible, whereas row-dependent signs can alter collision Gram entries. On the first primitive $3$–$7$ collision, at $Q=25$, the aligned and odd-sign Gram blocks differ off diagonal by exactly $-1/80000$. This rigorously blocks an automatic transfer of the finite profile sign to the physical source compiler while preserving the finite model result itself. The result is structural; no arithmetic cancellation or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The Route-B program studies a fixed twin-prime correlation through a sequence of exact reorganizations. The source-native scalar compiler expresses the physical bilinear form by four quadratic packets $$a^{(j)}=\beta+\mathrm i^j w,\qquad
 \mathfrak C_x=\frac14\sum_{j=0}^3\mathrm i^j
 \mathcal V^{\circ}_{\mathcal Q,H}(a^{(j)}),
 \label{eq:physical-polarization}$$ using a single smooth profile $\psi_+$ in every functional $\mathcal V^{\circ}_{\mathcal Q,H}$ `\cite{tpc59}`. Later finite row models allowed independent bounded profiles $\psi_j$ as a structural Hilbert-space lift `\cite{tpc218}`. That freedom was useful for testing collision geometry but did not change the typing of [\[eq:physical-polarization\]](sections/1_introduction.tex#L10){reference-type="eqref" reference="eq:physical-polarization"}.

The first legitimate primitive collision occurs at dilation four and has resonance $7p+3r=16Q$ `\cite{tpc226}`. On that graph an odd row profile reverses the sign of the cross-prime correction. The natural next question is whether this sign can be read as the source phase in [\[eq:physical-polarization\]](sections/1_introduction.tex#L10){reference-type="eqref" reference="eq:physical-polarization"}. The answer is not a matter of boundedness or support: it is an exact Gram compatibility question.

Our main result gives a necessary-and-sufficient criterion. It separates three facts that otherwise look similar: a phase multiplying an entire transform, a sign attached to a source packet, and a sign depending on the row preimage of a collision. Only the first is automatically invisible to quadratic energy. The third changes cross-row Gram entries and therefore requires an independent physical realization theorem.

This paper contributes an exact operator theorem, a rational first-collision witness, and a fail-closed certificate. It does not estimate the arithmetic source sequences.

# The two axes in the source compiler

Let $\mathcal H_{\rm src}$ contain source coefficient vectors and let $\mathcal H_{\rm out}$ contain the localized character/Fourier output. The physical transform $T:\mathcal H_{\rm src}\to\mathcal H_{\rm out}$ includes the common kernel and profile. Four-phase polarization is the scalar identity $$\langle Tx,Ty\rangle
 =\frac14\sum_{j=0}^3\mathrm i^j\|T(x+\mathrm i^jy)\|^2.
 \label{eq:common-transform}$$ The packet label $j$ changes the input $x+\mathrm i^j y$; it does not change $T$.

Suppose instead that a structural model uses $T_j$ in packet $j$ and forms $$F_{\boldsymbol T}(x,y)
 :=\frac14\sum_{j=0}^3\mathrm i^j\|T_j(x+\mathrm i^jy)\|^2.
 \label{eq:packet-transform}$$ Equation [\[eq:packet-transform\]](sections/2_source_typing.tex#L17){reference-type="eqref" reference="eq:packet-transform"} is well-defined for arbitrary bounded operators, but it need not equal the physical target [\[eq:common-transform\]](sections/2_source_typing.tex#L9){reference-type="eqref" reference="eq:common-transform"}. In particular, a uniform norm bound on $T_j$ controls size but not the phase moments that remove the self and conjugate-cross terms.

> **Remark** If $T_j=\zeta_jT$ with $|\zeta_j|=1$, then every squared norm in [\[eq:packet-transform\]](sections/2_source_typing.tex#L17){reference-type="eqref" reference="eq:packet-transform"} is unchanged. Such an output phase cannot create a signed energy effect. A row-dependent sign is different: after two input rows meet at one output coordinate, it changes their mutual Gram entry.

# Exact Gram compatibility

We take Hilbert inner products to be linear in the first argument.

> **Theorem: Four-Gram criterion** <span id="thm:gram" label="thm:gram">\[thm:gram\]</span> Let $T,T_0,T_1,T_2,T_3:\mathcal H_{\rm src}\to\mathcal H_{\rm out}$ be bounded linear operators. Then $$F_{\boldsymbol T}(x,y)=\langle Tx,Ty\rangle
>  \quad\text{for every }x,y\in\mathcal H_{\rm src}
>  \label{eq:target}$$ if and only if $$T_j^*T_j=T^*T\qquad(0\leq j\leq3).
>  \label{eq:four-gram}$$

> **Proof** Write $Q_j=T_j^*T_j$, $Q=T^*T$, and introduce the four-point operator Fourier moments $$A_k=\frac14\sum_{j=0}^3\mathrm i^{kj}Q_j.$$ Expanding the norm in [\[eq:packet-transform\]](sections/2_source_typing.tex#L17){reference-type="eqref" reference="eq:packet-transform"} gives $$F_{\boldsymbol T}(x,y)=
>  \langle A_1x,x\rangle+\langle A_1y,y\rangle
>  +\langle A_0x,y\rangle+\langle A_2y,x\rangle.
>  \label{eq:dft-expansion}$$ Assume [\[eq:target\]](sections/3_gram_criterion.tex#L11){reference-type="eqref" reference="eq:target"}. Setting $y=0$ and polarizing the real and imaginary Hermitian parts gives $A_1=0$. Since $A_3=A_1^*$, also $A_3=0$. We are left with $$\langle A_0x,y\rangle+\langle A_2y,x\rangle=\langle Qx,y\rangle.
>  \label{eq:two-crosses}$$ Replace $y$ by $\mathrm iy$. The first and target terms in [\[eq:two-crosses\]](sections/3_gram_criterion.tex#L37){reference-type="eqref" reference="eq:two-crosses"} acquire the factor $-\mathrm i$, while the second acquires $\mathrm i$. Combining the two equations gives $A_2=0$, and then $A_0=Q$. Fourier inversion yields $Q_j=Q$ for every $j$, proving necessity.
>
> Conversely, [\[eq:four-gram\]](sections/3_gram_criterion.tex#L16){reference-type="eqref" reference="eq:four-gram"} makes every quadratic form in [\[eq:packet-transform\]](sections/2_source_typing.tex#L17){reference-type="eqref" reference="eq:packet-transform"} equal to the corresponding quadratic form for $T$. The ordinary four-phase polarization identity then gives [\[eq:target\]](sections/3_gram_criterion.tex#L11){reference-type="eqref" reference="eq:target"}.

For real finite matrices, Theorem [\[thm:gram\]](sections/3_gram_criterion.tex#L6){reference-type="ref" reference="thm:gram"} is checked by the exact conditions $$A_0=Q,\quad
 \Re A_1=(Q_0-Q_2)/4=0,\quad
 \Im A_1=(Q_1-Q_3)/4=0,\quad
 A_2=(Q_0-Q_1+Q_2-Q_3)/4=0.$$ These are equivalent to four separate target-Gram equalities, not merely to equality among the packet Grams.

# The first-collision obstruction

TPC-226 identifies the first stable primitive collision at $$Q=25,\qquad h=400,\qquad (p,r)=(37,47),$$ with multipliers $3$ and $-7$. Restrict the synthesis map to one shared output coordinate and to the two colliding source atoms. The aligned map and the row-odd map are respectively $$T=\frac1{400}(1,1),\qquad S=\frac1{400}(1,-1).$$ Their Gram matrices are $$T^*T=\frac1{160000}\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
 S^*S=\frac1{160000}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
 \label{eq:witness-grams}$$ Thus $$S^*S-T^*T=\frac1{160000}\begin{pmatrix}0&-2\\-2&0\end{pmatrix}.
 \label{eq:witness-difference}$$ The exact off-diagonal difference is $-1/80000$. This is precisely the local sign reversal seen in the AP collision correction. By Theorem [\[thm:gram\]](sections/3_gram_criterion.tex#L6){reference-type="ref" reference="thm:gram"}, the odd row map cannot replace the aligned physical target for every source pair.

This conclusion is scoped. It does not invalidate the finite odd-profile theorem: [\[eq:witness-difference\]](sections/4_collision_witness.tex#L22){reference-type="eqref" reference="eq:witness-difference"} explains it. Nor does it say that the physical source correlation is positive. It says only that its sign must be derived with the packet phase on the source sequence and the Poisson profile kept common.

> **Corollary** An arbitrary choice of packet profiles in the structural row lift cannot be promoted to the source-native four-packet compiler from boundedness and common support alone. Exact target-Gram equality is necessary.

# Exact certification

The executable certificate uses rational matrices and four-point Fourier moments. It contains six fixtures summarized in Table [1](sections/5_certification.tex#L23){reference-type="ref" reference="tab:fixtures"}. The first two are positive controls. The remaining four independently expose target mismatch, conjugate cross contamination, or a nonzero first Fourier moment.

<div id="tab:fixtures">

| Fixture                    | Criterion                      | Verdict |
|:---------------------------|:-------------------------------|:--------|
| Common physical transform  | all four Grams equal target    | pass    |
| Global packet signs        | signs cancel in each Gram      | pass    |
| Row-dependent odd sign     | collision off diagonal flips   | fail    |
| Alternating scales         | nonzero zeroth/second residual | fail    |
| Four unequal scales        | nonzero first moment           | fail    |
| Mixed aligned/odd profiles | packet Gram mismatch           | fail    |

: Exact-rational compatibility fixtures.

</div>

The producer rebuilds the committed JSON certificate. A separate checker rederives the two $2\times2$ Gram matrices and audits the six verdicts without importing the producer module. Normal and optimized Python modes emit byte-identical output. An adversarial script rejects mutations of the schema, theorem criterion, positive and negative controls, and witness check. These tests certify the finite algebra and claim boundary; they are not numerical evidence for an asymptotic prime estimate.

# Conclusion

The four-phase source identity has two distinct axes: packet phase belongs to the input sequence, while the Poisson profile belongs to one common transform. Theorem [\[thm:gram\]](sections/3_gram_criterion.tex#L6){reference-type="ref" reference="thm:gram"} gives the exact boundary for any packet-dependent replacement. The first primitive collision supplies a minimal witness showing that a row sign changes the target Gram rather than realizing a source packet phase.

The next useful step is therefore not another free profile search. It is a source-native collision compiler that carries $\beta+\mathrm i^jw$ through the common-profile prime/AP representation and exposes the actual signed $3$–$7$ correlation. Until that theorem is proved, arithmetic cancellation, Route-B level 2, and the strict $1/400$ budget remain open.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc59,
  author = {Liang Wang},
  title = {Polarized Local BDH Scalar Compiler},
  year = {2026},
  note = {V59 repository proof record}
}

@misc{tpc218,
  author = {Liang Wang},
  title = {Prime-Shell Packet Lift},
  year = {2026},
  note = {TPC-218 repository proof record}
}

@misc{tpc226,
  author = {Liang Wang},
  title = {First Primitive-Collision Transition in Dilated Shared Clocks},
  year = {2026},
  note = {TPC-226 repository proof record}
}
```

<!-- SOURCE_BODY_END -->
