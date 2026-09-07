# A Rank-Three Physical Cross-Gram Channel in the Literal V59 Interface

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-262 identified the literal signed cross-Gram as the correct growing-shell observable, but left its actual source packets untreated. We combine two source-backed inputs on the same V59 clock. The maximal-interval hybrid estimate controls all four consecutive block sums, while the four-block Haar construction supplies three adjoint coefficients with explicit asymptotics. The resulting rank-three physical channel is $O_{M,K}(x^{5/3}/(\log x)^{M+3})$ for every fixed admissible $K$ and fixed logarithmic strength $M$. We prove the exact complementary split and keep the orthogonal residual explicit. Thus this is a genuine logarithmic channel advance, with zero fixed-power credit; it is not a full $L^2$ bound, an endpoint payment, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The Route-B object is the literal common-clock coupling $C_x=\left\langle w,A_x\beta\right\rangle$, with the prime shell, unit masks, deleted diagonal, and smooth kernel retained. TPC-257 constructed a source-only four-block frame $z_0,z_1,z_2$ and proved $$\left\langle z_i,A_x\beta\right\rangle=-(9\kappa_i/2+o(1))\frac{x^{7/6}}{(\log x)^3}.$$ TPC-254 controlled the hybrid residual on every consecutive interval to an arbitrary fixed logarithmic order. The question here is whether those two facts can be multiplied on the same physical object, without replacing the full coupling by a finite diagonal surrogate.

Our maximum claim is $$\boxed{C_3(x):=\left\langle \mathsf P_3w,\mathsf P_3A_x\beta\right\rangle
   =O_{M,K}\!\left(\frac{x^{5/3}}{(\log x)^{M+3}}\right)}.$$ The notation `x^(5/3)` in the release certificate refers to the same power. The theorem is for fixed $M,K$, and its constants are not claimed uniform in either parameter.

# The source-only rank-three frame

Let $I_x=(x/2,x]\cap\mathbb Z$, $N=|I_x|$, $\ell=\lfloor N/2\rfloor$, and $r=N-\ell$. Split the two rank children into consecutive blocks $B_1,B_2,B_3,B_4$, with sizes $s_1,s_2,s_3,s_4$. For adjacent sets of sizes $p,q$, define $$h(A,B)=\sqrt{\frac{pq}{p+q}}\left(\frac{1_A}{p}-\frac{1_B}{q}\right).$$ Set $$z_0=h(B_1\cup B_2,B_3\cup B_4),\qquad
 z_1=h(B_1,B_2),\qquad z_2=h(B_3,B_4).$$

> **Lemma: exact frame geometry** The vectors $z_0,z_1,z_2$ are source-only and orthonormal for every admissible real clock. Consequently $$\mathsf P_3=\sum_{i=0}^2 z_i\otimes z_i$$ is an orthogonal projection.

> **Proof** For $h(A,B)$, its squared norm is $pq(p^{-1}+q^{-1})/(p+q)=1$. The block-weighted product of $z_0$ and $z_1$ is $$s_1\frac1\ell\frac1{s_1}+s_2\frac1\ell\frac{-1}{s_2}=0.$$ The same calculation applies to $z_0,z_2$, while $z_1,z_2$ have disjoint support. This also covers odd child cardinalities because the definitions are made by rank, not by an integer-only macroscopic threshold.

# Three hybrid moments

