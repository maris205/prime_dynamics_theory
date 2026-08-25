# Bridge B V95: phase-Fourier separation of the unsigned collision channel

Date: 2026-08-25

Status: `PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER`.

TPC-242 answers the narrow question left by TPC-241 without inventing the
missing physical attachment.  The literal V59 projector is a nontrivial
Fourier coefficient in the four source phases.  An unsigned marginal energy
belongs to the trivial phase character.  TPC-242 computes the complete
`C_4` phase spectrum, determines the exact feasible set of the selected
cross coefficient at fixed total energy, and proves an exact defect identity.

The conclusion is deliberately typed.  TPC-241's fixed-profile lower bound
has no direct quantitative implication for the V59 signed coefficient.  This
does not prove that the physical top-prime contribution vanishes: no
source-backed theorem identifies the TPC-241 kernel with either V59 marginal
or with a phase-independent additive term in all four physical packet
energies.

## Registry and claim firewall

```text
TPC242_MAXIMUM_CLAIM = EXACT_C4_PHASE_FOURIER_SPECTRUM_SHARP_FIXED_ENERGY_CROSS_DISK_AND_TYPED_NO_TRANSFER
TPC242_ROUTE_ADVANCE = YES_OBSTRUCTION
TPC242_V59_PHASE_CONVENTION = PROVED_I_POWER_J_SELECTS_X_CONJUGATE_Y
TPC242_COMPLETE_PHASE_SPECTRUM = PROVED_F0_TOTAL_F1_ORIENTED_CROSS_F2_ZERO_F3_CONJUGATE_CROSS
TPC242_PHASE_BLIND_ADDITIVE_TERM = PROVED_TRIVIAL_CHARACTER_ONLY
TPC242_FIXED_F0_FEASIBLE_SET = PROVED_CLOSED_DISK_RADIUS_F0_OVER_TWO
TPC242_PHASE_DEFECT_IDENTITY = PROVED_IMBALANCE_SQUARED_PLUS_FOUR_GRAM_DETERMINANT
TPC242_TPC241_DIRECT_SIGNED_CREDIT = ZERO
TPC242_TPC241_TO_V59_IDENTIFICATION = OPEN
TPC242_PHYSICAL_TOP_PRIME_ANNIHILATION = NOT_CLAIMED
TPC242_LITERAL_C_H_SIGNED_CANCELLATION = NONE
TPC242_ARITHMETIC_ADVANCE = NO
TPC242_FIXED_ATOM_CREDIT = 0
TPC242_L2 = NONE
TPC242_FULL_GATE_B = OPEN
TPC242_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC242_TWIN_PRIME_RESULT = NONE
TPC242_STATUS = PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER
TPC242_ROUND2_CLUE = EXPRESS_THE_LITERAL_TOP_PRIME_CONTRIBUTION_PHASE_BY_PHASE_BEFORE_SQUARING_AND_COMPUTE_ITS_ACTUAL_K_EQUALS_ONE_COEFFICIENT
```

## 1. Source-locked orientation

V59 freezes

```text
a^(j)=beta+i^j w,  j=0,1,2,3,
mathfrak C_x=(1/4)sum_j i^j V_circle(a^(j)).
```

Its scalar identity is

```text
x conjugate(y)=(1/4)sum_j i^j |x+i^j y|^2.
```

We use the standard Hilbert convention that the inner product is
conjugate-linear in the first variable.  Then `x conjugate(y)=<y,x>`.
This is the same orientation as TPC-228 after translating its explicitly
declared linear-first convention.  No convention is silently changed.

TPC-228 additionally proves that, after the same-prime diagonal is deleted
before polarization, the selected coefficient is the off-prime form

```text
sum_(q!=r)<V_r,U_q>
```

in the present convention.  The theorem below applies to every common linear
row map, but it does not manufacture the open literal V59-to-primitive-atom
crosswalk.

## 2. Complete `C_4` phase spectrum

Let `X,Y` lie in a complex Hilbert space and put

```text
E_j=||X+i^jY||^2,
F_k=(1/4)sum_(j=0)^3 i^(kj)E_j,  k=0,1,2,3.
```

Write

```text
S=||X||^2+||Y||^2,
c=<Y,X>.
```

Expansion gives

```text
E_j=S+i^j conjugate(c)+i^(-j)c.
```

