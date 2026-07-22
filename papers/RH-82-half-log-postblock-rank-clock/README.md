# RH-82: half-log postblock rank clock

This directory contains the eighty-second RH-layer paper:

> *Exponential Excess-Rank Tails and the Half-Logarithmic Postblock Clock*

## Main theorem

Let `R_sigma` be the endpoint-projected Gaussian resolution operator from
RH-16, and let

    J_sigma = max{k : delta_k >= sigma}.

If the geometric endpoint ladder obeys `delta_(k+1)/delta_k <= q < 1` and the
unresolved row energy satisfies `F(t) <= C t^2`, then

    tau_(J_sigma+ell)(R_sigma)
        <= sqrt(C/(1-q^2)) q^ell.

Thus the Hilbert--Schmidt tail decays exponentially in every rank added beyond
the half-logarithmic clock

    J_sigma = log(1/sigma)/(2 log(lambda)) + O(1).

If a physical postblock state factors as

    B_sigma = U_sigma R_sigma V_sigma + E_sigma,

then

    tau_(J_sigma+ell)(B_sigma)
      <= ||U_sigma|| ||V_sigma|| sqrt(C/(1-q^2)) q^ell
         + ||E_sigma||_HS.

Polylogarithmic outer, remainder, and observability bounds therefore provide
the effective-rank premise required by RH-78 with logarithmic rank. The actual
endpoint-to-postblock factorization remains open.

## Validated audit

A 192-bit Arb audit uses the exact frozen binary64 matrices from RH-77 and the
rank schedule

    r_sigma = ceil(log(1/sigma)/(2 log(lambda))) + 2.

Across all ten channels:

- ranks range only from 4 to 7;
- maximum relative postblock residual is `2.33935e-7`;
- minimum energy capture is greater than `0.999999999999945`;
- maximum complete-future Hardy perturbation is `5.04303e-9`.

The RH-16 linear endpoint-row model was also replayed from `sigma=1e-2` to
`1e-12`. Its clock-plus-two optimal Hilbert--Schmidt tail remains below
`9.19e-8`.

## Route consequence

The uniform Stage-A problem is no longer an unspecified singular-value decay
ansatz. It is the concrete task of factoring the physical postblock state
through the already understood endpoint Gaussian resolution operator with
polylogarithmic outer norms and remainder.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_half_log_rank_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_half_log_rank_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf half-log-postblock-rank-clock.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

