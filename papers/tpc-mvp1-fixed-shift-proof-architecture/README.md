# TPC-MVP1: Fixed-shift proof architecture

Paper title:

> *TPC-MVP1: A Falsifiable Proof Architecture for Fixed-Shift
> Prime-Pair Correlations: Verified Interfaces, Explicit Working
> Hypotheses, and Stop-Go Tests at the Parity Frontier*

Here **MVP** means **Minimum Viable Proof Program**.  The paper is a
conjectural architecture and conditional synthesis, not a minimum
version of a proof.

## Purpose

TPC-MVP1 compresses TPC-1 through TPC-102 into:

- a seven-stage audit of what is actually established;
- eight imported established interfaces `[E]`;
- nine explicit working hypotheses `[H]`;
- one conditional fixed-shift Hardy-Littlewood synthesis `[C]`;
- genuine go/stop/fallback criteria for every major route;
- an eighteen-paper TPC-103 through TPC-120 verification queue; and
- an explicit list of results that remain unproved `[N]`.

Every statement continues to distinguish:

- `L0`: finite algebra, exact model identities, spectra, and
  countermodels;
- `L1`: literal physical interfaces preserving the prescribed shift,
  actual support, native keys, masks, coefficients, and normalization;
- `L2`: a new growing estimate for the complete literal coefficient
  attached to one prescribed nonzero shift.

TPC-MVP1 is an `L1` synthesis.  It proves no new `L2` estimate.

## Three macro hypotheses

The architecture is:

```text
L: literal completeness
        +
P: literal packet saving
        +
S: physical synthesis with strict endpoint slack
        |
        v
B_(h0,delta)(X) = o(X)
        |
        v
weighted fixed-shift Hardy-Littlewood
```

The macro hypotheses are resolved into nine gates:

1. canonical physical synthesis;
2. literal positive resonance (`W_X`, `P_X`, and `X_X`);
3. restricted growing fixed-`h0` signed affine Mobius cancellation;
4. high-frequency, ultra-tail, short-fiber, boundary, and outer return;
5. determinant-energy and distinguished-zero-mode compatibility;
6. full-block physical return;
7. prescribed-shift localization;
8. literal reconnection to the original hard packet; and
9. a nonduplicated physical loss strictly below `1/400`.

Gate 3 is explicitly identified as the unresolved parity-facing
arithmetic hypothesis.  It is not called technical.

## Conditional theorem

For a fixed admissible nonzero even `h0` and a fixed smooth compactly
supported weight `W`, if all nine hypotheses hold in the same literal
normalization and quantifier scope, then

```text
sum_n Lambda(n)Lambda(n+h0)W(n/X)
  = singular_series(h0) X int W + o(X).
```

For a nonnegative weight, the conditional asymptotic gives
`>> X/log^2 X` prime pairs in a dyadic interval.  Only after every
hypothesis has been proved for `h0=2` may this be specialized to a
conditional twin-prime corollary.

This implication does not establish the hypotheses, and their
conjunction may contain the full difficulty of the parity problem.

## Finite route audit

Run:

```powershell
python experiments/tpc_mvp1_route_audit.py
```

The script audits 98 recorded dependency, claim-typing, stop-go,
queue, and rational-ledger items.  It confirms that:

- all nine hypotheses feed the conditional synthesis;
- the dependency graph is acyclic;
- no established node is labeled `L2`;
- every gate has a go certificate, genuine stop certificate, and
  fallback; and
- the endpoint and scale identities are internally consistent.

The script tests no asymptotic Mobius estimate or prime-pair data.

## Claim boundary

The paper does **not** establish:

- any new growing fixed-`h0` arithmetic cancellation;
- the nine working hypotheses;
- a parity breakthrough;
- a Hardy-Littlewood asymptotic;
- a prime-pair lower bound or twin-prime theorem;
- that the hypothesis stack is easier than the original problem;
- a Riemann-hypothesis consequence; or
- an identification of Riemann zeros with a dynamical spectrum.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-mvp1-fixed-shift-proof-architecture.pdf`

SHA-256:

`86953CD14D12B9D49E6DBC710EAC1F7B646D74B2AFC2EB8E8459FFD04B51CD79`
