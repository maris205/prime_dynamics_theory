# TPC-264: Orthogonal-Residual Schur Firewall

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University of Science and Technology; Wuhan, China
- Source date: August 26, 2026
- Source repository commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding rank-three physical cross-Gram channel controls a projected part of the literal V59 coupling but leaves an orthogonal residual. This paper gives an exact finite-dimensional Schur classification of that residual. If the projected vectors and both residual norms are fixed, the residual inner product is a closed disk when the complement has dimension at least two, a circle when the complement is one-dimensional, and a singleton in the degenerate cases. The full coupling is the corresponding translate by the projected inner product. The result is sharp: exact Gaussian-rational witnesses realize the disk endpoints, its interior, and the dimension transition. A synthetic endpoint-scale family has radius $x^{5/3}$, so rank-three logarithmic control plus norm-only residual data cannot pay a fixed-power saving. This is a structural firewall, not a literal prime-shell counterexample.

<!-- SOURCE_BODY_BEGIN -->

# Scope and motivation

We use the conjugate-linear-first-slot convention $$\left\langle u,v\right\rangle=\sum_j\overline{u_j}v_j.$$ The current Route-B object is a common-clock coupling $ip{w}{g_x}$, where $g_x=A_x\beta$. TPC-263 constructs an exact rank-three source frame and proves a source-backed bound for $$C_3(x)=\left\langle P_3w,P_3g_x\right\rangle
       =O_{M,K}\!\left(\frac{x^{5/3}}{(\log x)^{M+3}}\right).$$ The exact identity still contains $$C_\perp(x)=\left\langle (I-P_3)w,(I-P_3)g_x\right\rangle.$$ The purpose of this paper is not to guess an estimate for $C_\perp$. Instead, we determine the complete set of values compatible with the data already exposed by the projection. This makes the missing theorem explicit.

There are two reasons to isolate this finite question. First, a positive semidefinite Gram constraint is an exact source of information, and its sharp boundary should be recorded rather than replaced by a loose Cauchy bound. Second, the dimension of the unobserved complement changes the geometry: in dimension one the residual has fixed modulus, whereas in dimension two it can also cancel completely. These are different obstructions for a future literal argument.

Our contributions are:

1.  an exact projection-plus-residual decomposition;

2.  a Schur feasible-set theorem with a complete dimension split;

3.  a translated disk/circle/singleton description for the full scalar; and

4.  an endpoint-scale structural witness and a precise $1/400$ consequence.

All finite vectors below are audit objects. They do not model a new prime distribution law, and no finite witness is treated as asymptotic evidence.

# The projected and residual data

Let $\mathcal H$ be a complex Hilbert space and let $P$ be an orthogonal projection. For two vectors $w,g\in\mathcal H$, define $$p=Pw,\qquad q=Pg,\qquad u=(I-P)w,\qquad v=(I-P)g.$$ Then $p,q\in\operatorname{ran}(P)$ and $u,v\in\ker(P)$. We call $$a=\left\lVert u\right\rVert,\qquad b=\left\lVert v\right\rVert,\qquad c=\left\langle p,q\right\rangle$$ the residual radii and projected center. The unresolved scalar is $$z=\left\langle u,v\right\rangle.$$

> **Lemma: orthogonal splitting** For every $w,g$ and every orthogonal projection $P$, $$\left\langle w,g\right\rangle=c+z.
>  \label{eq:split}$$

