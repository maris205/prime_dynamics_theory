# TPC-416 proof package

Pool the complete shells `Q=65536,131072,262144,524288`, retaining
`5709+10749+20390+38635=75483` primes.  Use shell-local
`a_i=p_i^3/[Q_i^2(p_i-1)]`, alternating CRT residues, `H=66`, and `N=264`.
The odd pooled cardinality gives `m_minus=37741` and `m_plus=37742`.
Every prime exceeds `N`, so

    G0=V_minus S0,  G1=V_minus S1+V_plus(S1-t1^2),  M=t1 P_minus.

Cauchy--Schwarz, `V_minus>=m_minus a_min^2`, `G1>=V_minus S1`, and
`S0,S1>=H/4` imply `0<=z<=t1/(a_min sqrt(S0 S1))<=4/H`.  This is one
finite four-shell synthetic proxy entry with explicit odd parity, not a full
operator or arithmetic theorem.
