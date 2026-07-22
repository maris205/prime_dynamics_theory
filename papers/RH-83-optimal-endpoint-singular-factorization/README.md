# RH-83: optimal endpoint singular factorization

This directory contains the eighty-third RH-layer paper:

> *Optimal Endpoint Singular Factorization and the Coordinate-Matching Barrier*

## Main theorem

Let `R` and `B_r` be compact operators of rank at least `r`, with singular
values `rho_j` and `b_j`. Among all factorizations

    B_r = U R V,

the optimal product of outer operator norms is

    inf ||U|| ||V|| = max_(j<=r) b_j/rho_j.

The lower bound follows from the ideal property of approximation numbers. It
is attained by aligning the singular bases. For an arbitrary `B`, taking its
truncated SVD gives

    B = U R V + E_r,
    ||E_r||_HS = tau_r(B).

Thus an all-level singular-value majorization theorem is sufficient for the
RH-82 endpoint factorization criterion; coordinate alignment is unnecessary.

## Validated audit

The endpoint Gram formula and frozen postblock states are propagated at
192-bit precision. Across the five archived scales:

- the optimal factor constant is at most `0.161572`;
- the certified mediator rank is never more than one below the
  `ceil(H_sigma)+2` schedule;
- the optimal remainder is at most `1.232e-9`;
- the corresponding maximum relative remainder is `2.340e-7`.

## Negative coordinate branch

Directly identifying sampled endpoint rows with the physical postblock
coordinate space fails strongly. The clock-rank coordinate projection leaves
between `46.86%` and `97.90%` relative residual. Therefore the required outer
factor must encode nontrivial dynamical rotation; it cannot be the identity
embedding.

This is a branch-level negative result, not an obstruction to endpoint
singular majorization.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_singular_factorization_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_singular_factorization_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf optimal-endpoint-singular-factorization.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

