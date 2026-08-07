# Bridge B V22: the centered-projector firewall and the two surviving compilers

Date: 2026-08-07

Status:

```text
COMPLETE_PRIME_ENSEMBLE_CENTERED_OPERATOR
 = PROVED_EXACT_IDENTITY_MINUS_LOW_RANK_MEAN_OPERATOR;

DIRECT_RESIDUE_FOURIER_TO_KLOOSTERMAN
 = STOP_SCOPED_EXACT_ZERO_MARGINAL_AND_KERNEL_MISMATCH;

DIRECT_MESOSCOPIC_PROJECTOR_DISPERSION
 = STOP_SCOPED_PAID_MEAN_BRANCH_ONLY;

LITERAL_SHBD2_DIAGONAL_POST_POISSON_COMPILER
 = OPEN_CONDITIONAL;

BP_LOCAL_X_SAVING_BEFORE_COMPILER_LOSSES
 = CONDITIONAL_X_MINUS_1_OVER_96;

V21_TO_ODOMETER_DISTINGUISHED_ORBIT_SUM
 = PROVED_EXACT_L0_NO_CANCELLATION;

TRANSVERSAL_COMMON_RETURN_CENTERED_PHYSICAL_CARRIER
 = OPEN_NEW_CONSTRUCTION;

ARITHMETIC_ADVANCE = NO;
STRICT_1_OVER_400 = UNPAID;
L2 = NONE;
TPC_207_TRIGGER = false.
```

The point of this gate is route selection, not another small variant of the
V21 split.  It proves that a direct transform of the mesoscopic residue
projectors can only repackage the already-paid mean branch.  It also records
two genuinely surviving highways: a source-compatible post-Poisson compiler
for the central HB2 cell, and a common-return transversal dynamical carrier.

## 1. Frozen physical object

Keep the V19--V21 object literally:

```text
h0=2,
x=2X,
I_x={t in Z:x/2<t<=x},
H=#I_x=X,
z=(log x)^K,
w_x^(z)(t)=Lambda(t+2)-b_x^(z)(t),
beta_x^raw(t)=the combined V19 MASTER coefficient,

Q=x^(1/3),
Q_x={q prime:Q<q<=2Q},
R=#Q_x.                                                (1.1)
```

The literal `+2,-1` HB2 outer constants, all Möbius signs,
`log(f_1)/log(t)`, the strict shell, the complete equal-weight prime
ensemble and the actual ragged fiber counts remain frozen.  `Q` in (1.1) is
the V21 mesoscopic scale, not the physical packet parameter
`X^(267/400+o(1))`.

For `a mod q`, write

```text
I_(q,a)={t in I_x:t=a mod q},
n_(q,a)=#I_(q,a),
B_(q,a)=sum_(t in I_(q,a))beta_x^raw(t),
W_(q,a)=sum_(t in I_(q,a))w_x^(z)(t).                 (1.2)
```

V21 proved, for every fixed `A,K`,

```text
S_x=Hbar_Q+Cbar_Q,
Hbar_Q<<_(A,K)x/log^A x,                              (1.3)

S_x=sum_(t in I_x)beta_x^raw(t)w_x^(z)(t).
```

Thus `Cbar_Q` is equivalent at arbitrary log-power scale to the original
combined raw MASTER scalar.  V22 does not reopen or weaken the paid mean.

## 2. Exact counting projectors

On `V_x=C^(I_x)`, use the counting Hermitian geometry

```text
(f,g)_2=sum_(t in I_x)f(t)conjugate(g(t))
```

for orthogonality, positivity and operator norms.  The physical covector
evaluation is instead the no-conjugation bilinear form

```text
[beta,f]=sum_(t in I_x)beta(t)f(t).
```

All finite physical vectors used below are real, but this distinction fixes
the types.  Define

```text
(E_(x,q)f)(t)
 =1/n_(q,t mod q)
  sum_(u in I_x,u=t mod q)f(u).                       (2.1)
```

Each `E_(x,q)` is the orthogonal projector onto functions constant on the
actual shell fibers.  Put

```text
Pbar_x=R^(-1)sum_(q in Q_x)E_(x,q).                   (2.2)
```

Then, with the physical bilinear evaluation,

