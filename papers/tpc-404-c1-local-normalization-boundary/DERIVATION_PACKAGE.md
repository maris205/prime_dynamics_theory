# Derivation package

Let `a_p=p^3/[Q^2(p-1)]` be the TPC-403 coefficients, with even-index primes positive and
odd-index primes negative.  The CRT masks give `p|o` for positive primes and
`p∤o,o+1` for negative primes.  At `o`, each positive row is deleted and each
negative row contributes the full off-diagonal energy `S_0`; hence
`G(o)=V_minus S_0`, where `V_minus=sum_{odd i}a_{p_i}^2` and
`V_plus=sum_{even i}a_{p_i}^2`.

At `o+1`, every selected prime is a unit.  Each negative row contributes
`S_1`, while a positive row has its `d=1` contribution removed because its
row was deleted at `o`, giving `S_1-T_1^2`.  Summing squared row amplitudes
gives `G(o+1)=V_minus S_1+V_plus(S_1-T_1^2)`.

TPC-403 gives the signed adjacent coefficient
`M(o,o+1)=T_1 P_minus`.  Division by the two positive local diagonal energies
therefore yields the exact normalized square
`(T_1P_minus)^2/(G(o)G(o+1))`.

All assertions above are finite identities under the declared CRT masks.
