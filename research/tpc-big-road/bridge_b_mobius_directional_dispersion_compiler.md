# Bridge A / Gate B V42: proper-factor directional dispersion and the operator-only no-go

Date: 2026-08-10

Status: unnumbered big-road research artifact.  The q-local residual is lifted
exactly to the V35 proper-factor variables, its occurrence diagonal is paid,
and a disjoint dyadic compiler reduces Gate B to one coefficient-native
Möbius--prime directional dispersion theorem.  A separate theorem proves that
operator-norm, stable-rank, or Schatten information without the physical input
direction cannot certify the required loss.  The directional dispersion
theorem and terminal Gate A remain open; there is no arithmetic trigger.

## 1. Inherited q-local residual row

Keep the V41 data

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.1}
\]

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \beta(t)=\beta_x^{\rm raw}(t),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),
 \tag{1.2}
\]

\[
 K_H(h)=\widehat\psi_+(h/H),\qquad
 c'_q(h)=\mathbf1_{q\mid h}-\frac1{q-1}.
 \tag{1.3}
\]

For sufficiently large \(x\), every \(q\in\mathcal Q\) exceeds \(z\).  The
V30/V41 local profile is

\[
 \Gamma_q(u)=
 \begin{cases}
 -q(q-2)/(q-1)^2,&u\equiv-2\pmod q,\\
 0,&u\equiv0\pmod q,\\
 q/(q-1)^2,&u\not\equiv0,-2\pmod q.
 \end{cases}
 \tag{1.4}
\]

Write \(r_q(u)=w(u)-\Gamma_q(u)\).  The open V41 row is

\[
 \rho_q=
 \sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)r_q(u)K_H(u-t)c'_q(u-t),
 \tag{1.5}
\]

with energy and occurrence-collapsed diagonal

\[
 \mathcal E_{\rm res}=\sum_{q\in\mathcal Q}|\rho_q|^2,
 \tag{1.6}
\]

\[
 G^{\rm res}_{q,t}=
 \sum_{\substack{u\in I_x\\u\ne t\\q\nmid u}}
 r_q(u)K_H(u-t)c'_q(u-t),
 \qquad
 \mathcal D_{\rm res}=
 \sum_q\sum_{\substack{t\in I_x\\q\nmid t}}
 |\beta(t)G^{\rm res}_{q,t}|^2.
 \tag{1.7}
\]

V41 proved

\[
 \mathcal D_{\rm res}\ll x^{95/48+o(1)}
 \tag{1.8}
\]

and isolated the sufficient loss

\[
 \mathcal E_{\rm res}\ll x^{\tau+o(1)}\mathcal D_{\rm res},
 \qquad \tau<\frac{419}{1200}.
 \tag{1.9}
\]

The preferred benchmark is \(\tau=1/3\).  V42 does not assume that an
arbitrary matrix satisfies (1.9).  It identifies the physical direction that
must be retained and compiles it into factor-native cells.

## 2. Exact proper-factor lift of the residual

V35 proved, for every \(t\in I_x\),

\[
 \boxed{
 \beta_x^{\rm raw}(t)=
 \sum_{\substack{dk=t\\d,k\geq2}}
 \mu(d)\omega_x(d,k),}
 \tag{2.1}
\]

where

\[
 \omega_x(d,k)=
 \begin{cases}
 -\dfrac{\log d}{\log(dk)},&d^{400}\leq x^{133},\\[2mm]
 \dfrac{\log k}{\log(dk)},&d^{400}>x^{133},
 \end{cases}
 \qquad |\omega_x(d,k)|\leq1.
 \tag{2.2}
\]

Substituting (2.1) into (1.5) before any absolute value gives the exact lift

\[
 \boxed{
 \rho_q=
 \sum_{\substack{dk\in I_x\\d,k\geq2\\q\nmid dk}}
 \mu(d)\omega_x(d,k)G^{\rm res}_{q,dk}.}
 \tag{2.3}
\]

Equivalently, without collapsing the physical endpoint \(u\),

