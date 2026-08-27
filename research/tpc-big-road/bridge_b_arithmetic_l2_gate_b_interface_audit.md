# Bridge B: typed arithmetic `L2` / Gate-B interface audit

Date: 2026-08-27

TPC-281 is the direct continuation of TPC-280's additive-leakage compiler.  It
does not pretend that an arithmetic estimate exists; it types the exact
interface that would be used if a literal source operator
`A_X:H_X -> ell^2(I_X)` satisfied

```text
||A_X||_(2->2) <= K X^(-sigma).
```

For four packets with `D=sum ||V_j||^2`, `G=||sum V_j||^2`, and `q=G/D`, the
operator contraction gives

```text
||A_X S||_2^2 <= K^2 X^(-2sigma) Q_X D.
```

If TPC-280 supplies
`Q_X <= B X^(-gamma)+(ell/d)X^(-delta) <= (B+ell/d)X^(-kappa)`, with
`kappa=min(gamma,delta)`, and `D<=d_+X^a`, then

```text
||A_X S||_2^2 <= K^2 d_+ (B+ell/d) X^(a-2sigma-kappa).
```

A scalar readout of norm at most one is bounded by the output norm.  A separate
exact obstruction shows why this is not an attachment theorem: in `R^2`, the
parallel and perpendicular rank-one functionals for the same nonzero packet
sum have equal operator norm but squared attachments `G^2` and `0`.

Four exact packet fixtures, four typed interface cases (including a genuine
two-term leakage case), and all twelve TPC-280 parent rows are certified with
rational arithmetic.  The transfer grants no power credit and is not an
asymptotic arithmetic estimate.

```text
TPC281_MAXIMUM_CLAIM = PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT
TPC281_ROUTE_ADVANCE = YES_SCOPED_TYPED_ARITHMETIC_L2_GATE_B_INTERFACE_AUDIT
TPC281_TYPED_ARITHMETIC_L2 = PROVED_CONDITIONAL_INTERFACE_ONLY
TPC281_ATTACHMENT_IDENTIFIABILITY = REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL
TPC281_FINITE_ATTACHMENT_AUDIT = NUMERICALLY_CERTIFIED_FINITE_4_PACKET_FIXTURES
TPC281_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC281_ARITHMETIC_ADVANCE = NO
TPC281_L2 = OPEN_LITERAL_SOURCE
TPC281_FIXED_POWER_CREDIT = 0
TPC281_FULL_GATE_B = OPEN
TPC281_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC281_TWIN_PRIME_RESULT = NONE
TPC281_STATUS = PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT
TPC281_ROUND2_CLUE = REQUIRE_LITERAL_SOURCE_ARITHMETIC_L2_AND_TYPED_ATTACHMENT_NONDEGENERACY
```

Strongest positive result: a precise typed theorem translating arithmetic
operator decay and packet gain into output energy.  Strongest obstruction:
equal norm and equal packet geometry do not prevent zero scalar attachment.
Open theorem: prove the literal source `L2` estimate and a typed
attachment/nondegeneracy statement on the common growing schedule.

The Session-named `propose.md` and Route evaluator files are absent in this
checkout.  The local proof package, canonical certificate, independent replay,
hostile stress audit, and fail-closed checker provide the scoped Route-B
evaluation.
