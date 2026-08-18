# Bridge A / Gate B TPC-212: truncated divisor bands and reciprocal-emitter boundary

Date: 2026-08-18

Status: `PROVED_STRUCTURAL_L1 / STOP_SCOPED_BOUNDARY_EMITTER`.

TPC-211 proved the complete-packet logarithmic Mobius derivative for the
literal product-coupled Euler profiles.  TPC-212 isolates the two pieces that
the complete packet does not control: the divisor band `Y0<d<=U` and the
divisor-dependent reciprocal emitter `A_d(r)`.

## Exact boundary theorem

Let `P` be a finite active-prime set, let `S` range over nonempty subsets, and
write `d_S=product_(p in S) p` and `epsilon_S=(-1)^|S|`.  For a selected family
`A`, define

```text
eta_p(A) = sum_(S in A, p in S) epsilon_S
L(A)     = sum_(S in A) epsilon_S log(d_S)
         = sum_p eta_p(A) log(p)
```

The complete Boolean packet has `eta_p=0` for every `p` when at least two
primes are active.  For a proper selected family the endpoint contribution is
exactly `L(A) w`.  If `M` is the missing family and `R_S=w-Delta_S`, then

```text
sum_(S in A) epsilon_S log(d_S) R_S
 = sum_(S nonempty) epsilon_S log(d_S) R_S
   - sum_(S in M) epsilon_S log(d_S) R_S.
```

For the TPC-211 product profiles, the first term has the marked-prime
derivative form; the second term is a genuine endpoint-plus-profile boundary.
The smallest physical cut `t=35`, `Y0=5`, `U=35` selects `{7,35}` and has
`eta=(1,0)`, hence logarithmic endpoint leakage `log(5)`.

## Exact reciprocal-emitter theorem

For finite `I_d={(q,m): q in Q, 0<|m|<=floor(dq/H)}`, define

```text
(E_d a)(r) = sum_(q,m in I_d) a(q,m) 1_(r = m q^(-1) mod d).
```

The exact collision identity is

```text
||E_d a||_2^2
 = sum_(q1,m1,q2,m2) a(q1,m1) conjugate(a(q2,m2))
   1_(d divides m1*q2 - m2*q1).
```

In the natural direct sum of residue spaces over a divisor family, different
divisor blocks are orthogonal.  The emitter Gram is therefore block diagonal;
if each occupancy row is nonzero its rank is the number of divisor blocks.
The normalized residual `r_d=sign(d) v_d/||v_d||^2` aligns every block, so the
unit-weight coherent-to-diagonal ratio equals the block count.

This is a scoped interface obstruction.  It does not claim that the literal
physical residuals can choose these residuals independently.  It proves that
the divisor cut and reciprocal congruence alone do not supply the missing
cross-divisor coupling.

## Claim firewall

```text
TPC212_MAXIMUM_CLAIM = EXACT_TRUNCATED_BOOLEAN_BOUNDARY_AND_RECIPROCAL_EMITTER_GRAM_OBSTRUCTION
TPC212_ROUTE_ADVANCE = YES
TPC212_STRUCTURAL_THRESHOLD_A = PASS
TPC212_CUT_ENDPOINT_LEAKAGE = PROVED_EXACT
TPC212_BOUNDARY_DECOMPOSITION = PROVED_EXACT
TPC212_RECIPROCAL_COLLISION = PROVED_EXACT_FINITE
TPC212_EMITTER_GRAM = PROVED_EXACT_BLOCK_DIAGONAL
TPC212_EMITTER_ONLY_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC212_LITERAL_PHYSICAL_BOUNDARY_BOUND = OPEN
TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC212_ARITHMETIC_ADVANCE = NO
TPC212_FIXED_ATOM_CREDIT = 0
TPC212_L2 = NONE
TPC212_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC212_TPC_TRIGGER = true
```

## Finite certificate and route position

The numbered paper and exact certificate are in
`papers/tpc-212-truncated-boundary-emitter/`.  The producer and independent
checker cover four boundary cuts, 5,810 profile coordinates, three unit-weight
emitter fixtures, and nine divisor rows.  The emitter fixture sets `psi=1` on
finite `(q,m)` sets; this is a modeling choice, not the physical smooth
emitter.

```text
V65 / TPC-212 / Bridge A--Gate B
truncated divisor-band boundary and reciprocal-emitter zone
        |
        +-- signed Boolean endpoint incidence             PROVED
        +-- complete-minus-missing boundary identity      PROVED
        +-- reciprocal collision Gram                     PROVED finite
        +-- emitter-only universal saving                 REFUTED scoped
        +-- literal physical boundary/Gram bound          OPEN
        +-- prime-only signed reassembly                  OPEN
        +-- strict 1/400 and twin-prime endpoint          UNPAID
```

The next theorem must construct a nontrivial coupling map from the literal V46
profile at divisor `d` into the emitter blocks before any direct-sum Cauchy
estimate or outer absolute value.  Until then the physical Gate-B estimate is
still open.
