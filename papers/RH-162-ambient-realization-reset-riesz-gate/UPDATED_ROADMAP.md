# Roadmap after RH-162

The physical packet-to-Riesz bridge now starts with an ambient type gate:

```text
reset memory packet --X: (J, primal defect, adjoint defect)--> transfer-space packet
                     --contour/Schur certificate-----------> Riesz cloud
```

The next paper should use the two directed coupling bounds separately.  A
Schur-complement product can remain small even when the symmetric Neumann
bound from RH-161 fails.

For the actual family, `X` is open: construct a target-independent map `J_j`,
prove its normalization/canonicity, and bound both `A_j J_j-J_j M_j` and its
adjoint analogue.  Dimension matching or a fitted eigenvector map is not an
acceptable substitute.
