# RH-380 adversarial review audit

Decision: **ACCEPT WITH ALL IDENTIFIED ISSUES RESOLVED**

## Independent proof review

The proof audit reconstructed the full chain independently:

1. per-run deletion gives `s-2` descendants for even runs and `l-1` for odd
   runs;
2. summation gives the exact even-run recurrence;
3. substitution with the RH-374 odd-run recurrence and `A,D` recurrences
   gives the displayed increment;
4. the persistent length-eight run gives the uniform strict term;
5. exact `delta/theta` scaling plus zero-weight separators gives the special
   same-support saturation theorem;
6. clock lifting, lcm support, strict square-clock growth, and telescoping
   give nonattainment and the explicit gap.

The final proof review reports zero mathematical blockers.

## Issues found and repaired

- A preliminary deletion argument did not explicitly control the cyclic
  seam. The final proof unwraps each run between persistent old zeros.
- Distinct new-prime deletions are now separated by the exact congruence
  `2(d-d')=0 mod s` and `0<2|d-d'|<=14<s`.
- The odd-run prose initially conflated the two endpoints when `l=1`. The
  final proof treats `l=1` separately.
- Early saturation fixtures scored run histograms alone. The final artifact
  adds an independent generic cyclic max-plus DP for every fine clock.
- Exact every-residue density scaling and cause-specific mod-4/mod-9
  separator checks were added.
- Euler-product integer conversion and ambiguous Euler-value comparison now
  fail closed.
- `Q=180` is a scoped new-prime negative control, and its strict inequality
  is proved from the locked H enclosure.
- Bibliographic provenance was corrected: RH-374 defines/proves the
  square-clock limit, while RH-375 identifies the one-site all-clock
  supremum.
- The roadmap now records the immediate normalized tail-rate reopen target
  before the phase-weighted `c11` class-enlargement blocker.

## Statistical and numerical review

There is no statistical inference or fitted model. Finite computations are
exact rational identities and adversarial fixtures. The manuscript states
that the all-order theorems come from symbolic proofs.

## Scope decision

Route A is GO for the stated recurrence, monotonicity, special saturation,
nonattainment, and gap. Route B is `STOP_SCOPED` at nonzero phasewise
`c11`. Gates A--E remain false/open.
