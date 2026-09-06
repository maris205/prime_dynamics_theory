# TPC-411 proof package

## Theorem (finite pooled complete-shell proxy)

Pool the two complete shells `65536<p<=131072` and
`131072<p<=262144`, retaining all `5709+10749=16458` primes.  For each
prime use its shell scale `Q_i` in `a_i=p_i^3/[Q_i^2(p_i-1)]`, order the
pooled primes increasingly, and impose CRT residues zero on even indices and
`-N` on odd indices.  With `H=66`, `N=264=4H`, and the TPC-404 local proxy,
define `S_0,S_1,P_-,V_-,V_+` as usual.  Since the pooled cardinality is even,
`m_-=m_+=8229`; the adjacent entry obeys

    G_0=V_-S_0,  G_1=V_-S_1+V_+(S_1-t_1^2),  M=t_1P_-,
    0 <= z=M/sqrt(G_0G_1) <= t_1/(a_min sqrt(S_0S_1)) <= 4/H.

## Proof

Every pooled prime exceeds `N`.  The even CRT class therefore masks offset
zero, the odd class first hits offset `N`, and no prime masks offset one.
This gives the displayed local identities.  Cauchy--Schwarz gives
`P_-^2<=m_-V_-`, while `V_->=m_-a_min^2`; also `G_1>=V_-S_1`.
The same cancellation and the bounds `S_0,S_1>=H/4`, `a_i>1` prove the
inequality.  The certificate is one exact finite pooled proxy row, not a
full operator or arithmetic theorem.
