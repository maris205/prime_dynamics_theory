# Bridge B V28: Euler zero-axis cancellation, short inverse residues, and compressed kernel carriers

Date: 2026-08-08

Status:

~~~text
EXACT_L0_EULER_ZERO_AXIS_AND_KERNEL_CARRIER_ROUTE
MAXIMUM_CLAIM = EXACT_OCCURRENCE_NATIVE_EULER_ZERO_AXIS_AND_REDUCED_RADICAL_CORRIDOR_PLUS_SOURCE_BACKED_CONDITIONAL_BETTIN_CHANDEE_ENGINE_PLUS_STATIONARY_FACTOR_NO_GO_AND_COMPRESSED_KERNEL_ROUTE
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

V27 reduced the analytic error to one Ramanujan-weighted shift energy, but
also showed that a generic smooth main returns its value at the deleted
correlation-zero coordinate.  This note identifies a different, occurrence-
native Euler carrier whose zero coordinate vanishes exactly.  It then exposes
the remaining short inverse-residue corridor and separates two honest ways to
continue: a tagged joint main/error theorem, or a direct product-local
flatness theorem.

On the dynamical side, this note proves that a stationary mixing Logistic or
Hénon system cannot factor measure-preservingly onto the arithmetic odometer.
The surviving third carrier is not a same-output parameter average.  It is a
target-independent, low-norm conditional-expectation kernel.  The natural
full-primorial point-evaluation kernel has exponentially large norm and is
therefore stopped.

These are route advances and exact interfaces, not an arithmetic power
saving.

## 1. Frozen physical object and operators

Keep all V19/V25/V27 types literally:

\[
h_0=2,\qquad I_x=(x/2,x]\cap\mathbb Z,\qquad
z=(\log x)^K,
\tag{1.1}
\]

\[
w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u),
\tag{1.2}
\]

and the V19 ordered coefficient \(\beta_x^{\rm raw}\), including source
slots, literal \(+2,-1\), Mobius/log weights, MASTER/H2 routing, occurrence
multiplicity and \(1/\log t\).  For every correlation shift
\(h\in\mathbb Z\), put

