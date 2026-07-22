# Updated roadmap after RH-93

## What RH-93 changes

RH-92 had a green four-step variable Schur budget, but refreshed the old
packet from an ambient leading eigenspace at every update. RH-93 removes that
in-block reset on the frozen windows.

The recursive width-one packet fails the sub-quarter block target in all four
fine channels at `sigma=0.02` and `sigma=0.01`. Selecting the first two left
singular directions of the projected cross operator repairs every failure.

The second direction is therefore a genuine route threshold in the archived
recursive construction.

## Combined gate

Define `D2` to mean:

    a uniform two-direction projected-cross Ritz chain
    with a contracting fixed-length block product.

Such a theorem would provide both:

- the block contraction formerly called `S_blk`; and
- the reduced in-block packet refresh formerly separated as `R`.

The preferred Stage-A alternatives can therefore be written as

    L

or

    D2 AND O,

where `L` is the inherited full-block corridor and `O` remains the
finite-prefix, normalization, and observability bridge.

## What remains inside D2

RH-93 validates one four-step block per frozen channel. An all-level theorem
still has to:

1. construct a clock-rank seed packet uniformly;
2. control the first two singular directions of `(I-P) G P`;
3. prove repeated block contraction after a uniform burn-in;
4. realize the ambient Gram action on a rank-`O(log(1/sigma))` packet with
   acceptable physical bounds.

The selected packet dimension is small, but applying the ambient Gramian is
not yet a continuum complexity theorem.

## Width three

Two directions are sufficient for contraction. Three directions are a
separate near-optimality diagnostic: the worst endpoint tail is at most
`1.05595` times the frozen leading-packet tail. Do not silently strengthen
`D2` into a three-direction assumption unless stable packet identification is
actually needed downstream.

## Later gates

The prefix/observability bridge `O` and the RH-81 moving-cloud projection,
coefficient bridge, and uniform trace-class complement remain open and
unchanged.

There is no Hilbert-Polya operator, zeta-zero identification, or proof of the
Riemann Hypothesis in this roadmap.