\[
 \boxed{
 \rho_q=
 \sum_{\substack{dk,u\in I_x\\d,k\geq2, u\ne dk\\q\nmid dku}}
 \mu(d)\omega_x(d,k)r_q(u)
 K_H(u-dk)c'_q(u-dk).}
 \tag{2.4}
\]

This is an identity, not a divisor-envelope replacement.  It preserves the
single common prime shell, the V19 ordered \(+2,-1\) coefficient after exact
collapse, the hybrid subtraction, the hard shell, the off-diagonal deletion,
and the q-local residual.  Both factor endpoints are absent.  In particular,

\[
 \boxed{\beta_x^{\rm raw}(p)=0\quad(p\ {\rm prime})}
 \tag{2.5}
\]

is preserved occurrence by occurrence as an empty proper-factor sum.
Here and below, `occurrence` means an algebraic proper-factor occurrence in
(2.1), not a claim that the V19 occurrence-native local carrier has been
reconstructed.

## 3. The proper-factor occurrence diagonal is paid

Define

\[
 \mathcal D_{\rm pf}=
 \sum_{q\in\mathcal Q}
 \sum_{\substack{dk\in I_x\\d,k\geq2\\q\nmid dk}}
 |\mu(d)\omega_x(d,k)G^{\rm res}_{q,dk}|^2.
 \tag{3.1}
\]

For fixed \(q,t\), the centered kernel has absolute mass

\[
 \sum_{\substack{u\in I_x\\u\ne t\\q\nmid u}}
 |K_H(u-t)c'_q(u-t)|\ll_\psi \frac Hq.
 \tag{3.2}
\]

The inherited divisor envelopes therefore give

\[
 |G^{\rm res}_{q,t}|\ll x^{o(1)}\frac Hq.
 \tag{3.3}
\]

Moreover,

\[
 \#\{(d,k):d,k\geq2,\ dk\in I_x\}
 \leq\sum_{t\leq x}\tau(t)=x^{1+o(1)}.
 \tag{3.4}
\]

Since \(\#\mathcal Q\leq Qx^{o(1)}\), (2.2)--(3.4) give

\[
 \boxed{
 \mathcal D_{\rm pf}
 \ll Qx^{1+o(1)}\left(\frac HQ\right)^2
 =\frac{x^{1+o(1)}H^2}{Q}
 =x^{95/48+o(1)}.}
 \tag{3.5}
\]

Divisor Cauchy applied to (2.1) also gives

\[
 \mathcal D_{\rm res}\leq x^{o(1)}\mathcal D_{\rm pf}.
 \tag{3.6}
\]

The reverse inequality is neither asserted nor needed: the occurrence
diagonal deliberately refuses to borrow cancellation between divisors of the
same \(t\).  The exponent survives this stronger bookkeeping.

### 3.1 The narrow physical Gram gate

Extend \(G^{\rm res}_{q,t}\) by zero when \(q\mid t\), and put

\[
 a_{q,t}=\beta(t)G^{\rm res}_{q,t},\qquad
 A=(a_{q,t})_{q\in\mathcal Q,t\in I_x}.
 \tag{3.7}
\]

The exact Gram expansion is

\[
 \boxed{
 \mathcal E_{\rm res}=\mathcal D_{\rm res}+\mathcal O_{\rm res},}
 \qquad
 \mathcal O_{\rm res}=
 \sum_q\sum_{t_1\ne t_2}a_{q,t_1}\overline{a_{q,t_2}}.
 \tag{3.8}
\]

The ordered off-diagonal sum \(\mathcal O_{\rm res}\) is real but may have
either sign.  Since \(\mathcal D_{\rm res}\ll x^{95/48+o(1)}\), the narrowest
benchmark theorem is only

\[
 \boxed{
 (\mathcal O_{\rm res})_+\ll x^{37/16+o(1)}.}
 \tag{3.9}
\]

It asks for the positive coherent collision of the one physical direction;
it does not ask for arbitrary occurrence coefficients or for the absolute
value of every off-diagonal collision.  The cell theorem below is a
source-facing sufficient implementation of (3.9), not an equivalent
reformulation.

There is a second exact view which must retain its cross term.  Define

\[
 R_q(h)=
 \sum_{\substack{t,t+h\in I_x\\h\ne0\\q\nmid t(t+h)}}
 \beta(t)r_q(t+h),
 \tag{3.10}
\]

\[
 \mathsf S_q=\sum_{\substack{h\ne0\\q\mid h}}K_H(h)R_q(h),
 \qquad
 \mathsf B_q=\frac1{q-1}\sum_{h\ne0}K_H(h)R_q(h).
 \tag{3.11}
\]

Then \(\rho_q=\mathsf S_q-\mathsf B_q\) and

\[
 \boxed{
 \mathcal E_{\rm res}=
 \sum_q|\mathsf S_q|^2+\sum_q|\mathsf B_q|^2
 -2\Re\sum_q\mathsf S_q\overline{\mathsf B_q}.}
 \tag{3.12}
\]

Estimating the spike and background separately is a valid but stronger
triangle route.  It receives no claim that the signed physical cross term has
been used.

An exact finite diagnostic takes \(q=5\), six active \(t\)-columns, one shift
\(h=5\), \(K_H(5)=1\), and residual endpoint value \(4/3\).  Each centered
column equals \(1\), while

\[
 \mathsf S_5=8,\qquad \mathsf B_5=2,\qquad
 -2\mathsf S_5\mathsf B_5=-32,
 \tag{3.13}
\]

\[
 \rho_5=6,\qquad \mathcal D=6,\qquad
 \mathcal E=36=64+4-32.
 \tag{3.14}
\]

This is an algebraic cross-term fixture, not an arithmetic example.

## 4. Disjoint dyadic directional compiler

For active integers \(j\), let

\[
 \mathcal C_j=
 \{(d,k):d,k\geq2,\ dk\in I_x,\ 2^j\leq d<2^{j+1}\}.
 \tag{4.1}
\]

These are disjoint and their number \(J_x\) is \(O(\log x)\).  Put

\[
 \rho_{q,j}=
 \sum_{\substack{(d,k)\in\mathcal C_j\\q\nmid dk}}
 \mu(d)\omega_x(d,k)G^{\rm res}_{q,dk},
 \tag{4.2}
\]

\[
 \mathcal D_j=
 \sum_{q\in\mathcal Q}
 \sum_{\substack{(d,k)\in\mathcal C_j\\q\nmid dk}}
 |\mu(d)\omega_x(d,k)G^{\rm res}_{q,dk}|^2.
 \tag{4.3}
\]

Then exactly

\[
 \rho_q=\sum_j\rho_{q,j},\qquad
 \sum_j\mathcal D_j=\mathcal D_{\rm pf}.
 \tag{4.4}
\]

The narrow source-facing theorem is the following fixed-physical-direction
estimate, uniformly in every active cell:

\[
 \boxed{
 \mathsf H_{\rm MPD}(j):\qquad
 \sum_{q\in\mathcal Q}|\rho_{q,j}|^2
 \ll Qx^{o(1)}\mathcal D_j.}
 \tag{4.5}
\]

Here `MPD` means Möbius--prime directional dispersion.  It is not a theorem
for arbitrary arrays: the literal \(\mu(d)\omega_x(d,k)\), the physical
\(w-\Gamma_q\), and the centered q-row all remain inside the estimate.

If (4.5) holds for all cells, Hilbert-space triangle and Cauchy give

\[
 \begin{aligned}
 \mathcal E_{\rm res}^{1/2}
 &\leq\sum_j\left(\sum_q|\rho_{q,j}|^2\right)^{1/2}\\
 &\ll Q^{1/2}x^{o(1)}\sum_j\mathcal D_j^{1/2}\\
 &\ll Q^{1/2}x^{o(1)}J_x^{1/2}
       \mathcal D_{\rm pf}^{1/2}.
 \end{aligned}
 \tag{4.6}
\]

Thus

\[
 \boxed{
 \mathsf H_{\rm MPD}(j)\ \text{for every }j
 \quad\Longrightarrow\quad
 \mathcal E_{\rm res}\ll Qx^{o(1)}\mathcal D_{\rm pf}.}
 \tag{4.7}
\]

The factor \(J_x\) is absorbed by \(x^{o(1)}\); there is still one outer
\(\ell^2(\mathcal Q)\) norm, not one absolute value per modulus.

### 4.1 Exact coefficient preparation

Let \(U=x^{133/400}\).  Splitting the unique dyadic cell that meets \(U\)
creates only a constant number of subcells.  On the two sides, the signed
factor coefficient is exactly

\[
 -\frac{\mu(d)\log d}{\log(dk)}
 \quad(d\leq U),
 \qquad
 \frac{\mu(d)\log k}{\log(dk)}
 \quad(d>U).
 \tag{4.8}
\]

The denominator can be handled without replacing the coefficient.  If
\(F(y)\) is the cumulative sum of any one cell over
\(x/2<dk\leq y\), then exact Stieltjes partial summation gives

\[
 \sum_{x/2<dk\leq x}\frac{a_{d,k}}{\log(dk)}
 =\frac{F(x)}{\log x}
 +\int_{x/2}^{x}\frac{F(y)}{y(\log y)^2}\,dy.
 \tag{4.9}
\]

Therefore a source theorem uniform in the product cutoff sees one
Möbius/log factor and one complementary factor, while the total partial-
summation variation is logarithmic.  Equation (4.9) is only a compiler; it
does not prove (4.5).

## 5. Endpoint clock and one-outer-absolute theorem

Combining (3.5) and (4.7) at \(Q=x^{1/3}\) gives

\[
 \boxed{
 \mathcal E_{\rm res}\ll x^{37/16+o(1)},\qquad
 \mathcal E_{\rm res}^{1/2}\ll x^{37/32+o(1)}.}
 \tag{5.1}
\]

This is the V41 sample \(\tau=1/3\), equivalently
\(\kappa=1/48\).  With the already-paid q-local model row,

\[
 |\mathfrak C_x|\ll
 Q^{3/2+o(1)}
 \left(\mathcal E_{\rm model}^{1/2}
       +\mathcal E_{\rm res}^{1/2}\right)
 \ll x^{53/32+o(1)}.
 \tag{5.2}
\]

The strict numerator margin remains

\[
 \boxed{\frac{1997}{1200}-\frac{53}{32}=\frac{19}{2400}.}
 \tag{5.3}
\]

For one cell, (4.5) is equivalent to

\[
 \boxed{
 \sup_{\sum_q|\lambda_q|^2=1}
 \left|
 \sum_{q\in\mathcal Q}\lambda_q
 \sum_{\substack{(d,k)\in\mathcal C_j\\q\nmid dk}}
 \mu(d)\omega_x(d,k)G^{\rm res}_{q,dk}
 \right|
 \ll Q^{1/2}x^{o(1)}\mathcal D_j^{1/2}.}
 \tag{5.4}
\]

Opening \(G^{\rm res}_{q,dk}\) in (5.4) produces the literal ternary
\((d,k,u)\) form with a single external vector \(\lambda_q\).  This is the
preferred theorem interface.

## 6. Why operator-only and Schatten-only roads cannot certify the gate

Use the matrix \(A\) from (3.7).

Let

\[
 \mathcal T_{\rm act}=\{t\in I_x:\text{the column }(a_{q,t})_q
 \text{ is nonzero}\},\qquad N_{\rm act}=\#\mathcal T_{\rm act}.
 \tag{6.1}
\]

Delete the zero columns, and let \({\bf1}_{\rm act}\) be the all-ones vector
on \(\mathcal T_{\rm act}\).  Then

\[
 \mathcal E_{\rm res}=\|A{\bf1}_{\rm act}\|_2^2,
 \qquad
 \mathcal D_{\rm res}=\|A\|_{\rm HS}^2.
 \tag{6.2}
\]

Let \(R=\#\mathcal Q=x^{1/3+o(1)}\).  The stable rank satisfies

\[
 {\rm sr}(A)=\frac{\|A\|_{\rm HS}^2}{\|A\|_{\rm op}^2}
 \leq {\rm rank}(A)\leq R.
 \tag{6.3}
\]

An argument that discards the direction \({\bf1}_{\rm act}\) and uses only
\(\|A\|_{\rm op}\), \(\|A\|_{\rm HS}\), rank/stable rank, and
\(\|{\bf1}_{\rm act}\|_2^2=N_{\rm act}\) can supply only

\[
 \|A{\bf1}_{\rm act}\|_2^2
 \leq N_{\rm act}\|A\|_{\rm op}^2
 =\frac{N_{\rm act}}{{\rm sr}(A)}\|A\|_{\rm HS}^2.
 \tag{6.4}
\]

Even at the most favorable possible value \({\rm sr}(A)=R\), this certificate
has loss

\[
 \frac{N_{\rm act}}R.
 \tag{6.5}
\]

The endpoint requires a loss exponent strictly below \(419/1200\).  Therefore
an operator-only certificate first requires the independent support
compression

\[
 \boxed{
 N_{\rm act}\leq x^{1/3+419/1200-o(1)}
 =x^{273/400-o(1)}.}
 \tag{6.6}
\]

No such power support compression is proved here.  In the full-active regime
\(N_{\rm act}=x^{1+o(1)}\), the certificate loss is

\[
 x^{2/3+o(1)},\qquad
 \frac23-\frac{419}{1200}=\boxed{\frac{127}{400}}.
 \tag{6.7}
\]

At the preferred \(Q=x^{1/3}\) benchmark it then misses by a full
\(x^{1/3}\).  This is a conditional no-go for a proof *certificate*, not a
claim that the physical matrix is full-active and not a lower bound for the
physical \(\mathcal E_{\rm res}\).  A support-compression theorem, or
singular-vector information proving that the physical direction avoids the
coherent subspace, lies outside the no-go; the latter is precisely directional
dispersion.

The obstruction is sharp in finite dimension.  Take the \(2\times8\) matrix
whose first row is all \(1\) and whose second row alternates \(1,-1\).  Its
rows are orthogonal and equally long, so its stable rank is the maximal value
\(2\), but

\[
 \|A\|_{\rm HS}^2=16,\qquad
 \|A{\bf1}_{\rm act}\|_2^2=64,\qquad
 \frac{\|A{\bf1}_{\rm act}\|_2^2}{\|A\|_{\rm HS}^2}=4=\frac82.
 \tag{6.8}
\]

Thus maximal stable rank alone does not even imply loss equal to the number
of rows.

## 7. Two coefficient-blind firewalls

### 7.1 Centered q-kernel counterexample

The desired \(Q\)-loss is also false for generic bounded endpoint
coefficients, even with the exact centered residue kernel.  Take \(q=5\),
three copies of each unit residue, \(K=1\), and residual endpoint data
\(r(u)=\mathbf1_{u\equiv1\ (5)}\).  Delete \(u=t\) as in the physical row.
Then

\[
 G_t=
 \begin{cases}
 3(M-1)/4,&t\equiv1\pmod5,\\
 -M/4,&t\equiv2,3,4\pmod5,
 \end{cases}
 \qquad(M=3).
 \tag{7.1}
\]

Choose \(\beta(t)={\rm sgn}(G_t)\).  Exact summation gives

\[
 \rho_5=\frac{45}{4},\qquad
 \mathcal D=\frac{189}{16},\qquad
 |\rho_5|^2=\frac{2025}{16},
 \tag{7.2}
\]

and hence

\[
 \frac{|\rho_5|^2}{\mathcal D}=\frac{75}{7}>5.
 \tag{7.3}
\]

This is a finite typing counterexample, not a model for the actual prime
sequence.  It proves that (4.5) must retain the physical Möbius/prime
direction; boundedness and the centered kernel alone do not imply it.

### 7.2 Prime-row cancellation

For a prime \(p\in I_x\), the two terms in

\[
 \beta_x^{\rm raw}(p)=\frac{\Lambda(p)}{\log p}
 -\sum_{\substack{d\mid p\\d^{400}\leq x^{133}}}\mu(d)
 \tag{7.4}
\]

are each \(1\), while their signed combination is zero.  The proper-factor
sum (2.1) is empty.  Consequently, splitting these channels and taking
separate outer absolute values destroys an exact physical cancellation.
Such bounds remain formally sufficient if independently strong enough, but
they do not constitute an attachment to the directional theorem and receive
no power credit here.

## 8. Primary-source boundary

The following source screen uses primary theorem texts current on
2026-08-10.

1. [Matomäki--Radziwiłł--Tao, arXiv:1707.01315v3, Theorem 1.3 and Proposition 3.1](https://arxiv.org/abs/1707.01315)
   gives source-native almost-all shift asymptotics and an abstract minor-arc
   energy reduction.  It neither identifies the q-dependent
   \(w-\Gamma_q\) row nor proves the cellwise fixed-direction estimate (4.5).

2. [Harper, arXiv:2412.19644v1, Theorems 1--2](https://arxiv.org/abs/2412.19644)
   treats the progression variance of one fixed sequence under additional
   hypotheses and in different modulus regimes.  In (4.5), the endpoint
   sequence and the centered row both depend on \(q\), and the theorem must
   retain a joint Möbius--prime direction.

3. [Bazin, arXiv:2607.15137v1, Theorem 8](https://arxiv.org/abs/2607.15137)
   accepts the collapsed \(\beta_x^{\rm raw}\) marginal through a Type-I/II
   interface.  It is a one-sided marginal theorem and does not accept the
   simultaneous residual endpoint or the modulus-family square in (4.5).

4. [Runbo Li, arXiv:2602.20917v6, Theorem 1.1](https://arxiv.org/abs/2602.20917)
   proves Bombieri--Vinogradov type distribution for the prime indicator with
   divisor-bounded weights on factored moduli \(q_1q_2\).  The factors there
   parameterize the modulus; they do not supply the proper-factor endpoint
   direction \((d,k)\), the q-dependent residual, or its row square.

5. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1](https://arxiv.org/abs/2607.24311)
   gives a \(q^{-1/32}\) saving in the critical square-root range for one
   fixed-modulus bilinear Kloosterman cell.  V38 supplies an exact local
   emitter for such balanced cells.  What remains unpaid is the aggregate
   block atomic/nuclear budget and the collective \(\ell^2(q)\) reassembly;
   the theorem is a reusable local engine, not (4.5).

6. [Milićević--Qin--Wu, arXiv:2511.07550v1, Theorem 1.1](https://arxiv.org/abs/2511.07550)
   proves power-saving bounds for arbitrary bilinear coefficients against the
   completed kernel \({\rm Kl}_2(cmn;q)\), for a fixed modulus \(q\) and
   explicit length ranges; in the square-root range its stated general-
   modulus saving is \(q^{-1/100+o(1)}\).  It is another local engine after a
   successful transform, not a theorem for the untransformed mixed
   \((q,d,k,u)\) residual family or its prime-shell energy.

No checked source proves (4.5) for the literal proper-factor lift.  In
particular, a local Kloosterman engine cannot be inserted before one has
compiled the q-dependent prime residual and the hard-shell occurrence family
into its two arrays.

## 9. Route after V42

The macro route is now

```text
V41 q-local split
  model row m_q = PAID at x^(37/16)
  residual row rho_q
    -> V42 positive physical Gram collision = NARROW PRIMARY OPEN
    -> V42 exact proper-factor lift (d,k,u)
    -> occurrence diagonal x^(95/48) = PAID
    -> generic operator / stable-rank / Schatten certificate
         requires active support <= x^(273/400) or is STOP
    -> coefficient-blind centered-kernel theorem = STOP
    -> physical dyadic MPD cells with Q loss = PREFERRED IMPLEMENTATION OPEN
         if paid: residual energy x^(37/16), output x^(53/32)
  -> terminal q-local Gate A = INDEPENDENT OPEN
  -> dynamics C = RESERVE.
```

The bridge has moved from an abstract residual-row label to its positive
physical Gram collision and a coefficient-native implementation span.  The
first fatal is the positive collision theorem itself; the preferred
source-facing implementation is a uniform physical Type-I/II-style
directional estimate for the same Möbius--prime residual cells.

## 10. Canonical status registry

```text
V42_MAXIMUM_CLAIM = EXACT_QLOCAL_POSITIVE_GRAM_GATE_PROPER_FACTOR_LIFT_PAID_OCCURRENCE_DIAGONAL_DYADIC_DIRECTIONAL_COMPILER_AND_OPERATOR_ONLY_CERTIFICATE_NO_GO
V42_ROUTE_ADVANCE = YES
V42_CONDITIONAL_BRIDGE_ADVANCE = YES
V42_ARITHMETIC_ADVANCE = NO
V42_FIXED_ATOM_CREDIT = 0
V42_STRICT_1_OVER_400 = UNPAID
V42_L2 = NONE
V42_TPC_207_TRIGGER = false
V42_NUMBERED_RELEASE = NO
V42_DERIVATION_STATUS = COHERENT_AFTER_EXACT_PROPER_FACTOR_LIFT_OCCURRENCE_DIAGONAL_DYADIC_REASSEMBLY_DIRECTIONAL_AND_ZERO_AXIS_FIREWALLS
V42_ASSUMPTION_POLICY = CELLWISE_PHYSICAL_MOBIUS_PRIME_DIRECTIONAL_DISPERSION_REMAINS_EXPLICIT_OPEN_THEOREM
V42_SELECTED_RESEARCH_ROUTE = PROPER_FACTOR_DIRECTIONAL_DISPERSION_FIRST__SOURCE_NATIVE_TYPE_I_II_TRANSFORM_SECOND__GENERIC_OPERATOR_AND_MARGINAL_ROADS_STOP__A_TERMINAL__C_RESERVE
V42_V41_QLOCAL_SPLIT = RETAINED_EXACT_MODEL_PAID_RESIDUAL_OPEN
V42_V35_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA
V42_PROPER_FACTOR_SUPPORT = PROVED_EXACT_D_AND_K_AT_LEAST_2
V42_PRIME_ROW_CANCELLATION = PROVED_EXACT_EMPTY_PROPER_FACTOR_SUM
V42_RESIDUAL_PROPER_FACTOR_LIFT = PROVED_EXACT_BEFORE_ANY_OUTER_ABSOLUTE
V42_PROPER_FACTOR_OCCURRENCE_DIAGONAL = PROVED_X_POWER_95_OVER_48
V42_COLLAPSED_TO_OCCURRENCE_DIAGONAL = PROVED_WITH_DIVISOR_X_O1_LOSS
V42_RESIDUAL_GRAM_IDENTITY = PROVED_EXACT_E_RES_EQUALS_D_RES_PLUS_REAL_SIGNED_O_RES
V42_PRIMARY_POSITIVE_GRAM_GATE = OPEN_CONJECTURE_POSITIVE_O_RES_LE_X_POWER_37_OVER_16
V42_SPIKE_BACKGROUND_ENERGY = PROVED_EXACT_WITH_SIGNED_CROSS_TERM_RETAINED
V42_DYADIC_D_CELLS = PROVED_EXACT_DISJOINT_O_LOG_X_PARTITION
V42_DYADIC_RESIDUAL_REASSEMBLY = PROVED_EXACT_RHO_EQUALS_SUM_J_RHO_J
V42_CELLWISE_MOBIUS_PRIME_DIRECTIONAL_GATE = OPEN_CONJECTURE_E_J_LE_Q_X_O1_D_J
V42_CELLWISE_DIRECTIONAL_LOSS = Q_EQUALS_X_POWER_1_OVER_3
V42_CELLWISE_TO_GLOBAL_COMPILER = PROVED_BY_L2_TRIANGLE_AND_CELL_CAUCHY
V42_CONDITIONAL_RESIDUAL_ENERGY = X_POWER_37_OVER_16
V42_CONDITIONAL_RESIDUAL_DUAL_NORM = X_POWER_37_OVER_32
V42_CONDITIONAL_SCALAR_OUTPUT = X_POWER_53_OVER_32
V42_CONDITIONAL_ENDPOINT_MARGIN = 19_OVER_2400
V42_CONDITIONAL_KAPPA = 1_OVER_48
V42_CELLWISE_L2_DUAL = PROVED_ONE_OUTER_ABSOLUTE_MODULUS_FAMILY
V42_OMEGA_TWO_BRANCH_FORM = PROVED_EXACT_MU_LOG_D_OR_MU_LOG_K_OVER_LOG_DK
V42_LOG_DENOMINATOR_ABEL_COMPILER = PROVED_EXACT_UNIFORM_PRODUCT_CUTOFF_INTERFACE
V42_OPERATOR_MATRIX_IDENTITY = PROVED_E_RES_EQUALS_NORM_A_ONE_ACTIVE_SQUARED_AND_D_RES_EQUALS_HS_SQUARED
V42_STABLE_RANK_CEILING = PROVED_AT_MOST_NUMBER_OF_Q_ROWS_X_POWER_1_OVER_3
V42_OPERATOR_ONLY_CERTIFICATE_LOSS_FLOOR = N_ACTIVE_OVER_X_POWER_1_OVER_3
V42_OPERATOR_ONLY_THRESHOLD_SUPPORT_CEILING = X_POWER_273_OVER_400
V42_OPERATOR_ONLY_FULL_ACTIVE_LOSS = X_POWER_2_OVER_3
V42_OPERATOR_ONLY_ENDPOINT_EXCESS = 127_OVER_400
V42_MAXIMAL_STABLE_RANK_FIXTURE = PROVED_2_BY_8_HADAMARD_ROWS_RATIO_4
V42_GENERIC_CENTERED_KERNEL_Q_LOSS = STOP_SCOPED_Q5_M3_COUNTEREXAMPLE_RATIO_75_OVER_7
V42_COEFFICIENT_BLIND_ROW_BESSEL = STOP_SCOPED_PHYSICAL_DIRECTION_REQUIRED
V42_SPLIT_BETA_CHANNELS_BEFORE_OUTER_ABSOLUTE = STOP_SCOPED_PRIME_ROW_EXACT_CANCELLATION_DESTROYED
V42_OFFZERO_DIRECTIONAL_GATE_TO_ZERO_AXIS = STOP_SCOPED_DELTA_ZERO_FIREWALL_RETAINED
V42_TERMINAL_QLOCAL_GATE_A = OPEN_INDEPENDENT_SIGNED_COVARIANCE
V42_MRT_DIRECT_ATTACHMENT = STOP_SCOPED_SOURCE_COEFFICIENTS_AND_Q_DEPENDENT_RESIDUAL_MISMATCH
V42_HARPER_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_FIXED_SEQUENCE_AND_MODULUS_HYPOTHESES_MISMATCH
V42_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_SIDED_BETA_MARGINAL_NOT_JOINT_ROW_SQUARE
V42_RUNBO_LI_DIRECT_ATTACHMENT = STOP_SCOPED_FACTORED_MODULUS_PRIME_DISTRIBUTION_NOT_PROPER_FACTOR_RESIDUAL_DIRECTION
V42_BLOMER_PASCADI_BALANCED_CELL = SOURCE_BACKED_LOCAL_ENGINE_Q_MINUS_1_OVER_32_AFTER_V38_EXACT_EMITTER
V42_LOCAL_KLOOSTERMAN_ENGINE_TO_MPD = STOP_SCOPED_BLOCK_ATOMIC_BUDGET_AND_Q_L2_REASSEMBLY_UNPAID
V42_MILICEVIC_QIN_WU_DIRECT_ATTACHMENT = STOP_SCOPED_POST_TRANSFORM_FIXED_MODULUS_KLOOSTERMAN_ARRAYS_ONLY
V42_DIRECT_PRIMARY_SOURCE_FOR_MPD_CELL_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V42_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_POSITIVE_PHYSICAL_OFFDIAGONAL_GRAM_COLLISION_AT_X_POWER_37_OVER_16_WHILE_RETAINING_CENTERED_SPIKE_BACKGROUND_CROSS_TERM
V42_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_PROPER_FACTOR_DIRECTIONAL_SPAN_OPEN
V42_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V42_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```
