# TPC-278 computational protocol

The producer imports the hash-locked TPC-277 exact source engine and evaluates
12 rows at `s=2`: three scales with `Q-1,Q,Q+1`, plus two clock controls at
`N=192`, and one additional natural control at `N=384`.  It uses exact
`Fraction` arithmetic and stores outward
`10^15` intervals for `r`, `kappa`, and the normalized cross term.

The independent checker accumulates by source column, verifies the exact
`D,G` digest and every interval, and checks the expected 8/4 sign census.  The
stress checker mutates the sign census, flip count, parent hash, and fixed-
power field and requires rejection.
