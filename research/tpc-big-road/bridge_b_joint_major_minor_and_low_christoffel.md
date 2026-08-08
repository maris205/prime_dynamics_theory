# Bridge B V29: exact local corridor, the independent major gate, and low-Christoffel carriers

Date: 2026-08-08

Status:

~~~text
EXACT_LOCAL_COMPILER_AND_GLOBAL_ZERO_AXIS_FIREWALL
MAXIMUM_CLAIM = EXACT_LOCAL_CARRIER_BETTIN_CHANDEE_COMPILER_PLUS_ZERO_AXIS_TWO_GATE_FIREWALL_PLUS_LOW_CHRISTOFFEL_RIESZ_CRITERION
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
~~~

V28 found an occurrence-native Euler carrier and a reduced-radical
Kloosterman-fraction corridor.  This note completes that corridor: the
literal hard shell, both Fourier signs, the \(q\mid D\) branch, the
\(F/G\) difference, the two coprimality compilers, the rough-factor
reassembly and the coupled smooth weight all fit Bettin--Chandee's three
arbitrary arrays.  It proves

\[
 E(M_x^{\rm loc}),\ J(M_x^{\rm loc})
 \ll x^{1891/1920+o(1)}.
\tag{0.1}
\]

That is a real local theorem.  It is not a theorem about the physical
scalar.  Since \(M_x^{\rm loc}(0)=0\), its \(J\)- and \(E\)-contributions
cancel exactly.  The residual still has its full physical value at the
zero coordinate.  V29 therefore separates the remaining global problem
into an independent major gate for \(J(e_x)\) and an off-zero gate for
\(E(e_x)\).

The dynamical reserve is also sharpened.  A target-blind finite-dimensional
carrier is governed by the Christoffel/Riesz complexity
\(\kappa=\|K^*\|_2^2\), with centered complexity
\(\kappa_0=\kappa-1\).  With variance \(O(x)\), the exact uniform
\(L^2\) threshold is \(\kappa_0=o(x/\log^4x)\), equivalently the same
condition with \(\kappa\).  Finite Fourier spaces show
that this channel is nonempty, while complete coordinates, coarse cells,
sparse martingale levels and target-calibrated one-vector kernels each have
exact scoped failures.

## 1. Frozen physical object and \(J/E\) operators

Keep the V19/V21/V27/V28 object literally:

\[
h_0=2,\qquad I_x=(x/2,x]\cap\mathbb Z,\qquad
z=(\log x)^K,
\tag{1.1}
\]

\[
w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u),
\tag{1.2}
\]

\[
r_x(h)=
\sum_{\substack{t,t+h\in I_x}}
\beta_x^{\rm raw}(t)w_x^{(z)}(t+h).
\tag{1.3}
\]

The coefficient \(\beta_x^{\rm raw}\) retains occurrence IDs, source
slots, ordered \(+2,-1\), Möbius and logarithmic weights, unit slots,
MASTER/H2 routing, multiplicity and \(1/\log t\).  The shift \(h\) in
(1.3) is not the fixed physical gap \(h_0\).

Set

\[
Q=x^{1/3},\qquad H=x^{21/32},\qquad
\mathcal Q=\{q\ {\rm prime}:Q<q\le2Q\},
\tag{1.4}
\]

\[
A_Q(h)=\sum_{q\in\mathcal Q}c_q(h),\qquad
L_{\rm pr}=A_Q(0)=\sum_{q\in\mathcal Q}(q-1),
\tag{1.5}
\]

\[
\kappa_x(h)=
\frac{\widehat\psi_+(h/H)A_Q(h)}{L_{\rm pr}}.
\tag{1.6}
\]

The source normalization is \(\widehat\psi_+(0)=1\), so
\(\kappa_x(0)=1\).  For a shift carrier \(f\), define

\[
J(f)=\sum_{h\in\mathbb Z}\kappa_x(h)f(h),
\qquad
E(f)=f(0)-J(f)
=-\sum_{h\ne0}\kappa_x(h)f(h).
\tag{1.7}
\]

Thus

\[
\boxed{J(f)+E(f)=f(0).}
\tag{1.8}
\]

Let \(M_x^{\rm loc}\) be the V28 occurrence-native Euler carrier and put

\[
e_x(h)=r_x(h)-M_x^{\rm loc}(h).
\tag{1.9}
\]

V28 proves

\[
M_x^{\rm loc}(0)=0,\qquad
J(M_x^{\rm loc})+E(M_x^{\rm loc})=0.
\tag{1.10}
\]

Consequently,

