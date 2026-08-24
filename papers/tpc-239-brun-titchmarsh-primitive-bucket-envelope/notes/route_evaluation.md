# Route Evaluation

## Verdict

```text
TPC239_ROUTE_ADVANCE = YES_LOGARITHMIC_ONLY
TPC239_ARITHMETIC_ADVANCE = NO
```

The route advance is real: source-backed prime density removes a factor
`log x/loglog x` from the TPC-237 packet-trace upper bound. The fixed-power
exponent remains `1/48`, so the program's arithmetic `L2`/Gate-B meaning does
not advance.

## Comparison

| Interface | TPC-237 | TPC-239 | Change |
|---|---|---|---|
| Primitive row | `4Q^2/H+4UQ/H` | `<<(Q^2/H)loglog x/log x` | Prime-density logarithm |
| Normalized trace | `<<JM^2x^(1/48)(log x)^5` | `<<JM^2x^(1/48)(log x)^4loglog x` | Factor `log x/loglog x` |
| Fixed-power exponent | `1/48` | `1/48` | None |
| Leading unnormalized exponent | `49/48+o(1)` | `49/48+o(1)` | None |

## Required extraction

```text
STRONGEST_POSITIVE_RESULT = finite-window common-source packet trace with x^(1/48)(log x)^4 loglog x
STRONGEST_OBSTRUCTION = prime density saves only logarithm and leaves fixed-power 1/48
OPEN_THEOREM = weighted or signed within-bucket cancellation beyond coefficient-blind prime counting
REUSABLE_STRUCTURE = primitive residue -> reduced prime AP compiler
ROUND2_CLUE = test exact top-band C_h before seeking further uniform bucket savings
```

The reusable compiler is exact: primitivity of `a` propagates to the physical
multiplier `m`, and therefore the associated prime class is reduced. A further
uniform bucket census of the same coefficient-blind kind is unlikely to change
the power. The next test should retain the literal top-band `C_h` weights and
look for weighted or signed cancellation inside a bucket.
