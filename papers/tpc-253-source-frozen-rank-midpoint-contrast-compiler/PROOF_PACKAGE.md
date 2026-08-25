# Proof Package

## Claim

Let $x>0$ be real and let
$I_x=(x/2,x]\cap\mathbb Z=\{n_1<\cdots<n_N\}$ with $N\geq2$. Define

$$
\ell=\lfloor N/2\rfloor,\qquad r=N-\ell,
$$

$L=\{n_1,\ldots,n_\ell\}$, $R=I_x\setminus L$,

$$
\rho^2=\frac{\ell r}{N},\qquad
z=\rho\left(\frac{\mathbf1_L}{\ell}-\frac{\mathbf1_R}{r}\right).
$$

With an inner product conjugate-linear in the first slot, this source-only
split has the exact normalization, projector, integer-threshold,
partial-sum, longitudinal/transverse covariance, within-child, literal
TPC-247 kernel, and safe-adjoint identities stated in the frozen TPC-253
theorem. The constant and signed controls are exact nonliteral finite
examples. No sign or arithmetic conclusion is included in the claim.

## Status

`PROVABLE AS STATED`

Project status:

```text
PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER
```

## Assumptions

- $x>0$ is real and $N=\#I_x\geq2$.
- Coordinates are ordered increasingly before the split is formed.
- $L,R$ are selected before $\beta,w,A_x\beta$, margins, and signs are
  inspected.
- The inner product is conjugate-linear in its first slot.
- $g=A_x\beta$ and $C_x=\langle w,g\rangle$.
- The literal TPC-247 definitions of $H,Q,\mathcal Q_x,K_H,\beta,w,A_x$ are
  retained.

## Notation

Let

$$
h=\frac{\mathbf1_L}{\ell}-\frac{\mathbf1_R}{r},\qquad z=\rho h.
$$

For $J\subset I_x$, write $S_f(J)=\sum_{n\in J}f(n)$ and
$\mu_f(J)=S_f(J)/|J|$. Let $u_J=|J|^{-1/2}\mathbf1_J$,

$$
M_c=u_{I_x}\otimes u_{I_x},\qquad
M_m=u_L\otimes u_L+u_R\otimes u_R.
$$

The rank-one convention is $(z\otimes z)f=z\langle z,f\rangle$.

## Proof Strategy

Use the orthogonal decomposition of the two-dimensional child-flat space.
Apply the resulting rank-one projector update to $w$ and $g$, then evaluate
each term by partial sums. Prove the integer crosswalk in four residue
classes. Substitute the literal source kernel directly and invoke only the
definition of the finite adjoint.

## Dependency Map

1. Contrast normalization depends only on $N=\ell+r$.
2. The projector identity depends on the orthonormal basis
   $\{u_{I_x},z\}$ of the child-flat space.
3. Longitudinal and transverse updates depend on that projector identity and
   first-slot conjugation.
4. The within-child formula depends on childwise orthogonal centering.
5. The literal expansion depends only on substituting the TPC-247 matrix
   entries.
6. The safe transfer depends on the finite adjoint definition, not on
   self-adjointness.
7. The claim ceiling is witnessed by exact nonliteral controls.

## Proof

### Step 1: the split is source-only and nondegenerate

Since $N\geq2$, both $\ell=\lfloor N/2\rfloor$ and
$r=N-\ell=\lceil N/2\rceil$ are positive. The ordered sets $L$ and $R$ are
therefore nonempty, disjoint, and exhaustive. Their construction uses only
$x$ and the ordered set $I_x$, so it precedes every coefficient-dependent
quantity by definition.

### Step 2: zero sum, unit norm, and uniqueness

The sum of $h$ is

$$
\ell\frac1\ell+r\left(-\frac1r\right)=0.
$$

Moreover,

$$
\|z\|^2
=\rho^2\left(\ell\frac1{\ell^2}+r\frac1{r^2}\right)
=\frac{\ell r}{N}\left(\frac1\ell+\frac1r\right)=1.
$$

For uniqueness, let a child-flat zero-sum vector equal $a>0$ on $L$ and
$b<0$ on $R$. The zero-sum condition gives $b=-\ell a/r$. Unit norm then
gives

