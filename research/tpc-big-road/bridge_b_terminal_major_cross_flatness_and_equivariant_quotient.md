# Bridge B V30: q-local major extraction, cell cross-flatness, and the terminal gate

Date: 2026-08-08

Status:

~~~text
EXACT_QLOCAL_MAJOR_AND_CELL_PRODUCT_REDUCTION
MAXIMUM_CLAIM = EXACT_QLOCAL_MAJOR_MODEL_X_95_OVER_96_PLUS_CELL_PRODUCT_MRT_REDUCTION_PLUS_ENDPOINT_EQUIVALENCE_PLUS_EQUIVARIANT_QUOTIENT_NO_GO
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
~~~

V29 separated the physical scalar into an independent Jutila major gate and
an off-zero weighted \(L^2\) gate.  V30 sharpens both sides without pretending
to close either one.

On the major side, the local shifted-prime and hybrid Euler densities admit an
exact \(q\)-periodic difference.  Poisson summation pays its complete model
contribution by

\[
 \mathfrak M_x^{q\mathrm{loc}}
 \ll x^{95/96+o(1)},
 \qquad
 \frac{399}{400}-\frac{95}{96}=\frac{19}{2400}.
\tag{0.1}
\]

The remainder is still a literal signed covariance and still contains the
physical zero coordinate with coefficient one.  Thus (0.1) is a genuine
major-side subgate, not an arithmetic bound for the twin-prime scalar.

On the minor side, a geometric partition of the circle turns the abstract MRT
product estimate into a strictly weaker cross-flatness condition: only
simultaneous spectral spikes of the two physical factors must be excluded.
Once that minor gate is paid, the remaining major estimate and the physical
endpoint estimate are equivalent in strict exponent class.  This changes the
research order to minor first, terminal major second, and dynamics third.

Finally, an exact finite theorem closes one tempting dynamical shortcut: on a
full cyclic coordinate space, a translation-equivariant quotient through
which point evaluation factors must be injective.  Only a symmetry-breaking
arithmetic carrier remains open.

## 1. Frozen object, Fourier sign, and the exact \(J\)-scalar

Keep the V19/V21/V27--V29 object literally:

\[
 h_0=2,\qquad I_x=(x/2,x]\cap\mathbb Z,\qquad z=(\log x)^K,
\tag{1.1}
\]

\[
 w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u),
\qquad
 r_x(h)=\sum_{\substack{t,t+h\in I_x}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(t+h).
\tag{1.2}
\]

The coefficient \(\beta_x^{\rm raw}\) retains every occurrence ID, source
slot, ordered \(+2,-1\), Möbius and logarithmic weight, unit slot,
MASTER/H2 route, multiplicity, and \(1/\log t\).  Write the complete labelled
occurrence expansion as

\[
 \beta_x^{\rm raw}(t)=\sum_{o:t_o=t}a_o,
 \qquad
 a_o=c_{j(o)}\prod_i\mu(e_i(o))
       \frac{\log f_1(o)}{\log t_o},
 \quad c_1=+2,\ c_2=-1.
\tag{1.3}
\]

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

and

\[
 \kappa_x(h)=
 \frac{\widehat\psi_+(h/H)A_Q(h)}{L_{\rm pr}},
 \qquad
 \widehat\psi_+(\xi)=\int_{\mathbb R}\psi(v)e(+\xi v)\,dv.
\tag{1.6}
\]

Here \(\psi:\mathbb R\to[0,1]\) is smooth, supported on \([-1,1]\),
and \(\int\psi=1\).  Thus \(\widehat\psi_+(0)=1\) and
\(\kappa_x(0)=1\).  Define

\[
 J(f)=\sum_h\kappa_x(h)f(h),\qquad
 E(f)=f(0)-J(f)=-\sum_{h\ne0}\kappa_x(h)f(h).
\tag{1.7}
\]

Let \(M_x^{\rm loc}\) be the V28/V29 occurrence-native Euler carrier and

\[
 e_x(h)=r_x(h)-M_x^{\rm loc}(h),
 \qquad M_x^{\rm loc}(0)=0.
\tag{1.8}
\]

Then

\[
 \boxed{S_x^{\rm physical}=e_x(0)=J(e_x)+E(e_x).}
\tag{1.9}
\]

