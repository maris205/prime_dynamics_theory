# Bridge B / Gate B TPC-216: direct-sum row-energy envelope and the Cauchy bottleneck

Date: 2026-08-21

Status: `PROVED_STRUCTURAL_L1 / DIRECT_SUM_ROW_ENERGY_ENVELOPE`.

TPC-215 reduced the complete-period cluster Gram to the source-locked divisor
direct-sum row energy up to `O((log x)^2)`.  TPC-216 bounds that direct-sum
quantity at the deterministic envelope scale before finite-window cross
frequencies are reintroduced.

## Registry and claim firewall

```text
TPC216_MAXIMUM_CLAIM = SOURCE_LOCKED_COMPLETE_PERIOD_DIRECT_SUM_ROW_ENERGY_ENVELOPE_WITH_FIXED_Q_NO_COLLISION_AND_ALIGNED_SHELL_OBSTRUCTION
TPC216_ROUTE_ADVANCE = YES
TPC216_STRUCTURAL_THRESHOLD_A = PASS
TPC216_FIXED_Q_NO_COLLISION = PROVED_EXACT
TPC216_FIXED_Q_ROW_ENERGY = PROVED_EXACT
TPC216_SHELL_CAUCHY_ENVELOPE = PROVED_EXACT
TPC216_PRIME_SHELL_CARDINALITY = PROVED_P_LE_2Q
TPC216_NORMALIZED_EXPONENT = PROVED_11_OVER_32
TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE = PROVED_X_11_OVER_32_LOG_CUBED
TPC216_ARITHMETIC_CANCELLATION = NONE
TPC216_ALIGNED_SUPPORT_ADVERSARY = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC216_FREE_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC216_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC216_PRIME_SHELL_REASSEMBLY = OPEN
TPC216_FULL_GATE_B = OPEN
TPC216_ARITHMETIC_ADVANCE = NO
TPC216_FIXED_ATOM_CREDIT = 0
TPC216_L2 = NONE
TPC216_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC216_TPC_TRIGGER = true
```

The theorem is a complete-period normalized row-energy envelope.  It is not a
finite-window Gram estimate, does not use Mobius cancellation, and does not
close any arithmetic Gate-B condition.

## 1. Source lock

Keep the literal V46 scales

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
Q_x={prime q: Q<q<=2Q}, P=#Q_x,
D_x={d: Y0<d<=U, mu(d)^2=1}, c_d=mu(d)log(d)/d.
```

The coefficient-free row is

```text
B_d(r)=sum_(q in Q_x) sum_(0<|m|<=floor(dq/H))
        psi(Hm/(dq)) 1_(m q^(-1)=r mod d).
```

The source exponents imply

```text
H/(4Q)=x^(31/96)/4 -> infinity,
U/Q=x^(-1/1200) -> 0.
```

Thus for sufficiently large `x`, `4Q<H` and `U<Q`.  The stronger `4Q<H`
condition, rather than only `2Q<H`, is what is needed for no collision when the
prime shell reaches `2Q`.

## 2. Fixed-q row energy

### Theorem: fixed-q no-collision

Fix `d in D_x` and `q in Q_x`.  Put

```text
n_(d,q)=floor(dq/H)
B_(d,q)(r)=sum_(0<|m|<=n_(d,q))
            psi(Hm/(dq)) 1_(m q^(-1)=r mod d).
```

Then the admissible integers `m` have distinct residues modulo `d` after
multiplication by `q^(-1)`, and

```text
sum_(r mod d)|B_(d,q)(r)|^2
  = sum_(0<|m|<=n_(d,q)) |psi(Hm/(dq))|^2
  <= 2 ||psi||_infty^2 d q/H.
