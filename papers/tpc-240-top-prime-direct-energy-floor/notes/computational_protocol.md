# Computational Protocol

## Classification

The theorem is analytic.  All executable results are
`NUMERICAL_FINITE_ILLUSTRATION_ONLY` or deterministic schema/provenance checks;
they are not asymptotic evidence.

## Producer

`code/tpc240_top_prime_energy_certificate.py` builds a canonical JSON payload,
adds its SHA-256 digest, and supports a read-only `--check` mode.  Every integer
and Boolean field has a strict runtime type guard.  Exact exponent and rational
constant ledgers use Python `Fraction` objects before serialization.

## Independent checker

`experiments/tpc240_independent_checker.py` does not import the producer.  It
independently reconstructs the certificate, validates the canonical byte
encoding and payload hash, and rejects mutations of status, integer type,
constant, exponent, coefficient sign, profile class, p-domain, q-split object,
and plateau exclusion.

## Profile stress

`experiments/tpc240_profile_stress.py` uses two fixed profiles of the form

```text
psi(t)=raw(t)/int raw,
raw(t)=exp(-1/(1-t^2))*shape(t) for |t|<1,
```

with positive smooth shape factors.  Composite Simpson quadrature only
approximates the normalization and `kappa_psi` for the finite test.  The exact
mathematical profiles are defined by their exact integrals.  The program checks
nonnegativity, the bound by one, fixed-q residue injectivity, direct/row energy
equality, and improving Riemann error over increasing prime fixtures.

## Required commands

```bash
python -B code/tpc240_top_prime_energy_certificate.py --check
python -O -B code/tpc240_top_prime_energy_certificate.py --check
python -B experiments/tpc240_independent_checker.py --check
python -O -B experiments/tpc240_independent_checker.py --check
python -B experiments/tpc240_profile_stress.py --check
python -O -B experiments/tpc240_profile_stress.py --check
```

Each normal/optimized pair must exit zero, emit no stderr, and have
byte-identical stdout.
