# RH-35: exact packet-pair physical count

This paper removes the final stored-coordinate caveat left by RH-34 at
sigma = 1e-2.

For the exact stored packet arrays, ordinary binary64 construction gives a
tiny but nonzero dyadic defect

\[
G=WV\ne I_4,\qquad
\|G-I_4\|_F\le 6.501\times10^{-16}.
\]

Because this bound is below one, the exact rational correction

\[
\widehat W=G^{-1}W
\]

exists and satisfies \(\widehat W V=I_4\) exactly.  With
\(\widehat Q=I-V\widehat W\), the corrected blocks are an exact oblique
packet/complement representation of the stored Perron/parity-extracted
physical two-step matrix \(U^2\).

The RH-27 componentwise factor graph and the RH-33 949-leaf resolvent atlas
give

\[
\max_\Gamma q_B\le 3.768\times10^{-9}<1
\]

for the stored-to-corrected complement homotopy.  The complete RH-28
Feshbach remainder is included leafwise, giving

\[
\max_\Gamma q_F\le 0.547185<1.
\]

Therefore

\[
N_\Gamma(\widehat B)=0,\qquad
\operatorname{wind}_\Gamma\det\widehat F=1.
\]

The exact coordinate determinant identity is

\[
z^4\det(zI-U^2)
=\det(zI-\widehat B)\det\widehat F(z).
\]

Since zero lies outside the counting circle, the main theorem is

\[
\boxed{N_\Gamma(U^2)=1}.
\]

This is a theorem for one exact finite stored binary64 discretization.  It
does not prove a continuum or zero-noise limit and makes no statement about
zeta zeros, Hilbert--Pólya, or the Riemann hypothesis.

## Fast verification

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
MPLBACKEND=Agg python experiments/make_figures.py
python experiments/verify_archive.py
~~~

## Rebuild the rigorous certificate

~~~bash
OPENBLAS_NUM_THREADS=32 OMP_NUM_THREADS=32 \
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/run_packet_pair_certificate.py \
  --sigma 0.01 --chunk-size 256
~~~

The formal manuscript is exact-packet-pair-physical-count.pdf.
