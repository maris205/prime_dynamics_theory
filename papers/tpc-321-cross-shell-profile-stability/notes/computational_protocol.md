# TPC-321 computational protocol

* Source interval: (I_X=(X/2,X]capmathbb Z), with (X=640,1280,2560).
* Prime shells: (S_Q=(Q,2Q]capmathbb P), with (Q=24,36,54,80).
* Kernel height: (h=66); exponents: (s=1,2).
* Matrix: literal block accumulation followed by (G=A^{\mathsf T}A).
* Producer paths: forward and reverse prime accumulation; NumPy and SciPy full
  symmetric eigensolvers on each matrix.
* Comparison: all nine producer path pairs for each adjacent Q transition;
  outward guard (10^{-12}), sign tolerance (10^{-8}).
* Independent path: reverse shell order, `numpy.einsum`, NumPy full spectrum.
* Certificate: canonical sorted JSON with a SHA-256 payload digest and a
  SHA-256 lock on the TPC-320 parent certificate.
* Stress controls: positive-scalar invariance, metric symmetry/triangle bounds,
  majorization labels, near-tie guard, and threshold enclosure.

No random seed, external data, or unrecorded parameter is used.
