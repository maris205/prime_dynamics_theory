# RH-337: Algebraic clock drift and parity--alias replacement obstruction

RH-337 audits the exact-rational clock used by the isolated RH-329 model.
The physical expansion rate is the unique positive root of

    lambda^3 + 4 lambda^2 - 16 = 0,

whereas RH-329 defines

    Lambda_hat = 2098216888035403 / 1250000000000000.

Exact rational evaluation gives

    p(Lambda_hat)
      = 5765081705833725291502719395827
        / 1953125000000000000000000000000000000000000000
      > 0.

Since the polynomial is strictly increasing on the positive half-line,
Lambda_hat is strictly larger than the physical root.  Thus the RH-329 clock

    sigma_k = Lambda_hat^(-2k)

has physical phase

    eta_k = k (1 - log(Lambda_hat)/log(lambda)) -> -infinity.

The diagnostic slope is about -1.5515885691166900e-16 per unit k.  This
decimal measures the very slow drift; it does not certify its sign.

## Off-phase theorem

Starting directly from the uniform parity binomial remainder and the physical
counterloop multiplier law, the paper proves for every fixed Lambda_c>1:

    P_route,k
      = 2 k C_star r_H^(-2k) Lambda_c^(-k) (1+o(1)),

    A_route,k
      = (2k/C_M) r_H^(-2k) lambda^(-k) (1+o(1)),

    P_route,k / A_route,k
      = C_star C_M (lambda/Lambda_c)^k (1+o(1)).

This proof does not reuse RH-326 or RH-330 outside their bounded-phase
hypotheses.

For Lambda_c=Lambda_hat, define the actual-route versus hatted-model scalar
defect with the inherited signs:

    D_k = (P_route,k - P_hat,k) - (A_route,k - A_hat,k).

Then

    D_k / A_route,k -> -1,
    A_route,k / H_k -> +infinity,
    D_k / H_k -> -infinity.

This is a strict scoped negative result: RH-329 cannot serve as a physical
fixed-phase parity--alias comparator.  D_k is not the complete replacement
aggregate, not the actual five-slot coefficient, and not a physical
full-trace residual.  RH-330's fixed-phase transfer theorem is not activated.

## Correct-clock barrier

Replacing Lambda_hat by the exact physical lambda removes this exponential
clock mismatch, but the route remains NOT_TESTABLE.  The archived packet
laws have only relative o(1) remainders, while target-scale replacement
requires

    o(H_k/A_route,k) = o((beta R)^(-2k)).

Because beta R>1, this is exponentially stronger.  The present sources do
not prove or disprove the required rate.

Finite hatted rows are exact reproduction checks only.  The paper does not
close the physical boundary/shell aggregate, signed far remainder,
off-alias background, noisy-head/counterloop gluing, or any Gate A--E
condition.  It constructs no Hilbert--Polya operator, identifies no Riemann
zero, proves no von Mangoldt trace formula or completed-zeta divisor equality,
and does not prove RH.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf algebraic-clock-drift-and-parity-alias-replacement-obstruction.pdf
