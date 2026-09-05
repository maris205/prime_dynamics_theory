# Derivation package

TPC-405 already supplies the local masked-energy calculation.  Selecting all
872 primes in the shell changes only the profile cardinality: `m=436`.

`G_0=V_-S_0`, `G_1=V_-S_1+V_+(S_1-t_1^2)`, and `M=t_1P_-`.  Since
`G_1>=V_-S_1`, `P_-^2<=mV_-`, and `V_->=m a_min^2`,

    z^2 <= t_1^2/(a_min^2 S_0 S_1).

The kernel terms `d=1,...,H` occur in both sums and satisfy `t_d>=1/2`, so
`S_0,S_1>=H/4`.  Shell membership gives `a_i>1`.  Thus the complete-shell
profile obeys `z<=4/(a_min H)<=4/H` exactly.  The certificate checks five
heights; it is evidence for the finite instantiation, not an asymptotic claim.
