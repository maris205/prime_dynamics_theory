# TPC-233 proof package

## Theorem

Let the TPC-226/232 support at depth `L` be

\[
S_{q,L}=\{mq^{-1}\pmod{4LQ}:0<|m|\le\lfloor Lq/Q\rfloor,
(m,4LQ)=1\}.
\]

There is a sequence `L->infinity`, `Q=Q_L`, satisfying

\[
L\sim\frac{\log Q}{\log\log Q},
\]

and primes `p,r` in `(Q,2Q)` for which

\[
|S_{p,L}|=2,
\qquad
|S_{r,L}|=2\{1+\pi(2L-1)-\pi(L)\}.
\]

Therefore the raw row comparability constant diverges at least as
`(1+o(1))L/log L`.  For every admissible clock it is at most `2L-1`.

## Status

`PROVABLE AS STATED / PROVED_ARITHMETIC_OBSTRUCTION_L1` in the declared modeled
clock.  The use of a classical PNT remainder is the source-backed arithmetic input.

## Proof

### Step 1: universal bound

For every prime row `Q<q<2Q`, its cutoff `R_q=floor(Lq/Q)` lies in
`[L,2L-1]`.  The multiplier `1` is primitive, so `|S_{q,L}|>=2`.  Internal
injectivity holds in the short-multiplier regime, and there are at most `2R_q`
signed multipliers.  Hence

\[
2\le |S_{q,L}|\le2(2L-1).
\]

The ratio of maximum to minimum support size is therefore at most `2L-1`.

### Step 2: a critical primorial clock

Write `theta(L)=sum_(prime ell<=L) log ell` and define

\[
P_L=\prod_{\ell\le L}\ell,
\qquad
j_L=\left\lfloor\frac{L\log L-\theta(L)}{\log2}\right\rfloor,
\qquad
Q_L=2^{j_L}P_L.
\]

The prime number theorem gives `theta(L)~L`, so `j_L` is nonnegative for all large
`L`.  The floor changes the logarithm by less than `log 2`, and thus

\[
\log Q_L=L\log L+O(1).
\]

Taking another logarithm gives

\[
\frac{\log Q_L}{\log\log Q_L}
=\frac{L\log L+O(1)}{\log L+\log\log L+o(1)}\sim L.
\]

Every prime divisor of `Q_L` is at most `L`.

### Step 3: low and high shell primes

The classical zero-free-region form of the PNT gives, for some `c>0`,

\[
\pi(x)=\operatorname{Li}(x)+O(xe^{-c\sqrt{\log x}}).
\]

Take `x=Q_L` and `y=Q_L/(2L)`.  Since `L~log Q_L/loglog Q_L`,

\[
L\log Q_L\,e^{-c\sqrt{\log Q_L}}\to0.
\]

The main term `y/log Q_L` therefore dominates the difference of the two error
terms.  For all large `L`, there is a prime

\[
Q_L<p_L<Q_L+Q_L/(2L).
\]

Applying the same argument to the interval immediately below `2Q_L` gives a prime

\[
2Q_L-Q_L/(2L)<r_L<2Q_L.
\]

The strict inequalities imply

\[
\left\lfloor\frac{Lp_L}{Q_L}\right\rfloor=L,
\qquad
\left\lfloor\frac{Lr_L}{Q_L}\right\rfloor=2L-1.
\]

### Step 4: exact support separation

Put `h_L=4LQ_L`.  If `2<=m<=L`, then `m` has a prime divisor at most `L`, which
divides `Q_L`; hence `(m,h_L)>1`.  Thus the only positive primitive multiplier up
to `L` is `1` and `|S_{p_L,L}|=2`.

Now let `L<m<2L`.  If `m` is composite, it has a prime divisor at most
`sqrt(m)<sqrt(2L)<L` for `L>=3`, so it is not primitive.  If `m` is prime, then
`m>L`; it divides neither `Q_L` nor `4L`, so it is primitive.  Therefore the
positive primitive multipliers up to `2L-1` are exactly `1` and the primes in
`(L,2L)`.  This proves

\[
|S_{r_L,L}|=2\{1+\pi(2L-1)-\pi(L)\}.
\]

The PNT on `(L,2L)` gives the claimed asymptotic ratio and divergence.  This also
shows that a fixed row-mass comparability constant cannot be deduced from clock
geometry, even at critical depth.  ∎

## Proof audit

- The narrow prime windows are justified by the explicit classical PNT error, not by
  the bare statement `pi(x)~x/log x`.
- The construction concerns raw uniform-atom support mass only.
- It refutes automatic fixed comparability, not the possibility of source-valid row
  normalization.
