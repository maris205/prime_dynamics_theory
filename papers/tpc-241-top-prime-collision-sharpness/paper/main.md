# A Top-Prime Collision Lower Bound at the $1/48$ Barrier

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

We study the unsigned common-profile kernel at the finite-window interface of a twin-prime analytic program. At the frozen scales $H=x^{21/32}$, $Q=x^{1/3}$, and $U=x^{133/400}$, the preceding upper-bound route produced the normalized power $x^{1/48+o(1)}$ after shell-prime rows were collapsed at primitive rational frequencies. We prove that this power cannot be improved by any fixed amount on the same unsigned object. For every fixed nonnegative normalized smooth profile, a uniform first-moment lattice estimate, Cauchy’s inequality on primitive residues, and weighted prime-number-theorem asymptotics give $$\liminf_{x\to\infty}\frac{\log x}{x^{1/48}}\mathcal{E}_{\mathrm{top}}^{\psi}
 \geq \frac{10773\log 2}{1600}.$$ Applying the finite-window lower frame to the complete coefficient vector before restricting to the top-prime subenergy yields $$\liminf_{x\to\infty}\frac{\log x}{x^{1/48}}
 \frac{1}{N}\sum_{n\in I_x}|K_\psi(n)|^2
 \geq \frac{10773\log 2}{3200}.$$ Consequently every upper bound of size $x^{1/48-\delta}(\log x)^A$, with fixed $\delta>0$ and fixed real $A$, is false for this kernel. The result is a structural sharpness obstruction: it does not control the signed four-packet projection, prove arithmetic cancellation, or imply a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

A recurring danger in analytic reassembly arguments is to spend substantial effort sharpening an upper envelope whose power is already attained by a positive collision mode. The purpose of this paper is to locate such a mode inside the exact common-profile kernel of the present twin-prime program.

The immediate upstream papers separate three mechanisms. First, q-labels are collapsed inside each primitive frequency bucket before a finite-window large sieve is applied. Second, a lower frame shows that distinct reduced frequencies cannot cancel by a fixed power after this collapse `\cite{WangTPC238}`. Third, on top-prime denominator rows the q-split direct energy has an exact positive asymptotic of order $x^{1/96}$ `\cite{WangTPC240}`. What remained undecided was whether q-collapse supplies a second factor of this size or whether the collision excess is power-smaller.

We answer that question without estimating individual collision patterns. A fixed nonnegative profile has a positive normalized first moment. After all shell primes are collapsed, the total mass in a top-prime row is asymptotic to $$\frac{3}{2}\frac{pQ^2}{H\log Q}.$$ There are only $p-1$ primitive residue boxes. Cauchy’s inequality therefore forces a coefficient energy of at least the square of this mass divided by $p-1$. Summation against the exact top-prime coefficient $|C_p|^2=(\log p)^2/p^2$ creates the power $$\frac{Q^4}{H^2}=x^{1/48}.$$ The weighted prime average also supplies an explicit logarithmic coefficient.

The order of operations in the finite-window step matters. It is not legal to discard cross terms in the physical window and then keep only top-prime frequencies. We instead apply the existing lower frame to the complete primitive-frequency vector. The resulting coefficient norm is nonnegative, so only at that stage may it be restricted to top primes. This produces half of the coefficient liminf constant and preserves the literal full kernel.

Our conclusion is sharp only in the fixed-power sense. The lower bound is $x^{1/48}/\log x$, whereas available structural upper envelopes carry positive logarithmic losses. Thus logarithmic optimization remains possible, but no argument that forgets signs and polarization before squaring can gain $x^{-\delta}$ for a fixed $\delta>0$.

This distinction is decisive for the route map. The top-prime coefficient $C_p=-\log p/p$ has a fixed sign, but that sign disappears in $|C_p|^2$. Likewise, the four literal polarized packets are absent from the unsigned energy. The theorem therefore neither proves nor refutes cancellation in the signed Gate-B scalar. It says that any successful next argument must expose that signed or polarized structure before taking absolute squares.