\[
\boxed{
e_x(0)=r_x(0)=S_x^{\rm physical},\qquad
S_x^{\rm physical}=J(e_x)+E(e_x).}
\tag{1.11}
\]

## 2. The zero-coordinate firewall and the exact two-gate theorem

Take any \(T>0\) and the finite carrier

\[
e(h)=T\mathbf1_{\{h=0\}}.
\tag{2.1}
\]

Then every off-zero datum vanishes:

\[
\left(
\sum_{h\ne0}|\widehat\psi_+(h/H)|\,|e(h)|^2
\right)^{1/2}=0,
\qquad E(e)=0,
\tag{2.2}
\]

but

\[
J(e)=e(0)=T.
\tag{2.3}
\]

This remains true if a circle-method minor region is empty: every
minor-arc product norm is zero while the target is \(T\).  Hence an
off-zero variance theorem, product-local flatness, or a bound for
\(E(e_x)\) alone cannot imply a bound for the physical scalar.

The weakest clean global contract has two independent gates.  Fix

\[
\theta<\frac{13}{4800}.
\tag{2.4}
\]

The major gate is

\[
\boxed{
|J(e_x)|=|J(r_x)-J(M_x^{\rm loc})|
\ll x^{399/400-\eta_M}}
\tag{2.5}
\]

for some fixed \(\eta_M>0\), proved without assuming the value of
\(S_x^{\rm physical}\).  The off-zero gate is

\[
\boxed{
\mathcal N_e:=
\left(
\sum_{0<|h|<x/2}
|\widehat\psi_+(h/H)|\,|e_x(h)|^2
\right)^{1/2}
\ll x^{1+\theta+\varepsilon_N}.}
\tag{2.6}
\]

V27 proves

\[
\frac1{L_{\rm pr}}
\left(
\sum_{h\ne0}|\widehat\psi_+(h/H)|\,|A_Q(h)|^2
\right)^{1/2}
=x^{-1/192+o(1)}.
\tag{2.7}
\]

Weighted Cauchy therefore gives

\[
|E(e_x)|
\ll x^{191/192+\theta+\varepsilon_N+o(1)}.
\tag{2.8}
\]

Since

\[
\frac{399}{400}-\frac{191}{192}
=\frac{13}{4800},
\tag{2.9}
\]

equality in (2.4) is insufficient.  One common final slack is legal after
choosing

\[
0<\varepsilon_*<
\min\left\{\eta_M,\,
\frac12\left(\frac{13}{4800}-\theta\right)\right\}.
\tag{2.10}
\]

Then (2.5) with \(+\varepsilon_*\) in the harmless error and (2.8) with
\(\varepsilon_N=\varepsilon_*\) both lie strictly below \(399/400\).

Thus the current first global fatal is not the local corridor:

~~~text
V29_OFFZERO_RESIDUAL_ENERGY_ALONE
  = STOP_SCOPED_DELTA_ZERO_SELF_RETURN

V29_TAGGED_RESIDUAL_INDEPENDENT_JUTILA_MAJOR
  = SELECTED_PRIMARY_OPEN_NEW_THEOREM

V29_TAGGED_RESIDUAL_OFFZERO_WEIGHTED_L2
  = OPEN_NEW_THEOREM

V29_TAGGED_RESIDUAL_TWO_GATE_CLOSURE
  = OPEN_MAJOR_AND_MINOR_THEOREM
~~~

## 3. The weakest MRT product-local interface

Let

\[
\mathcal B_x(\alpha)
=\sum_{t\in I_x}\beta_x^{\rm raw}(t)e(t\alpha),
\qquad
\mathcal W_x(\alpha)
=\sum_{u\in I_x}w_x^{(z)}(u)e(u\alpha).
\tag{3.1}
\]

Fix one predeclared measurable hard major set
\(\mathfrak M\subset\mathbb T\), put
\(\mathfrak m=\mathbb T\setminus\mathfrak M\), and define the actual
major coefficient

\[
MT_{\mathfrak M,h}
=\int_{\mathfrak M}
\mathcal B_x(\alpha)\overline{\mathcal W_x(\alpha)}
e(+h\alpha)\,d\alpha.
\tag{3.2}
\]

Matomäki--Radziwiłł--Tao, arXiv:1707.01315v3, Proposition 3.1, is an
abstract finite-support reduction.  With

\[
P_0=\int_{\mathfrak m}
|\mathcal B_x(\alpha)\mathcal W_x(\alpha)|\,d\alpha,
\tag{3.3}
\]

\[
P_Y=
\sup_\alpha
\int_{\mathfrak m\cap
[\alpha-1/(2Y),\alpha+1/(2Y)]}
|\mathcal B_x(\beta)\mathcal W_x(\beta)|\,d\beta,
\tag{3.4}
\]

