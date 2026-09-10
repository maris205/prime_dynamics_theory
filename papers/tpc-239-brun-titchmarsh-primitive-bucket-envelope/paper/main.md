# **A Brun–Titchmarsh Primitive-Bucket Envelope\ for Finite-Window Prime-Shell Reassembly**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China; liang.wang@hust.edu.cn
- Source date: August 24, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

We prove a source-backed prime-density envelope for the primitive collision buckets in a finite-window prime-shell kernel. If $4Q<H$, $2\leq h\leq U<Q$, and $a$ is a unit modulo $h$, then the physical row multiplicity $R_h(a)$ is bounded by a sum of prime counts in reduced residue classes. The standard Brun–Titchmarsh inequality and the exact signed multiplier count give

$$R_h(a)
 \leq 16\frac{Q^2}{H}\frac{h}{\varphi(h)}
       \frac{1}{\log(2Q/h)}.$$

The modulus-one row is empty because $2Q<H$. At the frozen scales $H=x^{21/32}$, $Q=x^{1/3}$, and $U=x^{133/400}$, the scale gap $Q/U=x^{1/1200}$ yields

$$\max_{h\leq U,\,(a,h)=1}R_h(a)
 \ll x^{1/96}\frac{\log\log x}{\log x}.$$

Substituting this row envelope into the unchanged common-source composition, before the reduced-frequency large sieve, gives the normalized packet trace

$$\frac1N\sum_{n\in(x/2,x]\cap\mathbb Z}\sum_{j=1}^{J}|K_j(n)|^2
 \ll J M^2x^{1/48}(\log x)^4\log\log x.$$

This improves the preceding estimate by the factor $\log x/\log\log x$, but it leaves the fixed-power exponent $1/48$ unchanged. The result is an unsigned $L^1$-level prime-density advance; it does not prove signed cancellation, arithmetic $L^2$, Gate B, or a twin-prime statement.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

The prime-shell labels in the finite-window kernel collide before distinct rational frequencies can be separated by the large sieve. A previous collision argument controlled each primitive bucket by an integer row census, which retained the correct fixed-power scale but ignored that the row label is prime. The present note uses that omitted arithmetic fact at the same pre-large-sieve interface.

The key observation is exact. A physical atom in a primitive bucket satisfies $mq^{-1}\equiv a\pmod h$. Because $a$ and the shell prime $q$ are units modulo $h$, the multiplier $m$ is also a unit, and the prime lies in the reduced class $q\equiv a^{-1}m\pmod h$. This turns the physical bucket into a finite collection of reduced prime progressions without changing the packet profiles, the shell weights, or the signed source coefficient $C_h$.

Our contributions are the following.

1.  We prove the explicit primitive-bucket envelope $$R_h(a)\leq
     16\frac{Q^2}{H}\frac{h}{\varphi(h)\log(2Q/h)},$$ including the empty $h=1$ branch and the reduced-class check required by Brun–Titchmarsh.

2.  We specialize the envelope at the V59 scales and obtain $R_h(a)\ll x^{1/96}\log\log x/\log x$, uniformly over active primitive buckets.

3.  We insert the new row factor into the frozen common-source composition and prove

    $$\frac1N\sum_{n\in I_x}\sum_{j=1}^{J}|K_j(n)|^2
     \ll JM^2x^{1/48}(\log x)^4\log\log x.$$

4.  We give a deterministic finite certificate with an independent reconstruction and mutation tests. Its numerical rows illustrate the finite inequalities and are not used as evidence for the analytic theorem.

