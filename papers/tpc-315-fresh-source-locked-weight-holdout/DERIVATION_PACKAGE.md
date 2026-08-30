# TPC-315 derivation package

Let

    I={641,...,1280},       H=66,
    S_Q={p prime: Q<p<=2Q}, Q in {24,36,54,80}, s in {1,2}.

The locked TPC-268 source rule supplies rational coefficients `beta_t`.  For
each prime in a shell, define the deleted-diagonal physical output

    g_p(u) = sum_{t in I, t != u, p does not divide ut}
             p H^(2s)/(H^2+(u-t)^2)^s
             (1_{u == t mod p} - 1/(p-1)) beta_t.

The exact Gram matrix is

    G_(p,q) = sum_{u in I} g_p(u) g_q(u).

All physical quantities are rational.  The producer first materializes the
three TPC-314 laws on the declared shell, then computes the fresh Gram matrix
and enumerates signs.  Thus the law menu is procedurally fixed before the
fresh target labels are read.  This ordering is a finite anti-selection
protocol, not external statistical independence.

For a sign vector `c` and positive weight vector `w`, define

    E_w(c) = sum_(p,q) c_p c_q w_p G_(p,q) w_q,
    D_w    = sum_p w_p^2 G_(p,p),
    R_w(c) = E_w(c)/D_w.

The menu is

    C: w_p=1,
    R: w_p=1/(p-1)=1/phi(p),
    L: w_p=log(p).

For the logarithmic interval, set `k=floor(log_2 p)`, `y=p/2^k`, and
`z=(y-1)/(y+1)`.  Then `0<=z<=1/3` and

    log(p)=k log(2)+2 sum_(j=0)^(N-1) z^(2j+1)/(2j+1)+E_N(z),
    0 <= E_N(z) <= 2 z^(2N+1)/((2N+1)(1-z^2)).

TPC-315 fixes `N=120`.  The same enclosure at `z=1/3` supplies `log(2)`.
Every interval endpoint is rounded down/up to the common grid `10^-36`
after each rational operation.

The fresh target `c^-` is the exact minimum of `c^T G c / tr(G)` over all
sign classes with the first sign fixed to `+1`; the control `c^+` is the
all-positive vector, which the finite enumeration verifies is the maximum on
each row.  Gray-code updates enumerate exactly `2^(|S_Q|-1)` classes.  The
certificate records the unique extrema modulo global sign, modular Gram rank,
exact-rational digests, interval endpoints, and strict law orders.
