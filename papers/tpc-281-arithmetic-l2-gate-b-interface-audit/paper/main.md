# A Typed Arithmetic $L^2$ Interface for Four-Packet Gate-B Reassembly

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding four-packet analysis separates a signed reassembly gain from the arithmetic estimate that would have to produce it. This note makes that separation typed. Let $A_X$ be an operator from a source Hilbert space into $\ell^2(I_X)$ and suppose $\|A_X\|_{2\to2}\le KX^{-\sigma}$. If four packets have diagonal energy $D$, reassembled energy $G$, and normalized gain input $G/D\le Q_X$, then the exact interface is $$\|A_XS\|_2^2\le K^2X^{-2\sigma}Q_XD.$$ Combining the two-term budget from TPC-280, $Q_X\le BX^{-\gamma}+(\ell/d)X^{-\delta}$, with an upper source envelope $D\le d_+X^a$ gives the collapsed exponent $a-2\sigma-\min(\gamma,\delta)$. Scalar readouts contract by Cauchy–Schwarz. We then prove an exact attachment obstruction: for the same nonzero packet sum in $\mathbb R^2$, two rank-one functionals have equal operator norm but give respectively full and zero attachment. Thus packet geometry and an $L^2$ norm do not identify the arithmetic attachment. Four exact rational packet witnesses, four interface cases, and the twelve-row TPC-280 transfer are independently certified. The operator estimate and nondegenerate attachment for the literal growing prime source remain open; no fixed-power credit or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Typed source interface

Let $X\ge1$ be a scale, $\mathcal H_X$ a Hilbert space, and $I_X$ an index set. Write $$A_X:\mathcal H_X\longrightarrow\ell^2(I_X)$$ for a linear operator. Four source packets $V_0,\ldots,V_3\in\mathcal H_X$ are reassembled as $$S=\sum_{j=0}^3V_j,\qquad
 D=\sum_{j=0}^3\|V_j\|^2,\qquad
 G=\|S\|^2,
 \qquad q=G/D,$$ when $D>0$. The notation follows the exact coherence-to-gain interface in TPC-279 `\cite{tpc279}`. TPC-280 showed that a raw additive leakage estimate must be normalized using a source lower bound `\cite{tpc280}`.

The present question is narrower: once an arithmetic operator estimate is available, what does it actually buy at the Gate-B output? We assume the typed hypotheses $$\|A_X\|_{2\to2}\le KX^{-\sigma},\qquad
 q\le Q_X,\qquad D\le d_+X^a,
 \label{eq:hyp}$$ where $K,d_+>0$. The first condition is deliberately stated as an operator statement. It is not inferred from a finite matrix experiment.

# The exact interface theorem

