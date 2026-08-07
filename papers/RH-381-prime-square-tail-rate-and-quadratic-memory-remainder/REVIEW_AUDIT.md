# RH-381 adversarial review audit

Decision: **ACCEPT WITH ALL IDENTIFIED ISSUES RESOLVED**

## Independent proof review

The read-only proof review reconstructed the full chain independently:

1. the RH-374 run formula gives the exact finite Euler form for `X_j` and the
   positive limiting anchor;
2. a factorwise product union bound gives `|X_j-X_infinity|<=170T_j`;
3. the RH-379 product gives the `H` tail bound, and the run interpretation
   gives `0<=M_j/A_j<=1`;
4. two finite tail telescopes give the exact current-tail and next-tail
   identities;
5. finite RH-380 increment telescopes followed by the frozen RH-379 cofinal
   limit give the infinite sum;
6. the ledgers `340` and `2` combine to the uniform `342` quadratic
   remainder, and division by positive `T_y` gives the ratio limit.

Successor indices, Euler-factor positivity, the order of limits, and every
constant were checked independently. The final proof review reports zero
mathematical blockers and zero mathematical minors. It found 34 unique
labels, 27 resolved cross-references, and 4 resolved citation keys.

## Issues found and repaired

- Early directed-decimal candidates leaked the global 28-digit Decimal
  context through absolute value and margin subtraction. The final protocol
  uses context-free `copy_abs`, explicit 60-digit floor/ceiling operations,
  and exact rational tail factors. Two independent reconstructions matched
  the final 6,851-byte digest
  `e0342f871b1f952039da2b1025fa7598771b9fa089295f07cb60b11f70cee15c`
  field for field.
- Digest equality is a hard fail-closed gate rather than a diagnostic flag.
- Frozen constants, cutoff, and precision now require exact integer types;
  float and Boolean aliases are rejected. Tail identities require exact
  `Fraction` inputs, and prime-square weights validate odd primality.
- Release checks no longer rely on Python `assert`; optimized-mode replay is
  explicitly tested.
- Archive JSON loaders now reject duplicate keys and non-finite constants.
- Archive replay compares the complete stored source-lock object with freshly
  regenerated release locks; duplicate rows and group/commit rebinding no
  longer disappear through a path-to-hash map.
- A malformed LaTeX alignment row, a math token in a PDF heading, stale
  hand-written theorem numbering in the trace, and an inaccurate RH-MVP2
  bibliography title/author were corrected before sealing.

## Numerical review

There is no statistical inference, regression, or fitted model. Six exact
run rows, four exact finite tail-identity rows, and six directed interval
rows are reproduction and mutation fixtures. The all-`y` conclusions come
from the symbolic proof.

## Scope decision

Route A is GO only for the first-order prime-square-tail rate and explicit
quadratic remainder inside the frozen phasewise `c11=0` class. A genuine
second-order coefficient remains open. Route B remains `STOP_SCOPED` at the
missing phase-weighted shift-two Mobius correlation theorem. Gates A--E
remain false/open.
