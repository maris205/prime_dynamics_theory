# Literal Two-Channel Compatibility for the Twin-Prime Bridge

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology; Wuhan 430074, P.R. China
- Source date: August 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-223 left a precise but conditional interface between a prime-AP/collision channel and a four-packet polarized channel. The unresolved question was whether those channels can be evaluated on one literal coefficient family, rather than on two objects that merely share an exponent ledger. We answer the structural part of this question. For vectors $W_{q,j}$ in one common Hilbert space, define the AP marginal by summing over $q$, the polarized marginal by summing over $j$, and the full target by summing over both labels. Then $$E_{\mathrm{all}}\leq \min(JE_{\mathrm{AP}},PE_{\mathrm{pol}})
 \leq \frac{PJ}{P+J}(E_{\mathrm{AP}}+E_{\mathrm{pol}}).$$ The additive constant is sharp. We instantiate the vectors with the exact prime-AP row rule of TPC-220, keeping the same $h,q,j,m$ and normalization in all three quantities. Nine finite growing source-surrogate scales pass the sharp inequality by exact rational arithmetic. A separate congruence-aligned stress clock reaches the sharp constant at five scales and refutes the tempting unit-constant interface. The result removes a structural reassembly black box, but it supplies neither marginal arithmetic saving: AP dispersion, polarized cross-correlation, $L^2$ credit, and the twin-prime conclusion remain open.

<!-- SOURCE_BODY_BEGIN -->

#### Claim level.

`PROVED_STRUCTURAL_L1 / LITERAL_TWO_CHANNEL_COMPATIBILITY`.\
The finite Hilbert theorem is unconditional algebra. The two finite clocks are explicitly modeling choices and are not an asymptotic prime theorem.

# Why compatibility is the next bridge

The current analytic route contains two different kinds of information. The prime-AP line rewrites a $q$-labelled row family as a multiplicative collision Gram; the four-packet line recovers signed cross-terms by phase polarization. Those constructions are useful only if their estimates refer to the same physical object. TPC-223 therefore stated a conditional compiler with three inputs: an AP estimate, a polarized estimate, and a literal reassembly interface `\cite{tpc220,tpc222,tpc223}`.

The third input is easy to understate. One can write two marginal estimates with identical powers of $x$ while changing the order of label summation or the normalization of the coefficient vector. Such a change is invisible to an exponent ledger but can change a finite quadratic form by a fixed factor or more. The present paper freezes the common object first and asks only the algebraic question that follows.

Our contribution is a sharp compatibility theorem. Let $P=|\mathcal Q|$ be the number of prime labels and let $J$ be the number of packet labels. For one family of vectors $W_{q,j}$, form the three energies $$\begin{aligned}
 E_{\mathrm{AP}}&=\sum_{j=0}^{J-1}\left\|\sum_{q\in\mathcal Q}W_{q,j}\right\|^2,\label{eq:ap}\\
 E_{\mathrm{pol}}&=\sum_{q\in\mathcal Q}\left\|\sum_{j=0}^{J-1}W_{q,j}\right\|^2,\label{eq:pol}\\
 E_{\mathrm{all}}&=\left\|\sum_{q\in\mathcal Q}\sum_{j=0}^{J-1}W_{q,j}\right\|^2.\label{eq:all}\end{aligned}$$ The theorem gives a common interface for exactly these quantities. It also shows why the coefficient one is not available: aligned literal rows attain the factor $PJ/(P+J)$.

The claim boundary is deliberate. A finite vector identity is not an AP dispersion theorem. We do not infer prime cancellation from the observed scales, and we do not replace the V46 source clock by the finite clocks used for the audit.

# The common literal coefficient family

We use the row notation inherited from TPC-220. For a modulus $h$, a prime $q$ coprime to $h$, a packet profile $\psi_j$, and a residue $a\pmod h$, define $$B_{h,q}^{(j)}(a)=
 \sum_{0<|m|\leq \lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m\bar q\equiv a\pmod h}.
 \label{eq:row}$$ The important point is that this row is created once. We then set $$W_{q,j}(h,a)=C_h B_{h,q}^{(j)}(a),
 \qquad W_{q,j}\in\ell^2(\mathcal F),
 \label{eq:vector}$$ where $\mathcal F$ is the finite set of active $(h,a)$ coordinates. The certificate uses the explicit shared normalization $C_h=1/h$. A different common normalization would leave the theorem unchanged, but replacing it in only one channel would produce a different problem.