For sign auditing, put

\[
 \chi_x(\alpha)=\frac H{L_{\rm pr}}
 \sum_{q\in\mathcal Q}\sum_{a\bmod q}^{*}\sum_{k\in\mathbb Z}
 \psi\!\left(H\left(\alpha-\frac aq+k\right)\right).
\tag{1.10}
\]

Direct substitution gives

\[
 \int_{\mathbb T}\chi_x(\alpha)e(+h\alpha)\,d\alpha
 =\kappa_x(h).
\tag{1.11}
\]

With

\[
 G_x(\alpha)=\sum_{t,u\in I_x}
 \beta_x^{\rm raw}(t)w_x^{(z)}(u)e((u-t)\alpha),
\tag{1.12}
\]

one has \(J(r_x)=\int\chi_xG_x\).  With the V29 convention

\[
 \mathcal B_x(\alpha)=\sum_t\beta_x^{\rm raw}(t)e(t\alpha),
 \qquad
 \mathcal W_x(\alpha)=\sum_uw_x^{(z)}(u)e(u\alpha),
\tag{1.13}
\]

the same scalar is

\[
 J(r_x)=\int_{\mathbb T}\chi_x(-\alpha)
 \mathcal B_x(\alpha)\overline{\mathcal W_x(\alpha)}\,d\alpha.
\tag{1.14}
\]

The reflection in (1.14) is forced by the already frozen signs.  It may not
be removed unless an additional evenness hypothesis is declared.

## 2. The endpoint-equivalence theorem and the adjoint normal form

Let

\[
 \tau=\frac{399}{400}.
\tag{2.1}
\]

Suppose the off-zero gate has already paid

\[
 |E(e_x)|\ll x^{\tau-\eta_E},\qquad \eta_E>0.
\tag{2.2}
\]

Then the two identities

\[
 S_x^{\rm physical}=J(e_x)+E(e_x),\qquad
 J(e_x)=S_x^{\rm physical}-E(e_x)
\tag{2.3}
\]

give the following exact implication pair:

\[
 |J(e_x)|\ll x^{\tau-\eta_J}
 \Longrightarrow
 |S_x^{\rm physical}|\ll x^{\tau-\min(\eta_J,\eta_E)+o(1)},
\tag{2.4}
\]

\[
 |S_x^{\rm physical}|\ll x^{\tau-\eta_S}
 \Longrightarrow
 |J(e_x)|\ll x^{\tau-\min(\eta_S,\eta_E)+o(1)}.
\tag{2.5}
\]

Thus, after the minor payment, the independent major theorem and the physical
theorem are equivalent in strict fixed-power class.  The major gate remains
necessary, but it is not a strictly easier preliminary theorem.

The V27 coefficient norm and V29 off-zero contract give

\[
 |E(e_x)|\ll x^{191/192+\theta+\varepsilon_N+o(1)},
\tag{2.6}
\]

and

\[
 \frac{399}{400}-\frac{191}{192}=\frac{13}{4800}.
\tag{2.7}
\]

Hence (2.2) has a strict positive margin only when

\[
 \boxed{\theta+\varepsilon_N<\frac{13}{4800}.}
\tag{2.8}
\]

There is also an exact adjoint rewrite.  Define

\[
 (T_\kappa w)(t)=\sum_h\kappa_x(h)w(t+h).
\tag{2.9}
\]

Finite reindexing yields

\[
 J(r_x)=\sum_t\beta_x^{\rm raw}(t)(T_\kappa w_x^{(z)})(t),
\tag{2.10}
\]

and therefore

\[
 J(e_x)=\sum_t\beta_x^{\rm raw}(t)(T_\kappa w_x^{(z)})(t)
 -J(M_x^{\rm loc}).
\tag{2.11}
\]

Formula (2.11) is a useful bilinear normal form, not a saving.

## 3. The exact \(q\)-local density tensor

For sufficiently large \(x\), every \(q\in\mathcal Q\) satisfies \(q>z\).
Fix \(a\bmod q\) and define

\[
 F_{q,a}(h)=\frac q{q-1}
 \mathbf1_{a+h+2\not\equiv0\pmod q},
\tag{3.1}
\]

