# TPC-329 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| Literal deleted-diagonal block | `PROVED_EXACT_FINITE` | displayed finite matrix formula |
| `C_e=sum_p e_p B_p` reassembly | `PROVED_EXACT_FINITE` | finite signed matrix |
| `E_e(v)=D_e(v)+O_e(v)` | `PROVED_EXACT_FINITE` | finite Gram expansion |
| Affine placement map is bijective | `PROVED_EXACT_FINITE` | `gcd(5,2048)=gcd(5,4096)=1` |
| Placement preserves source multiset and `L2` | `PROVED_EXACT_FINITE` | permutation-matrix identity |
| V59 source-vector formula | `PROVED_EXACT_FINITE_DECLARED_MODEL` | finite Euler/log enclosure |
| Actual 32-row four-law replay | `NUMERICALLY_CERTIFIED_FINITE` | independent checker and JSON |
| Permuted 32-row four-law replay | `NUMERICALLY_CERTIFIED_FINITE` | independent checker and JSON |
| Two-scale growth pairing | `NUMERICALLY_CERTIFIED_FINITE` | 64 guarded finite pairs |
| All-plus actual census | `NUMERICALLY_CERTIFIED_FINITE` | 31 negative / 1 positive |
| All-plus permuted census | `NUMERICALLY_CERTIFIED_FINITE` | 0 negative / 32 positive |
| Placement classification changes | `NUMERICALLY_CERTIFIED_FINITE` | 31/32 all-plus comparisons |
| Positive component controls | `NUMERICALLY_CERTIFIED_FINITE` | 32/32 for both components |
| Source-norm-only sign explanation | `REFUTED_SCOPED` | actual/permuted finite contrast |
| Growing source-native arithmetic `L2` | `OPEN` | no source-uniform estimate |
| Placement-aware reassembly theorem | `OPEN` | no uniform cross-term control |
| Canonical arithmetic sign | `OPEN` | four laws remain noncanonical |
| Fixed-power credit | `0` | no asymptotic payment |
| Route-B Gate B | `OPEN` | reassembly and endpoint remain open |
| Twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

A held-out two-scale source-native audit and a fixed norm-preserving placement
control are both independently replayed.  The latter isolates a genuine
finite coordinate-placement effect in the signed Gram diagnostic.

## Strongest obstruction

The all-plus sign changes from `31/32` negative actual rows to `32/32`
positive permuted rows while the source multiset and `L2` norm are unchanged.

## Open theorem

Characterize or uniformly bound the position-sensitive part of
`v^T C_e^T C_e v`, retaining the literal divisibility masks and physical
normalization.

## Reusable structure

```text
locked source -> coherent operator -> Gram split -> actual/null pairing
              -> growth audit -> independent replay -> claim firewall
```

## ROUND2_CLUE

`SEPARATE_SOURCE_NORM_FROM_ARITHMETIC_PLACEMENT_WITH_MULTIPLE_PREDECLARED_CONTROLS`