$$
1=\ell a^2+r\frac{\ell^2a^2}{r^2}
=\frac{\ell N}{r}a^2,
$$

so $a=\sqrt{r/(\ell N)}=\rho/\ell$ and
$b=-\sqrt{\ell/(rN)}=-\rho/r$. Thus the positive-on-$L$ unit contrast is
exactly $z$.

### Step 3: exact projector identity

Both $u_{I_x}$ and $z$ are child-flat. Their inner product vanishes because
$z$ has zero sum, and Step 2 gives unit norms. The child-flat subspace has
dimension two and is also spanned by the orthonormal pair $u_L,u_R$.
Therefore

$$
M_m=M_c+z\otimes z.
$$

Although $\rho$ need not be rational, every matrix entry of the added
projector is exact rational data:

$$
(z\otimes z)_{ij}=\rho^2h_i h_j.
$$

This representation proves the projector identity without a floating
radical.

### Step 4: integer $\lfloor3k/4\rfloor$ crosswalk

Let $x=k\geq3$ be integral. Then

$$
I_k=\{\lfloor k/2\rfloor+1,\ldots,k\},\qquad
N=k-\lfloor k/2\rfloor.
$$

Write $k=4m+s$, where $s\in\{0,1,2,3\}$. The values of
$\lfloor k/2\rfloor$, $N$, $\ell$, and the final coordinate
$\lfloor k/2\rfloor+\ell$ are

| $s$ | $\lfloor k/2\rfloor$ | $N$ | $\ell$ | final coordinate |
|---:|---:|---:|---:|---:|
| $0$ | $2m$ | $2m$ | $m$ | $3m$ |
| $1$ | $2m$ | $2m+1$ | $m$ | $3m$ |
| $2$ | $2m+1$ | $2m+1$ | $m$ | $3m+1$ |
| $3$ | $2m+1$ | $2m+2$ | $m+1$ | $3m+2$ |

The final column equals $\lfloor3k/4\rfloor$ in every row. Hence

$$
L=(k/2,\lfloor3k/4\rfloor]\cap\mathbb Z,
\qquad
R=(\lfloor3k/4\rfloor,k]\cap\mathbb Z.
$$

This establishes the integer crosswalk. The ordered rank definition remains
the theorem's definition for nonintegral real $x$.

### Step 5: partial-sum contrast and longitudinal formulas

Because $z$ is real and constant on each child,

$$
\langle z,f\rangle
=\sum_{n\in I_x}z(n)f(n)
=\rho\left(\frac{S_f(L)}\ell-\frac{S_f(R)}r\right).
$$

Let $W_J=S_w(J)$ and $G_J=S_g(J)$. The coarse projection has value
$(W_L+W_R)/N$ on every coordinate for $w$, and analogously for $g$.
Therefore

$$
C_{\rm long}(c)=\langle M_cw,M_cg\rangle
=\frac{\overline{W_L+W_R}(G_L+G_R)}N.
$$

The midpoint projection has childwise means, so

$$
C_{\rm long}(m)=\langle M_mw,M_mg\rangle
=\frac{\overline{W_L}G_L}{\ell}+\frac{\overline{W_R}G_R}{r}.
$$

These equalities establish the exact partial-sum compiler.

### Step 6: conjugate-first covariance transfer

The ranges of $M_c$ and $z\otimes z$ are orthogonal. Applying Step 3 gives

$$
\begin{aligned}
C_{\rm long}(m)
&=\langle M_cw+(z\otimes z)w,\,M_cg+(z\otimes z)g\rangle\\
&=C_{\rm long}(c)+\langle(z\otimes z)w,(z\otimes z)g\rangle\\
&=C_{\rm long}(c)+\overline{\langle z,w\rangle}\langle z,g\rangle.
\end{aligned}
$$

The last line uses conjugate linearity in the first slot. Inserting Step 5
gives

$$
C_{\rm long}(m)-C_{\rm long}(c)
=\frac{\ell r}{N}
\overline{\left(\frac{W_L}{\ell}-\frac{W_R}{r}\right)}
\left(\frac{G_L}{\ell}-\frac{G_R}{r}\right).
$$

No inequality or sign inference appears in this calculation.

### Step 7: opposite transverse update and child covariance

Define

