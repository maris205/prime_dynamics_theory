# Source-Native Masked $L^2$ Polarization:\ Exact Operator Attachment and Finite Firewall

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 3 September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

The source-native residual $\beta(t)=\Lambda(t+2)-b^{(2)}(t)$ has so far been studied either before applying the literal divisibility masks or through operator-only envelopes. We attach the declared finite residual to the physical masked prime-shell operator and expose the missing cross term. For every finite row the identity $\|A\beta\|_2^2=\|A\Lambda\|_2^2+\|Ab\|_2^2-2\langle A\Lambda,Ab\rangle$ is exact, with a corresponding Cauchy envelope. On a fresh low-origin panel of 216 law-level rows, all four predeclared sign laws have positive output alignment. For the all-plus law the normalized alignment coefficient ranges from $0.6929$ to $0.9963$, whereas the source-level coefficient ranges only from $0.3957$ to $0.4358$. The operator therefore changes the polarization geometry substantially. This is a finite attachment and a scoped obstruction to source-only promotion; it supplies no asymptotic arithmetic estimate, power credit, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

TPC-352 subjected a reciprocal-shell finite repair to a disjoint holdout and found a high-shell floor below its balanced parent. That branch is frozen. The remaining local question is narrower: can the actual source-native vector be attached to the literal masked operator without silently replacing either the source or the masks? The answer here is yes at the finite algebraic level, but the resulting cross term is a new object that must be controlled.

Throughout, all conclusions are explicitly classified as finite, declared model statements or numerically certified finite observations. In particular, the finite V59 convention used below is not identified with an asymptotic twin-prime formula.

# Finite object and exact identities

Let $I$ be a finite interval and let $S_Q=\{p: p$ prime, $Q<p\leq 2Q\}$. For a sign law $e$ define the literal operator $$A_e(u,t)=\sum_{p\in S_Q}e_p\,1_{u\ne t}1_{p\nmid ut}
 p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(1_{u\equiv t\pmod p}-\frac1{p-1}\right).
 \label{eq:operator}$$ Both endpoint masks in $1_{p\nmid ut}$ are retained. The source is the finite declared model $$\beta=\Lambda-b,\qquad
 b(t)=2C_2,1_{2\nmid t}\prod_{p\mid t,\ p>2}\frac{p-1}{p-2},
 \label{eq:source}$$ with the inherited finite Euler-tail enclosure and logarithm midpoint rule.

#### Proposition 1 (operator polarization).

For any real finite matrix $A$ and finite vectors $L,b$, putting $\beta=L-b$ gives $$\|A\beta\|_2^2=\|AL\|_2^2+\|Ab\|_2^2-2\langle AL,Ab\rangle.
 \label{eq:polar}$$ This follows by expanding the finite Euclidean square; no limit or interchange is used.

Write $E_L=\|AL\|_2^2$, $E_b=\|Ab\|_2^2$, and, when their sum is nonzero, $$\kappa_A=\frac{2\langle AL,Ab\rangle}{E_L+E_b},qquad
 R_A=\frac{\|A\beta\|_2^2}{E_L+E_b}.
 \label{eq:kappa}$$ Then $R_A=1-\kappa_A$. Cauchy–Schwarz gives the exact finite envelope $$\frac{(\sqrt{E_L}-\sqrt{E_b})^2}{E_L+E_b}
 \leq R_A\leq
 \frac{(\sqrt{E_L}+\sqrt{E_b})^2}{E_L+E_b}.
 \label{eq:cauchy}$$ The envelope is an interface for a specified finite source and operator, not a source-uniform operator theorem.

# Protocol and independent audit

The panel was fixed before evaluating responses:

|                          |                                                          |
|:-------------------------|:---------------------------------------------------------|
| origins                  | $6001,8001,10001$                                        |
| source counts            | $256,512,1024$                                           |
| shell anchors            | $Q=24,54,80$                                             |
| kernel exponents         | $s=1,2$                                                  |
| sign laws                | all-plus, alternating-index, mod-4 character, half split |
| height and source cutoff | $H=66$, $50000$                                          |