> **Theorem: typed arithmetic $L^2$ interface** Assume [\[eq:hyp\]](main.tex#L73){reference-type="eqref" reference="eq:hyp"}. Then $$\|A_XS\|_2^2
>  \le K^2X^{-2\sigma}Q_XD.
>  \label{eq:two}$$ If, in addition, $$Q_X\le BX^{-\gamma}+\frac{\ell}{d}X^{-\delta}
>  \le \left(B+\frac{\ell}{d}\right)X^{-\kappa},
>  \qquad \kappa=\min(\gamma,\delta),$$ then $$\|A_XS\|_2^2
>  \le K^2d_+\left(B+\frac{\ell}{d}\right)
>  X^{a-2\sigma-\kappa}.
>  \label{eq:collapsed}$$

> **Proof** The operator norm and the definition of $G$ give $$\|A_XS\|_2^2\le \|A_X\|_{2\to2}^2\|S\|^2
>  \le K^2X^{-2\sigma}G.$$ Since $G=qD\le Q_XD$, this is [\[eq:two\]](main.tex#L85){reference-type="eqref" reference="eq:two"}. The second displayed assumption and $D\le d_+X^a$ yield [\[eq:collapsed\]](main.tex#L98){reference-type="eqref" reference="eq:collapsed"} by substitution.

> **Corollary: scalar readout** If $\lambda\in(\ell^2(I_X))^*$ and $\|\lambda\|\le1$, then $$|\lambda(A_XS)|^2\le \|A_XS\|_2^2
>  \le K^2X^{-2\sigma}Q_XD.
>  \label{eq:scalar}$$

> **Proof** Cauchy–Schwarz (or the definition of the dual norm) gives $|\lambda(y)|\le\|\lambda\|\|y\|_2\le\|y\|_2$.

The theorem is a typed interface rather than a source theorem. In particular, it does not assert that the literal prime/Möbius operator has norm $O(X^{-\sigma})$. It records exactly how such an estimate would enter the existing packet budget. If the inherited margin identity is available, $m^2=(D/G)m_D^2$, then the TPC-280 compiler contributes $\kappa/2$ to the margin exponent, while the typed operator contributes $\sigma$ to the output energy. The endpoint ledger therefore still needs the separately paid strict inequality $\sigma-\eta_{\rm eff}>1/400$.

# Attachment is an independent input

The norm estimate in Theorem 1 controls an output from above. It cannot by itself provide a lower bound for a particular scalar attachment. The next proposition makes this non-identifiability exact.

> **Proposition: equal-norm attachment obstruction** Let $S=(S_1,S_2)\in\mathbb R^2$ be nonzero and put $G=\|S\|^2$. Define Riesz representatives $$u_{\parallel}=S,\qquad u_{\perp}=(-S_2,S_1),$$ and rank-one functionals $L_u(v)=\langle u,v\rangle$. Then $$\|L_{u_{\parallel}}\|^2=\|L_{u_{\perp}}\|^2=G,$$ whereas $$L_{u_{\parallel}}(S)=G,\qquad L_{u_{\perp}}(S)=0.$$ Consequently, the packet data $(D,G)$ and the operator norm do not imply any positive lower bound for the squared attachment of $S$.

> **Proof** Rotation by $90$ degrees preserves the Euclidean norm, so both functional norms squared equal $G$. Direct calculation gives $$\langle S,S\rangle=G,\qquad
>  \langle(-S_2,S_1),(S_1,S_2)\rangle=0.$$ The two choices have identical packet geometry and norm data but attachments $G^2$ and $0$ after squaring. This proves the claim.

> **Remark** The perpendicular functional is an information-model adversary, not a claim about the actual arithmetic operator. To use Theorem 1 for a prime source one needs a typed identification or nondegeneracy theorem linking the arithmetic readout to the packet direction. Such a theorem is not supplied here.

# Exact audit and finite transfer

The release certificate uses four rational packet tuples in $\mathbb R^2$. The balanced witness has $(D,G)=(5,5)$; the near-cancel witness has $(D,G)=(1141/100,1/100)$; the aligned witness has $(4,16)$; and the mixed witness has $(14,2)$. Their normalized ratios are respectively $1$, $1/1141$, $4$, and $1/7$. For each tuple the parallel and perpendicular functionals have the same squared norm, while the latter has zero attachment.

<div id="tab:packets">

| fixture     |         $D$|      $G$|     $G/D$|  parallel/perpendicular attachment$^2$|
|:------------|-----------:|--------:|---------:|--------------------------------------:|
| balanced    |         $5$|      $5$|       $1$|                             $25\,;\,0$|
| near-cancel |  $1141/100$|  $1/100$|  $1/1141$|                        $1/10000\,;\,0$|
| aligned     |         $4$|     $16$|       $4$|                            $256\,;\,0$|
| mixed       |        $14$|      $2$|     $1/7$|                              $4\,;\,0$|

: Exact packet and attachment audit.

</div>

Four finite interface cases instantiate the theorem with $X\in\{8,16\}$, integer exponents, rational $K,B,\ell/d$, and source upper envelope $D\le X^2$. The mixed case deliberately has both budget lanes: $B=3$, $\ell/d=1$, $\gamma=1$, $\delta=2$, so its two-term budget is $49/256$ and its collapsed budget is $1/4$. All comparisons are exact.

As a provenance control, the certificate also copies the twelve coordinate rows from TPC-280. It preserves the eight positive-deficit and four negative-deficit labels and grants zero fixed power. This transfer validates schema and coordinates only; it cannot turn a finite parent table into a growing arithmetic estimate.

# Claim firewall and conclusion

The main implication is elementary but useful: it tells the next source-level proof exactly what a literal arithmetic $L^2$ theorem would purchase. The attachment proposition prevents a common category error in which an operator norm or packet cancellation is treated as a lower bound for a selected scalar. The strongest current route statement is therefore $$\text{packet geometry}\ \longrightarrow\ \text{typed arithmetic }L^2
 \longrightarrow\ \text{output energy}\ \longrightarrow\ \text{scalar readout},$$ with the middle arrow conditional and the final attachment requiring its own nondegeneracy input.

The literal source arithmetic $L^2$ estimate, typed attachment theorem, full Gate B, and the twin-prime conclusion remain open. The fixed-power credit is zero. The Session-named Route-A and Route-B evaluator files are not present in the checkout; the local proof package, exact certificate, independent replay, hostile stress audit, and fail-closed Bridge-B checker provide the scoped release evaluation.

# References

9 Liang Wang, “A Minimal Coherence-to-Gain Criterion for Four-Packet Reassembly,” TPC-279 project release, 2026.

Liang Wang, “An Additive-Leakage Compiler for Signed Gain and Endpoint Budgets,” TPC-280 project release, 2026.

<!-- SOURCE_BODY_END -->
