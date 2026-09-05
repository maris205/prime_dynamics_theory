# Proof package

## Theorem (uniform adjacent-entry proxy bound)

Let H,N,Q be integers with H>=1, N>=H+2, and Q>N. Let
p_0<...<p_{2m-1} be distinct primes in (Q,2Q], with m>=1, and let o be any
CRT solution above a prescribed lower bound satisfying o=0 (mod p_i) for even
i and o=-N (mod p_i) for odd i. Set t_d=H^2/(H^2+d^2),
S_0=sum_{d=1}^{N-1}t_d^2, and S_1=sum_{d=1}^{N-2}t_d^2+t_1^2.
For a_i=p_i^3/[Q^2(p_i-1)], define P_- = sum_{i odd}a_i,
V_- = sum_{i odd}a_i^2, and V_+ = sum_{i even}a_i^2. In the TPC-404
selected-prime local proxy, G_0=V_-S_0, G_1=V_-S_1+V_+(S_1-t_1^2),
and M=t_1P_-. If z=M/sqrt(G_0G_1) and a_min=min_i a_i, then

    0 <= z <= t_1/(a_min sqrt(S_0S_1)) <= 4/(a_min H) <= 4/H.

## Proof

All amplitudes and t_d are positive, so z>=0 and the two energies are
positive. Since S_1-t_1^2=sum_{d=1}^{N-2}t_d^2>=0, G_1>=V_-S_1.
Cauchy--Schwarz gives P_-^2<=mV_-, while the m odd indices give
V_->=m a_min^2. Thus

    z^2 <= t_1^2(mV_-)/[(V_-S_0)(V_-S_1)]
         =  t_1^2 m/(V_-S_0S_1)
         <= t_1^2/(a_min^2 S_0S_1).

For 1<=d<=H, t_d>=1/2. Since N>=H+2, these terms occur in both finite
sums, so S_0,S_1>=H/4. Also
a_i=(p_i/Q)^2 p_i/(p_i-1)>1 because p_i>Q. Taking square roots proves the
sharp and coarse bounds. No asymptotic or source-identification step is used.

The theorem is PROVED_UNIFORM only for the single selected-prime adjacent
proxy entry. It says nothing about the full operator norm or the arithmetic
source.