\[
 G_{q,a}(h)=
 \begin{cases}
 q/(q-1),&a+h\equiv0\pmod q,\\
 q(q-2)/(q-1)^2,&a+h\not\equiv0\pmod q,
 \end{cases}
\tag{3.2}
\]

and

\[
 \Delta_{q,a}(h)=F_{q,a}(h)-G_{q,a}(h).
\tag{3.3}
\]

Equivalently, with \(u=a+h\), the profile \(\Gamma_q(u)\) is

\[
 \Gamma_q(u)=
 \begin{cases}
 -q(q-2)/(q-1)^2,&u\equiv-2\pmod q,\\
 0,&u\equiv0\pmod q,\\
 q/(q-1)^2,&u\not\equiv0,-2\pmod q.
 \end{cases}
\tag{3.4}
\]

The identities

\[
 \frac1q\sum_{h\bmod q}\Delta_{q,a}(h)=0,
\tag{3.5}
\]

\[
 \frac1q\sum_{h\bmod q}c_q(h)\Delta_{q,a}(h)
 =\Delta_{q,a}(0)=:\delta_q(a)
\tag{3.6}
\]

are exact.  Explicitly,

\[
 \delta_q(a)=
 \begin{cases}
 -q(q-2)/(q-1)^2,&a\equiv-2\pmod q,\\
 0,&a\equiv0\pmod q,\\
 q/(q-1)^2,&\text{otherwise},
 \end{cases}
\tag{3.7}
\]

so

\[
 \sum_{a\bmod q}\delta_q(a)=0,
 \qquad
 \sum_{a\bmod q}|\delta_q(a)|
 =\frac{2q(q-2)}{(q-1)^2}<2.
\tag{3.8}
\]

The interpretation is deliberately limited.  \(F\) is the formal local
shifted-prime density and \(G\) is the corresponding external
\(q>z\) hybrid Euler density.  Equations (3.1)--(3.8) do not assert a
weighted prime-distribution theorem for the physical coefficients.

## 4. Poisson extraction and the \(x^{95/96}\) payment

Because \(H>2Q\) eventually and \(\operatorname{supp}\psi\subset[-1,1]\),
all nonzero period aliases lie outside the support.  Periodic Poisson summation
and (3.6) give

\[
 \boxed{
 \sum_{h\in\mathbb Z}\widehat\psi_+(h/H)c_q(h)
 \Delta_{q,a}(h)=H\psi(0)\delta_q(a).}
\tag{4.1}
\]

The constant is \(H\psi(0)\), not
\(H\widehat\psi_+(0)=H\).  The latter normalization only proves
\(\kappa_x(0)=1\).

For all labelled occurrences, define the finite hard-shell model and residual

\[
 \mathfrak M_x^{q\mathrm{loc}}=
 \frac1{L_{\rm pr}}\sum_{q\in\mathcal Q}\sum_o a_o
 \sum_{\substack{h\\t_o+h\in I_x}}
 \widehat\psi_+(h/H)c_q(h)\Gamma_q(t_o+h),
\tag{4.2}
\]

\[
 \mathfrak R_x^{q\mathrm{loc}}=
 \frac1{L_{\rm pr}}\sum_{q\in\mathcal Q}\sum_o a_o
 \sum_{\substack{h\\t_o+h\in I_x}}
 \widehat\psi_+(h/H)c_q(h)
 \bigl(w_x^{(z)}(t_o+h)-\Gamma_q(t_o+h)\bigr).
\tag{4.3}
\]

Every occurrence, including every MASTER/H2 route, appears exactly once in
each side of the split.  Thus

\[
 \boxed{J(r_x)=\mathfrak M_x^{q\mathrm{loc}}
 +\mathfrak R_x^{q\mathrm{loc}}.}
\tag{4.4}
\]

The ordered divisor envelope gives

\[
 \sum_{o:t_o=t}|a_o|\le2d_2(t)+d_4(t)\le3d_4(t)=x^{o(1)}.
\tag{4.5}
\]

From

\[
 |\delta_q(t)|\le\mathbf1_{q\mid t+2}+\frac2q
\tag{4.6}
\]

one obtains

\[
 \sum_o|a_o|\,|\delta_q(t_o)|\ll\frac{x^{1+o(1)}}q.
\tag{4.7}
\]

The complete-lattice bulk is consequently

