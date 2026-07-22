# RH-75: log-square block contraction law

This directory contains the seventy-fifth RH-layer paper:

> *Log-Square Horizons and the Square-Root Block-Contraction Law*

## Main theorem

Let `sigma_k = sigma_0 2^{-k}`. Suppose a directional production family has

    M_k <= (k+a)^2,
    ||A_k^{M_k}|| <= C_q sqrt(sigma_k),
    sigma_k ||Y_k||_F^2 <= C_y,
    sum_{r<M_k} ||A_k^r X_k||_F^2 <= C_s (k+a)^s,

and finite-prefix energy at most `C_f (k+a)^f`. Then the block tail is

    T_k^2 <= C_y C_q^2 C_s (k+a)^s
             / (1-C_q^2 sigma_0),

and the full Hardy energy squared is polylogarithmic. Thus a growing
log-square horizon is sufficient; a universal fixed horizon is unnecessary.

## Five-anchor interval certificate

The RH-70/RH-74 data satisfy, in all ten channels,

- `M_k <= (k+2)^2`;
- `||A_k^{M_k}||/sqrt(sigma_k) <= 0.086`;
- `sigma_k ||Y_k||_F^2 <= 2.561`;
- one-block source energy `<= 3.1`;
- finite-prefix energy squared `<= 0.552 (k+2)`.

The resulting common tail envelope is `0.058788`; the largest certified tail
is `0.049421`.

## Route consequence

The uniform Stage A1 problem is now reduced to proving the displayed
all-dyadic square-root block law and its source/prefix companions. Five
validated anchors satisfy the law, but finite anchors do not prove the
all-level statement. RH-76 therefore attacks the phase-compression mechanism
that could generate the log-square horizon.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_log_square_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf log-square-block-contraction-law.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~
