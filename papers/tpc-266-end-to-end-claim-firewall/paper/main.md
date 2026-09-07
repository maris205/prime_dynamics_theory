# TPC-266: A Typed End-to-End Claim Firewall\ for the Residual Budget Chain

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`
- Converter: `source-markdown-audit-v2`

## Abstract

The recent Bridge-B sequence TPC-263–265 leaves a precise interface question: can a source-backed fixed-log center channel, an exact Schur residual set, and a radial endpoint envelope be composed without silently creating a fixed-power estimate? We define a typed endpoint compiler and prove its soundness. A lane is paid only when it is a genuine power or signed-phase bound whose effective saving exceeds the inherited gap $\Delta_*=1/400$. We also prove two firewalls: fixed logarithmic decay cannot be promoted to a positive power saving, and deleting the Schur residual is unsound because the aligned endpoint has size $|c|+R$. An exact six-state adversarial matrix (strict, log-only, missing, borderline, subcritical, and deleted-residual) is independently replayed with rational arithmetic. This is a structural composition result; the literal V59 radius and phase, arithmetic $L^2$, and the twin-prime conjecture remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

We work on the common V59 clock and use the conjugate-linear-first-slot convention $$\left\langle u,v\right\rangle=\sum_j\overline{u_j}v_j.$$ TPC-263 established a source-backed rank-three channel of the form $$\left\langle w,g_x\right\rangle=C_3(x)+C_\perp(x), \qquad g_x=A_x\beta,$$ with, for fixed $M$ and $K$, $$|C_3(x)|\ll_{M,K}x^{5/3}(\log x)^{-M-3}.$$ TPC-264 made the remaining orthogonal cross-Gram explicit: after the projected data and residual norms are fixed, its feasible set is a disk, circle, or singleton according to the dimension of the complement. TPC-265 then computed the sharp radial support of that set and translated it into an endpoint budget.

The present paper is a hostile audit of the composition itself. It records which type of evidence may flow from one stage to the next and which tempting shortcuts are invalid. In particular, the paper does not treat an arbitrary small numerical slope as a theorem and does not remove an unestimated orthogonal component.

Our contributions are:

1.  an exact typed compiler for the center and Schur-radius lanes;

2.  a soundness theorem and an exact failure classification;

3.  a fixed-log non-promotion and residual-retention firewall; and

4.  a reproducible rational certificate with an independent hostile replay.

# The three-stage interface

Let $P$ be the rank-three source projection. With $$p=Pw,\quad q=Pg_x,\quad u=(I-P)w,\quad v=(I-P)g_x,$$ orthogonality gives the exact split $$\left\langle w,g_x\right\rangle=\left\langle p,q\right\rangle+\left\langle u,v\right\rangle=:c_x+z_x.
 \label{eq:split}$$ If $a=\left\lVert u\right\rVert$ and $b=\left\lVert v\right\rVert$, the residual Gram matrix is positive semidefinite and hence $|z_x|\leq ab$. In complement dimension at least two, all points of the disk $|z_x|\leq ab$ are realizable; in dimension one the boundary circle is realizable. We denote the residual radius by $$R_x=ab.$$

The information types carried by the three stages are different:

| Stage   | Output type                            | What it certifies                                  |
|:--------|:---------------------------------------|:---------------------------------------------------|
| TPC-263 | $\mathrm{FIXED\mathchar`\_LOG}$ center | fixed $M$ logarithmic decay of $C_3$               |
| TPC-264 | Schur set                              | feasible residual geometry and radius symbol $R_x$ |
| TPC-265 | radial envelope                        | $\sup|c_x+z_x|=|c_x|+R_x$                          |
| TPC-266 | budget decision                        | typed payment or fail-closed status                |

