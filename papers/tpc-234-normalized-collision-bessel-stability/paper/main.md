# Depth-Uniform Bessel Stability\ for Normalized Prime-Shell Collision Rows

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

We prove a depth-uniform conditioning theorem for normalized collision rows in a dilated prime-shell clock. At depth $L<Q/4$, exact one-wrap geometry implies that each residue coordinate belongs to at most two prime rows. After normalizing every nonzero row to unit norm, the synthesis operator $Tc=\sum_qc_qu_q$ satisfies $\|Tc\|^2\le2\sum_q|c_q|^2$. Equivalently, its Gram operator obeys $0\le T^*T\le2I$, while the off-diagonal Gram part has norm at most one. The bound is independent of depth, raw row mass, and profile amplitudes, and the constant two is sharp in the ambient multiplicity-two class. Stability is not saving: a literal $Q=39,L=7$ block has normalized symmetric and antisymmetric energy ratios $4/3$ and $2/3$. Independent exact support compilers agree on five scales. The theorem repairs raw mass conditioning but leaves source-valid normalization and arithmetic cancellation open.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Growing-depth resonance models face two different conditioning problems. The first is raw row imbalance: different cutoffs can carry very different numbers of primitive atoms. The second is collision accumulation after those rows are assembled in one coordinate space. Unit-row normalization removes the first problem by definition, but it could in principle amplify the second if collision degree grew with depth.

We show that this does not happen in the short-multiplier dilated clock. The decisive invariant is not graph degree but coordinate multiplicity. Exact one-wrap geometry ensures that no residue bucket contains three prime rows. Pointwise Cauchy–Schwarz then gives a Bessel bound of two for the entire normalized family. The terminology is standard in frame theory `\citep{christensen2016,casazzakutyniok2013}`, although the argument here is a direct one-line coordinate estimate.

The theorem separates two statements that are easy to conflate. Normalization makes the operator uniformly bounded as $L$ grows, but it does not force the assembled energy below its diagonal. A literal two-row block has ratio $4/3$ in its symmetric mode and $2/3$ in its antisymmetric mode. Thus the sign or phase of source coefficients remains essential.

Finally, normalization changes each row by its norm. We treat this as a modeling transform. Whether the physical arithmetic source admits the same rescaling is a separate crosswalk theorem, not a consequence of the Bessel estimate.

# The multiplicity-two Bessel theorem

Let $X$ be a finite coordinate set and $\mathcal H$ a Hilbert space. For each prime-row label $q$, let $v_q\in\ell^2(X;\mathcal H)$ be nonzero and supported on $S_q$. Put $$u_q=\frac{v_q}{\|v_q\|},
 \qquad Tc=\sum_qc_qu_q,
 \qquad G=T^*T.$$ No common profile or equal support size is assumed.

> **Theorem: Normalized collision stability**<span id="thm:bessel" label="thm:bessel">\[thm:bessel\]</span> Suppose every $x\in X$ lies in at most two supports $S_q$. Then $$\|Tc\|^2\le2\sum_q|c_q|^2, \tag{1}$$ and consequently $$0\le G\le2I,
>  \qquad \sigma(G)\subset[0,2],
>  \qquad \|G-I\|\le1. \tag{2}$$ The constant two is sharp under the stated hypothesis.

> **Proof** At a fixed coordinate, at most two Hilbert vectors occur, so $$\left\|\sum_{q:x\in S_q}c_qu_q(x)\right\|^2
>  \le2\sum_{q:x\in S_q}|c_q|^2\|u_q(x)\|^2.$$ Summing over $x$ and using $\|u_q\|=1$ proves (1). Positivity of $G$ is automatic and (1) gives $G\le2I$. Its diagonal is one, hence $K=G-I$ is self-adjoint with $-I\le K\le I$, proving (2).
>
> For sharpness, take two copies of the same singleton unit row. Coefficients $(1,1)$ give output energy four and diagonal coefficient energy two.

