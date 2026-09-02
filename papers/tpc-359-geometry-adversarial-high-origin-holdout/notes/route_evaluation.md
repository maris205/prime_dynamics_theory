# TPC-359 route evaluation and proof package

## Object and scope

The object is the literal finite matrix

\[
 B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 (1_{p\mid u-t}-(p-1)^{-1})1_{u\ne t}1_{p\nmid u}1_{p\nmid t},
\]

summed over primes `Q < p <= 2Q`, with the unsigned geometry
`G_u=sum_{p,t} B_p(u,t)^2` and normalized matrix
`D_G^{-1/2} A D_G^{-1/2}`.  The finite panel is fully specified in the
certificate protocol.  The source response is not evaluated.

## Evidence ledger

| item | status | evidence |
|---|---|---|
| geometry-only candidate selection | `PROVED_EXACT_FINITE_RESPONSE_BLIND` | deterministic 51-candidate scan and greedy separation |
| finite Schur and Frobenius inequalities | `PROVED_EXACT_FINITE` | elementary finite matrix inequalities; rational anchor |
| high-origin operator replay | `NUMERICALLY_CERTIFIED_FINITE_288_ROWS` | producer, reverse-shell checker, mutation stress, Bridge-B |
| parent-cap transfer | `NUMERICALLY_CERTIFIED_FINITE_SCOPED` | maxima within 0.001 of TPC-358 |
| monotone spectral decay | `REFUTED_SCOPED_ON_DECLARED_LADDER` | 12/36/6 transition census |
| growing masked-operator estimate | `OPEN` | no quantifier beyond declared finite panel |
| source-uniform arithmetic `L2` | `OPEN` | source response intentionally absent |
| Route-B reassembly / twin-prime endpoint | `OPEN` / `NONE` | official evaluator files absent; no arithmetic credit |

## Route A / Route B decision

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are not present in the repository.  Therefore an
official evaluator verdict cannot be issued.  Local Bridge-B is used only as a
fail-closed artifact checker.  The maximum release claim is finite and scoped;
`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and `FULL_GATE_B=OPEN`.

## Reusable structure

```text
unsigned geometry-only scan
 -> separated high-origin selection
 -> raw/normalized all-law envelopes
 -> all-plus spectral ladder
 -> reverse-shell and mutation checks
 -> finite cap transfer plus uniformity firewall
```

## Strongest result and obstruction

The strongest positive result is a response-blind high-origin transfer of the
finite normalized caps.  The strongest obstruction is that the normalized
spectral sequence remains nonmonotone, so the finite cap has no demonstrated
growing-origin or source-uniform consequence.

## ROUND2_CLUE

`TEST_SCHUR_TIGHTNESS_AND_INDEPENDENT_HIGH_ORIGIN_REPLICATION`.
