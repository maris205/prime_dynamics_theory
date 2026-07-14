# Exact Mellin certificate

The script verifies the all-rational five-node certificate used in the
paper. It checks:

- the genuine prime-target row `3^4 + 2 = 83`;
- equality of the first four normalized log-scale moments of the two
  probability profiles;
- their exact central-window gap `3/4`;
- the annihilator `(1,-4,6,-4,1)` and the sharp minimax radius `3/8`;
- equioscillation of the best cubic-space approximant
  `q(x)=5/8-x^2/16`.

Run:

```bash
python exact_mellin_certificate.py \
  --output data/exact-mellin-certificate.json
python -m unittest -v test_exact_mellin_certificate.py
```

Only the Python standard library is required. No floating-point arithmetic
is used in the certificate.
