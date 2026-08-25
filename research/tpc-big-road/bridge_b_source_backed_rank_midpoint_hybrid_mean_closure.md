# Bridge B V107: source-backed rank-midpoint hybrid-mean closure

Date: 2026-08-26

Status: `PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_ADJOINT_LANE_SOURCE_GAP`

TPC-254 audits the two literal moments isolated by TPC-253.  The physical
hybrid residual `w` is already covered by the source-backed maximal-interval
Type-I theorem: its `m=1` row pays both deterministic rank children to every
fixed logarithmic order.  No locked theorem pays the second moment
`<z_mid,A_x beta>` beyond the exact adjoint identity and Cauchy.  The two lanes
are therefore separated rather than promoted together.

## 1. Frozen physical data and notation

Fix a finite admissible `K>0` and write

```text
Z_x=(log x)^K,
w(u)=Lambda(u+2)-b_x^(Z_x)(u).
```

The symbol `Z_x` is the hybrid cutoff.  It is distinct from the real rank
contrast `z_mid`.  On

```text
I_x=(x/2,x] intersect Z={n_1<...<n_N},
N=floor(x)-floor(x/2)>=2,
```

retain TPC-253's source-frozen split

```text
ell=floor(N/2), r=N-ell,
L={n_1,...,n_ell}, R={n_(ell+1),...,n_N},
rho^2=ell*r/N,
z_mid=rho(1_L/ell-1_R/r).
```

Both children are consecutive integer intervals for every real `x`.  No
integer-only `floor(3x/4)` threshold is used when `x` is nonintegral.

## 2. Source-backed maximal-interval extraction

The hybrid H2 theorem in `fm_local_comparison_compiler.md` states that for
every fixed `gamma<1/2` and every requested fixed logarithmic strength, the
maximal Type-I sum has the form

```text
sum_(m<=x^gamma) tau(m)^B max_J
  |sum_(x/2<ms<=x, s in J) w(ms)|
  <<_(B,K,gamma) x/(log x)^B.                         (2.1)
```

Here `J` ranges over active integer intervals.  Section 8.3 of that compiler
proves the hybrid comparison side uniformly in `J`, and maximal
Bombieri--Vinogradov supplies the shifted-prime side.  Every summand in (2.1)
is nonnegative.

Freeze, for example, `gamma_0=1/4`.  For sufficiently large `x`, the row
`m=1` occurs and has weight `tau(1)^B=1`.  It follows directly, without any
signed extraction, that for every fixed target `M>0`,

```text
max_(J consecutive, J subset I_x) |sum_(u in J)w(u)|
 <<_(M,K) x/(log x)^M.                               (2.2)
```

In particular, with

```text
W_L=sum_(u in L)w(u),
W_R=sum_(u in R)w(u),
```

one has

```text
max(|W_L|,|W_R|)<<_(M,K)x/(log x)^M.                 (2.3)
```

This is a source-backed corollary of a proved maximal-interval theorem.  It is
not numerical evidence and it is not obtained from the V21 full-shell AP
mean.

## 3. Child means and the literal midpoint `w` moment

The exact cardinality ledger is

```text
N=x/2+O(1), ell=x/4+O(1), r=x/4+O(1).
```

Thus (2.3) gives

```text
|W_L/ell-W_R/r|<<_(M,K)(log x)^(-M).                 (3.1)
```

More precisely,

```text
rho^2=ell*r/N
     =N/4                         if N is even,
     =N/4-1/(4N)                  if N is odd,
```

and hence

```text
rho^2=x/8+O(1),
rho=x^(1/2)/(2sqrt(2))+O(x^(-1/2)).                  (3.2)
```

TPC-253's exact partial-sum identity now yields the arithmetic conclusion

```text
|<z_mid,w>|
 =rho|W_L/ell-W_R/r|
 <<_(M,K) x^(1/2)/(log x)^M.                         (3.3)
```

The statement holds for every fixed `M`, with a constant depending on `M,K`.
It is arbitrary fixed logarithmic saving, not a fixed power saving.

