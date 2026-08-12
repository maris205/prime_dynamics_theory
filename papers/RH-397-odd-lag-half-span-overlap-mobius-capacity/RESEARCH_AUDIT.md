# RH-397 research audit

## Research question

For a centered three-value Mobius rule whose two consecutive windows overlap
in two symbols and whose positive outputs are forbidden at separation `h`,
what is the exact universally safe fixed-clock terminal-log capacity, and
which finite clocks maximize it when `h` is odd?

## Supported answer

- Every fixed `h,q` has an exact collision-aware weighted step-`h`
  independent-set formula.
- Positive projection, two overlap flags, four exact rectangles, and
  nonnegative edge filling lose no optimum.
- For every fixed odd `h`, the maximum over finite declared clocks is
  `K1-kappa2(h)/2+kappa3(h)/4`.
- The two-phase clock attains, every even declared clock attains by literal
  repetition, and every odd declared clock is strict.
- Both signs of every nonzero optimum occur by input reflection.

## Novel contribution

The contribution is the exact half-span overlap reduction and declared-clock
parity classification.  Its load-bearing steps are:

1. retaining the RH-394 analytic law on exactly three shifts despite the
   four-letter finite safety word;
2. deriving the exact safety obstruction `t_r s_(r+h)=0` from a two-symbol
   overlap;
3. proving the complete relation census and the `4,6,6,9` saturating
   rectangles;
4. deriving collision-aware `M,U,V,W` coefficients and the all-branch
   translation `V_r=U_(r+h)`;
5. saturating every binary edge with a nonnegative exact gain;
6. proving surjectivity from step-`h` independent sets to flag strings;
7. extracting the exact weighted capacity formula;
8. proving two-phase attainment for odd `h` and CRT strictness on every odd
   clock.

The novelty statement is bounded by the frozen RH corpus and source closure;
it is not a claim that no analogous theorem exists outside that search
boundary.

## Evidence layers

| Layer | Role |
|---|---|
| RH-394 through RH-396 | sole analytic fixed-three-shift terminal-law bridge |
| manuscript proofs | flags, rectangles, weights, edge filling, surjection, and parity theorem |
| RH-392, RH-395, RH-375 | transitive comparison only |
| 72-row certificate | finite exact reproduction and negative controls |
| mutation and release tests | implementation, schema, source, and scope protection |

The certificate is not asymptotic evidence.  No ordinary-Cesaro statement,
four-shift constant, or collision-free density is substituted for the fixed
terminal-log theorem.

## Adversarial questions resolved

| Question | Resolution |
|---|---|
| Does the fourth safety letter require a four-shift analytic law? | No. It belongs only to the universal finite concatenation test. |
| Is the safety separation `2h` as in a full-span centered overlap? | No. The exact half-span separation is `h`, and two symbols are shared. |
| Can relation weights depend only on flag cardinality? | No. They retain phase-resolved collision-aware `Theta` weights. |
| Does edge filling change previously saturated edges? | No. Each gain is local and nonnegative, and the constraints are directed edgewise. |
| Is the optimizer an unweighted independent set? | No. It is weighted by `Theta_(h,q,r)({L,C,R})`. |
| Must an attaining even clock have minimal period two? | No. Declared-clock repetition is explicitly allowed. |
| Can an odd clock attain for odd `h`? | No. CRT produces adjacent positive triple weights, forcing strict loss. |
| Does the even-lag control classify even lags? | No. It is a finite negative control only. |

Research verdict: GO within fixed-data, centered, noncausal, three-shift
terminal-log scope.
