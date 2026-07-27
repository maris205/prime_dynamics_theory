# RH-202: adjacent edge-quartet transport

This paper performs the first direct cross-scale transport audit of the
source-observable outer quartet selected in RH-200. The natural dyadic Haar
map gives order-one subspace, projector, source-state, and residue defects.
The quartet therefore survives as a local spectral packet but not as a
literal Haar-transported shell.

Run the focused audit with:

```bash
/root/math/.venv/bin/python experiments/run_adjacent_transport_audit.py
/root/math/.venv/bin/python -m pytest -p no:cacheprovider
```

The result is finite and floating. It does not reject renormalized transport
or a scalar divisor route, and it does not close Gate A.
