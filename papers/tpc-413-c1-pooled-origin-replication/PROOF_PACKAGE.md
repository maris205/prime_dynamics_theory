# TPC-413 proof package

Use the pooled complete shells `65536<p<=131072` and `131072<p<=262144`, with
shell-local `a_i=p_i^3/[Q_i^2(p_i-1)]`, alternating CRT residues, and
`H=16,32,66,128`, `N=4H`.  For each CRT period `L`, use the three distinct
representatives `o_s=r+sL`, `s=1,2,3`.  Every representative has identical
residues modulo every prime.  Thus the exact local identities and the pooled
counts `m_minus=m_plus=8229` are unchanged at all 12 rows:

    G0=V_minus S0,  G1=V_minus S1+V_plus(S1-t1^2),  M=t1 P_minus.

Cauchy--Schwarz, `V_minus>=m_minus a_min^2`, `G1>=V_minus S1`, and
`S0,S1>=H/4` give `0<=z<=t1/(a_min sqrt(S0 S1))<=4/H`.  The result is a
finite origin-replication audit of one synthetic proxy entry, not a physical,
arithmetic, full-operator, or twin-prime theorem.