```text
Hbar_Q=[beta_x^raw,Pbar_x w_x^(z)],
Cbar_Q=[beta_x^raw,(I-Pbar_x)w_x^(z)].                (2.3)
```

The matrix kernel of the paid operator is exact:

```text
Pbar_x(t,u)
 =R^(-1)sum_(q in Q_x)
   1_(q divides t-u)/n_(q,t mod q).                   (2.4)
```

This is a ragged congruence projector.  It is not a Kloosterman kernel.

## 3. Residue Fourier annihilation

For one `q`, set

```text
r_q(t)=[(I-E_(x,q))w_x^(z)](t)
      =w_x^(z)(t)-W_(q,a)/n_(q,a),  t in I_(q,a).     (3.1)
```

By construction,

```text
sum_(t in I_(q,a))r_q(t)=0                            (3.2)
```

for every actual fiber, including the two ragged sizes.  Hence for every
`h mod q`,

```text
sum_(t in I_x)r_q(t)e(ht/q)
 =sum_(a mod q)e(ha/q)sum_(t in I_(q,a))r_q(t)
 =0.                                                  (3.3)
```

All residue-only Fourier marginals vanish identically.  Nevertheless,

```text
C_q=sum_(t in I_x)beta_x^raw(t)r_q(t)                 (3.4)
```

need not vanish because the physical coefficient varies inside a fiber.
The missing information is a within-fiber covariance, not a nonzero
frequency on `Z/qZ`.

There is an exact information-loss fixture using a literal physical
coefficient but a deliberately synthetic second vector.  At `x=166,q=7`,
set

```text
w_syn(t)=beta_166^raw(t),
r_syn=(I-E_(166,7))w_syn.                             (3.5)
```

Every residue marginal of `r_syn` vanishes, while exact rational arithmetic
gives

```text
<beta_166^raw,r_syn>=2359675/77616.                  (3.6)
```

This proves that the residue transform loses within-fiber information even
when the coefficient is literal.  It is not a computation of the actual
prime residual `w_166^(z)` and gives no arithmetic credit.

Writing `t=a+qk` makes the scale mismatch explicit:

```text
#k=n_(q,a) asymp X/q asymp x^(2/3) asymp q^2.         (3.7)
```

A direct residue DFT sees only (3.3), while the natural quotient interval is
much longer than the modulus.  Parseval on residues therefore cannot be
renamed as a bound for (3.4).

## 4. The complete ensemble still leaves an identity space

Every `E_(x,q)` is positive semidefinite.  Consequently,

```text
ker(Pbar_x)=intersection_(q in Q_x)ker(E_(x,q)),       (4.1)

rank(Pbar_x)
 <=sum_(q in Q_x)rank(E_(x,q))
 <=sum_(q in Q_x)q
 =O(Q^2)=O(x^(2/3)).                                  (4.2)
```

No prime number theorem is required for the last upper bound: there are at
most `Q+1` integers in `(Q,2Q]`, each at most `2Q`.  Since `H=x/2`, (4.2)
gives

```text
dim ker(Pbar_x)>=x/2-O(x^(2/3)).                      (4.3)
```

For sufficiently large `x`, this kernel is nonzero.  On it,

```text
(I-Pbar_x)v=v,
||I-Pbar_x||_(2->2)=1.                                (4.4)
```

There is also an explicit common-kernel construction.  If

`sum_(q in Q_x)q<H`, choose a shift `t_0` so the support stays in `I_x` and
define the coefficient vector of

```text
z^(t_0)product_(q in Q_x)(1-z^q).                    (4.5)
```

For every selected `q`, (4.5) is a `q`-step finite difference.  Its sum in
each residue class modulo `q` is zero, so it lies in (4.1), and its constant
coefficient makes it nonzero.  This is an exact complete-ensemble witness,
not a statement about the actual residual.

For the V21 finite ensemble `x=1000`,

```text
Q_x={11,13,17,19},
H=500,
dim span_(q) ran(E_q)
 =1+sum_(q in Q_x)(q-1)=57,
dim ker(Pbar_x)=443.                                  (4.6)
```

The rank in (4.6) follows either from exact elimination or from the
Vandermonde independence of the distinct nontrivial roots of unity on at
least 57 consecutive integers.