> **Remark** The word “type” is substantive. A statement of type $\mathrm{FIXED\mathchar`\_LOG}$ has a quantifier with fixed $M$; a statement of type $\mathrm{POWER}$ has a positive power saving. No conversion between the two is permitted without a new theorem.

# Typed endpoint compiler

The common exponents are $$E_0=\frac53, \qquad E_*=\frac{1997}{1200}, \qquad
 \Delta_*=E_0-E_* = \frac1{400}.$$ For a lane with saving $\delta$ and reassembly loss $\lambda$, set $$\sigma=\delta-\lambda.$$

> **Definition: paid lane** A lane is paid if its type is $\mathrm{POWER}$ or $\mathrm{SIGNED\mathchar`\_PHASE}$ and $\sigma>\Delta_*$. A fixed-log, missing, or deleted lane is not paid. The two-lane compiler returns `CLOSED_CONDITIONAL` exactly when both the center and radius lanes are paid and the residual-retained flag is true.

> **Theorem: sound composition** Suppose $$T_x=c_x+z_x, \qquad |z_x|\leq R_x,$$ and the residual is retained. If, for every sufficiently small $\varepsilon>0$, $$\begin{aligned}
>  |c_x|&\leq C_c(\varepsilon)x^{E_0-\delta_c+\lambda_c+\varepsilon},\\
>  R_x&\leq C_r(\varepsilon)x^{E_0-\delta_r+\lambda_r+\varepsilon},
>  \label{eq:powerlanes}\end{aligned}$$ with $$\delta_c-\lambda_c>\Delta_*, \qquad
>  \delta_r-\lambda_r>\Delta_*,$$ then $T_x=o(x^{E_*})$.

