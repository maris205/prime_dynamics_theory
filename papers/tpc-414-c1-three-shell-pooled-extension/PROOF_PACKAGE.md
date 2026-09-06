# TPC-414 proof package

Pool the complete shells with `Q=65536,131072,262144`, retaining
`5709+10749+20390=36848` primes.  For each prime use
`a_i=p_i^3/[Q_i^2(p_i-1)]`, order the pool increasingly, and impose alternating
CRT residues.  At `H=66,N=264`, the even pooled cardinality gives
`m_minus=m_plus=18424`.  Since every prime exceeds `N`,

    G0=V_minus S0,  G1=V_minus S1+V_plus(S1-t1^2),  M=t1 P_minus.

Cauchy--Schwarz, `V_minus>=m_minus a_min^2`, `G1>=V_minus S1`, and
`S0,S1>=H/4` imply `0<=z<=t1/(a_min sqrt(S0 S1))<=4/H`.  This is one
finite three-shell synthetic proxy entry, not a full operator or arithmetic
theorem.
