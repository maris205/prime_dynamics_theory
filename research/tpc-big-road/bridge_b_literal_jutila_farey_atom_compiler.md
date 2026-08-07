# Bridge B V24: literal determinant to Jutila--Farey/Kloosterman atoms

Date: 2026-08-08

Status:

```text
UNNUMBERED_WORKING_ARTIFACT
EXACT_L0_LITERAL_DETERMINANT_JUTILA_FAREY_KLOOSTERMAN_ATOMIZATION
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
```

V23 found a nonempty exponent window for a prime-shell Jutila method followed
by a Kloosterman-sensitive compiler.  V24 answers the next, more literal
question: how far can the actual fixed-`h0=2` physical scalar be transformed
before a new theorem is needed?

The answer is exact and sharply split.

```text
literal V19 determinant atoms
  -> exact Jutila main/error split
  -> corrected signed Farey identity
  -> complete Kloosterman atoms
```

All arrows above close at `L0`.  The published Blomer--Li proof does not then
attach to the TPC coefficients or clock, and the resulting complete atoms are
not yet the short two-array input of Blomer--Pascadi.  The maximum claim is

```text
EXACT_L0_LITERAL_DETERMINANT_TO_JUTILA_MAIN_AND_FAREY_KLOOSTERMAN_ATOMIZATION_WITH_SOURCE_TRANSFER_FIREWALLS
```

This artifact proves no cancellation estimate.

## 1. Frozen physical scalar and literal atom ledger

Keep the V19--V23 conventions

```text
h0=2,
x=2X,
I_x={t in Z:x/2<t<=x},
z=(log x)^K,
w_x^(z)(t)=Lambda(t+2)-b_x^(z)(t).
```

For every ordered V19 MASTER occurrence `o`, put

```text
T_o=T(o),
a_o=c_(j(o)) product_i mu(e_i(o)) log(f_1(o))/log(T_o),
c_1=+2, c_2=-1.                                      (1.1)
```

Thus

```text
beta_x^raw(t)=1_(t in I_x)sum_(o:T_o=t)a_o,
S_x=sum_(t in I_x)beta_x^raw(t)w_x^(z)(t).           (1.2)
```

The tensor-local comparison is

```text
b_x^(z)(u)
 =1_(u in I_x) C_z W_z 1_((u+2,P(z))=1)
  sum_(d_rough|u)g_z(d_rough),                        (1.3)

C_z=product_(p>z)(1-1/(p-1)^2),
W_z=product_(p<=z)p/(p-1),
g_z(d)=mu^2(d)1_(P^-(d)>z)product_(p|d)1/(p-2).
```

Expand the prime and hybrid channels before enforcing the diagonal.  A prime
atom is

```text
nu_p=(o,d_phys,r_p),
u_p=d_phys r_p-2 in I_x,
A_x(nu_p)=a_o mu(d_phys)log(r_p),
D_x(nu_p)=d_phys r_p-T_o-2.                           (1.4)
```

A hybrid atom is

```text
nu_h=(o,d_rough,e_sieve,r_h),
e_sieve|P(z),
u_h=e_sieve r_h-2 in I_x,
d_rough|u_h,
A_x(nu_h)=-a_o C_z W_z g_z(d_rough)mu(e_sieve),
D_x(nu_h)=e_sieve r_h-T_o-2.                         (1.5)
```

All displayed atom families are finite for fixed `x`.  With

```text
G_x(alpha)=sum_(nu)A_x(nu)e(alpha D_x(nu)),           (1.6)
```

the exact physical statement is

```text
S_x=int_0^1 G_x(alpha)dalpha
   =sum_(nu:D_x(nu)=0)A_x(nu).                       (1.7)
```

Equation (1.7) retains the original occurrence multiplicity, the `+2,-1`
coefficients, the physical shell, the shifted determinant, the prime/hybrid
sign, and the factor `1/log(T_o)`.  It does not replace equality by a
congruence.

## 2. Typed alphabet

The following indices have different mathematical types:

```text
d_phys   physical divisor in Lambda(u+2),
d_rough  divisor in the tensor-local comparison,
e_sieve  small sieve divisor of P(z),
q_J      Jutila modulus,
a_J      reduced Jutila numerator,
beta_J   Jutila archimedean shift,
d_J      divisor of q_J in Blomer--Li (2.2),
ell_J    rational-evaluation index in Blomer--Li (2.2),
c_F      Farey denominator,
b_F      reduced Farey numerator,
z_F      Farey archimedean shift,
u_F      Farey additive detector frequency,
t_F      integer in the Farey interval I(c_F,z_F),
d_BL     later Poisson variable in the Blomer--Li proof,
m_BP,n_BP,a_BP,c_BP  Blomer--Pascadi input labels.     (2.1)
```

In particular,

```text
d_phys != d_J != d_BL,
q_J != c_F,
q_J != d_phys,
c_BP may equal c_F only after an explicit compiler,
c_BP may equal q_J only inside a separately proved local slice. (2.2)
```

No later formula may use a shared letter to erase these distinctions.

## 3. Universal Jutila interface

The source is Blomer--Li,
[*A higher rank shifted convolution problem with applications to
L-functions*](https://arxiv.org/html/2511.03294v1), Section 2.1, Lemma 1.
It assumes

```text
Q_src>=1,
omega:[1,Q_src]->[0,infinity),
L=sum_q phi(q)omega(q) != 0,
psi:R->[0,1] smooth, supported on [-1,1], integral psi=1,
0<delta<1/2.                                         (3.1)
```

The source defines

```text
chi(alpha)=1/(delta L)
 sum_q omega(q)sum_(a mod q)^*sum_(k in Z)
 psi((alpha-a/q+k)/delta)                            (3.2)
```

and proves

```text
int_0^1|1-chi(alpha)|^2 dalpha
 <<_psi Q_src^2||omega||_infinity|log delta|^3/(L^2 delta).
                                                               (3.3)
```

V23 specializes this universal identity by

```text
Q_mes=x^(1/3), Q_src=2Q_mes,
omega_pr(q)=1_(q prime,Q_mes<q<=2Q_mes),
L_pr=sum_(q in prime shell)(q-1),
eta=1/32,
delta_pr=Q_mes^(-2+eta)=Q_mes^(-63/32)=x^(-21/32).   (3.4)
```

The exact split is only the identity `1=chi+(1-chi)`:

```text
S_x=M_x+E_x,
M_x=int_0^1 chi(alpha)G_x(alpha)dalpha,
E_x=int_0^1(1-chi(alpha))G_x(alpha)dalpha.            (3.5)
```

For the Fourier convention
`hatpsi(y)=int_R psi(v)e(-yv)dv`, expansion of (1.6) gives the exact main
kernel

```text
M_x=sum_nu A_x(nu)K_chi(D_x(nu)),

K_chi(D)=1/L sum_q omega(q)c_q(D)hatpsi(-delta D),

c_q(D)=sum_(a mod q)^*e_q(aD).                       (3.6)
```

For a prime `q`, `c_q(D)=q-1` if `q|D` and `-1` otherwise.  Therefore the
Jutila main contains all determinant copies; it is a weighted Ramanujan
kernel, not an exact diagonal.  Writing it as

```text
1/R_x sum_q [R_x/(delta L)](...)
```

does not create a free `1/R_x` gain: the two factors cancel before any
estimate.

## 4. Corrected Farey/Kloosterman atomization of the error

Blomer--Li Lemma 2, equations (2.3)--(2.8), starts from the exact Farey
partition, but its displayed refinement is not literally correct as printed.
Equation (2.5) writes

```text
(C-c,max(1/(c|z|)-c,C)],                              (4.1)
```

and (2.4) uses `e_c(u t)e_c(u inverse(b))` on both signs of `z`.  Both
features have finite counterexamples.  For `C=c=1,z=1/4`, the printed
interval contains three integers although the Farey-arc indicator is one;
as `z` tends to zero its cardinality is unbounded.  For
`C=5,c=3,b=1,z=-1/22`, the actual left-neighbor denominator is `4`, but the
printed fixed-plus detector is zero.

The proof immediately above (2.7) supplies only the exact neighbor relations
used in the repository repair.  If `b'/c'` and `b''/c''` are the left and
right level-`C` neighbors of `b/c`, then

```text
C-c<c',c''<=C,
c' congruent inverse(b) mod c,
c'' congruent -inverse(b) mod c.                     (4.2)
```

For `z!=0`, define

```text
I_C^corr(c,z)
 =(C-c,min(1/(c|z|)-c,C)] intersect Z,
sigma(z)=+1 if z>0, -1 if z<0.                       (4.3)
```

The interval has length at most `c`, so it contains at most one representative
of each residue class.  The exact arc indicator is therefore

```text
1/c sum_(u mod c)sum_(t_F in I_C^corr(c,z))
 e_c(u t_F)e_c(sigma(z)u inverse(b)).                 (4.4)
```

At `z=0` either value of `sigma` may be chosen; this measure-zero convention
does not change an integral.  Summing the corrected indicators over the exact
Farey partition gives, for every smooth one-periodic `f`,

```text
int_0^1 f(alpha)dalpha
 =sum_(c<=C)int_(-1/(cC))^(1/(cC)) 1/c
   sum_(u mod c)sum_(t_F in I_C^corr(c,z))e_c(u t_F)
   sum_(b mod c)^*e_c(sigma(z)u inverse(b))
   f(b/c+z)dz.                                       (4.5)
```

Thus (4.5) is a repository-derived exact correction of the printed source,
not a verbatim source-backed use of Lemma 2.  Record the firewall

```text
V24_BLOMER_LI_LEMMA2_AS_PRINTED_MAX_FIXED_PLUS
 = STOP_SCOPED_LITERAL_FAREY_COUNTEREXAMPLES;
V24_CORRECTED_SIGNED_FAREY_IDENTITY
 = PROVED_EXACT_L0_REPOSITORY_DERIVATION.             (4.6)
```

Apply (4.5) to `f=(1-chi)G_x`.  Split `1-chi` into the identity branch and
the negative `chi` branch.  For one physical atom of mismatch `D`, the
complete `b`-sum in the identity branch is

```text
sum_(b mod c)^*e_c(bD+sigma(z)u inverse(b))
 =S(D,sigma(z)u;c),                                  (4.7)
```

where `S` is the unnormalized complete Kloosterman sum.  Consequently

```text
E_x^(1)=sum_nu A_x(nu)sum_(c<=C)int dz 1/c
 sum_(u mod c)sum_(t_F in I_C^corr(c,z))
 e_c(u t_F)e(zD_x(nu))S(D_x(nu),sigma(z)u;c).        (4.8)
```

This proves a literal complete-Kloosterman atomization after the explicit
repository correction.  It does not prove a bound, a short support statement,
or a Blomer--Pascadi attachment.

## 5. Rational evaluation of chi and the signed emitter

Blomer--Li equation (2.2) has two exactly equal forms:

```text
chi(b/c+z)
 =1/L sum_q omega(q)sum_(d_J|q)d_J mu(q/d_J)
   sum_ell hatpsi(delta d_J ell)e(-(b/c+z)ell),       (5.1)

chi(b/c+z)
 =1/(delta L)sum_q omega(q)sum_(d_J|q)mu(q/d_J)
   sum_(ell congruent b d_J mod c)
   psi(delta^(-1)(ell/(c d_J)+z)).                   (5.2)
```

There is no extra factor `q` in (5.2).  For prime `q`, the `d_J=1` branch
has sign `-1` and the `d_J=q` branch has sign `+1` inside `chi`.

Substitution into the corrected identity (4.5) gives the exact
negative-`chi` contribution

```text
E_x^(-chi)=-1/(delta L)
 sum_nu sum_q omega(q)sum_(d_J|q)mu(q/d_J)
 sum_(c<=C)int dz 1/c
 sum_(u mod c)sum_(t_F in I_C^corr(c,z))
 sum_(b mod c)^*sum_(ell congruent b d_J mod c)
 A_x(nu)e_c(u t_F+sigma(z)u inverse(b)+bD_x(nu))
 e(zD_x(nu))psi(delta^(-1)(ell/(c d_J)+z)).          (5.3)
```

The identity branch (4.4), both prime `d_J` branches in (5.3), all
`q,c,b,u,t_F,ell,z` labels, and both physical channels must be assembled
before the unique physical outer absolute value.  This defines the primary
new construction gate

```text
V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER
 = OPEN_NEW_CONSTRUCTION.                             (5.4)
```

The `ell=0` branch, nonunits, `D=0`, `u=0`, prime powers, perfect powers,
hard-shell endpoints, rough tails, smoothing tails, and hybrid zero modes
remain separate registry rows.

## 6. Exact finite type diagnostic

The checker first attacks the source correction itself:

```text
C=c=1,z=1/4:
  printed max interval cardinality = 3,
  corrected min interval cardinality = 1;

C=5,c=3,b=1,z=-1/22:
  I_C^corr={3,4},
  fixed-plus detector = 0,
  signed negative detector = 3.                     (6.1)
```

The last value is the unnormalized additive-character sum; division by `c`
gives the required indicator one.

Use the V19 literal raw row at `x=166`.  It has

```text
beta support=30,
sum_t beta_166^raw(t)=839/42.                         (6.2)
```

For a type diagnostic only, not for an actual residual theorem, set `q=7`
and use the source-backed local profile

```text
d_7(0)=0,
d_7(-2)=-35/36,
d_7(a)=7/36 otherwise.                               (6.3)
```

On the strict shell this synthetic profile has support `71` and sum `-7/36`.
Periodize `beta` and this profile modulo `c=5`:

```text
B=(43/3,1/2,3,1/7,2),
W=(7/12,-7/9,7/18,7/18,-7/9).                       (6.4)
```

The determinant-difference residue coefficient

```text
kappa(n)=sum_(a mod c)B(a)W(a+n)                     (6.5)
```

is

```text
kappa=(275/36,-943/108,53/27,821/108,-2669/216).
                                                               (6.6)
```

It has full support `5/5`, `kappa(0)=275/36`, and total `-839/216`.  At
`c=7`, the same construction has support `7/7` and
`kappa(0)=407/108`.  Thus neither the determinant zero mode nor the
Kloosterman axes disappear automatically.

For every tested `u` and both `sigma=+1,-1`, direct cyclotomic coefficient
collection verifies

```text
 sum_(t,v)beta(t)d_7(v)
 sum_(b mod c)^*X^((v-t)b+sigma u inverse(b))

 =sum_(n mod c)kappa(n)
  sum_(b mod c)^*X^(nb+sigma u inverse(b))           (6.7)
```

in `Q[X]/(X^c-1)`.  This is a type and periodization fixture only.  It gives
no growing cancellation and does not replace `w_x^(z)` by the synthetic
profile in the theorem target.

The local `ell=0` condition in (5.2) is also non-vacuous.  Since `b` is a
unit, it requires `c|d_J`; for prime `q=7`, it is present at `c=7,d_J=7`
and absent at `c=5`.

## 7. Direct Blomer--Li transfer is stopped

Lemma 1 is source-backed and reusable.  From Lemma 2 only the exact Farey
partition and neighbor relations used in the repository derivation are
retained; its printed `max`/fixed-plus display remains the scoped stop in
(4.6).  The proved Blomer--Li Theorems 1 and 2 are about

```text
sum_(lambda_1 m-lambda_2 n=h)A(n,1)tau(m)smooth_weights
```

and its smooth two-divisor variant.  Their proof uses divisor Voronoi in the
`tau` variable and GL(3) Voronoi in the `A(n,1)` variable.  There is no
source-backed transform with the same output, uniform constants and tails
for the ordered V19 HB2 Möbius/log row and the literal
`Lambda-b_x^(z)` channel.

The source proof also chooses at equation (3.14)

```text
omega_BL(q)=sum_(p t=q,
 p prime,Q_1/2<=p<=Q_1,
 p not dividing h lambda_1 lambda_2)rho(t/Q_2),       (7.1)
```

where `rho:[1/2,1]->[0,1]` is fixed, smooth and nonzero.  Immediately before
Poisson summation in its later `d_BL` variable, the paper states that `t`
must carry no arithmetic restriction; in particular `t` cannot be restricted
to primes.  The prime-only V23 shell therefore cannot be called the
factorable source weight by setting one growing factor to `1`.

The source's internally consistent optimized total scale is

```text
Q_1=x^(4/21), Q_2=x^(8/21), Q=Q_1Q_2=x^(4/7),
C_0=x^(19/42-o(1)), C=x^(23/42+o(1)),
delta=x^(-1+o(1)).                                   (7.2)
```

Version 1 prints `q^(8/21)` once in (3.42); `x^(8/21)` in (7.2) is the
explicit inference forced by `Q=Q_1Q_2=x^(12/21)`, not a silent quotation.

The Blomer--Li error bound (3.25) contains

```text
x^(1+epsilon)[x/(Q C_0)+C/Q+...].                    (7.3)
```

At the V23 clock `Q=x^(1/3)`, its own dualization constraints give
`C_0<=x^(1/2+o(1))` and `C>=x^(1/2+o(1))`; each of the first two bracket
terms is at least `x^(1/6+o(1))`.  Thus the transferred bound would be
`x^(7/6+o(1))`, not a saving.

Finally, the complete `b`-sum in that proof is a one-dimensional
GL(3)-Voronoi character sum of the form

```text
Sigma(c)=sum_(b mod c)^*e_c(bh+inverse(b)d)
 S(inverse(b),n_2;c/n_1),                            (7.4)
```

bounded through Blomer--Li Lemma 7.  It is not the two arbitrary interval
arrays in Blomer--Pascadi Theorem 1.1.  The two papers are independent
primary inputs; Blomer--Li v1 does not cite the later Blomer--Pascadi v1.

Therefore

```text
V24_DIRECT_BLOMER_LI_GL3_DIVISOR_TO_LITERAL_TPC_TRANSFER
 = STOP_SCOPED_COEFFICIENT_VORONOI_CLOCK_AND_REASSEMBLY_MISMATCH;

V24_PRIME_ONLY_JUTILA_SHELL_AS_BLOMER_LI_FACTORIZABLE_WEIGHT
 = STOP_SCOPED_UNRESTRICTED_SMOOTH_t_REQUIRED_FOR_POISSON.      (7.5)
```

These stops do not stop Lemma 1, the underlying exact Farey partition, the
repository-derived corrected atomization, or a new theorem for the literal
coefficients.

## 8. What Blomer--Pascadi still supplies

Blomer--Pascadi,
[*Bilinear forms with Kloosterman sums via quadratic
characters*](https://arxiv.org/html/2607.24311v1), accepts already-emitted
arrays in intervals of lengths at most the modulus and a fixed unit.  It does
not emit those arrays from (5.3), average over the moving physical unit, or
pay the outer label family.

The V23 local `d_phys=q_J` double-Poisson island remains a legal fixed-unit
input.  It does not cover `d_phys!=q_J`, J1, the hybrid channel, zero/nonunit
axes or the whole ensemble.  At `eta=1/32`, the conditional local ledger is

```text
dual support=q^(17/32),
q-saving=11/512,
x-saving=11/1536,
strict margin=179/38400.                              (8.1)
```

All compiler and reassembly losses remain unpaid.

## 9. Route split after atomization

V23's combined compiler gate is now refined into two distinct prime-shell
theorems:

```text
V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM
 = OPEN_NEW_THEOREM;

V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER
 = OPEN_NEW_THEOREM.                                 (9.1)
```

The first must prove, for the literal fixed-`h0=2` object,

```text
|int_0^1(1-chi_pr(alpha))G_x(alpha)dalpha|
 <<_K x^(1-1/400-epsilon_0)                          (9.2)
```

for some `epsilon_0>0`.  The second must emit actual BP arrays and retain a
total additional physical loss

```text
lambda_comp<179/38400.                               (9.3)
```

A separate architectural reserve may replace the prime shell by a
source-native factorable ensemble:

```text
V24_FACTORIZABLE_AUXILIARY_JUTILA_ENSEMBLE_WITH_LITERAL_PHYSICAL_REASSEMBLY
 = OPEN_NEW_CONSTRUCTION.                             (9.4)
```

It must declare its own auxiliary modulus, unrestricted smooth `t`, nonzero
normalizer, Jutila error, clock, literal coefficient attachment and complete
loss ledger.  It receives no credit from V21's prime-shell mean and no
automatic `41/42` credit from Blomer--Li.

The V23 stable-block dynamical reserve and the independent A1/A2 analytic
reserves remain open and unchanged.

## 10. Loss ledger and release boundary

A successful main compiler must pay

```text
lambda_comp=
 lambda_atom+lambda_coeff+lambda_smooth+lambda_interval
 +lambda_norm+lambda_unit+lambda_zero_axis+lambda_outer
 +lambda_hybrid+lambda_tail+lambda_ensemble+lambda_cover
 <179/38400.                                         (10.1)
```

The Jutila error still has only

```text
|E_x|<=||1-chi||_2||G_x||_2.
```

At the prime clock a pure energy proof would require

```text
||G_x||_2<=x^(1+theta+o(1)), theta<13/4800,          (10.2)
```

while the committed crude bound is `x^(3/2+o(1))`.

The companion checker verifies the typed alphabet, exact finite determinant
identity, prime Ramanujan kernel, rational `chi` branches, the printed
max/fixed-plus Farey counterexamples, the corrected min/signed detector,
complete-Kloosterman periodization on both half-arcs, factorability witness,
exponent clock, literal dependency paths/hashes, and all claim firewalls.  It
does not certify
(9.2), (9.3), a BP emitter, a factorable physical compiler, an arithmetic
saving, or TPC.

The final state is

```text
V24_LITERAL_DETERMINANT_JUTILA_FAREY_ATOMIZATION
 = PROVED_EXACT_L0
V24_BLOMER_LI_LEMMA1_JUTILA_INTERFACE
 = PROVED_SOURCE_BACKED
V24_BLOMER_LI_LEMMA2_AS_PRINTED_MAX_FIXED_PLUS
 = STOP_SCOPED_LITERAL_FAREY_COUNTEREXAMPLES
V24_CORRECTED_SIGNED_FAREY_IDENTITY
 = PROVED_EXACT_L0_REPOSITORY_DERIVATION
V24_BARE_FAREY_B_SUM_TO_COMPLETE_KLOOSTERMAN_BILINEAR
 = PROVED_EXACT_L0
V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER
 = OPEN_NEW_CONSTRUCTION
V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM
 = OPEN_NEW_THEOREM
V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER
 = OPEN_NEW_THEOREM
V24_FACTORIZABLE_AUXILIARY_JUTILA_ENSEMBLE_WITH_LITERAL_PHYSICAL_REASSEMBLY
 = OPEN_NEW_CONSTRUCTION
V24_DIRECT_BLOMER_LI_GL3_DIVISOR_TO_LITERAL_TPC_TRANSFER
 = STOP_SCOPED_COEFFICIENT_VORONOI_CLOCK_AND_REASSEMBLY_MISMATCH
V24_PRIME_ONLY_JUTILA_SHELL_AS_BLOMER_LI_FACTORIZABLE_WEIGHT
 = STOP_SCOPED_UNRESTRICTED_SMOOTH_t_REQUIRED_FOR_POISSON
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false.                              (10.3)
```