\[
 |\mathfrak M_{x,\mathrm{full}}^{q\mathrm{loc}}|
 \ll\frac H{L_{\rm pr}}\sum_{q\in\mathcal Q}\frac{x^{1+o(1)}}q
 \ll\frac{xH}{Q^2}x^{o(1)}
 =x^{95/96+o(1)}.
\tag{4.8}
\]

Use the same V29 exact cover

\[
 Y=Hx^\varepsilon,
 \qquad 0<\varepsilon<\frac{11}{1920}.
\tag{4.9}
\]

The boundary contribution is

\[
 \ll Y\frac HQx^{o(1)}
 =x^{47/48+\varepsilon+o(1)},
\tag{4.10}
\]

while the interior tail begins at \(|h|\ge Y\) and is paid by
arbitrary-order Schwartz decay.  Since

\[
 \frac{95}{96}-\left(\frac{47}{48}+\frac{11}{1920}\right)
 =\frac3{640},
\tag{4.11}
\]

the boundary is strictly smaller.  Therefore

\[
 \boxed{\mathfrak M_x^{q\mathrm{loc}}\ll x^{95/96+o(1)}.}
\tag{4.12}
\]

Together with the V29 bound

\[
 J(M_x^{\rm loc})\ll x^{1891/1920+o(1)},
\tag{4.13}
\]

and

\[
 \frac{95}{96}-\frac{1891}{1920}=\frac3{640},
\tag{4.14}
\]

the exact reassembly (4.4) yields

\[
 \boxed{
 J(e_x)=\mathfrak R_x^{q\mathrm{loc}}
 +O\!\left(x^{95/96+o(1)}\right).}
\tag{4.15}
\]

The model margin to the endpoint is

\[
 \boxed{\frac{399}{400}-\frac{95}{96}=\frac{19}{2400}.}
\tag{4.16}
\]

## 5. Unit, nonunit, diagonal, and circularity ledger

For prime \(q\), the Jutila numerator is a unit:

\[
 \sum_{a\bmod q}^{*}e_q(a(u-t))
 =q\mathbf1_{u\equiv t\pmod q}-1=c_q(u-t).
\tag{5.1}
\]

The \(-1\) term is exactly the compensation for adding the nonunit
\(a=0\).  It may not be dropped.  The congruence branch contains both
\(u-t=qk\ne0\) and the diagonal \(u=t\).

At \(u=t\), the coefficient for each \(q\) is \(q-1\); summing and dividing
by \(L_{\rm pr}\) leaves the physical scalar with coefficient one.  The
q-local model diagonal satisfies

\[
 D_x^{q\mathrm{loc}}=
 \frac1{L_{\rm pr}}\sum_{q\in\mathcal Q}(q-1)
 \sum_o a_o\Gamma_q(t_o)
 \ll x^{2/3+o(1)}.
\tag{5.2}
\]

Hence the residual diagonal is

\[
 \boxed{
 S_x^{\rm physical}-D_x^{q\mathrm{loc}}
 =S_x^{\rm physical}+O(x^{2/3+o(1)}).}
\tag{5.3}
\]

Neither the q-local subtraction nor \(M_x^{\rm loc}(0)=0\) cancels the
unknown target.  The first major-side open theorem is therefore

\[
 \boxed{
 |\mathfrak R_x^{q\mathrm{loc}}|
 \ll x^{399/400-\eta_R}}
\tag{5.4}
\]

for some fixed \(\eta_R>0\), on the same occurrence ledger, prime shell,
hard endpoints, signs, and one outer absolute value.  Estimating
\(J(e_x)=S_x^{\rm physical}-E(e_x)\) instead is circular.

## 6. The cell-product cross-flatness compiler

Fix one predeclared measurable hard major set
\(\mathfrak M\subset\mathbb T\), and put
\(\mathfrak m=\mathbb T\setminus\mathfrak M\).  For an integer dyadic
\(Y\), partition \(\mathbb T\) into \(2Y\) half-open cells

\[
 I_j=\left[\frac j{2Y},\frac{j+1}{2Y}\right),
 \qquad 0\le j<2Y.
\tag{6.1}
\]

Define

\[
 u_j=\|\mathcal B_x\|_{L^2(I_j\cap\mathfrak m)},\qquad
 v_j=\|\mathcal W_x\|_{L^2(I_j\cap\mathfrak m)},\qquad
 c_j=u_jv_j.
\tag{6.2}
\]

