# **Collision-Compressed Prime-Shell Reassembly on Finite Windows**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 24, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We prove a collision-compressed finite-window envelope for the exact TPC-218 common-source packet kernel. The previous scalar recovery collapsed the prime-shell label by a factor $P=\#\mathcal Q_x$. We instead combine the prime rows inside each primitive physical frequency bucket before applying the reduced-frequency additive large sieve. The TPC-236 incidence theorem gives the uniform bucket factor $$R_{\!*}=\frac{4Q^2}{H}+\frac{4UQ}{H},$$ while the direct coefficient energy is $O(JM^2(Q^2/H)(\log x)^5)$. On $I_x=(x/2,x]\cap\mathbb Z$ this yields $$\frac1{|I_x|}\sum_{n\in I_x}\sum_{j=1}^J|K_j(n)|^2
 \ll JM^2\bigl(x^{1/48}+x^{1/50}\bigr)(\log x)^5.$$ The leading unnormalized exponent is $49/48+o(1)$, and $U^2/|I_x|=x^{-67/200+o(1)}$ makes the finite-window correction lower order. An exact V59-shaped, source-active fixture at $h=82$ independently reproduces the collision and window composition. The theorem controls an unsigned packet trace. It proves neither signed divisor cancellation nor the signed four-packet Gate-B scalar, and it makes no sharpness claim.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1`. The certified object is the common-source, collision-compressed finite-window packet trace.

# Introduction

The common-source finite-window kernel retains two outer labels that should not be discarded casually: the prime-shell row $q$ and the packet profile $j$. TPC-218 kept both labels through a Hilbert-valued large-sieve estimate, but recovering the scalar prime-shell sum by pointwise Cauchy cost $P=\#\mathcal Q_x$ and returned the normalized power $x^{11/32}$ `\citep{WangTPC218}`. The resulting bound was source-valid but ignored the fact that only a small number of physical prime rows can meet one residue coordinate.

TPC-236 supplied the missing local geometry. At a fixed denominator $h$, a residue $a$ belongs to at most $$\frac{4Q^2}{H}+\frac{4hQ}{(a,h)H}$$ prime rows `\citep{WangTPC236}`. The finite-window kernel already uses reduced primitive frequencies. Thus $(a,h)=1$, and the collision theorem can be inserted exactly at the scalar-recovery step. This insertion is made before, rather than after, the additive large sieve.

The changed order replaces the coarse factor $P$ by $R_{\!*}=4Q^2/H+4UQ/H$. Combining this factor with the inherited direct coefficient energy produces powers $x^{1/48}$ and $x^{1/50}$, a substantial structural reduction from $x^{11/32}$. The same primitive coordinates remain separated by $U^{-2}$, so the finite-window attachment of TPC-217 applies without changing the physical object `\citep{WangTPC217}`.

The paper establishes three precise points:

1.  a collision Bessel inequality for the literal $q$ sum on primitive coordinates;

2.  its composition with the reduced-frequency large sieve and the explicit $C_h$ coefficient energy;

3.  an exact exponent ledger and an independently checked source-active finite fixture.

Every step is unsigned. In particular, the theorem does not convert the packet trace into the signed four-packet Gate-B scalar and does not exploit signs of $C_h$.

# Frozen common-source object

Set $$H=x^{21/32},\qquad Q=x^{1/3},\qquad
 U=x^{133/400},                                      \label{eq:scales}$$ and define $$\begin{aligned}
 \mathcal Q_x&=\{q\text{ prime}:Q<q\le2Q\},\\
 \mathcal D_x&=\{d:H/(4Q)<d\le U,\ \mu(d)^2=1\},\\
 C_h&=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}
       \frac{\mu(d)\log d}{d}.                       \label{eq:Ch}\end{aligned}$$ Let $J$ be fixed. For bounded profiles $\psi_j$, write $M=\max_j\|\psi_j\|_\infty$ and $$B_{h,q}^{(j)}(a)=
 \sum_{0<|m|\le\lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod h}.                    \label{eq:row}$$ The object studied here is $$K_j(n)=
 \sum_{h\le U}\ \sum_{\substack{a\bmod h\\(a,h)=1}}
 C_h\left(\sum_{q\in\mathcal Q_x}B_{h,q}^{(j)}(a)\right)
 \mathrm e^{2\pi i n a/h}.                                 \label{eq:kernel}$$

Equation [\[eq:kernel\]](sections/2_source.tex#L28){reference-type="eqref" reference="eq:kernel"} freezes all interfaces used below. The outer $q$ weight is one, $C_h$ is the literal signed divisor coefficient, and no row-dependent normalization or packet-dependent transform is inserted. The pairs $(h,a)$ are primitive at the point where they enter the large sieve. Passing all residues to that step would duplicate rational frequencies and is therefore forbidden.

For sufficiently large $x$, $U<Q$ and $4Q<H$. Hence every shell prime is invertible modulo every $h\le U$. The frequency $0/1$ contributes no atom because $\lfloor q/H\rfloor=0$ for $q\le2Q$.

# Prime-shell collision compression

Let $R_h(a)$ count the shell rows for which $B_{h,q}^{(j)}(a)$ can be nonzero. TPC-236 proves its gcd-fiber bound uniformly in the row amplitudes. Restricting that incidence matrix to primitive coordinates gives the following consequence.

> **Lemma: Primitive collision factor**<span id="lem:collision" label="lem:collision">\[lem:collision\]</span> For every frequency in [\[eq:kernel\]](sections/2_source.tex#L28){reference-type="eqref" reference="eq:kernel"}, $$R_h(a)\le \frac{4Q^2}{H}+\frac{4hQ}{H}
>           \le \frac{4Q^2}{H}+\frac{4UQ}{H}=:R_{\!*}.  \label{eq:Rstar}$$ Consequently, $$\sum_{h,a,j}|C_h|^2
>  \left|\sum_{q\in\mathcal Q_x}B_{h,q}^{(j)}(a)\right|^2
>  \le R_{\!*}
>  \sum_{h,a,j,q}|C_hB_{h,q}^{(j)}(a)|^2.              \label{eq:collision-bessel}$$ All $a$-sums in this paper are over $(a,h)=1$.

> **Proof** The physical multiplicity theorem has second term $4hQ/(gH)$ with $g=(a,h)$. Here $g=1$, which proves [\[eq:Rstar\]](sections/3_collision_compression.tex#L12){reference-type="eqref" reference="eq:Rstar"}. At one fixed $(h,a,j)$, at most $R_h(a)$ values of $q$ contribute. Cauchy–Schwarz therefore bounds the squared $q$ sum by $R_h(a)$ times the sum of the individual squares. Multiplication by $|C_h|^2$ and summation prove [\[eq:collision-bessel\]](sections/3_collision_compression.tex#L19){reference-type="eqref" reference="eq:collision-bessel"}.

The right side of [\[eq:collision-bessel\]](sections/3_collision_compression.tex#L19){reference-type="eqref" reference="eq:collision-bessel"} is already controlled by the source.

> **Lemma: Direct coefficient energy**<span id="lem:direct" label="lem:direct">\[lem:direct\]</span> Under the scales [\[eq:scales\]](sections/2_source.tex#L6){reference-type="eqref" reference="eq:scales"}, $$\sum_{h,a,j,q}|C_hB_{h,q}^{(j)}(a)|^2
>  \ll JM^2\frac{Q^2}{H}(\log x)^5.                    \label{eq:direct-energy}$$

> **Proof** The condition $4Q<H$ makes $m\mapsto mq^{-1}\pmod h$ injective on the range in [\[eq:row\]](sections/2_source.tex#L21){reference-type="eqref" reference="eq:row"}. Thus $$\sum_{(a,h)=1}|B_{h,q}^{(j)}(a)|^2
>  \le 2M^2\frac{hq}{H}.$$ If this row is active, then $h\ge H/(2Q)$. Writing $d=hk$ in [\[eq:Ch\]](sections/2_source.tex#L13){reference-type="eqref" reference="eq:Ch"} and discarding the lower band and squarefree restrictions gives $$|C_h|\le\frac{\log U}{h}\sum_{k\le U/h}\frac1k
>  \ll\frac{(\log x)^2}{h}.$$ It follows that $$\sum_{h\text{ active}}h|C_h|^2
>  \ll(\log x)^4\sum_{H/(2Q)\le h\le U}\frac1h
>  \ll(\log x)^5.$$ Finally $q\le2Q$ and $\#\mathcal Q_x\le2Q$. Summing the row estimate over $j,q,h$ proves [\[eq:direct-energy\]](sections/3_collision_compression.tex#L38){reference-type="eqref" reference="eq:direct-energy"}.

# Finite-window theorem

The remaining analytic input is the additive large sieve in its standard separated- frequency form `\citep{MontgomeryVaughan1973}`. If the frequencies are separated modulo one by $\delta$, then on any consecutive interval $I$ of $N$ integers, $$\sum_{n\in I}\left|\sum_\ell z_\ell\mathrm e^{2\pi i n\alpha_\ell}\right|^2
 \le (N-1+\delta^{-1})\sum_\ell|z_\ell|^2.           \label{eq:large-sieve}$$

> **Lemma: Primitive spacing**<span id="lem:spacing" label="lem:spacing">\[lem:spacing\]</span> Distinct primitive fractions $a/h$ and $a'/h'$ with $h,h'\le U$ have circular distance at least $U^{-2}$.

> **Proof** Their difference, or its complement modulo one, is a nonzero rational whose denominator divides $hh'$. Its numerator is a nonzero integer, so the distance is at least $(hh')^{-1}\ge U^{-2}$.

> **Theorem: Collision-compressed finite-window reassembly** <span id="thm:finite-window" label="thm:finite-window">\[thm:finite-window\]</span> For every consecutive interval $I$ of $N$ integers, $$\begin{aligned}
>  \sum_{n\in I}\sum_{j=1}^J|K_j(n)|^2
>  &\le (N-1+U^2)R_{\!*}
>  \sum_{h,a,j,q}|C_hB_{h,q}^{(j)}(a)|^2,              \label{eq:exact-chain}\\
>  &\ll (N+U^2)JM^2R_{\!*}\frac{Q^2}{H}(\log x)^5.
>                                                                     \label{eq:source-chain}\end{aligned}$$

> **Proof** Apply [\[eq:large-sieve\]](sections/4_finite_window.tex#L8){reference-type="eqref" reference="eq:large-sieve"} for each packet $j$ to the coefficients $$z_{h,a}^{(j)}=C_h\sum_{q\in\mathcal Q_x}B_{h,q}^{(j)}(a).$$ Lemma [\[lem:spacing\]](sections/4_finite_window.tex#L11){reference-type="ref" reference="lem:spacing"} permits $\delta^{-1}\le U^2$. Summing in $j$ and applying Lemma [\[lem:collision\]](sections/3_collision_compression.tex#L8){reference-type="ref" reference="lem:collision"} proves [\[eq:exact-chain\]](sections/4_finite_window.tex#L28){reference-type="eqref" reference="eq:exact-chain"}. Lemma [\[lem:direct\]](sections/3_collision_compression.tex#L34){reference-type="ref" reference="lem:direct"} then gives [\[eq:source-chain\]](sections/4_finite_window.tex#L30){reference-type="eqref" reference="eq:source-chain"}.

The order of the proof is load-bearing. Collapsing $q$ by the unconditional bound $|\sum_qz_q|^2\le P\sum_q|z_q|^2$ would restore the TPC-218 exponent. Here physical occupancy replaces $P$ before the finite-window Gram is diagonalized.

# V59 exponent ledger and method boundary

Take $I=I_x=(x/2,x]\cap\mathbb Z$ and $N=|I_x|$. The exact exponent identities are $$\begin{aligned}
 \frac{Q^2}{H}&=x^{1/96}, &
 \frac{UQ}{H}&=x^{23/2400},\label{eq:factor-exponents}\\
 \left(\frac{Q^2}{H}\right)^2&=x^{1/48}, &
 \frac{UQ}{H}\frac{Q^2}{H}&=x^{1/50},\label{eq:product-exponents}\\
 \frac{U^2}{N}&=x^{-67/200+o(1)}.                     \label{eq:window-exponent}\end{aligned}$$ Dividing [\[eq:source-chain\]](sections/4_finite_window.tex#L30){reference-type="eqref" reference="eq:source-chain"} by $N$ therefore yields $$\frac1N\sum_{n\in I_x}\sum_j|K_j(n)|^2
 \ll JM^2\bigl(x^{1/48}+x^{1/50}\bigr)(\log x)^5
 \ll JM^2x^{1/48}(\log x)^5.                         \label{eq:main-result}$$ The leading unnormalized exponent is $1+1/48=49/48$.

| Interface                                                                                                             | Normalized power | Information retained         |
|:----------------------------------------------------------------------------------------------------------------------|:-----------------|:-----------------------------|
| TPC-218 split packet array                                                                                            | $1/96$           | separate $q,j$ labels        |
| TPC-218 scalar recovery                                                                                               | $11/32$          | unsigned scalar trace        |
| Theorem [\[thm:finite-window\]](sections/4_finite_window.tex#L23){reference-type="ref" reference="thm:finite-window"} | $1/48$ (main)    | primitive physical occupancy |

The comparison records a structural upper bound, not a sharp asymptotic. The proof sequentially composes a collision Bessel inequality, an absolute $C_h$ harmonic majorant, and the additive large sieve. Valid upper bounds need not be simultaneously saturated by one physical source. Conversely, no step uses the signs in $C_h$.

The terminal firewall is therefore strict: $$\text{unsigned packet trace}
 \ne \text{signed four-packet Gate-B scalar}.$$ No arithmetic $L^2$, fixed-atom credit, strict $1/400$ payment, full Gate B, or twin-prime conclusion follows from [\[eq:main-result\]](sections/5_exponent_ledger.tex#L15){reference-type="eqref" reference="eq:main-result"}.

# Independent finite reproduction

The certificate uses $$(Q,H,U,h)=(101,8830,99,82).$$ Exact integer-power comparisons give $$8830^{32}\le101^{63}<8831^{32},\qquad
 99^{400}\le101^{399}<100^{400}.$$ Thus the fixture reproduces the V59 floor exponents. Unlike the earlier $h=80$ collision adversary, $h=82=2\cdot41$ is squarefree and source-active. In the band $H/(4Q)<d\le U$, its rational marked-divisor reproduction has the single term $$C_{82}^{\mathrm{rat}}=\frac{\mu(82)}{82}=\frac1{82}.$$ The replacement of $\log d$ by $1$ makes the finite ledger rational; it is not used in the asymptotic theorem.

For $q=109,137,191$, every row has primitive support $\{3,79\}$. With the constant packet and the signed-multiplier packet, the direct energy and collapsed trace are $$E_{\mathrm{dir}}=\frac3{1681},\qquad
 E_{\mathrm{col}}=\frac5{1681},\qquad
 \frac{E_{\mathrm{col}}}{E_{\mathrm{dir}}}=\frac53.$$ The constant packet alone has collision ratio three. On the complete $82$-point window, orthogonality of $3/82$ and $79/82$ gives exact trace energy $10/41$, hence normalized energy $5/1681$.

The producer and a separately implemented checker reconstruct the floor relations, Möbius band, modular rows, primitive frequencies, energies, collision factor, and large-sieve composition. A third program tests 21 shifted intervals, including lengths $82$ and $164$. Normal and optimized Python runs have identical output. The certificate record digest is

`41acb31d49f21e305e97941038b96ef0f6c938474e1e02cb0085f9ae01044848`.

Finite agreement certifies the implementation and displayed algebra only.

# Conclusion

Physical collision compression can be performed before reduced-frequency finite-window attachment on the exact TPC-218 common-source kernel. Primitive coordinates turn the TPC-236 gcd-fiber estimate into the factor $4Q^2/H+4UQ/H$. After the direct coefficient-energy bound and additive large sieve, the normalized packet-trace exponent becomes $1/48$, with a secondary $1/50$ term and a lower-order window correction.

The strongest remaining obstruction is now narrower. Estimate [\[eq:collision-bessel\]](sections/3_collision_compression.tex#L19){reference-type="eqref" reference="eq:collision-bessel"} uses only a uniform occupancy maximum, while Lemma [\[lem:direct\]](sections/3_collision_compression.tex#L34){reference-type="ref" reference="lem:direct"} discards all signs through $|C_h|^2$. The next admissible theorem should test the literal weighted collision energy $$\sum_{h,j}\sum_{(a,h)=1}|C_h|^2
 \left|\sum_qB_{h,q}^{(j)}(a)\right|^2$$ against the product of $R_{\!*}$ and the direct energy. A strict saving would identify new source structure; a matching source-valid fixture would establish an obstruction. Signed cross-denominator cancellation should be attempted only after this test.

# Reproducibility and declarations

#### Data and code availability.

All mathematical source files, exact certificate data, and deterministic checking programs are included in the TPC-237 project directory. No external dataset is used.

#### Author contributions.

Liang Wang: conceptualization, methodology, formal analysis, software, validation, and writing.

#### Ethics.

This theoretical and computational study involves no human participants, animals, or sensitive personal data.

#### Competing interests and funding.

The author declares no competing interests. No external funding supported this work.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@article{MontgomeryVaughan1973,
  author       = {H. L. Montgomery and R. C. Vaughan},
  title        = {The Large Sieve},
  journal      = {Mathematika},
  volume       = {20},
  number       = {2},
  pages        = {119--134},
  year         = {1973},
  doi          = {10.1112/S0025579300004708}
}

@misc{WangTPC217,
  author       = {Liang Wang},
  title        = {Finite-Window Attachment by Reduced Rational-Frequency Large Sieve},
  year         = {2026},
  note         = {TPC-217 project, prime\_dynamics\_theory repository}
}

@misc{WangTPC218,
  author       = {Liang Wang},
  title        = {Prime-Shell Hilbert Lift and the Sharp Collapse Barrier},
  year         = {2026},
  note         = {TPC-218 project, prime\_dynamics\_theory repository}
}

@misc{WangTPC236,
  author       = {Liang Wang},
  title        = {A Multi-Wrap Collision Envelope for Physical V59 Denominator Fibers},
  year         = {2026},
  note         = {TPC-236 project, prime\_dynamics\_theory repository}
}
```

<!-- SOURCE_BODY_END -->
