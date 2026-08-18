# Bridge A / Gate B TPC-210: Poisson profile realizability and Mobius alignment

Date: 2026-08-18

Status: numbered structural paper, `PROVED_STRUCTURAL_L1 / STOP_SCOPED`.

TPC-209 reduced the whole-frame route to a profile-aware nonprincipal-character
expression. TPC-210 asks whether the remaining Schwartz/Poisson origin of each
profile, together with the literal Mobius signs, already rules out coherent
cross-divisor alignment.

It does not. The result is a class-level theorem and a scoped obstruction:

1. For every prime `q>2`, every finite residue vector `b` on
   `G_q=F_q^*` is the exact Poisson residue profile of a compactly supported
   smooth Fourier packet.
2. For any squarefree unit divisor family, the literal choice
   `c_D=mu(D)` admits the exact profiles `B_D=mu(D) U_D^* z`, where `z` is
   centered. Every weighted output then equals `z`.
3. The coherent-to-weighted-diagonal energy ratio is exactly the number of
   divisor components.
4. Every profile-aware energy is the positive-semidefinite cross-divisor Gram
   quadratic form `sum_(D,E) c_D conjugate(c_E) G_(D,E)`.

The interpolation construction uses `n_s=s+10qs` and a bump supported in an
interval of radius `1/(4q)` around `n_s/q`. These intervals contain exactly one
point of the full dual lattice and therefore realize arbitrary target values in
the residue sums.

The construction deliberately allows independent `F_D`. It therefore does not
claim that the literal coupled TPC physical coefficient family realizes the
aligned profiles. It proves that individual Schwartz regularity, Poisson
reindexing, and Mobius signs alone cannot supply a saving. A positive TPC
theorem must control the physical cross-divisor Gram matrix while retaining the
exact `(q-2)` diagonal, prime shell, kernel localization, four-packet signs,
and block reassembly.

## Theorem ledger

```text
T210.1 = PROVED_EXACT_FINITE_PROFILE_INTERPOLATION_BY_C_C_INFINITY_FOURIER_BUMPS
T210.2 = PROVED_EXACT_MOBIUS_WEIGHTED_ADJOINT_DILATION_ALIGNMENT
T210.3 = PROVED_EXACT_CROSS_DIVISOR_GRAM_QUADRATIC_REDUCTION
T210.R1 = REFUTED_SCOPED_SCHWARTZ_POISSON_MOBIUS_UNIVERSAL_SAVING
T210.S1 = STOP_SCOPED_PROFILE_CLASS_ONLY
T210.OPEN = ACTUAL_PHYSICAL_MOBIUS_POISSON_CROSS_DIVISOR_GRAM_BOUND
```

## Canonical registry

```text
TPC210_MAXIMUM_CLAIM = EXACT_FINITE_POISSON_PROFILE_INTERPOLATION_PLUS_MOBIUS_WEIGHTED_ALIGNED_GRAM_OBSTRUCTION
TPC210_ROUTE_ADVANCE = YES
TPC210_STRUCTURAL_THRESHOLD_A = PASS
TPC210_FINITE_PROFILE_INTERPOLATION = PROVED_EXACT
TPC210_MOBIUS_WEIGHTED_ALIGNED_FAMILY = PROVED_EXACT
TPC210_CROSS_DIVISOR_GRAM_REDUCTION = PROVED_EXACT
TPC210_PROFILE_CLASS_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC210_ACTUAL_PHYSICAL_PROFILE_BOUND = OPEN
TPC210_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC210_ARITHMETIC_ADVANCE = NO
TPC210_GLOBAL_GATE_B_ADVANCE = NO
TPC210_FIXED_ATOM_CREDIT = 0
TPC210_L2 = NONE
TPC210_FIRST_FATAL = NO_CROSS_DIVISOR_PHYSICAL_COUPLING_FROM_SCHWARTZ_POISSON_MOBIUS_INTERFACE_ALONE
TPC210_ROUND2_CLUE = FIND_A_LITERAL_PHYSICAL_CROSS_DIVISOR_COUPLING_OR_GRAM_BOUND_BEFORE_ANY_NEW_PRIME_BDH_ATTACHMENT
TPC210_REUSABLE_STRUCTURE = ISOLATED_FOURIER_NODE_PROFILE_INTERPOLATION_PLUS_MOBIUS_ADJOINT_ALIGNMENT_PLUS_PSD_GRAM
TPC210_TPC_TRIGGER = true
TPC_210_TRIGGER = true
```

The finite certificate and paper are located at
`papers/tpc-210-poisson-profile-realizability/`. The certificate checks
`q=3,5,7,11,13`, 20 divisor-profile rows, 178 residue-coordinate rows, and the
q=5 ratio-2 resonance. These checks certify the finite construction only; they
do not prove an asymptotic prime correlation estimate.