\[
r_x(h)=\sum_{\substack{t,t+h\in I_x}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(t+h).
\tag{1.3}
\]

The symbol \(h\) in (1.3) is not the fixed physical gap \(h_0=2\).
The Jutila error scalar later sums only \(h\ne0\), while \(r_x(0)\) is
retained for the exact \(J+E\) bookkeeping.

Use

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

and

\[
\kappa_x(h)=
\frac{\widehat\psi_+(h/H)A_Q(h)}{L_{\rm pr}}.
\tag{1.6}
\]

Since \(\widehat\psi_+(0)=1\), one has \(\kappa_x(0)=1\).  For every
shift carrier \(f\), define

\[
J(f)=\sum_{h\in\mathbb Z}\kappa_x(h)f(h),\qquad
E(f)=f(0)-J(f)=-\sum_{h\ne0}\kappa_x(h)f(h).
\tag{1.7}
\]

Thus

\[
\boxed{J(f)+E(f)=f(0).}
\tag{1.8}
\]

For \(f=r_x\), the second term is the V27 Jutila-error normal form.  An
estimate for \(E(r_x)\) alone remains blind to a change of the determinant
zero coefficient unless the Jutila main is also paid.

## 2. The occurrence-native Euler carrier

Let \(o\) be a labelled V19 MASTER occurrence.  Write

\[
t(o)=e_1\cdots e_jf_1\cdots f_j,
\qquad
a_o=c_j\prod_i\mu(e_i)\frac{\log f_1}{\log t(o)},
\tag{2.1}
\]

where \(c_1=+2\) and \(c_2=-1\).  Let \(m(o)\) be the actual group selected
by the deterministic V19 routing and put

\[
D(o)=\operatorname{rad}m(o),\qquad
(x/2)^{133/400}<m(o)\le\sqrt x.
\tag{2.2}
\]

For every prime \(p\), define the shifted-prime local tensor

\[
F_p(h)=\frac p{p-1}\mathbf 1_{h\not\equiv-2\pmod p}.
\tag{2.3}
\]

The literal hybrid tensor is

\[
G_{p,z}(h)=
\begin{cases}
F_p(h),&p\le z,\\[1mm]
\dfrac p{p-1},&p>z,\ h\equiv0\pmod p,\\[2mm]
\dfrac{p(p-2)}{(p-1)^2},&p>z,\ h\not\equiv0\pmod p.
\end{cases}
\tag{2.4}
\]

For an integer \(m\ge2\), set

\[
P_m(h)=\prod_{p\mid m}F_p(h),\qquad
B_{m,z}(h)=\prod_{p\mid m}G_{p,z}(h),
\tag{2.5}
\]

\[
\Delta_{m,z}(h)=P_m(h)-B_{m,z}(h).
\tag{2.6}
\]

The exact algebraic carrier and residual are

\[
M_x^{\rm loc}(h)=
\sum_{\substack{o:\ {\rm MASTER}\\t(o),t(o)+h\in I_x}}
a_o\Delta_{m(o),z}(h),
\qquad
e_x(h)=r_x(h)-M_x^{\rm loc}(h).
\tag{2.7}
\]

Equation (2.7) is an exact definition.  It does **not** assert that the
Euler tensor is already a source-backed weighted arithmetic-progression
asymptotic for the complete occurrence family.

## 3. Exact zero-axis and complete-period theorem

Both \(F_p\) and \(G_{p,z}\) have normalized mean one on
\(\mathbb Z/p\mathbb Z\).  If \(p\le z\), they are identical.  If
\(p>z\), then

\[
F_p(0)=G_{p,z}(0)=\frac p{p-1}.
\tag{3.1}
\]

For \(p=2\), the prime lies below the legal \(z\), and both factors vanish
at \(h=0\).  Consequently, for every \(m\), with
\(D=\operatorname{rad}m\),

\[
\boxed{\Delta_{m,z}(0)=0},
\qquad
\boxed{\sum_{h\bmod D}\Delta_{m,z}(h)=0}.
\tag{3.2}
\]

More strongly, for every prime \(q\),

\[
\boxed{
\sum_{h\bmod\operatorname{lcm}(q,D)}
c_q(h)\Delta_{m,z}(h)=0.}
\tag{3.3}
\]

If \(q\nmid D\), (3.3) is CRT independence and the zero mean of \(c_q\).
If \(q\mid D\), then

\[
\mathbb E(c_q\Delta)
=q\,\mathbb E(\mathbf1_{q\mid h}\Delta)-\mathbb E\Delta=0,
\tag{3.4}
\]

because, conditional on \(h\equiv0\pmod q\), the \(q\)-factors agree and
all remaining local factors still have mean one.

Literal \(+2,-1\), Mobius signs, \(\log f_1/\log t\), source slots and
occurrence multiplicity are common outer scalars in (3.2)--(3.3).  No J1/J2
or prime/hybrid cross-species cancellation is borrowed.

It follows occurrencewise that

\[
M_x^{\rm loc}(0)=0,
\qquad
\boxed{J(M_x^{\rm loc})+E(M_x^{\rm loc})=0}.
\tag{3.5}
\]

This must be distinguished from a smooth interpolant \(M\) satisfying
\(M(0)=r_x(0)\).  For such an interpolant, V27 Poisson gives
\(E(M)=M(0)+\text{small}\), so the original physical target returns with
coefficient one.  That design is circular.

Hence

~~~text
V28_SMOOTH_MAIN_WITH_M0_EQUAL_PHYSICAL_TARGET
  = STOP_SCOPED_CIRCULAR_ZERO_AXIS_COEFFICIENT_ONE

V28_MASTER_OCCURRENCE_LOCAL_EULER_TENSOR
  = PROVED_EXACT_ALGEBRAIC

V28_LOCAL_EULER_ZERO_MEAN_RAMANUJAN_ORTHOGONALITY
  = PROVED_EXACT_ALGEBRAIC

V28_LOCAL_MAIN_JUTILA_J_PLUS_E_CANCELLATION
  = PROVED_EXACT_ALGEBRAIC
~~~

The last token is an identity for the local carrier.  A theorem that attaches
that carrier to the complete literal arithmetic main and controls the
residual is still absent.

## 4. Fourier coefficients and the short inverse-residue corridor

With normalized local DFT,

\[
\widehat F_p(0)=1,
\qquad
\widehat F_p(k)=-\frac{e_p(2k)}{p-1}\quad(k\ne0).
\tag{4.1}
\]

For \(p>z\),

\[
\widehat G_{p,z}(0)=1,
\qquad
\widehat G_{p,z}(k)=\frac1{(p-1)^2}\quad(k\ne0).
\tag{4.2}
\]

For \(p\le z\), the two transforms agree.  If \(C_{m,z}(k)\) is the
Fourier coefficient of \(\Delta_{m,z}\) modulo \(D=\operatorname{rad}m\),
then

\[
C_{m,z}(0)=0,
\qquad
\|C_{m,z}\|_1+\|C_{m,z}\|_2=x^{o(1)}.
\tag{4.3}
\]

If every prime divisor of \(m\) is at most \(z\), the whole difference is
identically zero.

For a full-lattice constant-amplitude occurrence, Poisson summation and the
compact support of \(\psi\) turn the product of a Ramanujan frequency
\(a/q\) and a local frequency \(k/D\) into

\[
n=aD+kq-\ell qD.
\tag{4.4}
\]

If \(q\nmid D\), the zero determinant is impossible because reduction
modulo \(q\) would force \(a=0\).  The active rows are exactly

\[
0<|n|\le\frac{qD}{H},\qquad q\nmid n,
\tag{4.5}
\]

with

\[
a\equiv nD^{-1}\pmod q,
\qquad
k\equiv nq^{-1}\pmod D.
\tag{4.6}
\]

Up to the fixed Fourier sign convention, the kernel is

\[
\mathcal K_q(D)=
-\frac H{L_{\rm pr}}
\sum_{\substack{0<|n|\le qD/H\\q\nmid n}}
\psi\!\left(\pm\frac{Hn}{qD}\right)
C_{m,z}(nq^{-1}\bmod D).
\tag{4.7}
\]

If \(q\mid D\), individual zero-frequency rows can be nonzero, but their
complete unit-frequency sum is zero by (3.3).  Every remaining frequency is
at distance at least \(1/D\) from an integer.  Since
\(D\le\sqrt x<H\), compact support kills those rows.  Thus

\[
\boxed{\mathcal K_q(D)=0\quad(q\mid D)}
\tag{4.8}
\]

only after the full unit-frequency reassembly and before absolute values.

If \(q\nmid D\) but \(qD<H\), (4.5) is empty.  The active corridor therefore
satisfies

\[
D\ge H/q=x^{31/96+o(1)},
\tag{4.9}
\]

and, because \(D\le x^{1/2}\),

\[
1\le qD/H\le x^{17/96+o(1)}.
\tag{4.10}
\]

At the full-radical MASTER lower edge \(D\asymp x^{133/400}\), the dual
length is

\[
x^{1/3+133/400-21/32}=x^{23/2400}.
\tag{4.11}
\]

The apparent nonunit rows have a sharper exact reduction.  Put

\[
g=(n,D),\qquad D=gR,\qquad n=ga.
\tag{4.12}
\]

Then \((a,qR)=1\), and the compact-support condition in (4.5) becomes

\[
0<|a|\le\frac{qR}{H}.
\tag{4.13}
\]

For the normalized DFT convention in (4.1), CRT gives the local frequency
\(k_p=r\overline{D/p}\pmod p\), where
\(r=n\overline q\pmod D\).  Hence \(k_p=0\) for \(p\mid g\), while for
\(p\mid R\),

\[
k_p\equiv a\overline q\,\overline{R/p}\pmod p.
\tag{4.14}
\]

The common divisor \(g\) cancels exactly.  Consequently,

\[
\widehat P_D(n\overline q)
=\frac{\mu(R)}{\varphi(R)}
 e_R(2a\overline q).
\tag{4.15}
\]

Write

\[
R=R_0R_1,\qquad
R_0=\prod_{\substack{p\mid R\\p\le z}}p,\qquad
R_1=\prod_{\substack{p\mid R\\p>z}}p.
\tag{4.16}
\]

The hybrid tensor has

\[
\widehat B_{D,z}(n\overline q)
=
\frac{\mu(R_0)}
{\varphi(R_0)\varphi(R_1)^2}
e_{R_0}\!\left(2a\overline{qR_1}\right),
\tag{4.17}
\]

where the phase equals \(1\) when \(R_0=1\).  If \(R_1=1\), the two
coefficients agree and their difference is zero.  Thus
\(C_{m,z}(n\overline q)\) is the literal difference of (4.15) and
(4.17), not a divisor-envelope substitute.

The true active radical is \(R\), not \(D\):

\[
R\ge H/q=x^{31/96+o(1)},\qquad
1\le qR/H\le x^{17/96+o(1)}.
\tag{4.18}
\]

The exponent \(23/2400\) in (4.11) describes only the primitive
\(g=1\), full-radical lower-MASTER subcell.  General rows can begin at
unit reduced length.  Both signs, \(g>1\), the \(R_0/R_1\) split and the
conditions \(q\mid D\) versus \(q\mid n\) remain literal: \(q\mid n\) is
forbidden in (4.5), whereas \(q\mid D\) cancels only collectively.

## 5. Bulk and endpoint loss ledger

The local Fourier coefficients satisfy

\[
|C_{m,z}(nq^{-1})|
\le x^{o(1)}\frac{(n,D)}D,
\qquad
\sum_{1\le n\le N}(n,D)\le N\tau(D).
\tag{5.1}
\]

Together with

\[
\sum_{o:t(o)=t}|a_o|
\le2d_2(t)+d_4(t)\le3d_4(t),
\tag{5.2}
\]

this gives the absolute bulk ceiling

\[
\boxed{|E(M_x^{\rm loc})|\le x^{1+o(1)}.}
\tag{5.3}
\]

It misses the required \(x^{399/400}\) by exactly \(1/400\).  An independent
bulk theorem must therefore prove a fixed signed saving

\[
\eta>1/400.
\tag{5.4}
\]

The hard-shell endpoint is not the first fatal.  Choose

\[
Y=Hx^\varepsilon,
\qquad 0<\varepsilon<11/600.
\tag{5.5}
\]

The two boundary layers have cost

\[
Y\frac HQx^{o(1)}
=x^{47/48+\varepsilon+o(1)},
\tag{5.6}
\]

and

\[
\frac{399}{400}-\frac{47}{48}=\frac{11}{600}.
\tag{5.7}
\]

Hence

~~~text
V28_LOCAL_MAIN_SHARED_Q_DIVIDES_RADICAL_BRANCH
  = PROVED_EXACT_AFTER_FULL_UNIT_FREQUENCY_SUM

V28_LOCAL_MAIN_HARD_SHELL_ENDPOINT
  = PROVED_ELEMENTARY_X_47_OVER_48_PLUS_EPSILON
~~~

### 5.1 A conditional Bettin--Chandee corridor engine

The reduced phase (4.15) is a genuine Kloosterman fraction.  Its coefficient
size is not an extra conjecture.  For every exact selected MASTER group
\(M\), the V19 occurrence rules give

\[
\sum_{\substack{o:m(o)=M\\t(o)\in T}}|a_o|
\le
3d_4(M)\sum_{n\le x/M}d_4(n)
\ll \frac{x^{1+o(1)}}M
\tag{5.8}
\]

uniformly for any restriction \(T\subseteq I_x\).  This uses the actual
ordered \(+2,-1\) families, units in their original slots, and
\(|\log f_1/\log t|\le1\).  Deterministic routing selects only one \(M\)
per occurrence.  Since

\[
\sum_{\operatorname{rad}M=D}\frac1M
\le
\prod_{p\mid D}\sum_{\nu\ge1}p^{-\nu}
=\frac1{\varphi(D)},
\tag{5.9}
\]

the total signed coefficient \(A_T(D)\) satisfies

\[
|A_T(D)|\le \frac{x^{1+o(1)}}{\varphi(D)}.
\tag{5.10}
\]

After \(D=gR\), the \(F\)-corridor amplitude in (4.15) therefore obeys

\[
|B_F(R)|
\le
\frac1{\varphi(R)}
\sum_{\substack{g\le\sqrt x/R\\(g,R)=1}}
|A_T(gR)|
\ll \frac{x^{1+o(1)}}{R^2},
\tag{5.11}
\]

and on a dyadic block \(R\asymp S\),

\[
\|B_F\|_2\ll \frac{x^{1+o(1)}}{S^{3/2}}.
\tag{5.12}
\]

For the \(G\)-corridor, fix \(R_1\) and let \(R_0\asymp S\).  Formula
(4.17) similarly gives

\[
\|B_G(\,\cdot\,;R_1)\|_2
\ll
\frac{x^{1+o(1)}}{S^{3/2}R_1^3}.
\tag{5.13}
\]

Summing exact \(R_1\asymp L\) after the local estimate costs at most \(L\),
leaving \(L^{-2}\).  Möbius inversion for \((a,R)=1\) gains a convergent
\(d^{-2+o(1)}\) factor in the \(F\) branch, and
\(d_0^{-2+o(1)}d_1^{-3+o(1)}\) in the \(G\) branch.  Thus it causes no
power loss.  These are elementary coefficient envelopes; they are not a
claim that hard-shell smoothing and signed reassembly have already been
compiled.

Now let \(R=x^\rho\) and

\[
A=\frac{QR}{H}=x^{\rho-31/96}.
\tag{5.14}
\]

Bettin--Chandee, arXiv:1502.00769v1, Theorem 1, accepts arbitrary
coefficient trilinear Kloosterman fractions after a valid smooth dyadic
emitter has produced its three arrays.  For the \(F\) branch the parameter
map is

\[
(A,M,N)=(QR/H,Q,R),\qquad \vartheta=\pm2.
\tag{5.15}
\]

The prime-\(q\) array has \(L^2\)-norm \(Q^{1/2+o(1)}\), the short
\(a\)-array has norm \(A^{1/2+o(1)}\), and the \(R\)-array has the norm
in (5.12).  The outside normalization is \(H/L_{\rm pr}\).  Substituting
these four factors into both terms of the theorem gives

\[
\mathfrak E_F(\rho)\le
\begin{cases}
\displaystyle \frac{2077}{1920}-\frac{3\rho}{10},
 &31/96\le\rho\le1/3,\\[6pt]
\displaystyle \frac{639}{640}-\frac{\rho}{20},
 &1/3\le\rho\le1/2.
\end{cases}
\tag{5.16}
\]

The branches agree at \(\rho=1/3\), where they equal \(377/384\).
The worst endpoint is

\[
\mathfrak E_F(31/96)=\frac{1891}{1920},
\qquad
\frac{399}{400}-\frac{1891}{1920}
=\frac{121}{9600}>0.
\tag{5.17}
\]

The second Bettin--Chandee term is at most \(737/768\) for
\(\rho\le1/3\), and at most \(23/24\) for \(\rho\ge1/3\).  For the
\(G\) branch the exact-\(R_1\) parameter map is

\[
(A,M,N)=(QR_0R_1/H,QR_1,R_0),
\tag{5.18}
\]

where \(m=qR_1\) is a sparse coefficient array and
\((m,n)=1\) is retained by the Möbius coprimality split.  If
\(R_0=x^\sigma\), \(R_1=x^\lambda\), then (5.13) gives for the first
\(G\)-term

\[
\begin{cases}
\displaystyle
\frac{2077}{1920}-\frac{3\sigma}{10}-\frac{11\lambda}{20},
 &\max(\sigma,1/3+\lambda)=1/3+\lambda,\\[6pt]
\displaystyle
\frac{1917}{1920}-\frac{\sigma}{20}-\frac{4\lambda}{5},
 &\max(\sigma,1/3+\lambda)=\sigma.
\end{cases}
\tag{5.19}
\]

Under \(\sigma+\lambda\ge31/96\), its worst endpoint is again
\((\sigma,\lambda)=(31/96,0)\), hence \(1891/1920\).

The second \(G\)-term is

\[
\mathfrak E_{G,2}(\sigma,\lambda)\le
\begin{cases}
\displaystyle 1-\frac{\sigma}{8}-\frac{\lambda}{2},
 &1/3+\lambda\ge\sigma,\\[6pt]
\displaystyle \frac{23}{24}-\frac{5\lambda}{8},
 &\sigma\ge1/3+\lambda.
\end{cases}
\tag{5.20}
\]

The first branch is at most
\(1-31/768=737/768\), and the second is at most \(23/24\).
Thus both Bettin--Chandee terms for both \(F\) and \(G\) branches lie
strictly below \(399/400\), conditional on the exact emitter and
reassembly.

This is a real source-backed local engine with a positive \(1/400\)
margin.  It is still conditional on an exact emitter that preserves the
moving \(R_0/R_1\) split, smooth weights, both signs, \(q\mid D\)
pre-cancellation, hard-shell endpoints and one collective outer absolute
value.  Bettin--Chandee does not estimate the residual \(e_x\) and does not
prove the complete TPC scalar.

~~~text
V28_SELECTED_MASTER_RADICAL_L2_ENVELOPE
  = PROVED_ELEMENTARY_FROM_ORDERED_D2_D4_AND_RADICAL_EULER_SUM

V28_SHORT_INVERSE_RESIDUE_BETTIN_CHANDEE_CORRIDOR
  = SOURCE_BACKED_POWER_SAVING_AFTER_EXACT_COMPILER

V28_LITERAL_MASTER_CORRIDOR_SMOOTH_EMITTER_AND_G_REASSEMBLY
  = OPEN_EXACT_COMPILER
~~~

## 6. Direct residual energy and product-local flatness

After the local carrier is removed, put

\[
\mathcal N_e^2=
\sum_{0<|h|<x/2}
|\widehat\psi_+(h/H)|\,|e_x(h)|^2.
\tag{6.1}
\]

The V27 coefficient norm gives the sufficient target

\[
\boxed{
\mathcal N_e\ll x^{1+\theta+\varepsilon},
\qquad \theta<13/4800.}
\tag{6.2}
\]

Let

\[
\mathcal B_x(\alpha)=\sum_{t\in I_x}\beta_x^{\rm raw}(t)e(t\alpha),
\qquad
\mathcal W_x(\alpha)=\sum_{u\in I_x}w_x^{(z)}(u)e(u\alpha).
\tag{6.3}
\]

The correlation \(r_x(h)\) is a Fourier coefficient of the product
\(\mathcal B_x\overline{\mathcal W_x}\), with the sign determined by the
chosen Fourier convention.  The abstract finite-support circle-method
reduction in Matomaki--Radziwill--Tao, arXiv:1707.01315v3, Proposition 3.1,
motivates the following literal sufficient theorem: uniformly for every
dyadic \(Y\ge H\) and every interval \(I\) of length \(1/Y\) in the
declared minor region,

\[
\boxed{
\int_I|\mathcal B_x(\xi)\mathcal W_x(\xi)|\,d\xi
\ll \frac{x^{1+2\theta+\varepsilon}}Y,
\qquad \theta<13/4800.}
\tag{6.4}
\]

Together with a separately paid major/local-main branch and the dyadic
Schwartz tail, (6.4) is a product-local flatness contract sufficient for
the squared form of (6.2).  A stronger factorized sufficient form asks for
two-sided local \(L^2\) flatness of both \(\mathcal B_x\) and
\(\mathcal W_x\).  Existing MRT/MRSTT inputs do not prove either statement
for the literal MASTER-routed \(\beta_x^{\rm raw}\) and hybrid residual.

One-sided local control on only the prime residual leaves a norm scale
\(xH^{1/4}=x^{1+21/128}\), far above (6.2).  Scalar log savings, an
almost-all set of shifts, or triangle over rational phases cannot pay a
fixed power gap.

The exact source normalization and the deduction from (6.4) remain a
source-attachment gate until independently audited against the final
major/minor partition.  No arithmetic theorem is claimed here.

~~~text
V28_MRT_ABSTRACT_PRODUCT_LOCAL_L2_REDUCTION
  = SOURCE_BACKED_ABSTRACT_INTERFACE_ONLY

V28_LITERAL_BILINEAR_PRODUCT_LOCAL_FLATNESS
  = OPEN_NEW_THEOREM

V28_ONE_SIDED_MRT_TO_ENDPOINT
  = STOP_SCOPED_H_QUARTER_LOSS

V28_TAGGED_RESIDUAL_JUTILA_MAIN_ERROR_REASSEMBLY
  = SELECTED_PRIMARY_OPEN_ATTACHMENT
~~~

## 7. Stationary mixing cannot carry the arithmetic clock

Let \((Y,\nu,T)\) be mixing and suppose, for an integer \(M\ge2\), there is
a measure-preserving factor

\[
\pi:Y\to\mathbb Z/M\mathbb Z,
\qquad
\pi(Ty)=\pi(y)+1\pmod M.
\tag{7.1}
\]

The pushforward invariant probability is uniform.  With
\(\zeta_M=e^{2\pi i/M}\), the function

\[
f(y)=\zeta_M^{\pi(y)}
\tag{7.2}
\]

is nonconstant, has mean zero and satisfies \(f\circ T=\zeta_M f\).
Consequently,

\[
\int(f\circ T^n)\overline f\,d\nu=\zeta_M^n
\tag{7.3}
\]

does not tend to zero, contradicting mixing.  Weak mixing already suffices.
Any factor onto the profinite odometer composes with a nontrivial finite
quotient and gives the same contradiction.

This stops stationary exact Logistic/CE or mixing Hénon factors to the
arithmetic clock.  It does not stop stage-dependent nonautonomous maps
\(\pi_{j+1}\circ F_j=R_j\circ\pi_j\), because there is then no fixed
Koopman eigenfunction.  Existing parameter or sequential ASIP theorems do
not supply the required growing triangular CE family and common pointed
parameter.

~~~text
V28_STATIONARY_MIXING_TO_ROTATION_ODOMETER_FACTOR
  = STOP_SCOPED_ROOT_OF_UNITY_EIGENFUNCTION_NO_GO

V28_NONAUTONOMOUS_POINTED_ESCAPE
  = LOGICALLY_OPEN_EXACT_STAGE_DIAGRAM_REQUIRED
~~~

## 8. The compressed kernel carrier and its exact threshold

Let \(x_j\) be the predeclared disjoint safe schedule and

\[
B_j^{\rm arith}
=\sum_{x_j/2<t\le x_j}
\mathbf1_{\{t,t+2\ \mathrm{prime}\}}.
\tag{8.1}
\]

The genuine third carrier asks for one common probability space \((C,\nu)\),
one fixed parameter and critical seed across all stages, a nonconstant block
\(S_j\ge0\), and real-valued \(L^2(\nu)\) objects \(K_j,S_j\), with
\(K_j\) target-independent, such that

\[
\int_C K_j\,d\nu=1,
\qquad
\boxed{B_j^{\rm arith}=\int_CK_j(a)S_j(a)\,d\nu(a).}
\tag{8.2}
\]

Suppose a physical main and fluctuation obey

\[
m_j\ge c\frac{x_j}{\log^2x_j},
\qquad
V_j=\|S_j-m_j\|_{L^2(\nu)}.
\tag{8.3}
\]

Cauchy gives

\[
B_j^{\rm arith}
\ge m_j-\|K_j\|_2V_j.
\tag{8.4}
\]

Thus the exact sufficient loss condition is

\[
\boxed{
\|K_j\|_2V_j=o(x_j/\log^2x_j).}
\tag{8.5}
\]

If \(V_j^2=O(x_j)\), this becomes

\[
\boxed{
\|K_j\|_2=o(\sqrt{x_j}/\log^2x_j).}
\tag{8.6}
\]

The natural full-primorial point-evaluation kernel fails exactly.  Let

\[
M_j=P(\sqrt{x_j+2})=\prod_{p\le\sqrt{x_j+2}}p.
\tag{8.7}
\]

On \(\mathbb Z/M_j\mathbb Z\) with normalized Haar measure, the unique
Riesz representer of \(f\mapsto f(0)\) is

\[
K_j(r)=M_j\mathbf1_{\{r=0\}},
\tag{8.8}
\]

so

\[
\|K_j\|_1=1,
\qquad
\|K_j\|_2=\sqrt{M_j},
\qquad
\|K_j\|_\infty=M_j.
\tag{8.9}
\]

The prime number theorem gives

\[
\boxed{
\|K_j\|_2
=\exp\!\left((1/2+o(1))\sqrt{x_j}\right).}
\tag{8.10}
\]

Chebyshev bounds already give \(\exp(\Theta(\sqrt{x_j}))\), enough for the
STOP.  This overwhelms (8.6).  It stops only full-cylinder evaluation, not
a smaller target-independent physical quotient.

Two finite examples prevent false positivity claims.  On two equally
weighted points,

\[
K=(3,-1),\quad S=(1,3)
\quad\Longrightarrow\quad
\int K=1,\ S>0,\ \int KS=0.
\tag{8.11}
\]

A signed kernel can therefore erase parameterwise positivity.  Even with

\[
K=(2,0),\quad S=(0,1),
\tag{8.12}
\]

a positive block at one parameter does not control the kernel-weighted bad
set.  The norm ledger (8.5), or a stronger nonnegative conditional-
expectation theorem, is indispensable.

~~~text
V28_POSITIVE_MEAN_WITHOUT_KERNEL_COVARIANCE_CONTROL
  = STOP_SCOPED_EXACT_TWO_POINT_FALSIFIERS

V28_FULL_PRIMORIAL_POINT_RIESZ_NORM
  = PROVED_EXACT_FINITE_PLUS_STANDARD_PNT_ASYMPTOTIC

V28_LOW_NORM_POINT_EVALUATION_KERNEL_CRITERION
  = PROVED_EXACT_ALGEBRAIC

V28_COMPRESSED_TARGET_INDEPENDENT_KERNEL_WHOLE_SHELL_COMPILER
  = SELECTED_DYNAMICS_OPEN_NEW_THEOREM
~~~

## 9. Source and geometry boundaries

The reviewed source interfaces remain sharply typed:

1. Matomaki--Radziwill--Tao, arXiv:1707.01315v3, Proposition 3.1, is an
   abstract finite-support circle-method energy reduction.  It does not
   prove literal product-local flatness.
2. Bettin--Chandee, arXiv:1502.00769v1, Theorem 1, supplies the
   trilinear Kloosterman-fraction estimate used in (5.16)--(5.20).  It is
   a conditional local engine only after the literal reduced-radical
   arrays and their collective smoothing/reassembly have been emitted.
3. Aspenberg--Baladi--Persson, arXiv:2212.12202v2, Theorem 1.1, treats the
   Logistic critical seed \(1/2\) for one fixed Holder observable on an
   almost-everywhere parameter space.  It does not give a common growing
   triangular carrier.
4. Haydn--Nicol--Torok--Vaienti, arXiv:1406.4266, Theorem 3.1, requires
   uniform expanding DFLY/LB hypotheses, uniformly bounded observable norm
   and variance growth.  It does not directly attach to CE Logistic
   primorial cylinders.
5. Boronski--Stimac, arXiv:2104.14780, prove a source-backed natural-
   extension description for Wang--Young Hénon attractors over a densely
   branching metric tree.  This is real topological geometry, but not a
   Logistic interval, residue odometer or TPC physical section.

Accordingly,

~~~text
V28_ABP_HNTV_INTERFACES
  = SOURCE_BACKED_TOOL_CLASSES_ONLY

V28_HENON_WANG_YOUNG_DENSE_TREE_NATURAL_EXTENSION
  = SOURCE_BACKED_TOPOLOGICAL_GEOMETRY_ONLY

V28_HENON_TPC_STAGE_EVENT_MEASURE_SEED_FUNCTIONAL_DIAGRAM
  = OPEN_ATTACHMENT
~~~

The Euler tensors, Fourier coefficients and finite-dimensional Riesz norms
are exact algebra.  The missing arithmetic steps remain:

~~~text
uniform actual AP attachment of the occurrence Euler carrier;
literal reduced-radical smooth emitter and collective G reassembly;
short inverse-residue Bettin--Chandee corridor completion;
tagged residual product-local flatness and weighted L2;
joint Jutila main/error reassembly for the same residual;
all hard physical cover, normalization, A/B and provenance gates.
~~~

## 10. Route decision and reopen gates

The canonical status atlas, shared verbatim with the checker and release
documents, is:

~~~text
V28_MAXIMUM_CLAIM = EXACT_OCCURRENCE_NATIVE_EULER_ZERO_AXIS_AND_REDUCED_RADICAL_CORRIDOR_PLUS_SOURCE_BACKED_CONDITIONAL_BETTIN_CHANDEE_ENGINE_PLUS_STATIONARY_FACTOR_NO_GO_AND_COMPRESSED_KERNEL_ROUTE
V28_ROUTE_ADVANCE = YES
V28_ARITHMETIC_ADVANCE = NO
V28_FIXED_ATOM_CREDIT = 0
V28_STRICT_1_OVER_400 = UNPAID
V28_L2 = NONE
V28_TPC_207_TRIGGER = false
V28_NUMBERED_RELEASE = NO
V28_MASTER_OCCURRENCE_LOCAL_EULER_TENSOR = PROVED_EXACT_ALGEBRAIC
V28_LOCAL_EULER_ZERO_MEAN_RAMANUJAN_ORTHOGONALITY = PROVED_EXACT_ALGEBRAIC
V28_LOCAL_EULER_TENSOR_AS_ACTUAL_WEIGHTED_AP_MAIN = OPEN_ATTACHMENT
V28_SMOOTH_MAIN_WITH_M0_EQUAL_PHYSICAL_TARGET = STOP_SCOPED_CIRCULAR_ZERO_AXIS_COEFFICIENT_ONE
V28_LOCAL_MAIN_JUTILA_J_PLUS_E_CANCELLATION = PROVED_EXACT_ALGEBRAIC
V28_REDUCED_RADICAL_CRT_PHASE = PROVED_EXACT_G_CANCELLATION_AND_PLUS_TWO_PHASE
V28_LOCAL_MAIN_SHARED_Q_DIVIDES_RADICAL_BRANCH = PROVED_EXACT_AFTER_FULL_UNIT_FREQUENCY_SUM
V28_SELECTED_MASTER_RADICAL_L2_ENVELOPE = PROVED_ELEMENTARY_FROM_ORDERED_D2_D4_AND_RADICAL_EULER_SUM
V28_SHORT_INVERSE_RESIDUE_BETTIN_CHANDEE_CORRIDOR = SOURCE_BACKED_POWER_SAVING_AFTER_EXACT_COMPILER
V28_SHORT_INVERSE_RESIDUE_CORRIDOR_EXPONENT = 1891/1920
V28_SHORT_INVERSE_RESIDUE_CORRIDOR_MARGIN_TO_399_400 = 121/9600
V28_LITERAL_MASTER_CORRIDOR_SMOOTH_EMITTER_AND_G_REASSEMBLY = OPEN_EXACT_COMPILER
V28_LOCAL_MAIN_HARD_SHELL_ENDPOINT = PROVED_ELEMENTARY_X_47_OVER_48_PLUS_EPSILON
V28_MRT_ABSTRACT_PRODUCT_LOCAL_L2_REDUCTION = SOURCE_BACKED_ABSTRACT_INTERFACE_ONLY
V28_LITERAL_BILINEAR_PRODUCT_LOCAL_FLATNESS = OPEN_NEW_THEOREM
V28_ONE_SIDED_MRT_TO_ENDPOINT = STOP_SCOPED_H_QUARTER_LOSS
V28_TAGGED_RESIDUAL_JUTILA_MAIN_ERROR_REASSEMBLY = SELECTED_PRIMARY_OPEN_ATTACHMENT
V28_STATIONARY_MIXING_TO_ROTATION_ODOMETER_FACTOR = STOP_SCOPED_ROOT_OF_UNITY_EIGENFUNCTION_NO_GO
V28_NONAUTONOMOUS_POINTED_ESCAPE = LOGICALLY_OPEN_EXACT_STAGE_DIAGRAM_REQUIRED
V28_LOW_NORM_POINT_EVALUATION_KERNEL_CRITERION = PROVED_EXACT_ALGEBRAIC
V28_POSITIVE_MEAN_WITHOUT_KERNEL_COVARIANCE_CONTROL = STOP_SCOPED_EXACT_TWO_POINT_FALSIFIERS
V28_FULL_PRIMORIAL_POINT_RIESZ_NORM = PROVED_EXACT_FINITE_PLUS_STANDARD_PNT_ASYMPTOTIC
V28_COMPRESSED_TARGET_INDEPENDENT_KERNEL_WHOLE_SHELL_COMPILER = SELECTED_DYNAMICS_OPEN_NEW_THEOREM
V28_ABP_HNTV_INTERFACES = SOURCE_BACKED_TOOL_CLASSES_ONLY
V28_HENON_WANG_YOUNG_DENSE_TREE_NATURAL_EXTENSION = SOURCE_BACKED_TOPOLOGICAL_GEOMETRY_ONLY
V28_HENON_TPC_STAGE_EVENT_MEASURE_SEED_FUNCTIONAL_DIAGRAM = OPEN_ATTACHMENT
V28_O161_PARENTS_PAIR_NATIVE_H1_GLOBAL = OPEN_UNCHANGED
V28_A1_A2_TAIL_SELECTION_PACKET_PROVENANCE = INDEPENDENT_AND_UNPAID
~~~

The V28 route order is:

~~~text
ANALYTIC PRIMARY:
  exact occurrence-local Euler cancellation inside joint Jutila main+error
  + tagged residual product-local flatness / weighted L2.

ANALYTIC SECOND ROAD, NOW SOURCE-BACKED CONDITIONAL:
  reduced-radical F/G corridor
  + exact smooth emitter and collective Bettin--Chandee reassembly.

DYNAMICAL RESERVE:
  compressed target-independent nonconstant kernel whole-shell compiler.
~~~

The direct MRT/MRSTT black-box splice remains stopped.  Bettin--Chandee has
now replaced the former unspecified \(\eta>1/400\) reserve by a concrete
conditional local engine with margin \(121/9600\), but no arithmetic credit
is recorded until its literal emitter and global reassembly close.  The stationary
mixing-to-odometer factor is now stopped for a theorem-level spectral reason,
not merely because a construction was absent.

Reopening the analytic primary requires one theorem that retains:

~~~text
literal V19 occurrence IDs and selected MASTER group;
fixed physical h0=2 and actual Lambda-b_z residual;
the exact F_p/G_p tensor and tagged residual e_x;
prime-only Q=x^(1/3), H=x^(21/32), both signs and Schwartz tail;
joint Jutila main/error identity before species-wise absolute values;
weighted residual norm with theta<13/4800;
all axes, endpoints, normalization and exactly-once provenance.
~~~

Completing the analytic second road requires a narrower, now explicit
compiler:

~~~text
aggregate the actual selected MASTER groups by D=rad(M);
emit the reduced variables g=(n,D), R=D/g, a=n/g;
retain the exact F phase e_R(2a q^{-1});
retain the exact G phase on R0 with the moving rough factor R1;
perform coprimality Mobius splits without deleting nonunit source rows;
smooth the hard shell with only x^{o(1)} variation cost;
sum q|D rows before absolute values;
apply Bettin--Chandee blockwise and reassemble both signs exactly once.
~~~

Reopening the dynamics reserve requires (8.2)--(8.6) on one common parameter
space with a fixed critical seed, a target-independent kernel, a positive
physical main and an exact stage/event/measure/normalization diagram.  Future
twin-hit calibration is forbidden.

The endpoint remains:

~~~text
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
~~~

TPC-206 remains the last numbered theorem package.  No local V28 identity
automatically creates TPC-207.
