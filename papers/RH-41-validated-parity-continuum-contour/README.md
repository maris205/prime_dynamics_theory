# RH-41: Validated parity continuum contour

This paper closes the full-kernel continuum parity-isolation gate left open
by RH-40.

At the exact first band-merging parameter

\[
u_{\mathrm c}^3-2u_{\mathrm c}^2+2u_{\mathrm c}-2=0
\]

and fixed noise width sigma = 1/100, let K be the exactly normalized
folded-Gaussian Markov operator on L-infinity([0,1]). For

\[
c=-0.9865481927458079,\qquad r=0.05,
\]

the circle |z-c|=r lies in the resolvent set of K, contains exactly one
eigenvalue counted with algebraic multiplicity, and satisfies

\[
\sup_{|z-c|=r}\|(z-K)^{-1}\|_{L^\infty\to L^\infty}
\le 148.84153451786617.
\]

The unique enclosed eigenvalue is therefore real, negative, and
algebraically simple.

## Certificate chain

| gate | rigorous upper/product |
|---|---:|
| exact-stored Grushin residual | 4.587902979431811e-11 |
| exact-stored contour resolvent | 41.89853481734383 |
| stored to exact midpoint defect | 7.314948554132701e-06 |
| stored to Galerkin Neumann product | 0.06618141240061828 |
| 4096 to 8192 Schur product | 0.011027753039369056 |
| 8192 to 16384 Schur product | 0.002945448152785376 |
| Galerkin to continuum product | 0.649968453137824 |

The exact continuum-normalized midpoint family also has count one on the
same circle for every dimension n >= 32768; the resulting uniform lifted
L-infinity resolvent upper is 2192.043145718256.

## Proof layers

- A balanced rank-one Grushin border certifies one eigenvalue of the exact
  stored binary64 4096 matrix by a scalar Rouché argument.
- A 224-bit Arb ledger bridges every stored row to the exact critical
  parameter and exact continuum-normalized midpoint kernel.
- Cell-average conditional-expectation Galerkin matrices have exact coarse
  consistency and explicit L-infinity Haar block bounds.
- Two Schur steps and one finite-rank-to-continuum Neumann transfer preserve
  the algebraic count and produce the continuum resolvent upper.

## Result boundary

- The theorem is for the exact full continuum kernel at fixed
  sigma = 1/100.
- The validated norm is the continuum/Galerkin L-infinity norm.
- RH-40's simple-isolated full-kernel parity premise is closed at this noise
  width.
- Adaptive cutoff transfer is available asymptotically in L-infinity.
- No dimension-uniform Euclidean resolvent theorem for the archived sparse
  midpoint matrices is claimed.
- No zero-noise limit, zeta-zero identification, self-adjoint
  Hilbert--Pólya operator, or Riemann-hypothesis conclusion is made.

## Reproduce

From this directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_coarse_grushin_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_midpoint_bridge_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_continuum_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-parity-continuum-contour.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~

The Grushin replay is the longest step, typically about one minute on the
current server. The Arb bridge takes roughly ten seconds.

## Layout

- main.tex, references.bib: manuscript sources.
- validated-parity-continuum-contour.pdf: publication PDF.
- src/parity_contour/: analytic derivative, Galerkin, Schur, and Grushin
  bounds.
- experiments/run_coarse_grushin_certificate.py: exact-stored bordered
  inverse certificate.
- experiments/build_midpoint_bridge_certificate.py: 224-bit exact
  stored-to-midpoint bridge.
- experiments/build_continuum_certificate.py: complete continuum
  composition.
- experiments/make_figures.py: publication figure.
- experiments/build_archive.py, experiments/verify_archive.py: hashed
  archive construction and replay.
- results/: three theorem ledgers, dependency manifest, summary, and archive
  verification.
- tests/: analytic identities and archived gate checks.
