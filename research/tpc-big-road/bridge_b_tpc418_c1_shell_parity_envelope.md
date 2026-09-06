# Bridge B — TPC-418 finite-family shell-parity envelope

TPC-418 closes the finite-family synthetic shell envelope after correcting the
parity bookkeeping. `epsilon_j` is the global start sign, while
`sigma_j=epsilon_j*(-1)^(n_j+1)` is the actual sign of the alternating block.
The exact certificate contains a fixed four-shell replay, a small complete
multi-shell replay, and a mixed-parity regression that rejects the old
start-sign grouping.

The theorem is deliberately scoped to finite declared families. It does not
assert growing uniformity, a physical `h0`, arithmetic sign or `L2` savings,
fixed-power credit, Route-B closure, or a twin-prime result.

The companion checker verifies the certificate digest, independent exact
replay, adversarial mutations, normal/optimized execution, and the compiled
paper artifacts.
