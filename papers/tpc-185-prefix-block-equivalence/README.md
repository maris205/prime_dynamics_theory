# TPC-185: Prefix Maxima and Consecutive Blocks: An Exact Deterministic Equivalence

## Exact result

For every finite sequence, the largest consecutive-block sum is at most twice the largest prefix sum, while every prefix is itself a consecutive block.  Thus a uniform block theorem and the desired prefix theorem are equivalent up to the literal factor two, with no phase, scale, support, or power change.

```text
classification = REDUCTION_L1
verdict = EXACT_FACTOR_TWO_EQUIVALENCE
selected_route = O161.bad_endpoint_pointwise_fixed_atom
smallest_missing = NAMED_ATOM_CONSECUTIVE_BLOCK_POWER_SAVING

fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
```

The result is L0/L1 only. Any `STOP_SCOPED` declaration applies only to the
named method cell and does not stop an O161 pointwise parent or the global
architecture. No program-positive L2, prime-pair lower bound, or twin-prime
theorem is claimed.

## Reproduce

```powershell
python experiments/tpc185_prefix_block_equivalence.py
python experiments/tpc185_prefix_block_equivalence.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
