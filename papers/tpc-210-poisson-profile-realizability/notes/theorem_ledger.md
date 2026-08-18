# Theorem Ledger

## PROVED

`T210.1` — For every prime `q>2`, the map

```text
F_D in Schwartz(R) -> B_D(s) = sum_(n = s mod q) Fhat_D(n/q)
```

is surjective onto `C^(F_q^*)`. A finite family of target profiles is
realized simultaneously by compactly supported smooth Fourier transforms.

`T210.2` — For any squarefree unit divisor family and `c_D=mu(D)`, the
realizable profiles `B_D=mu(D) U_D^* z` satisfy exact coherent alignment.

`T210.3` — The profile-aware whole-frame energy is the positive-semidefinite
cross-divisor Gram quadratic form

```text
sum_(D,E) c_D conjugate(c_E) G_(D,E),
G_(D,E) = <P U_D B_D, P U_E B_E>.
```

## REFUTED_SCOPED

`T210.R1` — Schwartz regularity plus finite Poisson reindexing plus literal
Mobius signs imply a universal profile-level power saving.

## NUMERICALLY_CERTIFIED

Finite construction checks pass at `q=3,5,7,11,13`; exact interpolation error is
zero in all 20 realized divisor-profile rows (178 residue coordinates).

## STOP_SCOPED

`T210.S1` — No theorem that treats the admissible profile class alone can
produce the required cross-divisor saving. The aligned family is an interface
obstruction, not a counterexample to the literal coupled physical TPC packet.

## OPEN

Prove a cross-divisor Gram bound for the actual Mobius/Poisson profiles after
the exact `(q-2)` diagonal subtraction, prime shell, kernel localization,
four-packet signs, and block reassembly.

## Status

```text
CLAIM_LEVEL = PROVED_STRUCTURAL_L1_STOP_SCOPED_PROFILE_CLASS
TPC210_ROUTE_ADVANCE = YES
TPC210_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC210_ARITHMETIC_ADVANCE = NO
TPC210_FIXED_ATOM_CREDIT = 0
TPC210_L2 = NONE
```
