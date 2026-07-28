# TPC-170: Metric packet-corridor return

Paper title:

> *Metric All-Prefix Return on Prescribed Determinant-Two Packet
> Corridors: Borel-Cantelli, Representative Invariance, and the
> Fixed-Atom Stop*

For each dyadic ambient scale `X_n`, let `P_n` be a **prescribed
finite packet list**.  A packet specifies `(a,s)`, a terminal scale,
a bounded multiplier, and one canonical determinant-two
representative.  If

```text
V_(n,p) =
  D_(n,p)^2 ||rho_(n,p)||_infinity^2
  [q_(n,p)/T_(n,p)+q_(n,p)^2/T_(n,p)^2],
```

then TPC-170 proves:

```text
sum_n lambda_n^(-2) sum_(p in P_n) V_(n,p) < infinity
```

implies that for Lebesgue-almost every **fixed** phase `alpha`, all
sufficiently large `n`, every declared packet, and every prefix in
that packet satisfy

```text
(q_(n,p)/T_(n,p)) |S_(n,p,k)(alpha)| <= lambda_n.
```

No independence is required.

If

```text
X_n = 2^n,
T_(n,p) >= sqrt(X_n),
q_(n,p) <= (log X_n)^eta,
|P_n| <= (log X_n)^C,
||rho_(n,p)||_infinity <= B,
```

then every `delta<1/4` is admissible with
`lambda_n=X_n^(-delta)`.  Dyadic terminal shells convert this to
natural normalization on all endpoints in the declared shell
corridor, with a factor at most two.

All determinant-two Bezout representatives for fixed `(a,s)` are
translations:

```text
(d,u) -> (d+s*k,u+a*k).
```

With the multiplier translated covariantly, they give the same
coefficient packet and the same maximal function.  They are therefore
canonicalized rather than union-counted.

Exact Abel summation returns the metric maximal estimate to any
literal weight with certified total variation.  Atomic prefix
cutoffs have variation one.

Typed status and norm axes:

```text
status = PROVED_L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR
analytic_norm = L2_PHASE_MAXIMAL_BC
program_positive_L2 = false
fixed_atom = false
```

The quantifier is `LEBESGUE_AE_FIXED_PHASE`.  It is not
`FIXED_ATOM`, does not cover a phase selected after the scale, and
does not provide the absent production phase registry.  No physical
H3, `1/400`, prime-pair lower bound, or twin-prime theorem is claimed.

Reproduce:

```powershell
python experiments/tpc170_metric_corridor_audit.py
python experiments/tpc170_metric_corridor_audit.py --check
```