The Cartesian product has $3\cdot3\cdot3\cdot2\cdot4=216$ rows. The producer uses Decimal/Fraction source enclosures followed by a float64 matrix replay. A separate checker rebuilds the source with a trial sieve and accumulates shell primes in reverse order. It does not import the producer. Eight in-memory mutation tests verify the certificate firewall.

An exact fourteen-point anchor on $[6001,6014]$ and shell $\{5,7\}$ uses two fixed rational vectors. Its four reduced-fraction digests are independently recomputed, and equation [\[eq:polar\]](main.tex#L76){reference-type="eqref" reference="eq:polar"} holds exactly. The largest floating point identity residual over the numerical panel is $5.2154064178466797\times10^{-7}$.

# Results

Table [1](main.tex#L134){reference-type="ref" reference="tab:summary"} reports the output coefficient $\kappa_A$ and the remaining residual fraction $R_A$. Every row is separated from zero by the declared $10^{-7}$ guard; no row is unresolved.

<div id="tab:summary">

| law               |  rows|  $\kappa_{\min}$|  $\kappa_{\max}$|  $\overline\kappa$|        $R$ range|
|:------------------|-----:|----------------:|----------------:|------------------:|----------------:|
| all-plus          |    54|          .692912|          .996268|            .895612|  .003732–.307088|
| alternating-index |    54|          .013867|          .711596|            .189627|  .288404–.986133|
| mod-4 character   |    54|          .007749|          .739230|            .319670|  .260770–.992251|
| half split        |    54|          .062606|          .733296|            .354920|  .266704–.937394|

: Operator-level polarization on 54 rows per law.

</div>

The source coefficient, computed before applying $A_e$, lies in $[0.3957036548,0.4358137670]$ on all 216 rows. For all-plus, the output coefficient is strictly larger than the source coefficient on every row, with output-minus-source range $[0.2800699287,0.5933775836]$. For the other laws the corresponding deltas range across both signs: alternating-index $[-0.3954689750,0.2757819450]$, mod-4 $[-0.4106327201,0.3243854834]$, and half split $[-0.3483020559,0.3184512854]$. Thus the positive all-plus output alignment is a finite observation, not a law-independent source theorem.

The output cosine for all-plus is $0.723300$–$0.996291$; for the other laws the minima are respectively $0.055472$, $0.034838$, and $0.148569$. These values make the geometry visible without replacing the exact identity: the masked operator can align the two source components much more strongly than their source-space inner product suggests.

# Claim firewall and route decision

The exact claims are the finite operator identity and Cauchy envelope. The declared-model claim is the literal source attachment. The numerical claims are the 216-row replay, positive alignment on $216/216$, and the ranges in Table [1](main.tex#L134){reference-type="ref" reference="tab:summary"}. The narrow obstruction is that source-level polarization does not determine operator-level polarization; consequently a source-only $L^2$ ledger cannot be promoted silently to a masked estimate.

No source-uniform arithmetic $L^2$ bound, uniform masked-operator bound, canonical sign law, strict $1/400$ payment, fixed-power credit, Route-B reassembly, or twin-prime endpoint follows. The Session-named Route-A and Route-B evaluator files are absent from this checkout, so the local Bridge-B is fail-closed fallback evidence rather than an official evaluator pass. The next admissible test is a higher-origin source panel or a position-aware masked bound; adding the same finite panel again would not pay the open theorem.

# References

1 Standard finite-dimensional Cauchy–Schwarz and polarization identities are used only in the elementary form displayed in equations [\[eq:polar\]](main.tex#L76){reference-type="eqref" reference="eq:polar"}–[\[eq:cauchy\]](main.tex#L92){reference-type="eqref" reference="eq:cauchy"}.

<!-- SOURCE_BODY_END -->
