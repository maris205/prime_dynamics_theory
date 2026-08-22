# TPC-217 Paper Plan

## Title

Finite-Window Attachment by Reduced Rational-Frequency Large Sieve

## Research question

Can the TPC-216 complete-period direct-sum envelope be attached to the literal
physical interval without assuming free orthogonality between prime rows?

## Main theorem

For the literal V46 common-source kernel on `I_x=(x/2,x]`, exact reduced-frequency
regrouping and the standard additive large sieve yield

```text
N^(-1) sum_(n in I_x)|K(n)|^2
  <<_psi x^(11/32)(log x)^5,
```

where `N=|I_x|`.  Equivalently, the unnormalized finite-window energy is
`<<_psi x^(43/32)(log x)^5`.

## Proof architecture

1. Use TPC-214 divisor dilation to regroup all rows by reduced frequency.
2. Use Farey spacing `delta >= U^(-2)` for denominators `h<=U`.
3. Apply the additive large sieve on the consecutive physical interval.
4. Apply TPC-215's `O((log x)^2)` cluster-to-direct majorant.
5. Apply TPC-216's `x^(11/32)(log x)^3` direct-sum envelope.

## Explicit claim classes

```text
PROVED_STRUCTURAL_L1 = exact regrouping, Farey spacing, finite-window large-sieve attachment
NUMERICALLY_CERTIFIED = exact finite regrouping/energy fixture and aligned one-point control
NUMERICAL_OBSERVATION = decimal fixture energy ratios
HEURISTIC = none required
CONJECTURE = none required
OPEN = prime-shell reassembly, four-packet arithmetic reassembly, full Gate B
REFUTED_SCOPED = one-point free finite-window orthogonality shortcut
ARITHMETIC_ADVANCE = NO
```

## Adversarial control

Reuse the aligned shell `d=5`, `H=500`, `q={101,131,151,181}`.  At a one-point
window the coherent row energy is exactly twice the diagonal row energy.  This
does not contradict the long-window large sieve; it rules out a zero-length or
one-point orthogonality shortcut.

## Reproducibility

The project includes a producer, independent checker, optimized-mode checker,
and an explicit frequency-crowding adversary.  All finite row values use exact
rational arithmetic before decimal presentation.
