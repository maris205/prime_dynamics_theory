# Computational Protocol

## Purpose and evidence class

The scripts check finite algebra, serialization, and implementation invariants.
Every physical-census result is labeled
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`. No finite check is theorem evidence for
Brun--Titchmarsh or for the asymptotic packet trace.

## Producer

`code/tpc239_bt_bucket_certificate.py` uses exact runtime type guards and no
`assert` statements. It emits sorted deterministic JSON, hashes the canonical
payload without the digest field, and verifies byte-for-byte regeneration in
`--check` mode. Its exponent ledger is built with exact `Fraction` values.

## Primary physical fixture

```text
(Q,H,h)=(101,8830,82), 4Q<H, h<Q, M_h=1.
```

The producer enumerates:

- all 20 primes in `(Q,2Q]`;
- each physical `q`-dependent cutoff and row support;
- all 40 primitive residues modulo `82`;
- both unit multipliers `m=-1,1`;
- every reduced AP class and its shell-prime list;
- actual row multiplicity, AP pair census, classwise BT real RHS, and the
  factor-16 real RHS.

The buckets `a=3` and `a=79` have actual multiplicity three. Some other buckets
show a strict inequality because the AP census has dropped the physical cutoff.

## Independent checker

`experiments/tpc239_independent_checker.py` imports no producer module. It uses
a separate prime sieve, a multiplicative totient calculation, and the congruence
`m=a q mod h` to reconstruct every physical row and AP bucket. It independently
recomputes the payload digest, exact Fraction ledger, h=1 branch, status
firewall, and mutation set.

## Stress checker

`experiments/tpc239_bucket_stress.py` checks

```text
(Q,H,h) in {
  (11,100,7),
  (17,220,13),
  (29,700,23),
  (43,1500,35),
  (101,8830,82)
}.
```

For every primitive residue in all five fixtures it compares direct physical
row multiplicity with the AP census and the analytic factor-16 RHS. It also
checks every AP class against the standard real Brun--Titchmarsh RHS and tests
the separate `h=1` empty-row branch.

## Mutation firewalls

The producer and independent checker reject strict-type confusion, a composite
shell entry, a cutoff decrement, constant `15`, equality `4Q=H`, `h=Q`, misuse
of `h=1`, a nonprimitive bucket, a nonunit multiplier, reversed
`actual<=census`, and inclusion of the lower shell endpoint.

## Determinism protocol

Set `PYTHONDONTWRITEBYTECODE=1` and run every checker with `python -B` and
`python -O -B`. A subprocess harness requires exit code zero, empty stderr, and
byte-identical stdout between normal and optimized modes.
