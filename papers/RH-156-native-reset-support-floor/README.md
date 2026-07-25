# RH-156: Native Reset Support Floor

RH-156 composes the RH-155 native recent/tail pair with the RH-153 robust
overlap base law.  From selected full-memory eigenvalue endpoints `ell,u`,
tail mass `tau`, and overlap lower `alpha`, it proves the sharp support lower

`alpha * sqrt((ell-tau)/u) * (1-sqrt(tau/(ell-tau)))^4`.

All 120 frozen transitions are positive.  The minimum is `3.26204e-8`, 111
exceed `1e-6`, and 74 exceed `1e-4`.  All 62 terminal-half transitions form a
common finite native-support tube with the same minimum.  This is not yet the
directional cross-action support used by the earlier Stage-A route.
