# Bridge A / Gate B TPC-211: product-coupled Euler profiles and the boundary handoff

Date: 2026-08-18

Status: `PROVED_STRUCTURAL_L1 / STOP_SCOPED_PHYSICAL_COUPLING`.

TPC-211 closes the finite structural question left by TPC-210.  The literal
V46 local factors are genuinely coupled across squarefree divisors, but the
coupling does not reduce the number of divisor degrees of freedom.

For active odd primes \(p>z\), write

\[
 P_S(a)=\prod_{p\in S}F_p(a),\qquad
 B_S(a)=\prod_{p\in S}G_{p,z}(a),\qquad
 \Delta_S=P_S-B_S.
\]

After lifting all rows to the common CRT space modulo \(M=\prod p\), the
following facts are exact:

1. The defects satisfy the product cocycle
   \(\Delta_{S\cup T}=P_S\Delta_T+B_T\Delta_S\) for disjoint \(S,T\),
   and every defect has zero value at the zero residue and zero mean.
2. The nonempty family \(\{\Delta_S\}\) has rank \(2^s-1\).  Fourier
   support triangularity gives a nonzero diagonal coefficient for every
   divisor support, so the product coupling is full divisor rank.
3. On a complete packet, the exact \(\mu(d)\log d\) sum is the marked-prime
   Euler derivative
   \[
   \sum_{S\ne\varnothing}\mu(d_S)\log(d_S)\Delta_S
   =-\sum_p\log(p)\left(P_p\prod_{r\ne p}(1-P_r)
       -B_p\prod_{r\ne p}(1-B_r)\right).
   \]
4. For at least two active primes the product-frozen common endpoint cancels
   on the complete packet.
5. Positive-definite Gram duality constructs one finite shared endpoint with
   \(\langle w,\Delta_S\rangle=\mu(d_S)\) for every nonempty \(S\).

The fifth item is a scoped obstruction: product coupling, finite rank, and a
shared endpoint do not by themselves imply a cross-divisor saving.  It is not
an arithmetic counterexample for the literal sequence
\(\Lambda(u+2)-b_x^{(z)}(u)\), because the actual transition uses the band

\[
 \mathcal A_{Y,U}(t)=\{d:d\mid t,\ Y_0<d\le U,\ \mu^2(d)=1\}
\]

and the divisor-dependent reciprocal emitter \(A_d(r)\).  This band is not
generally a complete Boolean packet.  The next structural object is therefore
the boundary-weighted packet after the emitter has been retained.

## Claim firewall

```text
TPC211_MAXIMUM_CLAIM = EXACT_LITERAL_PRODUCT_COUPLED_EULER_PACKET_FULL_RANK_LOG_MOBIUS_DERIVATIVE_AND_SHARED_ENDPOINT_OBSTRUCTION
TPC211_ROUTE_ADVANCE = YES
TPC211_STRUCTURAL_THRESHOLD_A = PASS
TPC211_PRODUCT_COUPLING_COCYCLE = PROVED_EXACT
TPC211_LITERAL_PRODUCT_PROFILE_FULL_RANK = PROVED_EXACT
TPC211_LOG_MOBIUS_PACKET_DERIVATIVE = PROVED_EXACT
TPC211_COMPLETE_PACKET_ENDPOINT_CANCELLATION = PROVED_EXACT
TPC211_SHARED_ENDPOINT_ALIGNMENT = PROVED_STRUCTURAL_FINITE
TPC211_PRODUCT_COUPLING_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC211_TRANSITION_BOUNDARY_CONTROL = OPEN
TPC211_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC211_ARITHMETIC_ADVANCE = NO
TPC211_FIXED_ATOM_CREDIT = 0
TPC211_L2 = NONE
TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC211_TPC_TRIGGER = true
```

## Finite certificate

The numbered paper and exact certificate are in
`papers/tpc-211-product-coupled-euler-gram/`.  The producer and independent
checker use exact rational arithmetic for prime sets
\((5,7)\), \((5,7,11)\), and \((5,7,11,13)\), with cutoff \(z=3\).  They
cover 25 profile rows, 77,875 CRT coordinates, and 9 marked-prime derivative
rows.  All three cases have full divisor rank, nonzero Gram determinant,
complete-packet endpoint cancellation, and the exact alignment ratios
\(3,7,15\).

These are finite structural certificates.  They do not estimate the prime
shell, the reciprocal occupancy, the transition boundary, or Gate B.

## Route position and next theorem

```text
V64 / TPC-211 / Bridge A--Gate B
literal product-coupled physical profile zone
        |
        +-- complete packet: marked-prime derivative      PROVED
        +-- product rank / shared endpoint obstruction     PROVED, scoped
        +-- truncated band boundary after A_d(r)           OPEN
        +-- physical cross-divisor Gram saving             OPEN
        +-- prime-only signed reassembly                   OPEN
        +-- strict 1/400 and twin-prime endpoint           UNPAID
```

The next smallest research question is not another generic profile theorem:
it is an exact boundary operator for the cut divisor band, with the
reciprocal emitter kept before any outer absolute value.  A positive result
would have to control both endpoint leakage and the emitter-weighted boundary
profiles.  A negative result would identify a literal finite obstruction to
that shortcut.
