# TPC-315 citation verification

TPC-315 uses the same deliberately modest arithmetic motivation as TPC-314;
the citations motivate labels for a finite menu, not a canonical choice or a
twin-prime theorem.  The following sources were checked on 2026-08-30:

1. Marco Cantarini, *Explicit formula for the average of Goldbach and prime
   tuples representations*, arXiv:1801.08475.  Its prime-tuple discussion
   uses the von-Mangoldt convention:
   <https://arxiv.org/abs/1801.08475>.
2. Szilárd Gy. Révész, *A Riemann-von Mangoldt-type formula for the
   distribution of Beurling primes*, arXiv:2110.11463.  The prime-element
   value of the corresponding von-Mangoldt function is the logarithm:
   <https://arxiv.org/abs/2110.11463>.
3. William Banks, Kevin Ford, and Terence Tao, *Large prime gaps and
   probabilistic models*, Inventiones Mathematicae 233 (2023), 1471--1518,
   DOI <https://doi.org/10.1007/s00222-023-01199-0>.  Its sieve discussion
   supplies context for coprimality-density notation; `phi(p)=p-1` is
   elementary.

The physical engine, source coefficients, and fresh target labels are local
finite constructions.  No cited source is used as an external data feed or
as an asymptotic proof.
