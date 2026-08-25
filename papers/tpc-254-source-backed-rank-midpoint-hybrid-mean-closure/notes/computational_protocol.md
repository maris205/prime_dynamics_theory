# Computational Protocol

## Exact producer

The producer constructs one-line key-sorted ASCII JSON with a terminal
newline. All finite scalar data are canonical rational strings or pairs of
canonical rational strings. Radical quantities are represented by exact
squares: the Haar projector uses `rho^2 h_i h_j`, and the `N=2` Cauchy
fixture records squared norms. No floating-point value is proof data.

The certificate checks six finite fixtures:

1. a noninteger odd-rank clock with exact child endpoints, `rho^2`, projector,
   child sums, and Haar-moment square;
2. nonnegative maximal-row logic with a unit-weight `m=1` row;
3. a whole-shell-zero but nonzero-Haar symbolic control;
4. a Gaussian-rational adjoint-orientation fixture that rejects transpose;
5. a real zero-diagonal derangement at arbitrary signed scale;
6. exact squared-norm equality for the `N=2` Cauchy constant.

The producer's `--check` mode regenerates the expected document in memory and
requires byte equality with the released JSON.

## Independent checker

The checker imports no producer. It uses strict JSON parsing with duplicate
key and nonfinite-token rejection, canonical byte verification, exact source
hashes (with the dynamic handoff read from its frozen baseline Git blob),
exact object shapes, canonical fractions, and `type(value) is int`
for all integer/count fields. This explicitly rejects bool-as-int at top-level
and nested locations. It independently reconstructs every finite identity and
rejects 82 adversarial mutations.

## Stress suite

The stress program checks 192 deterministic exact-rational families:

- 96 integer and 96 noninteger clocks;
- 96 odd-rank and 96 even-rank active intervals;
- exact child consecutiveness, Haar normalization, projector action and
  idempotence, child partial sums, and whole-shell controls;
- nonnegative `m=1` extraction logic;
- Gaussian-rational adjoint identities;
- 96 positive and 96 negative real zero-diagonal derangement scales;
- the exact `N=2` squared Cauchy equality.

No script contains an `assert` statement. Normal and optimized Python modes
must have empty stderr, exit zero, and byte-identical stdout.

## Scope

These programs do not evaluate `Lambda-b_x^(Z_x)`, do not sample a maximal
Type-I sum, and do not claim to prove any asymptotic theorem. The source-backed
analytic result is established in the locked compiler; the executable layer
only validates the deterministic attachment and its firewalls.