Write $W_j=\sum_{u\in B_j}w(u)$. The maximal Type-I source theorem used in TPC-254 is a nonnegative sum over active intervals. Its $m=1$ row therefore controls each of these four consecutive sums, for every fixed $M,K$: $$|W_j|\ll_{M,K}\frac{x}{(\log x)^M}.$$ Each frame vector is a normalized difference of two block means, and every block size is comparable with $x$. Hence $$|\left\langle z_i,w\right\rangle|\ll_{M,K}\frac{x^{1/2}}{(\log x)^M},
 \qquad i=0,1,2.                                      \label{eq:w}$$ The order of operations matters: the four interval bounds are established before a signed contrast is assembled. A whole-shell mean would not imply ([\[eq:w\]](main.tex#L100){reference-type="ref" reference="eq:w"}).

# Exact physical channel split

Put $g_x=A_x\beta$. Since $\mathsf P_3$ is orthogonal, $$\left\langle w,g_x\right\rangle=\left\langle \mathsf P_3w,\mathsf P_3g_x\right\rangle+
 \left\langle (I-\mathsf P_3)w,(I-\mathsf P_3)g_x\right\rangle.                            \label{eq:split}$$ There are no mixed terms. Expanding the first term in the orthonormal frame gives the signed cross-Gram formula $$C_3(x)=\sum_{i=0}^2
 \overline{\left\langle z_i,w\right\rangle}\,\left\langle z_i,A_x\beta\right\rangle.             \label{eq:channel}$$ This is the physical counterpart of the phase-typed object isolated in TPC-262: the projection is applied to both actual vectors, not merely to their packet diagonals.

> **Theorem: rank-three physical cross-Gram channel** For every fixed admissible $K$ and every fixed $M>0$, $$|C_3(x)|\ll_{M,K}\frac{x^{5/3}}{(\log x)^{M+3}}.$$

> **Proof** The three source-backed coefficient asymptotics from TPC-257 are $$\left\langle z_i,g_x\right\rangle=-(9\kappa_i/2+o(1))
>        \frac{x^{7/6}}{(\log x)^3},$$ where $$\kappa_0=\frac{\log(32/27)}{\sqrt2},\quad
>  \kappa_1=\frac12\log(3456/3125),\quad
>  \kappa_2=\frac12\log(884736/823543).$$ Combine this with ([\[eq:w\]](main.tex#L100){reference-type="ref" reference="eq:w"}) in ([\[eq:channel\]](main.tex#L116){reference-type="ref" reference="eq:channel"}) and sum three fixed terms. The powers multiply as $$x^{1/2}x^{7/6}=x^{5/3},$$ and the logarithmic orders add to $M+3$. The finitely many $o(1)$ factors are absorbed after $M,K$ are fixed and $x$ is sufficiently large.

# What the theorem does not pay

The second term in ([\[eq:split\]](main.tex#L110){reference-type="ref" reference="eq:split"}) is $$C_\perp(x)=\left\langle (I-\mathsf P_3)w,(I-\mathsf P_3)A_x\beta\right\rangle.$$ TPC-263 supplies no estimate for it. This is not a cosmetic qualification: TPC-260 showed that finite packet marginals and a finite list of null/Haar coordinates do not identify a four-packet residual. The present paper pays the rank-three channel while preserving the missing complement as a named object for the next attack.

The channel is logarithmic only. For any fixed $\eta>0$, $$\frac{x^{5/3}/(\log x)^{M+3}}{x^{5/3-\eta}}
 =\frac{x^\eta}{(\log x)^{M+3}}\longrightarrow\infty.$$ Thus no fixed-power credit is generated, and TPC-261’s strict $1/400$ endpoint obligation remains unpaid.

# Finite certificate and route evaluation

The release certificate checks exact rational frame geometry on 48 mixed clocks, an independent Gaussian-rational projection fixture with a nonzero residual, and the exponent ledger $$\frac12+\frac76=\frac53,\qquad
 \frac53-\frac{1997}{1200}=\frac1{400}.$$ These checks validate identities and provenance only; they do not numerically prove the maximal Type-I theorem or the PNT input.

| Item                                  | Status                                   |
|:--------------------------------------|:-----------------------------------------|
| Rank-three frame and projection       | proved exactly                           |
| Three hybrid frame moments            | source-backed, arbitrary fixed log power |
| Three adjoint frame coefficients      | source-backed from TPC-257               |
| Rank-three physical cross-Gram        | proved source-backed, log-only           |
| Orthogonal residual                   | open                                     |
| Fixed-power credit                    | 0                                        |
| Arithmetic $L^2$, Gate B, twin primes | none / open                              |

: TPC-263 claim firewall.

# Conclusion

The natural next question is now sharply localized: estimate the orthogonal complement after the rank-three logarithmic channel has been removed, or find an explicit residual obstruction. The reusable chain is $$\begin{gathered}
 \text{rank-three Haar frame}\to\text{blockwise hybrid control}\to\\
 \text{adjoint asymptotics}\to\text{exact projection split}\to\\
 \text{logarithmic channel}+\text{residual firewall}.
\end{gathered}$$ The named Session Route-A/Route-B evaluator files are absent from this checkout; the proof package, theorem ledger, certificate, bridge checker, and `AGENTS.md` are the available fail-closed authority.

# References

9 L. Wang, “Source-backed rank-midpoint hybrid-mean closure,” TPC-254 project artifact, 2026. L. Wang, “Four-block Haar lift and a transverse norm floor,” TPC-257 project artifact, 2026. L. Wang, “Literal signed reduced-residue operator and phase-character firewall,” TPC-262 project artifact, 2026.

<!-- SOURCE_BODY_END -->
