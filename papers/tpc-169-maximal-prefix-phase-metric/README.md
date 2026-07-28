# TPC-169: Maximal-prefix phase metric

Paper title:

> *One Phase-Exceptional Set for Every Atomic Prefix:
> A Dyadic Maximal Parseval Theorem on Determinant-Two Fibers*

For ordered positive fiber points `t(z_1)<...<t(z_L)<=T`, bounded
periodic `rho`, and

```text
S_k(alpha) =
  sum_(j<=k) mu(d+s*z_j) mu(u+a*z_j) rho(z_j)
             exp(-2*pi*i*alpha*z_j),
D_L = 1+ceil(log_2 L),
G_T(alpha) = max_(k<=L) (q/T)|S_k(alpha)|,
```

TPC-169 proves

```text
integral_0^1 G_T(alpha)^2 d alpha
  <= D_L^2 ||rho||_infinity^2 (q/T+q^2/T^2).
```

The proof is the elementary dyadic Rademacher-Menshov decomposition:
each prefix is a union of at most one dyadic block at each level,
and Parseval sums every block level exactly.

Thus one phase-exceptional set controls every prefix endpoint,
including endpoints inside the TPC-159 dyadic scale shadow.  For
endpoints `U in [theta*T,T]`, the natural normalization loses only
`theta^(-1)`.

Typed status and norm axes:

```text
status = PROVED_L1_ACTUAL_CORE_PHASE_METRIC_MAXIMAL_PREFIX
analytic_norm = L2_PHASE_MAXIMAL
program_positive_L2 = false
fixed_atom = false
```

The statement is pointwise in the endpoint but averaged in the
phase.  It therefore advances a phase-metric child of the bad-endpoint
OPEN node, not the original theorem at a specified phase such as
`alpha=0`.

Reproduce:

```powershell
python experiments/tpc169_maximal_prefix_audit.py
python experiments/tpc169_maximal_prefix_audit.py --check
```
