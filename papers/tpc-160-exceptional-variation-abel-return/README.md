# TPC-160: Exceptional-variation Abel return

Paper title:

> *Exceptional-Variation Abel Return:
> Literal Weights, Almost-Prefixes, and the Atomic All-Prefix Barrier*

TPC-159 bounds cumulative periodic-core sums at every endpoint outside
the low range and the dyadic exceptional shadow. This paper inserts
that prefix theorem into exact Abel summation.

For ordered fiber points `t_1 < ... < t_m <= T`, let

```text
sigma_i = mu(d+s*z_i) mu(u+a*z_i) rho(z_i),
A_i = sum_{j <= i} sigma_j,
d_i = w_i-w_(i+1),  i<m,
d_m = w_m.
```

Then

```text
sum sigma_i*w_i = sum A_i*d_i.
```

Splitting the variation of `w` according to whether `t_i` lies
outside or inside the dyadic bad set gives

```text
(q/T)|sum sigma_i*w_i|
 << ||rho||_infinity [
      epsilon_X*V_good(w)
      +(1+q/T)*V_bad(w)
    ],

epsilon_X = (log X)^(-kappa_0)+2^(-J)+q/T.
```

This is a proved weighted almost-endpoint interface. A decaying
literal physical estimate additionally requires a source-locked
physical weight with controlled good variation and small bad
variation. The stated logarithmic promotion also assumes the terminal
scale lies in `2^J*sqrt(X) <= T <= X`, so the `q/T` normalization term
is super-logarithmically small. That production input remains
`NOT_TESTABLE`.

For the prefix cutoff `w_i=1_(i<=k)`, the Abel derivative is exactly
one atom at `t_k`. Consequently, this route controls every literal
prefix only if the actual endpoint registry avoids the dyadic bad set,
or if an additional pointwise theorem covers the bad endpoints.
Continuous exceptional-set density cannot establish this atomic
avoidance.

No full physical H3 return, fixed-X power saving, `1/400`,
prime-pair lower bound, or twin-prime theorem is claimed.

Reproduce:

```powershell
python experiments/tpc160_abel_return_audit.py
python experiments/tpc160_abel_return_audit.py --check
```
