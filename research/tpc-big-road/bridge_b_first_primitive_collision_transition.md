# TPC-226: first primitive-collision transition

更新时间：2026-08-24

状态：`PROVED_STRUCTURAL_L1 / FIRST_PRIMITIVE_COLLISION_TRANSITION`

## Exact finite object

For an integer `Q>=8`, let `q` range over the primes in `(Q,2Q)` and put

```text
x=Q^3, H=4Q^2, h_L=4LQ, C_h=1/h_L, L in {1,2,3,4}.
```

The literal primitive row support is

```text
S_(q,L) = {m q^(-1) mod h_L:
           0<|m|<=floor(Lq/Q), gcd(m,h_L)=1}.
```

The dilation `h_L=4LQ` is a finite `MODELING_CHOICE`.  It is not identified with
the physical V46 clock.

## Primitive-collision theorem

```text
TPC226_PRIMITIVE_SOURCE_ROW = PROVED_EXACT
TPC226_L_LE_3_DISJOINTNESS = PROVED_EXACT
TPC226_FIRST_PRIMITIVE_COLLISION_DILATION = 4
TPC226_L4_RESONANCE_CLASSIFICATION = PROVED_EXACT
TPC226_Q25_RESONANCE = PROVED_EXACT
```

A shared coordinate between distinct prime rows is equivalent to

```text
m_1 q_2 - m_2 q_1 = 0 mod 4LQ.
```

The cutoff gives `|m_i|<=2L-1<=7`.  Equal signs cannot wrap modulo `4LQ`, and
zero difference would force an active prime to divide a smaller nonzero multiplier.
Thus the signs are opposite.  Writing `a=|m_1|`, `b=|m_2|`, every collision obeys

```text
a q_2 + b q_1 = 4LQ,
2L < a+b < 4L,
a,b odd.
```

For `L=1` no odd pair remains.  For `L=2`, the only candidate `(3,3)` violates
its cutoff lower bound.  For `L=3`, multiplier `3` is nonprimitive modulo `12Q`,
and the remaining `(5,5)` candidate violates its cutoff lower bound.  Hence distinct
prime rows are pairwise disjoint for `L<=3`.

For `L=4`, size and cutoff constraints leave `(3,7)`, `(5,5)`, `(5,7)`, and
`(7,7)`.  The last two are too large.  The `(5,5)` equation would be
`5(q_1+q_2)=16Q`, whereas primitive use of multiplier `5` requires `5` not to divide
`Q`.  Therefore every collision is, up to exchange and simultaneous sign change,

```text
7p + 3r = 16Q,
m_p = 3,
m_r = -7.
```

Conversely, every pair satisfying this equation together with the literal shell,
cutoff, and primitive conditions produces exactly two sign-symmetric shared
coordinates.

At `Q=25`, `(p,r)=(37,47)` is the first exact boundary-census witness:

```text
7*37 + 3*47 = 400,
37^(-1) = 173 mod 400,
47^(-1) = 383 mod 400,
shared residues = {119,281} mod 400.
```

## Signed resonance theorem

For a resonance `(p,r)`, put

```text
u_p=3Q/(4p), v_r=7Q/(4r).
```

Its exact contribution to `E_AP-E_diag` is

```text
2/h^2 Re sum_j [psi_j(u_p) conjugate(psi_j(-v_r))
                +psi_j(-u_p) conjugate(psi_j(v_r))].
```

Consequently:

- aligned profiles make every resonance positive;
- the inherited affine profiles `psi_j(t)=1+s_j t`,
  `s=(0,1,-1,2)/10`, make every resonance positive;
- smooth balanced odd-sign profiles `psi_j=alpha_j chi`,
  `alpha=(1,-1,1,-1)`, make every resonance negative and give
  `E_pol=E_all=0`.

On the full `Q=25` shell the exact ratios are

```text
aligned:       E_AP/E_diag = 15/13
affine:        E_AP/E_diag = 14610396266802411880605/12679409642889136447511
balanced_sign: E_AP/E_diag = 11/13
balanced_sign: E_pol = E_all = 0.
```

Thus nonempty overlap supplies an interface for cancellation but does not determine
the sign.  A uniform profile-independent AP saving is false on this finite clock.

## Exact certificate

The exact-rational certificate checks every `Q=8,...,512`:

```text
classification scales = 505
L=1 collision scales = 0
L=2 collision scales = 0
L=3 collision scales = 0
L=4 collision-bearing scales = 182
L=4 total resonances = 235
first collision Q = 25
maximum resonances at one scale = 4 (Q=502)
classification SHA-256 = fe678364061af5b70411105e05344e51fbc8bd0c2418172d67cedaa068c58d8d
```

It also records 30 exact profile evaluations on ten collision-bearing scales.  The
independent checker reproduces the classification and all profile records without
importing the producer.  The adversarial checker confirms that dropping primitivity
creates a fake `L=3`, `Q=8` collision through the nonprimitive multiplier `m=4`.

## Audit scope and firewall

```text
TPC226_ROUTE_ADVANCE = YES
TPC226_DILATED_CLOCK_FAMILY = MODELING_CHOICE
TPC226_ALIGNED_AP_SAVING = REFUTED_SCOPED
TPC226_AFFINE_AP_SAVING = REFUTED_SCOPED
TPC226_BALANCED_SIGN_AP_SAVING = PROVED_EXACT_FINITE_PROFILE
TPC226_BALANCED_SIGN_POLARIZED_CANCELLATION = PROVED_EXACT_FINITE_PROFILE
TPC226_UNIFORM_PROFILE_INDEPENDENT_SAVING = REFUTED_SCOPED
TPC226_V46_PROFILE_TRANSFER = OPEN
TPC226_ARITHMETIC_CANCELLATION = NONE
TPC226_ARITHMETIC_ADVANCE = NO
TPC226_FIXED_ATOM_CREDIT = 0
TPC226_L2 = NONE
TPC226_FULL_GATE_B = OPEN
TPC226_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC226_TPC_TRIGGER = true
TPC226_NUMBERED_RELEASE = YES
TPC226_STATUS = PROVED_STRUCTURAL_L1
TPC226_ROUND2_CLUE = SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

Strongest positive result: the first legitimate primitive overlap is classified
exactly, and a balanced signed profile converts every such resonance into strict
finite AP saving while annihilating the polarized and total packet sums.

Strongest obstruction: the same exact collision graph amplifies aligned and inherited
affine profiles, so geometry alone cannot prove the desired marginal saving.

Open theorem: transfer the literal V46 packet source to a nontrivial-cutoff shared
clock and determine the signed `3--7` resonance correlation with a quantitative
arithmetic saving.

Reusable structure: primitive multiplier sieve, finite collision equation, resonance
graph, and signed cross-term formula.

`ROUND2_CLUE`:

```text
SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

This proof record is structural evidence only.  It proves no prime-distribution
estimate, fixed-atom theorem, strict `1/400` payment, or twin-prime conclusion.
