# TPC-417 — four-shell finite full-operator bound

This release proves an exact finite theorem for the complete locally
normalized `N=4H` synthetic C1 matrix, using the four full shells
`Q=65536,131072,262144,524288` and retaining all `75483` primes.  At each
`H=16,32,66,128`, the endpoint-star/interior-bulk decomposition gives

```text
||Z||_2 <= 2/(a_min*sqrt(H)) + 16*abs(A_signed_bulk)/V_minus.
```

All aggregate quantities are exact rational strings.  The producer, an
independent aggregate replay, and a mutation checker are deliberately separate.

```bash
python -B papers/tpc-417-c1-four-shell-finite-operator-bound/code/tpc417_c1_four_shell_finite_operator_bound.py --check
python -O -B papers/tpc-417-c1-four-shell-finite-operator-bound/code/tpc417_c1_four_shell_finite_operator_bound.py --check
python -B papers/tpc-417-c1-four-shell-finite-operator-bound/experiments/tpc417_independent_checker.py --check
python -O -B papers/tpc-417-c1-four-shell-finite-operator-bound/experiments/tpc417_independent_checker.py --check
python -B papers/tpc-417-c1-four-shell-finite-operator-bound/experiments/tpc417_adversarial_certificate_stress.py --check
python -O -B papers/tpc-417-c1-four-shell-finite-operator-bound/experiments/tpc417_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc417_c1_four_shell_finite_operator_bound_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc417_c1_four_shell_finite_operator_bound_checker.py --check
```

The finite full-operator bound does not establish a bound uniform in growing
`H,Q,N`; it does not identify physical coefficients or `h_0`, pay arithmetic
`L2` or the strict `1/400` loss, close Route-B, or imply twin primes.
