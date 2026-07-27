# RH-193: Source-Cyclic Spectral Quotient

For one physical matrix seed `S`, the correct low-dimensional state is

```text
K_S = span{S, AS, A^2 S, ...}.
```

It is invariant under left multiplication, cyclic, and has dimension at
most `deg(mu_A) <= n`, independent of the source width `m`.  Every RH-185
right temporal packet lies in this space.  Restricting the physical
observation to `K_S` preserves every Markov parameter
`<O*, A^j S>_F` and the complete scalar transfer germ at infinity.

A 140-case complex audit verifies closure, the intertwining identity,
temporal inclusion, and moment preservation with zero failures.  This
removes the RH-192 multiplicity obstruction at the correct source-relative
type; it does not prove that the physical cyclic dimension is uniformly
small or identify a canonical all-level spectral packet.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_source_cyclic_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf source-cyclic-spectral-quotient.pdf
```
