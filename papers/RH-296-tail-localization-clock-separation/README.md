# RH-296: Tail/localization clock separation

The current projection-free tail and the archived Gaussian orbit-tube proof
require incompatible logarithmic clocks.

For q=1/2, R=7/5 and Hilbert--Schmidt mass exponent one, uniform tail decay
requires

    a >= a_tail = 1/log(10/7) = 2.803673252057129...

in m_sigma=ceil(a log(1/sigma)).  To cover every order below such a moving
prefix, the existing interior Gaussian localization architecture must in
particular handle the largest even order below the cut.  Its boundary
clearance argument can only do so while

    a <= a_loc = 1/log(lambda) = 1.930709419186936...

and its stronger interior asymptotic requires a<a_loc.  Hence the two slope
ranges are disjoint, with gap 0.872963832870193.

This is a rigorous obstruction to reusing the RH-9/RH-10 orbit-tube proof
uniformly over the weighted prefix.  It is not a theorem that the actual
noisy traces fail to converge on the longer clock; a moving-order
boundary-layer method could in principle replace the old proof.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf tail-localization-clock-separation.pdf
