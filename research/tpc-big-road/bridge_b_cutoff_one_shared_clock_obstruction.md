# TPC-225: cutoff-one shared-clock obstruction

更新时间：2026-08-22

状态：`PROVED_STRUCTURAL_L1 / CUTOFF_ONE_SHARED_CLOCK_OBSTRUCTION`

## Exact finite object

For an integer `Q>=3`, let `q` range over the primes in `(Q,2Q]` and set

```text
x=Q^3, H=4Q^2, h=4Q, C_h=1/h.
```

For four packet profiles define the literal row

```text
W_(q,j)(a) = C_h sum_(0<|m|<=floor(hq/H))
             psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h).
```

## Structural theorem

```text
TPC225_CUTOFF_ONE = PROVED_EXACT
TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT
TPC225_AP_EQUALS_DIAGONAL = PROVED_EXACT
TPC225_ALL_EQUALS_POLARIZED = PROVED_EXACT
TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED
```

Indeed `floor(hq/H)=floor(q/Q)=1`, so the row support is
`{q^(-1),-q^(-1)}` modulo `4Q`. If two distinct active primes had intersecting
supports, then `q_2` would be congruent to `q_1` or `-q_1` modulo `4Q`. The
first case forces equality; the second forces `q_1+q_2=4Q`, which is
impossible because both primes are at most `2Q` and `2Q` is not prime.

For

```text
E_diag = sum_(q,j) ||W_(q,j)||^2
E_AP   = sum_j ||sum_q W_(q,j)||^2
E_pol  = sum_q ||sum_j W_(q,j)||^2
E_all  = ||sum_(q,j) W_(q,j)||^2,
```

Pythagoras across the disjoint prime supports gives

```text
E_AP = E_diag,
E_all = E_pol.
```

Therefore `E_AP <= (1-delta) E_diag` is false for every `delta>0` whenever
the finite row family is nonzero.

## Audit scope and firewall

The exact-rational certificate contains nine affine-profile source scales,
seven aligned-profile scales, seven balanced-profile scales, and a complete
`Q=3..99` support regression. It does not use TPC-224's collision-stress
clock and does not identify this named clock with V46.

```text
TPC225_POLARIZED_SAVING = PROFILE_DEPENDENT_OPEN
TPC225_V46_CLOCK_TRANSFER = OPEN
TPC225_ARITHMETIC_ADVANCE = NO
TPC225_FIXED_ATOM_CREDIT = 0
TPC225_L2 = NONE
TPC225_FULL_GATE_B = OPEN
TPC225_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC225_TPC_TRIGGER = true
TPC225_NUMBERED_RELEASE = YES
TPC225_STATUS = PROVED_STRUCTURAL_L1
TPC225_ROUND2_CLUE = MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

The proof record is structural evidence only. It does not prove a prime-distribution
estimate, a fixed-atom theorem, or the twin-prime conjecture.
