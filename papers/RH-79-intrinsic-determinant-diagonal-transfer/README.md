# RH-79: intrinsic determinant diagonal transfer

This directory contains the seventy-ninth RH-layer paper:

> *Intrinsic Bulk-Square Transfer and the Shrinking-Disk Determinant Gate*

## Main theorem

If an intrinsic bulk and an anchored bulk satisfy

    ||B_int-B||_HS <= epsilon,
    ||B||_HS <= M,

then

    ||B_int^2-B^2||_1 <= epsilon(2M+epsilon).

The Fredholm determinants obey, on `|w|<=R`,

    |det(I-w B_int^2)-det(I-w B^2)|
      <= R delta exp(1+R M^2+R(M+epsilon)^2).

Under the RH-78 conditional identification bound and
`M=O(sigma^(-1/2))`, the square error tends to zero on every strict
`n sigma^2 -> infinity` schedule. The determinant bound is uniform on
shrinking disks `R=O(sigma)`, but the generic exponential is not controlled
on a fixed disk.

## Five-anchor audit

Using the stress mesh `n=sigma^(-2)(k+2)` and the conservative bulk constant
`1.55/sqrt(sigma)`:

- square trace error decreases from `0.5754` to `0.09180`;
- the `R=0.01 sigma` determinant error decreases from `2.63e-3` to `2.62e-5`;
- the fixed `R=0.01` standard bound bottoms near `1.57e-2` and worsens to
  `0.3051`.

## Route consequence

Conditional A4 reaches trace-norm bulk squares and shrinking-disk
determinants. Entry to A5 on fixed disks requires pole renormalization or a
relative determinant estimate. More finite precision cannot remove the
`exp(O(R/sigma))` barrier.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_determinant_transfer_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf intrinsic-determinant-diagonal-transfer.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~
