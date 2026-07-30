# RH-292: Tail-absorbed weighted bridge clock

The RH-288 prefix was stated at the convenient spectral cut

    m_sigma = ceil(4 log(1/sigma)).

It is not necessary to prove the coefficient bridge all the way to that
order.  Put

    a_* = 1 / log(10/7) = 2.803673252057129...,
    h_sigma = ceil(a_* log(1/sigma)).

For the modulus complement and the deterministic anchor,

    P_sigma(m_sigma)
      <= P_sigma(h_sigma) + S_sigma(h_sigma) + T_sigma(h_sigma).

RH-282/RH-283 give S_sigma(h_sigma)=O(1/log(1/sigma)) even at the
critical slope, while RH-267/RH-268 give T_sigma(h_sigma)->0 because
q_* R<1.  Therefore a direct weighted bridge at h_sigma, or both typed
budgets E_sigma(h_sigma) and D_sigma(h_sigma), already implies the original
RH-288 prefix at m_sigma.

This strictly shortens the missing bridge clock but does not supply the
bridge itself.  Gates A--E remain false/open.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf tail-absorbed-weighted-bridge-clock.pdf
