# TPC-409 proof package

## Theorem (finite odd complete-shell height ladder)

Fix `Q=65536`. For each `H` in `{16,32,66,128}`, set `N=4H` and retain all
primes in the complete shell `Q<p<=2Q`. The shell has `r=5709` primes, so
`m_-=floor(r/2)=2854` odd-index terms and `m_+=ceil(r/2)=2855` even-index
terms. Impose `o=0 (mod p_i)` for even `i` and `o=-N (mod p_i)` for odd `i`,
with `o>10^6`. Define `t_d=H^2/(H^2+d^2)`,
`S_0=sum_{d=1}^{N-1}t_d^2`, `S_1=sum_{d=1}^{N-2}t_d^2+t_1^2`, and
`a_i=p_i^3/[Q^2(p_i-1)]`. Then the complete-shell local proxy has

    G_0=V_- S_0,  G_1=V_- S_1+V_+(S_1-t_1^2),  M=t_1 P_-,

and `z=M/sqrt(G_0 G_1)` satisfies

    0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.

## Proof

Every shell prime exceeds `Q>N`. Therefore the even CRT class masks offset
zero, the odd class first masks offset `N`, and no class masks offset one.
This gives the three local identities for every declared height. Since
`m_->=1`, Cauchy--Schwarz gives `P_-^2<=m_-V_-`, while
`V_->=m_-a_min^2`; also `G_1>=V_-S_1`. Hence

    z^2 <= t_1^2 m_-/(V_- S_0 S_1)
         <= t_1^2/(a_min^2 S_0 S_1).

The terms `1<=d<=H` occur in both sums and have `t_d>=1/2`, giving
`S_0,S_1>=H/4`. Finally `a_i=(p_i/Q)^2p_i/(p_i-1)>1`. Taking square roots
proves the claim. The four certificate rows are exact finite instances of
this theorem; they do not establish a growing or full-operator result.
