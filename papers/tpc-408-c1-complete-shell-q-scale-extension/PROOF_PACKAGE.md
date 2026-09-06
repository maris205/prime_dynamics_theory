# TPC-408 proof package

## Theorem (finite complete-shell Q-scale extension)

Fix `H=66` and `N=264=4H`. Let `Q>N` and let the complete shell
`Q<p<=2Q` contain `r>=2` primes, ordered as `p_0<...<p_{r-1}`. No parity
assumption on `r` is made. Impose `o=0 (mod p_i)` for even `i` and
`o=-N (mod p_i)` for odd `i`, with `o` chosen above `10^6`. Put
`m_- = floor(r/2)`, `m_+ = ceil(r/2)`, and
`a_i=p_i^3/[Q^2(p_i-1)]`. With the TPC-404 local proxy definitions

    S_0=sum_{d=1}^{N-1} t_d^2,
    S_1=sum_{d=1}^{N-2} t_d^2+t_1^2,
    t_d=H^2/(H^2+d^2),

and `P_-`, `V_-`, `V_+` denoting the odd-index amplitude sum and the odd/even
square sums, the adjacent local row has

    G_0=V_- S_0,
    G_1=V_- S_1+V_+(S_1-t_1^2),
    M=t_1 P_-.

For `z=M/sqrt(G_0 G_1)` and `a_min=min_i a_i`,

    0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.

## Proof

Since `p_i>Q>N`, the even-index congruence masks offset zero and the
odd-index congruence first hits offset `N`; neither class masks offset one.
This gives the three displayed identities, independently of whether `r` is
even. The odd class has `m_->=1` terms. Cauchy--Schwarz gives
`P_-^2<=m_- V_-`, while `V_->=m_- a_min^2`; also
`G_1>=V_- S_1`. Hence

    z^2 <= t_1^2 m_-/(V_- S_0 S_1)
         <= t_1^2/(a_min^2 S_0 S_1).

For `1<=d<=H`, `t_d>=1/2`, and those terms occur in both sums, so
`S_0,S_1>=H/4`. Finally
`a_i=(p_i/Q)^2 p_i/(p_i-1)>1`. Taking square roots proves the claim.

The exact certificate instantiates this extension at the full shells
`Q=65536` and `Q=131072`, with respectively `5709` and `10749` primes.
Both are odd shells and are retained in full; the unequal index counts are
`2854/2855` and `5374/5375`. This is a finite single-entry proxy theorem,
not a growing or source-valid operator theorem.
