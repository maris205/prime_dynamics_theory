# TPC-233 source lock

## Arithmetic input

The proof uses the classical prime number theorem with a de la Vallee Poussin
zero-free-region error term

```text
pi(x) = Li(x) + O(x exp(-c sqrt(log x))).
```

This is used only to place primes in two relative intervals of width `1/(2L)` when
`L~log Q/loglog Q`.  The bare asymptotic PNT would not by itself justify this shrinking
window subtraction.

Standard references:

- H. Davenport, *Multiplicative Number Theory*, 3rd ed., Springer, 2000.
- H. L. Montgomery and R. C. Vaughan, *Multiplicative Number Theory I: Classical
  Theory*, Cambridge University Press, 2007.
- H. Iwaniec and E. Kowalski, *Analytic Number Theory*, AMS, 2004.

## Internal source lock

- TPC-226 supplies the exact dilated-clock support.
- TPC-230 supplies the row-mass comparability transfer.
- TPC-232 identifies critical depth as the first range not excluded by incidence
  density.

The primorial clock is a modeled adversarial family.  No actual V59 coefficient is
identified with uniform atom mass.
