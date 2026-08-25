# Computational protocol

Run from the repository root with bytecode disabled:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-247-literal-v59-source-operator-attachment/code/tpc247_source_operator_certificate.py --check
python -O -B papers/tpc-247-literal-v59-source-operator-attachment/code/tpc247_source_operator_certificate.py --check
python -B papers/tpc-247-literal-v59-source-operator-attachment/experiments/tpc247_independent_checker.py --check
python -O -B papers/tpc-247-literal-v59-source-operator-attachment/experiments/tpc247_independent_checker.py --check
python -B papers/tpc-247-literal-v59-source-operator-attachment/experiments/tpc247_source_operator_stress.py --check
python -O -B papers/tpc-247-literal-v59-source-operator-attachment/experiments/tpc247_source_operator_stress.py --check
```

The independent checker does not import the producer.  It reconstructs every
matrix entry, block sum, triple count and norm formula, then rejects typed and
digest-rebound mutations.
