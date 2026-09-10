# A Multi-Wrap Collision Envelope\ for Physical V59 Denominator Fibers

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

We prove an unnormalized collision envelope for the physical denominator rows in the V59 Gate-B source. For $4Q<H$, $h\le Q$, and a fixed residue $a\pmod h$, let $g=(a,h)$ and $M_h=\lfloor2hQ/H\rfloor$. The number of prime-shell rows meeting that residue is at most $$2\lfloor M_h/g\rfloor\lceil Qg/h\rceil
 \le \frac{4Q^2}{H}+\frac{4hQ}{gH}
 \le \frac{8Q^2}{H}.$$ Pointwise Cauchy–Schwarz converts this count into a fixed-$h$ Bessel inequality without row-dependent normalization and then into an explicit-$C_h$ orthogonal direct-sum bound. At the V59 scales the sharper uniform loss is $4x^{1/96}+4x^{23/2400}=(4+o(1))x^{1/96}$. This exponent cannot be removed by transferring the preceding multiplicity-two theorem: an exact V59-shaped floor fixture with $(Q,H,U,h)=(101,8830,99,80)$ has three identical prime rows and Bessel ratio three. The result supplies a source-valid single-fiber compiler while leaving cross-denominator rational-frequency reassembly and divisor-weight cancellation open.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The physical-depth crosswalk identifies the V59 residue row at denominator $h$ as $$B_{h,q}(a)=
 \sum_{0<|m|\le\lfloor hq/H\rfloor}
 \psi\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod h},                 \label{eq:physical-row}$$ where $Q<q\le2Q$ is prime. The full source retains the divisor coefficient $$C_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}
 \frac{\mu(d)\log d}{d}.$$ The correct next question is therefore not how to normalize a surrogate clock, but how many physical prime rows can occupy one residue coordinate.

The modeled one-wrap clock had coordinate multiplicity at most two. Physical rows have a different modulus–depth relation, and products of multipliers with shell primes may wind around the modulus many times. We quantify this effect directly. The key reduction is arithmetic but elementary: fixing a residue also fixes the gcd of every admissible multiplier with $h$, and after division by this gcd each multiplier places $q$ in one class modulo a reduced modulus.

The resulting multiplicity bound gives a Bessel estimate in the usual frame-theoretic sense `\citep{christensen2016}`, but no unit-row transform is used. All amplitudes, explicit $C_h$ weights, and a common linear packet transform can therefore remain in the ledger. The cost is a factor of order $Q^2/H=x^{1/96}$ at V59. A three-row exact fixture proves that the previous constant two is genuinely unavailable on the physical interface.

The direct sum below is pre-reassembly. Frequencies belonging to different denominators are not declared orthogonal on the physical finite window, and no cancellation in $C_h$ is claimed.

# The gcd-fiber collision theorem

