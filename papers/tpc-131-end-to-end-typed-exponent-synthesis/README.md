# TPC-131: End-to-end typed exponent synthesis

Paper title:

> *End-to-End Endpoint Synthesis on the Literal Fixed-Shift Carrier:
> Acyclic Proof Certificates, Typed Exponent Transport, and Strict
> Physical Slack*

## Core result

The paper composes the arithmetic and physical ledgers without
identifying them.  If the nonsoft literal packets have one uniform raw
saving

```text
max_b |P_b| <= X^(1 - sigma_raw + o(1)),
```

the complete soft remainder is `o(X)`, exact reconnection holds, and
the theorem-backed physical synthesis cost is

```text
X^(Lambda_phys + o(1)),
```

then

```text
|B_h0,delta(X)|
  <= o(X) + X^(1 - sigma_raw + Lambda_phys + o(1)).
```

Thus the route closes only when

```text
sigma_raw - Lambda_phys > 0.
```

For the MVP1 raw target `sigma_raw = 1/400`, this is precisely the
strict endpoint condition `Lambda_phys < 1/400`; equality is a stop.

The determinant/zero-mode condition is a separate admissibility test:

```text
(lambda_E + 2 lambda_phi - gamma_R)_+
  <= 2 min(delta_prefix - ell_Z, eta_cont),
delta_prefix >= ell_Z.
```

Its reserve is never physical endpoint slack.

## Audit protections

- an acyclic proof DAG plus a semantic firewall against target-as-premise
  arguments;
- a robust occurrence registry with globally unique token IDs and
  explicit scale, scope, carrier, and branch tags, so repeated
  applications are never silently merged;
- explicit energy-to-amplitude exponent conversion before occurrence
  costs are summed;
- acyclic exact-cover dependency replacement for joint operator
  bounds, rejecting self-dependencies and overlapping primitive-leaf
  sets;
- exact tail coverage: the H3 squarefree truncation tail, H5 content
  remainder, and physical high/ultra tail occupy separate namespaces
  and are each assigned exactly once, with neither omission nor
  duplication across raw, H5, soft-physical, or joint-token branches;
- refusal to treat a finite regression, a reduction, or a conditional
  interface as an L2 theorem.

The paper supplies an L0/L1 composition theorem and certificate format.
It proves no growing fixed-`h0` arithmetic saving.

## Reproduce

```powershell
python experiments/tpc131_typed_synthesis_audit.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-131-end-to-end-typed-exponent-synthesis.pdf`

SHA-256:

`f2b6950a4540e9408c31d780e9e6166c49e5639bdadc301d675151b44a3b9d24`
