# RH-91: Schur packet route review

This directory contains the tenth layer in the RH-82--RH-91 block:

> *From Half-Log Rank Clocks to Schur Packet Bootstrap: A Ten-Layer Review
> and the Revised Stage-A Frontier*

## Synthesis theorem

For normalized memory Gramians

    G_j = X_j*X_j / ||X_j||_HS^2 + eta G_(j-1),

assume a nondecreasing clock-rank packet law gives

    E_(j+1) <= rho E_j,       0 < rho < 1,

for `m` consecutive post-burn-in updates. Since `tr(G_j) <= 1/(1-eta)`,

    E_(b+m) <= rho^m/(1-eta),
    tau_r(X_(b+m))/||X_(b+m)||_HS
      <= rho^(m/2)/sqrt(1-eta).

RH-90's Schur sign condition is a sufficient one-step premise for this
bootstrap. Combined with the inherited reduced-future and observability
conditions, it supplies the RH-78 effective-rank residual gate.

## Ten-layer verdict

- RH-82--RH-84 progressively weaken endpoint factorization to captured
  energy.
- RH-85--RH-87 construct strict-prefix and late-memory packets and reduce
  drift to scalar Rayleigh injection.
- RH-88 closes the global-norm and point-packet contraction shortcuts.
- RH-89 finds a rank-one complement Ritz corrector.
- RH-90 replaces the full reference packet by a small Schur sign certificate.

At `eta=1/512`, `rho=0.24`, the bootstrap needs 20 updates for a `1e-6`
relative tail and 39 updates for `1e-12`.

## Revised frontier

Stage A still has two alternatives:

1. prove the all-level full-block law; or
2. complete the Schur packet bundle: uniform late Schur contraction,
   polylogarithmic reduced packet future, and the inherited
   prefix/observability bridge.

The A5 moving-cloud projection, coefficient bridge, and uniform complement
gates are unchanged. No Hilbert--Polya or Riemann-hypothesis conclusion is
made.

See `UPDATED_ROADMAP.md` and `THEOREM_LEDGER.md`.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_route_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_route_review.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf schur-packet-route-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
