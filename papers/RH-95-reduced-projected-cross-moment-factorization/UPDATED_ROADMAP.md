# Updated roadmap after RH-95

## Exact progress

The ambient projected-cross SVD is not algebraically essential. Its singular
data live in the `r x r` matrix

    C = V* G^2 V - (V* G V)^2,

and the full small Ritz compression is determined by packet moments through
order three. A QR-stabilized reconstruction preserves every RH-94 endpoint.

## Newly exposed barrier

The fourth cross mode can be extremely weak. The smallest audited ratio is

    s_4(K) / s_1(K) = 2.77e-11.

Normal equations square this condition number, while the moment identities
subtract nearly equal matrices. Consequently a naive binary64 moment-only
implementation is unstable in fifty of 120 updates. This is a real route
boundary, not merely a coding detail.

## Preferred RH-96 gate: weak-mode quotient

The stabilized corrected tails remain essentially identical even when the
selected direction projectors differ visibly. This suggests that weak cross
modes need not be identified geometrically; they should be quotiented by an
energy criterion.

RH-96 should derive an a posteriori bound of the form

    Ritz-tail loss <= function(discarded cross energy,
                               compressed spectral gap,
                               complement energy),

then test adaptive widths that retain only modes above a certified threshold.
The goal is tail-stable identification, not unstable direction recovery.

## Later route

After weak-mode quotienting:

1. compose repeated reduced blocks or introduce a stopped exit clock;
2. control source-to-block burn-in uniformly;
3. build normalization and observability gate `O`;
4. return to moving-cloud determinant limits only after those finite gates.

No Hilbert--Polya operator, zero identification, or proof of RH is asserted.
