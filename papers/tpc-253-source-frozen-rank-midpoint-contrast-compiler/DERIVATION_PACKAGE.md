# Derivation Package

## Target

Derive the exact source-frozen rank-midpoint compiler for the finite literal
TPC-247 scalar

$$
g=A_x\beta,\qquad C_x=\langle w,g\rangle,
$$

including the ordered split, normalized contrast, integer crosswalk,
partial-sum moments, coarse/midpoint longitudinal and transverse formulas,
literal kernel expansion, safe adjoint identity, and sharp finite controls.

## Status

`COHERENT AS STATED`

Project status:

```text
PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER
```

The target survives unchanged. Every derived statement is an exact finite
identity; no approximation enters.

## Invariant Object

The invariant object is the fixed scalar $C_x=\langle w,A_x\beta\rangle$ on
the ordered physical coordinate interval. Changing from the coarse average
to the rank midpoint only reallocates one exact covariance between the
longitudinal and transverse terms; it does not change $C_x$.

## Assumptions

- $x>0$ is real and
  $I_x=(x/2,x]\cap\mathbb Z=\{n_1<\cdots<n_N\}$ has $N\geq2$.
- The inner product on $\mathbb C^{I_x}$ is conjugate-linear in its first
  slot.
- The ordered rank split is declared from $x$ and $I_x$ before inspecting
  $\beta$, $w$, $A_x\beta$, any margin, or any sign.
- $g=A_x\beta$ and $C_x=\langle w,g\rangle$ retain the literal TPC-247 source
  orientation.
- No symmetry of $K_H$, equality $A_x^*=A_x$, smooth-partition
  identification, or canonicality of the rank midpoint is assumed.

## Notation

Set

$$
\ell=\lfloor N/2\rfloor,\qquad r=N-\ell=\lceil N/2\rceil,
$$

and define $L=\{n_1,\ldots,n_\ell\}$ and
$R=\{n_{\ell+1},\ldots,n_N\}$. Write

$$
h=\frac{\mathbf1_L}{\ell}-\frac{\mathbf1_R}{r},\qquad
\rho^2=\frac{\ell r}{N},\qquad z=\rho h.
$$

For $J\subset I_x$, let $S_f(J)=\sum_{n\in J}f(n)$ and
$\mu_f(J)=S_f(J)/|J|$. Let $u_J=|J|^{-1/2}\mathbf1_J$,
$M_{\rm coarse}=u_{I_x}\otimes u_{I_x}$, and
$M_{\rm mid}=u_L\otimes u_L+u_R\otimes u_R$.

## Derivation Strategy

First derive the orthogonal rank-one geometry from the ordered coordinate
set. Next express all moments using partial sums. Then substitute the literal
TPC-247 kernel without altering its factors or orientation. Finally use the
finite adjoint definition and exact controls to locate the claim ceiling.

## Derivation Map

1. Ordered $I_x$ fixes $L,R,\ell,r$ independently of coefficients.
2. Cardinality identities give $\sum h=0$ and
   $\rho^2\sum h(n)^2=1$.
3. The child-flat space is the orthogonal sum of the coarse-flat direction
   and $\operatorname{span}\{z\}$, giving the projector update.
4. Partial sums give the two longitudinal terms and the covariance transfer.
5. Orthogonal complement subtraction gives the opposite transverse update
   and childwise covariance formula.
6. Literal substitution expands $\langle z,A_x\beta\rangle$; no
   approximation or kernel symmetry is used.
7. The adjoint definition transfers $A_x$ safely to $z$.
8. Constant and signed synthetic controls show why sign/nonzero claims do not
   follow from geometry.

## Main Derivation

### Step 1: normalized rank contrast

The rank split gives

$$
\sum_{n\in I_x}h(n)=\ell\frac1\ell-r\frac1r=0
$$

and

$$
\rho^2\sum_{n\in I_x}h(n)^2
=\frac{\ell r}{N}\left(\frac1\ell+\frac1r\right)=1.
$$

Thus $z=\rho h$ has zero sum and unit norm. For executable exact arithmetic,
the contrast projector is represented without radicals by

$$
(z\otimes z)_{ij}=\rho^2h_i h_j\in\mathbb Q.
$$

This is an identity, not an approximation to $\rho$.

### Step 2: projector update

The vectors $u_{I_x}$ and $z$ are orthonormal and span the same two-dimensional
space as $u_L,u_R$. Hence

$$
M_{\rm mid}=M_{\rm coarse}+z\otimes z.
$$

Among child-flat unit contrasts with positive sign on $L$, zero sum fixes the
ratio of the two constants and unit norm fixes their magnitude; therefore
$z$ is unique with that sign convention.

### Step 3: integer threshold crosswalk

When $x=k\geq3$ is an integer,
$I_k=\{\lfloor k/2\rfloor+1,\ldots,k\}$ and
$N=k-\lfloor k/2\rfloor$. The final left coordinate is

$$
\lfloor k/2\rfloor+\lfloor N/2\rfloor=\lfloor3k/4\rfloor.
$$

Checking $k=4m+s$ for $s=0,1,2,3$ gives endpoints
$3m,3m,3m+1,3m+2$, respectively. Therefore