This stops automatic complete-ensemble compression.  It does not forbid a
new theorem exploiting the literal arithmetic vectors.

## 5. Why direct projector dispersion touches only the paid branch

The exact pair identity is

```text
C_q=sum_(a mod q)1/(2n_(q,a))
 sum_(t,u in I_(q,a))
 [beta(t)-beta(u)][w(t)-w(u)].                        (5.1)
```

Expanding (5.1) gives, without approximation,

```text
C_q=S_x-H_q.                                          (5.2)
```

If the zero pairs `t=u` are omitted before expansion, the two self terms
have coefficient

```text
(n_(q,a)-1)/n_(q,a)=1-O(x^(-2/3)).                   (5.3)
```

Thus the self/identity part is

```text
D_q=S_x-sum_(a mod q)1/n_(q,a)
                 sum_(t in I_(q,a))beta(t)w(t)
    =S_x+O_K(x^(1/3)log^C x),                        (5.4)
```

using the committed divisor bounds.  The off-diagonal cross part is
`-H_q` plus the opposite correction in (5.4).  Averaging over `q` preserves
the same identity.

Therefore an additive-congruence, determinant, Poisson or Kloosterman
expansion applied only to `Pbar_x` rewrites `Hbar_Q`, the branch already paid
in (1.3).  The identity branch `S_x` has no mesoscopic `q` modulus and remains
unchanged.  The pair-difference notation does not delete it.

The exact scoped stop is

```text
DECLARED_TPC_BRIDGE_B_20260807_COMPLETE_MESOSCOPIC_PRIME_ENSEMBLE_
DIRECT_PROJECTOR_DISPERSION_OR_KLOOSTERMAN_BYPASS_V1
 = STOP_SCOPED_PAID_MEAN_BRANCH_AND_IDENTITY_SPACE.    (5.5)
```

This does not stop a source-structured transform of the original literal
`S_x`, nor a joint post-Poisson theorem that proves the whole equality with
all diagonal and reassembly terms.

## 6. Blomer--Pascadi: a real local engine after a missing diagonal compiler

The primary source is Blomer--Pascadi,
*Bilinear forms with Kloosterman sums via quadratic characters*,
arXiv:2607.24311v1 (2026-07-27), Theorems 1.1, 5.2 and 5.5.

For a modulus `c`, intervals of lengths at most `N<=c`, arbitrary complex
arrays and a unit `a mod c`, Theorem 1.1 bounds

```text
sum_(m,n,(m,n,c)=1) alpha_m gamma_n S(am,n;c)

 <<||alpha||_2||gamma||_2 c^(1+o(1))
   [N^(1/8)c^(-3/32)
    +N^(5/16)c^(-3/16)
    +N^(2/3)c^(-7/18)].                               (6.1)
```

At `c=q` prime and `M,N asymp q^(1/2)`, (6.1) saves

```text
q^(-1/32+o(1))=x^(-1/96+o(1))                       (6.2)
```

over the unnormalized trivial block.  Its exponent margin beyond the TPC
endpoint is

```text
1/96-1/400=19/2400>0.                                (6.3)
```

So the source theorem is quantitatively strong enough *if* an exact
physical compiler loses less than `19/2400` and all errors have a fixed
power saving.  It is not directly attached: (3.3) is zero, (3.7) has length
`q^2`, the kernel (2.4) is not `S(am,n;q)`, and the physical coefficients,
ragged weights, diagonal and reassembly are absent from the source input.

The surviving conditional contract must start from the original diagonal
`S_x`, not from the already-paid congruence projector.  For the canonical
HB2-B3 central cell, it would have to derive an exact finite equality

```text
S_x=R^(-1)sum_(q in Q_x)sum_j kappa_(q,j)
 sum_(m in M_(q,j),n in N_(q,j),(mn,q)=1)
 alpha_(q,j)(m)gamma_(q,j)(n)S(a_(q,j)m,n;q)
 +Err,                                                (6.4)
```

where

```text
|M_(q,j)|,|N_(q,j)| asymp q^(1/2),

R^(-1)sum_(q,j)|kappa_(q,j)|
 ||alpha_(q,j)||_2||gamma_(q,j)||_2 q
 <<x^(1+o(1)).                                        (6.5)
```

