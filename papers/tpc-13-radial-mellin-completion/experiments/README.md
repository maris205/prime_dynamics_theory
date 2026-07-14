# Finite certificate

This package checks only the finite algebra used in TPC-13:

- the factor-pair/GCD-coordinate bijection;
- equality of the direct and compressed two-coordinate transforms;
- the explicit dyadic-sector log-gap lower bounds;
- tensor-Fejer coefficient recovery and exact dephasing;
- the product-center identity for the fully radial energy;
- the exact total-energy minimax witnesses.

Run from the paper directory:

    python experiments/radial_mellin_certificate.py
    python -m unittest experiments.test_radial_mellin_certificate

The scripts use only the Python standard library. They do not test the
Guth--Maynard theorem, a fixed quadratic-prime asymptotic, or any
fixed-shift prime-pair assertion.
