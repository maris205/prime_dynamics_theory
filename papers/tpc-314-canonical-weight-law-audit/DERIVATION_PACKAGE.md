# TPC-314 derivation package

Let I={321,...,640}, H=66, and let the frozen TPC-268 source rule at scale
640 supply rational coefficients beta_t.  For a prime p and exponent s in
{1,2}, the physical component is

    g_p(u) = sum_{t in I, t != u, p does not divide ut}
             p H^(2s)/(H^2+(u-t)^2)^s
             (1_{u == t mod p} - 1/(p-1)) beta_t.

For S_Q={p prime: Q<p<=2Q}, define the exact Gram matrix
G_{p,q}=sum_{u in I} g_p(u)g_q(u).  For a target sign vector c and a
positive weight vector w, TPC-314 audits

    E_w(c)=sum_{p,q} c_p c_q w_p G_{p,q} w_q,
    D_w=sum_p w_p^2 G_{p,p},
    R_w(c)=E_w(c)/D_w.

The three declared laws are

    w_p^count=1,   w_p^red=1/(p-1)=1/phi(p),   w_p^Lambda=log p.

The first law is counting measure.  The second records the elementary
reduced-residue normalization on a prime modulus.  The third is the
prime-support value of the von-Mangoldt convention Lambda(p)=log p.  These
are motivation labels, not a proof that one law is canonical.

For the logarithm, put k=floor(log_2 p), y=p/2^k, and
z=(y-1)/(y+1).  Then 1<=y<2, 0<=z<=1/3, and

    log p = k log 2 + 2 sum_{j=0}^{N-1} z^(2j+1)/(2j+1) + E_N(z),
    0 <= E_N(z) <= 2 z^(2N+1)/((2N+1)(1-z^2)).

The same series with z=1/3 encloses log 2; the release fixes N=120.
Every rational operation on these intervals, including the weighted numerator,
denominator, and quotient, is rounded outward to the grid 10^-36.

The target c^- is the exact minimum label inherited from TPC-312, while
c^+=(1,...,1) is a fixed control.  The result contains 8 rows, 3 laws, and
2 targets per law.  Exact interval comparisons certify the class relative to
one and the strict law order whenever adjacent intervals are disjoint.