> **Proof** The radial envelope from TPC-265 gives $$|T_x|\leq |c_x|+|z_x|\leq |c_x|+R_x.$$ Let $\eta>0$ be smaller than half the two strict gaps $\delta_c-\lambda_c-\Delta_*$ and $\delta_r-\lambda_r-\Delta_*$. Choose $\varepsilon<\eta$ in [\[eq:powerlanes\]](main.tex#L151){reference-type="eqref" reference="eq:powerlanes"}. Both terms are then $O(x^{E_* -\eta})$, after possibly shrinking $\eta$, and their sum is $o(x^{E_*})$. This is exactly the compiler’s paid-lane decision.

> **Theorem: strict threshold and failure side** If a lane has effective saving equal to $\Delta_*$, its exponent is only at the target power (up to $\varepsilon$). If its effective saving is smaller, the exponent is at or above the target scale. Therefore the typed compiler cannot return a strict target payment in either case without an additional rate factor.

> **Proof** The lane exponent is $E_0-\sigma+\varepsilon=E_*+(\Delta_*-\sigma)+\varepsilon$. Substitution of $\sigma=\Delta_*$ gives the borderline case; substitution of $\sigma<\Delta_*$ gives a nonnegative power excess.

# Two hostile firewalls

> **Theorem: fixed-log non-promotion** For fixed $M$ and every $\delta>0$, $$\frac{x^{E_0}}{(\log x)^M}\not=O(x^{E_0-\delta}).$$ Consequently a fixed-log center or radius estimate carries zero fixed-power credit.

> **Proof** The ratio of the left-hand scale to the proposed power scale is $x^\delta/(\log x)^M$, which tends to infinity. Thus the transition $\mathrm{FIXED\mathchar`\_LOG}\to\mathrm{POWER}(\delta)$ is not a valid interface transition.

> **Theorem: residual-retention firewall** For every $R>0$ and $c\in\mathbb C$, $$\sup_{|z|\leq R}|c+z|=|c|+R.$$ Hence a certificate that retains $c$ but deletes the Schur residual is not sound: the admissible endpoint can exceed the deleted output by the full radius $R$.

> **Proof** The triangle inequality gives the upper bound. Equality is attained by $z=Rc/|c|$ when $c\neq0$, and by any point of modulus $R$ when $c=0$. The deleted output has size $|c|$, so the aligned endpoint creates a gap $R$.

# Exact hostile matrix

The certificate uses $c=2$ and $R=3$. The disk endpoints include the aligned value $5$, the opposite value $-1$, and the cancellation point $0$; the circle has upper edge $5$ and lower edge $1$. Three independent residual lanes with radii $1,2,3$ have Minkowski radius $6$ and upper edge $8$ over the same center. Every value is an exact rational identity.

The six compiler states are shown below. “Strict” uses saving $1/320$; the subcritical row uses $1/320-1/1200=11/4800$.

<div id="tab:matrix">

| State            | Typed input                        | Decision                    |
|:-----------------|:-----------------------------------|:----------------------------|
| Strict pair      | power center + signed-phase radius | `CLOSED_CONDITIONAL`        |
| Fixed-log center | fixed-log center + power radius    | `OPEN_LOG_CENTER`           |
| Missing radius   | power center + missing radius      | `OPEN_RADIUS`               |
| Borderline lane  | one lane has $\sigma=1/400$        | `BORDERLINE`                |
| Subcritical lane | one lane has $\sigma<1/400$        | `INSUFFICIENT`              |
| Deleted residual | retained flag is false             | `UNSOUND_RESIDUAL_DELETION` |

: The exact six-state end-to-end firewall.

</div>

> **Theorem: minimal interface classification** Relative to the declared lane interface, the six decisions in Table [1](main.tex#L246){reference-type="ref" reference="tab:matrix"} are exact. In particular, no row other than the strict pair can be relabelled as a closed conditional endpoint proof.

> **Proof** The strict row is Theorem 1. The fixed-log row is rejected by the fixed-log non-promotion theorem, and the deleted row by the residual-retention theorem. A missing radius supplies no bound for the second summand. At equality the exponent is exactly the target power before the arbitrary $\varepsilon$ loss; below equality it is worse. The rational fixture computations attain the displayed endpoint and exponent comparisons, so each failure label is witnessed rather than inferred from a parser convention.

# Route consequence and limitations

The audited chain has the following current typed state: $$\begin{aligned}
 \text{center}&=\mathrm{FIXED\mathchar`\_LOG},\\
 \text{residual}&=\text{Schur set with radius OPEN},\\
 \text{endpoint}&=\text{radial envelope}.
 \end{aligned}$$ It is therefore correctly open for the literal V59 endpoint. TPC-266 pays no new arithmetic lane; it prevents invalid credit from being assigned to one. The next legitimate input is a literal residual-radius estimate or a signed phase theorem with effective saving strictly greater than $1/400$ after all losses. Such an input must preserve the hard window, unit masks, signs, and the deleted diagonal inherited by the previous interfaces.

| Claim                                  | Status                              |
|:---------------------------------------|:------------------------------------|
| Typed composition and six-state matrix | `PROVED_EXACT`                      |
| Fixed-log non-promotion                | `PROVED_EXACT`                      |
| Residual retention                     | `PROVED_EXACT`                      |
| Strict endpoint threshold              | $1/400$ (exact interface threshold) |
| Literal V59 radius and phase           | `OPEN`                              |
| Arithmetic $L^2$ and full Gate B       | `NONE / OPEN`                       |
| Twin-prime conclusion                  | `NONE`                              |

# Conclusion

The TPC-263–265 interfaces compose into a typed, fail-closed endpoint compiler. Its positive theorem is conditional and exact; its negative results are equally important: fixed logarithms do not buy power savings, and the Schur residual cannot be erased. The hostile matrix makes these rules machine-checkable while leaving the actual arithmetic bottleneck visible.

# References

9 L. Wang, “Schur radius to endpoint-budget compiler,” TPC-265 project, repository release, 2026.

L. Wang, “Orthogonal-residual Schur firewall,” TPC-264 project, repository release, 2026.

L. Wang, “Rank-three physical cross-Gram channel,” TPC-263 project, repository release, 2026.

R. A. Horn and C. R. Johnson, *Matrix Analysis*, Cambridge University Press, 2012.

<!-- SOURCE_BODY_END -->
