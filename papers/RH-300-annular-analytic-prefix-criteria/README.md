# RH-300: Annular analytic prefix criteria

Let

    g_sigma(z) = sum_(n>=2) (tau_(sigma,n)-a_n) z^n/n

be the direct complement-to-anchor logarithmic mismatch.  If it is
holomorphic on a neighborhood of the closed disk of radius rho>R, then
either of two aggregate estimates implies the full weighted coefficient
budget:

    ||g_sigma||_(H-infinity,rho) <= M_sigma
      => sum |tau_(sigma,n)-a_n|R^n/n
         <= M_sigma (R/rho)^2/(1-R/rho),

    ||g_sigma||_(H2,rho) <= H_sigma
      => sum |tau_(sigma,n)-a_n|R^n/n
         <= H_sigma (R/rho)^2/sqrt(1-(R/rho)^2).

Thus M_sigma->0 or H_sigma->0 directly supplies the RH-292 bridge without
resolving individual roots.  The certified target radius is
rho_*=1.4267874838..., so rho=1.41 leaves a strict annulus above R=1.4.
At that radius the two constants are 139.0070922 and 8.2924679.

The strict annulus matters for H2: at rho=R there are polynomials with
H2 norm tending to zero but weighted coefficient l1 norm equal to one.
No annular convergence theorem for the actual noisy complement is currently
proved.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf annular-analytic-prefix-criteria.pdf