> **Proof** Write $w=p+u$ and $g=q+v$. The mixed terms vanish because the range and kernel of an orthogonal projection are orthogonal: $$\left\langle p,v\right\rangle=\left\langle u,q\right\rangle=0.$$ Expanding the inner product gives [\[eq:split\]](main.tex#L107){reference-type="eqref" reference="eq:split"}.

The projected center $c$ is the quantity controlled by TPC-263. The question is how much freedom remains in $z$ after $a$ and $b$ are also specified.

# The Schur feasible set

> **Definition: residual Gram matrix** For $z\in\mathbb C$ and nonnegative $a,b$, set $$\Gamma(a,b;z)=
>  \begin{pmatrix}
>   a^2 & z\\
>   \overline z & b^2
>  \end{pmatrix}.$$ The set of $z$ for which this matrix is positive semidefinite is the Schur feasible set at radii $(a,b)$.

> **Theorem: exact Schur feasible set** Let $m=\dim\ker(P)$, allowing $m=\infty$. With $a,b,c,z$ as above, the possible residual values, when $p,q,a,b$ are fixed, are as follows.
>
> 1.  If $m\geq2$, the set is the closed disk $$\{z\in\mathbb C:\ |z|\leq ab\}.$$
>
> 2.  If $m=1$ and $ab>0$, the set is the circle $$\{z\in\mathbb C:\ |z|=ab\}.$$
>
> 3.  If $m=0$ or $ab=0$, the set is the singleton $\{0\}$.
>
> Consequently, the possible full scalars are obtained by translating these sets by $c$.

> **Proof** The residual Gram matrix of $u,v$ is exactly $\Gamma(a,b;z)$, hence it is positive semidefinite. Its determinant is nonnegative, so $$a^2b^2-|z|^2\geq0.
>  \label{eq:schur}$$ This proves the upper bound in every dimension.
>
> Suppose first that $m\geq2$ and $a,b>0$. Choose orthonormal vectors $e_1,e_2\in\ker(P)$. Given any $z$ with $|z|\leq ab$, put $$r=\frac{|z|}{ab},\qquad z=ab r e^{i\theta},$$ and define $$u=a e_1,\qquad
>  v=b\bigl(r e^{i\theta}e_1+\sqrt{1-r^2}\,e_2\bigr).$$ Then $\left\lVert u\right\rVert=a$, $\left\lVert v\right\rVert=b$, and the chosen inner-product convention gives $\left\langle u,v\right\rangle=z$. Thus every point of the disk is attained.
>
> If $m=1$, write $u=\alpha e$ and $v=\beta e$ for a unit vector $e$. Fixed norms give $|\alpha|=a$ and $|\beta|=b$, so $$|\left\langle u,v\right\rangle|=|\overline\alpha\beta|=ab.$$ Varying the relative phase of $\alpha$ and $\beta$ realizes every point on the circle. If $m=0$, both residual vectors vanish. If $a=0$ or $b=0$, the same conclusion follows immediately from Cauchy–Schwarz. Finally, [\[eq:split\]](main.tex#L107){reference-type="eqref" reference="eq:split"} translates the residual set by $c$.

> **Remark** The inequality [\[eq:schur\]](main.tex#L161){reference-type="eqref" reference="eq:schur"} is often called the $2\times2$ Schur or Gram condition. The theorem is stronger than an upper bound: it proves that the condition is sufficient in complement dimension at least two. Thus no hidden finite-dimensional constraint has been left in the disk statement.

# An exact finite audit

For a concrete fixture take an ambient space with five coordinates and let $P$ keep the first three. Fix $$p=(1,0,0),\qquad q=(2+i,0,0),\qquad a=\frac32,\qquad b=2.$$ Then $c=\left\langle p,q\right\rangle=2+i$ and the Schur radius is $ab=3$. In the last two coordinates, use the following residual pairs: $$\begin{array}{c|c|c|c}
 \text{label}&u&v&\left\langle u,v\right\rangle\\ \midrule
 \text{plus}&(\frac32,0)&(2,0)&3\\
 \text{minus}&(\frac32,0)&(-2,0)&-3\\
 \text{zero}&(\frac32,0)&(0,2)&0\\
 \text{quarter-turn}&(\frac32,0)&(2i,0)&3i
\end{array}$$ Each row has the same residual norms. The first and second rows are the two Schur boundary endpoints, the third is an interior point, and the fourth demonstrates phase freedom. Their full scalars are respectively $5+i$, $-1+i$, $2+i$, and $2+4i$.

The release certificate recomputes these values with rational arithmetic. It also checks a one-dimensional complement: the zero residual is rejected from the positive-radius circle, while the three boundary phases are accepted. A zero residual norm collapses the classification in every complement dimension. This finite audit is deliberately small enough to inspect line by line and large enough to exercise every branch of the theorem.

# Endpoint-scale consequence

The rank-three channel provides a center that is small in fixed logarithmic powers. The Schur theorem says that this fact is not enough if the residual radius is left at the natural baseline scale. Consider the synthetic choice $$a=b=x^{5/6},\qquad ab=x^{5/3}.$$ The disk contains both $z=x^{5/3}$ and $z=-x^{5/3}$. For any center satisfying $|c|=O(x^{5/3}/(\log x)^M)$, one of these choices has $$|c+z|\geq x^{5/3}-|c|.$$ Since $x^\delta/(\log x)^M\to\infty$ for every fixed $\delta>0$, this quantity cannot be forced to $O(x^{5/3-\delta})$ from the declared data alone.

The inherited endpoint budget is $$\frac53-\frac{1997}{1200}=\frac1{400}.$$ Therefore a future literal theorem needs at least one of the following:

1.  a residual-radius estimate $$\left\lVert (I-P_3)w\right\rVert\,\left\lVert (I-P_3)g_x\right\rVert
           \ll x^{5/3-\delta},\qquad \delta>\frac1{400},$$ after all reassembly losses; or

2.  a direct signed estimate for $C_\perp$ with an effective saving greater than $1/400$.

The first is a norm theorem and the second is a phase/cross-Gram theorem. The Schur firewall shows why neither can be replaced by a statement about the projected channel alone.

# Claim firewall and route consequence

| Object                                     | Status                  |
|:-------------------------------------------|:------------------------|
| Schur disk/circle/singleton classification | `PROVED_EXACT`          |
| Finite Gaussian-rational witnesses         | `NUMERICALLY_CERTIFIED` |
| Literal V59 residual radius or phase       | `OPEN`                  |
| Fixed-power credit in this paper           | $0$                     |
| Arithmetic $L^2$ and full Gate B           | `NONE / OPEN`           |
| Twin-prime conclusion                      | `NONE`                  |
| Literal growing-shell counterexample       | `NONE`                  |

The phrase “Orthogonal-Residual Schur Firewall” records the exact role of the result: it blocks an invalid promotion from a paid projection to a paid full coupling. It does not block a future literal estimate. The next natural research object is the actual V59 residual radius or its signed phase, with the hard window, unit masks, deleted diagonal, and common clock retained.

# Conclusion

TPC-264 turns the unresolved term in TPC-263 into a complete finite geometry. The data $(p,q,a,b)$ determine a disk, circle, or singleton according to the unobserved dimension, and this description is sharp. At endpoint scale the disk has the full baseline radius unless a new literal theorem shrinks it or controls its phase. The result is therefore a reusable obstruction and a minimal specification for the next bridge, while all arithmetic and twin-prime claims remain open.

# References

9 L. Wang, “Rank-three physical cross-Gram channel,” TPC-263 project, repository release, 2026.

R. A. Horn and C. R. Johnson, *Matrix Analysis*, Cambridge University Press, 2012.

J. B. Conway, *A Course in Functional Analysis*, Springer, 1990.

<!-- SOURCE_BODY_END -->
