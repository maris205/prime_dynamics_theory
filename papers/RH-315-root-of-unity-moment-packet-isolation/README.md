# RH-315: Root-of-unity moment packet isolation

For a nonzero real target moment `w`, order `d`, and integer multiplicity `L`, take
all roots of

    z^d = w/(dL),

each repeated `L` times.  The packet is conjugate closed, has zero power sums
below order `d`, and has power sum exactly `w` at order `d`.  Its higher
multiple moments are

    p_(md) = w^m/(dL)^(m-1).

Choosing `L >= |w|/(d q^d)` places every root in `|z|<=q`.  This is a genuine
finite normal spectrum packet, but it is a synthetic algebraic object rather
than the actual noisy spectrum.  Gates A--E remain false/open.

When `w=0`, no packet is needed.
