# TPC-167: Direct additive-twist Parseval corridor

Paper title:

> *A Parseval Corridor for Direct Additive Twists on the
> Determinant-Two Mobius Core*

For the literal determinant-two core

```text
q = a*s,
t(z) = a*d+q*z,
c_z = mu(d+s*z) mu(u+a*z),
I_N = {z : N < t(z) <= 2N},
F_N(alpha) = (q/N) sum_(z in I_N) c_z exp(-2*pi*i*alpha*z),
E_N = sum_(z in I_N) |c_z|^2,
```

TPC-167 proves the exact identity

```text
integral_0^1 |F_N(alpha)|^2 d alpha = q^2 E_N/N^2.
```

Consequently,

```text
meas{alpha : |F_N(alpha)| > lambda}
  <= q^2 E_N/(N^2 lambda^2)
  <= (q/N+q^2/N^2)/lambda^2.
```

The same identity holds on every complete Fourier grid of size
`M >= |I_N|`.  It is valid at every scale, including scales excluded
by the exceptional set used in TPC-149.

When `q <= (log X)^eta_0` and `N >= sqrt(X)`, the analytic
phase-`L2` norm is at most

```text
sqrt(2) X^(-1/4) (log X)^(eta_0/2)
```

for sufficiently large `X`.  This is a genuine positive
fixed-`X` power only in the phase-averaged norm.  It is not a theorem
for a specified production phase and does not close the original
pointwise direct-twist node.

Typed status and norm axes:

```text
status = PROVED_L1_ACTUAL_CORE_PHASE_METRIC_SINGLE_CELL
analytic_norm = L2_PHASE
program_positive_L2 = false
fixed_atom = false
```

No production phase registry, deterministic all-phase estimate,
physical H3 return, `1/400`, prime-pair lower bound, or twin-prime
theorem is claimed.

Reproduce:

```powershell
python experiments/tpc167_parseval_audit.py
python experiments/tpc167_parseval_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