$$
Q_{\rm trans}(c)=\langle(I-M_c)w,(I-M_c)g\rangle,
$$

and define $Q_{\rm trans}(m)$ with $M_m$. Orthogonal decomposition gives
$C_x=C_{\rm long}(c)+Q_{\rm trans}(c)$ and
$C_x=C_{\rm long}(m)+Q_{\rm trans}(m)$. Subtracting these two identities and
using Step 6 yields

$$
Q_{\rm trans}(m)-Q_{\rm trans}(c)
=-\overline{\langle z,w\rangle}\langle z,g\rangle.
$$

The vector $(I-M_m)w$ equals $w-\mu_w(L)$ on $L$ and
$w-\mu_w(R)$ on $R$. The same statement holds for $g$. Expanding their inner
product gives

$$
Q_{\rm trans}(m)
=\sum_{J\in\{L,R\}}\sum_{n\in J}
\overline{w(n)-\mu_w(J)}[g(n)-\mu_g(J)].
$$

Thus

$$
Q_{\rm trans}(c)
=\overline{\langle z,w\rangle}\langle z,g\rangle
+Q_{\rm trans}(m).
$$

### Step 8: literal TPC-247 kernel substitution

Retain

$$
H=x^{21/32},\quad Q=x^{1/3},\quad
\mathcal Q_x=\{q\text{ prime}:Q<q\leq2Q\},\quad
K_H(h)=\widehat{\psi_+}(h/H),
$$

$$
\beta(t)=\frac{\Lambda(t)}{\log t}
-\sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d),
\qquad
w(u)=\Lambda(u+2)-b_x^{(z)}(u),
$$

and

$$
A_x(u,t)=\mathbf1_{u\ne t}\sum_{q\in\mathcal Q_x}q
\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}K_H(u-t)
\left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right).
$$

Substitute these matrix entries into Step 5 with $f=A_x\beta$. Finite
summation gives

$$
\begin{aligned}
\langle z,A_x\beta\rangle
={}&\rho\sum_{q\in\mathcal Q_x}q\sum_{u,t\in I_x}
\left(\frac{\mathbf1_L(u)}\ell-\frac{\mathbf1_R(u)}r\right)
\mathbf1_{u\ne t}\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}\\
&\quad\times\beta(t)K_H(u-t)
\left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right).
\end{aligned}
$$

This formula retains output $u$, input $t$, outer $q$, both masks, the
deleted diagonal, $K_H(u-t)$, the centered bracket, and literal $\beta(t)$.

### Step 9: safe adjoint identity

For the finite matrix $A_x$, define

$$
(A_x^*z)(t)=\sum_{u\in I_x}\overline{A_x(u,t)}z(u).
$$

Then

$$
\begin{aligned}
\langle A_x^*z,\beta\rangle
&=\sum_t\overline{\sum_u\overline{A_x(u,t)}z(u)}\,\beta(t)\\
&=\sum_{u,t}\overline{z(u)}A_x(u,t)\beta(t)
=\langle z,A_x\beta\rangle.
\end{aligned}
$$

The proof uses neither $K_H(-h)=\overline{K_H(h)}$ nor $A_x^*=A_x$.

### Step 10: sharp structural controls

If $w$ is constant, Step 5 gives $\langle z,w\rangle=0$ because
$\sum z=0$; the same conclusion holds for constant $g$. For the synthetic
choice $w=z,g=z$, unit normalization gives

$$
\overline{\langle z,w\rangle}\langle z,g\rangle=1.
$$

For $w=z,g=-z$, the value is $-1$. These examples prove that source-free
geometry permits zero and both signs. They are labeled nonliteral and make no
claim about the physical V59 coefficients.

Steps 1--10 prove the claim. $\square$

## Corrections or Missing Assumptions

None. The theorem is proved with the frozen assumptions. A sign-sensitive or
nonzero arithmetic conclusion would require an additional source-backed
estimate and is outside this claim.

## Open Risks

No proof dependency remains open at structural L1. The unresolved theorem is
to estimate the two literal rank-midpoint contrasts, or their product, on one
common growing V59 clock. The present proof supplies no smooth-partition
identification, canonicality, self-adjointness, sign, asymptotic, arithmetic,
L2, Gate-B, strict `1/400`, or twin-prime promotion.
