# TPC-265: Schur Radius to Endpoint-Budget Compiler

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-264 identified the exact Schur feasible set of the orthogonal residual left by the rank-three physical channel. We now compile that finite geometry into the endpoint ledger. For a projected center $c$ and a residual disk of radius $R$, the worst-case reassembled scalar has the sharp value $|c|+R$, while the disk lower edge is $\max(|c|-R,0)$. The same upper edge holds for a free-phase circle. Combining the two resulting lanes with the V59 baseline $E_0=5/3$ and target $E_*=1997/1200$ gives the exact strict payment threshold $1/400$ for each power-saving lane. Fixed logarithmic suppression has zero fixed-power credit. This is an interface theorem and obstruction: it does not estimate the literal V59 residual or prove a twin-prime statement.

<!-- SOURCE_BODY_BEGIN -->

# Scope and motivation

We use the conjugate-linear-first-slot convention $$\left\langle u,v\right\rangle=\sum_j\overline{u_j}v_j.$$ On the common V59 clock, TPC-263 decomposes the physical coupling as $$\left\langle w,g_x\right\rangle=C_3(x)+C_\perp(x),\qquad g_x=A_x\beta,$$ where the rank-three term satisfies, for fixed $M,K$, $$|C_3(x)|\ll_{M,K}\frac{x^{5/3}}{(\log x)^{M+3}},$$ and $C_\perp$ is an exact orthogonal-complement cross-Gram. TPC-264 showed that, after fixing the projected vectors and residual norms, this cross-Gram is a point in a disk (or in its dimension-one degeneration).

The present paper answers the next bookkeeping question. If the residual is only known through that feasible set, what is the largest possible full scalar? The answer is not a new Cauchy estimate; it is an exact support calculation. This matters because endpoint arguments sometimes treat a possible phase cancellation as though it were paid by a norm bound. The support calculation separates those two kinds of information.

Our contributions are:

1.  a sharp radial envelope for Schur disks and circles;

2.  a two-lane endpoint compiler with the exact strict threshold $1/400$;

3.  a logarithmic/power firewall for both the center and radius lanes; and

4.  exact rational endpoint and multi-lane audits.

All conclusions about the literal V59 residual are explicitly left open.

# Schur geometry as an endpoint set

Let $P$ be an orthogonal projection on a complex Hilbert space and write $$p=Pw,\quad q=Pg,\quad u=(I-P)w,\quad v=(I-P)g.$$ Set $c=\left\langle p,q\right\rangle$ and $z=\left\langle u,v\right\rangle$. The orthogonal splitting from TPC-264 is $$\left\langle w,g\right\rangle=c+z.
 \label{eq:split}$$ If $a=\left\lVert u\right\rVert$ and $b=\left\lVert v\right\rVert$, the residual Gram matrix is $$\begin{pmatrix}a^2&z\\ \overline z&b^2\end{pmatrix}\succeq0,
 \qquad |z|\leq ab.$$ When the complement has dimension at least two, every point of this disk is realizable with the same $p,q,a,b$. We therefore write its radius as $$R=ab,qquad \mathcal D(c,R)=\{c+z:|z|\leq R\}.$$ The one-dimensional complement gives the boundary circle, and a zero complement or zero residual norm gives a singleton.

> **Remark** The use of a disk here is conditional on the fixed residual norms. It does not say that the actual V59 residual norms equal a proposed scale. The point of the notation is to make the missing information visible in the endpoint ledger.

# Sharp radial support

> **Theorem: disk radial envelope** For $c\in\mathbb C$ and $R\geq0$, $$\begin{aligned}
>  \sup_{y\in\mathcal D(c,R)}|y|&=|c|+R, \label{eq:upper}\\
>  \inf_{y\in\mathcal D(c,R)}|y|&=\max\{|c|-R,0\}. \label{eq:lower}\end{aligned}$$

