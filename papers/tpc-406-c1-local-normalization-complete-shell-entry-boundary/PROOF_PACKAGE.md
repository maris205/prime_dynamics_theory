# Proof package

## Theorem (complete-shell adjacent-entry proxy boundary)

Let `H,N,Q` be integers with `H>=1`, `N>=H+2`, and `Q>N`.  Assume the
complete shell `(Q,2Q]` has even cardinality `2m`, and let
`p_0<...<p_{2m-1}` be every prime in that shell, so that `m=436` for
`Q=8192`.  Impose the CRT residues `o=0 (mod p_i)` for even `i`
and `o=-N (mod p_i)` for odd `i`, and choose any CRT representative above a
prescribed lower bound.  Put `t_d=H^2/(H^2+d^2)`,
`S_0=sum_{d=1}^{N-1}t_d^2`, and
`S_1=sum_{d=1}^{N-2}t_d^2+t_1^2`.  For
`a_i=p_i^3/[Q^2(p_i-1)]`, define `P_-`, `V_-`, and `V_+` by odd/even
indices.  In the selected-prime local proxy,

    G_0=V_-S_0,  G_1=V_-S_1+V_+(S_1-t_1^2),  M=t_1P_-.

If `z=M/sqrt(G_0G_1)` and `a_min=min_i a_i`, then

    0 <= z <= t_1/(a_min sqrt(S_0S_1)) <= 4/(a_min H) <= 4/H.

## Proof

The complete shell is still a finite selected-prime profile, so the
TPC-404 mask calculation gives the displayed formulas.  Positivity gives
`z>=0`, and `S_1-t_1^2>=0` gives `G_1>=V_-S_1`.  Cauchy--Schwarz gives
`P_-^2<=mV_-`; the `m` odd-indexed amplitudes give
`V_->=m a_min^2`.  Hence

    z^2 <= t_1^2/(a_min^2 S_0S_1).

For `1<=d<=H`, `t_d>=1/2`.  Since `N>=H+2`, these terms occur in both
finite sums, so `S_0,S_1>=H/4`.  Finally `p_i>Q` implies
`a_i=(p_i/Q)^2 p_i/(p_i-1)>1`.  Taking square roots proves the result.

The five certificate rows are an exact finite complete-shell audit of this
identity.  They do not turn the one-entry proxy theorem into a full
operator, source, or arithmetic theorem.
