# Proof package

`PROVED_EXACT_FINITE_CRT_PROXY_OBSTRUCTION`: for every finite set of distinct
primes `p_i>N` and every `B`, the displayed CRT congruences have a positive
solution `o>B`.  Since `0<=r<N<p_i`, the congruence `o=-N (mod p_i)` has no
zero in `o+r` for `0<=r<N`, while `o=0 (mod p_i)` has exactly the zero at
`r=0`.  The difference of the witness pair is `-1`, so the difference mask is
zero.  Substitution into the exact TPC-402 coefficient identity proves
`M_sigma(o,o+1)=T_1P_-`.

The code checks this theorem for four finite cases and records exact rational
values.  The result is not a normalized growing lower bound, not an arithmetic
sign theorem, and not a twin-prime result.
