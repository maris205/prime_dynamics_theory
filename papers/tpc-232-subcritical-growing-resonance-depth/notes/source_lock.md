# TPC-232 source lock

## Repository source

- TPC-226 defines the exact primitive dilated-clock row
  \(h=4LQ\), cutoff \(\lfloor Lq/Q\rfloor\), and labels the clock
  `MODELING_CHOICE`.
- TPC-230 proves the unmatched-mass saving ceiling.
- TPC-231 supplies the fixed-form Selberg local-density compiler.

## External analytic engine

The only imported analytic engine is the classical Selberg upper-bound sieve
for a dimension-two sequence with

\[
A_d=X\nu(d)/d+O(\nu(d)).
\]

Locked references:

1. H. Halberstam and H.-E. Richert, *Sieve Methods*, Chapter 5, 1974.
2. H. Iwaniec and E. Kowalski, *Analytic Number Theory*, Chapter 6, 2004.
3. Ben Green, *Additive Combinatorics*, Section 2.3:
   <https://people.maths.ox.ac.uk/greenbj/papers/additive-combinatorics.pdf>.
4. Zeev Rudnick, *Selberg's Sieve---Twin Primes*:
   <https://www.math.tau.ac.il/~rudnick/courses/sieves2015/selberg%20sieve%20twin%20primes.pdf>.

TPC-232 derives the coefficient uniformity from the explicit interval remainder
and chooses a sieve level below a fixed power of the parameter interval.  It
does not cite a fixed-coefficient theorem as if its constant were uniform.

## Firewall

The source supports an upper bound only.  It supplies neither a critical-depth
lower bound nor a V59 clock/source identification nor signed cancellation.
