# TPC-218 Source Lock

## Repository inputs

- TPC-217 finite-window attachment:
  research/tpc-big-road/bridge_b_finite_window_rational_large_sieve.md.
- TPC-216 fixed-q row-energy envelope:
  papers/tpc-216-direct-sum-row-energy-envelope/PROOF_PACKAGE.md.
- TPC-215 short-quotient cluster majorant:
  papers/tpc-215-short-quotient-mobius-majorant/PROOF_PACKAGE.md.
- Repository workflow and claim firewall: AGENTS.md and TPC_HANDOFF.md.

## Frozen physical fields

~~~
h0/fixed atom: retained upstream; no new fixed-atom credit
source coefficient: c_d=mu(d)log(d)/d
prime shell: Q<q<=2Q
packet labels: j=0,1,2,3 at the four-packet interface
window: I_x=(x/2,x] intersect Z
normalization: divide by N=|I_x|
~~~

## New standard input

The only analytic input newly invoked is the standard additive large-sieve
inequality for U^(-2)-separated rational frequencies. Its Hilbert-valued form
is obtained by applying the scalar inequality to each coordinate and summing.

## Source boundary

The proof controls a common-source structural kernel. It does not identify an
arithmetic signed cancellation theorem for the literal fixed atom. Therefore
TPC218_ARITHMETIC_ADVANCE = NO and TPC218_FIXED_ATOM_CREDIT = 0.
