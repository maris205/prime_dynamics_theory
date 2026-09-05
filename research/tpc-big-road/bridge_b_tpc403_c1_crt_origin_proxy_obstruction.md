# Bridge-B: TPC-403 CRT-origin proxy obstruction

TPC-403 is a finite exact continuation of TPC-402.  It uses the declared
TPC proxy with `N=1024`, `Q=8192`, `H=66`, alternating-index synthetic signs,
and the corrected CRT pattern `o=0 (mod p_{2k})`, `o=-N (mod p_{2k+1})`.

For `m=1,2,3,4`, the first `2m` primes in the fixed shell produce an origin
above `B=10^6` whose positive and negative mask profiles are separated.  The
raw adjacent coefficient is exactly `T_1 P_-`; this is a proxy obstruction,
not a normalized growing theorem or arithmetic sign result.

The project producer, reverse-order independent checker, strict mutation
stress test, PDF artifacts, and this bridge checker are hash-locked.  The
official Route-A/Route-B evaluator files are absent, so this is local
fail-closed repository evidence only.
