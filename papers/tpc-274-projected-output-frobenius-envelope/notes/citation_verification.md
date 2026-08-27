# Citation verification

The only new analytic ingredient is the finite-dimensional rowwise
Cauchy--Schwarz inequality, proved directly in `PROOF_PACKAGE.md`.  The
operator, source vector, masks, projection, and interval data are inherited
from the released TPC-268 certificate; the producer and independent replay
check the parent payload digest before using it.  Standard background sources
are listed in `paper/references.bib`; no external asymptotic theorem is used
to support the finite claim.
