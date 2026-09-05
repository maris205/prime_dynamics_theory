# TPC-394 derivation package

## Finite kernel

For `p` in `(Q,2Q]`, define

`K_p(u,v) = p (p/Q)^2 H^2/(H^2+(u-v)^2)
             (1_{p | u-v} - 1/(p-1))
             1_{u != v}1_{p not | u}1_{p not | v}`

with `Q=8192` and `H=66`.  The row geometry is

`G(u) = sum_p sum_v K_p(u,v)^2`,

and the two signed matrices are `M_l(u,v)=sum_p s_l(p)K_p(u,v)`, with
`s_all_plus(p)=1` and `s_alternating(p)=(-1)^index(p)` in ascending shell
order.

## Band and normalizations

Partition the `N=1024` coordinates into eight blocks of length 128.  The
`fixed_c3` mask retains block pairs with index distance at most three.  The
local matrix is `M_l/sqrt(G(u)G(v))`.  The three scalar matrices divide by,
respectively, the five-origin calibration mean of `G`, the current-origin
mean of `G`, and the first calibration-origin mean of `G`.

For each law/normalization cell, let `S(o)` be the masked spectral diagnostic
at origin `o`.  The primary finite statistic is

`R_all=(max_o S(o)-min_o S(o))/mean_o S(o)`.

The calibration and holdout summaries use the first five and last three
values.  The secondary transfer error is

`T = mean_holdout(S)/mean_calibration(S) - 1`.

No parameter is selected after seeing `S(o)`.  The one-percent and three-
percent thresholds are protocol constants, not fitted tolerances.

## Exact anchor

At the first origin and `Q=8`, the shell is `{11,13}`.  On the 13-point
interval `[5000001,5000014)`, all rational kernel entries are evaluated as
fractions.  The producer records exact positivity and symmetry digests;
the checker verifies the corresponding structural fields.

## Interpretation boundary

The computation tests a finite normalized proxy.  It does not identify the
proxy with a prime-pair correlation, does not supply a source measure, and
does not convert a finite spectral/Schur diagnostic into an analytic norm
bound.  Consequently no power saving or Route gate is paid.