it gives, up to an absolute convention constant,

\[
\sum_{|h-h_*|\le Y}
|r_x(h)-MT_{\mathfrak M,h}|^2
\ll YP_0P_Y.
\tag{3.5}
\]

To apply (3.5) to the literal residual, one must independently prove

\[
MT_{\mathfrak M,h}
=M_x^{\rm loc}(h)+a_x(h)
\tag{3.6}
\]

and pay

\[
\left(
\sum_{0<|h|<x/2}
|\widehat\psi_+(h/H)|\,|a_x(h)|^2
\right)^{1/2}
\ll x^{1+\theta+\varepsilon_N}.
\tag{3.7}
\]

The weakest product condition used by (3.5) is the product, not two
separate estimates:

\[
\boxed{
P_0P_Y
\ll
\frac{x^{2+2\theta+2\varepsilon_N}}Y
\quad\text{for every dyadic }H\le Y\le x.}
\tag{3.8}
\]

The stronger pair \(P_0\ll x^{1+o(1)}\) and
\(P_Y\ll x^{1+2\theta+o(1)}/Y\) is sufficient but unnecessary.
Existing MRT and MRSTT applications do not identify (3.6) for the
MASTER-routed \(\beta_x^{\rm raw}\) and
\(\Lambda(\cdot+2)-b_x^{(z)}\).  Almost-all shifts, a
\(\Lambda-\Lambda^\sharp\) comparison, one-sided local flatness, or
separate prime/hybrid absolute values do not provide the required
attachment.

In particular, even ideal one-sided control leaves the norm scale
\(xH^{1/4}=x^{1+21/128}\), with deficit

\[
\frac{21}{128}-\frac{13}{4800}
=\frac{1549}{9600}.
\tag{3.9}
\]

## 4. Literal interior aggregation and hard-shell boundary

For a labelled V19 MASTER occurrence \(o\), write

\[
t(o)=e_1\cdots e_jf_1\cdots f_j,\qquad
a_o=c_j\prod_i\mu(e_i)\frac{\log f_1}{\log t(o)},
\qquad c_1=+2,\ c_2=-1.
\tag{4.1}
\]

Let \(m(o)\) be the unique group selected by deterministic V19 routing
and \(D(o)=\operatorname{rad}m(o)\).  Then

\[
(x/2)^{133/400}<m(o)\le\sqrt x.
\tag{4.2}
\]

Choose

\[
Y=Hx^\varepsilon,\qquad
0<\varepsilon<\frac{11}{1920},
\tag{4.3}
\]

and set

\[
T_Y=\{t\in I_x:\operatorname{dist}(t,\partial I_x)\ge Y\}.
\tag{4.4}
\]

For squarefree \(D\), define

\[
A_Y(D)=
\sum_{\substack{o:\ {\rm MASTER}\\
t(o)\in T_Y\\D(o)=D}}a_o.
\tag{4.5}
\]

Every occurrence enters exactly one of \(T_Y\) and
\(I_x\setminus T_Y\), exactly one selected group \(m(o)\), and exactly
one radical \(D(o)\).  Formula (4.5) retains its sign and occurrence
provenance.  The ordered divisor envelope and radical Euler sum give

\[
|A_Y(D)|\ll\frac{x^{1+o(1)}}{\varphi(D)}.
\tag{4.6}
\]

The complete kernel has

\[
\frac1{L_{\rm pr}}
\sum_{q\in\mathcal Q}\sum_h
|\widehat\psi_+(h/H)c_q(h)|
\ll\frac HQ.
\tag{4.7}
\]

The boundary contribution is therefore

\[
\ll Y\frac HQx^{o(1)}
=x^{47/48+\varepsilon+o(1)}.
\tag{4.8}
\]

For \(t\in T_Y\), replacing the shifted shell by the full \(h\)-lattice
starts at \(|h|\ge Y\).  Arbitrary-order Schwartz decay makes this tail
\(O(x^{-A})\).  The full-lattice bulk can consequently execute the
complete unit-frequency cancellations before any absolute value.

## 5. Exact reduced-radical \(F/G\) emitter

For \(q\mid D\), V28's complete-period identity gives

\[
\mathcal K_q(D)=0
\tag{5.1}
\]

after the full unit-frequency sum and before absolute values.

For \(q\nmid D\), write

\[
g=(n,D),\qquad D=gR,\qquad
n=\epsilon ga,\quad
\epsilon\in\{\pm1\},\ a\ge1.
\tag{5.2}
\]

Then