For scalar rows the estimate has an exact sum-of-squares residual. If the one or two contributions at $x$ are denoted $a_x,b_x$, with $b_x=0$ at singleton buckets, then $$2\sum_x(|a_x|^2+|b_x|^2)-\sum_x|a_x+b_x|^2
 =\sum_{|B_x|=1}|a_x|^2+\sum_{|B_x|=2}|a_x-b_x|^2. \tag{3}$$ This identity is useful for exact rational certification.

In the dilated prime-shell clock $h=4LQ$, $L<Q/4$, the one-wrap collision theorem supplies the multiplicity-two hypothesis. Theorem [\[thm:bessel\]](sections/2_bessel_theorem.tex#L12){reference-type="ref" reference="thm:bessel"} is therefore uniform in $Q,L$ and in all nonzero row amplitudes.

# A literal normalized block

The smallest convenient equal-mass witness occurs at $$Q=39,\qquad L=7,\qquad h=1092,
 \qquad (p,r)=(67,71).$$ Both rows have positive primitive multipliers $(1,5,11)$ and therefore six signed atoms. Their supports intersect exactly at $$\begin{array}{c|cc}
 \text{residue}&m_p&m_r\\ \hline
 277&-5&11\\
 815&5&-11
 \end{array}$$ because $5\cdot71+11\cdot67=1092$. Uniform unit rows have inner product $2/6=1/3$. Thus $$\frac{\|u_p+u_r\|^2}{\|u_p\|^2+\|u_r\|^2}=\frac43,
 \qquad
 \frac{\|u_p-u_r\|^2}{\|u_p\|^2+\|u_r\|^2}=\frac23. \tag{4}$$

Equation (4) gives both directions with the same geometry. Unit normalization removes the raw mass ratio, but symmetric coefficients amplify and antisymmetric coefficients save. Therefore the operator upper bound cannot be reinterpreted as a strict estimate $G\le(1-\delta)I$ for any positive $\delta$.

The ambient sharpness example in Theorem [\[thm:bessel\]](sections/2_bessel_theorem.tex#L12){reference-type="ref" reference="thm:bessel"} is intentionally not claimed to be a literal prime clock. The Q39 block is the source-model witness needed for the scoped no-saving statement; it establishes ratio above one without claiming that the global constant two is attained arithmetically.

# Finite reproduction and claim boundary

Two independent support compilers evaluate the scales $$(Q,L)=(25,4),(39,7),(101,16),(211,32),(401,64).$$ They agree on every prime-row count, atom count, singleton bucket, and double bucket. The corresponding numbers of double buckets are $2,2,10,20,78$, and every maximum bucket multiplicity is two. The Q39 supports and both exact ratios in (4) are rebuilt independently.

The certificate also evaluates (3) over four rational buckets and verifies equality of the direct residual and its pointwise sum-of-squares decomposition. An abstract doubleton reaches ratio two, while a tripleton reaches ratio three and is rejected as outside the proved geometry. The combined record digest is

`d6c3c62ea5698c5941c14fab872b8951dd1939e6f45484651a13e7ccc473bed9`.

All computations are exact finite reproduction, not evidence for arithmetic cancellation. More importantly, replacing $v_q$ by $v_q/\|v_q\|$ changes the actual row coefficients. The next theorem must trace the physical V59 source into this row space and determine whether normalization is licensed, paid by explicit weights, or incompatible with the source.

# Conclusion

Multiplicity two turns unit-row normalization into a complete depth-uniform conditioning repair: the normalized Gram spectrum always lies in $[0,2]$, regardless of growing resonance depth or raw row imbalance. The repair is structural and exact.

It is not an arithmetic saving. The literal Q39 block realizes both amplification and reduction, so source signs and phases remain decisive. Nor is row normalization yet a source-valid operation. No actual V59 crosswalk, arithmetic cancellation, $L^2$ estimate, fixed-atom credit, strict $1/400$ payment, full Gate B, or twin-prime theorem is claimed.

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

@book{casazzakutyniok2013,
  editor    = {Peter G. Casazza and Gitta Kutyniok},
  title     = {Finite Frames: Theory and Applications},
  publisher = {Birkh{\"a}user},
  year      = {2013}
}
```

<!-- SOURCE_BODY_END -->