The compiler must retain the literal shift-two unit, `+2,-1`, Möbius/log
coefficients, the shell, `1/R`, one outer absolute and an exactly-once block
registry.  If it is derived through the V21 pair identity, it must additionally
retain and reassemble every actual `n_(q,a)`.  Zero frequencies, the original
determinant-two diagonal, nonunits, prime powers, rough tails, endpoints and
every transform tail must be classified and paid.  Under (6.4)--(6.5) and a
power-saving error,

```text
|S_x|<<x^(1-1/96+o(1))+|Err|.                         (6.6)
```

This would close every fixed log-power target and hence `Cbar_Q` by V21.  At
present (6.4) is absent, so the status is `OPEN_CONDITIONAL`, not arithmetic
credit.

The first obvious completion is already stopped.  In the coprime Lambda bulk,
Poisson can create a reciprocal phase `e_q(k(T+2) inverse(d))`; completing the
full `d mod q` coefficient creates a Kloosterman sum only after a full additive
Fourier transform.  The transformed coefficient generally occupies all `q`
frequencies.  Cutting it into `B asymp q^(1/2)` blocks and using only
black-box Cauchy gives

```text
sum_(j<=B)||a_j||_2<=B^(1/2)||a||_2
                    asymp q^(1/4)||a||_2.             (6.7)
```

This possible `q^(1/4)` factor is sharp for equal block masses.  Full support
alone does not prove that the literal coefficient saturates it; rather, a
Cauchy-only uniform proof certifies no net gain against `q^(-1/32)` without
additional block structure.  Therefore

```text
NAIVE_FULL_Q_FOURIER_COMPLETION_TO_BP_BLACK_BOX_CAUCHY
 = STOP_SCOPED_CERTIFIES_NO_NET_GAIN_WITHOUT_BLOCK_STRUCTURE.   (6.8)
```

This narrow stop does not exclude a source-exact transform whose arithmetic
coefficient already has short frequency support or a collective assembler
that avoids the possible black-box `q^(1/4)` factor.

Milićević--Qin--Wu and Kowalski--Michel--Sawin provide neighboring
Kloosterman engines after a valid compiler.  Zheng's simultaneous-AP theorem
does not substitute for it: the arbitrary-modulus exponent `7/36` is below
`1/3`, and its well-factorable slots are not the V21 centered fibers.  These
source locks may not be spliced.

## 7. Exact odometer return and the honest dynamical fork

Let `T:r -> r+1` be the adding map on the profinite integers with
distinguished seed `0`.  Define the finite orbit table directly by

```text
Phi_x(T^t0):=beta_x^raw(t)/R
 sum_(q in Q_x)[(I-E_(x,q))w_x^(z)](t),  t in I_x.   (7.1)
```

Because `T^t(0)=t`, the V21 scalar has the lossless orbit-sum encoding

```text
Cbar_Q=sum_(x/2<t<=x)Phi_x(T^t0).                     (7.2)
```

The inverse-limit digit system, or its Bratteli--Vershik adding-path model,
is a stage-preserving symbolic representation.  If a global locally constant
function is desired, choose a cylinder modulus `M_x>x` and extend this finite
table arbitrarily off the listed orbit points.  No uniform regularity bound
is claimed.  Equation (7.2) preserves the distinguished arithmetic seed and
all physical normalization.

It gives no cancellation.  The orbit table in (7.1) depends on `x`, the
complete modulus ensemble, the raw coefficient and the prime residual.  It
has no source-backed uniform BV/Hölder norm, independent zero mean, variance
bound or martingale/coboundary decomposition.  Centering `w` does not center
the product `beta*w`; that product is precisely the unknown covariance.

Existing sequential ASIP and dynamical Borel--Cantelli theorems are metric:
they apply almost surely under uniform map/observable hypotheses.  Logistic
parameter-typicality theorems are for almost every parameter.  None proves
that a fixed arithmetic seed lies in the full-measure set, and none supplies
an exact physical intertwiner for (7.1).  Ordinary ergodicity or positive
event measure therefore cannot be attached to (7.2).

The strongest honest conditional dynamics is a predeclared positive-measure
transversal family `lambda` with:

