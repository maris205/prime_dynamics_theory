# TPC-228 paper plan

## Question

After TPC-227 separates packet and profile axes, what is the exact common-profile
collision quantity produced by the V59 four-phase source packets?

## Theorem edge

For arbitrary finite prime-labelled Hilbert rows `U_q,V_q`, prove that the four-phase
combination of packet AP energy minus packet diagonal equals exactly the off-diagonal
source collision sum `sum_(q!=r)<U_q,V_r>`.

## Deliverables

1. Keep `i^j` on the source input and one transform on every packet.
2. Delete the same-prime diagonal before interpreting collisions.
3. Derive the exact Q25 `3--7` source block.
4. Certify positive, negative, zero, directed and single-coordinate controls.
5. State the remaining actual V59-to-atom crosswalk and arithmetic sign theorem as open.

## Exit condition

The exact compiler, independent reproduction, adversarial validation, bridge checker and
PDF must agree without claiming arithmetic `L2`.
