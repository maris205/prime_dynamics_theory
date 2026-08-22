# TPC-223: conditional signed-reassembly compiler

更新时间：2026-08-22

状态：`CONDITIONAL_THEOREM / FULL_GATE_B_OPEN`

## 1. Interface inherited from the previous papers

TPC-220 identifies the q-row transverse object with a literal weighted prime-AP and
multiplicative collision packet.  TPC-222 proves that the four-packet signed quantity
cannot be recovered from diagonal or trace data alone, and that phase-labelled energies
are the exact algebraic data needed for a cross-term.

TPC-223 does not claim either missing estimate.  It asks a narrower question: if the
literal reassembly can be split into the two named channels, what exact exponent ledger
would be sufficient to pay the strict endpoint margin?

## 2. Conditional input

Fix a baseline exponent `E0` and nonnegative rational parameters
`delta_AP`, `kappa_pol`, and `lambda_struct`.  The conditional interface consists of

```text
A_x << x^(E0-delta_AP+o(1)),
P_x << x^(E0-kappa_pol+o(1)),
S_x << x^lambda_struct (A_x+P_x).
```

Here `A_x` is the literal prime-AP/collision channel from TPC-220, `P_x` is the
phase-labelled polarized four-packet cross-correlation channel from TPC-222, and
`lambda_struct` is the sum of already-paid finite-window, lift, normalization, and
other structural losses.  All three lines are declared conditional inputs.  In
particular, no source in this repository currently proves them simultaneously on the
named fixed prime shell.

## 3. Compiler theorem

**Theorem (conditional two-channel compiler).** Under the displayed interface,

```text
S_x << x^(E0-sigma+o(1)),
sigma = min(delta_AP,kappa_pol)-lambda_struct.
```

Consequently, if

```text
min(delta_AP,kappa_pol)-lambda_struct > 1/400,
```

then the strict `1/400` endpoint threshold is paid with a positive margin.

**Proof.** The two channel terms have exponents `E0-delta_AP` and
`E0-kappa_pol`; their sum has the larger of those two exponents, which is
`E0-min(delta_AP,kappa_pol)`, up to the common `x^(o(1))` factor.  The structural
factor adds `lambda_struct`.  Rearranging gives the formula for `sigma`.  Strict
inequality over `1/400` leaves a positive residual margin.  □

The result is a conditional theorem about the compiler only.  It does not promote
the input lines to `PROVED`, and it gives no arithmetic `L2` credit by itself.

## 4. Exact ledger and boundary certificate

The canonical strict fixture uses

```text
E0=5/3, delta_AP=1/100, kappa_pol=1/80, lambda_struct=1/1200.
```

Its effective saving is `11/1200`, its strict margin over `1/400` is `1/150`, and
the compiled exponent is `663/400`, below the target exponent `1997/1200`.
The certificate also contains an exact borderline case, a failed case, a zero
polarized-channel case, and a loss-dominated case.  Equality at `1/400` is explicitly
classified as `BORDERLINE`, never as a strict pass.

## 5. Claim firewall and route evaluation

```text
TPC223_ROUTE_ADVANCE = YES
TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA
TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT
TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT
TPC223_LITERAL_REASSEMBLY_INTERFACE = OPEN_CONDITIONAL_INPUT
TPC223_EFFECTIVE_SAVING = CERTIFIED_EXACT_MIN_MINUS_LOSS
TPC223_STRICT_1_OVER_400 = CONDITIONAL_ONLY
TPC223_ARITHMETIC_ADVANCE = NO
TPC223_FIXED_ATOM_CREDIT = 0
TPC223_L2 = NONE
TPC223_FULL_GATE_B = OPEN
TPC223_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC223_STATUS = CONDITIONAL_THEOREM
TPC223_ROUND2_CLUE = PROVE_OR_REFUTE_THE_COMMON_LITERAL_TWO_CHANNEL_INTERFACE
```

Strongest positive result: the exact minimum-of-two-savings compiler.  Strongest
obstruction: either missing channel or an exact boundary ledger fails the strict gate.
The next theorem must prove the two inputs on one common literal object and clock.