\[
(a,qR)=1,\qquad
a\le\frac{qR}{H},\qquad
R\ge\frac Hq=x^{31/96+o(1)}.
\tag{5.3}
\]

Moreover,

\[
g=\frac DR\le\frac{q\sqrt x}{H}
=x^{17/96+o(1)}<q.
\tag{5.4}
\]

Thus the possible \(q\mid g\) correction is exactly empty, and
\(q\nmid D\) is equivalent to \(q\nmid R\) on active support.

The normalized local transforms are

\[
\widehat P_D(n\overline q)
=\frac{\mu(R)}{\varphi(R)}
e_R(2\epsilon a\overline q),
\tag{5.5}
\]

\[
\widehat B_{D,z}(n\overline q)
=
\frac{\mu(R_0)}
{\varphi(R_0)\varphi(R_1)^2}
e_{R_0}(2\epsilon a\overline{qR_1}),
\tag{5.6}
\]

where

\[
R=R_0R_1,\qquad
p\mid R_0\Longleftrightarrow p\le z.
\tag{5.7}
\]

If \(R_1=1\), (5.5) and (5.6) agree exactly and are removed before
absolute values.  Define

\[
S_Y(R)=
\sum_{\substack{g:\ (g,R)=1\\gR\le\sqrt x}}A_Y(gR),
\tag{5.8}
\]

\[
B_F(R)=\frac{\mu(R)}{\varphi(R)}S_Y(R),
\qquad
B_G(R_0,R_1)=
\frac{\mu(R_0)}
{\varphi(R_0)\varphi(R_1)^2}S_Y(R_0R_1).
\tag{5.9}
\]

Then the interior bulk is exactly

\[
E_{\rm bulk}
=-\frac H{L_{\rm pr}}\mathfrak F
+\frac H{L_{\rm pr}}\mathfrak G,
\tag{5.10}
\]

with

\[
\mathfrak F=
\sum_{\epsilon=\pm1}
\sum_{q\in\mathcal Q}
\sum_{\substack{R\\(q,R)=1\\R_1(R)>1}}
B_F(R)
\sum_{\substack{a\ge1\\(a,R)=1}}
\Psi_\epsilon\!\left(\frac{Ha}{qR}\right)
e_R(2\epsilon a\overline q),
\tag{5.11}
\]

\[
\mathfrak G=
\sum_{\epsilon=\pm1}
\sum_{q\in\mathcal Q}
\sum_{\substack{R_0,R_1\\
(q,R_0R_1)=1\\R_1>1}}
B_G(R_0,R_1)
\sum_{\substack{a\ge1\\(a,R_0R_1)=1}}
\Psi_\epsilon\!\left(\frac{Ha}{qR_0R_1}\right)
e_{R_0}(2\epsilon a\overline{qR_1}).
\tag{5.12}
\]

The signs in (5.10) are literal consequences of
\(\Delta=P-B\) and the outer minus in \(E\).

## 6. Coprimality, smooth separation and Bettin--Chandee

For the \(F\) branch, expand

\[
\mathbf1_{(a,R)=1}
=\sum_{d\mid(a,R)}\mu(d),
\qquad R=dr,\quad a=db.
\tag{6.1}
\]

Since \(R\) is squarefree,

\[
e_{dr}(2\epsilon db\overline q)
=e_r(2\epsilon b\overline q).
\tag{6.2}
\]

The Bettin--Chandee variables are therefore

\[
(a_{\rm BC},m_{\rm BC},n_{\rm BC})=(b,q,r),
\qquad
e\!\left(2\epsilon\frac{b\overline q}{r}\right),
\tag{6.3}
\]

and

\[
\|\mu(d)B_F(d\,\cdot)\|_{2,r\asymp S}
\ll\frac{x^{1+o(1)}}{d^2S^{3/2}}.
\tag{6.4}
\]

For the \(G\) branch, write

\[
R_0=d_0s,\qquad R_1=d_1l,\qquad
a=d_0d_1b.
\tag{6.5}
\]

The exact phase identity is

\[
e_{d_0s}\!\left(
2\epsilon d_0d_1b\overline{qd_1l}
\right)
=e_s(2\epsilon b\overline{ql}),
\tag{6.6}
\]

and

\[
\left\|
\mu(d_0)\mu(d_1)B_G(d_0\,\cdot,d_1l)
\right\|_{2,s\asymp S}
\ll
\frac{x^{1+o(1)}}
{d_0^2d_1^3l^3S^{3/2}}.
\tag{6.7}
\]

The \(d^{-2}\), \(d_0^{-2}\) and \(d_1^{-3}\) sums are convergent up to
\(x^{o(1)}\).  For fixed exact \(l\), the source variables are

