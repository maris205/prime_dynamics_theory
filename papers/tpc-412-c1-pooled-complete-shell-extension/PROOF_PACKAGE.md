# TPC-412 proof package

Pool the complete shells `65536<p<=131072` and `131072<p<=262144`, retaining
`16458` primes.  For each prime use `a_i=p_i^3/[Q_i^2(p_i-1)]`, where `Q_i`
is its source shell, and impose alternating CRT residues in the pooled order.
For each `H` in `{16,32,66,128}`, set `N=4H`.  The pooled even cardinality gives
`m_minus=m_plus=8229`; the exact local identities are

    G0=V_minus S0,  G1=V_minus S1+V_plus(S1-t1^2),  M=t1 P_minus.

Cauchy--Schwarz gives `P_minus^2<=m_minus V_minus`, while
`V_minus>=m_minus a_min^2` and `G1>=V_minus S1`.  Since `S0,S1>=H/4` and
`a_i>1`,

    0 <= z <= t1/(a_min sqrt(S0 S1)) <= 4/(a_min H) <= 4/H.

The certificate and independent literal replay establish only this finite
four-height synthetic proxy extension, not a full operator or arithmetic
theorem.