The paper is organized as follows. Section [2](sections/2_frozen_setup.tex#L1){reference-type="ref" reference="sec:setup"} freezes the source object. Section [3](sections/3_row_mass_and_cauchy.tex#L1){reference-type="ref" reference="sec:row"} proves the uniform row mass and the collision inequality. Section [4](sections/4_coefficient_liminf.tex#L1){reference-type="ref" reference="sec:coefficient"} derives the explicit coefficient liminf. Section [5](sections/5_finite_window_transfer.tex#L1){reference-type="ref" reference="sec:window"} performs the legal lower-frame transfer. Section [6](sections/6_sharpness_and_route.tex#L1){reference-type="ref" reference="sec:sharpness"} gives the fixed-power obstruction and its route boundary. Section [7](sections/7_certificate.tex#L1){reference-type="ref" reference="sec:certificate"} describes reproducible finite checks, which are deliberately separated from theorem evidence.

# Frozen source object

Let $x\to\infty$ and freeze $$\label{eq:scales}
 H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400}.$$ Let $$\mathcal{Q}_x=\{q\text{ prime}:Q<q\leq 2Q\},
 \qquad I_x=(x/2,x]\cap\mathbb Z,
 \qquad N=\#I_x.$$ Fix once and for all a real function $\psi\in C_c^\infty(\mathbb R)$ such that $$\label{eq:profile}
 0\leq\psi\leq1,\qquad \operatorname{supp}\psi\subseteq[-1,1],
 \qquad \int_{\mathbb R}\psi(t)\,dt=1.$$ All asymptotic constants may depend on this fixed profile. We do not assert a threshold uniform over the whole profile class.

For an active denominator $h\leq U$, a shell prime $q\in\mathcal{Q}_x$, and a primitive residue $a\pmod h$, define $$\label{eq:B_hq}
 B_{h,q}^{\psi}(a)
 =\sum_{0<|m|\leq\lfloor hq/H\rfloor}
 \psi\!\left(\frac{Hm}{hq}\right)
 \mathbf{1}_{m q^{-1}\equiv a\, (\mathrm{mod}\,h)}.$$ Because $h\leq U<q$ eventually, the inverse $q^{-1}\pmod h$ exists whenever $h$ belongs to the squarefree source support. More precisely, let $$\mathcal{D}_x=\{d:H/(4Q)<d\leq U,\ \mu(d)^2=1\},\qquad
 C_h=\sum_{\substack{d\in\mathcal{D}_x\\h\mid d}}\frac{\mu(d)\log d}{d},$$ and put $$\label{eq:full_kernel}
 K_\psi(n)=\sum_{h\leq U}\ \sum_{\substack{a\, (\mathrm{mod}\,h)\\(a,h)=1}}
 C_h\left(\sum_{q\in\mathcal{Q}_x}B_{h,q}^{\psi}(a)\right)
 \mathrm{e}^{2\pi i n a/h}.$$

We use only the top-prime part of its coefficient norm. For primes $U/2<p\leq U$, eventually $p>H/(4Q)$, and the only multiple of $p$ not exceeding $U$ is $d=p$. The exact source identity is therefore $$\label{eq:Cp}
 C_p=-\frac{\log p}{p}.$$ Define $$\begin{aligned}
 B_p^\psi(a)&=\sum_{q\in\mathcal{Q}_x}B_{p,q}^\psi(a),\label{eq:Bp}\\
 S_p&=\sum_{a\in(\mathbb Z/p\mathbb Z)^\times}B_p^\psi(a),\label{eq:Sp}\\
 \mathcal{E}_{\mathrm{top}}^{\psi}&=\sum_{U/2<p\leq U}|C_p|^2
 \sum_{a\in(\mathbb Z/p\mathbb Z)^\times}|B_p^\psi(a)|^2.
 \label{eq:Etop}\end{aligned}$$

The scale arithmetic needed below is $$\label{eq:scale_arithmetic}
 \frac{UQ}{H}=x^{23/2400},\qquad
 \frac{Q^4}{H^2}=x^{1/48},\qquad
 \frac{U^4}{N^2}=x^{-67/100+o(1)}.$$

# Uniform row mass and residue collision

We begin with a fixed-profile lattice estimate.