$$
L=(k/2,\lfloor3k/4\rfloor]\cap\mathbb Z,
\quad
R=(\lfloor3k/4\rfloor,k]\cap\mathbb Z.
$$

The threshold formula is integer-only; the ordered rank definition remains
primary for arbitrary real $x$.

### Step 4: exact partial-sum moments

Since $z$ is real,

$$
\langle z,f\rangle
=\rho\left(\frac{S_f(L)}\ell-\frac{S_f(R)}r\right).
$$

Put $W_J=S_w(J)$ and $G_J=S_g(J)$. Direct block averaging gives

$$
C_{\rm long}({\rm mid})
=\frac{\overline{W_L}G_L}{\ell}+\frac{\overline{W_R}G_R}{r},
$$

and

$$
C_{\rm long}({\rm coarse})
=\frac{\overline{W_L+W_R}(G_L+G_R)}N.
$$

### Step 5: covariance transfer and within-child remainder

Applying the projector update to both arguments yields the identity

$$
C_{\rm long}({\rm mid})-C_{\rm long}({\rm coarse})
=\overline{\langle z,w\rangle}\langle z,g\rangle.
$$

The first-slot convention is visible after inserting partial sums:

$$
\overline{\langle z,w\rangle}\langle z,g\rangle
=\frac{\ell r}{N}
\overline{\left(\frac{W_L}{\ell}-\frac{W_R}{r}\right)}
\left(\frac{G_L}{\ell}-\frac{G_R}{r}\right).
$$

The total scalar is fixed, so the transverse term changes oppositely:

$$
Q_{\rm trans}({\rm mid})-Q_{\rm trans}({\rm coarse})
=-\overline{\langle z,w\rangle}\langle z,g\rangle.
$$

Centering separately in each child gives the exact residual

$$
Q_{\rm trans}({\rm mid})
=\sum_{J\in\{L,R\}}\sum_{n\in J}
\overline{w(n)-\mu_w(J)}\,[g(n)-\mu_g(J)].
$$

Consequently

$$
C_x=C_{\rm long}({\rm mid})+Q_{\rm trans}({\rm mid}),
$$

and $Q_{\rm trans}({\rm coarse})$ is the transferred contrast covariance
plus the within-child covariance. These are identities; no sign follows.

### Step 6: literal kernel expansion

Retain

$$
H=x^{21/32},\quad Q=x^{1/3},\quad
\mathcal Q_x=\{q\text{ prime}:Q<q\leq2Q\},\quad
K_H(h)=\widehat{\psi_+}(h/H),
$$

and the literal $\beta,w$. The TPC-247 kernel is

$$
A_x(u,t)=\mathbf1_{u\ne t}\sum_{q\in\mathcal Q_x}q
\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}K_H(u-t)
\left(\mathbf1_{u\equiv t\ (q)}-\frac1{q-1}\right).
$$

Substitution into the $g$-contrast gives

$$
\begin{aligned}
\langle z,A_x\beta\rangle
={}&\rho\sum_{q\in\mathcal Q_x}q\sum_{u,t\in I_x}
\left(\frac{\mathbf1_L(u)}\ell-\frac{\mathbf1_R(u)}r\right)
\mathbf1_{u\ne t}\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}\\
&\qquad\times\beta(t)K_H(u-t)
\left(\mathbf1_{u\equiv t\ (q)}-\frac1{q-1}\right).
\end{aligned}
$$

Every factor is inherited literally. The step is exact formal substitution.

### Step 7: safe adjoint transfer

For a finite matrix,

$$
(A_x^*z)(t)=\sum_{u\in I_x}\overline{A_x(u,t)}z(u).
$$

The definition of the adjoint gives

$$
\langle z,A_x\beta\rangle=\langle A_x^*z,\beta\rangle.
$$

No replacement of $A_x^*$ by $A_x$ is made.

### Step 8: sharp controls

If $w$ or $g$ is constant, its contrast moment vanishes because $\sum h=0$.
The synthetic choices $(w,g)=(z,z)$ and $(z,-z)$ produce transfer $+1$ and
$-1$, respectively. These controls are finite Hilbert-space examples, not
literal numerical V59 instances.

## Remarks and Interpretation

- The ordered interval supplies a reproducible nontrivial direction without
  observing the coefficients.
- Exact projector products avoid every floating-radical issue when $N$ is
  odd.
- The compiler exposes two concrete arithmetic targets:
  $\langle z,w\rangle$ and $\langle z,A_x\beta\rangle$ on one common clock.
- Formal kernel compilation and executable exact-sample replay verify
  orientation and algebra, not unknown physical values.

## Boundaries and Non-Claims

- The rank midpoint is not V59-canonical and is not identified with V59's
  smooth bounded-overlap mesoscopic partition.
- No self-adjointness or kernel symmetry is claimed.
- No sign, nonzero contrast, scale, power saving, asymptotic estimate,
  arithmetic advance, L2, fixed-atom credit, Gate-B closure, strict `1/400`,
  or twin-prime result is derived.
- Synthetic controls and exact-sample kernel values are labeled nonliteral.

## Open Risks

The structural proof has no unresolved algebraic step. The open mathematical
risk is entirely source-specific: no locked theorem currently estimates both
literal rank-midpoint imbalances, or their product, on one growing V59 clock.