Cellwise Cauchy--Schwarz gives

\[
 P_0:=\int_{\mathfrak m}|\mathcal B_x\mathcal W_x|
 \le\|c\|_1.
\tag{6.3}
\]

Every circular interval of length \(1/Y\) meets at most three cells in
positive measure.  Thus

\[
 P_Y:=\sup_\alpha
 \int_{\mathfrak m\cap[\alpha-1/(2Y),\alpha+1/(2Y)]}
 |\mathcal B_x\mathcal W_x|
 \le3\|c\|_\infty.
\tag{6.4}
\]

MRT, arXiv:1707.01315v3, Proposition 3.1, supplies the abstract reduction

\[
 \sum_{|h-h_*|\le Y}|r_x(h)-MT_{\mathfrak M,h}|^2
 \ll YP_0P_Y.
\tag{6.5}
\]

Combining (6.3)--(6.5) gives the exact compiler

\[
 \boxed{
 \sum_{|h-h_*|\le Y}|r_x(h)-MT_{\mathfrak M,h}|^2
 \ll3Y\|c\|_1\|c\|_\infty.}
\tag{6.6}
\]

The cell-index Cauchy inequality and the literal divisor envelopes give

\[
 \|c\|_1\le\|\mathcal B_x\|_2\|\mathcal W_x\|_2
 \ll x^{1+o(1)}.
\tag{6.7}
\]

It is therefore enough to prove, uniformly for every dyadic
\(H\le Y\le x\),

\[
 \boxed{
 \|c\|_\infty
 \ll\frac{x^{1+2\theta+2\varepsilon_N}}Y,}
\tag{6.8}
\]

with \(\theta+\varepsilon_N<13/4800\).  This is a theorem about joint
spectral collisions, not about either factor separately.

It is strictly weaker than two individual local-flatness theorems.  For
any \(R>1\), take

\[
 u=(R,R^{-1}),\qquad v=(R^{-1},R),\qquad c=(1,1).
\tag{6.9}
\]

Then \(\|c\|_\infty=1\) while both marginal maxima tend to infinity with
\(R\).

Two additional gates remain.  One must prove the literal attachment

\[
 MT_{\mathfrak M,h}=M_x^{\rm loc}(h)+a_x(h)
\tag{6.10}
\]

and the required weighted \(L^2\) bound for the same \(a_x\).  Merely
defining \(a_x\) by (6.10) is vacuous.  Also, \(\mathfrak M\) must be
predeclared.  If a common spike is observed first and its cell is then
moved into the major set, the minor certificate becomes zero while the
whole target has merely been renamed as major mass.

## 7. Primary-source boundary

The finite source screen supports the following exact roles.

1. Blomer--Li, arXiv:2511.03294v1, Lemma 1, supplies the Jutila
   approximant and its Ramanujan Fourier coefficients.  It supplies no
   estimate for the literal MASTER/hybrid scalar.
2. Matomäki--Radziwiłł--Tao, arXiv:1707.01315v3, Proposition 3.1,
   supplies only (6.5).  Its applied major theorem uses standard
   \(\Lambda,d_k\), polylogarithmic denominators, and nonzero shifts; it
   does not prove (6.10).
3. Matomäki--Radziwiłł--Tao, arXiv:1812.01224v1, Theorem 1.2 gives
   additive Fourier uniformity for the Liouville function on average over
   base intervals.  The arbitrary 1-bounded formulation is instead the
   Theorem 1.4 pretentiousness inverse theorem and yields the analogous
   conclusion only under the required non-pretentiousness condition.  Neither
   is a fixed tagged cross-flatness theorem for the two present,
   divisor-bounded factors.
4. Guth--Maynard, arXiv:2405.20552v2, treats large values of
   multiplicative-frequency Dirichlet polynomials with bounded
   coefficients.  Its transform and coefficient class do not match
   (6.8).
5. Bettin--Chandee, arXiv:1502.00769v1, Theorem 1, has already paid the
   local \(M_x^{\rm loc}\) corridor at exponent \(1891/1920\).  It does
   not identify the actual weighted AP major or estimate (5.4).
