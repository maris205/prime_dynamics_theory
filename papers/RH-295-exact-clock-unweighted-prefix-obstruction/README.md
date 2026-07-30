# RH-295: Exact-clock unweighted prefix obstruction

Uniform convergence on the correct growing window is still not a weighted
determinant theorem.  For any prescribed cut m_sigma->infinity and R>1,
define a single escaping coefficient spike at n=m_sigma-1 with amplitude

    epsilon_sigma = R^(-(m_sigma-1)/2).

Then every fixed coefficient is eventually zero and

    max_(2<=n<m_sigma) |e_(sigma,n)| = epsilon_sigma -> 0,

but its weighted prefix is

    epsilon_sigma R^(m_sigma-1)/(m_sigma-1)
      = R^((m_sigma-1)/2)/(m_sigma-1) -> infinity.

Thus even synchronizing the RH-294 type maximum to the exact RH-292 clock
would not suffice without a quantitative rate or an aggregate analytic norm.
The example is an abstract coefficient array, not a claimed physical noisy
spectrum.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf exact-clock-unweighted-prefix-obstruction.pdf
