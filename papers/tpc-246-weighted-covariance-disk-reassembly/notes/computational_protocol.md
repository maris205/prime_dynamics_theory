# TPC-246 computational protocol

- The producer, independent checker, and stress suite use only exact rational
  operations on Gaussian-rational pairs.
- Certificate JSON is ASCII, canonical, duplicate-key rejecting, and
  fail-closed under semantic mutations.
- The complex-weight fixture uses rational unit-modulus weights from
  Pythagorean triples, so every modulus and inverse construction stays exact.
- The finite fixtures illustrate the symbolic theorem; they are not asymptotic
  evidence and do not promote an arithmetic gate.
- Every checker is run with normal and optimized Python, with byte-identical
  output required.