6. Classical and modern BV/BDH/dispersion theorems concern fixed residue
   AP discrepancies and structured modulus weights.  The prime-shell,
   moving-residue, q-dependent signed covariance (5.4) is a different
   object.
7. Aspenberg--Baladi--Persson, arXiv:2212.12202v2, Theorem 1.1, and
   Haydn--Nicol--Török--Vaienti, arXiv:1406.4266, Theorem 3.1, remain
   dynamics-only interfaces; neither constructs the arithmetic quotient
   below.

`NONE_FOUND` here means only this declared primary corpus as of the date
above.  It is not a claim about every possible theorem in the literature.

The source firewall is therefore

\[
 \boxed{
 \text{no current source identifies (6.10) and proves either (6.8) or
 (5.4) on the literal object.}}
\tag{7.1}
\]

## 8. Translation-equivariant quotient no-go and the \(q=5\) survivor

Let \(G=\mathbb Z/N\mathbb Z\), let
\(\mathcal H=\ell^2(G)\) with normalized Haar measure, and let
\(Q:\mathcal H\to Z\) be linear and translation equivariant:

\[
 QT_g=\rho_gQ.
\tag{8.1}
\]

Suppose point evaluation factors through \(Q\):

\[
 \operatorname{ev}_0=\ell\circ Q.
\tag{8.2}
\]

Then \(\ker Q\subseteq\ker\operatorname{ev}_0\).  If \(f\in\ker Q\),
equivariance puts every translate \(T_gf\) in \(\ker Q\), so evaluating
all translates at zero gives \(f(g)=0\) for every \(g\).  Hence

\[
 \boxed{\ker Q=\{0\};\quad Q\text{ is injective}.}
\tag{8.3}
\]

The minimum Riesz kernel for \(\operatorname{ev}_0\) on the full space is

\[
 K_*=N\delta_0,\qquad
 \kappa=\|K_*\|_2^2=N,\qquad
 \kappa_0=\|K_*-1\|_2^2=N-1.
\tag{8.4}
\]

For \(N\asymp x\), this misses the V29 threshold
\(\kappa_0=o(x/\log^4x)\).  The conclusion is scoped: a restricted source
class not containing all translated atoms, a distinguished arithmetic
seed, a nonautonomous tag, or an approximate factor with an independent
error theorem can break translation symmetry and remains open.

There is a genuine five-point finite survivor.  For gap two, put

\[
 A_5=\{1,2,4\}\subset\mathbb Z/5\mathbb Z,
 \qquad K_5=\frac53\mathbf1_{A_5}.
\tag{8.5}
\]

Then

\[
 \mu(A_5)=\frac35,\qquad
 \frac{\mu(A_5)}{(4/5)^2}=\frac{15}{16},
\tag{8.6}
\]

\[
 \int K_5=1,\qquad
 \|K_5\|_2^2=\frac53,\qquad
 \|K_5-1\|_2^2=\frac23.
\tag{8.7}
\]

If \(f\) is already known to be supported on \(A_5\), then

\[
 \int f=\frac35\int K_5f.
\tag{8.8}
\]

This low-Christoffel local carrier does not prove a positive arithmetic
main: \(f\equiv0\) has the same admissible support and zero mass.

## 9. Finite fixtures and route order

All finite fixtures are type diagnostics, not asymptotic evidence.

For \(q=5\), ordered by \(a=0,1,2,3,4\),

\[
 (\delta_5(a))=
 \left(0,\frac5{16},\frac5{16},-\frac{15}{16},\frac5{16}\right),
 \quad \sum_a|\delta_5(a)|=\frac{15}{8}.
\tag{9.1}
\]

For \(q=7\),

\[
 (\delta_7(a))=
 \left(0,\frac7{36},\frac7{36},\frac7{36},\frac7{36},
 -\frac{35}{36},\frac7{36}\right),
 \quad \sum_a|\delta_7(a)|=\frac{35}{18}.
\tag{9.2}
\]

For \(\mathcal Q=\{5,7\}\), \(L_{\rm pr}=10\), and the unweighted
Ramanujan kernel satisfies

\[
 \kappa(0)=1,\quad \kappa(1)=-\frac15,\quad
 \kappa(5)=\frac3{10},\quad \kappa(7)=\frac12,\quad
 \kappa(35)=1.
\tag{9.3}
\]

