# TPC-415 proof package

Pool the complete shells `Q=65536,131072,262144`, retaining 36848 primes and
using shell-local `a_i=p_i^3/[Q_i^2(p_i-1)]`.  For every
`H` in `{16,32,66,128}`, set `N=4H` and impose alternating CRT residues in the
pooled order.  Since the pool is even, `m_minus=m_plus=18424`.  Every prime
exceeds the largest `N=512`, so the local identities are

    G0=V_minus S0,  G1=V_minus S1+V_plus(S1-t1^2),  M=t1 P_minus.

Cauchy--Schwarz, `V_minus>=m_minus a_min^2`, `G1>=V_minus S1`, and
`S0,S1>=H/4` imply `0<=z<=t1/(a_min sqrt(S0 S1))<=4/H` at all four heights.
This is finite synthetic proxy evidence, not a full operator or arithmetic
theorem.