\[
(a_{\rm BC},m_{\rm BC},n_{\rm BC})=(b,ql,s).
\tag{6.8}
\]

After the local estimate, triangle over exact \(l\asymp L\) costs \(L\).
Every original \(R_1\) appears once; the cost combines with \(l^{-3}\)
to leave \(L^{-2}\).  It is confined to the local \(G\)-branch and is
included in the exponent ledger.  The degenerate \(s=1\) row is
absolutely \(O(x^{65/96+o(1)})\).

Use disjoint half-open dyadic blocks in every positive variable.  On an
\(F\)-block \(q\asymp Q,r\asymp S,b\asymp B\), the coupled weight is a
fixed smooth compact-box function

\[
\Phi_c(u,v,w)
=\Psi_\epsilon\!\left(c\frac{w}{uv}\right),
\qquad c=\frac{HB}{QS}=O(1).
\tag{6.9}
\]

A smooth extension and log-Fourier inversion separate (6.9) exactly,
with transform \(L^1\)-norm \(O_\psi(1)\).  The unit-modulus twists are
absorbed into the three arbitrary arrays without changing their
\(L^2\)-norms.  The \(G\)-branch is identical after exact \(l\) is fixed.

Bettin--Chandee, arXiv:1502.00769v1, Theorem 1, accepts arbitrary
coefficient arrays in the trilinear Kloosterman fraction
\(e(\vartheta a\overline m/n)\).  For \(F\),

\[
(A,M,N)=(QS/H,Q,S),\qquad \vartheta=\pm2,
\tag{6.10}
\]

\[
\|\alpha_q\|_2\ll Q^{1/2+o(1)},\quad
\|\nu_b\|_2\ll A^{1/2+o(1)},\quad
\|\beta_r\|_2\ll x^{1+o(1)}S^{-3/2}.
\tag{6.11}
\]

With \(S=x^\rho\), its first term gives

\[
\mathfrak E_{F,1}(\rho)\le
\begin{cases}
\dfrac{2077}{1920}-\dfrac{3\rho}{10},
 &31/96\le\rho\le1/3,\\[2mm]
\dfrac{639}{640}-\dfrac{\rho}{20},
 &1/3\le\rho\le1/2.
\end{cases}
\tag{6.12}
\]

For \(G\), put \(S=x^\sigma,L=x^\lambda\).  After the exact-\(l\)
triangle, the first term is

\[
\mathfrak E_{G,1}(\sigma,\lambda)\le
\begin{cases}
\dfrac{2077}{1920}
-\dfrac{3\sigma}{10}-\dfrac{11\lambda}{20},
 &1/3+\lambda\ge\sigma,\\[2mm]
\dfrac{1917}{1920}
-\dfrac{\sigma}{20}-\dfrac{4\lambda}{5},
 &\sigma\ge1/3+\lambda.
\end{cases}
\tag{6.13}
\]

Under \(\sigma+\lambda\ge31/96\), both (6.12) and (6.13) have worst
value

\[
\frac{1891}{1920}.
\tag{6.14}
\]

The second source term is at most \(737/768\) in the lower branch and
\(23/24\) in the upper branch, for both \(F\) and \(G\).  Since

\[
\frac H{L_{\rm pr}}=x^{-1/96+o(1)},
\qquad
\frac{399}{400}-\frac{1891}{1920}
=\frac{121}{9600},
\tag{6.15}
\]

and

\[
\frac{1891}{1920}-\frac{47}{48}
=\frac{11}{1920},
\tag{6.16}
\]

the choice in (4.3) yields

\[
\boxed{
|E(M_x^{\rm loc})|
\ll x^{1891/1920+o(1)}.}
\tag{6.17}
\]

By (1.10),

\[
\boxed{
|J(M_x^{\rm loc})|
=|E(M_x^{\rm loc})|
\ll x^{1891/1920+o(1)}.}
\tag{6.18}
\]

The local carrier is now paid in each branch.  Its combined physical
contribution remains exactly zero.

## 7. Finite Riesz kernels and the Christoffel threshold

Let \((C,\nu)\) be a probability space and
\(\mathcal H\subset L^2(C,\nu;\mathbb R)\) a predeclared
finite-dimensional real Hilbert subspace containing \(1\).  Let

\[
L:\mathcal H\to\mathbb R,\qquad L(1)=1
\tag{7.1}
\]

be target-blind.  Its unique minimum-norm Riesz kernel
\(K^*\in\mathcal H\) satisfies

\[
L(f)=\langle K^*,f\rangle\quad(f\in\mathcal H),
\qquad
\int K^*\,d\nu=1.
\tag{7.2}
\]

