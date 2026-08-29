# TPC-309 proof package

## Claim ceiling

```text
PROVED_EXACT_FINITE = contiguous-window construction; prefix feasibility
                       nesting; finite Hamming enumeration and extrema;
                       radius monotonicity; radius-zero recovery; positive
                       interval classification; common-normalizer cancellation
NUMERICALLY_REPRODUCED_FINITE = 3 ladders x 18 cases x 3 radii = 162 envelope
                                 observations and 2106 candidate evaluations
NUMERICAL_OBSERVATION = the BASE obstruction is not profile-location invariant;
                        LOW/HIGH move strict discordances and broaden the
                        unresolved region under completion envelopes
OPEN = directed-rounding certificate; profile-independent preference theorem;
       causal identification; uniform asymptotic budget; arithmetic L2;
       fixed-power credit; full Gate B; twin-prime conclusion
```

## Proposition 1: neighboring profile windows

The three declared ladders are ordered 17-element contiguous subwindows of a
19-element ordered pool, and each adjacent pair shares 16 coordinates.

### Proof

This follows by direct indexing of the displayed tuple `P`.  The middle
window is the TPC-308 list, while the other two are its one-step left and
right shifts.  The construction is finite and introduces no unregistered
source value. `\square`

## Proposition 2: nested prefix feasibility

For a fixed ladder and target, the least-squares residual over the first `k`
columns is nonincreasing in `k`.  Hence, if `k(t,a)` exists, every longer
prefix up to the row rank remains feasible, and the maximum of the two first
feasible prefixes is feasible for both directional targets.

### Proof

The span of the first `k` columns is contained in the span of the first
`k+1` columns.  Orthogonal projection onto a larger finite-dimensional span
cannot increase the distance to the target.  Apply this separately to the two
targets and take the larger first-feasible index. `\square`

## Proposition 3: finite completion algebra

For binary `h`, every element of `C_r(h)` is obtained uniquely by flipping a
subset of at most `r` coordinates.  Consequently

```text
|C_r(h)| = sum_{j=0}^{min(r,m)} binom(m,j),
```

and the enumerated minimum and maximum are exact.  The lower envelope is
nonincreasing and the upper envelope nondecreasing in `r`; radius zero is the
native target; simultaneous global sign reversal preserves every loss.

### Proof

The difference set `{j:h'_j != h_j}` is the unique flip subset, and binary
values force a flip to be multiplication by `-1`.  Set inclusion gives the
monotonicity, the empty subset gives radius-zero recovery, and squaring makes
simultaneous negation loss-preserving. `\square`

## Proposition 4: budget normalizer cancellation

If both directional fits use the same positive normalizer `N_a`, then

```text
(E_right,a/N_a)/(E_left,a/N_a)=E_right,a/E_left,a.
```

Thus the three reported positive normalizers can differ in scale but cannot
change the exact right/left source ratio.  The interval implementation still
requires each denominator to be positive.

## Proposition 5: conservative class soundness

If the four envelope extrema are positive and their decimal enclosures are
valid, the displayed ratio interval contains every finite completion ratio.
An interval wholly below `0.9` is safely right-lower; one wholly above `1.1`
is safely left-lower; all other cells are unresolved.

## Numerical statement

The locked producer and standalone NumPy checker agree on the 54 profile
cases, their 162 envelope records, the 2106 candidate evaluations, and the
published class censuses.  BASE recovers TPC-308's class path.  LOW and HIGH
produce different strict-discordance locations, so the finite observation is
not profile-location invariant.

## Corrections and missing assumptions

- The source-first labels remain inherited from the physical-Gram-dependent
  TPC-302 construction.
- The profile windows are a declared finite modeling perturbation, not a
  probability distribution or an asymptotic family.
- Physical rows are float64 replays and the decimal padding is not directed
  rounding; the result is numerical reproduction, not a formal enclosure
  theorem.
- Completion balls are adversarial diagnostics, not causal interventions.
- No finite sensitivity result pays the arithmetic L2, uniform-budget,
  fixed-power, Gate-B, or twin-prime obligations.
