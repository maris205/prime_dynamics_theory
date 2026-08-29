# TPC-308 proof package

## Claim

On the frozen TPC-307 finite atlas, the Hamming completion-envelope protocol
is exact as a finite definition and the resulting 54 envelope observations
are numerically reproduced.  The native discordance count decreases from
`3` to `2` to `1` at radii `0,1,2`, with all surviving discordances on
`Q=70 -> 90` and exponent one.

## Status

```text
PROVED_EXACT_FINITE = Hamming-ball definition; candidate count; fixed-
                       prediction extrema; radius monotonicity; radius-zero
                       recovery; global-sign invariance; interval class rule
NUMERICALLY_REPRODUCED_FINITE = 18 cases x 3 radii = 54 observations and
                                 702 enumerated candidate evaluations
NUMERICAL_OBSERVATION = discordance attenuation 3 -> 2 -> 1 and localization
                        to the final 70 -> 90 transition
OPEN = directed-rounding certification; completion generation/causal
       identification; uniform asymptotic budget; arithmetic L2; fixed-power
       credit; full Gate B; twin-prime conclusion
```

## Assumptions

The parent TPC-307 certificate, physical matrix, overlap frontier, selected
prefix, and native binary labels are frozen and provenance-locked.  Holdout
losses are positive on the declared cells.  The numerical replay uses the
literal float64 physical construction followed by a high-precision frontier
solve and padded decimal enclosures, exactly as documented in the
computational note.

## Notation

For a directional holdout of length `m`, `h` is its native target and `y` is
the already-fitted prediction.  `C_r(h)` is the Hamming ball, and `L_r^-` and
`L_r^+` are its lower and upper mean-square losses.  `R_r` denotes the
right-over-left ratio enclosure.

## Proof strategy

The finite algebra is separated from the numerical replay.  First enumerate
the flip subsets and count them.  The finite set inclusion proves monotonicity
and the singleton case proves recovery.  Sign invariance follows by negating
both prediction and target.  For positive losses, interval division gives a
valid conservative ratio enclosure; the threshold implication is immediate.
The producer and independent checker then replay the declared finite object.

## Dependency map

```text
TPC-302 source-first labels
        -> TPC-307 common ambient / overlap fit / exclusive holdout
        -> TPC-308 fixed predictions + Hamming completion balls
        -> finite envelope extrema -> ratio classes -> stability atlas
```

## Proposition 1: finite Hamming-ball enumeration

For `h in {-1,+1}^m` and integer `r>=0`, every element of `C_r(h)` is
obtained exactly once by choosing a flip subset `F subset {1,...,m}` with
`|F|<=r` and replacing `h_j` by `-h_j` on `F`.  Therefore

```text
|C_r(h)| = sum_{j=0}^{min(r,m)} binom(m,j).
```

### Proof

Given a completion `h'`, let `F={j:h'_j != h_j}`.  Binary values imply
`h'_j=-h_j` exactly on `F`, and the Hamming constraint gives `|F|<=r`.
Conversely each such subset produces a binary completion at distance
`|F|`.  The recovered difference set is unique, so the correspondence is
bijective. `\square`

## Proposition 2: exhaustive extrema and radius monotonicity

For fixed `y,h`, the finite enumeration returns the exact minimum and maximum
of the squared holdout loss.  Moreover,

```text
L_{r+1}^- <= L_r^- <= L_r^+ <= L_{r+1}^+.
```

### Proof

An explicitly enumerated finite set contains every feasible completion, so the
ordinary minimum and maximum over the list are the desired extrema.  The
Hamming balls satisfy `C_r(h) subset C_{r+1}(h)`.  Taking a minimum over a
larger set cannot increase it, and taking a maximum cannot decrease it. `\square`

## Proposition 3: radius-zero and sign invariance

`C_0(h)={h}`.  Further, for every completion `h'` and prediction `y`,

```text
||(-y)-(-h')||_2^2 = ||y-h'||_2^2.
```

Hence the radius-zero envelope is native and simultaneous global negation
leaves all envelope extrema unchanged.

### Proof

The only subset of size at most zero is the empty set, proving the singleton
claim.  The displayed equality is the square of a sign reversal, and the
map `h' -> -h'` is a bijection of the corresponding completion balls. `\square`

## Proposition 4: conditional ratio classification

If all four envelope extrema are positive, then

```text
R_r in [L_r^-(y_R,h_R)/L_r^+(y_L,h_L),
         L_r^+(y_R,h_R)/L_r^-(y_L,h_L)].
```

Thus an interval upper endpoint below `0.9` implies right-lower, and a lower
endpoint above `1.1` implies left-lower.

### Proof

For positive `a in [a_-,a_+]` and `b in [b_-,b_+]`, the quotient lies between
`a_-/b_+` and `a_+/b_-`.  Apply this to the two finite loss intervals and use
the definitions of the strict classes. `\square`

## Numerical statement

The stored producer certificate and the standalone NumPy checker agree on the
declared finite envelope values within the documented replay slack.  The
aggregate candidate counts are `36,186,480` at radii `0,1,2`.  The exact
finite census is `13/3/2`, `11/2/5`, and `10/1/7` for
concordant/discordant/unresolved.  This is a numerical reproduction, not a
formal proof of decimal enclosures.

## Corrections and missing assumptions

- The fit coefficients are frozen from TPC-307; completions never feed back
  into the overlap frontier.
- The completion ball is an adversarial finite diagnostic, not a probability
  distribution or a source-generated law.
- TPC-302 labels depend on a physical Gram construction, so target-generation
  leakage is inherited.
- Float replay and padded intervals are not directed rounding.  A formal
  certificate would require exact or interval arithmetic for the physical
  matrix and optimization.
- The radius-two result is not an asymptotic statement about growing shells.

## Open risks

The remaining `70->90` discordance may depend on the chosen profile prefix,
the finite source window, or the native label construction.  A prefix
perturbation/stability audit is therefore the next natural paper.  Until an
independent target-generation and growing-parameter theorem is supplied, all
Route-B arithmetic and twin-prime gates remain open.