> **Lemma: First-moment lattice sum**<span id="lem:lattice" label="lem:lattice">\[lem:lattice\]</span> As $T\to\infty$, $$\sum_{0<|m|\leq\lfloor T\rfloor}\psi(m/T)=T+O_\psi(1).$$

> **Proof** The standard Riemann-sum estimate for a fixed smooth compactly supported function gives $$\sum_{m\in\mathbb Z}\psi(m/T)
>  =T\int_{\mathbb R}\psi(t)\,dt+O_\psi(1)=T+O_\psi(1).$$ Removing the $m=0$ term changes the sum by at most one. The support condition accounts for the displayed truncation. Notice that the integral over both signs is already one; no extra factor two occurs.

> **Lemma: Uniform top-prime row mass**<span id="lem:rowmass" label="lem:rowmass">\[lem:rowmass\]</span> Uniformly for primes $U/2<p\leq U$, $$\label{eq:rowmass}
>  S_p=\left(\frac32+o_\psi(1)\right)
>  \frac{pQ^2}{H\log Q}.$$

> **Proof** Eventually $p<q$, $4Q<H$, and $2\lfloor pq/H\rfloor<p$. Thus every active nonzero multiplier has $0<|m|<p$ and maps to a primitive residue modulo the prime $p$. Summing [\[eq:B\_hq\]](sections/2_frozen_setup.tex#L23){reference-type="eqref" reference="eq:B_hq"} over all primitive residues therefore gives $$S_p=\sum_{q\in\mathcal{Q}_x}
>  \sum_{0<|m|\leq\lfloor pq/H\rfloor}
>  \psi\!\left(\frac{Hm}{pq}\right).$$ On the top shells, $pq/H\geq \tfrac12 UQ/H\to\infty$. Lemma [\[lem:lattice\]](sections/3_row_mass_and_cauchy.tex#L5){reference-type="ref" reference="lem:lattice"} is consequently uniform and yields $$S_p=\frac{p}{H}\sum_{q\in\mathcal{Q}_x}q+O_\psi(\#\mathcal{Q}_x).$$ The prime number theorem with partial summation gives $$\label{eq:qfirstmoment}
>  \sum_{Q<q\leq2Q}q
>  =\left(\frac32+o(1)\right)\frac{Q^2}{\log Q};$$ see, for example, `\cite[Chapters 1--2]{MontgomeryVaughan2006}`. The relative lattice error is $$O_\psi\!\left(\frac{H}{pQ}\right)
>  =O_\psi\!\left(x^{-23/2400}\right),$$ uniformly for $p>U/2$. This proves [\[eq:rowmass\]](sections/3_row_mass_and_cauchy.tex#L26){reference-type="eqref" reference="eq:rowmass"}.

> **Lemma: Post-collapse residue Cauchy**<span id="lem:cauchy" label="lem:cauchy">\[lem:cauchy\]</span> For every top prime $p$, $$\label{eq:cauchy}
>  \sum_{a\in(\mathbb Z/p\mathbb Z)^\times}|B_p^\psi(a)|^2
>  \geq\frac{|S_p|^2}{p-1}.$$

> **Proof** There are exactly $p-1$ primitive residues. Apply Cauchy’s inequality to the vector $(B_p^\psi(a))_a$ and use [\[eq:Sp\]](sections/2_frozen_setup.tex#L51){reference-type="eqref" reference="eq:Sp"}.

The placement of Lemma [\[lem:cauchy\]](sections/3_row_mass_and_cauchy.tex#L61){reference-type="ref" reference="lem:cauchy"} is the new structural edge. It is applied after all $q$-rows have been summed. A separate fixed-$q$ application would see only the direct energy and would miss the collision amplification.

# The coefficient liminf

> **Theorem: Top-prime collision lower bound**<span id="thm:coefficient" label="thm:coefficient">\[thm:coefficient\]</span> For every fixed profile satisfying [\[eq:profile\]](sections/2_frozen_setup.tex#L14){reference-type="eqref" reference="eq:profile"}, $$\label{eq:coefficient_liminf}
>  \liminf_{x\to\infty}\frac{\log x}{x^{1/48}}\mathcal{E}_{\mathrm{top}}^{\psi}
>  \geq \frac{10773\log 2}{1600}.$$

> **Proof** Insert Lemma [\[lem:rowmass\]](sections/3_row_mass_and_cauchy.tex#L24){reference-type="ref" reference="lem:rowmass"} into Lemma [\[lem:cauchy\]](sections/3_row_mass_and_cauchy.tex#L61){reference-type="ref" reference="lem:cauchy"}, multiply by $|C_p|^2=(\log p)^2/p^2$, and sum over $U/2<p\leq U$. Since $p/(p-1)=1+o(1)$ uniformly on the top shell, we obtain $$\begin{aligned}
>  \mathcal{E}_{\mathrm{top}}^{\psi}
>  &\geq \left(\frac94+o_\psi(1)\right)
>  \frac{Q^4}{H^2(\log Q)^2}
>  \sum_{U/2<p\leq U}\frac{(\log p)^2}{p}.\label{eq:pre_pnt}\end{aligned}$$ Another standard partial-summation consequence of the prime number theorem is $$\label{eq:weighted_pnt}
>  \sum_{U/2<p\leq U}\frac{(\log p)^2}{p}
>  =(\log2+o(1))\log U.$$ Hence $$\label{eq:coefficient_preconstant}
>  \mathcal{E}_{\mathrm{top}}^{\psi}\geq
>  \left(\frac{9\log2}{4}+o_\psi(1)\right)
>  \frac{Q^4}{H^2}\frac{\log U}{(\log Q)^2}.$$
>
> It remains to record the constant without hiding a logarithmic conversion. From [\[eq:scales\]](sections/2_frozen_setup.tex#L4){reference-type="eqref" reference="eq:scales"}, $$\frac{\log U}{\log Q}=\frac{399}{400},
>  \qquad \frac{1}{\log Q}=\frac{3}{\log x},
>  \qquad \frac{Q^4}{H^2}=x^{1/48}.$$ Therefore $$\frac94\cdot\frac{399}{400}\cdot3
>  =\frac{10773}{1600},$$ and [\[eq:coefficient\_liminf\]](sections/4_coefficient_liminf.tex#L5){reference-type="eqref" reference="eq:coefficient_liminf"} follows.

> **Remark** The lower bound is profilewise. The leading constant is independent of the shape of the fixed admissible profile because it uses the normalized first moment $\int\psi=1$, rather than the second moment appearing in the q-split direct energy.

# Finite-window transfer without deleting cross terms

The coefficient lower bound concerns the full primitive-frequency expansion underlying [\[eq:full\_kernel\]](sections/2_frozen_setup.tex#L36){reference-type="eqref" reference="eq:full_kernel"}. We now transfer it to the literal physical window.

> **Theorem: Finite-window liminf**<span id="thm:window" label="thm:window">\[thm:window\]</span> For every fixed profile satisfying [\[eq:profile\]](sections/2_frozen_setup.tex#L14){reference-type="eqref" reference="eq:profile"}, $$\label{eq:window_liminf}
>  \liminf_{x\to\infty}\frac{\log x}{x^{1/48}}
>  \frac{1}{N}\sum_{n\in I_x}|K_\psi(n)|^2
>  \geq \frac{10773\log 2}{3200}.$$

> **Proof** The finite-window lower frame of `\cite{WangTPC238}`, applied to the complete coefficient vector indexed by distinct primitive fractions $a/h$, gives $$\begin{aligned}
>  \frac{1}{N}\sum_{n\in I_x}|K_\psi(n)|^2
>  &\geq
>  \left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+
>  \sum_{h\leq U}\ \sum_{\substack{a\, (\mathrm{mod}\,h)\\(a,h)=1}}
>  \left|C_h\sum_{q\in\mathcal{Q}_x}B_{h,q}^\psi(a)\right|^2.
>  \label{eq:full_lower_frame}\end{aligned}$$ Every term in the coefficient norm on the right is nonnegative. We may now, and only now, restrict it to prime denominators $U/2<p\leq U$. The restricted sum is exactly $\mathcal{E}_{\mathrm{top}}^{\psi}$. Thus $$\label{eq:window_top_restriction}
>  \frac{1}{N}\sum_{n\in I_x}|K_\psi(n)|^2
>  \geq
>  \left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+\mathcal{E}_{\mathrm{top}}^{\psi}.$$ By [\[eq:scale\_arithmetic\]](sections/2_frozen_setup.tex#L58){reference-type="eqref" reference="eq:scale_arithmetic"}, the bracket is $1/2-o(1)$. Combining [\[eq:window\_top\_restriction\]](sections/5_finite_window_transfer.tex#L30){reference-type="eqref" reference="eq:window_top_restriction"} with Theorem [\[thm:coefficient\]](sections/4_coefficient_liminf.tex#L3){reference-type="ref" reference="thm:coefficient"} proves [\[eq:window\_liminf\]](sections/5_finite_window_transfer.tex#L9){reference-type="eqref" reference="eq:window_liminf"}.

> **Remark: Why the order is necessary** The quadratic form on the left of [\[eq:full\_lower\_frame\]](sections/5_finite_window_transfer.tex#L25){reference-type="eqref" reference="eq:full_lower_frame"} contains cross-frequency terms that need not be nonnegative. Deleting them before applying the lower frame would be invalid. Our restriction occurs only after the complete quadratic form has been bounded below by a diagonal coefficient norm.

# Fixed-power sharpness and route closure

> **Corollary: No fixed-power improvement**<span id="cor:no_power" label="cor:no_power">\[cor:no\_power\]</span> Fix an admissible profile $\psi$, a number $\delta>0$, and a real number $A$. There is no constant $C_{\psi,\delta,A}$ for which $$\label{eq:false_upper}
>  \frac{1}{N}\sum_{n\in I_x}|K_\psi(n)|^2
>  \leq C_{\psi,\delta,A}
>  x^{1/48-\delta}(\log x)^A$$ holds for all sufficiently large $x$.

> **Proof** Theorem [\[thm:window\]](sections/5_finite_window_transfer.tex#L7){reference-type="ref" reference="thm:window"} has a positive liminf constant. Dividing its lower scale by the right side of [\[eq:false\_upper\]](sections/6_sharpness_and_route.tex#L6){reference-type="eqref" reference="eq:false_upper"} produces, up to a positive constant, $$\frac{x^\delta}{(\log x)^{A+1}},$$ which tends to infinity for every fixed real $A$. This contradicts [\[eq:false\_upper\]](sections/6_sharpness_and_route.tex#L6){reference-type="eqref" reference="eq:false_upper"}.

Corollary [\[cor:no\_power\]](sections/6_sharpness_and_route.tex#L3){reference-type="ref" reference="cor:no_power"} closes a specific route, not the whole twin-prime program. It excludes further fixed-power progress from a coefficient-blind unsigned envelope on the same fixed-profile common-source kernel. Three features remain outside the theorem:

1.  The sign of $C_h$ is erased by the absolute square. Even on top primes, the identity $C_p=-\log p/p$ contributes only $|C_p|^2$.

2.  The four literal polarized packets are not projected before the square. Their signed combination could cancel, attenuate, or annihilate the positive collision mode proved here.

3.  The theorem supplies no arithmetic $L^2$ saving, no strict $1/400$ payment, and no fixed-atom credit.

The most economical next question is therefore sign-sensitive: project the top-prime collision mode through the actual four-packet polarization before any absolute square, or retain the literal $C_h$ signs across denominator bands. Continuing to optimize unsigned bucket multiplicities cannot change the fixed-power exponent.

The phrase “sharp up to logarithms” is used only in this fixed-power sense. The present lower bound has one negative logarithm, while known structural upper bounds have positive logarithmic factors. Matching those logarithms is an open refinement and is not needed for Corollary [\[cor:no\_power\]](sections/6_sharpness_and_route.tex#L3){reference-type="ref" reference="cor:no_power"}.

# Exact finite certificate and adversarial controls

The release contains three executable checks. Their purpose is reproducibility of the algebraic ledger and software interface; none is used as evidence for an asymptotic theorem.

The producer records every exponent and leading rational as an exact fraction. In particular it recomputes $$\frac{Q^4}{H^2}=x^{1/48},\qquad
 \frac94\frac{399}{400}3=\frac{10773}{1600},\qquad
 \frac12\frac{10773}{1600}=\frac{10773}{3200}.$$ It also freezes the object type, profile class, shell domains, and the legal full-vector-frame-before-restriction order. Mutations that promote the status, change the profile to a signed class, replace q-collapse by a q-split object, or reverse the frame order are required to fail.

The finite fixture uses $Q=101$, $H=509$, $U=97$, three top primes, and all twenty primes in $(Q,2Q]$. Rational compact-support weights are collapsed at primitive residues. For each row, the program verifies $$\sum_a\left|\sum_q B_{p,q}(a)\right|^2
 \geq \frac{\left|\sum_{a,q}B_{p,q}(a)\right|^2}{p-1}$$ and finds strictly positive collision excess over the q-split direct energy. These weights are finite algebraic illustrations, not substitutions for the fixed smooth theorem profile.

An independent checker does not import the producer. It rejects duplicate JSON keys and nonfinite constants, recomputes every rational row, and verifies strict JSON types. A separate stress program repeats the collision test for four prime-shell scales and two rational bump shapes. Normal and optimized Python modes must have empty standard error and byte-identical standard output.

# Conclusion

The exact unsigned common-profile kernel contains a positive top-prime q-collision mode of size $x^{1/48}/\log x$. A full-vector lower frame transfers half of its explicit liminf constant to the literal finite window. Hence the power $1/48$ cannot be improved by any fixed amount within this unsigned lane.

This obstruction is useful because it changes the next problem rather than merely worsening an estimate. Any future fixed-power saving must retain the four-packet polarization or literal coefficient signs before squaring. Whether that signed projection cancels the sharp positive mode is the principal open theorem left by this paper.

# Claim and route ledger

For clarity, the release status is summarized in Table [1](sections/A_status_ledger.tex#L27){reference-type="ref" reference="tab:ledger"}.

<div id="tab:ledger">

| Item                                   | Status                         |
|:---------------------------------------|:-------------------------------|
| Fixed-profile top-prime row mass       | proved, uniform $3/2$ constant |
| Primitive-residue post-collapse Cauchy | proved exactly                 |
| Coefficient liminf                     | $10773\log2/1600$              |
| Finite-window liminf                   | $10773\log2/3200$              |
| Unsigned fixed-power exponent          | $1/48$, sharp up to logarithms |
| Class-uniform profile threshold        | not claimed                    |
| Physical-window cross-term deletion    | forbidden                      |
| Signed $C_h$ cancellation              | none                           |
| Signed four-packet Gate-B scalar       | open                           |
| Arithmetic $L^2$                       | none                           |
| Strict $1/400$                         | unpaid globally                |
| Twin-prime conclusion                  | none                           |

: TPC-241 claim firewall.

</div>

The strongest reusable structure is the composition $$\begin{aligned}
 &\text{normalized profile first moment}
 \longrightarrow \text{primitive-residue Cauchy}\\
 &\hspace{3em}\longrightarrow \text{weighted PNT}
 \longrightarrow \text{full-vector finite-window lower frame}.\end{aligned}$$ The resulting round-two clue is: retain four-packet polarization or literal $C_h$ signs before squaring, because the unsigned top-prime collision channel is fixed-power sharp.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{MontgomeryVaughan2006,
  author    = {Hugh L. Montgomery and Robert C. Vaughan},
  title     = {Multiplicative Number Theory I: Classical Theory},
  series    = {Cambridge Studies in Advanced Mathematics},
  volume    = {97},
  publisher = {Cambridge University Press},
  year      = {2006}
}

@unpublished{WangTPC238,
  author = {Liang Wang},
  title  = {A Finite-Window Lower-Frame Obstruction for Primitive Rational Frequencies},
  note   = {TPC-238 research manuscript and proof package},
  year   = {2026}
}

@unpublished{WangTPC240,
  author = {Liang Wang},
  title  = {A Top-Prime Direct-Energy Floor for the Frozen Common Profile},
  note   = {TPC-240 research manuscript and proof package},
  year   = {2026}
}
```

<!-- SOURCE_BODY_END -->
