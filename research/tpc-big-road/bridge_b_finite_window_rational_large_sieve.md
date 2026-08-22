# Bridge B / Gate B TPC-217: finite-window attachment by reduced rational-frequency large sieve

Date: 2026-08-21

Status: `PROVED_STRUCTURAL_L1 / FINITE_WINDOW_ATTACHMENT`.

TPC-216 bounded the complete-period direct-sum row energy but deliberately left
the physical interval open.  TPC-217 attaches that object to the literal
interval by regrouping the common-source kernel into distinct reduced rational
frequencies and applying the standard additive large sieve at Farey spacing.

## Registry and claim firewall

```text
TPC217_MAXIMUM_CLAIM = SOURCE_LOCKED_COMMON_SOURCE_FINITE_WINDOW_ATTACHMENT_BY_REDUCED_RATIONAL_LARGE_SIEVE
TPC217_ROUTE_ADVANCE = YES
TPC217_STRUCTURAL_THRESHOLD_A = PASS
TPC217_REDUCED_FREQUENCY_REGROUPING = PROVED_EXACT
TPC217_FAREY_SPACING = PROVED_EXACT
TPC217_ADDITIVE_LARGE_SIEVE = PROVED_STANDARD
TPC217_FINITE_WINDOW_ATTACHMENT = PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED
TPC217_UNNORMALIZED_WINDOW_EXPONENT = PROVED_43_OVER_32
TPC217_WINDOW_LOSS = PROVED_1_PLUS_U2_OVER_N
TPC217_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_LARGE_SIEVE
TPC217_ALIGNED_ONE_POINT_ORTHOGONALITY = REFUTED_SCOPED
TPC217_PRIME_SHELL_REASSEMBLY = OPEN
TPC217_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC217_ARITHMETIC_CANCELLATION = NONE
TPC217_ARITHMETIC_ADVANCE = NO
TPC217_FIXED_ATOM_CREDIT = 0
TPC217_L2 = NONE
TPC217_FULL_GATE_B = OPEN
TPC217_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC217_TPC_TRIGGER = true
```

The theorem is a finite-window structural attachment for the common-source
cluster kernel.  It is not a prime-shell cancellation theorem and does not
close the arithmetic Gate-B residual.

## 1. Source lock and physical kernel

Keep the TPC-216 scales

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
Q_x={q prime:Q<q<=2Q},
D_x={d:Y0<d<=U:mu(d)^2=1}, c_d=mu(d)log(d)/d.
```

For bounded `psi`, retain the literal integer-cutoff emitter

```text
B_d(r)=sum_(q in Q_x) sum_(0<|m|<=floor(dq/H))
        psi(Hm/(dq)) 1_(m q^(-1)=r mod d).
```

Let `I_x=(x/2,x] intersect Z`, `N=|I_x|`, and define

```text
K(n)=sum_(d in D_x)c_d sum_(r mod d)B_d(r)e(nr/d).
```

This is the common-source cluster kernel whose complete-period energy was
factored in TPC-214 and majorized in TPC-215.

## 2. Exact reduced-frequency regrouping

For `r mod d`, write `g=(r,d)`, `h=d/g`, and `a=r/g`; for `r=0`, use
`h=1,a=0`.  Then `a/h` is the reduced rational frequency represented by
`r/d`.  If `h|d` and `d=kh`, the literal congruence in `B_d` gives

```text
m q^(-1)=k a mod k h  =>  m=k n,
```

and the integer cutoff and profile argument reduce exactly to those of `B_h`:

```text
|n|<=floor(hq/H),  Hm/(dq)=Hn/(hq),
B_d(k a)=B_h(a).
```

Thus, with

```text
C_h=sum_(d in D_x,h|d)c_d,
```

the finite divisor sum is exactly

```text
K(n)=sum_(h<=U) sum_(a mod h,(a,h)=1)
        C_h B_h(a)e(na/h).
```

The `h=1` additive zero row vanishes because `q_max<H` and the nonzero integer
cutoff is then empty.  This is only an additive zero-axis statement.

## 3. Farey spacing

Distinct reduced fractions with denominators at most `U` have circular spacing

```text
delta >= 1/U^2.
```

Indeed, the difference of two distinct fractions, or its complement modulo one,
is a nonzero rational with denominator dividing the product of the two
denominators.  The denominator product is at most `U^2`.

## 4. Finite-window large-sieve attachment

Use the standard additive large-sieve inequality for a consecutive interval of
`N` integers:

```text
sum_(n in I)|sum_j z_j e(n alpha_j)|^2
 <= (N-1+delta^(-1)) sum_j|z_j|^2,
```

when the frequencies are separated modulo one by at least `delta`.  Applying
this with `delta=U^(-2)` and `z_(h,a)=C_hB_h(a)` gives

```text
sum_(n in I_x)|K(n)|^2
 <= (N+U^2) S_cluster,
S_cluster=sum_(h,a)|C_hB_h(a)|^2.
```

This is the missing finite-window off-frequency control.  It does not replace
the prime rows by an orthogonal family; all shell rows remain inside `B_h`.

## 5. Coefficient energy and exponent ledger

TPC-215 gives the exact coefficient-to-direct majorant

```text
S_cluster <= A_x E_direct/L,
A_x=O((log x)^2).
```

TPC-216 gives

```text
E_direct/L <<_psi (Q^3/H)(log U)^3
             = x^(11/32)(log x)^3.
```

Therefore

```text
sum_(n in I_x)|K(n)|^2
 <<_psi (N+U^2)x^(11/32)(log x)^5.
```

The source exponents give

```text
U^2/x=x^(-67/200),  N asymp x,
```

so the normalized form is

```text
N^(-1) sum_(n in I_x)|K(n)|^2
 <<_psi x^(11/32)(log x)^5,
```

and the unnormalized window exponent is `43/32+o(1)`.

No PNT, Möbius cancellation, prime-shell cancellation, or four-packet
arithmetic cancellation is used.

## 6. Finite crowding obstruction

The finite rational fixture

```text
d=5, H=500, q={101,131,151,181}, psi(t)=(1+t^2)^(-2)
```

has cutoff one and every fixed-prime row supported on `{1,4}` modulo five.  A
one-point window therefore has coherent energy exactly twice its diagonal
row-energy sum.  This refutes only a scoped shortcut: a short physical window
cannot be treated as a diagonal orthogonal sum.  It does not contradict the
large-sieve bound for a long interval.

## 7. Route-B evaluation

```text
STRONGEST_POSITIVE_RESULT = FINITE_WINDOW_COMMON_SOURCE_KERNEL_BOUND_AT_NORMALIZED_X_11_OVER_32_LOG_FIVE
STRONGEST_OBSTRUCTION = ONE_POINT_ALIGNED_SHELL_HAS_EXACT_COHERENT_RATIO_TWO
OPEN_THEOREM = PRIME_SHELL_AND_FOUR_PACKET_REASSEMBLY_AFTER_FINITE_WINDOW_ATTACHMENT
REUSABLE_STRUCTURE = EXACT_REDUCED_REGROUPING_PLUS_FAREY_SPACING_PLUS_LARGE_SIEVE_PLUS_TPC216_ENVELOPE
ROUND2_CLUE = PRESERVE_THE_FINITE_WINDOW_LARGE_SIEVE_ATTACHMENT_WHILE_REINTRODUCING_LITERAL_PRIME_SHELL_AND_FOUR_PACKET_REASSEMBLY
```

Route A is not applicable.  Route-B structural threshold A passes.  Arithmetic
advance, fixed-atom credit, `L2`, strict `1/400`, full Gate B, and the
twin-prime endpoint remain open.
