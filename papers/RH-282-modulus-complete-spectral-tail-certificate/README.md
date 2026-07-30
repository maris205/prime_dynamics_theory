# RH-282: Modulus-complete spectral-tail certificate

Let `A_sigma=K_sigma/0.85` and remove the Perron and negative-parity
eigenvalues from its algebraic spectrum.  Select every remaining eigenvalue
with modulus greater than `q=1/2` and realize the complementary multiset as a
normal diagonal operator `C_sigma`.  This is an exact projection-free
realization of the complementary `det_2` factor.

The RH-276 mass law gives, for all sufficiently small noise,

```text
sum |mu_j(sigma)|^2 <= ||A_sigma||_2^2 <= sigma^(-1).
```

On the tail, `|mu_j|<=1/2`.  Hence for every `n>=2`,

```text
|Tr C_sigma^n| <= sigma^(-1) 2^(-(n-2)).
```

At the certified target radius `R=7/5`, choose
`m_sigma=ceil(4 log(1/sigma))`.  Then the RH-279 trace norm, operator norm,
prefix, and root-rate conditions all hold, and the logarithmic tail beyond
`m_sigma` tends to zero uniformly on `|z|<=7/5`.  The limiting root-rate upper
bound is

```text
(7/10) exp(1/4) = 0.8988177916... < 1.
```

This is a genuine variable-rank spectral-tail certificate.  It does not
identify the modulus-complete noisy head with the deterministic monodromy
counterloop, and it does not construct a well-conditioned physical Riesz
quotient.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf modulus-complete-spectral-tail-certificate.pdf
```