> **Proof** The triangle inequality gives $|c+z|\leq|c|+R$. If $c\neq0$, choose the aligned residual $z=Rc/|c|$; if $c=0$, any boundary point gives equality. This proves [\[eq:upper\]](main.tex#L114){reference-type="eqref" reference="eq:upper"}. The reverse triangle inequality gives $|c+z|\geq\bigl||c|-|z|\bigr|$. If $|c|\geq R$, choose the opposite boundary point $z=-Rc/|c|$. If $|c|<R$, choose $z=-c$, which lies in the disk. Both choices attain [\[eq:lower\]](main.tex#L115){reference-type="eqref" reference="eq:lower"}.

> **Theorem: circle upper edge** For the free-phase circle $$\mathcal C(c,R)=\{c+z:|z|=R\},$$ $$\sup_{y\in\mathcal C(c,R)}|y|=|c|+R,
>  \qquad
>  \inf_{y\in\mathcal C(c,R)}|y|=\bigl||c|-R\bigr|.$$

> **Proof** The aligned and opposite boundary points used above both lie on the circle. The triangle and reverse-triangle inequalities are therefore sharp on the circle as well.

The first theorem is the key obstruction. If a residual phase is not controlled, the aligned point is admissible and the radius must be paid in a uniform upper bound. A phase theorem can change the feasible set, but it is additional information rather than a consequence of positive semidefiniteness.

# The endpoint-budget compiler

Fix the inherited exponents $$E_0=\frac53,\qquad E_*=\frac{1997}{1200},\qquad
 \Delta_*=E_0-E_* = \frac1{400}.$$ Suppose the center and radius have power bounds $$\begin{aligned}
 |c_x|&\leq C_c(\varepsilon)x^{E_0-\delta_c+\lambda_c+\varepsilon},\\
 R_x&\leq C_r(\varepsilon)x^{E_0-\delta_r+\lambda_r+\varepsilon}.
 \label{eq:lanes}\end{aligned}$$

> **Theorem: Schur-derived two-lane compiler** If both effective savings satisfy $$\delta_c-\lambda_c>\Delta_*\quad\text{and}\quad
>  \delta_r-\lambda_r>\Delta_* ,
>  \label{eq:strict}$$ then every scalar in the disk feasible set is $o(x^{E_*})$. If either effective saving equals $\Delta_*$, that lane is only power-level borderline; if either is smaller, the displayed hypotheses do not close the target.

> **Proof** By [\[eq:upper\]](main.tex#L114){reference-type="eqref" reference="eq:upper"}, every admissible scalar has modulus at most $|c_x|+R_x$. Let $\eta$ be smaller than half the two strict margins in [\[eq:strict\]](main.tex#L170){reference-type="eqref" reference="eq:strict"}, and choose $\varepsilon$ smaller than $\eta$. Each term in [\[eq:lanes\]](main.tex#L162){reference-type="eqref" reference="eq:lanes"} is then $O(x^{E_*-\eta})$, so their sum is $o(x^{E_*})$. At equality the exponent reaches $E_*$, and below equality it exceeds $E_*$; without an additional rate factor neither case gives the required strict little-oh conclusion.

This compiler differs in role from an abstract lane sum: the residual lane is forced by the exact Schur feasible set, and Theorem 1 proves that its radius is the sharp worst-case cost. No norm-only reassembly loss can be silently removed.

# Logarithmic firewall and finite audit

For fixed $M$ and $\delta>0$, $$\frac{x^{E_0}/(\log x)^M}{x^{E_0-\delta}}
 =\frac{x^\delta}{(\log x)^M}\longrightarrow\infty.$$ Thus a fixed-log center or radius estimate has zero fixed-power credit. In particular, TPC-263’s arbitrary fixed-log bound for $C_3$ cannot be entered as a positive $\delta_c$ in the compiler.

The exact certificate uses a real center $c=2$ and radius $R=3$. The disk has supremum $5$ and infimum $0$; its aligned and opposite residuals are $3$ and $-3$, and the cancellation point is $-2$. The free-phase circle has the same supremum and infimum $1$. Three independently free residual lanes with radii $1,2,3$ have Minkowski radius $6$, so their sharp upper edge over the same center is $8$. These are exact rational identities, not floating-point approximations.

| Lane          | Saving $\delta$ | Loss $\lambda$ | Classification |
|:--------------|:---------------:|:--------------:|:--------------:|
| Strict radius |     $1/320$     |       $0$      |     strict     |
| Borderline    |     $1/400$     |       $0$      |   borderline   |
| Loss test     |     $1/320$     |    $1/1200$    |  insufficient  |
| Log-only      |       $0$       |       $0$      | no fixed power |

: Exact endpoint classifications.

# Claim firewall and route consequence

| Object                           | Status                     |
|:---------------------------------|:---------------------------|
| Schur radial envelope            | `PROVED_EXACT`             |
| Two-lane compiler                | `PROVED_EXACT_CONDITIONAL` |
| Strict threshold                 | $1/400$                    |
| Log center/radius credit         | $0$                        |
| Literal V59 radius and phase     | `OPEN`                     |
| Arithmetic $L^2$ and full Gate B | `NONE / OPEN`              |
| Twin-prime conclusion            | `NONE`                     |

The phrase “Schur Radius to Endpoint-Budget Compiler” records an interface, not a completed arithmetic bridge. The next valid task is to estimate the literal residual radius with a fixed-power saving, or to prove a signed phase restriction that replaces the disk support. Either route must retain the common clock, hard window, unit masks, and deleted diagonal.

# Conclusion

The Schur residual is a radius lane. Its exact worst-case contribution is additive with the projected center, and the endpoint ledger therefore sees the sharp cost $|c|+R$. The inherited gap is strictly paid only when each relevant power lane has effective saving greater than $1/400$. Fixed logarithms do not alter that conclusion. TPC-265 consequently supplies a reusable budget compiler and a precise obstruction while leaving the actual V59 arithmetic residual open.

# References

9 L. Wang, “Orthogonal-residual Schur firewall,” TPC-264 project, repository release, 2026.

L. Wang, “Rank-three physical cross-Gram channel,” TPC-263 project, repository release, 2026.

R. A. Horn and C. R. Johnson, *Matrix Analysis*, Cambridge University Press, 2012.

<!-- SOURCE_BODY_END -->