The AP marginal in [\[eq:ap\]](main.tex#L82){reference-type="eqref" reference="eq:ap"} is the coefficient-space version of the prime-label reassembly. The polarized marginal in [\[eq:pol\]](main.tex#L83){reference-type="eqref" reference="eq:pol"} is the packet-space reassembly. If $T_I$ denotes the common finite-window synthesis map $$(T_IW)(n)=\sum_{(h,a)\in\mathcal F}W(h,a)\,e(na/h),
 \qquad n\in I,$$ the same definitions can be made with $T_IW_{q,j}$ in place of $W_{q,j}$. Thus the theorem is stable under a common physical window; it does not assume that the synthesis map is an isometry.

# Sharp common-vector theorem

> **Theorem: common two-channel compatibility** <span id="thm:compatibility" label="thm:compatibility">\[thm:compatibility\]</span> For any finite $\mathcal Q$ of size $P$, any positive integer $J$, and any vectors $W_{q,j}$ in a common complex Hilbert space, the energies [\[eq:ap\]](main.tex#L82){reference-type="eqref" reference="eq:ap"}–[\[eq:all\]](main.tex#L84){reference-type="eqref" reference="eq:all"} satisfy $$E_{\mathrm{all}}\leq JE_{\mathrm{AP}},\qquad E_{\mathrm{all}}\leq PE_{\mathrm{pol}},
>  \label{eq:directional}$$ and consequently $$E_{\mathrm{all}}\leq \frac{PJ}{P+J}(E_{\mathrm{AP}}+E_{\mathrm{pol}}).
>  \label{eq:sharp}$$ The coefficient $PJ/(P+J)$ is the smallest universal coefficient in [\[eq:sharp\]](main.tex#L144){reference-type="eqref" reference="eq:sharp"}.

> **Proof** Put $V_j=\sum_qW_{q,j}$ and $U_q=\sum_jW_{q,j}$. The full vector is both $\sum_jV_j$ and $\sum_qU_q$. Cauchy–Schwarz in the two finite label spaces gives $$\left\|\sum_jV_j\right\|^2\leq J\sum_j\|V_j\|^2=JE_{\mathrm{AP}},
>  \qquad
>  \left\|\sum_qU_q\right\|^2\leq P\sum_q\|U_q\|^2=PE_{\mathrm{pol}},$$ which proves [\[eq:directional\]](main.tex#L139){reference-type="eqref" reference="eq:directional"}.
>
> For nonnegative $a,b$, the scalar inequality $$\min(Ja,Pb)\leq \frac{PJ}{P+J}(a+b)$$ follows by considering the two cases $Ja\leq Pb$ and $Pb\leq Ja$. Applying it with $a=E_{\mathrm{AP}}$ and $b=E_{\mathrm{pol}}$ proves [\[eq:sharp\]](main.tex#L144){reference-type="eqref" reference="eq:sharp"}.
>
> To prove sharpness, choose a nonzero vector $u$ and set $W_{q,j}=u$ for every pair of labels. Then $$E_{\mathrm{AP}}=JP^2\|u\|^2,\qquad
>  E_{\mathrm{pol}}=PJ^2\|u\|^2,\qquad
>  E_{\mathrm{all}}=P^2J^2\|u\|^2,$$ so equality holds in [\[eq:sharp\]](main.tex#L144){reference-type="eqref" reference="eq:sharp"}. No smaller universal coefficient can therefore work.

> **Remark: What the theorem does and does not compile** The theorem proves the natural structural form of TPC-223’s reassembly input. For fixed $J=4$, its factor is less than $4$, hence it contributes no power of $x$ to an exponent ledger. It does not prove bounds for either $E_{\mathrm{AP}}$ or $E_{\mathrm{pol}}$. Those remain the two arithmetic estimates that must be supplied on the source-locked object.

# Literal growth audit

The exact certificate has two named experiments. The first is a finite source-surrogate clock with actual primes in $(Q,2Q]$, $x=Q^3$, $H=4Q^2$, and $h=4Q$. It uses affine profiles $$\psi_j(t)=1+\frac{\alpha_j}{10}t,
 \qquad (\alpha_0,\alpha_1,\alpha_2,\alpha_3)=(0,1,-1,2).$$ The second is a separate collision stress clock with $H=5Q$, $h=5$, constant profiles, and only primes $q\equiv1\pmod5$. The second clock is chosen to make the congruence alignment visible; it is not spliced with the first clock or promoted to the V46 asymptotic regime.

All row values, vector additions, and energies are computed as fractions. The independent checker reconstructs the rows without importing the producer. Table [1](main.tex#L227){reference-type="ref" reference="tab:source"} reports the source-surrogate unit ratio $E_{\mathrm{all}}/(E_{\mathrm{AP}}+E_{\mathrm{pol}})$; every sharp-interface residual is exactly zero or nonnegative as required.

<div id="tab:source">

|  $Q$|  $P$|  active coordinates|  unit ratio (decimal)|  sharp ratio|
|----:|----:|-------------------:|---------------------:|------------:|
|   11|    3|                   6|              0.799023|            1|
|   17|    4|                   8|              0.799007|            1|
|   29|    6|                  12|              0.798961|            1|
|   43|    9|                  18|              0.799066|            1|
|   61|   12|                  24|              0.799017|            1|
|   89|   16|                  32|              0.799002|            1|
|  127|   23|                  46|              0.798997|            1|
|  181|   30|                  60|              0.799012|            1|
|  257|   42|                  84|              0.799005|            1|

: Exact-rational source-surrogate audit. The displayed unit ratios are rounded only for presentation; the certificate stores exact fractions.

</div>

The stress clock realizes the aligned family in the theorem. Since the cutoff is one and $q^{-1}=1\pmod5$, every active row has the same two primitive coordinates. Consequently the sharp ratio is exactly one after dividing by $PJ/(P+J)$, while the unit ratio is the sharp constant itself.

<div id="tab:stress">

|   $Q$|  $P$|  $J$|  unit ratio|  $PJ/(P+J)$|
|-----:|----:|----:|-----------:|-----------:|
|   101|    4|    4|         $2$|         $2$|
|   211|    8|    4|       $8/3$|       $8/3$|
|   401|   15|    4|     $60/19$|     $60/19$|
|  1009|   34|    4|     $68/19$|     $68/19$|
|  2003|   62|    4|    $124/33$|    $124/33$|

: Literal congruence-aligned stress audit. The unit-factor interface is refuted at every scale, while the sharp interface is attained exactly.

</div>

The stress result is an obstruction to a normalization shortcut, not a lower bound for the original twin-prime expression. It says that any later proof must preserve the cross-label geometry until the two marginal estimates have been related on the same object.

# Route evaluation and relation to TPC-223

TPC-223’s exponent compiler remains valid. The present theorem supplies a structural candidate for its third input, with a bounded factor when $J=4$: $$S_x\ll \frac{PJ}{P+J}(A_x+P_x)$$ provided $A_x$ and $P_x$ are exactly the two marginal energies defined above on the same source-locked vector family. The phrase “provided” is an identification condition, not a hidden theorem. In particular, the current repository still has no proof of $$E_{\mathrm{AP}}\ll x^{E_0-\delta_{\rm AP}+o(1)},
 \qquad
 E_{\mathrm{pol}}\ll x^{E_0-\kappa_{\rm pol}+o(1)}$$ for the exact V46 object with the required normalization and fixed-atom quantifiers.

The route status is therefore: $$\begin{gathered}
\texttt{COMMON\_INTERFACE=PROVED\_STRUCTURAL\_L1}\\
\texttt{AP=OPEN},\quad \texttt{POLARIZED=OPEN}\\
\texttt{L2=NONE},\quad \texttt{FULL\_GATE\_B=OPEN}
\end{gathered}$$ The next useful theorem is not another abstract combination rule. It is a source-locked simultaneous estimate for the two marginals, with the same finite-window synthesis, zero/nonunit terms, and normalization.

# Conclusion

TPC-224 converts a vague compatibility requirement into a sharp finite theorem. The AP and polarized channels can be made literal restrictions of one vector family, and the full reassembly costs at most $PJ/(P+J)$ times their sum. A congruence-aligned prime shell shows that the unit constant is not legitimate, even though the sharp factor is bounded when the packet count is fixed.

This is a structural L1 result. The source-surrogate and stress clocks are finite modeling choices, not a replacement for the V46 asymptotic clock. No prime dispersion, polarized cancellation, arithmetic $L^2$ estimate, fixed-atom credit, strict $1/400$ payment, or twin-prime conclusion follows.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc220,
  author       = {Liang Wang},
  title        = {Prime-AP Collision Crosswalk for the Literal Shell},
  year         = {2026},
  note         = {TPC-220 repository proof record}
}

@misc{tpc222,
  author       = {Liang Wang},
  title        = {Four-Packet Polarization and the PSD Cross-Term Obstruction},
  year         = {2026},
  note         = {TPC-222 repository proof record}
}

@misc{tpc223,
  author       = {Liang Wang},
  title        = {A Conditional Signed-Reassembly Compiler for the Twin-Prime Bridge},
  year         = {2026},
  note         = {TPC-223 repository proof record}
}
```

<!-- SOURCE_BODY_END -->