```text
J_(lambda,x)E_(x,q)
 =E_(lambda,x,q)^dyn J_(lambda,x)                     (7.3)
```

coefficientwise for every `q`, and a common return

```text
Cbar_Q=sum_(t in I_x)
 phi_(lambda,x,t)(F_(lambda,x)^[t]z_lambda)           (7.4)
```

whose left side is independent of `lambda`.  It must additionally prove an
independent carrier mean of arbitrary log-power size and, for one good
parameter supplied by a genuine transversal theorem, a uniform triangular
pointed bound

```text
|orbit sum-carrier mean|
 <<x^(1-delta)(log x)^M                               (7.5)
```

for some fixed `delta>0` and all sufficiently large stages.  Since every
fixed power saving beats every fixed log power, (7.3)--(7.5) would close
`Cbar_Q` without declaring one preselected parameter typical by fiat.

The common-return family, its independent mean and the triangular pointed
theorem are all absent.  Hénon can only be an exact natural extension after
the factor, observable, measure and distinguished section all commute; it
does not repair the missing base covariance.

## 8. Finite fixtures and trust boundary

The companion checker verifies with exact integer/rational arithmetic:

- wrapped projector and pair identities with ragged fibers;
- every residue marginal in (3.2), which implies (3.3);
- the complete-ensemble kernel formula (2.4);
- exact rank `57` and common-kernel dimension `443` for (4.6);
- the finite-difference witness (4.5) for `q=11,13,17,19`;
- the synthetic `w_syn=beta_166^raw` information-loss fixture (3.5)--(3.6),
  explicitly not the physical residual;
- the identity/off-diagonal expansion (5.2)--(5.4);
- the odometer return (7.2) on independent rational fixtures;
- the exponent identities (3.7), (6.2) and (6.3);
- strict contract and semantic-registry mutation rejection.

The checker does not prove the Blomer--Pascadi theorem, a post-Poisson
compiler, source absence, a Logistic/Hénon intertwiner, an ASIP theorem or
the open arithmetic covariance.

## 9. Exact route verdict

V22 adds two broad scoped stops:

```text
DECLARED_TPC_BRIDGE_B_20260807_CENTERED_RESIDUAL_DIRECT_MOD_Q_FOURIER_
OR_KLOOSTERMAN_ATTACHMENT_V1
 = STOP_SCOPED_EXACT_ALL_RESIDUE_MARGINALS_ZERO;

DECLARED_TPC_BRIDGE_B_20260807_COMPLETE_MESOSCOPIC_PRIME_ENSEMBLE_
DIRECT_PROJECTOR_DISPERSION_OR_KLOOSTERMAN_BYPASS_V1
 = STOP_SCOPED_PAID_MEAN_BRANCH_AND_IDENTITY_SPACE.    (9.1)
```

They stop only direct residue/projector attachments.  They do not stop:

```text
V22_LITERAL_SHBD2_DIAGONAL_POST_POISSON_COMPILER_GATE
 = OPEN_CONDITIONAL;

V22_COMMON_RETURN_TRANSVERSALITY_COMPATIBILITY
 = INDEPENDENT_OPEN_DYNAMICAL_CONSTRUCTION;

SHB_D2_LITERAL_DETERMINANT_MASTER
 = OPEN_NEW_ARITHMETIC_THEOREM.                       (9.2)
```

The analytic gate starts from the literal determinant-two diagonal and asks
whether the canonical HB2-B3 cell actually emits two independent `q^(1/2)`
Kloosterman variables with the ledger (6.5), without relying on the stopped
black-box Cauchy-only completion.  A `q^2` fiber autocorrelation, dependent
arrays or an unpaid diagonal remains fatal; a full-spectrum coefficient is
fatal only if no additional block structure or collective assembler avoids
the possible `q^(1/4)` factor.  The dynamical gate first asks
whether an open parameter family can preserve the same coefficientwise
return at two adjacent stages while retaining nondegenerate transversality
and only polylogarithmic observable loss.

No numbered paper, PDF, build output or TPC-207 is created.  Fixed-atom
credit remains zero, strict `1/400` remains unpaid, `L2=NONE`, and all older
scoped stops remain frozen.
