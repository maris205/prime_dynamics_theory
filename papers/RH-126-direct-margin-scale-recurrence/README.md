# RH-126: direct-margin scale recurrence

For `m_tau(K)=s4(K)-tau*s1(K)`, RH-126 proves the sharp recurrence

```text
m_tau(K') >= c m_tau(K) - (1+tau) epsilon
```

whenever the first and fourth singular values move by at most `epsilon`
from a common scale `c`.  The iterated weighted-error formula is immediate.

The finite archive gives a useful barrier: only 26/96 optimal endpoint fits
retain a positive one-step margin, only 6/96 full four-mode fits do, and none
of the 24 five-scale endpoint chains remains positive.  This does not refute
all direct recurrences; it rules out the simplest scalar-profile mechanism
on the current pairings.
