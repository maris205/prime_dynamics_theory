# TPC-168: Separated-phase registry sieve

Paper title:

> *Separated Phase Registries for Direct Core Twists:
> A Finite Large-Sieve Gate and a Selector Firewall*

Let

```text
P(alpha) = sum_(n=0)^(L-1) b_n exp(2*pi*i*n*alpha)
```

and let `alpha_1,...,alpha_M` be `delta`-separated on the circle.
TPC-168 proves the elementary sampling inequality

```text
sum_j |P(alpha_j)|^2
  <= [delta^(-1)+4*pi*(L-1)] sum_n |b_n|^2.
```

Applied to the normalized determinant-two direct twist, this gives an
explicit upper bound on the number of bad phases in any finite
separated registry.  If the registry is quasi-uniform and has
`M >= theta*L`, then

```text
fraction{|F_N(alpha_j)| > lambda}
  <= C(c,theta) * (q/N+q^2/N^2) / lambda^2.
```

At `lambda=(q/N)^(1/4)`, a density-one proportion of the registry
has a fixed-`X` power saving whenever `q` is polylogarithmic and
`N >= sqrt(X)`.

This is a phase-metric finite-registry theorem with the following
separate axes:

```text
status = PROVED_L1_ACTUAL_CORE_PHASE_METRIC_FINITE_REGISTRY
analytic_norm = L2_PHASE_REGISTRY
program_positive_L2 = false
fixed_atom = false
```

It does not identify a distinguished production phase.  The explicit
constant-coefficient example with a registry containing phase zero
shows that a density-one phase theorem can coexist with one selected
bad phase.  That is a selector route stop, not evidence that the
literal Mobius core has a large twist.

Reproduce:

```powershell
python experiments/tpc168_registry_sieve_audit.py
python experiments/tpc168_registry_sieve_audit.py --check
```
