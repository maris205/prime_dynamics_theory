# Theorem Ledger

| Item | Status | Evidence | Boundary |
|---|---|---|---|
| V46 exponent/source lock | PROVED / LOCKED | parent Equation (1.1), (1.5) | no altered scale |
| `4Q<H` in the asymptotic source range | PROVED | `H/(4Q)=x^(31/96)/4` | sufficiently large `x` |
| fixed-q residue no-collision | PROVED_EXACT | integer cutoff and `2q<H` | fixed `q,d` rows |
| fixed-q row norm | PROVED_EXACT | injective atom supports | no shell cancellation |
| shell Cauchy envelope | PROVED | Cauchy plus `q<=2Q` | `P^2` factor retained |
| `P<=2Q` shell count | PROVED_ELEMENTARY | interval cardinality | no PNT saving |
| normalized exponent `11/32` | PROVED_EXACT_LEDGER | `Q^3/H=x^(11/32)` | logarithmic factor remains |
| divisor direct-sum envelope | PROVED_STRUCTURAL_L1 | sum of row bounds | complete period only |
| aligned-support fixture | NUMERICALLY_CERTIFIED | exact rational reconstruction | finite, not asymptotic |
| free shell orthogonality | REFUTED_SCOPED | all fixture rows support `{1,4}` | only the shortcut is refuted |
| Mobius cancellation | NONE | no signed cancellation used | arithmetic advance is NO |
| finite-window Gram | OPEN | not in theorem | physical interval missing |
| prime-shell/four-packet reassembly | OPEN | not in theorem | Gate B unpaid |
| fixed atom / twin-prime endpoint | OPEN | no attachment | credit `0` |

## Strongest positive result

The literal complete-period direct-sum emitter energy satisfies

```text
L^(-1)E_direct <= C_psi*x^(11/32)*(log x)^3
```

without a prime-counting theorem or Mobius cancellation.

## Strongest obstruction

Different prime-shell rows can have exactly aligned residue support, so the
shell Cauchy factor cannot be replaced by an orthogonal sum on structural
grounds alone.

## Open theorem

Attach this complete-period direct-sum envelope to the literal finite physical
window while preserving the source signs, four-packet reassembly, and the
remaining endpoint ledger.

## Reusable structure

```text
source inequality 4Q<H
  -> fixed-q injective integer atoms
  -> exact fixed-q row energy
  -> shell Cauchy envelope
  -> Mobius-log weighted divisor sum
  -> x^(11/32+o(1)) complete-period bound
```

## ROUND2_CLUE

```text
ATTACH_THE_COMPLETE_PERIOD_DIRECT_SUM_ENVELOPE_TO_THE_LITERAL_FINITE_WINDOW_WITHOUT_FREE_SHELL_ORTHOGONALITY
```