The fourth-root filter is one when its exponent is divisible by four and zero
otherwise.  Therefore

```text
F_0=S,
F_1=c=<Y,X>,
F_2=0,
F_3=conjugate(c)=<X,Y>.                         (2.1)
```

Thus phase-blind information and the V59 target occupy different irreducible
characters of `C_4`.  If a scalar `A` is genuinely added to every
`E_j`, then

```text
F'_k-F_k=A 1_(k=0).                              (2.2)
```

Equation (2.2) is exact annihilation of a proved phase-independent additive
term.  It is not permission to label an unrelated unsigned estimate as such a
term.

## 3. Sharp fixed-energy feasible disk

For fixed `S>=0`, the set of possible `c=<Y,X>` is exactly

```text
{z in C: |z|<=S/2}.                              (3.1)
```

The upper inclusion follows from Cauchy and arithmetic--geometric mean:

```text
|c|<=||X||||Y||<=(||X||^2+||Y||^2)/2=S/2.
```

For the reverse inclusion, if `S>0` and `|z|<=S/2`, put
`r=sqrt(S/2)` and in `C^2` take

```text
X=(r,0),
Y=(conjugate(z)/r, sqrt(r^2-|z|^2/r^2)).
```

Then both squared norms are `S/2` and `<Y,X>=z`.  When `S=0`,
both vectors vanish and the disk is `{0}`.  Hence exact knowledge of total
energy gives no positive lower bound, sign, phase, or strict improvement for
the selected cross coefficient.  A lower bound on total energy is weaker
still.

## 4. Exact phase-defect identity

Let

```text
Delta_G=||X||^2||Y||^2-|<Y,X>|^2>=0.
```

Direct expansion proves

```text
S^2-4|F_1|^2
 =(||X||^2-||Y||^2)^2+4 Delta_G.                 (4.1)
```

The two nonnegative terms distinguish norm imbalance from angular
decorrelation.  Equality `|F_1|=S/2` occurs exactly when the norms agree
and the Gram determinant vanishes.  Formula (4.1) is the reusable diagnostic
for the next arithmetic paper: any strict signed saving must create a
quantitative phase defect, not merely re-estimate the trivial-character
energy.

## 5. Typed consequence for TPC-241

TPC-241 proves a lower bound for

```text
E_top^psi
```

and for the finite-window norm of a standalone common-profile synthesis
`K_psi`.  Its proof explicitly does not project the four literal V59
packets.  In particular, the repository does not prove any of

```text
K_psi=T beta,
K_psi=T w,
E_top^psi=F_0,
TPC-241 floor = one common additive term in all four V59 energies.
```

Consequently the TPC-241 floor supplies no direct lower bound, upper bound,
nonvanishing, phase, or power-saving statement for `F_1`.  This is a
no-transfer theorem, not a physical annihilation theorem.  The actual
top-prime component may survive, attenuate, cancel, or vanish; all four
possibilities remain open until the phase-by-phase physical decomposition is
proved.

## 6. Route extraction

```text
STRONGEST_POSITIVE_RESULT = COMPLETE_C4_PHASE_SPECTRUM_PLUS_SHARP_FIXED_F0_CROSS_DISK_AND_EXACT_PHASE_DEFECT_IDENTITY
STRONGEST_OBSTRUCTION = EVEN_EXACT_PHASE_BLIND_TOTAL_ENERGY_DOES_NOT_DETERMINE_NONVANISHING_SIGN_PHASE_OR_SAVING_OF_THE_V59_CROSS_MODE
OPEN_THEOREM = SOURCE_BACKED_PHASE_BY_PHASE_TOP_PRIME_DECOMPOSITION_OF_THE_LITERAL_V59_REMAINDER
REUSABLE_STRUCTURE = C4_ENERGY_DFT_PLUS_NORM_IMBALANCE_AND_GRAM_DETERMINANT_DEFECT_LEDGER
ROUND2_CLUE = EXPRESS_THE_LITERAL_TOP_PRIME_CONTRIBUTION_PHASE_BY_PHASE_BEFORE_SQUARING_AND_COMPUTE_ITS_ACTUAL_K_EQUALS_ONE_COEFFICIENT
```

The maximum status is `PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER`.
Arithmetic `L2`, literal `C_h` cancellation, fixed-atom credit, strict
`1/400`, full Gate B, and the twin-prime endpoint remain open.
