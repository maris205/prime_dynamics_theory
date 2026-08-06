# RH-369: Branch-symmetric Markov family and Möbius orthogonality

RH-369 derives a one-parameter, nonadaptive Markov/Gibbs family on the
four-state graph frozen by RH-366.  In the state order
\((--,-+,+-,++)\), let \(0<t<1\), \(q=1-t\), and

```text
P_t = [[t,0,q,0], [1,0,0,0], [0,t,0,q], [0,1,0,0]].
```

The family uses exactly the allowed edges of the RH-366 graph but is not
claimed to be selected by the Hénon geometry.  Its stationary law is

```text
pi_t = (1,q,q,q^2)/(1+q)^2.
```

For the inherited sign observable
\(\epsilon=(-1,-1,+1,+1)\),

```text
E_t epsilon = -t/(2-t),       Var_t epsilon = 4(1-t)/(2-t)^2.
```

After centering and variance normalization, the exact covariance table is

```text
Cov_t(F_t, F_t o sigma^(2k+1)) = 0,
Cov_t(F_t, F_t o sigma^(2k))   = (-(1-t))^k.
```

The chain is primitive and mixing for every fixed \(t\in(0,1)\).  The
RH-366 Chebyshev/Borel--Cantelli argument therefore gives, for each fixed
\(t\), a \(\nu_t\)-full set on which Möbius averages of every continuous
observable vanish.  The quantifiers are pointwise in \(t\): no common full
measure set or uniform estimate over the open parameter interval is claimed.

For the weighted variance

```text
S_{N,t} = sum_{n<=N} mu(n) F_t(sigma^n omega),
```

the exact finite identity is

```text
V_{N,t} = sum_{n<=N} mu(n)^2
          + 2 sum_{k>=1} (-(1-t))^k
              sum_{n<=N-2k} mu(n)mu(n+2k),
```

and \(0\le V_{N,t}\le ((2-t)/t)N\).  The limit
\(V_{N,t}/N\to6/\pi^2\) is retained only as a conditional statement under
ordinary fixed-shift two-point Chowla; it is not asserted unconditionally.

The Parry law of RH-366 is the single parameter \(t=\varphi^{-1}\), so this
paper strictly extends the covariance calculation to the non-Parry interior
family.  The endpoints are excluded: \(t=0\) is deterministic periodic and
\(t=1\) has zero raw variance.  As \(t\downarrow0\) the mixing rate tends to
one, and as \(t\uparrow1\) the normalized observable is singular.

## Route boundary

Route A is `GO`: the parameterized stationary laws, exact covariance,
fixed-parameter almost-sure Möbius orthogonality, and finite variance theorem
form an independent nonadaptive theorem package.  Route B is `STOP_SCOPED`:
the parameter \(t\) is externally selected and the symbolic Markov averages
are not a canonical arithmetic coupling, operator trace, prime-power trace,
determinant, or zeta-zero model.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The executable checks are exact rational identities at \(t=1/2,2/3,3/4\)
and finite Möbius prefixes.  They do not fit or prove a new asymptotic
constant.
