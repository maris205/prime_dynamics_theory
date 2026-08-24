# TPC-231 source lock

## Classical engine

The only external analytic engine is the classical Selberg upper-bound sieve for a
dimension-two polynomial/linear-form sequence with interval remainder
`A_d=X nu(d)/d+O(nu(d))`.

Locked references:

1. H. Halberstam and H.-E. Richert, *Sieve Methods*, Academic Press, 1974,
   Chapter 5.
2. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, AMS Colloquium
   Publications 53, 2004, Chapter 6.
3. Ben Green, *Additive Combinatorics*, Section 2.3, official Oxford notes:
   <https://people.maths.ox.ac.uk/greenbj/papers/additive-combinatorics.pdf>.
   Proposition 2.2.4 gives the directly analogous uniform two-form upper bound with
   a determinant-prime correction.
4. Zeev Rudnick, *Selberg's Sieve---Twin Primes*, course notes, 2015:
   <https://www.math.tau.ac.il/~rudnick/courses/sieves2015/selberg%20sieve%20twin%20primes.pdf>.
   Theorem 1.1 supplies the upper-bound sieve form and Theorem 1.2 its dimension-two
   twin-prime specialization.

## Derived here, not imported

- the `Q=3t+a` parameterization;
- determinant `16Q`;
- special local behavior at `2`, `3`, and `7`;
- the exact singular-series factor `(ell-1)/(ell-2)` at `ell|Q`;
- the fixed-finite-resonance-family extension;
- the transfer through TPC-230's matched-mass ceiling.

## Firewall

The references justify an upper-bound sieve, not a lower bound for prime pairs and not
signed cancellation. PNT is used only to normalize by the prime-shell size. No finite
experiment is used in the asymptotic proof.