## 4. Quantifier firewall

The isolated TPC-254 corollary uses the order

```text
fixed finite admissible K
 -> freeze gamma_0=1/4
 -> target M
 -> choose a sufficiently strong integer H2 exponent B
 -> choose delta<1-gamma_0
 -> choose the divisor-tail cutoff and larger BV/fundamental-lemma saving
 -> x>=x_0(M,K).
```

The constants are not uniform as `K` tends to infinity or `gamma` tends to
`1/2`.  In the full upstream Ford--Maynard compiler, the separate order is

```text
target A,varpi -> Ford--Maynard B_FM -> fixed K=K(B_FM)
 -> x>=x_0(A,varpi,B_FM,K).
```

One fixed `K` is not claimed to pay every upstream Ford--Maynard parameter.
Moreover, for every fixed `eta,M>0`,

```text
[x^(1/2)/(log x)^M]/x^(1/2-eta)=x^eta/(log x)^M -> infinity.
```

Therefore (3.3) cannot be promoted to `x^(1/2-eta)`.

## 5. The adjoint lane remains open

Keep the literal TPC-247 operator and TPC-253 orientation.  The exact identity
is

```text
<z_mid,A_x beta>=<A_x^*z_mid,beta>,
(A_x^*z_mid)(t)=sum_(u in I_x)conjugate(A_x(u,t))z_mid(u).
```

Cauchy gives the strongest unconditional statement supported here:

```text
|<z_mid,A_x beta>|
 <=||A_x^*z_mid||_2||beta||_2.                       (5.1)
```

Combining (3.3) and (5.1) proves only the safe upper transfer

```text
|conjugate(<z_mid,w>)<z_mid,A_x beta>|
 <<_(M,K) [x^(1/2)/(log x)^M]
            ||A_x^*z_mid||_2||beta||_2.              (5.2)
```

No cancellation, sign, nonzero value, logarithmic saving or power saving for
`<z_mid,A_x beta>` is asserted.

The source typing is decisive:

| locked result | actual object | pays this lane? |
|---|---|---|
| hybrid maximal Type I | maximum over every active integer interval | yes for `w`, by `m=1` |
| V21 shifted-prime AP error | full-shell residue fibers averaged in `q` | no hard-child or adjoint test |
| V21 hybrid AP error | full-shell `I_(q,a)` fibers | no adjoint test |
| V21 paid mean | complete prime-modulus average weighted by raw `beta` | no `A_x^*z_mid` test |
| whole-shell mean | one total sum | no Haar moment |
| TPC-247/TPC-253 | exact operator and adjoint identities | no arithmetic estimate |

For the whole-shell warning, the synthetic vector `f=lambda z_mid` satisfies

```text
sum_(I_x)f=0,
<z_mid,f>=lambda.
```

Thus a total mean cannot control the midpoint moment.  The source-gap verdict
is scoped to the declared frozen corpus; it is not a universal literature
absence claim.

## 6. Sharp norm-only obstruction

Norm geometry, reality and a deleted diagonal do not improve (5.1).  Let
`N>=2`, let `z` be a real unit vector, choose a derangement `sigma`, put
`beta=1`, and define

```text
A_(i,sigma(i))=lambda z_i,
A_(i,j)=0 otherwise.
```

Then `A` is real, its diagonal is zero, and

```text
A beta=lambda z,
<z,A beta>=lambda.
```

At `N=2`, with `z=(1/sqrt(2),-1/sqrt(2))`,

```text
A=[[0,lambda/sqrt(2)],[-lambda/sqrt(2),0]],
beta=(1,1),
```

one also has

```text
||A^*z||_2||beta||_2=|lambda|=|<z,A beta>|.
```

Hence the Cauchy constant one is sharp even in this real zero-diagonal class.
These are synthetic finite controls, not literal V59 counterexamples.

## 7. Route evaluation

