# RH-34: interior complement pole count

This paper closes the interior complement pole-count gate left open by RH-33
for the exact finite operator defined by the stored binary64 factors at
`sigma = 1e-2`.

A floating complex Schur decomposition supplies arbitrary stored matrices
`Z` and `T_ref = triu(T)`.  It is not itself used as a proof.  The RH-27
componentwise factor graph certifies, against the exact stored complement
`B`,

\[
\|BZ-ZT_{\rm ref}\|_F\le 9.553\times10^{-10},\qquad
\|Z^*Z-I\|_F\le 5.331\times10^{-9}.
\]

Thus `Z` is rigorously invertible.  Transporting every one of the 949 RH-33
resolvent leaves through the exact similarity gives a worst boundary
homotopy product

\[
q_{\max}\le 7.653\times10^{-4}<1.
\]

The exact binary64 diagonal of the stored upper-triangular reference has all
2048 entries outside the counting circle and none on its boundary.  Hence

\[
N_\Gamma(B)=0.
\]

Combining this with the RH-33 exact relative count and winding gives

\[
N_\Gamma(\mathcal M_{\rm st})=1,
\qquad
\operatorname{wind}_\Gamma\det F=1,
\]

with no interior complement poles.  Equivalently, the stored Feshbach
determinant has exactly one interior zero counted with multiplicity.

The scope is deliberately finite and explicit.  This is not a continuum
limit, a theorem about zeta zeros, a Hilbert--Pólya construction, or a claim
about the Riemann hypothesis.

## Fast verification

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
MPLBACKEND=Agg python experiments/make_figures.py
python experiments/verify_archive.py
~~~

## Rebuild the full certificate

The ignored workspace stores the 2048-dimensional Schur factors for local
reruns.  A complete rebuild is

~~~bash
OPENBLAS_NUM_THREADS=32 OMP_NUM_THREADS=32 \
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/run_schur_similarity_certificate.py \
  --sigma 0.01 --chunk-size 256
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
~~~

For a local repeat using the existing ignored Schur workspace, add
`--reuse-workspace`.

The formal manuscript is `interior-complement-pole-count.pdf`.
