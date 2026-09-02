# TPC-348 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| Two-sided projection defect identity | `PROVED_EXACT_FINITE` | projection algebra |
| Position-aware mask-hit column formula | `PROVED_EXACT_FINITE_DECLARED_MODEL` | split according to `p\mid t` |
| Coordinate lower-witness inequality | `PROVED_EXACT_FINITE_LINEAR_ALGEBRA` | induced Euclidean norm |
| Mask-hit selector `J_I` | `PROVED_EXACT_FINITE_DECLARED_MODEL` | declared shell and interval |
| Positive witness census | `NUMERICALLY_CERTIFIED_FINITE_192_OF_192` | producer plus reverse replay |
| Position formula audit | `NUMERICALLY_CERTIFIED_FINITE_192_ROWS` | max discrepancy `2.0872192863e-14` |
| Best-hit / defect ratio | `NUMERICAL_OBSERVATION` | `0.453958762219--0.897148966365` |
| Best-hit / ideal ratio | `NUMERICAL_OBSERVATION` | `0.0183057714619--0.336311065586` |
| Mask-discard shortcut | `REFUTED_SCOPED` | finite declared panel only |
| Source-uniform arithmetic `L2` | `OPEN` | no growing estimate |
| Uniform masked operator bound | `OPEN` | no source-uniform control of `D_I` |
| Fixed-power credit | `0` | no asymptotic payment |
| Route-B Gate B | `OPEN` | reassembly and endpoint absent |
| Twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

The mask defect has an exact position-aware coordinate lower witness.  The
selected mask-hit column is at least `45.3958%` of the defect spectral norm on
every declared row.

## Strongest obstruction

The finite obstruction is localized: the masks leave a positive column witness
on all `192` rows, so the defect cannot be certified small by discarding the
mask terms on this panel.  The result does not imply a growing lower bound.

## Open theorem

Find a source-uniform estimate for the position-aware defect or prove arithmetic
cancellation while retaining all residue masks.  A natural next test is a
prime-balanced signed witness, without claiming it has asymptotic force.

## Reusable structure

```text
literal block -> projection defect -> mask-hit set -> coordinate witness
              -> exact lower inequality -> finite position audit -> firewall
```

## ROUND2_CLUE

`TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2`
