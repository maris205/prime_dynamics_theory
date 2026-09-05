# Proof package

## Proposition (finite local normalization identity)

For the declared TPC-403 CRT profile, with `N<Q<p`, adjacent points `o,o+1`,
and `T_d=H^2/(H^2+d^2)`, put `V_minus=sum_{odd i}a_{p_i}^2`,
`V_plus=sum_{even i}a_{p_i}^2`, and `P_minus=sum_{odd i}a_{p_i}`.
For the selected-prime proxy, define
`G(u)=sum_p a_p^2 1_{p∤u} sum_{v in I_o, v!=u}1_{p∤v}T_{u-v}^2`.
The local energies satisfy

```text
G(o)=V_minus S_0,
G(o+1)=V_minus S_1+V_plus(S_1-T_1^2),
M(o,o+1)=T_1P_minus.
```

Therefore the squared locally normalized coefficient equals
`(T_1P_minus)^2/(G(o)G(o+1))`.

## Proof

The CRT congruences imply that an even-index prime divides `o` and no
other point in the window, while an odd-index prime first divides the exterior
point `o+N`; consequently all selected primes are units at `o+1`.  A deleted
row contributes zero at its deleted diagonal point.  At `o`, exactly the
negative rows remain, and each has the same translated off-diagonal sum `S_0`.
At `o+1`, every negative row has the translated sum `S_1`; each positive row
loses precisely the `d=1` term coming from `o`, so its sum is `S_1-T_1^2`.
Multiplying by the squared row amplitudes and summing proves the two energy
identities.  The TPC-403 signed coefficient identity gives the displayed
formula for `M(o,o+1)`.  Squaring and dividing proves the final identity.

This proof is `PROVED_EXACT_FINITE`; it contains no limit in `Q`, `N`, or the
origin and makes no assertion about the arithmetic source signs.  A small
normalized entry is not an upper bound on the full normalized operator norm;
unselected shell primes and arbitrary origins are outside this statement.
