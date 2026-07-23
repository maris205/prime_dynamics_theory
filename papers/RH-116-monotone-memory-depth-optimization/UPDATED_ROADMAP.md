# Route update after RH-116

Memory depth is no longer an uncontrolled tuning parameter inside the nested
Weyl route.  Its lower bound is monotone, first passage is cost-optimal, and
full-history search is complete.  The one-path audit also removes the
cross-assembly weakness isolated in RH-115.

The next uncertainty is physical rather than algorithmic.  RH-117 should
audit capacity, concentration, support-margin, and depth envelopes across the
five scales.  Trend fits may be reported only as numerical evidence.  The
paper should also prove a finite-anchor barrier: finitely many positive scale
measurements cannot determine an all-level asymptotic law, because smooth
positive continuations can match every anchor while having incompatible
limits near zero.
