# Roadmap after RH-257

Continuous signed fitting is too permissive: all 32 finite jets can be fit,
but the weights are fractional and often enormous, so the induced product is
multivalued around reciprocal roots.  The next legitimate finite relaxation
is the bounded integer lattice, interpreted only as a necessary determinant-
quotient condition, not yet as an operator realization.

Route coordinate:

```text
fractional_signed_fits_monodromy_illegal_open_bounded_integer_quotient_lattice
```

RH-258 should audit small signed caps and report either an integer candidate
or a scoped lattice obstruction.  Gates A--E remain false/open.
