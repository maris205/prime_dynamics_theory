# Roadmap after RH-165

For normal blocks, contour selection is no longer open: use the midpoint
circle and test `2 sqrt(bc) < gap`.  The physical operator is nonnormal, so
this theorem is a benchmark and a falsifier, not the final certificate.

The next paper should formulate the packet and dual packet residuals that
produce `b` and `c` directly from a candidate frame.  It should also separate
the primal Riesz graph slope from the dual slope; a global projector norm can
hide useful one-way conditioning.