```

Proof: if two distinct admissible integers collide, then `d` divides their
difference.  But

```text
0 < |m1-m2| <= 2 floor(dq/H) <= 2dq/H < d,
```

because `q<=2Q` and `4Q<H`.  This is impossible.  The displayed norm identity
then follows by removing all cross terms between distinct residue supports;
the final inequality counts at most `2 floor(dq/H)` integers.  `QED`.

## 3. Shell Cauchy envelope

### Theorem: direct-sum row-energy envelope

Let `M_psi=||psi||_infty`.  Since `B_d=sum_q B_(d,q)`, Cauchy in the prime
shell and the preceding theorem give

```text
||B_d||_2^2
 <= P sum_(q in Q_x)||B_(d,q)||_2^2
 <= 4 M_psi^2 P^2 d Q/H.
```

The interval `(Q,2Q]` contains at most `2Q` integers for `Q>=1`, so `P<=2Q`.
Therefore

```text
||B_d||_2^2 <= 16 M_psi^2 d Q^3/H.
```

Define, as in TPC-215,

```text
E_direct=L sum_(d in D_x)|c_d|^2 ||B_d||_2^2.
```

Then

```text
L^(-1) E_direct
 <= 16 M_psi^2 (Q^3/H)
    sum_(Y0<d<=U) mu(d)^2 (log d)^2/d
 <= C_psi (Q^3/H)(log U)^3.
```

The last estimate follows by comparison with the integral of
`(log t)^2/t`.  Since

```text
Q^3/H=x^(1-21/32)=x^(11/32),
```

the normalized direct-sum row energy is

```text
L^(-1) E_direct <= x^(11/32+o(1)).
```

No prime number theorem and no Mobius cancellation are used.

## 4. Proposition: aligned-shell obstruction

The shell Cauchy factor cannot be replaced by orthogonality as a structural
identity.  The exact rational fixture is

```text
d=5, Q-scale=100, H=500,
q={101,131,151,181}, psi(t)=(1+t^2)^(-2).
```

All four primes are `1 mod 5`, and
`floor(5q/500)=1`.  Every fixed-q row has support exactly `{1,4}` modulo 5,
so the combined row is supported on the same two residues.  The exact
certificate records

```text
combined norm / sum individual norms
= 260748658086322583836897419347021086290217246085930053167204419990209924
  / 70364475771299731347712229517668330151453704760854551233185864997552481
> 1.
```

This is `NUMERICALLY_CERTIFIED` finite structural evidence and a scoped
obstruction to free shell orthogonality.  It is not an asymptotic statement
about the V46 prime shell.

## 5. Route-B evaluation

The strongest positive result is the complete-period envelope
`L^(-1)E_direct <= C_psi*x^(11/32)(log x)^3`.  The strongest obstruction is
the exact aligned-support fixture.  The next theorem must attach this envelope
to the literal finite physical window without discarding shell alignment,
Mobius signs, or the four-packet reassembly.

```text
STRONGEST_POSITIVE_RESULT = SOURCE_LOCKED_COMPLETE_PERIOD_DIRECT_SUM_ROW_ENERGY_IS_AT_MOST_X_11_OVER_32_LOG_CUBED
STRONGEST_OBSTRUCTION = FINITE_PRIME_SHELL_ROWS_CAN_HAVE_EXACTLY_ALIGNED_RESIDUE_SUPPORT
OPEN_THEOREM = ATTACH_COMPLETE_PERIOD_DIRECT_SUM_ENVELOPE_TO_LITERAL_FINITE_WINDOW
REUSABLE_STRUCTURE = FIXED_Q_INJECTIVE_ATOMS_PLUS_SHELL_CAUCHY_PLUS_MOBIUS_LOG_DIVISOR_SUM
ROUND2_CLUE = ATTACH_THE_COMPLETE_PERIOD_DIRECT_SUM_ENVELOPE_TO_THE_LITERAL_FINITE_WINDOW_WITHOUT_FREE_SHELL_ORTHOGONALITY
```

Route A is not applicable.  Route B structural threshold A passes; arithmetic
advance, `L2`, fixed-atom credit, strict `1/400`, full Gate B, and the
twin-prime endpoint remain open.