Define

\[
\kappa=\|K^*\|_2^2,\qquad
\kappa_0=\|K^*-1\|_2^2=\kappa-1.
\tag{7.3}
\]

Every other representing kernel \(K\) has

\[
P_{\mathcal H}K=K^*,\qquad
\|K\|_2^2
=\kappa+\|(I-P_{\mathcal H})K\|_2^2.
\tag{7.4}
\]

For \(S\in\mathcal H\), put

\[
m=\int S\,d\nu,\qquad
V=\|S-m\|_2.
\tag{7.5}
\]

Then

\[
L(S)
=m+\langle K^*-1,S-m\rangle
\ge m-\sqrt{\kappa_0}\,V.
\tag{7.6}
\]

If

\[
m\gg\frac{x}{\log^2x},
\qquad V^2=O(x),
\tag{7.7}
\]

the sharp uniform worst-case \(L^2\) threshold is

\[
\boxed{
\kappa_0=o(x/\log^4x).}
\tag{7.8}
\]

Using \(\kappa\) instead of \(\kappa_0\) is an equivalent sufficient
condition at growing complexity, but (7.8) is the exact centered form.
The Cauchy boundary is attained by a fluctuation parallel to
\(-(K^*-1)\).

For a quotient \(Q:\mathcal H\to Z\), the evaluation factors through the
quotient exactly when

\[
L=\ell\circ Q\ \text{for some }\ell
\quad\Longleftrightarrow\quad
\ker Q\subseteq\ker L.
\tag{7.9}
\]

For the point-evaluation specialization \(L=\operatorname{ev}_0\), with
point evaluation well defined, if \(0\) is an atom,
\(\delta_0\in\mathcal H\), and \(Q\) is specifically the restriction
that deletes the zero coordinate, then
\(\delta_0\in\ker Q\setminus\ker L\), so factorization fails.  For an
arbitrary \(L\), a quotient fails exactly when \(\ker Q\) contains some
\(f\in\mathcal H\) with \(L(f)\ne0\).

On \(G=\mathbb Z/N\mathbb Z\) with normalized Haar measure, let
\(A\subset\widehat G\) contain the trivial character and be closed under
complex conjugation, and let

\[
\mathcal H_A
=\operatorname{span}_{\mathbb C}\{\chi:\chi\in A\}
 \cap L^2(G;\mathbb R).
\tag{7.10}
\]

Point evaluation at \(0\) has

\[
K_A(n)=\sum_{\chi\in A}\chi(n),\qquad
\boxed{\kappa_A=|A|,\quad\kappa_{A,0}=|A|-1.}
\tag{7.11}
\]

Thus a predeclared translation-invariant arithmetic subspace of dimension
\(d=o(x/\log^4x)\) meets (7.8).  The channel is genuinely nonempty.  For
\(N=4,A=\{0,1,3\}\),

\[
K=(3,1,-1,1),\qquad
S=(4,2,0,2),
\tag{7.12}
\]

and normalized averaging gives

\[
\int K=1,\quad \|K\|_2^2=3,\quad
\int KS=4=S(0),\quad S\ge0.
\tag{7.13}
\]

For a general \(d\)-dimensional subspace with orthonormal basis
\(\phi_1,\ldots,\phi_d\), the leverage is

\[
\kappa(y)=\sum_{j=1}^d|\phi_j(y)|^2,\qquad
\int\kappa(y)\,d\nu(y)=d.
\tag{7.14}
\]

Rank alone does not control a distinguished point unless symmetry makes
\(\kappa(y)\) uniform.

## 8. Exact scoped kernel no-gos

The complete \(N\)-coordinate point kernel is

\[
K=N\delta_0,\qquad \kappa=N,\quad\kappa_0=N-1.
\tag{8.1}
\]

For \(N\asymp x\), it misses (7.8) by \(\log^4x\).  The full primorial
kernel is exponentially worse.  This stops only complete coordinates,
not a special low-leverage quotient.

For a partition atom \(C_0\) of mass \(p\), the kernel
\[
K=\mathbf1_{C_0}/p,\qquad\kappa=1/p
\tag{8.2}
\]
represents evaluation on the cell-measurable subspace.  It does not
represent point evaluation on arbitrary functions.  On four equal points,

\[
K=(2,2,0,0),\qquad S=(2,0,0,0)
\tag{8.3}
\]

gives

\[
\int KS=1\ne2=S(0).
\tag{8.4}
\]

The exact cell threshold is \(px/\log^4x\to\infty\), but a physical
compiler must also prove that every admissible arithmetic function is
cell-measurable or that unresolved directions lie in the evaluation
kernel.

