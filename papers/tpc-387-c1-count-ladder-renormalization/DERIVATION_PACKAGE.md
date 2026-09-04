# TPC-387 derivation package

For the finite kernel `K_p` and square-energy geometry `G` used in TPC-386,
form the local or pooled normalized masked matrix `B_{N}` at each declared
count. The pooled training scalar at `N=512` and `N=768` is the mean of `G`
over the three calibration origins at that count. Its `N=1024` denominator is
the log-count extrapolation of those two geometry scalars.

For each fixed tuple `(band mode, normalization, law, Q)`, let `S_512` and
`S_768` be the means of the spectral diagnostic over calibration origins. The
finite calibration slope is

\[
 \alpha = \frac{\log(S_{768}/S_{512})}{\log(768/512)},
 \qquad
 \widehat S_{1024}=S_{768}(1024/768)^\alpha .
\]

The holdout statistic is `S_1024 / \widehat S_1024`; its deviation from one
is recorded before any interpretation. This is a two-point interpolation/
extrapolation device, not an asymptotic derivation. The exact `Q=8`,
13-point anchor proves only positive geometry and symmetry by rational
arithmetic; all larger values are finite floating-point observations.