The gain is deliberately stated at its proper size. Table [1](sections/1_introduction.tex#L52){reference-type="ref" reference="tab:comparison"} shows that prime density removes one logarithm, up to a $\log\log x$ factor, but does not alter the fixed-power ledger.

<div id="tab:comparison">

| Quantity                      | Previous collision census    | This paper                             |
|:------------------------------|:-----------------------------|:---------------------------------------|
| Maximum primitive row         | $4Q^2/H+4UQ/H$               | $\ll (Q^2/H)\log\log x/\log x$         |
| Normalized trace              | $\ll JM^2x^{1/48}(\log x)^5$ | $\ll JM^2x^{1/48}(\log x)^4\log\log x$ |
| Fixed-power exponent          | $1/48$                       | $1/48$                                 |
| Leading unnormalized exponent | $49/48+o(1)$                 | $49/48+o(1)$                           |

: Loss comparison at the same frozen common-source interface. The TPC-239 advance is logarithmic only.

</div>

This limitation is structural to the argument used here. The proof counts prime rows without their signs or $C_h$-weighted interaction, and the direct coefficient estimate still uses $|C_h|^2$. Consequently, no signed four-packet projection, arithmetic $L^2$, strict $1/400$, Gate-B passage, or twin-prime conclusion follows. Section [2](sections/2_source_setup.tex#L2){reference-type="ref" reference="sec:source"} fixes the inherited interfaces, Section [3](sections/3_primitive_ap_compiler.tex#L2){reference-type="ref" reference="sec:compiler"} proves the AP compiler, Section [4](sections/4_v59_composition.tex#L2){reference-type="ref" reference="sec:composition"} performs the V59 substitution, and the remaining sections document the finite audit and route boundary.

# Frozen source and setup

## Scales and common-source kernel

We work with the frozen scales

$$H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400},
 \qquad 4Q<H,\qquad U<Q.
 \label{eq:scales}$$

Let

$$\mathcal Q_x=\{q\text{ prime}:Q<q\leq2Q\},
 \qquad
 \mathcal D_x=\{d:H/(4Q)<d\leq U,\ \mu(d)^2=1\},$$

and retain the literal source coefficient

$$C_h=\sum_{\substack{d\in\mathcal D_x\\h\mid d}}\frac{\mu(d)\log d}{d}.
 \label{eq:Ch}$$

For fixed packet profiles $\psi_j$, put $M=\max_j\lVert\psi_j\rVert_\infty$ and define

$$\begin{aligned}
 B_{h,q}^{(j)}(a)
 &=\sum_{0<|m|\leq\lfloor hq/H\rfloor}
   \psi_j\!\left(\frac{Hm}{hq}\right)
   \mathbf 1_{\{mq^{-1}\equiv a\ (\mathrm{mod}\ h)\}},
 \label{eq:B}\\
 K_j(n)
 &=\sum_{h\leq U}\ \sum_{\substack{a\ (\mathrm{mod}\ h)\\(a,h)=1}}
   C_h\left(\sum_{q\in\mathcal Q_x}B_{h,q}^{(j)}(a)\right)
   \mathrm e^{2\pi i n a/h}.
 \label{eq:K}\end{aligned}$$

These formulas are not renormalized in this paper. In particular, the $q$-weight is one, the packet profiles are unchanged, $C_h$ is not replaced by an absolute or averaged coefficient, and the frequency index remains primitive.

## Inherited physical and analytic interfaces

For a shell prime $q$, write

$$S_{h,q}=\{mq^{-1}\pmod h:0<|m|\leq\lfloor hq/H\rfloor\}.
 \label{eq:physical-support}$$

The row multiplicity is

$$R_h(a)=\#\{q\in\mathcal Q_x:a\in S_{h,q}\}.
 \label{eq:row-multiplicity}$$

The inherited internal injectivity statement says that the multiplier map in [\[eq:physical-support\]](sections/2_source_setup.tex#L56){reference-type="eqref" reference="eq:physical-support"} is injective. Indeed, if two allowed multipliers have the same image, then

$$|m-m'|\leq2\lfloor hq/H\rfloor\leq4hQ/H<h,$$

while $h\mid(m-m')$. Hence $m=m'$. This fact prevents hidden duplicates inside one physical $q$-row.

The arithmetic input is the standard Brun–Titchmarsh estimate in a reduced residue class,

$$\pi(2Q;h,b)\leq
 \frac{4Q}{\varphi(h)\log(2Q/h)},
 \qquad (b,h)=1,\qquad h<2Q,
 \label{eq:BT-standard}$$

where $\pi(y;h,b)$ counts primes $p\leq y$ with $p\equiv b\pmod h$; see, for example, `\citet{MontgomeryVaughan2007}`. The repository source lock locally verifies a prior interval Brun–Titchmarsh use and this bibliography metadata. It does not contain a page-level scan of the cited book, so no page pinpoint is claimed.

Finally, the inherited finite-window composition will be used only after the new row estimate is proved. Its direct coefficient-energy input is

$$\sum_{h,a,j,q}|C_hB_{h,q}^{(j)}(a)|^2
 \ll JM^2\frac{Q^2}{H}(\log x)^5.
 \label{eq:direct-energy}$$

All four ingredients—[\[eq:K\]](sections/2_source_setup.tex#L42){reference-type="eqref" reference="eq:K"}, physical injectivity, [\[eq:direct-energy\]](sections/2_source_setup.tex#L100){reference-type="eqref" reference="eq:direct-energy"}, and the reduced-frequency large sieve—remain unchanged.

# The primitive-residue to reduced-prime-AP compiler

For $h\geq2$, define

$$M_h=\left\lfloor\frac{2hQ}{H}\right\rfloor,
 \qquad
 \mathcal M_h^{\times}=\{m\in\mathbb Z:0<|m|\leq M_h,\ (m,h)=1\}.
 \label{eq:Mh}$$

We first dispose of the modulus-one branch, where a prime-progression bound is unnecessary.

> **Lemma: Empty modulus-one row** <span id="lem:h-one" label="lem:h-one">\[lem:h-one\]</span> If $2Q<H$, then $S_{1,q}$ is empty for every $q\in\mathcal Q_x$.

> **Proof** Every shell prime satisfies $q\leq2Q<H$, and therefore $\lfloor q/H\rfloor=0$. The defining multiplier range is empty.

> **Theorem: Brun–Titchmarsh primitive-bucket envelope** <span id="thm:bucket" label="thm:bucket">\[thm:bucket\]</span> Assume $4Q<H$ and $2\leq h\leq U<Q$. For every $a\pmod h$ with $(a,h)=1$,
>
> $$\begin{aligned}
>  R_h(a)
>  &\leq\sum_{m\in\mathcal M_h^{\times}}
>  \bigl\{\pi(2Q;h,a^{-1}m)-\pi(Q;h,a^{-1}m)\bigr\}
>  \label{eq:ap-census}\\
>  &\leq16\frac{Q^2}{H}\frac{h}{\varphi(h)}
>  \frac{1}{\log(2Q/h)}.
>  \label{eq:factor16}\end{aligned}$$

> **Proof** Suppose that a physical row $q\in\mathcal Q_x$ contains $a$. Then some multiplier $m$ obeys
>
> $$0<|m|\leq\lfloor hq/H\rfloor
>  \leq\lfloor2hQ/H\rfloor=M_h,
>  \qquad mq^{-1}\equiv a\pmod h.$$
>
> Since $q>Q>h$, the prime $q$ is invertible modulo $h$. Multiplication by $q$ gives $m\equiv aq\pmod h$, and hence
>
> $$(m,h)=(aq,h)=1.$$
>
> Thus $m\in\mathcal M_h^{\times}$. Multiplication by $a^{-1}$ instead gives
>
> $$q\equiv a^{-1}m\pmod h.
>  \label{eq:compiled-class}$$
>
> Every actual row is therefore represented by a pair counted on the right side of [\[eq:ap-census\]](sections/3_primitive_ap_compiler.tex#L35){reference-type="eqref" reference="eq:ap-census"}. Internal row injectivity shows that the physical row does not hide two copies of $a$ for the same $q$. We do not invoke disjointness among different multiplier rows: the displayed sum remains a pair census and is allowed, as an upper-bound device, to overcount across $m$. The support enlargement used in forming that census is the deletion of the $q$-dependent condition $|m|\leq\lfloor hq/H\rfloor$.
>
> Both $a$ and $m$ are units modulo $h$, so every class $a^{-1}m\pmod h$ in [\[eq:ap-census\]](sections/3_primitive_ap_compiler.tex#L35){reference-type="eqref" reference="eq:ap-census"} is reduced. We may therefore bound each shell difference by [\[eq:BT-standard\]](sections/2_source_setup.tex#L84){reference-type="eqref" reference="eq:BT-standard"}. The multiplier set satisfies
>
> $$\#\mathcal M_h^{\times}\leq2M_h\leq\frac{4hQ}{H}.
>  \label{eq:m-count}$$
>
> Combining [\[eq:BT-standard\]](sections/2_source_setup.tex#L84){reference-type="eqref" reference="eq:BT-standard"} and [\[eq:m-count\]](sections/3_primitive_ap_compiler.tex#L80){reference-type="eqref" reference="eq:m-count"} gives
>
> $$\frac{4hQ}{H}\cdot
>  \frac{4Q}{\varphi(h)\log(2Q/h)}
>  =16\frac{Q^2}{H}\frac{h}{\varphi(h)\log(2Q/h)},$$
>
> which proves [\[eq:factor16\]](sections/3_primitive_ap_compiler.tex#L38){reference-type="eqref" reference="eq:factor16"}. The two visible factors $4$ account for the constant $16$; no hidden weakening is used.

> **Remark: What the AP sum forgets** Theorem [\[thm:bucket\]](sections/3_primitive_ap_compiler.tex#L27){reference-type="ref" reference="thm:bucket"} remembers the shell interval, modulus, and primitive bucket, but forgets the physical cutoff after compiling the congruence. It also ignores packet values, the sign of $C_h$, and interaction among multiplier rows. The result is therefore a coefficient-blind prime census.

# V59 specialization and finite-window composition

## Uniform primitive-row density

> **Corollary: V59 row envelope** <span id="cor:v59-row" label="cor:v59-row">\[cor:v59-row\]</span> At the scales [\[eq:scales\]](sections/2_source_setup.tex#L11){reference-type="eqref" reference="eq:scales"},
>
> $$\max_{\substack{h\leq U,\ a\ (\mathrm{mod}\ h)\\(a,h)=1}}
>  R_h(a)
>  \ll x^{1/96}\frac{\log\log x}{\log x},
>  \label{eq:v59-row}$$
>
> where inactive rows contribute zero.

> **Proof** Lemma [\[lem:h-one\]](sections/3_primitive_ap_compiler.tex#L17){reference-type="ref" reference="lem:h-one"} handles $h=1$. For $2\leq h\leq U$, the exact scale gap is
>
> $$\frac QU=x^{1/3-133/400}=x^{1/1200}.
>  \label{eq:q-over-u}$$
>
> Consequently,
>
> $$\log(2Q/h)\geq\log(2Q/U)
>  =\log2+\frac{1}{1200}\log x\gg\log x.$$
>
> The standard maximal-order estimate $h/\varphi(h)\ll\log\log(3h)$ gives $h/\varphi(h)\ll\log\log x$ uniformly in this range. Since
>
> $$\frac{Q^2}{H}=x^{2/3-21/32}=x^{1/96},
>  \label{eq:q2h}$$
>
> Theorem [\[thm:bucket\]](sections/3_primitive_ap_compiler.tex#L27){reference-type="ref" reference="thm:bucket"} proves [\[eq:v59-row\]](sections/4_v59_composition.tex#L14){reference-type="eqref" reference="eq:v59-row"}.

## Substitution before the large sieve

Let $I_x=(x/2,x]\cap\mathbb Z$ and $N=\#I_x$. The frozen TPC-237 composition, written with a generic maximum primitive-row multiplicity $R_{\max}$, is

$$\sum_{n\in I_x}\sum_{j=1}^{J}|K_j(n)|^2
 \leq (N-1+U^2)R_{\max}\mathcal E,
 \qquad
 \mathcal E=\sum_{h,a,j,q}|C_hB_{h,q}^{(j)}(a)|^2.
 \label{eq:frozen-composition}$$

This inequality first compresses the $q$-rows at each primitive coordinate and only then applies the large sieve to distinct reduced fractions $a/h$. The order matters: passing unreduced frequencies to the large sieve would create duplicate points. No such change occurs here.

> **Theorem: Prime-density finite-window packet trace** <span id="thm:packet-trace" label="thm:packet-trace">\[thm:packet-trace\]</span> For the kernel [\[eq:K\]](sections/2_source_setup.tex#L42){reference-type="eqref" reference="eq:K"} and fixed $J$,
>
> $$\frac1N\sum_{n\in I_x}\sum_{j=1}^{J}|K_j(n)|^2
>  \ll JM^2x^{1/48}(\log x)^4\log\log x.
>  \label{eq:packet-trace}$$
>
> The leading unnormalized fixed-power exponent is $49/48+o(1)$.

> **Proof** Use Corollary [\[cor:v59-row\]](sections/4_v59_composition.tex#L7){reference-type="ref" reference="cor:v59-row"} for $R_{\max}$ in [\[eq:frozen-composition\]](sections/4_v59_composition.tex#L58){reference-type="eqref" reference="eq:frozen-composition"}, and use the unchanged direct-energy estimate [\[eq:direct-energy\]](sections/2_source_setup.tex#L100){reference-type="eqref" reference="eq:direct-energy"} for $\mathcal E$. Because $N\asymp x$,
>
> $$\frac{U^2}{N}
>  =x^{2(133/400)-1+o(1)}
>  =x^{-67/200+o(1)}.
>  \label{eq:window-correction}$$
>
> After division by $N$, the two principal factors are
>
> $$\left(x^{1/96}\frac{\log\log x}{\log x}\right)
>  \left(JM^2x^{1/96}(\log x)^5\right).$$
>
> Their product is the right side of [\[eq:packet-trace\]](sections/4_v59_composition.tex#L73){reference-type="eqref" reference="eq:packet-trace"}, since $1/96+1/96=1/48$. Removing the normalization multiplies by $N=x^{1+o(1)}$, so the leading fixed-power exponent becomes $1+1/48=49/48$.

## Loss ledger

The direct coefficient energy contributes $(\log x)^5$. The new row envelope contributes $\log\log x/\log x$. Hence the final logarithmic loss is $(\log x)^4\log\log x$. Relative to the preceding $(\log x)^5$ bound, the improvement factor is exactly

$$\frac{\log x}{\log\log x}.$$

The fixed-power exponent remains $1/48$. Theorem [\[thm:packet-trace\]](sections/4_v59_composition.tex#L67){reference-type="ref" reference="thm:packet-trace"} therefore gives genuine logarithmic progress, not a fixed-power saving, and does not establish sharpness of either fixed-power exponent.

# Deterministic finite certificate

The computational artifact tests whether the physical support, AP compiler, constant ledger, and status firewall have been encoded as stated. Its primary fixture is

$$(Q,H,h)=(101,8830,82),\qquad M_h=1.
 \label{eq:fixture}$$

The modulus is squarefree, $4Q<H$, and $h<Q$. The program enumerates all twenty primes in $(101,202]$, every $q$-dependent physical row, both unit multipliers $m=-1,1$, and all forty primitive residues modulo $82$. For each bucket it reconstructs the actual row count and the AP rows in [\[eq:ap-census\]](sections/3_primitive_ap_compiler.tex#L35){reference-type="eqref" reference="eq:ap-census"}.

<div id="tab:fixture">

| Quantity                      |              Value|
|:------------------------------|------------------:|
| Shell primes                  |               $20$|
| Primitive buckets             |               $40$|
| Maximum actual $R_h(a)$       |                $3$|
| Maximum AP census             |                $3$|
| Per-class Brun–Titchmarsh RHS |  $11.202947549259$|
| Factor-$16$ RHS               |  $42.030718732939$|
| Rejected producer mutations   |               $11$|

: Primary finite-fixture summary. The real upper bounds are numerical evaluations of the analytic formulas, not estimates inferred from the data.

</div>

The buckets $a=3$ and $a=79$ each contain the three documented physical rows associated with $q=109,137,191$. Other buckets demonstrate a strict gap between the physical count and the AP census because primes below the row-activation threshold survive after the cutoff is dropped. Every encoded bucket satisfies

$$\text{actual }R_h(a)
 \leq\text{AP pair census}
 \leq\text{factor-16 real RHS}.$$

The producer validates exact runtime types, emits sorted JSON, and attaches a SHA-256 digest to the canonical payload. It constructs every exponent with `Fraction`; in particular it checks

$$\frac13-\frac{133}{400}=\frac1{1200},\qquad
 \frac23-\frac{21}{32}=\frac1{96},\qquad
 \frac1{96}+\frac1{96}=\frac1{48}.$$

The independent checker imports no producer module. It uses a separate prime sieve, a multiplicative totient calculation, and the congruence $m\equiv aq\pmod h$ to rebuild the certificate. A stress checker repeats the direct-row, AP-census, classwise real Brun–Titchmarsh, and factor-$16$ comparisons for five parameter sets and 104 primitive buckets. It observes 26 buckets where dropping the physical cutoff makes the first inequality strict.

Eleven mutations test strict-type confusion, shell primality and endpoints, the $q$-dependent cutoff, the constant $16$, strict range hypotheses, primitivity, unit multipliers, and the direction $R_h(a)\leq\text{AP census}$. Both ordinary and optimized Python execution follow the same explicit checks; no validation relies on `assert`.

All statements in this section have the evidence class `NUMERICAL_FINITE_ILLUSTRATION_ONLY`. The general bucket theorem is proved in Section [3](sections/3_primitive_ap_compiler.tex#L2){reference-type="ref" reference="sec:compiler"} from the source-backed arithmetic input, not from this fixture.

# Route consequence and claim boundary

The strongest positive result is the finite-window common-source packet trace

$$JM^2x^{1/48}(\log x)^4\log\log x.$$

This result advances the route because a prime-density theorem has replaced an integer census at the exact primitive-bucket interface. Its status is

$$\texttt{TPC239\_ROUTE\_ADVANCE = YES\_LOGARITHMIC\_ONLY}.$$

The strongest obstruction is equally explicit: prime density saves only a logarithm and leaves the fixed-power cost $x^{1/48}$. In the program’s $L^2$/Gate-B meaning, the arithmetic status therefore remains

$$\texttt{TPC239\_ARITHMETIC\_ADVANCE = NO}.$$

The proof is coefficient-blind at the decisive step. It bounds each AP row by a nonnegative prime count, takes a maximum row multiplicity, and combines that maximum with a direct energy containing $|C_h|^2$. None of these operations detects cancellation among the signs of $C_h$, among multiplier rows, or in an actual signed four-packet projection. Sequential upper bounds also do not show that the exponent $1/48$ is attained, so we make no sharpness claim.

The open theorem is weighted or signed within-bucket cancellation beyond coefficient-blind prime counting. The reusable structure established here is the compiler

$$\boxed{\text{primitive residue}\ \longrightarrow\
        \text{reduced prime arithmetic progression}.}$$

That compiler can accept a stronger weighted prime theorem without changing the physical support algebra. A further uniform nonnegative bucket bound, however, would have to beat the present prime-density scale by a power to alter the fixed-power ledger.

The next-round clue is therefore narrow: test the exact top-band $C_h$ before seeking further uniform bucket savings. Such a test must retain the literal weights and phases. Until a source-backed weighted or signed theorem is available on that object, signed $C_h$ cancellation, arithmetic $L^2$, fixed-atom credit, strict $1/400$, full Gate B, and the twin-prime endpoint remain open or absent.

# Conclusion

Primitive physical buckets carry more arithmetic structure than an integer row census records. The congruence defining a bucket sends every admissible unit multiplier to a reduced prime residue class, and Brun–Titchmarsh then gives the explicit factor-$16$ row envelope. At V59 this changes the primitive collision factor from a power-scale census to $x^{1/96}\log\log x/\log x$.

Inserted at the unchanged pre-large-sieve interface, the envelope proves the finite-window trace bound

$$\frac1N\sum_{n\in I_x}\sum_j|K_j(n)|^2
 \ll JM^2x^{1/48}(\log x)^4\log\log x.$$

The improvement over the preceding result is the genuine logarithmic factor $\log x/\log\log x$. The fixed-power exponent and leading unnormalized exponent remain $1/48$ and $49/48+o(1)$, respectively. Further progress requires information that a coefficient-blind prime count cannot see: weighted or signed cancellation inside the literal top-band buckets.

# Status ledger and declarations

## Machine-readable status vocabulary

`TPC239_STATUS`

:   `PROVED_SOURCE_BACKED_PRIME_DENSITY_L1`

`TPC239_ROUTE_ADVANCE`

:   `YES_LOGARITHMIC_ONLY`

`TPC239_ARITHMETIC_INPUT`

:   `BRUN_TITCHMARSH`

`TPC239_ARITHMETIC_ADVANCE`

:   `NO`

`C_H_SIGNED_CANCELLATION`

:   `NONE`

`SIGNED_FOUR_PACKET_PROJECTION`

:   `NOT_PROVED`

`L2`

:   `NONE`

`FIXED_ATOM_CREDIT`

:   `0`

`STRICT_1_OVER_400`

:   `UNPAID_GLOBAL`

`FULL_GATE_B`

:   `OPEN`

`TWIN_PRIME_RESULT`

:   `NONE`

`SHARPNESS`

:   `NOT_CLAIMED`

## Research extraction

Strongest positive result

:   Finite-window common-source packet trace with $x^{1/48}(\log x)^4\log\log x$.

Strongest obstruction

:   Prime density saves only a logarithm and leaves fixed-power $1/48$.

Open theorem

:   Weighted or signed within-bucket cancellation beyond coefficient-blind prime counting.

Reusable structure

:   Primitive residue to reduced prime-AP compiler.

Round-2 clue

:   Test the exact top-band $C_h$ before seeking further uniform bucket savings.

## Reproducibility and competing interests

The paper directory contains the complete source, deterministic certificate producer, independent checker, stress checker, JSON result, and computational protocol. The finite computations are illustrations and regression tests, not proof evidence. The author declares no competing interests.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{MontgomeryVaughan2007,
  author = {Hugh L. Montgomery and Robert C. Vaughan},
  title = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  address = {Cambridge},
  year = {2007}
}
```

<!-- SOURCE_BODY_END -->