Sparse martingale levels give no norm gain by themselves.  On eight equal
points, the successive kernels for cells of size \(8,4,2,1\) have squared
norms \(1,2,4,8\), while the orthogonal increment energies are
\(1,2,4\).  Hence

\[
1+1+2+4=8.
\tag{8.5}
\]

Deleting the tail returns a cell average; retaining it restores the full
singleton norm.

One-vector fitting is circular.  If
\(m=\int S\), \(V^2=\|S-m\|_2^2>0\), then for any requested target \(B\),

\[
K_B=1+\frac{B-m}{V^2}(S-m)
\tag{8.6}
\]

satisfies

\[
\int K_B=1,\qquad
\int K_BS=B,\qquad
\|K_B\|_2^2=1+\frac{(B-m)^2}{V^2}.
\tag{8.7}
\]

It reads the answer \(B\) and the realized vector \(S\).  A legal kernel
must be declared before the future twin output and represent the whole
declared source class.

A stage tag also cannot improve the norm.  If a fiber has mass \(w\), the
same evaluation kernel scales by \(1/w\), so

\[
\kappa_{\rm skew}=\kappa/w\ge\kappa.
\tag{8.8}
\]

Nonautonomous evolution remains logically open, but exact compatibility
requires

\[
A_j^*K_{j+1}=K_j
\tag{8.9}
\]

or a defect whose accumulated physical evaluation is
\(o(x_j/\log^2x_j)\).

## 9. Source boundary and route order

The source roles are sharply separated.

1. Bettin--Chandee, arXiv:1502.00769v1, Theorem 1, supplies the
   arbitrary-array trilinear Kloosterman-fraction bound used in
   (6.10)--(6.18).  V29 supplies the missing literal local emitter.
2. Matomäki--Radziwiłł--Tao, arXiv:1707.01315v3, Proposition 3.1,
   supplies only the abstract product reduction (3.5).  It does not prove
   (3.6)--(3.8) for the TPC pair.
3. Aspenberg--Baladi--Persson, arXiv:2212.12202v2, Theorem 1.1, treats
   the Logistic critical seed \(1/2\) for one fixed Hölder observable on
   a normalized Lebesgue almost-everywhere parameter space.  It supplies
   neither a low-Christoffel quotient nor a named arithmetic parameter.
4. Haydn--Nicol--Török--Vaienti, arXiv:1406.4266, Theorem 3.1, requires
   uniform sequential expansion, observable norm and variance hypotheses.
   It does not attach the growing primorial/TPC class.

The direct-source screen as of 2026-08-08 found no theorem for the
independent \(J(e_x)\) gate.  MRSTT inputs concern
\(\Lambda-\Lambda^\sharp\), fixed-complexity phases or almost-all
intervals/shifts; newer factorable-modulus and Kloosterman-fraction
theorems are post-emitter engines.  None preserves the complete literal
MASTER and hybrid scalar through (2.5).

The route order is therefore:

~~~text
1. independent major J(e) attachment and the same residual's off-zero L2;
2. completed local Bettin--Chandee corridor as a reusable paid subgate;
3. target-blind low-Christoffel whole-shell quotient;
4. unchanged O161, pair-native, H1, A1/A2 and provenance reserves.
~~~

## 10. Canonical status registry and next theorem