Strongest positive result: the actual literal `w` rank-midpoint moment has
arbitrary fixed log-power flatness,

```text
<z_mid,w><<_(M,K)x^(1/2)(log x)^(-M).
```

Strongest obstruction: every remaining midpoint transfer depends on the
unestimated literal adjoint form `<A_x^*z_mid,beta>`; norm-only information is
sharp.

Open theorem: estimate

```text
sum_(t in I_x)conjugate((A_x^*z_mid)(t))beta(t)
```

on the same V59 clock while retaining the prime shell, `q` weight, both unit
masks, deleted diagonal, `K_H`, centered residue bracket and hard rank
midpoint, with an improvement over Cauchy at a declared natural scale.

Reusable structure: hybrid maximal interval Type I -> nonnegative `m=1`
extraction -> deterministic child means -> normalized Haar moment -> push the
fixed output test through `A_x^*` -> one literal `beta`-linear form.

`ROUND2_CLUE = PUSH_THE_FIXED_RANK_MIDPOINT_HAAR_TEST_THROUGH_A_X_STAR_AND_ESTIMATE_THE_LITERAL_BETA_LINEAR_FORM_ON_THE_SAME_CLOCK_BEFORE_ANY_COVARIANCE_OR_MARGIN_PROMOTION__DO_NOT_REUSE_WHOLE_SHELL_OR_AP_AVERAGES`

## 8. Claim firewall

```text
TPC254_MAXIMUM_CLAIM = SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER_CONTROL_OF_THE_LITERAL_V59_RANK_MIDPOINT_W_CONTRAST_WITH_ONLY_EXACT_ADJOINT_CAUCHY_TRANSFER
TPC254_HYBRID_CUTOFF = SOURCE_LOCKED_FIXED_FINITE_K_NO_K_UNIFORMITY
TPC254_RANK_CHILD_INTERVAL_ADMISSIBILITY = PROVED_EXACT_FOR_REAL_X
TPC254_MAXIMAL_TYPE_I_M1_EXTRACTION = PROVED_SOURCE_BACKED
TPC254_CHILD_SUM_HYBRID_MEAN = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC254_CHILD_MEAN_DIFFERENCE = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC254_W_MIDPOINT_HAAR_MOMENT = PROVED_SOURCE_BACKED_X_ONE_HALF_TIMES_ARBITRARY_FIXED_LOG_SAVING
TPC254_SAFE_ADJOINT_CAUCHY_TRANSFER = PROVED_EXACT
TPC254_G_MIDPOINT_HAAR_ESTIMATE = OPEN_NO_FROZEN_SOURCE_ATTACHMENT
TPC254_G_LANE_SOURCE_ATTACHMENT = STOP_SCOPED_DECLARED_CORPUS_NO_FIXED_HAAR_ADJOINT_ESTIMATE
TPC254_ZERO_DIAGONAL_DERANGEMENT_OBSTRUCTION = PROVED_SYNTHETIC_NOT_LITERAL_V59
TPC254_CAUCHY_CONSTANT_ONE_SHARPNESS = PROVED_EXACT_N2_SYNTHETIC
TPC254_ARBITRARY_LOG_TO_FIXED_POWER_PROMOTION = NOT_CLAIMED
TPC254_W_CONTRAST_SIGN_OR_NONZERO = NOT_CLAIMED
TPC254_G_CONTRAST_SIGN_OR_NONZERO = OPEN
TPC254_JOINT_TRANSFER_LOWER_BOUND = OPEN
TPC254_V21_CHILD_OR_ADJOINT_SUBSTITUTION = NOT_CLAIMED
TPC254_ARITHMETIC_ADVANCE = YES_SCOPED_LITERAL_W_LANE
TPC254_FIXED_ATOM_CREDIT = 0
TPC254_L2 = NONE
TPC254_FULL_GATE_B = OPEN
TPC254_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC254_TWIN_PRIME_RESULT = NONE
TPC254_STATUS = PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_ADJOINT_LANE_SOURCE_GAP
```
