# RH-362: Prime-return Euler dichotomy and clock-renormalization obstruction

RH-362 is the first numbered theorem paper after the four-volume synthesis of
RH-1--RH-361.  It is an independent trigger-5 arithmetic-dynamical branch; it
does not replace, renumber, or modify the four-volume foundation, and it does
not close the still-open physical route

```text
actual_same_clock_unnormalized_head_transport_open.
```

For

```text
H(x,y) = (1-6x^2-y,x)
```

and an integral point `P`, let `r_p(P)` be the return period of `P mod p`.
The source theorem gives

```text
p | a_n(P)  iff  r_p(P) | n,
```

where `a_n(P)` is the gcd of the two coordinate differences after `n`
iterates.  RH-362 derives the following all-prime consequences.

- For a nonperiodic integral orbit, the primes with `r_p(P)<K` are exactly
  the prime divisors of `prod_(n<K) a_n(P)`.  Hence `r_p(P)->infinity`
  outside a finite set at every fixed threshold.
- The pointed orbit of `P mod p` is one cycle with permutation matrix `U_p`,
  and

      det(I-z U_p) = 1-z^(r_p).

- The countable pointed-cycle bouquet has finite fixed-point counts in every
  order and the formal Artin--Mazur product

      prod_p (1-z^(r_p))^(-1).

- The Dirichlet Euler product

      Z_P(s) = prod_p (1-p^(-s r_p))^(-1)

  converges normally on every closed half-plane `Re(s)>=delta>0`; it is
  holomorphic and zero-free on `Re(s)>0`.
- Its Dirichlet coefficients are multiplicative `0/1` values, and its
  logarithmic derivative is supported at `p^(j r_p)` with weight
  `r_p log p`, not the von Mangoldt weight `log p`.
- The natural cycle-block operator is compact on `Re(s)>0` and is proved
  trace class for `Re(s)>3`, where its Fredholm determinant equals
  `Z_P(s)^(-1)`.  The scalar continuation below that region is not promoted
  to an ordinary Fredholm determinant.
- For nonperiodic `P`, weighting each block by `p^(-s/r_p)` forces the scalar
  Euler product for `zeta(s)`, but deletes the return length from every local
  factor.  The resulting block operator belongs to no finite Schatten class
  on any positive half-plane.  This is a rigorous clock-renormalization
  obstruction, not a bridge.

The periodic comparison is also exact: if an integral point has exact period
`N`, then all but finitely many `r_p` equal `N`, so the return Euler product is
`zeta(Ns)` times a finite Euler correction.  This injects zeta through the
almost-constant local periods and prime labels; it is not a spectral recovery
of Riemann zeros.

For the concrete seed `P=(0,0)`, the first coordinates are

```text
0, 1, -5, -150, -134994, ...
```

and a negative-cone induction proves strict escape and hence nonperiodicity.

## Foundation and claim boundary

The four provenance-preserving volumes remain the durable base:

```text
Volume I    RH-1--RH-160
Volume II   RH-161--RH-241
Volume III  RH-242--RH-281
Volume IV   RH-282--RH-361
```

The artifact hard-locks the outer four-volume manifest and verification:
four volumes, 361 numbered sources, 73 archive members, 1,548 dependency
hashes, eight result hashes, and zero replay failures.  Their SHA-256 seals
are respectively
`24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897`
and
`b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751`.

RH-362 touches none of the original physical triggers 1--4.  Gates A--E
remain false/open.  The pointed bouquet is not the zeta function of the full
finite-field maps, not a Hasse--Weil zeta function, not the actual noisy
determinant, and not a Hilbert--Polya construction.  No Riemann-zero spectral
identification, completed-zeta divisor equality, von Mangoldt trace theorem,
or proof of RH is claimed.

## Reproduction

```bash
make result
make test
make pdf
make archive
```

Finite rows reproduce exact modular-return and cycle-matrix identities only;
they are not evidence for an all-prime distribution law.
