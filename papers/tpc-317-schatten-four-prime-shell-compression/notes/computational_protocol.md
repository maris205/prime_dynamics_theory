# TPC-317 computational protocol

## Locks

* Parent certificate: `papers/tpc-316-literal-arithmetic-l2-fresh-panel/results/tpc316_certificate.json`.
* Parent normalized-LF SHA-256: `3bb9f3463daf7583ca07a672bf19be827af5404c2c7005b6e6bf6b766bd8ef26`.
* `H=66`, `Q={24,36,54,80}`, `s={1,2}`.
* Source scales: `640,1280,2560`, with `I_X=(X/2,X]`.

## Main calculation

For each row, the code reconstructs the literal matrix block by block and
accumulates the source Gram `G=A^*A`.  It repeats the block accumulation in
reverse prime-shell order.  The two Gram matrices are symmetrized because the
exact object is symmetric.  The reported interval contains both reductions,
the propagated binary64 guard, and a conservative display pad.

The label is `NUMERICALLY_CERTIFIED_FINITE`, not `PROVED_EXACT`, for the large
panels.  The exact rational anchor uses `I={17,...,32}`, one prime `p=5`, and
`s=1`; it checks both `trace(G)` and `trace(G^2)` independently.

## Pass criteria

* 24 unique `(X,Q,s)` rows.
* 16 adjacent-scale Schatten-4 intervals with strict decrease.
* 16 adjacent-scale Frobenius intervals with strict increase.
* Forward and reverse shell accumulation agree inside every stored interval.
* Normal and optimized Python, producer and independent checker, agree.

No fitted asymptotic exponent, external physical sample, or arithmetic
reassembly is part of the protocol.