For the single-point fixture \(\beta(1)=1,w(1)=10\), the q-local model
diagonal is \(29/120\), the residual diagonal is \(1171/120\), and their
sum is exactly \(10\).

The adjoint fixture on \(\mathbb Z/4\mathbb Z\) is

~~~text
beta   = (1, 2, 0, 1)
w      = (3, -1, 2, 0)
kappa  = (1, 1/2, 1/3, -1/2)
r      = (1, 6, 1, 8)
Tkw    = (19/6, -3/2, 7/2, 1/6)
J(r)   = <beta,Tkw> = 1/3
~~~

The route order is now

~~~text
1. B: predeclared hard-major Mloc+a attachment plus tagged cell cross-flatness;
2. A: terminal q-local residual major covariance on the same physical scalar;
3. C: symmetry-breaking low-Christoffel arithmetic quotient;
4. unchanged O161, pair-native, H1, A1/A2 and provenance reserves.
~~~

Steps 1 and 2 are both logically necessary.  The order ranks research
leverage; it does not allow either gate to borrow the other's theorem credit.

## 10. Canonical status registry and next theorem

~~~text
V30_MAXIMUM_CLAIM = EXACT_QLOCAL_MAJOR_MODEL_X_95_OVER_96_PLUS_CELL_PRODUCT_MRT_REDUCTION_PLUS_ENDPOINT_EQUIVALENCE_PLUS_EQUIVARIANT_QUOTIENT_NO_GO
V30_ROUTE_ADVANCE = YES
V30_ARITHMETIC_ADVANCE = NO
V30_FIXED_ATOM_CREDIT = 0
V30_STRICT_1_OVER_400 = UNPAID
V30_L2 = NONE
V30_TPC_207_TRIGGER = false
V30_NUMBERED_RELEASE = NO
V30_SELECTED_RESEARCH_ROUTE = B_TAGGED_HARD_MAJOR_CELL_PRODUCT_AND_MLOC_ATTACHMENT
V30_LOGICAL_TERMINAL_GATE = A_TAGGED_QLOCAL_RESIDUAL_MAJOR_AFTER_B
V30_LITERAL_JUTILA_MAJOR_SCALAR = PROVED_EXACT_L0_WITH_REFLECTED_KERNEL_SIGN
V30_J_ZERO_AXIS_SELF_RETURN = PROVED_EXACT_S_PLUS_OFFZERO
V30_OFFZERO_GATE_TO_E_MARGIN = PROVED_EXACT_CONDITIONAL_13_OVER_4800_MINUS_THETA_MINUS_EPSILON
V30_A_B_ENDPOINT_EQUIVALENCE = PROVED_EXACT_STRICT_EXPONENT_CLASS
V30_A_AS_EASIER_PRELIMINARY = STOP_SCOPED_TERMINAL_EQUIVALENCE_AFTER_B
V30_A_ADJOINT_CONVOLUTION_IDENTITY = PROVED_EXACT_ALGEBRAIC
V30_QLOCAL_F_G_DELTA_PROFILE = PROVED_EXACT_FINITE_PERIOD
V30_QLOCAL_RAMANUJAN_PAIRING = PROVED_EXACT_NORMALIZED_MEAN_EQUALS_DELTA_AT_ZERO
V30_QLOCAL_POISSON_CONSTANT = PROVED_EXACT_H_TIMES_PSI_AT_ZERO
V30_QLOCAL_UNIT_NONUNIT_LEDGER = PROVED_EXACT_ZERO_NUMERATOR_ADDED_AND_SUBTRACTED_ONCE
V30_QLOCAL_MODEL_RESIDUAL_REASSEMBLY = PROVED_EXACT_OCCURRENCEWISE
V30_QLOCAL_MODEL_BOUND = PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1
V30_QLOCAL_MODEL_MARGIN_TO_399_400 = 19/2400
V30_QLOCAL_BOUNDARY = PROVED_X_47_OVER_48_PLUS_EPSILON
V30_QLOCAL_DIAGONAL_MODEL_BOUND = PROVED_X_2_OVER_3_PLUS_O1
V30_QLOCAL_PHYSICAL_DIAGONAL_SURVIVES = PROVED_EXACT_COEFFICIENT_ONE_MINUS_SMALL_MODEL
V30_TAGGED_QLOCAL_RESIDUAL_MAJOR_COVARIANCE = SELECTED_TERMINAL_OPEN_NEW_THEOREM
V30_A_FIRST_FATAL = TAGGED_QLOCAL_RESIDUAL_MAJOR_COVARIANCE
V30_DIRECT_BV_BDH_ATTACHMENT = STOP_SCOPED_WRONG_SIGNED_COVARIANCE_OBJECT
V30_LOCAL_BC_CARRIER = PROVED_SOURCE_BACKED_X_1891_OVER_1920_BUT_ZERO_GLOBAL_CREDIT
V30_B_MRT_PRODUCT_LOCAL_REDUCTION = SOURCE_BACKED_REDUCTION_ONLY
V30_B_HARD_MAJOR_PREDECLARATION = REQUIRED_CIRCULARITY_FIREWALL
V30_B_CELL_PRODUCT_CERTIFICATE = PROVED_EXACT_PARTITION_AND_CAUCHY_SCHWARZ
V30_B_CELL_L1_GLOBAL_BOUND = PROVED_ELEMENTARY_X_1_PLUS_O1
V30_B_CELL_LINF_CROSS_FLATNESS = OPEN_ACTUAL_TAGGED_LOCAL_THEOREM
V30_B_ACTUAL_CELL_ENERGY_BOUND = OPEN_NEW_THEOREM
V30_B_MLOC_PLUS_A_ATTACHMENT = OPEN_WEIGHTED_AP_ATTACHMENT
V30_B_CROSS_FLATNESS_STRICTLY_WEAKER = PROVED_EXACT_ANTISPIKE_FAMILY
V30_B_ADAPTIVE_LARGE_SPECTRUM_EXCISION = STOP_SCOPED_MAJOR_ABSORBS_TARGET_WITHOUT_MLOC_ATTACHMENT
V30_MRT_FOURIER_UNIFORMITY_ATTACHMENT = STOP_SCOPED_LIOUVILLE_OR_NONPRETENTIOUS_1_BOUNDED_AVERAGED_WRONG_QUANTIFIERS
V30_GUTH_MAYNARD_LARGE_VALUES_ATTACHMENT = STOP_SCOPED_MULTIPLICATIVE_FREQUENCY_WRONG_TRANSFORM
V30_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V30_C_EQUIVARIANT_WHOLE_SHELL_QUOTIENT = STOP_SCOPED_TRANSLATION_INVARIANCE_FORCES_INJECTIVITY
V30_C_FULL_COORDINATE_CHRISTOFFEL = PROVED_EXACT_KAPPA_N_KAPPA0_N_MINUS_1
V30_C_DISTINGUISHED_SEED_SYMMETRY_BREAK = SURVIVES_SCOPED_OPEN
V30_C_ACTUAL_ARITHMETIC_QUOTIENT = OPEN_NEW_THEOREM
V30_Q5_GAP2_LOCAL_DENSITY_KERNEL = PROVED_EXACT_FINITE_LOW_CHRISTOFFEL_CARRIER
V30_Q5_TO_PHYSICAL_POSITIVE_MAIN = STOP_SCOPED_LOCAL_ADMISSIBILITY_DOES_NOT_FORCE_PRIME_MASS
V30_NEXT_THEOREM = TAGGED_HARD_MAJOR_CELL_CROSS_FLATNESS_PLUS_MLOC_WEIGHTED_ATTACHMENT
V30_FIRST_FATAL = MISSING_LITERAL_MT_EQUALS_MLOC_PLUS_A_AND_TAGGED_CELL_CROSS_FLATNESS
V30_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
V30_PROVENANCE_CASCADE = REQUIRED
~~~

The maximum supported claim is the exact q-local model payment, the geometric
MRT reduction, the strict endpoint-equivalence theorem, and the scoped cyclic
quotient no-go.  It is not an arithmetic power saving for
\(S_x^{\rm physical}\).

The next theorem must prove, on one predeclared hard-major set and the same
literal occurrence object, both the \(M_x^{\rm loc}+a_x\) attachment and the
cell cross-flatness bound (6.8), including its weighted reassembly and strict
\(13/4800\) slack.  Only after that minor gate is paid does (5.4) become the
terminal-equivalent arithmetic theorem.