For fixed $h$ and $q$, let $S_{h,q}$ be the residue support in [\[eq:physical-row\]](sections/1_introduction.tex#L8){reference-type="eqref" reference="eq:physical-row"}. We first verify that atoms within one physical row remain distinct.

> **Lemma: Internal injectivity**<span id="lem:injectivity" label="lem:injectivity">\[lem:injectivity\]</span> Suppose $4Q<H$, $h\le Q$, and $Q<q\le2Q$. Then $m\mapsto mq^{-1}\pmod h$ is injective for $0<|m|\le\lfloor hq/H\rfloor$.

> **Proof** If two multipliers have the same residue, then $h\mid m-m'$. On the other hand, $$|m-m'|\le2\lfloor hq/H\rfloor\le4hQ/H<h.$$ Thus $m=m'$.

Let $$R_h(a)=\#\{q:Q<q\le2Q\text{ prime},\ a\in S_{h,q}\}$$ and $M_h=\lfloor2hQ/H\rfloor$.

> **Theorem: Gcd-fiber multiplicity envelope**<span id="thm:gcd-envelope" label="thm:gcd-envelope">\[thm:gcd-envelope\]</span> For $a\pmod h$, put $g=(a,h)$. Under the hypotheses of Lemma [\[lem:injectivity\]](sections/2_gcd_fiber.tex#L7){reference-type="ref" reference="lem:injectivity"}, $$R_h(a)
>  \le2\left\lfloor\frac{M_h}{g}\right\rfloor
>        \left\lceil\frac{Qg}{h}\right\rceil
>  \le\frac{4Q^2}{H}+\frac{4hQ}{gH}
>  \le\frac{8Q^2}{H}.                                  \label{eq:multiplicity}$$

> **Proof** Every shell prime exceeds $h$ and is therefore a unit modulo $h$. An atom in bucket $a$ satisfies $m\equiv aq\pmod h$, so $(m,h)=(a,h)=g$. The global signed multiplier range contains at most $2\lfloor M_h/g\rfloor$ multiples of $g$.
>
> If $a=0$, then $g=h$ and $M_h<h$; no nonzero admissible multiplier is divisible by $h$, so the result is immediate. Assume henceforth that $a\ne0$. For one such $m$, divide the congruence by $g$. Since $a/g$ is a unit modulo $h/g$, the prime $q$ lies in exactly one residue class modulo $h/g$. An interval of length $Q$ contains at most $\lceil Q/(h/g)\rceil$ integers in that class. Multiplying the two counts proves the first inequality.
>
> Use $M_h\le2hQ/H$ and $\lceil Qg/h\rceil\le Qg/h+1$ for the second. Finally $h\le Q\le gQ$ bounds the second summand by $4Q^2/H$.

The reduced modulus $h/g$ is essential. A finite counterexample to counting modulo $h$ instead is given in Section [4](sections/4_triple_collision.tex#L1){reference-type="ref" reference="sec:fixtures"}.

# An unnormalized weighted Bessel compiler

Let $\mathcal V$ be a Hilbert space and let $v_{h,q}\in\ell^2(\mathbb Z/h\mathbb Z;\mathcal V)$ be arbitrary rows supported on $S_{h,q}$. Their values may include the full profile in [\[eq:physical-row\]](sections/1_introduction.tex#L8){reference-type="eqref" reference="eq:physical-row"}; no equality of amplitudes or row norms is assumed.

> **Corollary: Physical fixed-fiber Bessel bound**<span id="cor:bessel" label="cor:bessel">\[cor:bessel\]</span> For arbitrary complex coefficients $c_q$, $$\left\|\sum_qc_qv_{h,q}\right\|^2
>  \le B_h\sum_q|c_q|^2\|v_{h,q}\|^2,
>  \qquad
>  B_h\le\frac{4Q^2}{H}+\frac{4hQ}{H}
>       \le\frac{8Q^2}{H}.                              \label{eq:bessel}$$

> **Proof** At a fixed residue $a$, at most $R_h(a)$ rows contribute. Cauchy–Schwarz at that coordinate and summation over $a$ give [\[eq:bessel\]](sections/3_bessel.tex#L15){reference-type="eqref" reference="eq:bessel"}, with $B_h=\max_aR_h(a)$. Theorem [\[thm:gcd-envelope\]](sections/2_gcd_fiber.tex#L27){reference-type="ref" reference="thm:gcd-envelope"} and $g\ge1$ give the displayed uniform bounds.

The estimate immediately preserves the physical divisor weights in the orthogonal pre-reassembly direct sum: $$\sum_h|C_h|^2\left\|\sum_qc_{h,q}v_{h,q}\right\|^2
 \le B_{\rm phys}
 \sum_{h,q}|C_h|^2|c_{h,q}|^2\|v_{h,q}\|^2,           \label{eq:weighted-direct-sum}$$ where $B_{\rm phys}=max_hB_h$. Nothing has been absorbed into a row-dependent normalization.

If one common bounded linear map $T_h$ is subsequently applied to every packet output at denominator $h$, the right side acquires only $\sup_h\|T_h\|^2$. Because the map is common and linear, the four-phase polarization identity remains valid. This is the precise repair of the normalization obstruction: conditioning is paid by an explicit multiplicity factor rather than by independently renormalizing packet outputs.

# Exact adversarial fixtures

Take $$Q=101,\qquad H=8830,\qquad U=99,\qquad h=80.$$ Exact integer comparisons certify $$8830^{32}\le101^{63}<8831^{32},\qquad
 99^{400}\le101^{399}<100^{400}.$$ Thus $H=\lfloor Q^{63/32}\rfloor$, $U=\lfloor Q^{399/400}\rfloor$, and $h\le U$: this is a literal finite floor model of the V59 exponent relations.

For the three shell primes $q=113,127,193$, the cutoff is one. Their inverses modulo $80$ are $17,63,17$, respectively, so every row has support $$S_{80,113}=S_{80,127}=S_{80,193}=\{17,63\}.$$ In particular, residue $63$ is represented by multipliers $-1,1,-1$. The physical bucket multiplicity is three.

For uniform amplitudes let the three rows be $v_{113},v_{127},v_{193}$. Each has squared norm two, whereas their equal-coefficient sum has squared norm eighteen. Hence $$\frac{\|v_{113}+v_{127}+v_{193}\|^2}
      {\|v_{113}\|^2+\|v_{127}\|^2+\|v_{193}\|^2}=3. \label{eq:ratio-three}$$ Equation [\[eq:ratio-three\]](sections/4_triple_collision.tex#L28){reference-type="eqref" reference="eq:ratio-three"} refutes both physical multiplicity two and a universal Bessel constant two in this class. It is a finite structural obstruction, not an asymptotic lower bound for arithmetic source mass.

A second fixture explains the gcd reduction. For $(Q,H,h,a)=(16,65,8,6)$, one has $g=2$ and five rows in bucket $a=6$. Counting each multiplier in a class modulo $h$ gives the false upper bound four. The correct reduced modulus $h/g=4$ gives upper bound eight and contains all five rows.

# The V59 exponent ledger and remaining bridge

At the physical scales $$H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400},$$ the two terms in Corollary [\[cor:bessel\]](sections/3_bessel.tex#L8){reference-type="ref" reference="cor:bessel"} satisfy $$\begin{aligned}
 \frac{4Q^2}{H}&=4x^{1/96},\label{eq:main-toll}\\
 \frac{4UQ}{H}&=4x^{23/2400}.\end{aligned}$$ Because $23/2400<1/96=25/2400$, the source-uniform factor is $$B_{\rm phys}\le4x^{1/96}+4x^{23/2400}
 =(4+o(1))x^{1/96}.                                   \label{eq:v59-toll}$$

The exponent in [\[eq:main-toll\]](sections/5_v59_ledger.tex#L9){reference-type="eqref" reference="eq:main-toll"} is the same conductor-gap exponent that appears with the opposite sign in the benchmark local cell saving. If the two factors enter the same energy ledger multiplicatively, the power margin is zero. This conditional ledger observation does not prove that every future reassembly must factor in that way, but it shows that the present multiplicity estimate alone cannot certify a positive global saving.

More importantly, [\[eq:weighted-direct-sum\]](sections/3_bessel.tex#L31){reference-type="eqref" reference="eq:weighted-direct-sum"} is not yet the physical finite-window norm. Distinct denominators can reduce to the same rational frequency, and their coefficients $C_h$ may cancel or reinforce. The next theorem must combine the physical-fiber envelope with reduced-frequency regrouping and a finite-window large sieve while keeping the signed $C_h$ sum and all packet labels. That cross-$h$ step is where an arithmetic gain beyond [\[eq:v59-toll\]](sections/5_v59_ledger.tex#L15){reference-type="eqref" reference="eq:v59-toll"} would have to enter.

# Finite reproduction

Two independent compilers exhaust physical buckets at $$(Q,H)=(11,45),(17,70),(25,104),(53,220),(101,8830).$$ Their maximum multiplicities are respectively $3,4,6,11,3$. A sixth independent scale $(211,37664)$ has maximum three. Every bucket satisfies both the exact gcd-fiber count and the uniform $8Q^2/H$ envelope. The compilers independently rebuild the Q101 supports, the energies $6$ and $18$, and ratio three.

Mutation controls reject a modulus-$h$ count in place of $h/g$, a multiplicity-two upgrade, deletion of $C_h$, an unproved cross-$h$ reassembly, and a positive benchmark margin. The exact finite-record digest is

`6ce0173091ebdc11d91a2bc57b27018c8d7c147a162d5962f5c2a6ef83f73a10`.

These computations certify formulas and finite fixtures. They are not numerical evidence for cancellation in the physical divisor weights.

# Conclusion

Physical V59 rows admit a source-valid, unnormalized collision bound. Gcd-fiber counting converts every residue bucket into multiplier choices followed by one reduced arithmetic progression, yielding a universal factor $8Q^2/H$ and the sharper V59 loss $(4+o(1))x^{1/96}$. Explicit $C_h$ weights and common linear packet transforms survive the fixed-fiber direct-sum compiler.

The exact Q101 triple collision proves that multiplicity two does not survive the physical crosswalk. The remaining task is therefore sharply located: regroup and control collisions across distinct denominators while exploiting, rather than discarding, the signed divisor coefficients. No arithmetic cancellation, $L^2$ estimate, fixed-atom credit, strict $1/400$ payment, full Gate B, or twin-prime theorem is claimed.

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