~~~text
V29_MAXIMUM_CLAIM = EXACT_LOCAL_CARRIER_BETTIN_CHANDEE_COMPILER_PLUS_ZERO_AXIS_TWO_GATE_FIREWALL_PLUS_LOW_CHRISTOFFEL_RIESZ_CRITERION
V29_ROUTE_ADVANCE = YES
V29_ARITHMETIC_ADVANCE = NO
V29_FIXED_ATOM_CREDIT = 0
V29_STRICT_1_OVER_400 = UNPAID
V29_L2 = NONE
V29_TPC_207_TRIGGER = false
V29_NUMBERED_RELEASE = NO
V29_ZERO_AXIS_RESIDUAL_IDENTITY = PROVED_EXACT_FROM_V28_TAGGED_DEFINITION
V29_ZERO_AXIS_DIRAC_FIREWALL = PROVED_EXACT_FINITE_E_ZERO_J_FULL_EXAMPLE
V29_OFFZERO_RESIDUAL_ENERGY_ALONE = STOP_SCOPED_DELTA_ZERO_SELF_RETURN
V29_TAGGED_RESIDUAL_INDEPENDENT_JUTILA_MAJOR = SELECTED_PRIMARY_OPEN_NEW_THEOREM
V29_TAGGED_RESIDUAL_OFFZERO_WEIGHTED_L2 = OPEN_NEW_THEOREM
V29_TAGGED_RESIDUAL_TWO_GATE_CLOSURE = OPEN_MAJOR_AND_MINOR_THEOREM
V29_MRT_ABSTRACT_PRODUCT_LOCAL_L2 = SOURCE_BACKED_REDUCTION_ONLY
V29_WEAKEST_PRODUCT_LOCAL_CONDITION = PRODUCT_P0_TIMES_PY_WITH_HARD_MAJOR_ATTACHMENT
V29_ACTUAL_MAJOR_COEFFICIENT_MLOC_PLUS_A = OPEN_WEIGHTED_AP_ATTACHMENT
V29_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V29_MASTER_INTERIOR_BOUNDARY_EXACT_COVER = PROVED_WITH_X_47_OVER_48_PLUS_EPSILON
V29_Q_DIVIDES_D_PRE_ABSOLUTE_CANCELLATION = PROVED_EXACT_FULL_LATTICE_BULK
V29_Q_DIVIDES_G_CORRECTION = PROVED_EMPTY_BY_G_LT_Q
V29_F_G_SIGNED_REDUCED_RADICAL_EMITTER = PROVED_EXACT
V29_R1_EQUAL_ONE_PRE_ABSOLUTE_CANCELLATION = PROVED_EXACT
V29_F_COPRIMALITY_MOBIUS_COMPILER = PROVED_D_MINUS_2_SUMMABLE
V29_G_COPRIMALITY_MOBIUS_COMPILER = PROVED_D0_MINUS_2_D1_MINUS_3_SUMMABLE
V29_EXACT_R1_LOCAL_TRIANGLE = PROVED_L_FACTOR_PAID_IN_EXPONENT_LEDGER
V29_SMOOTH_DYADIC_SEPARATION = PROVED_EXACT_LOG_FOURIER_X_O1
V29_LOCAL_CARRIER_BC_BOUND = PROVED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V29_LOCAL_CARRIER_BC_EXPONENT = 1891/1920
V29_LOCAL_CARRIER_BC_MARGIN_TO_399_400 = 121/9600
V29_LOCAL_EULER_TENSOR_AS_ACTUAL_AP_MAIN = OPEN_ATTACHMENT
V29_PREDECLARED_SUBSPACE_MINIMUM_RIESZ_KERNEL = PROVED_EXACT_FINITE_HILBERT
V29_EVALUATION_FACTORIZATION_GATE = PROVED_EXACT_KER_Q_SUBSET_KER_L_IFF
V29_VARIANCE_O_X_CHRISTOFFEL_THRESHOLD = PROVED_EXACT_KAPPA0_O_X_OVER_LOG4
V29_FINITE_CYCLIC_SPECTRAL_KERNEL = PROVED_EXACT_KAPPA_EQUALS_FREQUENCY_DIMENSION
V29_NONCONSTANT_LOW_NORM_KERNEL_CHANNEL = PROVED_NONEMPTY_EXACT_FINITE_MODEL
V29_COARSE_CELL_AS_POINT_EVALUATION = STOP_SCOPED_EXACT_FOUR_POINT_COUNTEREXAMPLE
V29_SPARSE_MARTINGALE_LEVEL_COUNT = STOP_SCOPED_ORTHOGONAL_ENERGY_REASSEMBLES_SINGLETON_NORM
V29_TARGET_CALIBRATED_SINGLE_BLOCK_KERNEL = STOP_SCOPED_EXACT_CIRCULAR_ONE_VECTOR_FIT
V29_STAGE_TAG_SKEW_PRODUCT_NORM_GAIN = STOP_SCOPED_EXACT_KAPPA_DIVIDED_BY_FIBER_MASS
V29_ACTUAL_WHOLE_SHELL_LOW_CHRISTOFFEL_QUOTIENT = SELECTED_DYNAMICS_OPEN_NEW_THEOREM
V29_INDEPENDENT_POSITIVE_KERNEL_MAIN = OPEN_ATTACHMENT_NOT_SAME_OUTPUT_MEAN
~~~

The maximum supported claim is the exact local compiler, the two-gate
firewall, and the finite Hilbert/Riesz criterion.  It is not an arithmetic
power saving for \(S_x^{\rm physical}\).

The narrowest next theorem is:

~~~text
V29_TAGGED_RESIDUAL_INDEPENDENT_JUTILA_MAJOR
~~~

It must prove (2.5) on the same literal occurrence/provenance object,
without using the unknown zero coefficient, an almost-all exceptional
set, or specieswise absolute values.  Only after that gate is paid can
the MRT product-local route for (2.6) become a complete arithmetic road.
