# Bridge B: packet/profile axis separation

## 1. Source lock

The V59 source compiler is

```text
a_n^(j)=beta(n)+i^j w(n),
C_x=1/4 sum_(j=0)^3 i^j V_Q,H^circ(a^(j)),
```

and every quadratic functional uses the same `psi_+(v)`. TPC-218's independent
bounded `psi_j` are a structural row lift, not a source identification.

## 2. Exact operator theorem

Let `T` be the physical common transform and let `T_j` be four proposed packet
transforms. For complex Hilbert spaces,

```text
1/4 sum_j i^j ||T_j(x+i^j y)||^2 = <Tx,Ty> for all x,y
```

if and only if

```text
T_j^* T_j = T^* T for j=0,1,2,3.
```

Indeed, for `Q_j=T_j^*T_j` and

```text
A_k=1/4 sum_j i^(kj) Q_j,
```

the left side is

```text
<A_1 x,x> + <A_1 y,y> + <A_0 x,y> + <A_2 y,x>.
```

Equality for all `x,y` forces `A_1=A_2=A_3=0` and `A_0=T^*T`; four-point Fourier
inversion gives the criterion. The converse is ordinary four-phase polarization.

## 3. First-collision witness

At the TPC-226 witness `Q=25`, `h=400`, `(p,r)=(37,47)`, restrict to one shared
coordinate and the two colliding source atoms. The aligned and row-odd maps are

```text
T     = (1, 1)/400,
T_odd = (1,-1)/400.
```

Therefore

```text
T^*T     = [[1, 1],[ 1,1]]/160000,
T_odd^*T_odd = [[1,-1],[-1,1]]/160000,
```

and the off-diagonal mismatch is exactly `-1/80000`. A global packet sign is
Gram-invisible, but this row-dependent sign changes the collision Gram and cannot be
renamed as the V59 source phase.

## 4. Claim firewall

```text
TPC227_ROUTE_ADVANCE = YES
TPC227_V59_PACKET_AXIS = SOURCE_LOCKED
TPC227_V59_PROFILE_AXIS = SOURCE_LOCKED_COMMON
TPC227_FOUR_GRAM_CRITERION = PROVED_EXACT
TPC227_GLOBAL_PACKET_PHASE_VISIBILITY = GRAM_INVISIBLE
TPC227_Q25_ROW_SIGN_GRAM_MISMATCH = PROVED_EXACT
TPC227_TPC226_AUTOMATIC_SOURCE_TRANSFER = REFUTED_SCOPED
TPC227_SOURCE_NATIVE_COMMON_PROFILE_COMPILER = OPEN
TPC227_ARITHMETIC_CANCELLATION = NONE
TPC227_ARITHMETIC_ADVANCE = NO
TPC227_FIXED_ATOM_CREDIT = 0
TPC227_L2 = NONE
TPC227_FULL_GATE_B = OPEN
TPC227_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC227_STATUS = PROVED_STRUCTURAL_L1
TPC227_ROUND2_CLUE = KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON
```

## 5. Route decision

Strongest positive result: exact necessary-and-sufficient target-Gram criterion with a
source-locked interpretation.

Strongest obstruction: the finite row-dependent sign changes cross-row Gram data and
therefore does not automatically transfer to V59.

Open theorem: carry the literal coefficient packets through a common-profile
prime/AP collision compiler and determine the signed `3--7` source correlation.

Reusable structure: four-point Gram DFT, target compatibility test, and exact collision
block.

This is a structural L1 advance only. Arithmetic cancellation, fixed-atom credit,
Route-B L2 and strict `1/400` payment remain absent.
